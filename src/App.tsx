/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from 'react';
import { fetchCommits, fetchIssues } from './lib/github';
import { GitHubCommit, GitHubIssue } from './lib/types';
import { StatsCharts } from './components/Charts';
import { ActivityHeatmap } from './components/ActivityHeatmap';
import { WeeklyTimeline } from './components/WeeklyTimeline';
import { CollaboratorStats } from './components/CollaboratorStats';
import { CommitLog } from './components/CommitLog';
import { DiffSection } from './components/DiffSection';
import { RefreshCw, GitBranch, AlertCircle, CheckCircle2, Github, LayoutDashboard, Calendar, Flame, Users } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

export default function App() {
  const [commits, setCommits] = useState<GitHubCommit[]>([]);
  const [issues, setIssues] = useState<GitHubIssue[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Selection for comparison
  const [selectedShas, setSelectedShas] = useState<string[]>([]);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [commitData, issueData] = await Promise.all([
        fetchCommits(),
        fetchIssues(),
      ]);
      setCommits(commitData);
      setIssues(issueData);
    } catch (err: any) {
      console.error(err);
      setError('Erro ao carregar dados do GitHub. Limite de requisições excedido ou repositório inacessível.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSelectCommit = (sha: string) => {
    setSelectedShas(prev => {
      if (prev.includes(sha)) return prev.filter(s => s !== sha);
      if (prev.length >= 2) return [prev[1], sha];
      return [...prev, sha];
    });
  };

  const openIssues = issues.filter(i => i.state === 'open').length;

  return (
    <div className="min-h-screen flex flex-col font-sans bg-[#0f172a] text-slate-200">
      {/* Header */}
      <header className="bg-[#1e293b]/80 backdrop-blur-md border-b border-slate-800 px-6 py-4 flex flex-col md:flex-row items-center justify-between shadow-lg shrink-0 sticky top-0 z-20 transition-all">
        <div className="flex items-center gap-4">
          <div className="bg-cyan-500 text-slate-900 p-2 rounded shadow-[0_0_15px_rgba(34,211,238,0.4)]">
            <Github size={20} />
          </div>
          <div>
            <h1 className="text-lg font-black tracking-tight text-white leading-none uppercase italic">PRISMA Insight</h1>
            <p className="text-[10px] text-cyan-500/70 mt-1 font-mono uppercase tracking-widest font-bold">unb-mds / 2026-1-P.R.I.S.M.A</p>
          </div>
        </div>
        <div className="flex flex-wrap gap-3 items-center mt-4 md:mt-0">
          <div className="flex flex-col items-end gap-1">
            <span className="text-[9px] font-bold text-slate-500 uppercase leading-none">Token de Acesso do Github</span>
            <input 
              type="password" 
              placeholder="ghp_..."
              className="text-[10px] px-3 py-1 bg-slate-900 border border-slate-700 rounded-lg w-32 focus:w-56 transition-all outline-none focus:border-cyan-500 shadow-inner text-cyan-400"
              defaultValue={localStorage.getItem('gh_token') || ''}
              onChange={(e) => {
                const val = e.target.value;
                if (val) localStorage.setItem('gh_token', val);
                else localStorage.removeItem('gh_token');
              }}
            />
          </div>
          <button 
            onClick={loadData}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-1.5 bg-cyan-500 hover:bg-cyan-400 rounded-full font-bold text-slate-900 text-xs transition-all shadow-[0_0_10px_rgba(34,211,238,0.2)] hover:shadow-[0_0_20px_rgba(34,211,238,0.4)]"
          >
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            {loading ? 'Sincronizando...' : 'Sincronizar'}
          </button>
          <div className="text-slate-700 hidden md:block">|</div>
          <div className="font-mono text-[10px] text-cyan-400/60 bg-slate-900 px-2 py-1 rounded border border-slate-800">
            {commits[0]?.sha.substring(0, 7) || 'latest'}
          </div>
        </div>
      </header>

      <main className="flex-1 p-6 md:p-8 space-y-12 max-w-[1600px] mx-auto w-full">
        {error && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="p-4 bg-red-900/20 border border-red-500/30 text-red-400 rounded-xl flex items-center gap-3 text-sm shadow-xl"
          >
            <AlertCircle size={18} /> {error}
          </motion.div>
        )}

        {/* Metric Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6 flex flex-col justify-between shadow-xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/5 blur-3xl -mr-16 -mt-16 group-hover:bg-cyan-500/10 transition-all"></div>
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-4">Frequência de Commits</span>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-black text-white">{commits.length}</span>
              <span className="text-xs text-cyan-500 font-bold uppercase tracking-tighter">Total</span>
            </div>
            <div className="mt-6 flex gap-1 items-end h-10">
              {[0.4, 0.6, 1, 0.7, 0.5, 0.8, 0.4].map((h, i) => (
                <div 
                  key={i} 
                  className={`w-full rounded-t-sm transition-all duration-500 ${i === 2 ? 'bg-cyan-500 shadow-[0_0_10px_rgba(34,211,238,0.5)]' : 'bg-slate-700'}`} 
                  style={{ height: `${h * 100}%` }}
                />
              ))}
            </div>
          </div>

          <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6 flex flex-col justify-between shadow-xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-amber-500/5 blur-3xl -mr-16 -mt-16 group-hover:bg-amber-500/10 transition-all"></div>
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-4">Issues Abertas</span>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-black text-white">{openIssues}</span>
              <span className="text-xs text-amber-500 font-bold uppercase tracking-tighter">Pendentes</span>
            </div>
            <div className="mt-6 text-[10px] text-slate-500 italic font-mono">Resolução Média: -- dias</div>
          </div>

          <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6 flex flex-col justify-between shadow-xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/5 blur-3xl -mr-16 -mt-16 group-hover:bg-emerald-500/10 transition-all"></div>
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-4">Colaboradores</span>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-black text-white">{new Set(commits.map(c => c.commit.author.email)).size}</span>
              <span className="text-xs text-emerald-500 font-bold uppercase tracking-tighter">Ativos</span>
            </div>
            <div className="mt-6 flex -space-x-3">
               {commits.slice(0, 5).map((c, i) => (
                 <img key={i} src={c.author?.avatar_url} className="w-8 h-8 rounded-full border-2 border-[#1e293b] bg-slate-800 shadow-lg" alt="" />
               ))}
            </div>
          </div>

          <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6 flex flex-col justify-between shadow-xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/5 blur-3xl -mr-16 -mt-16 group-hover:bg-cyan-500/10 transition-all"></div>
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-4">Status do Build</span>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-black text-white">100%</span>
              <span className="text-xs text-cyan-400 font-bold uppercase tracking-tighter">Saudável</span>
            </div>
            <div className="mt-6 flex items-center gap-3 text-[10px] text-cyan-500 font-mono tracking-widest">
              <div className="relative">
                <div className="w-2.5 h-2.5 rounded-full bg-cyan-500 absolute animate-ping opacity-75"></div>
                <div className="w-2.5 h-2.5 rounded-full bg-cyan-500 relative"></div>
              </div>
              SISTEMA ESTÁVEL
            </div>
          </div>
        </div>

        {/* Charts and Data Visualization */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          <section className="lg:col-span-8 bg-[#1e293b] border border-slate-800 rounded-2xl shadow-2xl overflow-hidden shadow-cyan-900/10">
            <div className="bg-slate-900/50 border-b border-slate-800 px-8 py-5 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-1.5 bg-slate-800 rounded-lg text-cyan-400">
                  <LayoutDashboard size={14} />
                </div>
                <h2 className="text-xs font-black uppercase tracking-[0.2em] text-slate-300">Monitoramento Analítico</h2>
              </div>
              <div className="flex gap-6 text-[9px] font-bold uppercase tracking-widest">
                <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-cyan-500 shadow-[0_0_8px_rgba(34,211,238,0.6)]"></span> Commits</div>
                <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-cyan-800"></span> Issues</div>
              </div>
            </div>
            <StatsCharts commits={commits} issues={issues} />
          </section>

          <section className="lg:col-span-4 space-y-10">
            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl shadow-2xl overflow-hidden p-0 shadow-cyan-900/5">
               <div className="bg-slate-900/50 border-b border-slate-800 px-8 py-5 flex items-center gap-3">
                 <div className="p-1.5 bg-slate-800 rounded-lg text-orange-400">
                  <Flame size={14} />
                 </div>
                 <h2 className="text-xs font-black uppercase tracking-[0.2em] text-slate-300">Atividade Geral</h2>
               </div>
               <ActivityHeatmap commits={commits} issues={issues} />
            </div>
          </section>
        </div>

        {/* Development Team Section */}
        <section className="bg-[#1e293b] border border-slate-800 rounded-2xl shadow-2xl overflow-hidden shadow-cyan-900/5">
          <div className="bg-slate-900/50 border-b border-slate-800 px-8 py-5 flex items-center gap-3">
            <div className="p-1.5 bg-slate-800 rounded-lg text-cyan-400">
              <Users size={14} />
            </div>
            <h2 className="text-xs font-black uppercase tracking-[0.2em] text-slate-300">Time de Desenvolvimento</h2>
          </div>
          <CollaboratorStats commits={commits} issues={issues} />
        </section>

        {/* Weekly Analysis and Git Log Section */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
          <section className="lg:col-span-4">
             <div className="flex items-center gap-3 mb-6 bg-slate-900/40 p-3 rounded-xl border border-slate-800 w-fit">
               <Calendar size={18} className="text-cyan-500" />
               <h2 className="text-xs font-black uppercase tracking-[0.2em] text-slate-300">Histórico de Sessões</h2>
             </div>
             <WeeklyTimeline commits={commits} issues={issues} />
          </section>

          <section className="lg:col-span-8 bg-[#1e293b] border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col shadow-cyan-900/5">
            <div className="bg-slate-900/50 border-b border-slate-800 px-8 py-5 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-1.5 bg-slate-800 rounded-lg text-cyan-400">
                  <GitBranch size={14} />
                </div>
                <h2 className="text-xs font-black uppercase tracking-[0.2em] text-slate-300">Log de Atividade Git</h2>
              </div>
              {selectedShas.length > 0 && (
                <button 
                  onClick={() => setSelectedShas([])}
                  className="text-[10px] bg-cyan-500/10 text-cyan-400 px-3 py-1 rounded-full border border-cyan-500/20 hover:bg-cyan-500/20 transition-all font-bold uppercase tracking-widest"
                >
                  Limpar ({selectedShas.length})
                </button>
              )}
            </div>
            <CommitLog 
              commits={commits} 
              onSelect={handleSelectCommit} 
              selectedShas={selectedShas}
            />
          </section>
        </div>

        {/* Diff Analysis Section */}
        {selectedShas.length === 2 && (
          <section className="animate-in fade-in slide-in-from-bottom-10 space-y-6">
            <div className="bg-slate-900/40 p-4 rounded-2xl border border-slate-800 inline-flex items-center gap-4">
               <GitCompare size={20} className="text-cyan-400" />
               <h2 className="text-xs font-black uppercase tracking-[0.2em] text-slate-300">Análise de Diferenças entre Versões</h2>
            </div>
            <DiffSection 
              baseSha={selectedShas[0]} 
              headSha={selectedShas[1]} 
            />
          </section>
        )}
      </main>

      {/* Footer Info */}
      <footer className="mt-24 px-8 py-10 bg-[#0f172a] border-t border-slate-800 flex flex-col md:flex-row justify-between items-center text-[10px] text-slate-500 font-mono gap-6 relative overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-px bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent"></div>
        <div className="flex flex-col items-center md:items-start gap-1">
          <div className="font-bold text-slate-400">TIMESTAMP DE SINCRONIZAÇÃO</div>
          <div>{new Date().toLocaleString('pt-BR')}</div>
        </div>
        <div className="flex flex-col md:flex-row gap-6 items-center">
          <span className="text-cyan-500 font-black flex items-center gap-2 group">
             <span className="w-2 h-2 rounded-full bg-cyan-500 shadow-[0_0_8px_rgba(34,211,238,0.8)] animate-pulse"></span> 
             <span className="tracking-[0.3em]">AUTOMAÇÃO PRISMA ATIVA</span>
          </span>
          <div className="h-4 w-px bg-slate-800 hidden md:block"></div>
          <span className="tracking-widest opacity-50 uppercase">MDS-UNB-2026-1</span>
          <div className="h-4 w-px bg-slate-800 hidden md:block"></div>
          <span className="text-[8px] bg-slate-900 p-1 rounded border border-slate-800">BETA v2.4.0</span>
        </div>
      </footer>
    </div>
  );
}

