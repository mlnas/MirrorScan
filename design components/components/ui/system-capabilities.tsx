import React from 'react';
import { Card } from './card';

interface Capability {
  title: string;
  description: string;
  icon: React.ReactNode;
}

interface SystemCapabilitiesProps {
  capabilities: Capability[];
  className?: string;
}

export function SystemCapabilities({ capabilities, className = '' }: SystemCapabilitiesProps) {
  return (
    <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 ${className}`}>
      {capabilities.map((capability, index) => (
        <Card 
          key={index}
          className="cyber-card hover:border-primary transition-colors duration-200"
        >
          <div className="p-6">
            <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
              <div className="text-primary">{capability.icon}</div>
            </div>
            
            <h3 className="text-lg font-mono font-bold mb-2 text-foreground">
              {capability.title}
            </h3>
            
            <p className="text-sm text-muted-foreground font-mono leading-relaxed">
              {capability.description}
            </p>
          </div>
        </Card>
      ))}
    </div>
  );
} 