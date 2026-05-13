import React from 'react';
import { GitHubCommit } from '../lib/types';
import { formatDate } from '../lib/utils';
import { ExternalLink, GitCommit } from 'lucide-react';
import { motion } from 'motion/react';

interface CommitLogProps {
  commits: GitHubCommit[];
  onSelect?: (sha: string) => void;
  selectedShas: string[];
}

export const CommitLog: React.FC<CommitLogProps> = ({ commits, onSelect, selectedShas }) => {
  return (
    <div className="flex flex-col">
      <div className="grid grid-cols-[100px_1fr_120px_40px] col-header bg-slate-900/80 sticky top-0 z-10 border-b border-slate-800 backdrop-blur-sm">
        <div>REVISÃO</div>
        <div>MENSAGEM / AUTOR</div>
        <div className="text-right">DATA</div>
        <div></div>
      </div>
      <div className="max-h-[600px] overflow-y-auto divide-y divide-slate-800 scrollbar-thin scrollbar-thumb-slate-800">
        {commits.map((commit) => {
          const isSelected = selectedShas.includes(commit.sha);
          return (
            <motion.div 
              key={commit.sha}
              whileHover={{ x: 4 }}
              onClick={() => onSelect?.(commit.sha)}
              className={`data-row grid grid-cols-[100px_1fr_120px_40px] items-center cursor-pointer transition-all duration-300 ${
                isSelected ? 'bg-cyan-900/30 border-l-4 border-cyan-500 shadow-[inset_10px_0_20px_-10px_rgba(34,211,238,0.2)]' : 'hover:bg-slate-800/30'
              }`}
            >
              <div className="data-value truncate pr-2 font-black text-cyan-500/60 tracking-wider">
                {commit.sha.substring(0, 7)}
              </div>
              <div className="min-w-0 pr-4">
                <p className={`text-sm font-bold truncate transition-colors ${isSelected ? 'text-white' : 'text-slate-300'}`}>
                  {commit.commit.message}
                </p>
                <div className="flex items-center gap-1.5 mt-1">
                  <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest">
                    {commit.commit.author.name}
                  </span>
                </div>
              </div>
              <div className="text-[10px] text-slate-500 font-mono font-bold text-right tabular-nums">
                {formatDate(commit.commit.author.date).split(',')[0]}
              </div>
              <div className="flex justify-end pr-2 text-slate-600 hover:text-cyan-400">
                <a 
                  href={commit.html_url} 
                  target="_blank" 
                  rel="noreferrer"
                  onClick={(e) => e.stopPropagation()}
                  className="p-1.5 hover:bg-slate-800 rounded-lg transition-all"
                >
                  <ExternalLink size={14} />
                </a>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};
