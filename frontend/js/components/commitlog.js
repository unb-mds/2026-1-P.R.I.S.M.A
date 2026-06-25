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
    const badge = document.getElementById('commit-count-badge');
    
    if (!container) return;

    if (badge) badge.textContent = `${commitsArray.length} Registros`;
    container.innerHTML = '';

    const recentCommits = commitsArray.slice(0, 50);

    recentCommits.forEach(item => {
        const sha = item.sha.substring(0, 7);
        const msg = item.commit.message.split('\n')[0].replace(/"/g, '&quot;');
        const author = item.commit.author.name;
        const date = formatDate(item.commit.author.date);
        
        // Constrói a URL exata do diff no repositório da disciplina
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
                <div class="commit-author">${author}</div>
            </div>
            <div class="commit-date">${date}</div>
        `;

        container.appendChild(row);
    });
};