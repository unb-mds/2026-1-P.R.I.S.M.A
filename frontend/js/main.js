/**
 * PRISMA Insight - Main Application
 * Arquitetura: Singleton + Observer Pattern
 * Nível: Apple-grade UX/UI
 */

import { PrismaApp } from "./app.js";

// ============================================================
// CONSTANTES E CONFIGURAÇÕES
// ============================================================
const CONFIG = {
  TRANSITION_DURATION: 400, // ms
  RETRY_DELAY: 2000, // ms
  MAX_RETRIES: 3,
  DEBOUNCE_DELAY: 300, // ms
};

const SELECTORS = {
  views: {
    landing: "#landing-view",
    dashboard: "#dashboard-view",
  },
  buttons: {
    enterNav: "#btn-enter-dashboard",
    enterHero: "#btn-hero-dashboard",
    backHome: "#btn-back-home",
    sync: "#btn-sync",
    prevWeek: "#btn-prev-week",
    nextWeek: "#btn-next-week",
  },
  indicators: {
    commits: "#total-commits",
    issues: "#closed-issues",
    collabs: "#total-collabs",
    timestamp: "#build-timestamp",
  },
};

// ============================================================
// DOM CACHE (Performance)
// ============================================================
const $ = (selector, context = document) => context.querySelector(selector);
const $$ = (selector, context = document) => [
  ...context.querySelectorAll(selector),
];

const dom = {
  views: {
    landing: $(SELECTORS.views.landing),
    dashboard: $(SELECTORS.views.dashboard),
  },
  buttons: {
    enterNav: $(SELECTORS.buttons.enterNav),
    enterHero: $(SELECTORS.buttons.enterHero),
    backHome: $(SELECTORS.buttons.backHome),
    sync: $(SELECTORS.buttons.sync),
    prevWeek: $(SELECTORS.buttons.prevWeek),
    nextWeek: $(SELECTORS.buttons.nextWeek),
  },
  indicators: {
    commits: $(SELECTORS.indicators.commits),
    issues: $(SELECTORS.indicators.issues),
    collabs: $(SELECTORS.indicators.collabs),
    timestamp: $(SELECTORS.indicators.timestamp),
  },
};

// ============================================================
// STATE MANAGEMENT (Observer Pattern)
// ============================================================
class AppState {
  constructor() {
    this._data = {
      commits: [],
      issues: [],
      isLoading: false,
      error: null,
      weekOffset: 0,
    };
    this._listeners = [];
  }

  subscribe(listener) {
    this._listeners.push(listener);
    return () => {
      this._listeners = this._listeners.filter((l) => l !== listener);
    };
  }

  setState(newState) {
    this._data = { ...this._data, ...newState };
    this._notify();
  }

  getState() {
    return { ...this._data };
  }

  _notify() {
    this._listeners.forEach((listener) => {
      try {
        listener(this._data);
      } catch (error) {
        console.error("[AppState] Listener error:", error);
      }
    });
  }
}

// ============================================================
// VIEW TRANSITION (Apple-like)
// ============================================================
function transitionTo(viewToShow, viewToHide) {
  return new Promise((resolve) => {
    viewToHide.classList.remove("is-active");
    viewToHide.classList.add("is-hidden");

    requestAnimationFrame(() => {
      viewToShow.classList.remove("is-hidden");
      void viewToShow.offsetHeight;
      viewToShow.classList.add("is-active");

      setTimeout(resolve, CONFIG.TRANSITION_DURATION);
    });
  });
}

// ============================================================
// DATA LOADING (with retry)
// ============================================================
async function loadDataWithRetry(retries = CONFIG.MAX_RETRIES) {
  let lastError = null;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      await PrismaApp.sync();
      state.setState({ isLoading: false, error: null });
      return;
    } catch (error) {
      lastError = error;
      console.warn(
        `[Load] Attempt ${attempt}/${retries} failed:`,
        error.message,
      );

      if (attempt < retries) {
        await new Promise((resolve) =>
          setTimeout(resolve, CONFIG.RETRY_DELAY * attempt),
        );
      }
    }
  }

  state.setState({ isLoading: false, error: lastError });
  showErrorFallback(lastError);
}

