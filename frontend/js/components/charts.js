// js/components/charts.js

let commitsChartInstance = null;
let issuesChartInstance = null;

export const renderCharts = (commits, issues) => {
    const ctxCommits = document.getElementById('commitsChart');
    const ctxIssues = document.getElementById('issuesChart');

    if (!ctxCommits || !ctxIssues) return;

    // Destrói os gráficos antigos caso a pessoa clique em "Atualizar Dados"
    if (commitsChartInstance) commitsChartInstance.destroy();
    if (issuesChartInstance) issuesChartInstance.destroy();

    // 1. Agrupamento Semanal (Últimas 12 semanas = ~84 dias)
    const weeks = 12;
    const labels = [];
    const commitsData = [];
    const openIssuesData = [];
    const closedIssuesData = [];

    const today = new Date();
    today.setHours(23, 59, 59, 999);

    for (let i = weeks - 1; i >= 0; i--) {
        // Define o início e o fim da semana
        const weekEnd = new Date(today);
        weekEnd.setDate(today.getDate() - (i * 7));
        
        const weekStart = new Date(weekEnd);
        weekStart.setDate(weekEnd.getDate() - 6);
        weekStart.setHours(0, 0, 0, 0);

        // Rótulo do eixo X: "15/06 - 21/06"
        const formatData = (d) => `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`;
        labels.push(`${formatData(weekStart)}`);

        // Filtra os commits que caem dentro desta janela de 7 dias
        const weekCommits = commits.filter(c => {
            const d = new Date(c.commit.author.date);
            return d >= weekStart && d <= weekEnd;
        }).length;

        // Filtra as issues que caem dentro desta janela
        const weekOpen = issues.filter(iss => {
            const d = new Date(iss.created_at);
            return d >= weekStart && d <= weekEnd;
        }).length;

        const weekClosed = issues.filter(iss => {
            if (!iss.closed_at) return false;
            const d = new Date(iss.closed_at);
            return d >= weekStart && d <= weekEnd;
        }).length;

        commitsData.push(weekCommits);
        openIssuesData.push(weekOpen);
        closedIssuesData.push(weekClosed);
    }

    // 2. Renderiza o Gráfico de Commits (Linha Suavizada)
    commitsChartInstance = new Chart(ctxCommits, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Commits na Semana',
                data: commitsData,
                borderColor: '#22d3ee', // Cyan
                backgroundColor: 'rgba(34, 211, 238, 0.1)',
                borderWidth: 3,
                pointBackgroundColor: '#030712',
                pointBorderColor: '#22d3ee',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                fill: true,
                tension: 0.4 // Aqui está a mágica do achatamento suavizado!
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { mode: 'index', intersect: false, backgroundColor: 'rgba(15, 23, 42, 0.9)' }
            },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { precision: 0 } },
                x: { grid: { display: false } }
            }
        }
    });

    // 3. Renderiza o Gráfico de Issues (Barras)
    issuesChartInstance = new Chart(ctxIssues, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Abertas',
                    data: openIssuesData,
                    backgroundColor: 'rgba(34, 211, 238, 0.8)', // Cyan
                    borderRadius: 4
                },
                {
                    label: 'Fechadas',
                    data: closedIssuesData,
                    backgroundColor: 'rgba(71, 85, 105, 0.8)', // Slate (Cinza)
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { mode: 'index', intersect: false, backgroundColor: 'rgba(15, 23, 42, 0.9)' }
            },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { precision: 0 }, stacked: true },
                x: { grid: { display: false }, stacked: true }
            }
        }
    });
};