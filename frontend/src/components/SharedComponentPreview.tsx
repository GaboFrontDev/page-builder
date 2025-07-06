import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Component } from '../types';
import { ComponentRenderer } from '../shared';

interface SharedComponentPreviewProps {
  component: Component;
  isSelected: boolean;
  onSelect: () => void;
  theme: string;
}

const SharedComponentPreview: React.FC<SharedComponentPreviewProps> = ({
  component,
  isSelected,
  onSelect,
  theme
}) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: component.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  } as React.CSSProperties;

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`
        relative cursor-pointer transition-all duration-200
        ${isSelected ? 'ring-2 ring-blue-500 ring-offset-2' : 'hover:ring-1 hover:ring-gray-300'}
        ${isDragging ? 'opacity-50 z-50' : ''}
      `}
      onClick={onSelect}
      {...attributes}
      {...listeners}
    >
      {/* Selection indicator */}
      {isSelected && (
        <div className="absolute -top-8 left-0 z-10 bg-blue-500 text-white px-2 py-1 text-xs rounded">
          {component.type.charAt(0).toUpperCase() + component.type.slice(1)} seleccionado
        </div>
      )}
      
      {/* Component preview using shared renderer */}
      <div className="pointer-events-none">
        <ComponentRenderer 
          component={component} 
          theme={theme} 
          isPreview={true}
        />
      </div>
      
      {/* Overlay for interaction */}
      <div className="absolute inset-0 bg-transparent hover:bg-blue-50 hover:bg-opacity-20 transition-colors duration-200" />
    </div>
  );
};

export default SharedComponentPreview;