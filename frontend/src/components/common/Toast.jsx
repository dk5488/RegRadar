import React, { useEffect, useState } from 'react';
import { FiCheckCircle, FiAlertCircle, FiInfo, FiX, FiAlertTriangle } from 'react-icons/fi';
import { useToast } from '../../hooks/useToast';
import '../../styles/components/Toast.css';

const iconMap = {
  success: <FiCheckCircle />,
  error: <FiAlertCircle />,
  warning: <FiAlertTriangle />,
  info: <FiInfo />,
};

const ToastItem = ({ id, message, type, duration }) => {
  const { removeToast } = useToast();
  const [isRemoving, setIsRemoving] = useState(false);

  useEffect(() => {
    if (duration) {
      const timer = setTimeout(() => {
        handleRemove();
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [duration]);

  const handleRemove = () => {
    setIsRemoving(true);
    setTimeout(() => {
      removeToast(id);
    }, 300); // Wait for fadeOut animation
  };

  return (
    <div className={`toast ${type} ${isRemoving ? 'removing' : ''}`} role="alert">
      <div className="toast-content">
        <span className="toast-icon">{iconMap[type] || iconMap.info}</span>
        <span className="toast-message">{message}</span>
      </div>
      <button className="toast-close" onClick={handleRemove} aria-label="Close toast">
        <FiX />
      </button>
      {duration && (
        <div 
          className="toast-progress" 
          style={{ animationDuration: `${duration}ms` }}
        />
      )}
    </div>
  );
};

export const ToastContainer = () => {
  const { toasts } = useToast();

  if (toasts.length === 0) return null;

  return (
    <div className="toast-container" aria-live="polite">
      {toasts.map((toast) => (
        <ToastItem key={toast.id} {...toast} />
      ))}
    </div>
  );
};
