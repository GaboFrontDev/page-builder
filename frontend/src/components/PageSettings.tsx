import React, { useState, useEffect } from 'react';
import { Page } from '../types';
import { useAuth } from '../contexts/AuthContext';

interface PageSettingsProps {
  page: Page;
  onUpdatePage: (page: Page) => void;
  onSavePage: () => void;
}

const PageSettings: React.FC<PageSettingsProps> = ({
  page,
  onUpdatePage,
  onSavePage
}) => {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    title: page.title,
    slug: page.slug,
    subdomain: page.subdomain,
    description: page.description,
    theme: page.config?.theme || 'default',
    is_published: page.is_published
  });

  useEffect(() => {
    setFormData({
      title: page.title,
      slug: page.slug,
      subdomain: page.subdomain,
      description: page.description,
      theme: page.config?.theme || 'default',
      is_published: page.is_published
    });
  }, [page]);

  const handleInputChange = (field: string, value: any) => {
    const newFormData = { ...formData, [field]: value };
    setFormData(newFormData);
    
    // Actualizar la página en tiempo real
    const updatedPage = {
      ...page,
      [field]: value,
      config: {
        ...page.config,
        theme: field === 'theme' ? value : page.config?.theme || 'default'
      }
    };
    onUpdatePage(updatedPage);
  };

  const handleSlugFocus = () => {
    // Convertir el título a slug si está vacío
    if (!formData.slug && formData.title) {
      const slug = formData.title
        .toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .trim();
      
      handleInputChange('slug', slug);
    }
  };

  const themes = [
    { 
      value: 'default', 
      name: 'Por Defecto', 
      description: 'Diseño limpio y moderno',
      icon: '🎨'
    },
    { 
      value: 'dark', 
      name: 'Oscuro', 
      description: 'Fondo oscuro con texto claro',
      icon: '🌙'
    },
    { 
      value: 'modern', 
      name: 'Moderno', 
      description: 'Gradientes y efectos visuales',
      icon: '✨'
    },
    { 
      value: 'minimal', 
      name: 'Minimalista', 
      description: 'Diseño simple y elegante',
      icon: '⚪'
    }
  ];

  const validateSlug = (slug: string): boolean => {
    const slugRegex = /^[a-z0-9-]+$/;
    return slugRegex.test(slug) && slug.length > 0;
  };

  const isSlugValid = validateSlug(formData.slug);

  return (
    <div className="p-6 space-y-8">
      <div>
        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-6 flex items-center">
          <svg className="w-5 h-5 mr-2 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Configuración de Página
        </h3>
        
        {/* Basic Settings */}
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Título de la Página
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => handleInputChange('title', e.target.value)}
              className="form-input"
              placeholder="Mi Landing Page"
            />
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
              Este será el título que aparece en el navegador
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              URL (Slug)
            </label>
            <div className="flex items-center mb-2">
              <span className="text-sm text-gray-500 dark:text-gray-400 font-mono">
                {formData.subdomain}.localhost/{formData.slug}
              </span>
            </div>
            <input
              type="text"
              value={formData.slug}
              onChange={(e) => handleInputChange('slug', e.target.value)}
              onFocus={handleSlugFocus}
              className={`form-input ${!isSlugValid ? 'border-red-500 dark:border-red-400' : ''}`}
              placeholder="mi-pagina"
            />
            {!isSlugValid && (
              <p className="text-xs text-red-600 dark:text-red-400 mt-2">
                El slug solo puede contener letras minúsculas, números y guiones
              </p>
            )}
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
              URL donde será accesible tu página
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Subdominio
            </label>
            <input
              type="text"
              value={formData.subdomain}
              onChange={(e) => handleInputChange('subdomain', e.target.value)}
              className="form-input"
              placeholder="mi-empresa"
            />
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
              Subdominio personalizado para tu página (ej: mi-empresa.localhost)
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Descripción
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              className="form-input"
              rows={3}
              placeholder="Describe tu página..."
            />
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
              Descripción para SEO y vista previa
            </p>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="is_published"
              checked={formData.is_published}
              onChange={(e) => handleInputChange('is_published', e.target.checked)}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded"
            />
            <label htmlFor="is_published" className="ml-3 text-sm font-medium text-gray-700 dark:text-gray-300">
              Página publicada
            </label>
          </div>
          {!formData.is_published && (
            <p className="text-xs text-yellow-600 dark:text-yellow-400 mt-2">
              La página debe estar publicada para poder ser desplegada
            </p>
          )}
        </div>
      </div>

      {/* Theme Selection */}
      <div>
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <svg className="w-4 h-4 mr-2 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v14a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v14a4 4 0 004 4h4a4 4 0 001-4V5zM7 5h10" />
          </svg>
          Tema Visual
        </h4>
        <div className="space-y-3">
          {themes.map((theme) => (
            <label
              key={theme.value}
              className={`block p-4 border rounded-xl cursor-pointer transition-all duration-200 ${
                formData.theme === theme.value
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-400 shadow-sm'
                  : 'border-gray-200 dark:border-slate-600 hover:border-gray-300 dark:hover:border-slate-500 hover:shadow-sm'
              }`}
            >
              <div className="flex items-center">
                <input
                  type="radio"
                  name="theme"
                  value={theme.value}
                  checked={formData.theme === theme.value}
                  onChange={(e) => handleInputChange('theme', e.target.value)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600"
                />
                <div className="ml-4 flex items-center">
                  <span className="text-2xl mr-3">{theme.icon}</span>
                  <div>
                    <div className="text-sm font-semibold text-gray-900 dark:text-white">
                      {theme.name}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-300">
                      {theme.description}
                    </div>
                  </div>
                </div>
              </div>
            </label>
          ))}
        </div>
      </div>

      {/* Page Info */}
      <div>
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <svg className="w-4 h-4 mr-2 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Información
        </h4>
        <div className="bg-gray-50 dark:bg-slate-700/50 p-4 rounded-xl space-y-3 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">ID:</span>
            <span className="font-mono text-gray-900 dark:text-white">{page.id}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Creado:</span>
            <span className="text-gray-900 dark:text-white">{new Date(page.created_at).toLocaleDateString('es-ES')}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Actualizado:</span>
            <span className="text-gray-900 dark:text-white">{new Date(page.updated_at).toLocaleDateString('es-ES')}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Estado:</span>
            <span className={`font-medium ${formData.is_published ? 'text-green-600 dark:text-green-400' : 'text-yellow-600 dark:text-yellow-400'}`}>
              {formData.is_published ? 'Publicado' : 'Borrador'}
            </span>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="space-y-3">
        <button
          onClick={onSavePage}
          disabled={!isSlugValid}
          className="w-full btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
          </svg>
          Guardar Cambios
        </button>
        
        <div className="text-xs text-gray-500 dark:text-gray-400 text-center">
          Los cambios se guardan automáticamente al editar
        </div>
      </div>

      {/* Tips */}
      <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border border-blue-200 dark:border-blue-800 p-4 rounded-xl">
        <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-3 flex items-center">
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          Consejos
        </h4>
        <ul className="text-sm text-blue-800 dark:text-blue-200 space-y-2">
          <li className="flex items-start">
            <span className="text-blue-600 dark:text-blue-400 mr-2">•</span>
            Usa títulos descriptivos para mejor SEO
          </li>
          <li className="flex items-start">
            <span className="text-blue-600 dark:text-blue-400 mr-2">•</span>
            El slug será la URL de tu página
          </li>
          <li className="flex items-start">
            <span className="text-blue-600 dark:text-blue-400 mr-2">•</span>
            Publica la página antes de desplegarla
          </li>
          <li className="flex items-start">
            <span className="text-blue-600 dark:text-blue-400 mr-2">•</span>
            Elige un tema que refleje tu marca
          </li>
        </ul>
      </div>
    </div>
  );
};

export default PageSettings;