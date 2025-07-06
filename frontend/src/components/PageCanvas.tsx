import React from 'react';
import { Page, Component } from '../types';
import { useAuth } from '../contexts/AuthContext';
import { 
  DndContext, 
  closestCenter, 
  KeyboardSensor, 
  PointerSensor, 
  useSensor, 
  useSensors,
  DragEndEvent
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import {
  restrictToVerticalAxis,
  restrictToParentElement,
} from '@dnd-kit/modifiers';
import ComponentPreview from './ComponentPreview';

interface PageCanvasProps {
  page: Page;
  components: Component[];
  selectedComponent: Component | null;
  onSelectComponent: (component: Component | null) => void;
  onReorderComponents: (components: Component[]) => void;
}

const PageCanvas: React.FC<PageCanvasProps> = ({
  page,
  components,
  selectedComponent,
  onSelectComponent,
  onReorderComponents
}) => {
  const { user } = useAuth();
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (active.id !== over?.id) {
      const oldIndex = components.findIndex((component) => component.id === active.id);
      const newIndex = components.findIndex((component) => component.id === over?.id);

      const newComponents = arrayMove(components, oldIndex, newIndex);
      // Update positions
      const updatedComponents = newComponents.map((comp, index) => ({
        ...comp,
        position: index + 1
      }));
      
      onReorderComponents(updatedComponents);
    }
  };

  const getThemeStyles = (theme: string) => {
    switch (theme) {
      case 'dark':
        return 'bg-gray-900 text-white';
      case 'modern':
        return 'bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-slate-800 dark:to-slate-900';
      case 'minimal':
        return 'bg-white text-gray-900 font-serif dark:bg-slate-800 dark:text-white';
      default:
        return 'bg-white text-gray-900 dark:bg-white dark:text-gray-900';
    }
  };

  const getThemeFromPage = (page: Page): string => {
    return page.config?.theme || 'default';
  };

  return (
    <div className="flex-1 overflow-auto bg-gray-50 dark:bg-slate-900 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Preview Header */}
        <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-t-xl shadow-sm border border-gray-200/50 dark:border-slate-700/50 p-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                Vista Previa: {page.title}
              </h2>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Tema: {getThemeFromPage(page)} • {components.length} componentes
              </p>
            </div>
            <div className="flex items-center space-x-3">
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
                page.is_published 
                  ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300'
                  : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300'
              }`}>
                <span className={`w-2 h-2 rounded-full mr-2 ${
                  page.is_published 
                    ? 'bg-green-500 dark:bg-green-400'
                    : 'bg-yellow-500 dark:bg-yellow-400'
                }`}></span>
                {page.is_published ? 'Publicado' : 'Borrador'}
              </span>
            </div>
          </div>
        </div>

        {/* Canvas */}
        <div className={`${getThemeStyles(getThemeFromPage(page))} min-h-96 shadow-xl rounded-b-xl border border-gray-200/50 dark:border-slate-700/50`}>
          {components.length === 0 ? (
            <div className="flex items-center justify-center py-24">
              <div className="text-center">
                <div className="mx-auto h-16 w-16 bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-600 dark:to-gray-700 rounded-full flex items-center justify-center mb-4">
                  <svg className="h-8 w-8 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v14a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v14a4 4 0 004 4h4a4 4 0 001-4V5zM7 5h10" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Página vacía
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Agrega componentes desde el panel izquierdo para comenzar.
                </p>
              </div>
            </div>
          ) : (
            <DndContext 
              sensors={sensors}
              collisionDetection={closestCenter}
              onDragEnd={handleDragEnd}
              modifiers={[restrictToVerticalAxis, restrictToParentElement]}
            >
              <SortableContext 
                items={components.map(c => c.id)} 
                strategy={verticalListSortingStrategy}
              >
                <div className="space-y-0">
                  {components
                    .filter(component => component.is_visible)
                    .sort((a, b) => a.position - b.position)
                    .map((component) => (
                      <ComponentPreview
                        key={component.id}
                        component={component}
                        isSelected={selectedComponent?.id === component.id}
                        onSelect={() => onSelectComponent(component)}
                        theme={getThemeFromPage(page)}
                      />
                    ))}
                </div>
              </SortableContext>
            </DndContext>
          )}
        </div>

        {/* Canvas Footer */}
        <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-b-xl shadow-sm border border-gray-200/50 dark:border-slate-700/50 p-6 mt-0">
          <div className="flex items-center justify-center space-x-6 text-sm text-gray-500 dark:text-gray-400">
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.122 2.122" />
              </svg>
              Haz clic en un componente para editarlo
            </span>
            <span className="text-gray-300 dark:text-gray-600">•</span>
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
              </svg>
              Arrastra para reordenar
            </span>
            <span className="text-gray-300 dark:text-gray-600">•</span>
            <span className="flex items-center font-mono">
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
              </svg>
              {page.subdomain}.localhost/{page.slug}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PageCanvas;