// js/components/userAudit.js

export const renderUserAudit = (commits, issues) => {
    const select = document.getElementById('audit-user-select');
    const logList = document.getElementById('audit-log-list');
    const badgeCommits = document.getElementById('audit-badge-commits');
    const badgeIssues = document.getElementById('audit-badge-issues');

    if (!select || !logList) return;

    //Extrair usuários únicos do JSON
    const users = new Set();
    commits.forEach(c => {
        const login = c.author?.login || c.commit.author.name;
        if (login) users.add(login);
    });
    issues.forEach(i => {
        const login = i.user?.login;
        if (login) users.add(login);
    });

    //Limpar e Popular o Select
    select.innerHTML = '<option value="all">Todos os Membros</option>';
    Array.from(users).sort().forEach(user => {
        const option = document.createElement('option');
        option.value = user;
        option.textContent = `@${user}`;
        select.appendChild(option);
    });

    //Função de Filtro e Renderização
    const updateAudit = (selectedUser) => {
        logList.innerHTML = '';

        let userCommits = commits;
        let userIssues = issues;

        // Se escolher um específico, aplica o filtro
        if (selectedUser !== 'all') {
            userCommits = commits.filter(c => (c.author?.login || c.commit.author.name) === selectedUser);
            userIssues = issues.filter(i => i.user?.login === selectedUser);
        }

        // Atualiza os selos (badges) do topo
        if (badgeCommits) badgeCommits.textContent = `${userCommits.length} Commits`;
        if (badgeIssues) badgeIssues.textContent = `${userIssues.length} Issues/PRs`;

        //Junta Commits e Issues em uma lista só e ordena por data
        const combinedLog = [
            ...userCommits.map(c => ({
                type: 'commit',
                date: new Date(c.commit.author.date),
                title: c.commit.message.split('\n')[0].replace(/"/g, '&quot;'),
                url: `https://github.com/unb-mds/2026-1-P.R.I.S.M.A/commit/${c.sha}`
            })),
            ...userIssues.map(i => ({
                type: i.pull_request ? 'pr' : 'issue',
                date: new Date(i.created_at),
                title: i.title,
                url: i.html_url,
                state: i.state
            }))
        ].sort((a, b) => b.date - a.date).slice(0, 50); // Mostra as 50 ações mais recentes

        if (combinedLog.length === 0) {
            logList.innerHTML = `<div class="placeholder-text">Nenhuma atividade recente encontrada.</div>`;
            return;
        }

        //Desenha a lista na tela
        combinedLog.forEach(item => {
            const dateStr = item.date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
            
            // Define o Ícone e a Cor com base no tipo da ação
            let icon = '⚲';
            let color = 'var(--accent-cyan)';
            let typeTitle = 'Commit';
            
            if (item.type === 'issue') { 
                icon = '!'; 
                color = item.state === 'closed' ? 'var(--accent-emerald)' : 'var(--accent-amber)';
                typeTitle = item.state === 'closed' ? 'Issue Resolvida' : 'Issue Aberta';
            }
            if (item.type === 'pr') { 
                icon = '⎇'; 
                color = '#818cf8'; // Roxo claro para Pull Requests
                typeTitle = 'Pull Request';
            }

            const row = document.createElement('div');
            row.style.cssText = `display: flex; gap: 12px; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.05); align-items: center;`;
            
            row.innerHTML = `
                <div style="color: ${color}; font-weight: 900; font-size: 1.2rem; min-width: 20px; text-align: center;" title="${typeTitle}">${icon}</div>
                <div style="flex: 1; min-width: 0;">
                    <a href="${item.url}" target="_blank" style="color: var(--text-light); text-decoration: none; font-size: 0.8rem; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; transition: color 0.2s;" onmouseover="this.style.color='${color}'" onmouseout="this.style.color='var(--text-light)'">
                        ${item.title}
                    </a>
                </div>
                <div style="font-family: var(--font-mono); font-size: 0.65rem; color: var(--text-muted);">${dateStr}</div>
            `;
            logList.appendChild(row);
        });
    };

    // Garante que o evento de filtro funcione toda vez que você trocar o usuário
    select.onchange = (e) => updateAudit(e.target.value);
    
    // Inicia mostrando os dados de todo mundo
    updateAudit('all');
};