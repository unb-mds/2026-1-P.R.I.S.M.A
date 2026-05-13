import React from 'react';
import { format, parseISO, startOfDay, eachDayOfInterval, subDays, isSameDay } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { GitHubCommit, GitHubIssue } from '../lib/types';
import { motion } from 'motion/react';

interface HeatmapProps {
  commits: GitHubCommit[];
  issues: GitHubIssue[];
}

export const ActivityHeatmap: React.FC<HeatmapProps> = ({ commits, issues }) => {
  const last90Days = eachDayOfInterval({
    start: startOfDay(subDays(new Date(), 89)),
    end: startOfDay(new Date()),
  });

  const getActivityCount = (day: Date) => {
    const commitCount = commits.filter(c => isSameDay(parseISO(c.commit.author.date), day)).length;
    const issueCount = issues.filter(i => isSameDay(parseISO(i.created_at), day)).length;
    const closedIssueCount = issues.filter(i => i.closed_at && isSameDay(parseISO(i.closed_at), day)).length;
    return commitCount + issueCount + closedIssueCount;
  };

  const getColor = (count: number) => {
    if (count === 0) return 'bg-slate-800';
    if (count < 3) return 'bg-cyan-900/40';
    if (count < 6) return 'bg-cyan-600/60';
    if (count < 10) return 'bg-cyan-500';
    return 'bg-cyan-300';
  };

  return (
    <div className="p-6 bg-transparent">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-[9px] font-black text-slate-500 uppercase tracking-[0.2em]">Mapa de Calor de Atividade (90 Dias)</h3>
        <div className="flex items-center gap-2 text-[8px] text-slate-500 font-black uppercase tracking-widest">
          <span>Menos</span>
          <div className="flex gap-1">
            <div className="w-2.5 h-2.5 bg-slate-800 rounded-[2px]"></div>
            <div className="w-2.5 h-2.5 bg-cyan-900/40 rounded-[2px]"></div>
            <div className="w-2.5 h-2.5 bg-cyan-600/60 rounded-[2px]"></div>
            <div className="w-2.5 h-2.5 bg-cyan-500 rounded-[2px]"></div>
            <div className="w-2.5 h-2.5 bg-cyan-300 rounded-[2px]"></div>
          </div>
          <span>Mais</span>
        </div>
      </div>
      
      <div className="flex flex-wrap gap-1 justify-center max-w-[280px] mx-auto">
        {last90Days.map((day, i) => {
          const count = getActivityCount(day);
          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.002 }}
              title={`${format(day, "dd 'de' MMMM 'de' yyyy", { locale: ptBR })}: ${count} atividades`}
              className={`w-2.5 h-2.5 rounded-[2px] ${getColor(count)} cursor-help transition-all hover:scale-150 hover:z-10 hover:shadow-[0_0_8px_rgba(34,211,238,0.6)]`}
            />
          );
        })}
      </div>
      <p className="mt-6 text-[9px] text-slate-600 text-center font-medium tracking-wide">
        Logs combinados: Commits + Issues Abertas/Fechadas
      </p>
    </div>
  );
};