// ============================================================
// ERROR HANDLING (User-friendly)
// ============================================================
function showErrorFallback(error) {
  const placeholders = document.querySelectorAll(".placeholder-text");
  placeholders.forEach((el) => {
    if (
      el.textContent.includes("Carregando") ||
      el.textContent.includes("Nenhum")
    ) {
      el.textContent =
        "⚠️ Não foi possível carregar os dados. Tente novamente.";
      el.style.color = "#f59e0b";
    }
  });
}

// ============================================================
// UI FEEDBACK (Apple-style)
// ============================================================
function setButtonLoading(button, isLoading) {
  if (!button) return;

  if (isLoading) {
    button.dataset.originalText = button.textContent;
    button.textContent = "Carregando…";
    button.disabled = true;
    button.style.opacity = "0.7";
  } else {
    button.textContent = button.dataset.originalText || "Atualizar Dados";
    button.disabled = false;
    button.style.opacity = "1";
  }
}

// ============================================================
// DEBOUNCE UTILITY
// ============================================================
function debounce(fn, delay = CONFIG.DEBOUNCE_DELAY) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// ============================================================
// MAIN APPLICATION
// ============================================================
const state = new AppState();

state.subscribe((data) => {
  if (data.commits && data.issues) {
    updateMetrics(data);
  }
});

async function handleLoadData() {
  if (state._data.isLoading) return;

  state.setState({ isLoading: true });
  setButtonLoading(dom.buttons.sync, true);

  try {
    await loadDataWithRetry();
  } finally {
    state.setState({ isLoading: false });
    setButtonLoading(dom.buttons.sync, false);
  }
}

function updateMetrics(data) {
  const commits = data.commits || [];
  const issues = data.issues || [];

  const totalCommits = commits.length;
  const closedIssues = issues.filter((i) => i.state === "closed").length;
  const collaborators = new Set(
    commits.filter((c) => c.author?.login).map((c) => c.author.login),
  ).size;

  animateCounter(dom.indicators.commits, totalCommits);
  animateCounter(dom.indicators.issues, closedIssues);
  animateCounter(dom.indicators.collabs, collaborators);

  if (dom.indicators.timestamp) {
    const now = new Date();
    dom.indicators.timestamp.textContent =
      now.toLocaleDateString("pt-BR") +
      " " +
      now.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
  }
}

// ============================================================
// ANIMAÇÕES E MICROINTERAÇÕES
// ============================================================
function animateCounter(element, target, duration = 1200) {
  if (!element) return;

  const start = 0;
  const startTime = performance.now();
  const isFloat = target % 1 !== 0;

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = start + (target - start) * eased;

    element.textContent = isFloat ? current.toFixed(1) : Math.round(current);

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      element.textContent = isFloat ? target.toFixed(1) : Math.round(target);
    }
  }

  requestAnimationFrame(update);
}

function setupScrollReveal() {
  const elements = document.querySelectorAll(
    ".card, .panel, .collab-card, .commit-row, .stat-box, .heat-box",
  );

  if (!("IntersectionObserver" in window)) {
    elements.forEach((el) => el.classList.add("revealed"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          const delay = index * 30;
          setTimeout(() => {
            entry.target.classList.add("revealed");
          }, delay);
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
      rootMargin: "0px 0px -30px 0px",
    },
  );

  elements.forEach((el) => observer.observe(el));
}

function setupCardParallax() {
  const cards = document.querySelectorAll(".card, .panel");

  cards.forEach((card) => {
    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;

      card.style.transform = `
                perspective(800px)
                rotateY(${x * 6}deg)
                rotateX(${-y * 6}deg)
                translateY(-4px)
            `;
    });

    card.addEventListener("mouseleave", () => {
      card.style.transform =
        "perspective(800px) rotateY(0deg) rotateX(0deg) translateY(0)";
      card.style.transition =
        "transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)";
      setTimeout(() => {
        card.style.transition = "";
      }, 600);
    });
  });
}

