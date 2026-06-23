// js/main.js
import { PrismaApp } from './app.js';

document.addEventListener('DOMContentLoaded', () => {
    // --- 1. Seleção de Elementos ---
    const views = {
        landing: document.getElementById('landing-view'),
        dashboard: document.getElementById('dashboard-view')
    };
    
    const btns = {
        enterNav: document.getElementById('btn-enter-dashboard'),
        enterHero: document.getElementById('btn-hero-dashboard'),
        backHome: document.getElementById('btn-back-home'),
        sync: document.getElementById('btn-sync') // Agora serve apenas para recarregar o gráfico
    };

    // --- 2. Lógica de Navegação (Transição de Telas) ---
    const toggleView = (viewToHide, viewToShow) => {
        viewToHide.classList.remove('active');
        setTimeout(() => {
            viewToHide.classList.add('hidden');
            viewToShow.classList.remove('hidden');
            setTimeout(() => viewToShow.classList.add('active'), 50);
        }, 400); // 400ms sincronizado com a transição CSS
    };

    btns.enterNav.addEventListener('click', () => toggleView(views.landing, views.dashboard));
    btns.enterHero.addEventListener('click', () => toggleView(views.landing, views.dashboard));
    btns.backHome.addEventListener('click', () => toggleView(views.dashboard, views.landing));

    // --- 3. Carregamento Automático (Motor JAMstack) ---
    const loadData = async () => {
        if (btns.sync) {
            btns.sync.textContent = 'Carregando...';
            btns.sync.disabled = true;
            btns.sync.style.opacity = '0.7';
        }

        try {
            // Executa a carga dos dados locais (dados.json) sem precisar de token
            await PrismaApp.sync();
            console.log("Sincronização com o pacote de dados estático concluída.");
        } catch (error) {
            console.error('Erro no fluxo de dados:', error);
        } finally {
            if (btns.sync) {
                btns.sync.textContent = 'Atualizar Dados';
                btns.sync.disabled = false;
                btns.sync.style.opacity = '1';
            }
        }
    };

    // Inicia a busca dos dados automaticamente assim que a página carrega em background
    loadData();

    // Se o usuário clicar em atualizar, refaz a leitura do JSON
    if (btns.sync) {
        btns.sync.addEventListener('click', loadData);
    }

    console.log("🚀 PRISMA Interface JAMstack inicializada.");
});