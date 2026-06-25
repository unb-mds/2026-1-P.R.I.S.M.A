// js/components/heatmap.js

export const renderHeatmap = (commits, issues) => {
    const grid = document.getElementById('heatmap-grid');
    if (!grid) return;
    
    grid.innerHTML = '';
    const today = new Date();
    today.setHours(0,0,0,0);

    for (let i = 89; i >= 0; i--) {
        const targetDate = new Date(today);
        targetDate.setDate(today.getDate() - i);
        const dateStr = targetDate.toISOString().split('T')[0];

        //Formata a data bonitinha para o tooltip aparecer como "25/06/2026"
        const dataFormatada = targetDate.toLocaleDateString('pt-BR');

        //Conta atividades no dia específico (Commits + Issues Abertas + Issues Fechadas)
        const dayCommits = commits.filter(c => c.commit.author.date.startsWith(dateStr)).length;
        const dayIssuesOpen = issues.filter(issue => issue.created_at && issue.created_at.startsWith(dateStr)).length;
        const dayIssuesClosed = issues.filter(issue => issue.closed_at && issue.closed_at.startsWith(dateStr)).length;
        
        const totalActivity = dayCommits + dayIssuesOpen + dayIssuesClosed;

        //Define o nível da cor (0 a 4) PRIMEIRO
        let lvl = 0;
        if (totalActivity > 0) lvl = 1;
        if (totalActivity >= 3) lvl = 2;
        if (totalActivity >= 6) lvl = 3;
        if (totalActivity >= 10) lvl = 4;
        
        //Cria a caixa aplicando as variáveis que agora estão corretas
        const box = document.createElement('div');
        box.className = `heat-box lvl-${lvl}`;
        box.title = `Dia: ${dataFormatada} | Atividades: ${totalActivity}`; 
        
        grid.appendChild(box);
    }
};