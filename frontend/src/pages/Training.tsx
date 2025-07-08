import { Move, Play, Plus, RotateCcw, Save, Trash2, Zap, ZapOff } from 'lucide-react';
import React, { useEffect, useRef, useState } from 'react';
import { ControlButton } from '../components/ControlButton';
import { robotApi } from '../services/robotApi';
import { LaserPosition } from '../types/robot';

export const Training: React.FC = () => {
  const [positions, setPositions] = useState<LaserPosition[]>([]);
  const [selectedPosition, setSelectedPosition] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [laserOn, setLaserOn] = useState(false);
  const [movingToPosition, setMovingToPosition] = useState<string | null>(null);
  const [robotConnected, setRobotConnected] = useState(false);
  const canvasRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadPositions();
    loadRobotStatus();

    // Set up periodic status refresh
    const statusInterval = setInterval(loadRobotStatus, 5000);

    return () => {
      clearInterval(statusInterval);
    };
  }, []);

  const loadPositions = async () => {
    try {
      const data = await robotApi.getPositions();
      setPositions(data || []);
    } catch (err) {
      setError('Failed to load positions');
      console.error('Load positions error:', err);
    }
  };

  const loadRobotStatus = async () => {
    try {
      const status = await robotApi.getRobotStatus();
      setLaserOn(status.laser_on || false);
      setRobotConnected(status.connected || false);
    } catch (err) {
      console.error('Load robot status error:', err);
      setRobotConnected(false);
    }
  };

  const savePositions = async () => {
    setLoading(true);
    try {
      await robotApi.savePositions(positions);
      setError(null);
    } catch (err) {
      setError('Failed to save positions');
    } finally {
      setLoading(false);
    }
  };

  const addPosition = (x: number, y: number) => {
    const newPosition: LaserPosition = {
      id: `pos_${Date.now()}`,
      x: Math.round(x),
      y: Math.round(y),
      name: `Position ${positions.length + 1}`,
      duration: 2000,
    };
    setPositions([...positions, newPosition]);

    // Auto-select the new position
    setSelectedPosition(newPosition.id);

    // Auto-scroll to the bottom after a short delay to ensure the DOM has updated
    setTimeout(() => {
      const container = document.querySelector('.max-h-96.overflow-y-auto');
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    }, 100);
  };

  const deletePosition = (id: string) => {
    setPositions(positions.filter(pos => pos.id !== id));
    if (selectedPosition === id) {
      setSelectedPosition(null);
    }
  };

  const updatePosition = (id: string, updates: Partial<LaserPosition>) => {
    setPositions(positions.map(pos =>
      pos.id === id ? { ...pos, ...updates } : pos
    ));
  };

  const testPosition = async (position: LaserPosition) => {
    try {
      setMovingToPosition(position.id);
      await robotApi.moveLaser(position.x, position.y);
      setError(null);
      // Refresh robot status to get updated position
      await loadRobotStatus();
    } catch (err) {
      setError('Failed to move to position');
    } finally {
      setMovingToPosition(null);
    }
  };

  const moveToSelectedPosition = async () => {
    if (!selectedPosition) return;

    const position = positions.find(p => p.id === selectedPosition);
    if (!position) return;

    try {
      setMovingToPosition(selectedPosition);
      await robotApi.moveLaser(position.x, position.y);
      setError(null);
      // Refresh robot status to get updated position
      await loadRobotStatus();
    } catch (err) {
      setError('Failed to move to selected position');
    } finally {
      setMovingToPosition(null);
    }
  };

  const toggleLaser = async () => {
    try {
      await robotApi.toggleLaser(!laserOn);
      setLaserOn(!laserOn);
      setError(null);
      // Refresh robot status to confirm laser state
      await loadRobotStatus();
    } catch (err) {
      setError('Failed to toggle laser');
    }
  };

  const clearAllPositions = () => {
    setPositions([]);
    setSelectedPosition(null);
  };

  const handleCanvasClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!canvasRef.current) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 200 - 100;
    const y = ((e.clientY - rect.top) / rect.height) * 200 - 100;

    addPosition(x, y);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700/50">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-white">Laser Position Training</h2>
            <p className="text-gray-400">Manage laser positions and test robot movements</p>
          </div>
          <div className="flex space-x-3">
            <ControlButton
              icon={laserOn ? ZapOff : Zap}
              label={laserOn ? "Laser Off" : "Laser On"}
              onClick={toggleLaser}
              variant={laserOn ? "danger" : "success"}
              disabled={!robotConnected}
              size="sm"
            />
            <ControlButton
              icon={Move}
              label="Move to Selected"
              onClick={moveToSelectedPosition}
              variant="primary"
              disabled={!selectedPosition || movingToPosition !== null || !robotConnected}
              loading={movingToPosition === selectedPosition}
              size="sm"
            />
            <ControlButton
              icon={Save}
              label="Save"
              onClick={savePositions}
              variant="success"
              disabled={loading}
              loading={loading}
              size="sm"
            />
            <ControlButton
              icon={RotateCcw}
              label="Clear All"
              onClick={clearAllPositions}
              variant="danger"
              size="sm"
            />
          </div>
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 mb-4">
            <span className="text-red-300">{error}</span>
          </div>
        )}

        <div className="text-sm text-gray-400">
          Positions: {positions.length} | Selected: {selectedPosition ? positions.find(p => p.id === selectedPosition)?.name : 'None'} |
          Robot: <span className={robotConnected ? 'text-green-400' : 'text-red-400'}>{robotConnected ? 'Connected' : 'Disconnected'}</span> |
          Laser: <span className={laserOn ? 'text-red-400' : 'text-gray-400'}>{laserOn ? 'ON' : 'OFF'}</span>
        </div>
      </div>

      {/* Position List */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700/50">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-white">Laser Positions</h3>
          <div className="text-sm text-gray-400">
            Robot angles: A1 (horizontal) and A2 (vertical) in degrees
          </div>
        </div>

        <div className="space-y-3 max-h-96 overflow-y-auto">
          {positions.length === 0 ? (
            <div className="text-center text-gray-400 py-12">
              <Plus className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p className="text-lg font-medium mb-2">No positions yet</p>
              <p className="text-sm">Add positions manually or import from a file</p>
            </div>
          ) : (
            positions.map((position, index) => (
              <div
                key={position.id}
                className={`bg-gray-700/50 rounded-xl p-4 border transition-all duration-200 ${selectedPosition === position.id
                  ? 'border-yellow-400/50 bg-yellow-400/10'
                  : 'border-gray-600/50 hover:border-gray-500/50'
                  }`}
              >
                <div className="flex items-center justify-between mb-3">
                  <input
                    type="text"
                    value={position.name}
                    onChange={(e) => updatePosition(position.id, { name: e.target.value })}
                    className="bg-transparent text-white font-medium text-base focus:outline-none focus:ring-1 focus:ring-blue-400 rounded px-2 py-1"
                  />
                  <div className="flex space-x-2">
                    <button
                      onClick={() => testPosition(position)}
                      className="p-2 rounded text-blue-400 hover:text-blue-300 hover:bg-blue-400/10 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                      title="Move to position"
                      disabled={movingToPosition !== null || !robotConnected}
                    >
                      {movingToPosition === position.id ? (
                        <div className="h-4 w-4 animate-spin rounded-full border border-blue-400 border-t-transparent" />
                      ) : (
                        <Move className="h-4 w-4" />
                      )}
                    </button>
                    <button
                      onClick={() => testPosition(position)}
                      className="p-2 rounded text-green-400 hover:text-green-300 hover:bg-green-400/10 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                      title="Test position"
                      disabled={movingToPosition !== null || !robotConnected}
                    >
                      {movingToPosition === position.id ? (
                        <div className="h-4 w-4 animate-spin rounded-full border border-green-400 border-t-transparent" />
                      ) : (
                        <Play className="h-4 w-4" />
                      )}
                    </button>
                    <button
                      onClick={() => deletePosition(position.id)}
                      className="p-2 rounded text-red-400 hover:text-red-300 hover:bg-red-400/10 transition-colors"
                      title="Delete position"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="space-y-2">
                    <div>
                      <label className="block text-gray-400 text-xs mb-1">A1 (Horizontal):</label>
                      <input
                        type="number"
                        value={position.x}
                        onChange={(e) => updatePosition(position.id, { x: parseFloat(e.target.value) || 0 })}
                        className="w-full bg-gray-600/50 text-white text-sm rounded px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-400 font-mono"
                        step="0.1"
                        min="-180"
                        max="180"
                      />
                    </div>
                    <div>
                      <label className="block text-gray-400 text-xs mb-1">A2 (Vertical):</label>
                      <input
                        type="number"
                        value={position.y}
                        onChange={(e) => updatePosition(position.id, { y: parseFloat(e.target.value) || 0 })}
                        className="w-full bg-gray-600/50 text-white text-sm rounded px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-400 font-mono"
                        step="0.1"
                        min="-180"
                        max="180"
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div>
                      <label className="block text-gray-400 text-xs mb-1">Duration (ms):</label>
                      <input
                        type="number"
                        value={position.duration || 2000}
                        onChange={(e) => updatePosition(position.id, { duration: parseInt(e.target.value) })}
                        className="w-full bg-gray-600/50 text-white text-sm rounded px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-400"
                        min="100"
                        max="10000"
                        step="100"
                      />
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Add Position Button */}
        <div className="mt-4 pt-4 border-t border-gray-600/50">
          <button
            onClick={() => addPosition(0, 0)}
            className="w-full bg-blue-500/20 hover:bg-blue-500/30 text-blue-300 hover:text-blue-200 border border-blue-500/30 hover:border-blue-500/50 rounded-xl p-4 transition-all duration-200 flex items-center justify-center space-x-2"
          >
            <Plus className="h-5 w-5" />
            <span className="font-medium">Add New Position</span>
          </button>
        </div>
      </div>
    </div>
  );
};