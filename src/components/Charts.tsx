import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
} from 'recharts';
import { format, parseISO, startOfDay, eachDayOfInterval, subDays } from 'date-fns';
import { GitHubCommit, GitHubIssue } from '../lib/types';

interface ChartProps {
  commits: GitHubCommit[];
  issues: GitHubIssue[];
}

export const StatsCharts: React.FC<ChartProps> = ({ commits, issues }) => {
  // Process Commits by Day
  const last30Days = eachDayOfInterval({
    start: startOfDay(subDays(new Date(), 29)),
    end: startOfDay(new Date()),
  });

  const commitData = last30Days.map(day => {
    const dateStr = format(day, 'yyyy-MM-dd');
    const count = commits.filter(c => 
      format(parseISO(c.commit.author.date), 'yyyy-MM-dd') === dateStr
    ).length;
    return { date: format(day, 'dd/MM'), count };
  });

  const issueData = last30Days.map(day => {
    const dateStr = format(day, 'yyyy-MM-dd');
    const opened = issues.filter(i => 
      format(parseISO(i.created_at), 'yyyy-MM-dd') === dateStr
    ).length;
    const closed = issues.filter(i => 
      i.closed_at && format(parseISO(i.closed_at), 'yyyy-MM-dd') === dateStr
    ).length;
    return { date: format(day, 'dd/MM'), opened, closed };
  });

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 p-6 min-h-[350px]">
      <div className="flex flex-col">
        <div className="flex-1 min-h-[250px] w-full">
          <ResponsiveContainer width="100%" height="100%" minHeight={250}>
            <LineChart data={commitData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" />
              <XAxis 
                dataKey="date" 
                fontSize={10} 
                axisLine={false} 
                tickLine={false} 
                tick={{ fill: '#94a3b8' }} 
              />
              <YAxis 
                fontSize={10} 
                axisLine={false} 
                tickLine={false} 
                tick={{ fill: '#94a3b8' }} 
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#111827', 
                  borderRadius: '12px', 
                  border: '1px solid #374151', 
                }}
                itemStyle={{ color: '#22d3ee', fontSize: '12px' }}
                labelStyle={{ color: '#94a3b8', fontSize: '10px', marginBottom: '4px' }}
              />
              <Legend 
                verticalAlign="top" 
                align="right" 
                iconType="circle"
                content={({ payload }) => (
                  <div className="flex gap-4 mb-4 justify-end">
                    {payload?.map((entry: any, index: number) => (
                      <div key={`item-${index}`} className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }} />
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{entry.value}</span>
                      </div>
                    ))}
                  </div>
                )}
              />
              <Line 
                type="monotone" 
                dataKey="count" 
                name="Entregas"
                stroke="#22d3ee" 
                strokeWidth={3} 
                dot={{ fill: '#22d3ee', r: 4, strokeWidth: 2, stroke: '#0f172a' }}
                activeDot={{ r: 6, strokeWidth: 0 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="flex flex-col">
        <div className="flex-1 min-h-[250px] w-full">
          <ResponsiveContainer width="100%" height="100%" minHeight={250}>
            <BarChart data={issueData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" />
              <XAxis 
                dataKey="date" 
                fontSize={10} 
                axisLine={false} 
                tickLine={false} 
                tick={{ fill: '#94a3b8' }} 
              />
              <YAxis 
                fontSize={10} 
                axisLine={false} 
                tickLine={false} 
                tick={{ fill: '#94a3b8' }} 
              />
              <Tooltip 
                cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                contentStyle={{ 
                  backgroundColor: '#111827', 
                  borderRadius: '12px', 
                  border: '1px solid #374151', 
                }}
                itemStyle={{ color: '#f8fafc', fontSize: '12px' }}
                labelStyle={{ color: '#94a3b8', fontSize: '10px', marginBottom: '4px' }}
              />
              <Legend 
                verticalAlign="top" 
                align="right" 
                iconType="circle"
                content={({ payload }) => (
                  <div className="flex gap-4 mb-4 justify-end">
                    {payload?.map((entry: any, index: number) => (
                      <div key={`item-${index}`} className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }} />
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{entry.value}</span>
                      </div>
                    ))}
                  </div>
                )}
              />
              <Bar dataKey="opened" fill="#0891b2" radius={[4, 4, 0, 0]} name="Abertas" />
              <Bar dataKey="closed" fill="#334155" radius={[4, 4, 0, 0]} name="Fechadas" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
