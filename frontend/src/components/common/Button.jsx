import React from 'react';
import { Spinner } from './Spinner';

export const Button = ({ 
  children, 
  isLoading = false, 
  variant = 'primary', 
  size = 'md', 
  className = '', 
  disabled, 
  ...props 
}) => {
  const baseClass = `btn btn-${variant} btn-${size} ${className}`;
  
  return (
    <button 
      className={baseClass} 
      disabled={isLoading || disabled} 
      {...props}
    >
      {isLoading && <Spinner size="sm" style={{ marginRight: 'var(--space-2)', width: '16px', height: '16px', borderWidth: '2px' }} />}
      {children}
    </button>
  );
};