function setupSkeletonShimmer() {
  const skeletons = document.querySelectorAll(".commit-row");
  skeletons.forEach((skeleton) => {
    skeleton.style.position = "relative";
    skeleton.style.overflow = "hidden";
    skeleton.style.background = "var(--color-bg-tertiary)";
    skeleton.style.borderRadius = "8px";
    skeleton.style.marginBottom = "4px";

    const shimmer = document.createElement("div");
    shimmer.style.cssText = `
            position: absolute;
            top: 0;
            left: -100%;
            width: 200%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent 0%,
                rgba(255, 255, 255, 0.03) 40%,
                rgba(255, 255, 255, 0.06) 50%,
                rgba(255, 255, 255, 0.03) 60%,
                transparent 100%
            );
            animation: shimmer 2.5s ease-in-out infinite;
            pointer-events: none;
        `;
    skeleton.appendChild(shimmer);
  });

  if (!document.getElementById("shimmer-style")) {
    const style = document.createElement("style");
    style.id = "shimmer-style";
    style.textContent = `
            @keyframes shimmer {
                0% { transform: translateX(-50%); }
                100% { transform: translateX(50%); }
            }
        `;
    document.head.appendChild(style);
  }
}

function initAnimations() {
  const metrics = [
    {
      el: document.getElementById("total-commits"),
      target:
        parseInt(document.getElementById("total-commits")?.textContent) || 0,
    },
    {
      el: document.getElementById("closed-issues"),
      target:
        parseInt(document.getElementById("closed-issues")?.textContent) || 0,
    },
    {
      el: document.getElementById("total-collabs"),
      target:
        parseInt(document.getElementById("total-collabs")?.textContent) || 0,
    },
  ];

  const observer = new MutationObserver(() => {
    metrics.forEach(({ el }) => {
      if (el && el.textContent !== "0" && !el.dataset.animated) {
        const finalValue = parseInt(el.textContent);
        el.dataset.animated = "true";
        animateCounter(el, finalValue);
      }
    });
  });

  metrics.forEach(({ el }) => {
    if (el) observer.observe(el, { childList: true, subtree: true });
  });

  setupScrollReveal();
  setupCardParallax();
  setupSkeletonShimmer();
}

function initParticles() {
  const hero = document.querySelector(".hero");
  if (!hero) return;

  const oldStars = hero.querySelector(".particles");
  if (oldStars) oldStars.remove();

  const container = document.createElement("div");
  container.className = "particles";
  container.style.cssText = `
        position: absolute;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
    `;

  const count = 70;
  for (let i = 0; i < count; i++) {
    const particle = document.createElement("div");
    const size = Math.random() * 3 + 1;
    const x = Math.random() * 100;
    const y = Math.random() * 100;
    const duration = Math.random() * 20 + 15;
    const delay = Math.random() * 10;

    particle.style.cssText = `
            position: absolute;
            left: ${x}%;
            top: ${y}%;
            width: ${size}px;
            height: ${size}px;
            background: radial-gradient(circle, rgba(34, 211, 238, ${Math.random() * 0.5 + 0.2}), transparent);
            border-radius: 50%;
            box-shadow: 0 0 ${size * 4}px rgba(34, 211, 238, 0.15);
            animation: floatParticle ${duration}s ease-in-out infinite;
            animation-delay: ${delay}s;
            opacity: ${Math.random() * 0.5 + 0.2};
        `;
    container.appendChild(particle);
  }

  hero.appendChild(container);

  if (!document.getElementById("particle-style")) {
    const style = document.createElement("style");
    style.id = "particle-style";
    style.textContent = `
            @keyframes floatParticle {
                0%, 100% { transform: translate(0, 0) scale(1); }
                25% { transform: translate(12px, -10px) scale(1.2); }
                50% { transform: translate(-15px, 8px) scale(0.8); }
                75% { transform: translate(8px, 14px) scale(1.1); }
            }
        `;
    document.head.appendChild(style);
  }
}

