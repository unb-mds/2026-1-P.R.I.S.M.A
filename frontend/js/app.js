/**
 * PRISMA Insight - Data Orchestration Layer
 */

import { renderCharts } from './components/charts.js';
import { renderHeatmap } from './components/heatmap.js';
import { initTimeline } from './components/timeline.js';
import { renderCommitLog } from './components/commitlog.js';
import { renderCollaborators } from './components/collaborators.js';

export const PrismaApp = {
    /**
     * Main sync method - fetches and renders all data
     * @returns {Promise<Object>} Metrics data
     */
    async sync() {
        try {
            const response = await fetch('dados.json');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();

            const commits = data.raw_commits || [];
            const issues = data.raw_issues || [];

            const metrics = {
                commits,
                issues,
                generated_at: data.generated_at || new Date().toISOString(),
            };

            this.renderAll(metrics);
            return metrics;

        } catch (error) {
            console.error('[PrismaApp] Sync error:', error);
            throw error;
        }
    },

    /**
     * Render all dashboard components
     * @param {Object} data - Data object with commits and issues
     */
    renderAll(data) {
        const { commits, issues } = data;

        // Render components (safe calls)
        if (typeof renderCharts === 'function') {
            renderCharts(commits, issues);
        }

        if (typeof renderHeatmap === 'function') {
            renderHeatmap(commits, issues);
        }

        if (typeof initTimeline === 'function') {
            initTimeline(commits, issues);
        }

        if (typeof renderCommitLog === 'function') {
            renderCommitLog(commits);
        }

        if (typeof renderCollaborators === 'function') {
            renderCollaborators(commits, issues);
        }
    },
};