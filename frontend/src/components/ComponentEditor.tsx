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

  // Helper function to safely get string values
  const getStringValue = (value: any): string => {
    if (value === null || value === undefined) return '';
    if (typeof value === 'string') return value;
    if (typeof value === 'number') return value.toString();
    if (typeof value === 'boolean') return value.toString();
    if (typeof value === 'object') return '';
    return String(value);
  };

  const renderHeaderEditor = () => (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Título
        </label>
        <input
          type="text"
          value={getStringValue(content.title)}
          onChange={(e) => handleContentChange('title', e.target.value)}
          className="form-input"
          placeholder="Título del sitio"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Logo URL
        </label>
        <input
          type="url"
          value={getStringValue(content.logo)}
          onChange={(e) => handleContentChange('logo', e.target.value)}
          className="form-input"
          placeholder="https://ejemplo.com/logo.png"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Elementos del Menú
        </label>
        {(content.menu_items as any[] || []).map((item, index) => (
          <div key={index} className="flex gap-2 mb-3">
            <input
              type="text"
              value={getStringValue(item?.text)}
              onChange={(e) => handleArrayFieldChange('menu_items', index, 'text', e.target.value)}
              placeholder="Texto"
              className="form-input flex-1"
            />
            <input
              type="text"
              value={getStringValue(item?.link)}
              onChange={(e) => handleArrayFieldChange('menu_items', index, 'link', e.target.value)}
              placeholder="Enlace"
              className="form-input flex-1"
            />
            <button
              onClick={() => removeArrayItem('menu_items', index)}
              className="btn btn-danger px-3"
              title="Eliminar elemento"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        ))}
        <button
          onClick={() => addArrayItem('menu_items', { text: 'Nuevo', link: '#' })}
          className="btn btn-outline w-full"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Agregar elemento
        </button>
      </div>
    </div>
  );

  const renderHeroEditor = () => (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Título Principal
        </label>
        <input
          type="text"
          value={getStringValue(content.title)}
          onChange={(e) => handleContentChange('title', e.target.value)}
          className="form-input"
          placeholder="Título atractivo"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Subtítulo
        </label>
        <textarea
          value={getStringValue(content.subtitle)}
          onChange={(e) => handleContentChange('subtitle', e.target.value)}
          className="form-input"
          rows={3}
          placeholder="Descripción atractiva de tu producto o servicio"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Texto del Botón
        </label>
        <input
          type="text"
          value={getStringValue(content.cta_text)}
          onChange={(e) => handleContentChange('cta_text', e.target.value)}
          className="form-input"
          placeholder="Comenzar"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Enlace del Botón
        </label>
        <input
          type="url"
          value={getStringValue(content.cta_link)}
          onChange={(e) => handleContentChange('cta_link', e.target.value)}
          className="form-input"
          placeholder="https://ejemplo.com"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Imagen de Fondo URL
        </label>
        <input
          type="url"
          value={getStringValue(content.image)}
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
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Contenido (HTML)
        </label>
        <textarea
          value={getStringValue(content.text)}
          onChange={(e) => handleContentChange('text', e.target.value)}
          className="form-input"
          rows={8}
          placeholder="<h2>Título</h2><p>Tu contenido aquí...</p>"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Alineación
        </label>
        <select
          title="Alineación"
          value={getStringValue(content.alignment) || 'left'}
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
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          URL de la Imagen
        </label>
        <input
          type="url"
          value={getStringValue(content.src)}
          onChange={(e) => handleContentChange('src', e.target.value)}
          className="form-input"
          placeholder="https://ejemplo.com/imagen.jpg"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Texto Alternativo
        </label>
        <input
          type="text"
          value={getStringValue(content.alt)}
          onChange={(e) => handleContentChange('alt', e.target.value)}
          className="form-input"
          placeholder="Descripción de la imagen"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Caption
        </label>
        <input
          type="text"
          value={getStringValue(content.caption)}
          onChange={(e) => handleContentChange('caption', e.target.value)}
          className="form-input"
          placeholder="Descripción de la imagen"
        />
      </div>
    </div>
  );

  const renderButtonEditor = () => (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Texto del Botón
        </label>
        <input
          type="text"
          value={getStringValue(content.text)}
          onChange={(e) => handleContentChange('text', e.target.value)}
          className="form-input"
          placeholder="Comenzar"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Enlace
        </label>
        <input
          type="url"
          value={getStringValue(content.link)}
          onChange={(e) => handleContentChange('link', e.target.value)}
          className="form-input"
          placeholder="https://ejemplo.com"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Variante
        </label>
        <select
          title="Variante"
          value={getStringValue(content.variant) || 'primary'}
          onChange={(e) => handleContentChange('variant', e.target.value)}
          className="form-input"
        >
          <option value="primary">Primario</option>
          <option value="secondary">Secundario</option>
          <option value="outline">Outline</option>
        </select>
      </div>
    </div>
  );

  const renderFooterEditor = () => (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Texto del Footer
        </label>
        <textarea
          value={getStringValue(content.text)}
          onChange={(e) => handleContentChange('text', e.target.value)}
          className="form-input"
          rows={3}
          placeholder="© 2024 Mi Sitio Web. Todos los derechos reservados."
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Enlaces
        </label>
        {(content.links as any[] || []).map((link, index) => (
          <div key={index} className="flex gap-2 mb-3">
            <input
              type="text"
              value={getStringValue(link?.text)}
              onChange={(e) => handleArrayFieldChange('links', index, 'text', e.target.value)}
              placeholder="Texto"
              className="form-input flex-1"
            />
            <input
              type="url"
              value={getStringValue(link?.url)}
              onChange={(e) => handleArrayFieldChange('links', index, 'url', e.target.value)}
              placeholder="URL"
              className="form-input flex-1"
            />
            <button
              onClick={() => removeArrayItem('links', index)}
              className="btn btn-danger px-3"
              title="Eliminar enlace"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        ))}
        <button
          onClick={() => addArrayItem('links', { text: 'Nuevo enlace', url: '#' })}
          className="btn btn-outline w-full"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Agregar enlace
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
    <div className="h-full flex flex-col bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b border-gray-200/50 dark:border-slate-700/50">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center">
          <svg className="w-5 h-5 mr-2 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          Editar {component.type}
        </h3>
        <button
          title="Cerrar"
          onClick={onClose}
          className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg transition-colors duration-200"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="space-y-8">
          {/* Content Editor */}
          <div>
            <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <svg className="w-4 h-4 mr-2 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v14a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v14a4 4 0 004 4h4a4 4 0 001-4V5zM7 5h10" />
              </svg>
              Contenido
            </h4>
            {renderContentEditor()}
          </div>

          {/* Styles Editor */}
          <div>
            <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <svg className="w-4 h-4 mr-2 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v14a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v14a4 4 0 004 4h4a4 4 0 001-4V5zM7 5h10" />
              </svg>
              Estilos
            </h4>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Color de Fondo
                  </label>
                  <input
                    title="Color de Fondo"
                    type="color"
                    value={getStringValue(styles.backgroundColor) || '#ffffff'}
                    onChange={(e) => handleStyleChange('backgroundColor', e.target.value)}
                    className="form-input h-10 w-full"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Color de Texto
                  </label>
                  <input
                    title="Color de Texto"
                    type="color"
                    value={getStringValue(styles.color) || '#000000'}
                    onChange={(e) => handleStyleChange('color', e.target.value)}
                    className="form-input h-10 w-full"
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Padding
                </label>
                <input
                  title="Padding"
                  type="text"
                  value={getStringValue(styles.padding)}
                  onChange={(e) => handleStyleChange('padding', e.target.value)}
                  className="form-input"
                  placeholder="ej: 20px 40px"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Margin
                </label>
                <input
                  type="text"
                  value={getStringValue(styles.margin)}
                  onChange={(e) => handleStyleChange('margin', e.target.value)}
                  className="form-input"
                  placeholder="ej: 10px 0px"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Tamaño de Fuente
                  </label>
                  <input
                    type="text"
                    value={getStringValue(styles.fontSize)}
                    onChange={(e) => handleStyleChange('fontSize', e.target.value)}
                    className="form-input"
                    placeholder="ej: 16px"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Peso de Fuente
                  </label>
                  <select
                    title="Peso de Fuente"
                    value={getStringValue(styles.fontWeight) || 'normal'}
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
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Border Radius
                </label>
                <input
                  type="text"
                  value={getStringValue(styles.borderRadius)}
                  onChange={(e) => handleStyleChange('borderRadius', e.target.value)}
                  className="form-input"
                  placeholder="ej: 8px"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Border
                </label>
                <input
                  type="text"
                  value={getStringValue(styles.border)}
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
      <div className="p-6 border-t border-gray-200/50 dark:border-slate-700/50">
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