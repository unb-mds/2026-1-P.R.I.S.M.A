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
        sync: document.getElementById('btn-sync')
    };
    
    const inputs = {
        token: document.getElementById('gh-token')
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

    // --- 3. Gerenciamento do Token ---
    const savedToken = localStorage.getItem('gh_token');
    if (savedToken) inputs.token.value = savedToken;

    inputs.token.addEventListener('change', (e) => {
        const val = e.target.value.trim();
        if (val) localStorage.setItem('gh_token', val);
        else localStorage.removeItem('gh_token');
    });

    // --- 4. Ação de Sincronização (Conecta com app.js) ---
    btns.sync.addEventListener('click', async () => {
        const token = inputs.token.value.trim();
        
        if (!token) {
            alert('Por favor, insira o Token de Acesso do GitHub para conectar ao motor PRISMA.');
            return;
        }

        // Feedback Visual de Loading
        btns.sync.textContent = 'Sincronizando...';
        btns.sync.disabled = true;
        btns.sync.style.opacity = '0.7';

        try {
            // Executa a lógica central da aplicação
            await PrismaApp.sync(token);
            console.log("Sincronização com o motor backend concluída.");
        } catch (error) {
            console.error('Erro no fluxo de dados:', error);
            alert(`Erro: ${error.message}`);
        } finally {
            // Restaura o botão
            btns.sync.textContent = 'Sincronizar';
            btns.sync.disabled = false;
            btns.sync.style.opacity = '1';
        }
    });

    console.log("🚀 PRISMA Interface inicializada.");
});