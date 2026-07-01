/**
 * ============================================
 * PRISMA Enhanced Navbar System
 * ============================================
 * Sistema interativo e visual para a barra
 * de navegação superior
 */

class NavbarEnhancer {
  constructor() {
    this.navbar =
      document.querySelector(".navbar") || document.querySelector(".top-nav");
    this.links = document.querySelectorAll(".navbar-links a, .top-nav a");
    this.currentPath = window.location.pathname;

    if (this.navbar) {
      this.init();
    }
  }

  init() {
    this.addNavbarStyles();
    this.setupHoverEffects();
    this.highlightCurrentPage();
  }

  addNavbarStyles() {
    const style = document.createElement("style");
    style.textContent = `
            /* Enhanced Navbar Styles */
            .navbar-links a, .top-nav a {
                position: relative;
                overflow: hidden;
            }

            /* Underline animado ao hover */
            .navbar-links a::before,
            .top-nav a:not([href="index.html"]):not([href="dashboard.html"]):not([href*=".html"])::before {
                content: '';
                position: absolute;
                bottom: -2px;
                left: 0;
                width: 0;
                height: 2px;
                background: linear-gradient(90deg, currentColor, transparent);
                transition: width 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            }

            .navbar-links a:hover::before,
            .top-nav a:hover::before {
                width: 100%;
            }

            /* Underline para link ativo */
            .navbar-links a.active::before,
            .top-nav a.active::before {
                width: 100%;
                background: linear-gradient(90deg, currentColor, transparent);
                opacity: 0.8;
            }

            /* Glow effect ao hover */
            .navbar-links a:hover,
            .top-nav a:not([href="index.html"]):not([href="dashboard.html"]):hover {
                text-shadow: 0 0 10px currentColor, 0 0 20px rgba(34, 211, 238, 0.3);
            }

            /* Animação de entrada da navbar */
            .navbar, .top-nav {
                animation: slideDown 0.6s ease-out;
            }

            @keyframes slideDown {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            /* Indicador com pulso */
            .nav-active-indicator {
                display: inline-block;
                width: 8px;
                height: 8px;
                background: currentColor;
                border-radius: 50%;
                margin-left: 8px;
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0%, 100% { opacity: 0.6; transform: scale(1); }
                50% { opacity: 1; transform: scale(1.2); }
            }

            /* Ripple effect ao clicar */
            @keyframes rippleEffect {
                0% { transform: scale(0); opacity: 0.6; }
                100% { transform: scale(2); opacity: 0; }
            }

            /* Responsive */
            @media (max-width: 768px) {
                .navbar-links {
                    gap: 1rem;
                    font-size: 0.85rem;
                }
            }
        `;
    document.head.appendChild(style);
  }

  setupHoverEffects() {
    this.links.forEach((link) => {
      link.addEventListener("mouseenter", (e) => {
        this.createRipple(e, link);
      });

      link.addEventListener("click", () => {
        this.updateActiveLink(link);
      });
    });
  }

  createRipple(e, link) {
    const ripple = document.createElement("span");
    ripple.style.cssText = `
            position: absolute;
            background: radial-gradient(circle, currentColor, transparent);
            border-radius: 50%;
            transform: scale(0);
            animation: rippleEffect 0.6s ease-out;
            pointer-events: none;
        `;

    link.style.position = "relative";
    link.style.overflow = "hidden";
    link.appendChild(ripple);

    setTimeout(() => ripple.remove(), 600);
  }

  highlightCurrentPage() {
    const fileName = this.currentPath.split("/").pop() || "index.html";

    this.links.forEach((link) => {
      const href = link.getAttribute("href") || "";

      if (
        (fileName === "" && href === "index.html") ||
        (fileName && href.includes(fileName.replace(".html", "")))
      ) {
        link.classList.add("active");

        // Adiciona indicador visual
        if (!link.querySelector(".nav-active-indicator")) {
          const indicator = document.createElement("span");
          indicator.className = "nav-active-indicator";
          link.appendChild(indicator);
        }
      }
    });
  }

  updateActiveLink(clickedLink) {
    // Remove active de todos os links
    this.links.forEach((link) => {
      link.classList.remove("active");
      const indicator = link.querySelector(".nav-active-indicator");
      if (indicator) indicator.remove();
    });

    // Adiciona active ao link clicado
    clickedLink.classList.add("active");

    // Adiciona indicador
    if (!clickedLink.querySelector(".nav-active-indicator")) {
      const indicator = document.createElement("span");
      indicator.className = "nav-active-indicator";
      clickedLink.appendChild(indicator);
    }

    // Efeito de feedback
    this.flashLink(clickedLink);
  }

  flashLink(link) {
    link.style.transition = "all 0.3s ease";
    link.style.transform = "scale(1.05)";

    setTimeout(() => {
      link.style.transform = "scale(1)";
    }, 300);
  }
}

// ==========================================
// INICIALIZAÇÃO
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
  new NavbarEnhancer();
});
