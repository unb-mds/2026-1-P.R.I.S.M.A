// js/app.js
import { renderCharts } from './components/charts.js';
import { renderHeatmap } from './components/heatmap.js';
import { initTimeline } from './components/timeline.js';
import { renderCommitLog } from './components/commitlog.js';
import { renderCollaborators } from './components/collaborators.js';
import { renderUserAudit } from './components/useraudit.js';

export const PrismaApp = {

    // Orquestra a busca e o cálculo dos dados
    async sync() {
        try {
            const response = await fetch('dados.json');
            if (!response.ok) throw new Error("Arquivo não encontrado.");
            const data = await response.json();
            
            const allCommits = data.raw_commits || [];
            const issues = data.raw_issues || [];
            
            // Exibe a data real da geração no card correspondente
            const timestampElement = document.getElementById('build-timestamp');
            if (timestampElement) {
                timestampElement.textContent = data.generated_at || "--/-- --:--";
            }

            const closedIssues = issues.filter(issue => issue.state === 'closed').length;
            
            // Consolidação precisa de colaboradores baseada no login único do GitHub
            const collaborators = new Set(
                allCommits
                    .filter(c => c.author && c.author.login)
                    .map(c => c.author.login)
            ).size;

            const metrics = {
                total_commits: allCommits.length, 
                closed_issues: closedIssues, // Repassando a métrica correta
                active_collaborators: collaborators,
                raw_commits: allCommits, 
                raw_issues: issues
            };

            this.updateDashboard(metrics);
            return metrics;
            
        } catch (error) {
            console.error("Erro ao carregar dados locais:", error);
        }
    },

    // Injeta os dados calculados no HTML e chama os componentes
    updateDashboard(data) {
        //Atualiza os Cards Numéricos Superiores
        const elements = {
            commits: document.getElementById('total-commits'),
            issues: document.getElementById('closed-issues'), // Atualizado para o novo ID do HTML
            collabs: document.getElementById('total-collabs')
        };

        if (elements.commits) elements.commits.textContent = data.total_commits;
        if (elements.issues) elements.issues.textContent = data.closed_issues;
        if (elements.collabs) elements.collabs.textContent = data.active_collaborators;

        //Chama a renderização de todos os módulos visuais que criamos
        if (typeof renderCharts === 'function') renderCharts(data.raw_commits, data.raw_issues);
        if (typeof renderHeatmap === 'function') renderHeatmap(data.raw_commits, data.raw_issues);
        if (typeof initTimeline === 'function') initTimeline(data.raw_commits, data.raw_issues);
        if (typeof renderCommitLog === 'function') renderCommitLog(data.raw_commits);
        if (typeof renderCollaborators === 'function') renderCollaborators(data.raw_commits, data.raw_issues);
        if (typeof renderUserAudit === 'function') renderUserAudit(data.raw_commits, data.raw_issues);
    }
};