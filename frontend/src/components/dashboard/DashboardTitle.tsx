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
  );
};

export default DashboardTitle; 