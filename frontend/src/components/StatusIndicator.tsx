import React from 'react';
import { Circle } from 'lucide-react';

interface StatusIndicatorProps {
  status: 'connected' | 'disconnected' | 'running' | 'stopped';
  label: string;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({ status, label }) => {
  const getStatusColor = () => {
    switch (status) {
      case 'connected':
      case 'running':
        return 'text-green-400';
      case 'disconnected':
      case 'stopped':
        return 'text-red-400';
      default:
        return 'text-gray-400';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'connected':
        return 'Connected';
      case 'disconnected':
        return 'Disconnected';
      case 'running':
        return 'Running';
      case 'stopped':
        return 'Stopped';
      default:
        return 'Unknown';
    }
  };

  return (
    <div className="flex items-center space-x-2">
      <Circle className={`h-3 w-3 fill-current ${getStatusColor()}`} />
      <span className="text-sm text-gray-300">
        {label}: <span className={getStatusColor()}>{getStatusText()}</span>
      </span>
    </div>
  );
};