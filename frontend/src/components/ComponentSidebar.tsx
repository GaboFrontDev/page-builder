import React from 'react';
import { ComponentType, Component } from '../types';

interface ComponentSidebarProps {
  onAddComponent: (type: ComponentType) => void;
  selectedComponent: Component | null;
  onUpdateComponent: (id: number, updates: Partial<Component>) => void;
  onDeleteComponent: (id: number) => void;
}

const ComponentSidebar: React.FC<ComponentSidebarProps> = ({
  onAddComponent,
  selectedComponent,
  onUpdateComponent,
  onDeleteComponent
}) => {
  const componentTypes: Array<{
    type: ComponentType;
    name: string;
    description: string;
    icon: string;
  }> = [
    {
      type: 'header',
      name: 'Header',
      description: 'Navegación y logo del sitio',
      icon: '🧭'
    },
    {
      type: 'hero',
      name: 'Hero Section',
      description: 'Sección principal con título y CTA',
      icon: '🏆'
    },
    {
      type: 'text',
      name: 'Texto',
      description: 'Sección de contenido de texto',
      icon: '📝'
    },
    {
      type: 'image',
      name: 'Imagen',
      description: 'Imagen con caption opcional',
      icon: '🖼️'
    },
    {
      type: 'button',
      name: 'Botón',
      description: 'Botón de llamada a la acción',
      icon: '🔲'
    },
    {
      type: 'footer',
      name: 'Footer',
      description: 'Pie de página con enlaces',
      icon: '📄'
    }
  ];

  return (
    <div className="p-4">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Agregar Componentes
      </h3>
      
      <div className="space-y-2">
        {componentTypes.map((componentType) => (
          <button
            key={componentType.type}
            onClick={() => onAddComponent(componentType.type)}
            className="component-item w-full text-left"
          >
            <span className="text-2xl mr-3">{componentType.icon}</span>
            <div>
              <div className="font-medium text-gray-900">
                {componentType.name}
              </div>
              <div className="text-sm text-gray-600">
                {componentType.description}
              </div>
            </div>
          </button>
        ))}
      </div>

      {selectedComponent && (
        <div className="mt-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Componente Seleccionado
          </h3>
          
          <div className="card">
            <div className="card-body">
              <div className="flex items-center justify-between mb-3">
                <span className="font-medium text-gray-900">
                  {componentTypes.find(t => t.type === selectedComponent.type)?.name}
                </span>
                <button
                  onClick={() => onDeleteComponent(selectedComponent.id)}
                  className="text-red-600 hover:text-red-800"
                  title="Eliminar componente"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
              
              <div className="space-y-3">
                <div>
                  <label className="form-label">Posición</label>
                  <input
                    type="number"
                    value={selectedComponent.position}
                    onChange={(e) => onUpdateComponent(selectedComponent.id, {
                      position: parseInt(e.target.value)
                    })}
                    className="form-input"
                    min="1"
                  />
                </div>
                
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="is_visible"
                    checked={selectedComponent.is_visible}
                    onChange={(e) => onUpdateComponent(selectedComponent.id, {
                      is_visible: e.target.checked
                    })}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label htmlFor="is_visible" className="ml-2 text-sm text-gray-700">
                    Visible
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="mt-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Ayuda
        </h3>
        
        <div className="bg-blue-50 p-4 rounded-lg">
          <h4 className="font-medium text-blue-900 mb-2">
            Cómo usar el editor
          </h4>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Haz clic en un componente para agregarlo</li>
            <li>• Selecciona componentes en el canvas para editarlos</li>
            <li>• Arrastra componentes para reordenarlos</li>
            <li>• Usa el panel derecho para editar contenido</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ComponentSidebar;