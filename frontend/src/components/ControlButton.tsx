import React from 'react';
import { DivideIcon as LucideIcon } from 'lucide-react';

interface ControlButtonProps {
  icon: LucideIcon;
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary' | 'success' | 'danger';
  disabled?: boolean;
  loading?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export const ControlButton: React.FC<ControlButtonProps> = ({
  icon: Icon,
  label,
  onClick,
  variant = 'primary',
  disabled = false,
  loading = false,
  size = 'md',
}) => {
  const getVariantStyles = () => {
    const baseStyles = 'transition-all duration-200 transform active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed';
    
    switch (variant) {
      case 'primary':
        return `${baseStyles} bg-blue-500 hover:bg-blue-600 text-white shadow-lg hover:shadow-xl`;
      case 'secondary':
        return `${baseStyles} bg-gray-600 hover:bg-gray-700 text-white shadow-lg hover:shadow-xl`;
      case 'success':
        return `${baseStyles} bg-green-500 hover:bg-green-600 text-white shadow-lg hover:shadow-xl`;
      case 'danger':
        return `${baseStyles} bg-red-500 hover:bg-red-600 text-white shadow-lg hover:shadow-xl`;
      default:
        return baseStyles;
    }
  };

  const getSizeStyles = () => {
    switch (size) {
      case 'sm':
        return 'px-4 py-2 text-sm';
      case 'md':
        return 'px-6 py-3 text-base';
      case 'lg':
        return 'px-8 py-4 text-lg';
      default:
        return 'px-6 py-3 text-base';
    }
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className={`flex items-center space-x-3 rounded-xl font-semibold ${getVariantStyles()} ${getSizeStyles()}`}
    >
      <Icon className={`${loading ? 'animate-spin' : ''} ${size === 'sm' ? 'h-4 w-4' : size === 'lg' ? 'h-6 w-6' : 'h-5 w-5'}`} />
      <span>{label}</span>
    </button>
  );
};