import React from 'react';
import { ScrollArea } from './scroll-area';

interface LogEntry {
  type: 'info' | 'warning' | 'error' | 'success';
  message: string;
  timestamp?: string;
}

interface TerminalProps {
  logs: LogEntry[];
  title?: string;
  className?: string;
}

export function Terminal({ logs, title = 'SYSTEM_LOG', className = '' }: TerminalProps) {
  return (
    <div className={`cyber-card ${className}`} style={{ background: 'var(--terminal-bg)' }}>
      <div className="flex items-center gap-2 mb-4">
        <div className="flex gap-1.5">
          <div className="w-3 h-3 rounded-full bg-[#FF5F56]" />
          <div className="w-3 h-3 rounded-full bg-[#FFBD2E]" />
          <div className="w-3 h-3 rounded-full bg-[#27C93F]" />
        </div>
        <span className="text-sm font-mono text-muted-foreground ml-2">{title}</span>
      </div>
      
      <ScrollArea className="h-[300px] w-full">
        <div className="font-mono text-sm space-y-2">
          {logs.map((log, index) => (
            <div key={index} className="flex items-start">
              <span className="text-terminal-prompt mr-2">$</span>
              <span className={`
                terminal-text
                ${log.type === 'warning' ? 'text-terminal-warning' : ''}
                ${log.type === 'error' ? 'text-destructive' : ''}
                ${log.type === 'success' ? 'text-success' : ''}
              `}>
                {log.message}
                {log.timestamp && (
                  <span className="text-muted-foreground ml-2 text-xs">
                    {log.timestamp}
                  </span>
                )}
              </span>
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
} 