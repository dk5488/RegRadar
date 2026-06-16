import React from 'react';

export const Spinner = ({ size = 'md', className = '' }) => {
  const sizeClass = size === 'lg' ? 'spinner-lg' : size === 'sm' ? 'spinner-sm' : '';
  
  return (
    <div className={`spinner ${sizeClass} ${className}`} role="status" aria-label="Loading">
      <span className="sr-only" style={{ display: 'none' }}>Loading...</span>
    </div>
  );
};
