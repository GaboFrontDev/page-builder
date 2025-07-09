import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Page, Component } from '../types';
import { pagesApi, componentsApi, deploymentApi, handleApiError } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { useNotification } from '../contexts/NotificationContext';
import { componentTypes, getDefaultContent, getDefaultStyles } from '@shared/utils/componentDefaults';
import ComponentSidebar from './ComponentSidebar';
import SharedComponentPreview from './SharedComponentPreview';
import ModernComponentEditor from './ModernComponentEditor';
import PageSettings from './PageSettings';
import { DndContext, DragEndEvent, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';

const ModernPageBuilder: React.FC = () => {
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

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

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
      const newPage = await pagesApi.createPage({
        title: 'Nueva Página',
        slug: `pagina-${Date.now()}`,
        subdomain: user?.username || 'usuario',
        description: 'Descripción de la nueva página',
        config: { theme: 'default' }
      });
      
      setPage(newPage);
      setComponents([]);
      navigate(`/builder/${newPage.id}`, { replace: true });
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      showNotification('error', errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const addComponent = async (type: string) => {
    if (!page) return;

    try {
      setSaving(true);
      const defaultContent = getDefaultContent(type as any);
      const defaultStyles = getDefaultStyles(type as any);
      
      const newComponent = await componentsApi.createComponent(page.id, {
        type: type as any,
        content: defaultContent,
        styles: defaultStyles,
        position: components.length,
        is_visible: true
      });

      setComponents([...components, newComponent]);
      showNotification('success', 'Componente agregado');
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      showNotification('error', errorMessage);
    } finally {
      setSaving(false);
    }
  };

  const updateComponent = async (id: number, updates: Partial<Component>) => {
    try {
      const updatedComponent = await componentsApi.updateComponent(id, updates);
      setComponents(components.map(c => c.id === id ? updatedComponent : c));
      
      // Update selected component if it's the one being edited
      if (selectedComponent?.id === id) {
        setSelectedComponent(updatedComponent);
      }
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      showNotification('error', errorMessage);
    }
  };

  const deleteComponent = async (id: number) => {
    try {
      await componentsApi.deleteComponent(id);
      setComponents(components.filter(c => c.id !== id));
      setSelectedComponent(null);
      showNotification('success', 'Componente eliminado');
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      showNotification('error', errorMessage);
    }
  };

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;
    
    if (!over || active.id === over.id) return;

    const activeIndex = components.findIndex(c => c.id === active.id);
    const overIndex = components.findIndex(c => c.id === over.id);

    if (activeIndex === -1 || overIndex === -1) return;

    const newComponents = [...components];
    const [removed] = newComponents.splice(activeIndex, 1);
    newComponents.splice(overIndex, 0, removed);

    // Update positions
    const updatedComponents = newComponents.map((component, index) => ({
      ...component,
      position: index
    }));

    setComponents(updatedComponents);

    try {
      await componentsApi.reorderComponents(
        page!.id,
        updatedComponents.map(c => c.id)
      );
      showNotification('success', 'Componentes reordenados');
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      showNotification('error', errorMessage);
      // Revert on error
      setComponents(components);
    }
  };

  const updatePage = async (updates: Partial<Page>) => {
    if (!page) return;

    try {
      setSaving(true);
      const updatedPage = await pagesApi.updatePage(page.id, updates);
      setPage(updatedPage);
      showNotification('success', 'Página actualizada');
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      showNotification('error', errorMessage);
    } finally {
      setSaving(false);
    }
  };

  const publishPage = async () => {
    if (!page) return;

    try {
      setSaving(true);
      const publishedPage = await pagesApi.publishPage(page.id);
      setPage(publishedPage);
      showNotification('success', 'Página publicada');
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      showNotification('error', errorMessage);
    } finally {
      setSaving(false);
    }
  };

  const deployPage = async () => {
    if (!page) return;

    try {
      setDeploying(true);
      const result = await deploymentApi.deployPage(page.id);
      showNotification('success', `Página desplegada: ${result.url}`);
    } catch (error: any) {
      const errorMessage = handleApiError(error);
      showNotification('error', errorMessage);
    } finally {
      setDeploying(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="loading-spinner w-8 h-8 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Cargando página...</p>
        </div>
      </div>
    );
  }

  if (error || !page) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Error al cargar la página'}</p>
          <button
            onClick={() => navigate('/')}
            className="btn btn-primary"
          >
            Volver al Dashboard
          </button>
        </div>
      </div>
    );
  }

  const currentTheme = page.config?.theme || 'default';

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/')}
              className="text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200"
              title="Volver al Dashboard"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">
              {page.title}
            </h1>
            {saving && (
              <span className="text-sm text-gray-500 dark:text-gray-400">Guardando...</span>
            )}
          </div>
          
          <div className="flex items-center space-x-3">
            <button
              onClick={publishPage}
              disabled={saving}
              className={`btn ${page.is_published ? 'btn-secondary' : 'btn-primary'}`}
            >
              {page.is_published ? 'Publicado' : 'Publicar'}
            </button>
            
            {page.is_published && (
              <button
                onClick={deployPage}
                disabled={deploying}
                className="btn btn-success"
              >
                {deploying ? 'Desplegando...' : 'Desplegar'}
              </button>
            )}
          </div>
        </div>
      </header>

      <div className="flex h-[calc(100vh-80px)]">
        {/* Sidebar */}
        <div className="w-80 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 overflow-y-auto">
          {/* Tabs */}
          <div className="flex border-b border-gray-200 dark:border-gray-700">
            <button
              onClick={() => setActiveTab('components')}
              className={`flex-1 py-3 px-4 text-sm font-medium ${
                activeTab === 'components'
                  ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-blue-900/20'
                  : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
              }`}
            >
              Componentes
            </button>
            <button
              onClick={() => setActiveTab('settings')}
              className={`flex-1 py-3 px-4 text-sm font-medium ${
                activeTab === 'settings'
                  ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-blue-900/20'
                  : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
              }`}
            >
              Configuración
            </button>
          </div>

          {/* Tab Content */}
          <div className="p-4">
            {activeTab === 'components' && (
              <ComponentSidebar
                onAddComponent={(type) => addComponent(type)}
                selectedComponent={selectedComponent}
                onUpdateComponent={updateComponent}
                onDeleteComponent={deleteComponent}
              />
            )}
            {activeTab === 'settings' && (
              <PageSettings
                page={page}
                onUpdatePage={(updatedPage) => updatePage(updatedPage)}
                onSavePage={() => {}}
              />
            )}
          </div>
        </div>

        {/* Main Canvas */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-4xl mx-auto p-6">
            <DndContext
              sensors={sensors}
              onDragEnd={handleDragEnd}
            >
              <SortableContext
                items={components.map(c => c.id)}
                strategy={verticalListSortingStrategy}
              >
                <div className="space-y-4">
                  {components.length === 0 ? (
                    <div className="text-center py-12 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
                      <p className="text-gray-500 dark:text-gray-400 mb-4">
                        No hay componentes en esta página
                      </p>
                      <p className="text-sm text-gray-400 dark:text-gray-500">
                        Agrega componentes desde el panel lateral
                      </p>
                    </div>
                  ) : (
                    components.map((component) => (
                      <SharedComponentPreview
                        key={component.id}
                        component={component}
                        isSelected={selectedComponent?.id === component.id}
                        onSelect={() => setSelectedComponent(component)}
                        theme={currentTheme}
                      />
                    ))
                  )}
                </div>
              </SortableContext>
            </DndContext>
          </div>
        </div>
      </div>

      {/* Component Editor Modal */}
      {selectedComponent && (
        <ModernComponentEditor
          component={selectedComponent}
          onUpdateComponent={updateComponent}
          onDeleteComponent={deleteComponent}
          onClose={() => setSelectedComponent(null)}
          theme={currentTheme}
        />
      )}
    </div>
  );
};

export default ModernPageBuilder;