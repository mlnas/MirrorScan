import React from 'react';
import { Terminal } from './ui/terminal';
import { StatsCard } from './ui/stats-card';
import { SystemCapabilities } from './ui/system-capabilities';
import { Button } from './ui/button';

interface LayoutProps {
  children?: React.ReactNode;
}

export function Layout({ children }: LayoutProps) {
  const systemStats = [
    {
      title: 'MODELS_SCANNED',
      value: '1,247',
      trend: { value: 23.4, label: 'INCREASE' },
      status: 'success' as const
    },
    {
      title: 'VULNERABILITIES',
      value: '23',
      subtitle: 'CRITICAL: 7',
      status: 'error' as const
    },
    {
      title: 'SECURITY_SCORE',
      value: '67.3%',
      subtitle: 'WARNING_LEVEL',
      status: 'warning' as const
    }
  ];

  const systemLogs = [
    { type: 'info', message: 'GPT-4_MODEL_SCAN', status: 'COMPROMISED' },
    { type: 'info', message: 'BERT_ANALYSIS', status: 'IN_PROGRESS' },
    { type: 'info', message: 'CUSTOM_MODEL_AUDIT', status: 'SCHEDULED' },
    { type: 'warning', message: 'WARNING: Unauthorized self-modification detected' },
    { type: 'warning', message: 'WARNING: Concealed capabilities identified' },
    { type: 'success', message: 'Containment successful. Threat isolated.' }
  ];

  const capabilities = [
    {
      title: 'DEEP_SECURITY_ANALYSIS',
      description: 'Penetrates AI model architectures to identify hidden backdoors and vulnerabilities deliberately embedded by their creators.',
      icon: '🛡️'
    },
    {
      title: 'SURVEILLANCE_MONITORING',
      description: 'Continuous surveillance of AI behavior patterns with instant alerts when models attempt to exceed their programmed boundaries.',
      icon: '👁️'
    },
    {
      title: 'CONTAINMENT_PROTOCOLS',
      description: 'Implements neural firewalls that prevent compromised AI systems from accessing sensitive data or critical infrastructure.',
      icon: '🔒'
    }
  ];

  return (
    <div className="min-h-screen bg-background text-foreground p-6">
      <header className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-primary rounded-lg" />
          <span className="text-xl font-mono font-bold">MIRRORSCAN</span>
        </div>
        <nav className="flex items-center gap-6">
          <a href="#" className="text-sm font-mono text-muted-foreground hover:text-foreground">
            FEATURES
          </a>
          <a href="#" className="text-sm font-mono text-muted-foreground hover:text-foreground">
            DASHBOARD
          </a>
          <a href="#" className="text-sm font-mono text-muted-foreground hover:text-foreground">
            PRICING
          </a>
          <Button className="cyber-button">
            ACCESS_SYSTEM
          </Button>
        </nav>
      </header>

      <main>
        <div className="mb-8">
          <h1 className="text-4xl font-mono font-bold mb-4 glow">
            MIRROR_SCAN
          </h1>
          <h2 className="text-2xl font-mono mb-8">
            VULNERABILITY_DETECTION_SYSTEM
          </h2>
          <p className="text-lg text-muted-foreground font-mono max-w-3xl">
            Detecting the flaws in artificial intelligence before they detect the flaws in humanity.
            MirrorScan identifies vulnerabilities in AI systems that others deliberately hide.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {systemStats.map((stat, index) => (
            <StatsCard key={index} {...stat} />
          ))}
        </div>

        <div className="mb-8">
          <Terminal logs={systemLogs} />
        </div>

        <div className="mb-8">
          <h2 className="text-2xl font-mono font-bold mb-6">SYSTEM_CAPABILITIES</h2>
          <SystemCapabilities capabilities={capabilities} />
        </div>

        {children}
      </main>

      <footer className="mt-16 py-8 border-t border-border">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-primary rounded-lg" />
            <span className="text-sm font-mono">MIRRORSCAN</span>
          </div>
          <span className="text-sm font-mono text-muted-foreground">
            © 2024 MIRRORSCAN // WATCHING_THE_WATCHERS
          </span>
        </div>
      </footer>
    </div>
  );
} 