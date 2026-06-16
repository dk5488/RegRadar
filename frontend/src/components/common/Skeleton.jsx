import React from 'react';

export const Skeleton = ({ width, height, borderRadius, className = '', style = {} }) => {
  return (
    <div
      className={`skeleton ${className}`}
      style={{
        width: width || '100%',
        height: height || '20px',
        borderRadius: borderRadius || 'var(--radius-md)',
        ...style
      }}
      aria-hidden="true"
    />
  );
};

export const SkeletonCard = () => (
  <div className="surface-card" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
    <Skeleton height="24px" width="60%" />
    <Skeleton height="16px" width="40%" />
    <Skeleton height="60px" width="100%" />
    <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 'var(--space-2)' }}>
      <Skeleton height="32px" width="80px" borderRadius="var(--radius-full)" />
      <Skeleton height="32px" width="100px" />
    </div>
  </div>
);

export const SkeletonRow = () => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)', padding: 'var(--space-3) 0', borderBottom: '1px solid var(--border-secondary)' }}>
    <Skeleton height="40px" width="40px" borderRadius="50%" />
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
      <Skeleton height="16px" width="30%" />
      <Skeleton height="12px" width="20%" />
    </div>
    <Skeleton height="24px" width="60px" borderRadius="var(--radius-full)" />
  </div>
);
