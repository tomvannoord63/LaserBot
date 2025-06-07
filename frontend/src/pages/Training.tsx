import React, { useState, useEffect, useRef } from 'react';
import { Plus, Trash2, Save, Play, RotateCcw } from 'lucide-react';
import { LaserPosition } from '../types/robot';
import { robotApi } from '../services/robotApi';
import { ControlButton } from '../components/ControlButton';

export const Training: React.FC = () => {
  const [positions, setPositions] = useState<LaserPosition[]>([]);
  const [selectedPosition, setSelectedPosition] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const canvasRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadPositions();
  }, []);

  const loadPositions = async () => {
    try {
      const data = await robotApi.getPositions();
      setPositions(data.positions || []);
    } catch (err) {
      setError('Failed to load positions');
      console.error('Load positions error:', err);
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
      await robotApi.moveLaser(position.x, position.y);
    } catch (err) {
      setError('Failed to test position');
    }
  };

  const clearAllPositions = () => {
    setPositions([]);
    setSelectedPosition(null);
  };

  const handleCanvasClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!canvasRef.current) return;
    
    const rect = canvasRef.current.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    
    addPosition(x, y);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700/50">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-white">Laser Position Training</h2>
            <p className="text-gray-400">Click on the training area to add laser positions</p>
          </div>
          <div className="flex space-x-3">
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
          Positions: {positions.length} | Selected: {selectedPosition ? positions.find(p => p.id === selectedPosition)?.name : 'None'}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Training Canvas */}
        <div className="lg:col-span-2">
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700/50">
            <h3 className="text-lg font-semibold text-white mb-4">Training Area</h3>
            <div
              ref={canvasRef}
              onClick={handleCanvasClick}
              className="relative w-full h-96 bg-gradient-to-br from-gray-900 to-gray-800 rounded-xl border-2 border-dashed border-gray-600 cursor-crosshair overflow-hidden"
            >
              {/* Grid lines */}
              <div className="absolute inset-0 opacity-20">
                {[...Array(10)].map((_, i) => (
                  <div key={`v-${i}`} className="absolute w-px h-full bg-gray-500" style={{ left: `${i * 10}%` }} />
                ))}
                {[...Array(10)].map((_, i) => (
                  <div key={`h-${i}`} className="absolute w-full h-px bg-gray-500" style={{ top: `${i * 10}%` }} />
                ))}
              </div>

              {/* Position markers */}
              {positions.map((position) => (
                <div
                  key={position.id}
                  className={`absolute w-4 h-4 rounded-full transform -translate-x-2 -translate-y-2 cursor-pointer transition-all duration-200 ${
                    selectedPosition === position.id
                      ? 'bg-yellow-400 ring-4 ring-yellow-400/30 scale-125'
                      : 'bg-red-500 hover:bg-red-400 hover:scale-110'
                  }`}
                  style={{
                    left: `${position.x}%`,
                    top: `${position.y}%`,
                  }}
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedPosition(position.id);
                  }}
                  title={position.name}
                />
              ))}

              {/* Center indicator */}
              <div className="absolute top-1/2 left-1/2 w-2 h-2 bg-blue-400 rounded-full transform -translate-x-1 -translate-y-1 opacity-50" />
            </div>
            <p className="text-sm text-gray-400 mt-2">
              Click anywhere to add a new laser position. Click existing positions to select them.
            </p>
          </div>
        </div>

        {/* Position List */}
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700/50">
          <h3 className="text-lg font-semibold text-white mb-4">Positions</h3>
          
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {positions.length === 0 ? (
              <div className="text-center text-gray-400 py-8">
                <Plus className="h-8 w-8 mx-auto mb-2 opacity-50" />
                <p>No positions yet</p>
                <p className="text-sm">Click on the training area to add some</p>
              </div>
            ) : (
              positions.map((position, index) => (
                <div
                  key={position.id}
                  className={`bg-gray-700/50 rounded-xl p-4 border transition-all duration-200 ${
                    selectedPosition === position.id
                      ? 'border-yellow-400/50 bg-yellow-400/10'
                      : 'border-gray-600/50 hover:border-gray-500/50'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <input
                      type="text"
                      value={position.name}
                      onChange={(e) => updatePosition(position.id, { name: e.target.value })}
                      className="bg-transparent text-white font-medium text-sm focus:outline-none focus:ring-1 focus:ring-blue-400 rounded px-2 py-1"
                    />
                    <div className="flex space-x-1">
                      <button
                        onClick={() => testPosition(position)}
                        className="p-1 rounded text-blue-400 hover:text-blue-300 hover:bg-blue-400/10"
                        title="Test position"
                      >
                        <Play className="h-3 w-3" />
                      </button>
                      <button
                        onClick={() => deletePosition(position.id)}
                        className="p-1 rounded text-red-400 hover:text-red-300 hover:bg-red-400/10"
                        title="Delete position"
                      >
                        <Trash2 className="h-3 w-3" />
                      </button>
                    </div>
                  </div>
                  
                  <div className="text-xs text-gray-400 space-y-1">
                    <div className="flex justify-between">
                      <span>X: {position.x.toFixed(1)}%</span>
                      <span>Y: {position.y.toFixed(1)}%</span>
                    </div>
                    <div>
                      <label className="block text-xs mb-1">Duration (ms):</label>
                      <input
                        type="number"
                        value={position.duration || 2000}
                        onChange={(e) => updatePosition(position.id, { duration: parseInt(e.target.value) })}
                        className="w-full bg-gray-600/50 text-white text-xs rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-blue-400"
                        min="100"
                        max="10000"
                        step="100"
                      />
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};