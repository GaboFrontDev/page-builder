import React from 'react';
import { Link } from 'react-router-dom';
import { Page } from '../../types';

interface PageCardProps {
  page: Page;
  onDelete: (pageId: number) => void;
  onDeploy: (pageId: number) => void;
}

const PageCard: React.FC<PageCardProps> = ({ page, onDelete, onDeploy }) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="card card-hover">
      <div className="card-body">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white truncate">
            {page.title}
          </h3>
          <div className="flex items-center space-x-2">
            {page.is_published ? (
              <span className="badge badge-success">
                <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Publicado
              </span>
            ) : (
              <span className="badge badge-warning">
                <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Borrador
              </span>
            )}
          </div>
        </div>
        <p className="text-gray-600 dark:text-gray-300 mb-4 line-clamp-2">
          {page.description}
        </p>
        <div className="flex items-center space-x-2 mb-4">
          <span className="text-xs font-mono bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
            {page.slug ? `/${page.slug}` : '/'}
          </span>
          <span className="text-xs text-gray-500 dark:text-gray-400">
            Tema: {page.config.theme}
          </span>
        </div>
        <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mb-4">
          <span>{formatDate(page.updated_at)}</span>
        </div>
        <div className="flex space-x-2">
          <Link
            to={`/builder/${page.id}`}
            className="btn btn-primary flex-1"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Editar
          </Link>
          {page.is_published && (
            <button
              onClick={() => onDeploy(page.id)}
              className="btn btn-success"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              Desplegar
            </button>
          )}
          <button
            onClick={() => onDelete(page.id)}
            className="btn btn-danger"
            title="Eliminar página"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default PageCard; 