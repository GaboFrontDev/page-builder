import React, { useState } from 'react';
import { Component, ComponentContent } from '../types';

interface ComponentEditorProps {
  component: Component;
  onUpdateComponent: (id: number, updates: Partial<Component>) => void;
  onDeleteComponent: (id: number) => void;
  onClose: () => void;
}

const ComponentEditor: React.FC<ComponentEditorProps> = ({
  component,
  onUpdateComponent,
  onDeleteComponent,
  onClose
}) => {
  const [content, setContent] = useState<ComponentContent>(component.content);
  const [styles, setStyles] = useState(component.styles);

  const handleContentChange = (field: string, value: any) => {
    const newContent = { ...content, [field]: value };
    setContent(newContent);
    onUpdateComponent(component.id, { content: newContent });
  };

  const handleStyleChange = (field: string, value: string) => {
    const newStyles = { ...styles, [field]: value };
    setStyles(newStyles);
    onUpdateComponent(component.id, { styles: newStyles });
  };

  const handleArrayFieldChange = (field: string, index: number, subField: string, value: string) => {
    const array = content[field] as any[] || [];
    const newArray = [...array];
    newArray[index] = { ...newArray[index], [subField]: value };
    handleContentChange(field, newArray);
  };

  const addArrayItem = (field: string, defaultItem: any) => {
    const array = content[field] as any[] || [];
    handleContentChange(field, [...array, defaultItem]);
  };

  const removeArrayItem = (field: string, index: number) => {
    const array = content[field] as any[] || [];
    const newArray = array.filter((_, i) => i !== index);
    handleContentChange(field, newArray);
  };

  const renderHeaderEditor = () => (
    <div className="space-y-4">
      <div>
        <label className="form-label">Título</label>
        <input
          type="text"
          value={content.title || ''}
          onChange={(e) => handleContentChange('title', e.target.value)}
          className="form-input"
        />
      </div>
      
      <div>
        <label className="form-label">Logo URL</label>
        <input
          type="url"
          value={content.logo || ''}
          onChange={(e) => handleContentChange('logo', e.target.value)}
          className="form-input"
          placeholder="https://ejemplo.com/logo.png"
        />
      </div>
      
      <div>
        <label className="form-label">Elementos del Menú</label>
        {(content.menu_items as any[] || []).map((item, index) => (
          <div key={index} className="flex gap-2 mb-2">
            <input
              type="text"
              value={item.text || ''}
              onChange={(e) => handleArrayFieldChange('menu_items', index, 'text', e.target.value)}
              placeholder="Texto"
              className="form-input flex-1"
            />
            <input
              type="text"
              value={item.link || ''}
              onChange={(e) => handleArrayFieldChange('menu_items', index, 'link', e.target.value)}
              placeholder="Enlace"
              className="form-input flex-1"
            />
            <button
              onClick={() => removeArrayItem('menu_items', index)}
              className="btn btn-danger text-sm px-2"
            >
              ×
            </button>
          </div>
        ))}
        <button
          onClick={() => addArrayItem('menu_items', { text: 'Nuevo', link: '#' })}
          className="btn btn-secondary text-sm mt-2"
        >
          + Agregar elemento
        </button>
      </div>
    </div>
  );

  const renderHeroEditor = () => (
    <div className="space-y-4">
      <div>
        <label className="form-label">Título Principal</label>
        <input
          type="text"
          value={content.title || ''}
          onChange={(e) => handleContentChange('title', e.target.value)}
          className="form-input"
        />
      </div>
      
      <div>
        <label className="form-label">Subtítulo</label>
        <textarea
          value={content.subtitle || ''}
          onChange={(e) => handleContentChange('subtitle', e.target.value)}
          className="form-input"
          rows={3}
        />
      </div>
      
      <div>
        <label className="form-label">Texto del Botón</label>
        <input
          type="text"
          value={content.cta_text || ''}
          onChange={(e) => handleContentChange('cta_text', e.target.value)}
          className="form-input"
        />
      </div>
      
      <div>
        <label className="form-label">Enlace del Botón</label>
        <input
          type="url"
          value={content.cta_link || ''}
          onChange={(e) => handleContentChange('cta_link', e.target.value)}
          className="form-input"
        />
      </div>
      
      <div>
        <label className="form-label">Imagen de Fondo URL</label>
        <input
          type="url"
          value={content.image || ''}
          onChange={(e) => handleContentChange('image', e.target.value)}
          className="form-input"
          placeholder="https://ejemplo.com/imagen.jpg"
        />
      </div>
    </div>
  );

  const renderTextEditor = () => (
    <div className="space-y-4">
      <div>
        <label className="form-label">Contenido (HTML)</label>
        <textarea
          value={content.text || ''}
          onChange={(e) => handleContentChange('text', e.target.value)}
          className="form-input"
          rows={8}
          placeholder="<h2>Título</h2><p>Tu contenido aquí...</p>"
        />
      </div>
      
      <div>
        <label className="form-label">Alineación</label>
        <select
          value={content.alignment || 'left'}
          onChange={(e) => handleContentChange('alignment', e.target.value)}
          className="form-input"
        >
          <option value="left">Izquierda</option>
          <option value="center">Centro</option>
          <option value="right">Derecha</option>
        </select>
      </div>
    </div>
  );

  const renderImageEditor = () => (
    <div className="space-y-4">
      <div>
        <label className="form-label">URL de la Imagen</label>
        <input
          type="url"
          value={content.src || ''}
          onChange={(e) => handleContentChange('src', e.target.value)}
          className="form-input"
          placeholder="https://ejemplo.com/imagen.jpg"
        />
      </div>
      
      <div>
        <label className="form-label">Texto Alternativo</label>
        <input
          type="text"
          value={content.alt || ''}
          onChange={(e) => handleContentChange('alt', e.target.value)}
          className="form-input"
        />
      </div>
      
      <div>
        <label className="form-label">Pie de Imagen</label>
        <input
          type="text"
          value={content.caption || ''}
          onChange={(e) => handleContentChange('caption', e.target.value)}
          className="form-input"
        />
      </div>
    </div>
  );

  const renderButtonEditor = () => (
    <div className="space-y-4">
      <div>
        <label className="form-label">Texto del Botón</label>
        <input
          type="text"
          value={content.text || ''}
          onChange={(e) => handleContentChange('text', e.target.value)}
          className="form-input"
        />
      </div>
      
      <div>
        <label className="form-label">Enlace</label>
        <input
          type="url"
          value={content.link || ''}
          onChange={(e) => handleContentChange('link', e.target.value)}
          className="form-input"
        />
      </div>
      
      <div>
        <label className="form-label">Estilo</label>
        <select
          value={content.variant || 'primary'}
          onChange={(e) => handleContentChange('variant', e.target.value)}
          className="form-input"
        >
          <option value="primary">Primario</option>
          <option value="secondary">Secundario</option>
          <option value="success">Éxito</option>
          <option value="danger">Peligro</option>
        </select>
      </div>
    </div>
  );

  const renderFooterEditor = () => (
    <div className="space-y-4">
      <div>
        <label className="form-label">Texto del Footer</label>
        <textarea
          value={content.text || ''}
          onChange={(e) => handleContentChange('text', e.target.value)}
          className="form-input"
          rows={3}
        />
      </div>
      
      <div>
        <label className="form-label">Enlaces</label>
        {(content.links as any[] || []).map((link, index) => (
          <div key={index} className="flex gap-2 mb-2">
            <input
              type="text"
              value={link.text || ''}
              onChange={(e) => handleArrayFieldChange('links', index, 'text', e.target.value)}
              placeholder="Texto"
              className="form-input flex-1"
            />
            <input
              type="url"
              value={link.url || ''}
              onChange={(e) => handleArrayFieldChange('links', index, 'url', e.target.value)}
              placeholder="URL"
              className="form-input flex-1"
            />
            <button
              onClick={() => removeArrayItem('links', index)}
              className="btn btn-danger text-sm px-2"
            >
              ×
            </button>
          </div>
        ))}
        <button
          onClick={() => addArrayItem('links', { text: 'Nuevo enlace', url: '#' })}
          className="btn btn-secondary text-sm mt-2"
        >
          + Agregar enlace
        </button>
      </div>
    </div>
  );

  const renderContentEditor = () => {
    switch (component.type) {
      case 'header':
        return renderHeaderEditor();
      case 'hero':
        return renderHeroEditor();
      case 'text':
        return renderTextEditor();
      case 'image':
        return renderImageEditor();
      case 'button':
        return renderButtonEditor();
      case 'footer':
        return renderFooterEditor();
      default:
        return <div>Editor no disponible para este tipo de componente.</div>;
    }
  };

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">
          Editar {component.type}
        </h3>
        <button
          onClick={onClose}
          className="text-gray-500 hover:text-gray-700"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-6">
          {/* Content Editor */}
          <div>
            <h4 className="text-md font-medium text-gray-900 mb-3">Contenido</h4>
            {renderContentEditor()}
          </div>

          {/* Styles Editor */}
          <div>
            <h4 className="text-md font-medium text-gray-900 mb-3">Estilos</h4>
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="form-label">Color de Fondo</label>
                  <input
                    type="color"
                    value={styles.backgroundColor || '#ffffff'}
                    onChange={(e) => handleStyleChange('backgroundColor', e.target.value)}
                    className="form-input h-10"
                  />
                </div>
                <div>
                  <label className="form-label">Color de Texto</label>
                  <input
                    type="color"
                    value={styles.color || '#000000'}
                    onChange={(e) => handleStyleChange('color', e.target.value)}
                    className="form-input h-10"
                  />
                </div>
              </div>
              
              <div>
                <label className="form-label">Padding</label>
                <input
                  type="text"
                  value={styles.padding || ''}
                  onChange={(e) => handleStyleChange('padding', e.target.value)}
                  className="form-input"
                  placeholder="ej: 20px 40px"
                />
              </div>
              
              <div>
                <label className="form-label">Margin</label>
                <input
                  type="text"
                  value={styles.margin || ''}
                  onChange={(e) => handleStyleChange('margin', e.target.value)}
                  className="form-input"
                  placeholder="ej: 10px 0px"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="form-label">Tamaño de Fuente</label>
                  <input
                    type="text"
                    value={styles.fontSize || ''}
                    onChange={(e) => handleStyleChange('fontSize', e.target.value)}
                    className="form-input"
                    placeholder="ej: 16px"
                  />
                </div>
                <div>
                  <label className="form-label">Peso de Fuente</label>
                  <select
                    value={styles.fontWeight || 'normal'}
                    onChange={(e) => handleStyleChange('fontWeight', e.target.value)}
                    className="form-input"
                  >
                    <option value="normal">Normal</option>
                    <option value="bold">Negrita</option>
                    <option value="lighter">Ligera</option>
                    <option value="300">300</option>
                    <option value="500">500</option>
                    <option value="700">700</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="form-label">Border Radius</label>
                <input
                  type="text"
                  value={styles.borderRadius || ''}
                  onChange={(e) => handleStyleChange('borderRadius', e.target.value)}
                  className="form-input"
                  placeholder="ej: 8px"
                />
              </div>
              
              <div>
                <label className="form-label">Border</label>
                <input
                  type="text"
                  value={styles.border || ''}
                  onChange={(e) => handleStyleChange('border', e.target.value)}
                  className="form-input"
                  placeholder="ej: 1px solid #ccc"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <button
          onClick={() => onDeleteComponent(component.id)}
          className="w-full btn btn-danger"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Eliminar Componente
        </button>
      </div>
    </div>
  );
};

export default ComponentEditor;