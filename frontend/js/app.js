// js/app.js
import { renderCharts } from './components/charts.js';
import { renderHeatmap } from './components/heatmap.js';
import { initTimeline } from './components/timeline.js';
import { renderCommitLog } from './components/commitlog.js';
import { renderCollaborators } from './components/collaborators.js';

const OWNER = 'unb-mds';
const REPO = '2026-1-P.R.I.S.M.A';
const GH_API_BASE = 'https://api.github.com/repos';

export const PrismaApp = {
    // Função genérica para bater na API do GitHub
    async fetchFromGitHub(endpoint, token) {
        const headers = {
            'Accept': 'application/vnd.github.v3+json'
        };
        
        // Se o visitante inserir o token, injetamos no header para evitar Rate Limit
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${GH_API_BASE}/${OWNER}/${REPO}/${endpoint}`, { headers });
        
        if (!response.ok) {
            // Tratamento específico de limite de requisições do GitHub (Rate Limit)
            if (response.status === 403) {
                throw new Error("Limite da API do GitHub excedido. Insira um Token para continuar.");
            }
            const error = await response.json().catch(() => ({}));
            throw new Error(error.message || `Erro HTTP: ${response.status}`);
        }
        
        return response.json();
    },

    // Orquestra a busca e o cálculo dos dados
    async sync(token) {
        // 1. Puxa TODAS as branches usando paginação (remove a limitação de 30 branches)
        const branches = await this.fetchAllPages('branches', token);
        
        let allCommitsRaw = [];
        for (const branch of branches) {
            // 2. Busca os commits resolvendo o bug do '#'
            const branchCommits = await this.fetchAllPages(`commits?sha=${encodeURIComponent(branch.name)}`, token);
            allCommitsRaw = allCommitsRaw.concat(branchCommits);
        }

        // 3. Remove duplicatas baseadas no hash único do commit
        const uniqueCommitsMap = new Map();
        allCommitsRaw.forEach(commit => {
            if (commit && commit.sha) {
                uniqueCommitsMap.set(commit.sha, commit);
            }
        });
        
        const allCommits = Array.from(uniqueCommitsMap.values()).sort((a, b) => 
            new Date(b.commit.author.date) - new Date(a.commit.author.date)
        );

        const issues = await this.fetchAllPages('issues?state=all', token);
        const openIssues = issues.filter(issue => issue.state === 'open').length;
        
        const collaborators = new Set(
            allCommits
                .filter(c => c.commit && c.commit.author)
                .map(c => c.commit.author.email)
        ).size;

        const metrics = {
            total_commits: allCommits.length, 
            open_issues: openIssues,
            active_collaborators: collaborators,
            raw_commits: allCommits, 
            raw_issues: issues
        };

        this.updateDashboard(metrics);
        return metrics;
    },

    async fetchAllPages(endpoint, token) {
        let allData = [];
        let page = 1;
        let hasMore = true;

        while (hasMore) {
            const separator = endpoint.includes('?') ? '&' : '?';
            const url = `${endpoint}${separator}per_page=100&page=${page}`;
            
            const data = await this.fetchFromGitHub(url, token);
            
            // Verifica se a API retornou um array válido
            if (Array.isArray(data) && data.length > 0) {
                allData = allData.concat(data);
                
                if (data.length < 100) {
                    hasMore = false;
                } else {
                    page++;
                }
            } else {
                hasMore = false; 
            }
            
            if (page > 50) hasMore = false; 
        }
        return allData;
    },
    // Injeta os dados calculados no HTML e chama os componentes
    updateDashboard(data) {
        // 1. Atualiza os Cards Numéricos Superiores
        const elements = {
            commits: document.getElementById('total-commits'),
            issues: document.getElementById('open-issues'),
            collabs: document.getElementById('total-collabs')
        };

        if (elements.commits) elements.commits.textContent = data.total_commits;
        if (elements.issues) elements.issues.textContent = data.open_issues;
        if (elements.collabs) elements.collabs.textContent = data.active_collaborators;

        // 2. Chama a renderização de todos os módulos visuais que criamos
        if (typeof renderCharts === 'function') renderCharts(data.raw_commits, data.raw_issues);
        if (typeof renderHeatmap === 'function') renderHeatmap(data.raw_commits, data.raw_issues);
        if (typeof initTimeline === 'function') initTimeline(data.raw_commits, data.raw_issues);
        if (typeof renderCommitLog === 'function') renderCommitLog(data.raw_commits);
        if (typeof renderCollaborators === 'function') renderCollaborators(data.raw_commits, data.raw_issues);
    }
};