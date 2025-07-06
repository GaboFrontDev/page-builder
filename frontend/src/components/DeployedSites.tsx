import React, { useState, useEffect } from 'react';
import { deploymentApi, handleApiError } from '../services/api';
import { DeployedSite } from '../types';

const DeployedSites: React.FC = () => {
  const [sites, setSites] = useState<DeployedSite[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingSites, setDeletingSites] = useState<Set<string>>(new Set());

  useEffect(() => {
    loadDeployedSites();
  }, []);

  const loadDeployedSites = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await deploymentApi.listDeployedSites();
      setSites(response.deployed_sites);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteSite = async (slug: string) => {
    if (!window.confirm(`¿Estás seguro de que quieres eliminar el sitio "${slug}"?`)) {
      return;
    }

    try {
      setDeletingSites(prev => new Set(prev).add(slug));
      await deploymentApi.undeployPageBySlug(slug);
      
      // Actualizar la lista
      setSites(prev => prev.filter(site => site.slug !== slug));
      
      // Mostrar mensaje de éxito
      alert(`Sitio "${slug}" eliminado correctamente`);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setDeletingSites(prev => {
        const newSet = new Set(prev);
        newSet.delete(slug);
        return newSet;
      });
    }
  };

  const handleRebuildAll = async () => {
    if (!window.confirm('¿Estás seguro de que quieres reconstruir todos los sitios?')) {
      return;
    }

    try {
      setLoading(true);
      await deploymentApi.rebuildAllSites();
      await loadDeployedSites();
      alert('Todos los sitios han sido reconstruidos');
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const mySites = sites.filter(site => site.is_owner);
  const otherSites = sites.filter(site => !site.is_owner);

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-20 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Mis Sitios Desplegados</h2>
        <button
          onClick={handleRebuildAll}
          disabled={loading}
          className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition-colors"
        >
          {loading ? 'Reconstruyendo...' : 'Reconstruir Todos'}
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {mySites.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-500">No tienes sitios desplegados</p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {mySites.map(site => (
            <SiteCard
              key={site.slug}
              site={site}
              onDelete={handleDeleteSite}
              isDeleting={deletingSites.has(site.slug)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

interface SiteCardProps {
  site: DeployedSite;
  onDelete: (slug: string) => void;
  isDeleting: boolean;
}

const SiteCard: React.FC<SiteCardProps> = ({ site, onDelete, isDeleting }) => {
  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 p-4">
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h4 className="font-semibold text-gray-900 truncate">
            {site.title || site.slug}
          </h4>
          <p className="text-sm text-gray-500">{site.slug}</p>
        </div>
        <button
          onClick={() => onDelete(site.slug)}
          disabled={isDeleting}
          className="ml-2 text-red-600 hover:text-red-800 disabled:text-gray-400 transition-colors"
          title="Eliminar sitio"
        >
          {isDeleting ? (
            <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          )}
        </button>
      </div>

      <div className="space-y-2">
        <a
          href={site.url}
          target="_blank"
          rel="noopener noreferrer"
          className="block text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          {site.url}
        </a>
        
        {site.page_id && (
          <p className="text-xs text-gray-400">
            ID: {site.page_id}
          </p>
        )}
      </div>
    </div>
  );
};

export default DeployedSites; 