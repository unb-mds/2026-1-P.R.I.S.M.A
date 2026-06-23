let currentWeekOffset = 0;
let globalCommits = [];
let globalIssues = [];

// Calcula o Domingo e o Sábado de uma semana específica
const getWeekBoundaries = (offset) => {
    const now = new Date();
    const currentDay = now.getDay(); // 0 = Domingo
    const start = new Date(now);
    start.setDate(now.getDate() - currentDay - (offset * 7));
    start.setHours(0,0,0,0);
    
    const end = new Date(start);
    end.setDate(start.getDate() + 6);
    end.setHours(23,59,59,999);
    
    return { start, end };
};

const formatDateDayMonth = (date) => {
    const d = date.getDate().toString().padStart(2, '0');
    const m = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'][date.getMonth()];
    return `${d} ${m}`;
};

export const initTimeline = (commits, issues) => {
    globalCommits = commits;
    globalIssues = issues;
    
    document.getElementById('btn-prev-week').addEventListener('click', () => {
        currentWeekOffset++;
        renderCurrentWeek();
    });
    
    document.getElementById('btn-next-week').addEventListener('click', () => {
        if (currentWeekOffset > 0) {
            currentWeekOffset--;
            renderCurrentWeek();
        }
    });

    renderCurrentWeek();
};

const renderCurrentWeek = () => {
    const boundaries = getWeekBoundaries(currentWeekOffset);
    
    // Atualiza o Rótulo "21 JUN - 27 JUN"
    document.getElementById('current-week-label').textContent = 
        `${formatDateDayMonth(boundaries.start)} - ${formatDateDayMonth(boundaries.end)}`;
    
    // Habilita/Desabilita botão de avançar
    document.getElementById('btn-next-week').disabled = currentWeekOffset === 0;

    // Filtra dados da semana
    const weekCommits = globalCommits.filter(c => {
        const d = new Date(c.commit.author.date);
        return d >= boundaries.start && d <= boundaries.end;
    });

    const weekIssues = globalIssues.filter(i => {
        const d = new Date(i.created_at);
        return d >= boundaries.start && d <= boundaries.end;
    });

    // Atualiza Cards Numéricos
    document.getElementById('week-commits-count').textContent = weekCommits.length;
    document.getElementById('week-issues-count').textContent = weekIssues.length;

    // Renderiza a lista de logs visuais (mockup)
    const listContainer = document.getElementById('weekly-logs-list');
    if (weekCommits.length === 0 && weekIssues.length === 0) {
        listContainer.innerHTML = '<div class="placeholder-text" style="padding-top: 20px; font-style: italic; font-size: 0.7rem; color: #94a3b8;">Silêncio no repositório nesta semana.</div>';
    } else {
        listContainer.innerHTML = '<div class="placeholder-text" style="padding-top: 20px; font-size: 0.7rem; color: #22d3ee;">Atividade detectada. (Logs renderizados aqui)</div>';
    }
};