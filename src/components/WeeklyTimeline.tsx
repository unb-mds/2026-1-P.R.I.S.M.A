import React, { useState } from 'react';
import { format, parseISO, startOfWeek, endOfWeek, eachWeekOfInterval, subWeeks, isWithinInterval } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { GitHubCommit, GitHubIssue } from '../lib/types';
import { GitCommit, AlertCircle, ChevronLeft, ChevronRight } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

interface TimelineProps {
  commits: GitHubCommit[];
  issues: GitHubIssue[];
}

export const WeeklyTimeline: React.FC<TimelineProps> = ({ commits, issues }) => {
  const [selectedWeekIdx, setSelectedWeekIdx] = useState(0);
  
  const weeks = eachWeekOfInterval({
    start: startOfWeek(subWeeks(new Date(), 7)),
    end: startOfWeek(new Date()),
  }).reverse();

  const currentWeek = weeks[selectedWeekIdx];
  const weekStart = startOfWeek(currentWeek);
  const weekEnd = endOfWeek(currentWeek);

  const weekCommits = commits.filter(c => 
    isWithinInterval(parseISO(c.commit.author.date), { start: weekStart, end: weekEnd })
  );

  const weekIssues = issues.filter(i => 
    isWithinInterval(parseISO(i.created_at), { start: weekStart, end: weekEnd })
  );

  return (
    <div className="bg-[#1e293b] border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col">
      <div className="bg-slate-900/50 border-b border-slate-800 px-6 py-4 flex items-center justify-between">
        <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Timeline Semanal</h3>
        <div className="flex items-center gap-4">
          <button 
            disabled={selectedWeekIdx >= weeks.length - 1}
            onClick={() => setSelectedWeekIdx(v => v + 1)}
            className="p-1.5 hover:bg-slate-800 text-slate-400 hover:text-cyan-400 rounded-lg disabled:opacity-10 transition-all border border-transparent hover:border-slate-700"
          >
            <ChevronLeft size={16} />
          </button>
          <span className="text-[11px] font-black text-white font-mono tracking-widest uppercase">
            {format(weekStart, 'dd MMM', { locale: ptBR })} — {format(weekEnd, 'dd MMM', { locale: ptBR })}
          </span>
          <button 
            disabled={selectedWeekIdx <= 0}
            onClick={() => setSelectedWeekIdx(v => v - 1)}
            className="p-1.5 hover:bg-slate-800 text-slate-400 hover:text-cyan-400 rounded-lg disabled:opacity-10 transition-all border border-transparent hover:border-slate-700"
          >
            <ChevronRight size={16} />
          </button>
        </div>
      </div>

      <div className="p-6 h-[400px] overflow-y-auto scrollbar-thin scrollbar-thumb-slate-800">
        <AnimatePresence mode="wait">
          <motion.div
            key={selectedWeekIdx}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="space-y-6"
          >
            <div className="grid grid-cols-2 gap-4 pb-4 border-b border-slate-800">
               <div className="bg-cyan-950/20 border border-cyan-500/10 p-4 rounded-xl">
                 <div className="flex items-center gap-2 text-cyan-500 mb-1">
                   <GitCommit size={14} />
                   <span className="text-[9px] font-black uppercase tracking-widest">Commits</span>
                 </div>
                 <div className="text-3xl font-black text-white">{weekCommits.length}</div>
               </div>
               <div className="bg-slate-850/20 border border-slate-700/50 p-4 rounded-xl">
                 <div className="flex items-center gap-2 text-slate-400 mb-1">
                   <AlertCircle size={14} />
                   <span className="text-[9px] font-black uppercase tracking-widest">Issues</span>
                 </div>
                 <div className="text-3xl font-black text-white">{weekIssues.length}</div>
               </div>
            </div>

            <div className="space-y-4">
              <h4 className="text-[9px] font-black text-slate-500 uppercase tracking-[0.2em] mb-4">Logs de Sessão</h4>
              {[...weekCommits.map(c => ({ type: 'commit', date: c.commit.author.date, msg: c.commit.message })),
                ...weekIssues.map(i => ({ type: 'issue', date: i.created_at, msg: i.title }))]
                .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
                .map((activity, idx) => (
                  <div key={idx} className="flex gap-4 items-start group relative">
                    <div className="pt-2 text-[10px] font-mono font-bold text-slate-600 w-10 text-right shrink-0">
                      {format(parseISO(activity.date), 'dd/MM')}
                    </div>
                    <div className={`p-3 rounded-xl border border-slate-800/50 flex-1 text-xs transition-all group-hover:border-slate-700 shadow-sm ${
                      activity.type === 'commit' ? 'bg-cyan-900/10' : 'bg-slate-800/40'
                    }`}>
                      <span className={`font-black uppercase text-[8px] tracking-widest block mb-1.5 ${
                        activity.type === 'commit' ? 'text-cyan-500' : 'text-slate-400'
                      }`}>
                        {activity.type === 'commit' ? 'COMMIT' : 'ISSUE'}
                      </span>
                      <p className="text-slate-300 leading-relaxed font-medium">
                        {activity.msg}
                      </p>
                    </div>
                  </div>
                ))}
              {weekCommits.length === 0 && weekIssues.length === 0 && (
                <div className="text-center py-16 text-slate-600 text-xs italic font-medium">
                  Silêncio no repositório nesta semana.
                </div>
              )}
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
};
