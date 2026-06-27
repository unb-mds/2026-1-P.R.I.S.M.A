// js/main.js
import { PrismaApp } from './app.js';

document.addEventListener('DOMContentLoaded', () => {
    
    // Verifica se estamos na página inicial ou no dashboard
    const syncBtn = document.getElementById('btn-sync');
    const dashboardView = document.getElementById('dashboard-view');
    
    if (!syncBtn && !dashboardView) {
        console.log("📍 Página Inicial Carregada. Sem necessidade de puxar dados.");
        return; // Interrompe a execução do JS aqui
    }

    // --- LÓGICA DO DASHBOARD ---
    const loadData = async () => {
        if (syncBtn) {
            syncBtn.textContent = 'Carregando...';
            syncBtn.disabled = true;
            syncBtn.style.opacity = '0.7';
        }

        try {
            await PrismaApp.sync();
            console.log("✅ Sincronização com o pacote de dados estático concluída.");
        } catch (error) {
            console.error('❌ Erro no fluxo de dados:', error);
        } finally {
            if (syncBtn) {
                syncBtn.textContent = 'Atualizar Dados';
                syncBtn.disabled = false;
                syncBtn.style.opacity = '1';
            }
        }
    };

    // Inicia a busca dos dados automaticamente assim que o dashboard carrega
    loadData();

    if (syncBtn) {
        syncBtn.addEventListener('click', loadData);
    }

    console.log("🚀 PRISMA Dashboard JAMstack inicializado.");
});