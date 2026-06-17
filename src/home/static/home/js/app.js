document.addEventListener("DOMContentLoaded", async () => {
    const basePath = window.location.pathname.includes('/pages/') ? '../../' : './';
    
    async function loadComponent(id, url) {
        const el = document.getElementById(id);
        if (el) {
            try {
                const res = await fetch(basePath + url);
                if (res.ok) el.innerHTML = await res.text();
            } catch (e) {
                console.error(`Erro ao carregar componente: ${url}`, e);
            }
        }
    }

    await loadComponent('sidebar-container', 'components/sidebar.html');
    await loadComponent('header-container', 'components/header.html');

    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(link => {
        if (currentPath.includes(link.getAttribute('href'))) {
            link.classList.add('bg-white/5', 'text-white', 'border-brand-primary');
            link.classList.remove('text-slate-300', 'border-transparent');
        }
    });

    lucide.createIcons();
});