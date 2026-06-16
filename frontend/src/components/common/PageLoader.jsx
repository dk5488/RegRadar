import React from 'react';
import { Spinner } from './Spinner';

export const PageLoader = ({ message = 'Loading...' }) => {
  return (
    <div 
      className="page-loader" 
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '60vh',
        width: '100%',
        gap: 'var(--space-4)'
      }}
    >
      <Spinner size="lg" />
      <p className="text-muted" style={{ fontSize: 'var(--text-sm)' }}>{message}</p>
    </div>
  );
};
