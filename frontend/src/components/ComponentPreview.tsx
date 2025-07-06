import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Component } from '../types';

interface ComponentPreviewProps {
  component: Component;
  isSelected: boolean;
  onSelect: () => void;
  theme: string;
}

const ComponentPreview: React.FC<ComponentPreviewProps> = ({
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
    ...component.styles,
  } as React.CSSProperties;

  const renderComponentContent = () => {
    const { content } = component;
    
    switch (component.type) {
      case 'header':
        return (
          <header className="bg-white border-b border-gray-200 px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                {content.logo && (
                  <img src={content.logo} alt="Logo" className="h-8 w-auto" />
                )}
                <h1 className="text-xl font-bold text-gray-900">
                  {content.title || 'Título del Sitio'}
                </h1>
              </div>
              {content.menu_items && (
                <nav className="flex space-x-6">
                  {content.menu_items.map((item: any, index: number) => (
                    <a
                      key={index}
                      href={item.link}
                      className="text-gray-700 hover:text-gray-900"
                    >
                      {item.text}
                    </a>
                  ))}
                </nav>
              )}
            </div>
          </header>
        );

      case 'hero':
        return (
          <section className="relative bg-gradient-to-r from-blue-600 to-purple-600 text-white py-24 px-6">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl font-bold mb-6">
                {content.title || 'Título Principal'}
              </h1>
              {content.subtitle && (
                <p className="text-xl mb-8 opacity-90">
                  {content.subtitle}
                </p>
              )}
              {content.cta_text && (
                <a
                  href={content.cta_link || '#'}
                  className="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
                >
                  {content.cta_text}
                </a>
              )}
            </div>
            {content.image && (
              <div className="absolute inset-0 z-0">
                <img
                  src={content.image}
                  alt="Hero background"
                  className="w-full h-full object-cover opacity-30"
                />
              </div>
            )}
          </section>
        );

      case 'text':
        return (
          <section className="py-16 px-6">
            <div className="max-w-4xl mx-auto">
              <div 
                className={`prose prose-lg ${content.alignment === 'center' ? 'text-center mx-auto' : content.alignment === 'right' ? 'text-right ml-auto' : ''}`}
                dangerouslySetInnerHTML={{ 
                  __html: content.text || '<p>Contenido de texto aquí...</p>' 
                }}
              />
            </div>
          </section>
        );

      case 'image':
        return (
          <section className="py-8 px-6">
            <div className="max-w-4xl mx-auto text-center">
              <img
                src={content.src || 'https://via.placeholder.com/600x400'}
                alt={content.alt || 'Imagen'}
                className="w-full h-auto rounded-lg shadow-lg"
              />
              {content.caption && (
                <p className="mt-4 text-gray-600 italic">
                  {content.caption}
                </p>
              )}
            </div>
          </section>
        );

      case 'button':
        return (
          <section className="py-8 px-6 text-center">
            <a
              href={content.link || '#'}
              className={`inline-block px-8 py-3 rounded-lg font-semibold transition-colors ${
                content.variant === 'secondary' 
                  ? 'bg-gray-600 text-white hover:bg-gray-700'
                  : content.variant === 'success'
                  ? 'bg-green-600 text-white hover:bg-green-700'
                  : content.variant === 'danger'
                  ? 'bg-red-600 text-white hover:bg-red-700'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              {content.text || 'Botón'}
            </a>
          </section>
        );

      case 'footer':
        return (
          <footer className="bg-gray-800 text-white py-12 px-6">
            <div className="max-w-4xl mx-auto text-center">
              <p className="mb-4">
                {content.text || '© 2024 Mi Sitio Web. Todos los derechos reservados.'}
              </p>
              {content.links && content.links.length > 0 && (
                <div className="flex justify-center space-x-6">
                  {content.links.map((link: any, index: number) => (
                    <a
                      key={index}
                      href={link.url}
                      className="text-gray-300 hover:text-white"
                    >
                      {link.text}
                    </a>
                  ))}
                </div>
              )}
            </div>
          </footer>
        );

      default:
        return (
          <div className="py-8 px-6 text-center text-gray-500">
            Componente no reconocido: {component.type}
          </div>
        );
    }
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      className={`component-preview group ${isSelected ? 'selected' : ''} ${
        isDragging ? 'opacity-50' : ''
      }`}
      onClick={onSelect}
    >
      {/* Drag Handle */}
      <div
        {...listeners}
        className="component-actions"
      >
        <button className="btn btn-secondary text-xs p-1" title="Arrastrar">
          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
          </svg>
        </button>
      </div>

      {/* Component Content */}
      <div className="pointer-events-none">
        {renderComponentContent()}
      </div>

      {/* Selection Indicator */}
      {isSelected && (
        <div className="absolute inset-0 border-2 border-blue-500 pointer-events-none">
          <div className="absolute -top-6 left-0 bg-blue-500 text-white text-xs px-2 py-1 rounded">
            {component.type}
          </div>
        </div>
      )}
    </div>
  );
};

export default ComponentPreview;