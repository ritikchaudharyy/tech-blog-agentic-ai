import { Component } from 'react';

class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error) {
    console.error('UI Crash:', error);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center">
          <p className="text-sm text-muted">
            Something went wrong. Please refresh.
          </p>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
