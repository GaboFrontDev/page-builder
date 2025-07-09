import React from 'react';
import { ComponentRenderProps } from '@/types';

const Header: React.FC<ComponentRenderProps> = ({ component, theme }) => {
  const { content } = component;
  const title = (content?.title as string) || '';
  const logo = (content?.logo as string) || '';
  const menu_items = (content?.menu_items as Record<string, unknown>[]) || [];

  const isDarkTheme = theme === 'dark' || theme === 'modern';
  const themeClasses = isDarkTheme ? 'text-white border-gray-700' : 'text-gray-900 border-gray-200';

  return (
    <header className={`p-5 border-b flex justify-between items-center ${themeClasses}`}>
      <div className="flex items-center">
        {logo && (
          <img 
            src={logo} 
            alt="Logo" 
            className="h-10 mr-4" 
          />
        )}
        <h1 className="text-2xl font-bold m-0">
          {title}
        </h1>
      </div>
      {menu_items.length > 0 && (
        <nav className="flex space-x-6">
          {menu_items.map((item: Record<string, unknown>, index: number) => (
            <a 
              key={index}
              href={(item.link as string) || '#'} 
              className="text-current no-underline hover:underline"
            >
              {(item.text as string) || ''}
            </a>
          ))}
        </nav>
      )}
    </header>
  );
};

export default Header;