// js/components/charts.js

// Guardamos as instâncias para poder destruí-las antes de atualizar (evita sobreposição)
let commitsChart = null;
let issuesChart = null;

// Função utilitária para gerar array dos últimos 30 dias no formato YYYY-MM-DD
const getLast30Days = () => {
  const dates = [];
  for (let i = 29; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    dates.push(d.toISOString().split("T")[0]);
  }
  return dates;
};

// Converte YYYY-MM-DD para DD/MM para o eixo X do gráfico
const formatLabel = (dateString) => {
  const [year, month, day] = dateString.split("-");
  return `${day}/${month}`;
};

export const renderCharts = (commits, issues) => {
  const last30Days = getLast30Days();
  const labels = last30Days.map(formatLabel);

  // --- 1. Agrupando Dados de Commits ---
  const commitsData = last30Days.map((date) => {
    return commits.filter((c) => c.commit.author.date.startsWith(date)).length;
  });

  // --- 2. Agrupando Dados de Issues ---
  const issuesOpenedData = last30Days.map((date) => {
    return issues.filter((i) => i.created_at.startsWith(date)).length;
  });

  const issuesClosedData = last30Days.map((date) => {
    return issues.filter((i) => i.closed_at && i.closed_at.startsWith(date))
      .length;
  });

  // Configurações Globais Visuais do Chart.js para o tema escuro
  Chart.defaults.color = "#94a3b8";
  Chart.defaults.font.family = "'JetBrains Mono', monospace";

  // --- 3. Renderizando Gráfico de Linha (Commits) ---
  const ctxCommits = document.getElementById("commitsChart").getContext("2d");
  if (commitsChart) commitsChart.destroy(); // Destrói o anterior se existir

  commitsChart = new Chart(ctxCommits, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Entregas (Commits)",
          data: commitsData,
          borderColor: "#22d3ee", // Cyan
          backgroundColor: "rgba(34, 211, 238, 0.1)",
          borderWidth: 3,
          pointBackgroundColor: "#0f172a",
          pointBorderColor: "#22d3ee",
          pointBorderWidth: 2,
          pointRadius: 4,
          tension: 0.4, // Suaviza a linha
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: "#334155", tickColor: "transparent" },
          border: { display: false },
        },
        x: { grid: { display: false }, border: { display: false } },
      },
      plugins: { legend: { display: false } }, // Escondemos a legenda para ficar minimalista
    },
  });

  // --- 4. Renderizando Gráfico de Barras (Issues) ---
  const ctxIssues = document.getElementById("issuesChart").getContext("2d");
  if (issuesChart) issuesChart.destroy();

  issuesChart = new Chart(ctxIssues, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Abertas",
          data: issuesOpenedData,
          backgroundColor: "#0891b2", // Cyan escuro
          borderRadius: 4,
        },
        {
          label: "Fechadas",
          data: issuesClosedData,
          backgroundColor: "#334155", // Slate
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: "#334155", tickColor: "transparent" },
          border: { display: false },
          stacked: true,
        },
        x: {
          grid: { display: false },
          border: { display: false },
          stacked: true,
        },
      },
      plugins: {
        legend: {
          position: "top",
          align: "end",
          labels: { boxWidth: 10, usePointStyle: true },
        },
      },
    },
  });
};
