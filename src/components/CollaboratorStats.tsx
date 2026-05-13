import React from 'react';
import { GitHubCommit, GitHubIssue } from '../lib/types';
import { User, MessageSquare, GitCommit, Award } from 'lucide-react';
import { motion } from 'motion/react';

interface CollaboratorStatsProps {
  commits: GitHubCommit[];
  issues: GitHubIssue[];
}

export const CollaboratorStats: React.FC<CollaboratorStatsProps> = ({ commits, issues }) => {
  // Aggregate stats by user
  // First pass: build email to login mapping
  const emailToLogin = commits.reduce((acc, commit) => {
    const login = commit.author?.login;
    const email = commit.commit.author.email;
    if (login && email) {
      acc[email] = login;
    }
    return acc;
  }, {} as Record<string, string>);

  const userStats = commits.reduce((acc, commit) => {
    const email = commit.commit.author.email;
    const login = commit.author?.login || emailToLogin[email] || email;
    const name = commit.commit.author.name;
    
    if (!acc[login]) {
      acc[login] = {
        login: commit.author?.login || emailToLogin[email] || 'external',
        name: name,
        avatar: commit.author?.avatar_url,
        commitCount: 0,
        issueCount: 0,
        recentMsg: commit.commit.message
      };
    }
    
    if (commit.author?.avatar_url && !acc[login].avatar) {
      acc[login].avatar = commit.author?.avatar_url;
    }

    acc[login].commitCount++;
    return acc;
  }, {} as Record<string, any>);

  // Add issue stats
  issues.forEach(issue => {
    const login = issue.user.login;
    if (userStats[login]) {
      userStats[login].issueCount++;
    }
  });

  const sortedUsers = Object.values(userStats).sort((a, b) => b.commitCount - a.commitCount);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 p-6">
      {sortedUsers.map((user, i) => (
        <motion.div 
          key={user.login}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1 }}
          className="bg-[#0f172a]/40 border border-slate-800 rounded-2xl p-6 shadow-sm hover:shadow-cyan-500/10 hover:border-cyan-500/30 transition-all relative overflow-hidden group border-b-4 border-b-transparent hover:border-b-cyan-500"
        >
          {i === 0 && (
            <div className="absolute top-3 right-3 text-cyan-400 drop-shadow-[0_0_8px_rgba(34,211,238,0.4)]">
              <Award size={20} />
            </div>
          )}
          
          <div className="flex items-center gap-4 mb-6">
            <div className="relative">
              <img 
                src={user.avatar || `https://ui-avatars.com/api/?name=${user.name}&background=1e293b&color=22d3ee`} 
                className="w-14 h-14 rounded-2xl border-2 border-slate-700 group-hover:border-cyan-500 transition-all rotate-3 group-hover:rotate-0"
                alt={user.login}
              />
              <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-cyan-500 border-2 border-[#1e293b] rounded-full shadow-[0_0_8px_rgba(34,211,238,0.6)]"></div>
            </div>
            <div className="min-w-0">
              <h4 className="text-sm font-black text-white leading-tight truncate">
                {user.name}
              </h4>
              <p className="text-[9px] font-black font-mono text-cyan-500/60 uppercase tracking-[0.2em] mt-0.5">
                @{user.login}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 mb-6">
            <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800/50">
              <div className="flex items-center justify-center gap-1.5 text-slate-500 mb-1">
                <GitCommit size={12} />
                <span className="text-[9px] font-black uppercase tracking-tighter">Entregas</span>
              </div>
              <div className="text-xl font-black text-white text-center">{user.commitCount}</div>
            </div>
            <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800/50">
              <div className="flex items-center justify-center gap-1.5 text-slate-500 mb-1">
                <MessageSquare size={12} />
                <span className="text-[9px] font-black uppercase tracking-tighter">Demandas</span>
              </div>
              <div className="text-xl font-black text-white text-center">{user.issueCount}</div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800">
            <p className="text-[8px] font-black text-slate-500 uppercase tracking-widest mb-1.5">Último Despacho</p>
            <p className="text-[11px] text-slate-400 font-medium leading-relaxed italic truncate group-hover:text-cyan-100 transition-colors">
              "{user.recentMsg}"
            </p>
          </div>
        </motion.div>
      ))}
    </div>
  );
};
