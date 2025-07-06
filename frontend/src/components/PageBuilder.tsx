import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Page, Component, ComponentType } from '../types';
import { pagesApi, componentsApi, deploymentApi, handleApiError } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import ComponentSidebar from './ComponentSidebar';
import PageCanvas from './PageCanvas';
import ComponentEditor from './ComponentEditor';
import PageSettings from './PageSettings';

const PageBuilder: React.FC = () => {
  const { pageId } = useParams<{ pageId: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  
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
      setError(handleApiError(error));
    } finally {
      setLoading(false);
    }
  };

  const createNewPage = async () => {
    try {
      const newPage = await pagesApi.createPage({
        title: 'Nueva Página',
        slug: `pagina-${Date.now()}`,
        description: 'Descripción de la página',
        config: { theme: 'default' },
        is_published: false
      });
      setPage(newPage);
      navigate(`/builder/${newPage.id}`, { replace: true });
    } catch (error: any) {
      setError(handleApiError(error));
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
    } catch (error: any) {
      setError(handleApiError(error));
    } finally {
      setSaving(false);
    }
  };

  const handlePublishPage = async () => {
    if (!page) return;
    
    try {
      const publishedPage = await pagesApi.publishPage(page.id);
      setPage(publishedPage);
    } catch (error: any) {
      setError(handleApiError(error));
    }
  };

  const handleDeployPage = async () => {
    if (!page) return;
    
    setDeploying(true);
    try {
      const deploymentResult = await deploymentApi.deployPage(page.id);
      alert(`Página desplegada en: ${deploymentResult.url}`);
    } catch (error: any) {
      setError(handleApiError(error));
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
    } catch (error: any) {
      setError(handleApiError(error));
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
      setError(handleApiError(error));
    }
  };

  const handleDeleteComponent = async (componentId: number) => {
    try {
      await componentsApi.deleteComponent(componentId);
      setComponents(components.filter(comp => comp.id !== componentId));
      setSelectedComponent(null);
    } catch (error: any) {
      setError(handleApiError(error));
    }
  };

  const handleReorderComponents = async (newOrder: Component[]) => {
    try {
      const componentIds = newOrder.map(comp => comp.id);
      await componentsApi.reorderComponents(page!.id, componentIds);
      setComponents(newOrder);
    } catch (error: any) {
      setError(handleApiError(error));
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
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!page) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Página no encontrada</h2>
          <button
            onClick={() => navigate('/')}
            className="mt-4 btn btn-primary"
          >
            Volver al Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="flex items-center justify-between px-4 py-3">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/')}
              className="text-gray-500 hover:text-gray-700"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
            </button>
            <div>
              <h1 className="text-lg font-semibold text-gray-900">{page.title}</h1>
              <p className="text-sm text-gray-600">{page.slug}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={handleSavePage}
              disabled={saving}
              className="btn btn-secondary text-sm"
            >
              {saving ? 'Guardando...' : 'Guardar'}
            </button>
            
            <button
              onClick={handlePublishPage}
              className="btn btn-success text-sm"
            >
              {page.is_published ? 'Publicado' : 'Publicar'}
            </button>
            
            {page.is_published && (
              <button
                onClick={handleDeployPage}
                disabled={deploying}
                className="btn btn-primary text-sm"
              >
                {deploying ? 'Desplegando...' : 'Desplegar'}
              </button>
            )}
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border-b border-red-200 px-4 py-3">
          <div className="flex items-center">
            <svg className="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <span className="text-red-800 text-sm">{error}</span>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex h-screen">
        {/* Sidebar */}
        <div className="sidebar">
          <div className="sidebar-header">
            <div className="flex space-x-1">
              <button
                onClick={() => setActiveTab('components')}
                className={`tab ${activeTab === 'components' ? 'active' : ''}`}
              >
                Componentes
              </button>
              <button
                onClick={() => setActiveTab('settings')}
                className={`tab ${activeTab === 'settings' ? 'active' : ''}`}
              >
                Configuración
              </button>
            </div>
          </div>
          
          <div className="sidebar-content">
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
        <div className="flex-1 flex flex-col">
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
          <div className="w-80 bg-white border-l border-gray-200">
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