function initParallax() {
  const hero = document.querySelector(".hero");
  const title = document.querySelector(".hero h1");
  const subtitle = document.querySelector(".hero .subtitle");
  const description = document.querySelector(".hero .description");
  const button = document.querySelector(".hero .btn-primary");
  const glow = document.querySelector(".glow-bg");

  if (!hero || !title) return;

  hero.addEventListener("mousemove", (e) => {
    const rect = hero.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;

    title.style.transform = `translate(${x * 20}px, ${y * 12}px) scale(${1 + Math.abs(x) * 0.02 + Math.abs(y) * 0.01})`;
    title.style.transition =
      "transform 0.15s cubic-bezier(0.34, 1.56, 0.64, 1)";

    if (subtitle) {
      subtitle.style.transform = `translate(${x * 12}px, ${y * 8}px)`;
      subtitle.style.transition =
        "transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1)";
    }

    if (description) {
      description.style.transform = `translate(${x * 8}px, ${y * 6}px)`;
      description.style.transition =
        "transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)";
    }

    if (button) {
      button.style.transform = `translate(${x * 6}px, ${y * 4}px) scale(${1 + Math.abs(x) * 0.01})`;
      button.style.transition =
        "transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)";
    }

    if (glow) {
      glow.style.transform = `translate(${-x * 20}px, ${-y * 15}px) scale(1.05)`;
      glow.style.transition =
        "transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)";
    }
  });

  hero.addEventListener("mouseleave", () => {
    [title, subtitle, description, button, glow].forEach((el) => {
      if (el) {
        el.style.transform = "";
        el.style.transition =
          "transform 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)";
      }
    });
    setTimeout(() => {
      [title, subtitle, description, button, glow].forEach((el) => {
        if (el) el.style.transition = "";
      });
    }, 900);
  });
}

function initTypewriter() {
  const subtitle = document.querySelector(".hero .subtitle");
  if (!subtitle) return;

  const originalText = subtitle.textContent;
  subtitle.textContent = "";
  subtitle.style.opacity = "0";

  let index = 0;
  const speed = 40;

  function type() {
    if (index < originalText.length) {
      subtitle.textContent += originalText.charAt(index);
      subtitle.style.opacity = "1";
      index++;
      setTimeout(type, speed);
    } else {
      subtitle.style.animation = "blinkCursor 1s step-end infinite";
      if (!document.getElementById("cursor-style")) {
        const style = document.createElement("style");
        style.id = "cursor-style";
        style.textContent = `
                    @keyframes blinkCursor {
                        0%, 100% { border-right: 2px solid var(--color-accent-cyan); }
                        50% { border-right: 2px solid transparent; }
                    }
                `;
        document.head.appendChild(style);
      }
    }
  }

  setTimeout(type, 600);
}

function initStagger() {
  const elements = document.querySelectorAll(
    ".hero h1, .hero .subtitle, .hero .description, .hero .btn-primary",
  );
  elements.forEach((el, i) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(40px) scale(0.95)";
    el.style.transition = `opacity 0.8s cubic-bezier(0.34, 1.56, 0.64, 1), transform 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)`;
    const delay = 200 + i * 200;
    setTimeout(() => {
      el.style.opacity = "1";
      el.style.transform = "translateY(0) scale(1)";
    }, delay);
  });
}

