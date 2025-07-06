import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Page } from '../types';
import { pagesApi, deploymentApi, handleApiError } from '../services/api';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [pages, setPages] = useState<Page[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [deployedSites, setDeployedSites] = useState<any[]>([]);

  useEffect(() => {
    loadPages();
    loadDeployedSites();
  }, []);

  const loadPages = async () => {
    try {
      const pagesData = await pagesApi.getPages();
      setPages(pagesData);
    } catch (error: any) {
      setError(handleApiError(error));
    } finally {
      setLoading(false);
    }
  };

  const loadDeployedSites = async () => {
    try {
      const sitesData = await deploymentApi.listDeployedSites();
      setDeployedSites(sitesData.deployed_sites);
    } catch (error: any) {
      console.error('Error loading deployed sites:', error);
    }
  };

  const handleDeletePage = async (pageId: number) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta página?')) {
      try {
        await pagesApi.deletePage(pageId);
        setPages(pages.filter(page => page.id !== pageId));
      } catch (error: any) {
        setError(handleApiError(error));
      }
    }
  };

  const handleDeployPage = async (pageId: number) => {
    try {
      await deploymentApi.deployPage(pageId);
      await loadDeployedSites();
      // Mostrar notificación de éxito
      alert('Página desplegada exitosamente');
    } catch (error: any) {
      setError(handleApiError(error));
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">Landing Builder</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">Hola, {user?.username}</span>
              <button
                onClick={logout}
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                Cerrar sesión
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Header del Dashboard */}
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Mis Páginas</h1>
              <p className="mt-1 text-sm text-gray-600">
                Crea y gestiona tus landing pages
              </p>
            </div>
            <Link
              to="/builder"
              className="btn btn-primary"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Nueva Página
            </Link>
          </div>
        </div>

        {error && (
          <div className="mx-4 mb-4 rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">{error}</h3>
              </div>
            </div>
          </div>
        )}

        {/* Lista de Páginas */}
        <div className="px-4 sm:px-0">
          {pages.length === 0 ? (
            <div className="text-center py-12">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">No hay páginas</h3>
              <p className="mt-1 text-sm text-gray-500">
                Empieza creando tu primera landing page.
              </p>
              <div className="mt-6">
                <Link
                  to="/builder"
                  className="btn btn-primary"
                >
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Nueva Página
                </Link>
              </div>
            </div>
          ) : (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {pages.map((page) => (
                <div key={page.id} className="card">
                  <div className="card-body">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-medium text-gray-900 truncate">
                        {page.title}
                      </h3>
                      <div className="flex items-center space-x-2">
                        {page.is_published ? (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Publicado
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            Borrador
                          </span>
                        )}
                      </div>
                    </div>
                    
                    <p className="mt-2 text-sm text-gray-600">
                      {page.description}
                    </p>
                    
                    <div className="mt-4 flex items-center justify-between text-sm text-gray-500">
                      <span>Tema: {page.config.theme}</span>
                      <span>{formatDate(page.updated_at)}</span>
                    </div>
                    
                    <div className="mt-4 flex space-x-2">
                      <Link
                        to={`/builder/${page.id}`}
                        className="flex-1 btn btn-primary text-sm"
                      >
                        <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                        Editar
                      </Link>
                      
                      {page.is_published && (
                        <button
                          onClick={() => handleDeployPage(page.id)}
                          className="btn btn-success text-sm"
                        >
                          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                          </svg>
                          Deploy
                        </button>
                      )}
                      
                      <button
                        onClick={() => handleDeletePage(page.id)}
                        className="btn btn-danger text-sm"
                      >
                        <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        Eliminar
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Sitios Desplegados */}
        {deployedSites.length > 0 && (
          <div className="px-4 sm:px-0 mt-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Sitios Desplegados</h2>
            <div className="card">
              <div className="card-body">
                <div className="space-y-4">
                  {deployedSites.map((site) => (
                    <div key={site.slug} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <h3 className="font-medium text-gray-900">{site.slug}</h3>
                        <p className="text-sm text-gray-600">{site.path}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <a
                          href={site.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="btn btn-outline text-sm"
                        >
                          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                          </svg>
                          Ver sitio
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;