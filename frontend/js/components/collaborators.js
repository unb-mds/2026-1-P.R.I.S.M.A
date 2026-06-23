// js/components/collaborators.js

export const renderCollaborators = (commits, issues) => {
    const container = document.getElementById('collaborators-grid');
    if (!container) return;

    // Objeto para agrupar as estatísticas por usuário
    const users = {};

    // 1. Varre os Commits
    commits.forEach(c => {
        const email = c.commit.author.email;
        const login = c.author?.login || email.split('@')[0];
        const name = c.commit.author.name;
        // Se a pessoa não tiver foto no Git, gera uma imagem com as iniciais dela
        const avatar = c.author?.avatar_url || `https://ui-avatars.com/api/?name=${name}&background=1e293b&color=22d3ee`;

        if (!users[login]) {
            users[login] = { 
                name, login, avatar, 
                commits: 0, closedIssues: 0, prs: 0, 
                lastMsg: c.commit.message 
            };
        }
        users[login].commits++;
    });

    // 2. Varre as Issues (Para contar Issues fechadas e PRs)
    issues.forEach(i => {
        const login = i.user?.login;
        if (!login || !users[login]) return;

        // Se a issue tiver o objeto 'pull_request', é um PR
        if (i.pull_request) {
            users[login].prs++;
        } 
        // Conta quantas issues a pessoa tem listada como "fechada"
        else if (i.state === 'closed') {
            users[login].closedIssues++;
        }
    });

    // Ordena do que tem mais commits pro que tem menos
    const sortedUsers = Object.values(users).sort((a, b) => b.commits - a.commits);

    // Limpa o estado de "Aguardando sincronização..."
    container.innerHTML = '';

    // Renderiza cada card HTML
    sortedUsers.forEach(u => {
        const card = document.createElement('div');
        card.className = 'collab-card';
        card.innerHTML = `
            <div class="collab-header">
                <img src="${u.avatar}" alt="${u.name}" class="collab-avatar">
                <div class="collab-info">
                    <h4>${u.name}</h4>
                    <span>@${u.login}</span>
                </div>
            </div>
            <div class="collab-stats">
                <div class="c-stat-box">
                    <span class="c-stat-label">Commits</span>
                    <span class="c-stat-val text-cyan">${u.commits}</span>
                </div>
                <div class="c-stat-box">
                    <span class="c-stat-label">Demandas</span>
                    <span class="c-stat-val text-amber" title="Issues Fechadas">${u.closedIssues}</span>
                </div>
                <div class="c-stat-box">
                    <span class="c-stat-label">PRs</span>
                    <span class="c-stat-val text-emerald" title="Pull Requests">${u.prs}</span>
                </div>
            </div>
            <div class="collab-footer">
                <span class="c-footer-label">Último Despacho</span>
                <div class="c-footer-msg" title="${u.lastMsg}">"${u.lastMsg.split('\n')[0].replace(/"/g, '&quot;')}"</div>
            </div>
        `;
        container.appendChild(card);
    });
};