import { motion } from 'motion/react';
import { 
  SquareDot, 
  Eye, 
  AlertTriangle, 
  Lightbulb, 
  Clock, 
  Building2, 
  Filter, 
  Bot, 
  FastForward, 
  BarChart3, 
  LayoutDashboard,
  Zap, 
  Settings, 
  Users, 
  Cpu,
  ArrowRight,
  ChevronRight
} from 'lucide-react';

interface LandingPageProps {
  onEnterDashboard: () => void;
}

export function LandingPage({ onEnterDashboard }: LandingPageProps) {
  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-200 selection:bg-cyan-500/30">
      {/* Navbar Minimalista */}
      <nav className="fixed top-0 w-full z-50 bg-[#0f172a]/80 backdrop-blur-md border-b border-slate-800/50 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="bg-cyan-500 p-1.5 rounded shadow-[0_0_15px_rgba(34,211,238,0.4)]">
              <SquareDot className="text-slate-900" size={18} />
            </div>
            <span className="font-black tracking-tighter text-white italic uppercase">PRISMA</span>
          </div>
          <div className="hidden md:flex gap-8 text-[10px] font-bold uppercase tracking-widest text-slate-400">
            <a href="#visao" className="hover:text-cyan-400 transition-colors">Visão</a>
            <a href="#problema" className="hover:text-cyan-400 transition-colors">O Problema</a>
            <a href="#funcionalidades" className="hover:text-cyan-400 transition-colors">Funcionalidades</a>
            <a href="#ia" className="hover:text-cyan-400 transition-colors">IA</a>
          </div>
          <button 
            onClick={onEnterDashboard}
            className="px-4 py-1.5 bg-cyan-500/10 border border-cyan-500/30 rounded-full text-[10px] font-black uppercase tracking-widest text-cyan-400 hover:bg-cyan-500 hover:text-slate-900 transition-all"
          >
            Acessar Desenvolvimento
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="relative pt-40 pb-32 px-6 overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-4xl h-[500px] bg-cyan-500/10 blur-[120px] rounded-full pointer-events-none"></div>
        <div className="max-w-4xl mx-auto text-center relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center gap-2 mb-6 bg-cyan-500/10 px-4 py-2 rounded-full border border-cyan-500/20">
              <Zap size={14} className="text-cyan-400" />
              <span className="text-[10px] font-black uppercase tracking-[0.3em] text-cyan-400">Inteligência Legislativa 2.0</span>
            </div>
            <h1 className="text-7xl md:text-9xl font-black italic tracking-tighter mb-6 text-white leading-none">
              PRISMA
            </h1>
            <p className="text-cyan-400 font-mono text-xs md:text-sm uppercase tracking-[0.5em] mb-8 font-bold leading-relaxed px-4">
              A clareza que o processo legislativo precisava
            </p>
            <p className="text-slate-400 max-w-2xl mx-auto mb-12 text-lg md:text-xl font-medium">
              Transformamos a complexidade burocrática em <span className="text-white">insights estratégicos</span>. Identifique gargalos, preveja prazos e monitore a eficiência parlamentar com precisão cirúrgica.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a 
                href="#visao" 
                className="px-8 py-4 bg-cyan-500 text-slate-900 font-black uppercase tracking-widest text-xs rounded-lg shadow-[0_0_30px_rgba(34,211,238,0.4)] hover:scale-105 active:scale-95 transition-all flex items-center justify-center gap-2"
              >
                Explorar Solução
                <ArrowRight size={16} />
              </a>
              <button 
                onClick={onEnterDashboard}
                className="px-8 py-4 bg-[#1e293b] border border-slate-800 font-black uppercase tracking-widest text-xs rounded-lg hover:bg-slate-800 transition-all"
              >
                Acessar Monitoramento
              </button>
            </div>
          </motion.div>
        </div>
      </header>

      {/* Como Começar Section */}
      <section className="py-24 px-6 bg-slate-900/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-xs font-black uppercase tracking-[0.4em] text-cyan-500 mb-4">Guia Rápido</h2>
            <h3 className="text-3xl font-black text-white">Como começar a usar o PRISMA</h3>
          </div>
          <div className="grid md:grid-cols-3 gap-12">
            {[
              {
                icon: <Settings className="text-cyan-500" />,
                title: "1. Configure o Acesso",
                desc: "Insira seu Token de Acesso do Github no painel de desenvolvimento para sincronizar os dados em tempo real."
              },
              {
                icon: <LayoutDashboard className="text-cyan-500" />,
                title: "2. Explore o Dashboard",
                desc: "Acesse a visão analítica para ver o volume de entregas, demandas ativas e o status de saúde do sistema."
              },
              {
                icon: <BarChart3 className="text-cyan-500" />,
                title: "3. Analise Trends",
                desc: "Use o mapa de calor e os logs de atividade para identificar padrões de produtividade e possíveis gargalos."
              }
            ].map((step, i) => (
              <div key={i} className="flex flex-col items-center text-center">
                <div className="w-16 h-16 bg-slate-900 border border-slate-800 rounded-2xl flex items-center justify-center mb-6 shadow-inner">
                  {step.icon}
                </div>
                <h4 className="text-white font-bold mb-4 uppercase text-sm tracking-widest">{step.title}</h4>
                <p className="text-slate-400 text-sm leading-relaxed">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Visão do Produto */}
      <section id="visao" className="py-32 px-6 border-y border-slate-800/50 bg-slate-900/30">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 mb-8 bg-cyan-500/10 px-4 py-2 rounded-full border border-cyan-500/20">
            <Eye size={16} className="text-cyan-500" />
            <span className="text-[10px] font-black uppercase tracking-widest text-cyan-400">Visão do Produto</span>
          </div>
          <h2 className="text-3xl md:text-4xl font-black text-white mb-8 tracking-tight">
            Por que algumas leis avançam rapidamente enquanto outras permanecem paradas por longos períodos?
          </h2>
          <div className="space-y-6 text-slate-400 text-lg leading-relaxed max-w-3xl mx-auto">
            <p>
              O Prisma nasce para tornar o processo legislativo mais transparente e compreensível, revelando padrões, gargalos institucionais e oportunidades de melhoria.
            </p>
            <p className="text-cyan-400 font-medium">
              Mais do que apresentar dados, o Prisma busca gerar insights acionáveis para cidadãos, jornalistas, pesquisadores e gestores públicos.
            </p>
          </div>
        </div>
      </section>

      {/* Problema e Solução */}
      <section id="problema" className="py-32 px-6">
        <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-12">
          <div className="bg-[#1e293b] border border-slate-800 p-10 rounded-3xl relative overflow-hidden group shadow-2xl">
            <div className="absolute top-0 right-0 w-32 h-32 bg-amber-500/5 blur-3xl -mr-16 -mt-16 group-hover:bg-amber-500/10 transition-all"></div>
            <AlertTriangle className="text-amber-500 mb-6" size={40} />
            <h3 className="text-2xl font-black text-white mb-6 uppercase tracking-tight">O Problema</h3>
            <p className="text-slate-400 mb-8 leading-relaxed">
              O processo legislativo é complexo e de difícil análise em escala. Não é simples quantificar a eficiência parlamentar.
            </p>
            <ul className="space-y-4 text-sm font-medium text-slate-300">
                {["Quanto tempo uma lei leva para ser aprovada?", "Onde ocorrem os principais atrasos?", "Quais temas avançam mais rápido?", "Quais etapas são mais demoradas?"].map((t, i) => (
                    <li key={i} className="flex gap-3 items-start">
                        <ChevronRight size={14} className="text-amber-500 mt-1 shrink-0" />
                        {t}
                    </li>
                ))}
            </ul>
          </div>

          <div className="bg-[#1e293b] border border-cyan-500/30 p-10 rounded-3xl relative overflow-hidden group shadow-[0_0_50px_rgba(34,211,238,0.05)]">
            <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/5 blur-3xl -mr-16 -mt-16 group-hover:bg-cyan-500/10 transition-all"></div>
            <Lightbulb className="text-cyan-400 mb-6" size={40} />
            <h3 className="text-2xl font-black text-white mb-6 uppercase tracking-tight">A Solução</h3>
            <p className="text-slate-400 mb-6 leading-relaxed">
              O Prisma organiza e analisa dados legislativos para oferecer uma visão clara do tempo de tramitação, identificando padrões e gargalos.
            </p>
            <p className="text-cyan-400/80 font-medium">
              Transformamos dados dispersos em informações acessíveis, comparáveis e estruturadas para auditoria técnica.
            </p>
          </div>
        </div>
      </section>

      {/* Funcionalidades */}
      <section id="funcionalidades" className="py-32 px-6 bg-slate-900/30 border-y border-slate-800/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-xs font-black uppercase tracking-[0.4em] text-cyan-500 mb-4">Funcionalidades</h2>
            <h3 className="text-4xl font-black text-white tracking-tight">Arquitetura de Análise</h3>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-8 bg-slate-900/50 border border-slate-800 rounded-2xl hover:border-cyan-500/50 transition-all group">
              <Clock className="text-cyan-500 mb-6 group-hover:scale-110 transition-transform" size={32} />
              <h4 className="text-lg font-bold text-white mb-4 uppercase tracking-tighter">Tempo Médio</h4>
              <p className="text-slate-400 text-sm leading-relaxed">
                Visualização do tempo de tramitação segmentado por tipo de projeto (PL, PEC, MPV).
              </p>
            </div>
            <div className="p-8 bg-slate-900/50 border border-slate-800 rounded-2xl hover:border-cyan-500/50 transition-all group">
              <Building2 className="text-cyan-500 mb-6 group-hover:scale-110 transition-transform" size={32} />
              <h4 className="text-lg font-bold text-white mb-4 uppercase tracking-tighter">Análise de Comissões</h4>
              <p className="text-slate-400 text-sm leading-relaxed">
                Mapeamento de quanto tempo os projetos permanecem retidos em cada comissão parlamentar.
              </p>
            </div>
            <div className="p-8 bg-slate-900/50 border border-slate-800 rounded-2xl hover:border-cyan-500/50 transition-all group">
              <Filter className="text-cyan-500 mb-6 group-hover:scale-110 transition-transform" size={32} />
              <h4 className="text-lg font-bold text-white mb-4 uppercase tracking-tighter">Mapeamento de Gargalos</h4>
              <p className="text-slate-400 text-sm leading-relaxed">
                Detecção precisa de instâncias com a maior concentração de atrasos burocráticos.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* IA */}
      <section id="ia" className="py-32 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between mb-20 gap-8">
            <div className="max-w-lg">
              <div className="flex items-center gap-3 mb-6">
                <Bot className="text-purple-500" size={24} />
                <h3 className="text-xs font-black uppercase tracking-[0.2em] text-purple-400">Inteligência Artificial Aplicada</h3>
              </div>
              <h4 className="text-4xl font-black text-white tracking-tight mb-6">Modelagem Preditiva</h4>
              <p className="text-slate-400 lg:text-lg">
                Utilizamos algoritmos avançados para extrair conhecimento de décadas de registros legislativos.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-purple-500/10 border border-purple-500/20 p-6 rounded-2xl">
                 <h5 className="text-white font-black text-2xl mb-1 italic leading-none">99.9%</h5>
                 <p className="text-[10px] text-purple-400 uppercase font-bold tracking-widest">Processamento</p>
              </div>
              <div className="bg-cyan-500/10 border border-cyan-500/20 p-6 rounded-2xl">
                 <h5 className="text-white font-black text-2xl mb-1 italic leading-none">IA Core</h5>
                 <p className="text-[10px] text-cyan-400 uppercase font-bold tracking-widest">Ativo</p>
              </div>
            </div>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
             {[
               { icon: <FastForward size={24}/>, title: "Previsão de Aprovação", desc: "Modelos preditivos que estimam o tempo provável de tramitação com base no histórico." },
               { icon: <BarChart3 size={24}/>, title: "Padrões de Atraso", desc: "Algoritmos de classificação para reconhecimento de comportamentos de retenção." },
               { icon: <Zap size={24}/>, title: "Extração de Insights", desc: "Análise automatizada para descobrir correlações entre áreas temáticas e velocidade." }
             ].map((item, i) => (
                <div key={i} className="p-8 bg-[#1e293b] border border-slate-800 rounded-3xl shadow-xl">
                    <div className="p-3 bg-slate-900 rounded-xl w-fit mb-6 text-cyan-400 border border-slate-800 shadow-inner">
                        {item.icon}
                    </div>
                    <h5 className="text-white font-black uppercase text-sm mb-4 tracking-tighter">{item.title}</h5>
                    <p className="text-slate-400 text-sm leading-relaxed">{item.desc}</p>
                </div>
             ))}
          </div>
        </div>
      </section>

      {/* Metodologia */}
      <section className="py-32 px-6 bg-[#1e293b]/50 border-t border-slate-800">
        <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-20 items-center">
            <div>
                <h3 className="text-xs font-black uppercase tracking-[0.4em] text-cyan-500 mb-8 flex items-center gap-3">
                    <Settings size={18} /> Metodologia
                </h3>
                <div className="space-y-6">
                    {[
                        "Coleta de dados legislativos em APIs públicas.",
                        "Tratamento e sanitização de dados temporais.",
                        "Análise exploratória e extração de métricas.",
                        "Treinamento de modelos preditivos.",
                        "Geração do dashboard interativo."
                    ].map((step, i) => (
                        <div key={i} className="flex gap-4 items-center">
                            <span className="w-8 h-8 rounded-full border border-slate-800 bg-slate-900 flex items-center justify-center text-[10px] font-black text-cyan-500 shrink-0">
                                {i+1}
                            </span>
                            <p className="text-slate-300 font-medium">{step}</p>
                        </div>
                    ))}
                </div>
            </div>
            <div className="bg-slate-900 p-10 rounded-3xl border border-slate-800 shadow-2xl relative">
                <div className="absolute -top-4 -right-4 bg-cyan-500 text-slate-900 px-4 py-1 rounded font-black text-[10px] uppercase tracking-widest shadow-lg">Target: 2026-1</div>
                <h3 className="text-xs font-black uppercase tracking-[0.4em] text-cyan-500 mb-8 flex items-center gap-3 font-mono">
                    <Users size={18} /> Público e Impacto
                </h3>
                <ul className="space-y-6">
                    <li>
                        <strong className="text-white block mb-1">Gestores e Analistas</strong>
                        <p className="text-sm text-slate-400">Otimização de processos e fluxos de decisão.</p>
                    </li>
                    <li>
                        <strong className="text-white block mb-1">Jornalistas e Cidadãos</strong>
                        <p className="text-sm text-slate-400">Transparência ativa e narrativas baseadas em dados.</p>
                    </li>
                    <li className="pt-6 border-t border-slate-800">
                        <p className="text-cyan-400 text-sm font-bold italic">
                            Impacto: Eficiência governamental e suporte à decisão baseada em evidências sólidas.
                        </p>
                    </li>
                </ul>
            </div>
        </div>
      </section>

      {/* Tech Specs */}
      <section className="py-20 text-center px-6">
          <div className="flex justify-center gap-4 mb-8">
            <div className="p-2 bg-slate-900 rounded-lg text-slate-500 border border-slate-800">
                <Cpu size={20} />
            </div>
          </div>
          <h4 className="text-xs font-black uppercase tracking-[0.6em] text-slate-500 mb-4">Especificações Técnicas</h4>
          <p className="text-white font-mono text-sm tracking-widest">
            STACK ANALÍTICA: <span className="text-cyan-400">PYTHON | DATA SCIENCE | MACHINE LEARNING</span>
          </p>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-slate-800 text-center">
          <p className="text-[10px] font-black uppercase tracking-[0.5em] text-slate-600">
            &copy; 2026 PROJETO PRISMA - ENGENHARIA DE SOFTWARE - MDS UNB
          </p>
      </footer>
    </div>
  );
}
