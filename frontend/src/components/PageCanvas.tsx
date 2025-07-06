import React from 'react';
import { Page, Component } from '../types';
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
        return 'bg-gradient-to-br from-blue-50 to-indigo-100';
      case 'minimal':
        return 'bg-white text-gray-900 font-serif';
      default:
        return 'bg-white text-gray-900';
    }
  };

  return (
    <div className="flex-1 overflow-auto bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Preview Header */}
        <div className="bg-white rounded-t-lg shadow-sm border-b p-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-gray-900">
                Vista Previa: {page.title}
              </h2>
              <p className="text-sm text-gray-600">
                Tema: {page.config.theme} • {components.length} componentes
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-500">
                {page.is_published ? '🟢 Publicado' : '🟡 Borrador'}
              </span>
            </div>
          </div>
        </div>

        {/* Canvas */}
        <div className={`${getThemeStyles(page.config.theme)} min-h-96 shadow-lg rounded-b-lg`}>
          {components.length === 0 ? (
            <div className="flex items-center justify-center py-24">
              <div className="text-center">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v14a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v14a4 4 0 004 4h4a4 4 0 001-4V5zM7 5h10" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">
                  Página vacía
                </h3>
                <p className="mt-1 text-sm text-gray-500">
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
                        theme={page.config.theme}
                      />
                    ))}
                </div>
              </SortableContext>
            </DndContext>
          )}
        </div>

        {/* Canvas Footer */}
        <div className="bg-white rounded-b-lg shadow-sm border-t p-4 mt-0">
          <div className="flex items-center justify-center space-x-4 text-sm text-gray-500">
            <span>Haz clic en un componente para editarlo</span>
            <span>•</span>
            <span>Arrastra para reordenar</span>
            <span>•</span>
            <span>URL: {page.slug}.localhost</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PageCanvas;