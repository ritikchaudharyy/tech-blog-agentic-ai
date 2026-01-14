import { useEffect, useState } from 'react';

const EXIT_DURATION = 220; // ms (must match CSS)

const RouteTransition = ({ children }) => {
  const [stage, setStage] = useState('enter');

  useEffect(() => {
    setStage('enter');

    return () => {
      setStage('exit');
    };
  }, []);

  return (
    <div
      className={
        stage === 'enter'
          ? 'route-enter'
          : 'route-exit'
      }
    >
      {children}
    </div>
  );
};

export default RouteTransition;
