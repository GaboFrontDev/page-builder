import React from 'react';
import { Link } from 'react-router-dom';
import { Page } from '../../types';
import PageCard from './PageCard';

interface SubdomainSectionProps {
  subdomain: string;
  pages: Page[];
  onDelete: (pageId: number) => void;
  onDeploy: (pageId: number) => void;
}

const SubdomainSection: React.FC<SubdomainSectionProps> = ({ 
  subdomain, 
  pages, 
  onDelete, 
  onDeploy 
}) => {
  return (
    <div className="dashboard-card">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
            <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
            </svg>
          </div>
          <div>
            <a
              href={`http://${subdomain}.localhost`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-2xl font-bold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-200 flex items-center gap-2 group"
            >
              {subdomain}.localhost
              <svg className="w-5 h-5 opacity-0 group-hover:opacity-100 transition-opacity duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
            <p className="text-gray-600 dark:text-gray-300">{pages.length} página(s)</p>
          </div>
        </div>
        <Link
          to={`/builder?subdomain=${subdomain}`}
          className="btn btn-outline"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Nueva Página
        </Link>
      </div>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {pages.map((page) => (
          <PageCard
            key={page.id}
            page={page}
            onDelete={onDelete}
            onDeploy={onDeploy}
          />
        ))}
      </div>
    </div>
  );
};

export default SubdomainSection; 