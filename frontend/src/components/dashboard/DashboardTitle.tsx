import React from 'react';
import { Link } from 'react-router-dom';

const DashboardTitle: React.FC = () => {
  return (
    <div className="mb-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">Mis Sitios y Páginas</h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Crea y gestiona tus landing pages agrupadas por subdominio
          </p>
        </div>
        <div className="flex space-x-4">
          <Link
            to="/subscription"
            className="btn btn-outline"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
            </svg>
            Planes
          </Link>
          <Link
            to="/builder"
            className="btn btn-primary"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Nueva Página
          </Link>
        </div>
      </div>
    </div>
  );
};

export default DashboardTitle; 