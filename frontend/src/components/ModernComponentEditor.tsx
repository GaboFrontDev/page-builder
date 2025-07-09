import React, { useState } from 'react';
import { Component, ComponentContent, ComponentStyles } from '../types';
import { getDefaultContent, getDefaultStyles, componentLabels } from '@shared/utils/componentDefaults';
import { ComponentRenderer } from '@shared/index';

interface ModernComponentEditorProps {
  component: Component;
  onUpdateComponent: (id: number, updates: Partial<Component>) => void;
  onDeleteComponent: (id: number) => void;
  onClose: () => void;
  theme: string;
}

const ModernComponentEditor: React.FC<ModernComponentEditorProps> = ({
  component,
  onUpdateComponent,
  onDeleteComponent,
  onClose,
  theme
}) => {
  const [content, setContent] = useState<ComponentContent>(component.content);
  const [styles, setStyles] = useState<ComponentStyles>(component.styles);
  const [activeTab, setActiveTab] = useState<'content' | 'styles' | 'preview'>('content');

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

  const resetToDefaults = () => {
    const defaultContent = getDefaultContent(component.type);
    const defaultStyles = getDefaultStyles(component.type);
    setContent(defaultContent);
    setStyles(defaultStyles);
    onUpdateComponent(component.id, { 
      content: defaultContent, 
      styles: defaultStyles 
    });
  };

  const renderContentFields = () => {
    switch (component.type) {
      case 'hero':
        return (
          <div className="space-y-4">
            <InputField
              label="Título"
              value={content.title || ''}
              onChange={(value) => handleContentChange('title', value)}
              placeholder="Título principal"
            />
            <InputField
              label="Subtítulo"
              value={content.subtitle || ''}
              onChange={(value) => handleContentChange('subtitle', value)}
              placeholder="Subtítulo descriptivo"
            />
            <InputField
              label="Imagen URL"
              type="url"
              value={content.image || ''}
              onChange={(value) => handleContentChange('image', value)}
              placeholder="https://ejemplo.com/imagen.jpg"
            />
            <InputField
              label="Texto del botón"
              value={content.cta_text || ''}
              onChange={(value) => handleContentChange('cta_text', value)}
              placeholder="Hacer clic aquí"
            />
            <InputField
              label="Enlace del botón"
              type="url"
              value={content.cta_link || ''}
              onChange={(value) => handleContentChange('cta_link', value)}
              placeholder="#"
            />
          </div>
        );
      
      case 'header':
        return (
          <div className="space-y-4">
            <InputField
              label="Título"
              value={content.title || ''}
              onChange={(value) => handleContentChange('title', value)}
              placeholder="Mi Sitio Web"
            />
            <InputField
              label="Logo URL"
              type="url"
              value={content.logo || ''}
              onChange={(value) => handleContentChange('logo', value)}
              placeholder="https://ejemplo.com/logo.png"
            />
            <ArrayField
              label="Elementos del menú"
              items={content.menu_items || []}
              onChange={(items) => handleContentChange('menu_items', items)}
              defaultItem={{ text: 'Nuevo', link: '#' }}
              renderItem={(item, index, onChange) => (
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={item.text || ''}
                    onChange={(e) => onChange({ ...item, text: e.target.value })}
                    placeholder="Texto"
                    className="form-input flex-1"
                  />
                  <input
                    type="text"
                    value={item.link || ''}
                    onChange={(e) => onChange({ ...item, link: e.target.value })}
                    placeholder="Enlace"
                    className="form-input flex-1"
                  />
                </div>
              )}
            />
          </div>
        );
      
      case 'text':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Contenido
              </label>
              <textarea
                value={content.text || ''}
                onChange={(e) => handleContentChange('text', e.target.value)}
                className="form-input h-32"
                placeholder="<p>Tu contenido aquí. Puedes usar HTML.</p>"
              />
            </div>
            <SelectField
              label="Alineación"
              value={content.alignment || 'left'}
              onChange={(value) => handleContentChange('alignment', value)}
              options={[
                { value: 'left', label: 'Izquierda' },
                { value: 'center', label: 'Centro' },
                { value: 'right', label: 'Derecha' }
              ]}
            />
          </div>
        );
      
      case 'image':
        return (
          <div className="space-y-4">
            <InputField
              label="URL de la imagen"
              type="url"
              value={content.src || ''}
              onChange={(value) => handleContentChange('src', value)}
              placeholder="https://ejemplo.com/imagen.jpg"
            />
            <InputField
              label="Texto alternativo"
              value={content.alt || ''}
              onChange={(value) => handleContentChange('alt', value)}
              placeholder="Descripción de la imagen"
            />
            <InputField
              label="Pie de imagen"
              value={content.caption || ''}
              onChange={(value) => handleContentChange('caption', value)}
              placeholder="Descripción opcional"
            />
          </div>
        );
      
      case 'button':
        return (
          <div className="space-y-4">
            <InputField
              label="Texto del botón"
              value={content.text || ''}
              onChange={(value) => handleContentChange('text', value)}
              placeholder="Hacer clic aquí"
            />
            <InputField
              label="Enlace"
              type="url"
              value={content.link || ''}
              onChange={(value) => handleContentChange('link', value)}
              placeholder="#"
            />
            <SelectField
              label="Variante"
              value={content.variant || 'primary'}
              onChange={(value) => handleContentChange('variant', value)}
              options={[
                { value: 'primary', label: 'Primario' },
                { value: 'secondary', label: 'Secundario' },
                { value: 'outline', label: 'Contorno' },
                { value: 'success', label: 'Éxito' },
                { value: 'danger', label: 'Peligro' }
              ]}
            />
          </div>
        );
      
      case 'footer':
        return (
          <div className="space-y-4">
            <InputField
              label="Texto del footer"
              value={content.text || ''}
              onChange={(value) => handleContentChange('text', value)}
              placeholder="© 2024 Mi Sitio Web"
            />
            <ArrayField
              label="Enlaces del footer"
              items={content.links || []}
              onChange={(items) => handleContentChange('links', items)}
              defaultItem={{ text: 'Nuevo enlace', url: '#' }}
              renderItem={(item, index, onChange) => (
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={item.text || ''}
                    onChange={(e) => onChange({ ...item, text: e.target.value })}
                    placeholder="Texto"
                    className="form-input flex-1"
                  />
                  <input
                    type="url"
                    value={item.url || ''}
                    onChange={(e) => onChange({ ...item, url: e.target.value })}
                    placeholder="URL"
                    className="form-input flex-1"
                  />
                </div>
              )}
            />
          </div>
        );
      
      default:
        return (
          <div className="text-center py-8 text-gray-500">
            Editor no disponible para este tipo de componente
          </div>
        );
    }
  };

  const renderStylesFields = () => (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <InputField
          label="Padding"
          value={styles.padding || ''}
          onChange={(value) => handleStyleChange('padding', value)}
          placeholder="20px"
        />
        <InputField
          label="Margin"
          value={styles.margin || ''}
          onChange={(value) => handleStyleChange('margin', value)}
          placeholder="10px"
        />
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <InputField
          label="Color de fondo"
          type="color"
          value={styles.backgroundColor || '#ffffff'}
          onChange={(value) => handleStyleChange('backgroundColor', value)}
        />
        <InputField
          label="Color de texto"
          type="color"
          value={styles.color || '#000000'}
          onChange={(value) => handleStyleChange('color', value)}
        />
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <InputField
          label="Tamaño de fuente"
          value={styles.fontSize || ''}
          onChange={(value) => handleStyleChange('fontSize', value)}
          placeholder="16px"
        />
        <SelectField
          label="Peso de fuente"
          value={styles.fontWeight || 'normal'}
          onChange={(value) => handleStyleChange('fontWeight', value)}
          options={[
            { value: 'normal', label: 'Normal' },
            { value: 'bold', label: 'Negrita' },
            { value: '100', label: 'Muy ligera' },
            { value: '300', label: 'Ligera' },
            { value: '500', label: 'Media' },
            { value: '700', label: 'Negrita' },
            { value: '900', label: 'Muy negrita' }
          ]}
        />
      </div>
      
      <InputField
        label="Border radius"
        value={styles.borderRadius || ''}
        onChange={(value) => handleStyleChange('borderRadius', value)}
        placeholder="8px"
      />
      
      <SelectField
        label="Alineación de texto"
        value={styles.textAlign || 'left'}
        onChange={(value) => handleStyleChange('textAlign', value)}
        options={[
          { value: 'left', label: 'Izquierda' },
          { value: 'center', label: 'Centro' },
          { value: 'right', label: 'Derecha' }
        ]}
      />
    </div>
  );

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            Editar {componentLabels[component.type]}
          </h2>
          <div className="flex items-center gap-2">
            <button
              onClick={resetToDefaults}
              className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-md transition-colors"
            >
              Restaurar
            </button>
            <button
              title="Cerrar"
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-gray-200 dark:border-gray-700">
          {['content', 'styles', 'preview'].map((tab) => (
            <button
              title={tab}
              key={tab}
              onClick={() => setActiveTab(tab as any)}
              className={`px-6 py-3 text-sm font-medium capitalize transition-colors ${
                activeTab === tab
                  ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-blue-900/20'
                  : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
              }`}
            >
              {tab === 'content' ? 'Contenido' : tab === 'styles' ? 'Estilos' : 'Vista previa'}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto">
          <div className="p-6">
            {activeTab === 'content' && renderContentFields()}
            {activeTab === 'styles' && renderStylesFields()}
            {activeTab === 'preview' && (
              <div className="border rounded-lg overflow-hidden">
                <ComponentRenderer
                  component={{ ...component, content, styles }}
                  theme={theme}
                  isPreview={true}
                />
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-6 border-t border-gray-200 dark:border-gray-700">
          <button
            title="Eliminar componente"
            onClick={() => onDeleteComponent(component.id)}
            className="px-4 py-2 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 font-medium transition-colors"
          >
            Eliminar componente
          </button>
          <button
            title="Guardar cambios"
            onClick={onClose}
            className="btn btn-primary"
          >
            Guardar cambios
          </button>
        </div>
      </div>
    </div>
  );
};

// Helper Components
interface InputFieldProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
  placeholder?: string;
}

const InputField: React.FC<InputFieldProps> = ({ 
  label, 
  value, 
  onChange, 
  type = 'text', 
  placeholder 
}) => (
  <div>
    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
      {label}
    </label>
    <input
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="form-input"
      placeholder={placeholder}
    />
  </div>
);

interface SelectFieldProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: { value: string; label: string }[];
}

const SelectField: React.FC<SelectFieldProps> = ({ label, value, onChange, options }) => (
  <div>
    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
      {label}
    </label>
    <select
      title={label}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="form-input"
    >
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  </div>
);

interface ArrayFieldProps {
  label: string;
  items: any[];
  onChange: (items: any[]) => void;
  defaultItem: any;
  renderItem: (item: any, index: number, onChange: (item: any) => void) => React.ReactNode;
}

const ArrayField: React.FC<ArrayFieldProps> = ({ 
  label, 
  items, 
  onChange, 
  defaultItem, 
  renderItem 
}) => {
  const addItem = () => {
    onChange([...items, { ...defaultItem }]);
  };

  const removeItem = (index: number) => {
    onChange(items.filter((_, i) => i !== index));
  };

  const updateItem = (index: number, item: any) => {
    const newItems = [...items];
    newItems[index] = item;
    onChange(newItems);
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
        {label}
      </label>
      {items.map((item, index) => (
        <div key={index} className="flex gap-2 mb-3">
          {renderItem(item, index, (newItem) => updateItem(index, newItem))}
          <button
            title="Eliminar"
            onClick={() => removeItem(index)}
            className="px-3 py-2 text-red-600 hover:text-red-800 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      ))}
      <button
        title="Agregar"
        onClick={addItem}
        className="btn btn-secondary text-sm"
      >
        Agregar {label.toLowerCase()}
      </button>
    </div>
  );
};

export default ModernComponentEditor;