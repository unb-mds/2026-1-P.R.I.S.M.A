import React, { useState, useEffect } from 'react';
import { GitHubDiff } from '../lib/types';
import { compareCommits } from '../lib/github';
import { GitCompare, Code2, Plus, Minus, RefreshCw } from 'lucide-react';

interface DiffSectionProps {
  baseSha: string | null;
  headSha: string | null;
}

export const DiffSection: React.FC<DiffSectionProps> = ({ baseSha, headSha }) => {
  const [diff, setDiff] = useState<GitHubDiff | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (baseSha && headSha) {
      const fetchDiff = async () => {
        setLoading(true);
        setError(null);
        try {
          // Comparison is always from Base to Head
          // GitHub compare API: base...head
          const data = await compareCommits(baseSha, headSha);
          setDiff(data);
        } catch (err) {
          setError('Erro ao buscar diff de comparação.');
        } finally {
          setLoading(false);
        }
      };
      fetchDiff();
    }
  }, [baseSha, headSha]);

  if (!baseSha || !headSha) {
    return (
      <div className="p-12 text-center border-2 border-dashed border-slate-800 rounded-2xl opacity-50 bg-slate-900/20">
        <GitCompare className="mx-auto mb-4 text-slate-700" size={48} />
        <h3 className="text-sm font-black text-slate-600 uppercase tracking-[0.2em] mb-2">Comparação em Espera</h3>
        <p className="text-xs text-slate-600 font-medium">Capture dois pontos na linha do tempo para comparar deltas.</p>
      </div>
    );
  }

  if (loading) return (
    <div className="p-12 text-center">
      <RefreshCw className="mx-auto mb-6 animate-spin text-cyan-500" size={32} />
      <p className="text-xs font-black uppercase tracking-[0.3em] text-cyan-500/60 animate-pulse">Extraindo Metadados...</p>
    </div>
  );
  
  if (error) return <div className="p-8 text-center text-red-400 text-sm bg-red-900/20 border border-red-500/20 rounded-xl font-bold uppercase tracking-widest">{error}</div>;
  if (!diff) return null;

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between p-6 bg-[#1e293b] border border-slate-800 rounded-2xl shadow-2xl relative overflow-hidden">
        <div className="absolute left-0 top-0 bottom-0 w-1.5 bg-cyan-500 shadow-[0_0_15px_rgba(34,211,238,0.5)]"></div>
        <div className="flex flex-col gap-4">
          <div className="flex items-center gap-4 group">
            <div className="px-2 py-1 bg-slate-900 rounded-[4px] text-[8px] font-black font-mono text-slate-500 tracking-widest group-hover:bg-slate-800 transition-colors">DE</div>
            <code className="text-xs font-black text-slate-400 tracking-wider font-mono">{baseSha.substring(0, 12)}</code>
          </div>
          <div className="flex items-center gap-4 group">
            <div className="px-2 py-1 bg-cyan-500/10 rounded-[4px] text-[8px] font-black font-mono text-cyan-500 tracking-widest group-hover:bg-cyan-500/20 transition-colors">PARA</div>
            <code className="text-xs font-black text-white underline decoration-cyan-500 shadow-cyan-500/20 font-mono tracking-wider">#{headSha.substring(0, 12)}</code>
          </div>
        </div>
        <div className="flex gap-6 mt-6 md:mt-0">
          <div className="px-4 py-2 bg-emerald-500/10 rounded-xl flex items-center gap-2 border border-emerald-500/20">
            <Plus size={14} className="text-emerald-500" /> 
            <span className="text-sm font-black font-mono text-emerald-400 tabular-nums">{diff.stats?.additions ?? 0}</span>
          </div>
          <div className="px-4 py-2 bg-rose-500/10 rounded-xl flex items-center gap-2 border border-rose-500/20">
            <Minus size={14} className="text-rose-500" /> 
            <span className="text-sm font-black font-mono text-rose-400 tabular-nums">{diff.stats?.deletions ?? 0}</span>
          </div>
        </div>
      </div>

      <div className="space-y-8 max-h-[800px] overflow-y-auto pr-4 scrollbar-thin scrollbar-thumb-slate-800">
        {diff.files.map((file) => (
          <div key={file.filename} className="bg-[#0b0f19] rounded-2xl overflow-hidden shadow-2xl border border-slate-800 group hover:border-slate-700 transition-colors">
            <div className="bg-slate-900/80 px-6 py-4 border-b border-slate-800 flex items-center justify-between backdrop-blur-sm">
              <div className="flex items-center gap-3 overflow-hidden">
                <div className="p-2 bg-slate-800 rounded-lg text-cyan-400 group-hover:scale-110 transition-transform">
                  <Code2 size={14} />
                </div>
                <span className="text-xs font-mono font-black text-slate-300 truncate tracking-tight">{file.filename}</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="flex gap-2">
                   <div className="text-[10px] font-black text-emerald-500/70">+{file.additions}</div>
                   <div className="text-[10px] font-black text-rose-500/70">-{file.deletions}</div>
                </div>
                <span className={`text-[9px] font-black px-2 py-1 rounded-[4px] uppercase tracking-widest ${
                  file.status === 'modified' ? 'bg-cyan-500/10 text-cyan-500 border border-cyan-500/20' : 
                  file.status === 'added' ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-500 border border-rose-500/20'
                }`}>
                  {file.status === 'modified' ? 'modificado' : file.status === 'added' ? 'adicionado' : 'removido'}
                </span>
              </div>
            </div>
            {file.patch ? (
              <div className="p-4 overflow-x-auto text-[11px] font-mono leading-relaxed bg-[#0d1117]">
                {file.patch.split('\n').map((line, i) => {
                  const isAdd = line.startsWith('+');
                  const isDel = line.startsWith('-');
                  const isHeader = line.startsWith('@@');
                  
                  return (
                    <div 
                      key={i} 
                      className={`
                        whitespace-pre flex gap-2 w-full px-2 py-0.5
                        ${isAdd ? 'bg-emerald-950/40 text-emerald-300 border-l-2 border-emerald-500' : ''} 
                        ${isDel ? 'bg-rose-950/40 text-rose-300 border-l-2 border-rose-500' : ''} 
                        ${isHeader ? 'text-cyan-600 font-black opacity-80 mt-4 bg-cyan-950/10' : ''}
                        ${!isAdd && !isDel && !isHeader ? 'text-slate-400' : ''}
                      `}
                    >
                      <span className="w-4 select-none opacity-30 inline-block text-right">{i+1}</span>
                      <span className="flex-1">{line}</span>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="p-8 text-center text-[10px] text-slate-500 italic">Arquivo binário ou muito grande para visualizar diff.</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
