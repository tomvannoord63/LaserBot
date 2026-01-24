import React from 'react';
import { Gauge, Zap } from 'lucide-react';

interface SpeedControlProps {
  speed: number;
  acceleration: number;
  onSpeedChange: (value: number) => void;
  onAccelerationChange: (value: number) => void;
  onApply: () => void;
  disabled?: boolean;
  loading?: boolean;
}

export const SpeedControl: React.FC<SpeedControlProps> = ({
  speed,
  acceleration,
  onSpeedChange,
  onAccelerationChange,
  onApply,
  disabled = false,
  loading = false,
}) => {
  return (
    <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700/50">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <Gauge className="h-6 w-6 text-purple-400" />
          <h2 className="text-2xl font-bold text-white">Motor Speed Control</h2>
        </div>
        <button
          onClick={onApply}
          disabled={disabled || loading}
          className="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg
                   transition-colors disabled:opacity-50 disabled:cursor-not-allowed
                   flex items-center space-x-2"
        >
          <Zap className="h-4 w-4" />
          <span>{loading ? 'Applying...' : 'Apply Speed'}</span>
        </button>
      </div>

      <div className="space-y-6">
        {/* Speed Slider */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-gray-300">
              Motor Speed
            </label>
            <span className="text-sm text-purple-400 font-mono bg-purple-500/10 px-3 py-1 rounded-lg">
              {speed}%
            </span>
          </div>
          <input
            type="range"
            min="10"
            max="100"
            step="5"
            value={speed}
            onChange={(e) => onSpeedChange(parseInt(e.target.value))}
            disabled={disabled}
            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer
                     disabled:opacity-50 disabled:cursor-not-allowed
                     [&::-webkit-slider-thumb]:appearance-none
                     [&::-webkit-slider-thumb]:w-4
                     [&::-webkit-slider-thumb]:h-4
                     [&::-webkit-slider-thumb]:rounded-full
                     [&::-webkit-slider-thumb]:bg-purple-500
                     [&::-webkit-slider-thumb]:cursor-pointer
                     [&::-webkit-slider-thumb]:hover:bg-purple-400
                     [&::-moz-range-thumb]:w-4
                     [&::-moz-range-thumb]:h-4
                     [&::-moz-range-thumb]:rounded-full
                     [&::-moz-range-thumb]:bg-purple-500
                     [&::-moz-range-thumb]:border-0
                     [&::-moz-range-thumb]:cursor-pointer
                     [&::-moz-range-thumb]:hover:bg-purple-400"
          />
          <p className="text-xs text-gray-400">
            How fast the motors move between positions (10% = slowest, 100% = fastest)
          </p>
        </div>

        {/* Acceleration Slider */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-gray-300">
              Acceleration
            </label>
            <span className="text-sm text-purple-400 font-mono bg-purple-500/10 px-3 py-1 rounded-lg">
              {acceleration}%
            </span>
          </div>
          <input
            type="range"
            min="10"
            max="100"
            step="5"
            value={acceleration}
            onChange={(e) => onAccelerationChange(parseInt(e.target.value))}
            disabled={disabled}
            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer
                     disabled:opacity-50 disabled:cursor-not-allowed
                     [&::-webkit-slider-thumb]:appearance-none
                     [&::-webkit-slider-thumb]:w-4
                     [&::-webkit-slider-thumb]:h-4
                     [&::-webkit-slider-thumb]:rounded-full
                     [&::-webkit-slider-thumb]:bg-purple-500
                     [&::-webkit-slider-thumb]:cursor-pointer
                     [&::-webkit-slider-thumb]:hover:bg-purple-400
                     [&::-moz-range-thumb]:w-4
                     [&::-moz-range-thumb]:h-4
                     [&::-moz-range-thumb]:rounded-full
                     [&::-moz-range-thumb]:bg-purple-500
                     [&::-moz-range-thumb]:border-0
                     [&::-moz-range-thumb]:cursor-pointer
                     [&::-moz-range-thumb]:hover:bg-purple-400"
          />
          <p className="text-xs text-gray-400">
            How quickly the motors speed up and slow down (10% = smooth, 100% = snappy)
          </p>
        </div>

      </div>
    </div>
  );
};
