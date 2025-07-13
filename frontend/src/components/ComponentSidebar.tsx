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
    <div className="p-6">
      <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-6 flex items-center">
        <svg className="w-5 h-5 mr-2 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Agregar Componentes
      </h3>
      
      <div className="space-y-3">
        {componentTypes.map((componentType) => (
          <button
            key={componentType.type}
            onClick={() => onAddComponent(componentType.type)}
            className="w-full text-left p-4 bg-white dark:bg-slate-700 rounded-xl border border-gray-200 dark:border-slate-600 hover:border-blue-300 dark:hover:border-blue-500 hover:shadow-md dark:hover:shadow-slate-900/50 transition-all duration-200 group"
          >
            <div className="flex items-center">
              <span className="text-2xl mr-4 group-hover:scale-110 transition-transform duration-200">{componentType.icon}</span>
              <div>
                <div className="font-semibold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors duration-200">
                  {componentType.name}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                  {componentType.description}
                </div>
              </div>
            </div>
          </button>
        ))}
      </div>

      {selectedComponent && (
        <div className="mt-8">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center">
            <svg className="w-5 h-5 mr-2 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Componente Seleccionado
          </h3>
          
          <div className="card">
            <div className="card-body">
              <div className="flex items-center justify-between mb-4">
                <span className="font-semibold text-gray-900 dark:text-white">
                  {componentTypes.find(t => t.type === selectedComponent.type)?.name}
                </span>
                <button
                  onClick={() => onDeleteComponent(selectedComponent.id)}
                  className="p-2 text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors duration-200"
                  title="Eliminar componente"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Posición
                  </label>
                  <input
                    title="Posición"
                    placeholder="Posición"
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
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded"
                  />
                  <label htmlFor="is_visible" className="ml-3 text-sm font-medium text-gray-700 dark:text-gray-300">
                    Visible
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="mt-8">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center">
          <svg className="w-5 h-5 mr-2 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Ayuda
        </h3>
        
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border border-blue-200 dark:border-blue-800 p-4 rounded-xl">
          <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-3">
            Cómo usar el editor
          </h4>
          <ul className="text-sm text-blue-800 dark:text-blue-200 space-y-2">
            <li className="flex items-start">
              <span className="text-blue-600 dark:text-blue-400 mr-2">•</span>
              Haz clic en un componente para agregarlo
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 dark:text-blue-400 mr-2">•</span>
              Selecciona componentes en el canvas para editarlos
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 dark:text-blue-400 mr-2">•</span>
              Arrastra componentes para reordenarlos
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 dark:text-blue-400 mr-2">•</span>
              Usa el panel derecho para editar contenido
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ComponentSidebar;