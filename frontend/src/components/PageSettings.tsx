import React, { useState, useEffect } from 'react';
import { Page, PageConfig } from '../types';

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
  const [formData, setFormData] = useState({
    title: page.title,
    slug: page.slug,
    description: page.description,
    theme: page.config.theme,
    is_published: page.is_published
  });

  const [slugEditing, setSlugEditing] = useState(false);

  useEffect(() => {
    setFormData({
      title: page.title,
      slug: page.slug,
      description: page.description,
      theme: page.config.theme,
      is_published: page.is_published
    });
  }, [page]);

  const handleInputChange = (field: string, value: any) => {
    const newFormData = { ...formData, [field]: value };
    setFormData(newFormData);

    // Auto-generate slug from title if not manually editing
    if (field === 'title' && !slugEditing) {
      const autoSlug = value
        .toLowerCase()
        .replace(/[^\w\s-]/g, '') // Remove special characters
        .replace(/\s+/g, '-') // Replace spaces with hyphens
        .replace(/-+/g, '-') // Replace multiple hyphens with single
        .trim();
      newFormData.slug = autoSlug;
      setFormData(newFormData);
    }

    // Update page object
    const updatedPage: Page = {
      ...page,
      title: newFormData.title,
      slug: newFormData.slug,
      description: newFormData.description,
      is_published: newFormData.is_published,
      config: {
        ...page.config,
        theme: newFormData.theme as any
      }
    };

    onUpdatePage(updatedPage);
  };

  const handleSlugFocus = () => {
    setSlugEditing(true);
  };

  const themes = [
    { 
      value: 'default', 
      name: 'Por Defecto', 
      description: 'Diseño limpio y moderno' 
    },
    { 
      value: 'dark', 
      name: 'Oscuro', 
      description: 'Fondo oscuro con texto claro' 
    },
    { 
      value: 'modern', 
      name: 'Moderno', 
      description: 'Gradientes y efectos visuales' 
    },
    { 
      value: 'minimal', 
      name: 'Minimalista', 
      description: 'Diseño simple y elegante' 
    }
  ];

  const validateSlug = (slug: string): boolean => {
    const slugRegex = /^[a-z0-9-]+$/;
    return slugRegex.test(slug) && slug.length > 0;
  };

  const isSlugValid = validateSlug(formData.slug);

  return (
    <div className="p-4 space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Configuración de Página
        </h3>
        
        {/* Basic Settings */}
        <div className="space-y-4">
          <div>
            <label className="form-label">Título de la Página</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => handleInputChange('title', e.target.value)}
              className="form-input"
              placeholder="Mi Landing Page"
            />
            <p className="text-xs text-gray-500 mt-1">
              Este será el título que aparece en el navegador
            </p>
          </div>

          <div>
            <label className="form-label">URL (Slug)</label>
            <div className="flex items-center">
              <span className="text-sm text-gray-500 mr-2">
                {formData.slug}.localhost
              </span>
            </div>
            <input
              type="text"
              value={formData.slug}
              onChange={(e) => handleInputChange('slug', e.target.value)}
              onFocus={handleSlugFocus}
              className={`form-input mt-1 ${!isSlugValid ? 'border-red-500' : ''}`}
              placeholder="mi-pagina"
            />
            {!isSlugValid && (
              <p className="form-error">
                El slug solo puede contener letras minúsculas, números y guiones
              </p>
            )}
            <p className="text-xs text-gray-500 mt-1">
              URL donde será accesible tu página
            </p>
          </div>

          <div>
            <label className="form-label">Descripción</label>
            <textarea
              value={formData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              className="form-input"
              rows={3}
              placeholder="Describe tu página..."
            />
            <p className="text-xs text-gray-500 mt-1">
              Descripción para SEO y vista previa
            </p>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="is_published"
              checked={formData.is_published}
              onChange={(e) => handleInputChange('is_published', e.target.checked)}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label htmlFor="is_published" className="ml-2 text-sm text-gray-700">
              Página publicada
            </label>
          </div>
          {!formData.is_published && (
            <p className="text-xs text-yellow-600">
              La página debe estar publicada para poder ser desplegada
            </p>
          )}
        </div>
      </div>

      {/* Theme Selection */}
      <div>
        <h4 className="text-md font-medium text-gray-900 mb-3">Tema Visual</h4>
        <div className="space-y-3">
          {themes.map((theme) => (
            <label
              key={theme.value}
              className={`block p-3 border rounded-lg cursor-pointer transition-colors ${
                formData.theme === theme.value
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center">
                <input
                  type="radio"
                  name="theme"
                  value={theme.value}
                  checked={formData.theme === theme.value}
                  onChange={(e) => handleInputChange('theme', e.target.value)}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
                />
                <div className="ml-3">
                  <div className="text-sm font-medium text-gray-900">
                    {theme.name}
                  </div>
                  <div className="text-sm text-gray-600">
                    {theme.description}
                  </div>
                </div>
              </div>
            </label>
          ))}
        </div>
      </div>

      {/* Page Info */}
      <div>
        <h4 className="text-md font-medium text-gray-900 mb-3">Información</h4>
        <div className="bg-gray-50 p-3 rounded-lg space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">ID:</span>
            <span className="font-mono">{page.id}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Creado:</span>
            <span>{new Date(page.created_at).toLocaleDateString('es-ES')}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Actualizado:</span>
            <span>{new Date(page.updated_at).toLocaleDateString('es-ES')}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Estado:</span>
            <span className={formData.is_published ? 'text-green-600' : 'text-yellow-600'}>
              {formData.is_published ? 'Publicado' : 'Borrador'}
            </span>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="space-y-2">
        <button
          onClick={onSavePage}
          disabled={!isSlugValid}
          className="w-full btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Guardar Cambios
        </button>
        
        <div className="text-xs text-gray-500 text-center">
          Los cambios se guardan automáticamente al editar
        </div>
      </div>

      {/* Tips */}
      <div className="bg-blue-50 p-4 rounded-lg">
        <h4 className="font-medium text-blue-900 mb-2">💡 Consejos</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Usa títulos descriptivos para mejor SEO</li>
          <li>• El slug será la URL de tu página</li>
          <li>• Publica la página antes de desplegarla</li>
          <li>• Elige un tema que refleje tu marca</li>
        </ul>
      </div>
    </div>
  );
};

export default PageSettings;