function initPulseButton() {
  const button = document.querySelector(".hero .btn-primary");
  if (!button) return;

  if (!document.getElementById("pulse-style")) {
    const style = document.createElement("style");
    style.id = "pulse-style";
    style.textContent = `
            .hero .btn-primary {
                position: relative;
                z-index: 2;
                animation: pulseButton 3s ease-in-out infinite;
            }
            @keyframes pulseButton {
                0%, 100% { box-shadow: 0 0 20px rgba(34, 211, 238, 0.3); }
                50% { box-shadow: 0 0 40px rgba(34, 211, 238, 0.6), 0 0 80px rgba(34, 211, 238, 0.2); }
            }
        `;
    document.head.appendChild(style);
  }
}

function initLandingEffects() {
  const landing = document.getElementById("landing-view");
  if (!landing || !landing.classList.contains("is-active")) return;

  initStagger();
  setTimeout(initTypewriter, 400);
  setTimeout(initParticles, 300);
  setTimeout(initParallax, 500);
  setTimeout(initPulseButton, 600);
}

// ============================================================
// EVENT BINDING (with debounce)
// ============================================================
function initEventListeners() {
  const showDashboard = () => {
    transitionTo(dom.views.dashboard, dom.views.landing);
    if (state._data.commits.length === 0) {
      handleLoadData();
    }
  };

  const showLanding = () => {
    transitionTo(dom.views.landing, dom.views.dashboard);
  };

  [dom.buttons.enterNav, dom.buttons.enterHero].forEach((btn) => {
    if (btn) btn.addEventListener("click", showDashboard);
  });

  if (dom.buttons.backHome) {
    dom.buttons.backHome.addEventListener("click", showLanding);
  }

  if (dom.buttons.sync) {
    const debouncedSync = debounce(handleLoadData, 200);
    dom.buttons.sync.addEventListener("click", debouncedSync);
  }

  document.addEventListener("keydown", (event) => {
    if (
      (event.metaKey || event.ctrlKey) &&
      event.shiftKey &&
      event.key === "R"
    ) {
      event.preventDefault();
      handleLoadData();
    }

    if (
      event.key === "Escape" &&
      dom.views.dashboard.classList.contains("is-active")
    ) {
      showLanding();
    }
  });
}

// ============================================================
// SKELETON LOADING
// ============================================================
function showSkeletonLoading() {
  const container = document.getElementById("commit-log-container");
  if (!container) return;

  const skeletonItems = Array(5)
    .fill(0)
    .map(
      () => `
        <div class="commit-row" style="opacity: 0.4; pointer-events: none;">
            <div class="commit-sha" style="background: var(--color-bg-tertiary); height: 16px; width: 60px; border-radius: 4px;"></div>
            <div class="commit-info">
                <div style="background: var(--color-bg-tertiary); height: 14px; width: 80%; border-radius: 4px; margin-bottom: 6px;"></div>
                <div style="background: var(--color-bg-tertiary); height: 10px; width: 40%; border-radius: 4px;"></div>
            </div>
            <div style="background: var(--color-bg-tertiary); height: 12px; width: 50px; border-radius: 4px; justify-self: end;"></div>
        </div>
    `,
    )
    .join("");

  container.innerHTML = skeletonItems;
}

// ============================================================
// INITIALIZATION
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
  console.log("🔷 PRISMA Insight initialized");

  if (dom.views.dashboard) {
    showSkeletonLoading();
  }

  initEventListeners();

  if (dom.views.dashboard?.classList.contains("is-active")) {
    handleLoadData();
  }

  if (import.meta.env?.MODE === "development") {
    window.__PRISMA = { state, dom, CONFIG };
  }

  initLandingEffects();
  initAnimations();
});

// ============================================================
// SERVICE WORKER REGISTRATION (Progressive Web App)
// ============================================================
if ("serviceWorker" in navigator) {
  // Optional: register service worker for offline support
  // navigator.serviceWorker.register('/sw.js');
}

export { state, handleLoadData, transitionTo };
