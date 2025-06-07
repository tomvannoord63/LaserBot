import React from 'react';
import { Play, Square, Wifi, WifiOff, Zap, ZapOff, RefreshCw, AlertCircle } from 'lucide-react';
import { useRobotStatus } from '../hooks/useRobotStatus';
import { StatusIndicator } from '../components/StatusIndicator';
import { ControlButton } from '../components/ControlButton';

export const Dashboard: React.FC = () => {
  const { status, loading, error, connect, disconnect, start, stop, toggleLaser, refresh } = useRobotStatus();

  return (
    <div className="space-y-8">
      {/* Status Section */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700/50">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Robot Status</h2>
          <button
            onClick={refresh}
            disabled={loading}
            className="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 text-gray-300 hover:text-white transition-colors"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-gray-700/30 rounded-xl p-4">
            <StatusIndicator
              status={status.connected ? 'connected' : 'disconnected'}
              label="Connection"
            />
          </div>
          <div className="bg-gray-700/30 rounded-xl p-4">
            <StatusIndicator
              status={status.running ? 'running' : 'stopped'}
              label="Robot Status"
            />
          </div>
          <div className="bg-gray-700/30 rounded-xl p-4">
            <div className="flex items-center space-x-2">
              {status.laserOn ? (
                <Zap className="h-3 w-3 fill-current text-yellow-400" />
              ) : (
                <ZapOff className="h-3 w-3 text-gray-400" />
              )}
              <span className="text-sm text-gray-300">
                Laser: <span className={status.laserOn ? 'text-yellow-400' : 'text-gray-400'}>
                  {status.laserOn ? 'On' : 'Off'}
                </span>
              </span>
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 mb-6">
            <div className="flex items-center space-x-2">
              <AlertCircle className="h-5 w-5 text-red-400" />
              <span className="text-red-300">{error}</span>
            </div>
          </div>
        )}
      </div>

      {/* Control Section */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700/50">
        <h2 className="text-2xl font-bold text-white mb-6">Controls</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Connection Controls */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-300">Connection</h3>
            {status.connected ? (
              <ControlButton
                icon={WifiOff}
                label="Disconnect"
                onClick={disconnect}
                variant="secondary"
                disabled={loading}
                loading={loading}
              />
            ) : (
              <ControlButton
                icon={Wifi}
                label="Connect"
                onClick={connect}
                variant="primary"
                disabled={loading}
                loading={loading}
              />
            )}
          </div>

          {/* Robot Controls */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-300">Robot</h3>
            {status.running ? (
              <ControlButton
                icon={Square}
                label="Stop Robot"
                onClick={stop}
                variant="danger"
                disabled={!status.connected || loading}
                loading={loading}
              />
            ) : (
              <ControlButton
                icon={Play}
                label="Start Robot"
                onClick={start}
                variant="success"
                disabled={!status.connected || loading}
                loading={loading}
              />
            )}
          </div>

          {/* Laser Controls */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-300">Laser</h3>
            <ControlButton
              icon={status.laserOn ? ZapOff : Zap}
              label={status.laserOn ? 'Turn Off Laser' : 'Turn On Laser'}
              onClick={toggleLaser}
              variant={status.laserOn ? 'secondary' : 'primary'}
              disabled={!status.connected || loading}
              loading={loading}
            />
          </div>

          {/* Emergency Stop */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-red-300">Emergency</h3>
            <ControlButton
              icon={Square}
              label="Emergency Stop"
              onClick={stop}
              variant="danger"
              disabled={!status.connected || loading}
              loading={loading}
              size="lg"
            />
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 rounded-2xl p-6 border border-blue-500/20">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-500 p-3 rounded-xl">
              <Wifi className="h-6 w-6 text-white" />
            </div>
            <div>
              <p className="text-blue-300 text-sm">Connection Status</p>
              <p className="text-white text-xl font-bold">
                {status.connected ? 'Online' : 'Offline'}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-500/20 to-green-600/20 rounded-2xl p-6 border border-green-500/20">
          <div className="flex items-center space-x-3">
            <div className="bg-green-500 p-3 rounded-xl">
              <Play className="h-6 w-6 text-white" />
            </div>
            <div>
              <p className="text-green-300 text-sm">Robot State</p>
              <p className="text-white text-xl font-bold">
                {status.running ? 'Active' : 'Idle'}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-yellow-500/20 to-yellow-600/20 rounded-2xl p-6 border border-yellow-500/20">
          <div className="flex items-center space-x-3">
            <div className="bg-yellow-500 p-3 rounded-xl">
              <Zap className="h-6 w-6 text-white" />
            </div>
            <div>
              <p className="text-yellow-300 text-sm">Laser Status</p>
              <p className="text-white text-xl font-bold">
                {status.laserOn ? 'Active' : 'Off'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};