import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Page, Component, ComponentType } from '../types';
import { pagesApi, componentsApi, deploymentApi, handleApiError } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { useNotification } from '../contexts/NotificationContext';
import ComponentSidebar from './ComponentSidebar';
import PageCanvas from './PageCanvas';
import ComponentEditor from './ComponentEditor';
import PageSettings from './PageSettings';

const PageBuilder: React.FC = () => {
  const { pageId } = useParams<{ pageId: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const { showNotification } = useNotification();
  
  const [page, setPage] = useState<Page | null>(null);
  const [components, setComponents] = useState<Component[]>([]);
  const [selectedComponent, setSelectedComponent] = useState<Component | null>(null);
  const [activeTab, setActiveTab] = useState<'components' | 'settings'>('components');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [saving, setSaving] = useState(false);
  const [deploying, setDeploying] = useState(false);

  useEffect(() => {
    if (pageId) {
      loadPage();
    } else {
      createNewPage();
    }
  }, [pageId]);

  const loadPage = async () => {
    try {
      const pageData = await pagesApi.getPage(parseInt(pageId!));
      setPage(pageData);
      
      const componentsData = await componentsApi.getComponents(pageData.id);
      setComponents(componentsData.sort((a, b) => a.position - b.position));
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      showNotification('error', errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const createNewPage = async () => {
    try {
      const timestamp = Date.now();
      const newPage = await pagesApi.createPage({
        title: 'Nueva Página',
        slug: 'root', // Usar 'root' para páginas root
        subdomain: `sitio-${timestamp}`,
        description: 'Descripción de la página',
        config: { theme: 'default' },
        is_published: false
      });
      setPage(newPage);
      navigate(`/builder/${newPage.id}`, { replace: true });
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      showNotification('error', errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleSavePage = async () => {
    if (!page) return;
    
    setSaving(true);
    try {
      const updatedPage = await pagesApi.updatePage(page.id, page);
      setPage(updatedPage);
      showNotification('success', 'Página guardada exitosamente');
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      showNotification('error', errorMessage);
    } finally {
      setSaving(false);
    }
  };

  const handlePublishPage = async () => {
    if (!page) return;
    
    try {
      const publishedPage = await pagesApi.publishPage(page.id);
      setPage(publishedPage);
      showNotification('success', 'Página publicada exitosamente');
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      showNotification('error', errorMessage);
    }
  };

  const handleDeployPage = async () => {
    if (!page) return;
    
    setDeploying(true);
    try {
      const deploymentResult = await deploymentApi.deployPage(page.id);
      showNotification('success', `Página desplegada en: ${deploymentResult.url}`);
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      showNotification('error', errorMessage);
    } finally {
      setDeploying(false);
    }
  };

  const handleAddComponent = async (componentType: ComponentType) => {
    if (!page) return;

    try {
      const newComponent = await componentsApi.createComponent(page.id, {
        type: componentType,
        content: getDefaultComponentContent(componentType),
        styles: {},
        position: components.length + 1,
        is_visible: true
      });
      
      setComponents([...components, newComponent]);
      setSelectedComponent(newComponent);
      showNotification('success', 'Componente agregado exitosamente');
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      showNotification('error', errorMessage);
    }
  };

  const handleUpdateComponent = async (componentId: number, updates: Partial<Component>) => {
    try {
      const updatedComponent = await componentsApi.updateComponent(componentId, updates);
      setComponents(components.map(comp => 
        comp.id === componentId ? updatedComponent : comp
      ));
      setSelectedComponent(updatedComponent);
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      showNotification('error', errorMessage);
    }
  };

  const handleDeleteComponent = async (componentId: number) => {
    try {
      await componentsApi.deleteComponent(componentId);
      setComponents(components.filter(comp => comp.id !== componentId));
      setSelectedComponent(null);
      showNotification('success', 'Componente eliminado exitosamente');
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      showNotification('error', errorMessage);
    }
  };

  const handleReorderComponents = async (newOrder: Component[]) => {
    try {
      const componentIds = newOrder.map(comp => comp.id);
      await componentsApi.reorderComponents(page!.id, componentIds);
      setComponents(newOrder);
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      showNotification('error', errorMessage);
    }
  };

  const getDefaultComponentContent = (type: ComponentType) => {
    switch (type) {
      case 'header':
        return {
          title: 'Mi Sitio Web',
          logo: '',
          menu_items: [
            { text: 'Inicio', link: '/' },
            { text: 'Acerca', link: '/acerca' },
            { text: 'Contacto', link: '/contacto' }
          ]
        };
      case 'hero':
        return {
          title: 'Título Principal',
          subtitle: 'Descripción atractiva de tu producto o servicio',
          cta_text: 'Comenzar',
          cta_link: '#',
          image: ''
        };
      case 'text':
        return {
          text: '<h2>Sección de Contenido</h2><p>Aquí puedes agregar el contenido principal de tu página.</p>',
          alignment: 'left' as 'left'
        };
      case 'image':
        return {
          src: 'https://via.placeholder.com/600x400',
          alt: 'Imagen de ejemplo',
          caption: 'Descripción de la imagen'
        };
      case 'button':
        return {
          text: 'Botón de Acción',
          link: '#',
          variant: 'primary' as 'primary'
        };
      case 'footer':
        return {
          text: '© 2024 Mi Sitio Web. Todos los derechos reservados.',
          links: [
            { text: 'Privacidad', url: '/privacidad' },
            { text: 'Términos', url: '/terminos' }
          ]
        };
      default:
        return {};
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-300 font-medium">Cargando el editor...</p>
        </div>
      </div>
    );
  }

  if (!page) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
        <div className="text-center">
          <div className="mx-auto h-24 w-24 bg-gradient-to-br from-red-200 to-red-300 dark:from-red-600 dark:to-red-700 rounded-full flex items-center justify-center mb-6">
            <svg className="h-12 w-12 text-red-400 dark:text-red-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Página no encontrada</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-6">La página que buscas no existe o no tienes permisos para acceder a ella.</p>
          <button
            onClick={() => navigate('/')}
            className="btn btn-primary"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Volver al Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      {/* Header moderno */}
      <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-b border-gray-200/50 dark:border-slate-700/50 shadow-sm">
        <div className="flex items-center justify-between px-6 py-4">
          <div className="flex items-center space-x-4">
            <button
              title="Volver al Dashboard"
              onClick={() => navigate('/')}
              type="button"
              className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg transition-colors duration-200"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
            </button>
            <div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">{page.title}</h1>
              <p className="text-sm text-gray-600 dark:text-gray-400 font-mono">{page.slug}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <button
              title="Guardar"
              onClick={handleSavePage}
              disabled={saving}
              type="button"
              className="btn btn-secondary"
            >
              {saving ? (
                <>
                  <div className="loading-spinner-small mr-2"></div>
                  Guardando...
                </>
              ) : (
                <>
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
                  </svg>
                  Guardar
                </>
              )}
            </button>
            
            <button
              onClick={handlePublishPage}
              className={`btn ${page.is_published ? 'btn-success' : 'btn-outline'}`}
              type="button"
            >
              {page.is_published ? (
                <>
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Publicado
                </>
              ) : (
                <>
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                  Publicar
                </>
              )}
            </button>
            
            {page.is_published && (
              <button
                onClick={handleDeployPage}
                disabled={deploying}
                className="btn btn-primary"
                type="button"
              >
                {deploying ? (
                  <>
                    <div className="loading-spinner-small mr-2"></div>
                    Desplegando...
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                    </svg>
                    Desplegar
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border-b border-red-200 dark:border-red-800 px-6 py-4">
          <div className="flex items-center">
            <svg className="w-5 h-5 text-red-400 mr-3" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <span className="text-red-800 dark:text-red-200 text-sm font-medium">{error}</span>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex h-[calc(100vh-120px)]">
        {/* Sidebar */}
        <div className="w-80 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-r border-gray-200/50 dark:border-slate-700/50 flex flex-col">
          <div className="p-4 border-b border-gray-200/50 dark:border-slate-700/50">
            <div className="flex space-x-1 bg-gray-100 dark:bg-slate-700 rounded-lg p-1">
              <button
                onClick={() => setActiveTab('components')}
                className={`flex-1 px-3 py-2 text-sm font-medium rounded-md transition-all duration-200 ${
                  activeTab === 'components'
                    ? 'bg-white dark:bg-slate-600 text-gray-900 dark:text-white shadow-sm'
                    : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
                }`}
              >
                <svg className="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Componentes
              </button>
              <button
                onClick={() => setActiveTab('settings')}
                className={`flex-1 px-3 py-2 text-sm font-medium rounded-md transition-all duration-200 ${
                  activeTab === 'settings'
                    ? 'bg-white dark:bg-slate-600 text-gray-900 dark:text-white shadow-sm'
                    : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
                }`}
              >
                <svg className="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Configuración
              </button>
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto">
            {activeTab === 'components' ? (
              <ComponentSidebar
                onAddComponent={handleAddComponent}
                selectedComponent={selectedComponent}
                onUpdateComponent={handleUpdateComponent}
                onDeleteComponent={handleDeleteComponent}
              />
            ) : (
              <PageSettings
                page={page}
                onUpdatePage={setPage}
                onSavePage={handleSavePage}
              />
            )}
          </div>
        </div>

        {/* Main Canvas */}
        <div className="flex-1 flex flex-col bg-gray-50 dark:bg-slate-900">
          <PageCanvas
            page={page}
            components={components}
            selectedComponent={selectedComponent}
            onSelectComponent={setSelectedComponent}
            onReorderComponents={handleReorderComponents}
          />
        </div>

        {/* Component Editor */}
        {selectedComponent && (
          <div className="w-80 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-l border-gray-200/50 dark:border-slate-700/50">
            <ComponentEditor
              component={selectedComponent}
              onUpdateComponent={handleUpdateComponent}
              onDeleteComponent={handleDeleteComponent}
              onClose={() => setSelectedComponent(null)}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default PageBuilder;