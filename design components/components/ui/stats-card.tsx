import React from 'react';
import { Card } from './card';

interface StatsCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: {
    value: number;
    label: string;
  };
  status?: 'success' | 'warning' | 'error';
  className?: string;
}

export function StatsCard({
  title,
  value,
  subtitle,
  trend,
  status,
  className = ''
}: StatsCardProps) {
  return (
    <Card className={`cyber-card ${className}`}>
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-mono text-muted-foreground">{title}</h3>
        {status && (
          <div className={`status-dot ${status}`} />
        )}
      </div>
      
      <div className="flex items-baseline gap-2">
        <div className="text-3xl font-mono font-bold glow">
          {value}
        </div>
        {trend && (
          <div className={`text-sm font-mono ${
            trend.value > 0 ? 'text-success' : 'text-destructive'
          }`}>
            {trend.value > 0 ? '+' : ''}{trend.value}% {trend.label}
          </div>
        )}
      </div>
      
      {subtitle && (
        <p className="text-sm font-mono text-muted-foreground mt-2">
          {subtitle}
        </p>
      )}
    </Card>
  );
} 