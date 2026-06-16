import React from 'react';
import { FiAlertTriangle } from 'react-icons/fi';
import { Button } from './Button';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '60vh',
          padding: 'var(--space-8)',
          textAlign: 'center'
        }}>
          <FiAlertTriangle style={{ fontSize: '48px', color: 'var(--color-error-500)', marginBottom: 'var(--space-4)' }} />
          <h2 className="heading-2" style={{ marginBottom: 'var(--space-2)' }}>Something went wrong</h2>
          <p className="text-muted" style={{ marginBottom: 'var(--space-6)', maxWidth: '400px' }}>
            We encountered an unexpected error while loading this component. Please try again.
          </p>
          <Button variant="primary" onClick={this.handleRetry}>
            Retry Reloading
          </Button>
        </div>
      );
    }

    return this.props.children;
  }
}
