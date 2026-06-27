// js/components/commitlog.js

const formatDate = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleDateString('pt-BR', { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric' 
    });
};

export const renderCommitLog = (commitsArray) => {
    const container = document.getElementById('commit-log-container');
    
    if (!container) return;
    container.innerHTML = '';

    const recentCommits = commitsArray.slice(0, 50);

    recentCommits.forEach(item => {
        const sha = item.sha.substring(0, 7);
        const msg = item.commit.message.split('\n')[0].replace(/"/g, '&quot;');
        
        // MUDANÇA: Prioriza o @login do GitHub. Se for um bot sem login, usa o nome de fallback.
        const author = item.author?.login ? `@${item.author.login}` : item.commit.author.name;
        
        const date = formatDate(item.commit.author.date);
        
        const diffUrl = `https://github.com/unb-mds/2026-1-P.R.I.S.M.A/commit/${item.sha}`;

        const row = document.createElement('div');
        row.className = 'commit-row';

        row.innerHTML = `
            <div class="commit-sha">
                <a href="${diffUrl}" target="_blank" style="color: var(--text-cyan); text-decoration: none;" title="Ver detalhes no GitHub">
                    #${sha} ↗
                </a>
            </div>
            <div class="commit-info">
                <div class="commit-msg" title="${msg}">${msg}</div>
                <div class="commit-author" style="color: var(--text-muted); font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;">${author}</div>
            </div>
            <div class="commit-date">${date}</div>
        `;

        container.appendChild(row);
    });
};