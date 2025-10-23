import React from 'react';
import { Page } from '../../types';

interface StatsCardsProps {
  pages: Page[];
  pagesBySubdomain: { [subdomain: string]: Page[] };
}

const StatsCards: React.FC<StatsCardsProps> = ({ pages, pagesBySubdomain }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-6 sm:mb-8">
      <div className="stats-card">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-blue-100 text-xs sm:text-sm font-medium">Total de Páginas</p>
            <p className="text-2xl sm:text-3xl font-bold">{pages.length}</p>
          </div>
          <svg className="w-6 h-6 sm:w-8 sm:h-8 text-blue-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
      </div>
      
      <div className="stats-card bg-gradient-to-br from-emerald-500 to-green-600">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-emerald-100 text-xs sm:text-sm font-medium">Páginas Publicadas</p>
            <p className="text-2xl sm:text-3xl font-bold">{pages.filter(p => p.is_published).length}</p>
          </div>
          <svg className="w-6 h-6 sm:w-8 sm:h-8 text-emerald-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
      </div>
      
      <div className="stats-card bg-gradient-to-br from-purple-500 to-pink-600 sm:col-span-2 lg:col-span-1">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-purple-100 text-xs sm:text-sm font-medium">Subdominios</p>
            <p className="text-2xl sm:text-3xl font-bold">{Object.keys(pagesBySubdomain).length}</p>
          </div>
          <svg className="w-6 h-6 sm:w-8 sm:h-8 text-purple-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
      </div>
    </div>
  );
};

export default StatsCards; 