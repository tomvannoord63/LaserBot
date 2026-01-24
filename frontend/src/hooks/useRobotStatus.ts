import { useCallback, useEffect, useState } from 'react';
import { robotApi } from '../services/robotApi';
import { RobotStatus } from '../types/robot';

export const useRobotStatus = () => {
  const [status, setStatus] = useState<RobotStatus>({
    connected: false,
    running: false,
    laserOn: true, // Default to on
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = useCallback(async () => {
    try {
      const backendStatus = await robotApi.getRobotStatus();

      // Map backend response to frontend expected structure
      const robotStatus: RobotStatus = {
        connected: backendStatus.connected,
        running: backendStatus.status === 'running',
        laserOn: backendStatus.laser_on,
      };

      setStatus(robotStatus);
      setError(null);
    } catch (err) {
      setError('Failed to fetch robot status');
      console.error('Status fetch error:', err);
    }
  }, []);

  const connect = async () => {
    setLoading(true);
    try {
      await robotApi.connectRobot();
      await fetchStatus();
      setError(null);
    } catch (err) {
      setError('Failed to connect to robot');
    } finally {
      setLoading(false);
    }
  };

  const disconnect = async () => {
    setLoading(true);
    try {
      await robotApi.disconnectRobot();
      await fetchStatus();
      setError(null);
    } catch (err) {
      setError('Failed to disconnect from robot');
    } finally {
      setLoading(false);
    }
  };

  const start = async (randomOrder: boolean = true, minDelay: number = 3.0, maxDelay: number = 5.0) => {
    setLoading(true);
    try {
      await robotApi.startRobot(randomOrder, minDelay, maxDelay);
      await fetchStatus();
      setError(null);
    } catch (err) {
      setError('Failed to start robot');
    } finally {
      setLoading(false);
    }
  };

  const stop = async () => {
    setLoading(true);
    try {
      await robotApi.stopRobot();
      await fetchStatus();
      setError(null);
    } catch (err) {
      setError('Failed to stop robot');
    } finally {
      setLoading(false);
    }
  };

  const toggleLaser = async () => {
    setLoading(true);
    try {
      await robotApi.toggleLaser(!status.laserOn);
      await fetchStatus();
      setError(null);
    } catch (err) {
      setError('Failed to toggle laser');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 2000); // Poll every 2 seconds
    return () => clearInterval(interval);
  }, [fetchStatus]);

  return {
    status,
    loading,
    error,
    connect,
    disconnect,
    start,
    stop,
    toggleLaser,
    refresh: fetchStatus,
  };
};