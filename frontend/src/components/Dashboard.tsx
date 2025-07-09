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
    
    if (sessionId && success === 'true') {
      try {
        const response = await fetch(`/api/subscription/verify-payment/${sessionId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
          }
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.success) {
            showNotification('success', '¡Suscripción activada exitosamente!');
            // Limpiar URL
            window.history.replaceState({}, document.title, '/');
          }
        }
      } catch (error) {
        console.error('Error verificando pago:', error);
      }
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