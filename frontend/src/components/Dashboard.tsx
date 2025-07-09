import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNotification } from '../contexts/NotificationContext';
import { Page } from '../types';
import { pagesApi, deploymentApi, handleApiError } from '../services/api';
import {
  DashboardHeader,
  DashboardTitle,
  StatsCards,
  ErrorAlert,
  EmptyState,
  SubdomainSection,
  LoadingSpinner
} from './dashboard/index';
import SubscriptionStatus from './dashboard/SubscriptionStatus';

const Dashboard: React.FC = () => {
  const { logout } = useAuth();
  const { showNotification } = useNotification();
  const [pages, setPages] = useState<Page[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    loadPages();
    checkPaymentSuccess();
  }, []);

  const checkPaymentSuccess = async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session_id');
    const success = urlParams.get('success');
    
    console.log('Checking payment success:', { sessionId, success });
    
    if (sessionId && success === 'true') {
      try {
        console.log('Verifying payment for session:', sessionId);
        
        const response = await fetch(`/api/subscription/verify-payment/${sessionId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
            'Content-Type': 'application/json'
          }
        });
        
        console.log('Payment verification response status:', response.status);
        
        if (response.ok) {
          const result = await response.json();
          console.log('Payment verification result:', result);
          
          if (result.success) {
            showNotification('success', '¡Suscripción activada exitosamente! 🎉');
            // Limpiar URL
            window.history.replaceState({}, document.title, '/dashboard');
          } else {
            showNotification('warning', result.message || 'El pago no se completó correctamente');
          }
        } else {
          const errorData = await response.json().catch(() => ({}));
          console.error('Payment verification failed:', errorData);
          showNotification('error', 'Error verificando el pago. Por favor, contacta soporte.');
        }
      } catch (error) {
        console.error('Error verificando pago:', error);
        showNotification('error', 'Error de conexión al verificar el pago');
      }
    } else if (success === 'true' && !sessionId) {
      // Caso donde success=true pero no hay session_id
      showNotification('warning', 'Pago completado, pero no se pudo verificar el estado');
    }
  };

  const loadPages = async () => {
    try {
      const pagesData = await pagesApi.getPages();
      setPages(pagesData);
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      showNotification('error', errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleDeletePage = async (pageId: number) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta página?')) {
      try {
        await pagesApi.deletePage(pageId);
        setPages(pages.filter(page => page.id !== pageId));
        showNotification('success', 'Página eliminada exitosamente');
      } catch (error: any) {
        const errorMessage = handleApiError(error);
        setError(errorMessage);
        showNotification('error', errorMessage);
      }
    }
  };

  const handleDeployPage = async (pageId: number) => {
    try {
      await deploymentApi.deployPage(pageId);
      showNotification('success', 'Página desplegada exitosamente');
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      showNotification('error', errorMessage);
    }
  };

  // Agrupar páginas por subdominio
  const pagesBySubdomain: { [subdomain: string]: Page[] } = {};
  pages.forEach((page) => {
    if (!pagesBySubdomain[page.subdomain]) {
      pagesBySubdomain[page.subdomain] = [];
    }
    pagesBySubdomain[page.subdomain].push(page);
  });

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      <DashboardHeader onLogout={logout} />

      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <DashboardTitle />
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2">
            <StatsCards pages={pages} pagesBySubdomain={pagesBySubdomain} />
          </div>
          <div>
            <SubscriptionStatus />
          </div>
        </div>
        
        <ErrorAlert error={error} />

        {/* Lista de Páginas agrupadas por subdominio */}
        <div className="space-y-8">
          {Object.keys(pagesBySubdomain).length === 0 ? (
            <EmptyState />
          ) : (
            Object.entries(pagesBySubdomain).map(([subdomain, subPages]) => (
              <SubdomainSection
                key={subdomain}
                subdomain={subdomain}
                pages={subPages}
                onDelete={handleDeletePage}
                onDeploy={handleDeployPage}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;