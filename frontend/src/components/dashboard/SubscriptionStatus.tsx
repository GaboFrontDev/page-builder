import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNotification } from '../../contexts/NotificationContext';

interface SubscriptionInfo {
  subscription_active: boolean;
  stripe_customer_id: string | null;
  plan_type?: string;
  current_period_end?: string;
}

const SubscriptionStatus: React.FC = () => {
  const { user } = useAuth();
  const { showNotification } = useNotification();
  const [subscriptionInfo, setSubscriptionInfo] = useState<SubscriptionInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      loadSubscriptionStatus();
    }
  }, [user]);

  // Función para recargar el estado de suscripción
  const refreshSubscriptionStatus = () => {
    if (user) {
      loadSubscriptionStatus();
    }
  };

  // Exponer la función para que otros componentes puedan usarla
  useEffect(() => {
    (window as any).refreshSubscriptionStatus = refreshSubscriptionStatus;
    return () => {
      delete (window as any).refreshSubscriptionStatus;
    };
  }, [user]);

  const loadSubscriptionStatus = async () => {
    try {
      const response = await fetch(`/api/subscription/user-status/${user?.id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setSubscriptionInfo(data);
      }
    } catch (error) {
      console.error('Error cargando estado de suscripción:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-card">
        <div className="flex items-center justify-center p-4">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  if (!subscriptionInfo) {
    return null;
  }

  return (
    <div className="dashboard-card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          Estado de Suscripción
        </h3>
        <div className="flex items-center space-x-2">
          {subscriptionInfo.subscription_active ? (
            <span className="badge badge-success">
              <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Activa
            </span>
          ) : (
            <span className="badge badge-warning">
              <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Inactiva
            </span>
          )}
        </div>
      </div>

      <div className="space-y-3">
        {subscriptionInfo.subscription_active ? (
          <>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-300">Plan:</span>
              <span className="text-sm font-medium text-gray-900 dark:text-white">
                {subscriptionInfo.plan_type || 'Premium'}
              </span>
            </div>
            {subscriptionInfo.current_period_end && (
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-300">Renovación:</span>
                <span className="text-sm font-medium text-gray-900 dark:text-white">
                  {new Date(subscriptionInfo.current_period_end).toLocaleDateString('es-ES')}
                </span>
              </div>
            )}
            <div className="pt-3 border-t border-gray-200 dark:border-gray-700">
              <a
                href="/subscription"
                className="btn btn-outline btn-sm w-full"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Gestionar Suscripción
              </a>
            </div>
          </>
        ) : (
          <>
            <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
              No tienes una suscripción activa. Suscríbete para acceder a todas las funcionalidades.
            </p>
            <a
              href="/subscription"
              className="btn btn-primary btn-sm w-full"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
              </svg>
              Ver Planes
            </a>
          </>
        )}
      </div>
    </div>
  );
};

export default SubscriptionStatus; 