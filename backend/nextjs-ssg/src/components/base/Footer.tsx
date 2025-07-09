import React from 'react';
import { ComponentRenderProps } from '@/types';

const Footer: React.FC<ComponentRenderProps> = ({ component, theme }) => {
  const { content } = component;
  const text = (content?.text as string) || '';
  const links = (content?.links as Record<string, unknown>[]) || [];

  const isDarkTheme = theme === 'dark' || theme === 'modern';
  const textColor = isDarkTheme ? 'text-gray-300' : 'text-gray-600';
  const borderColor = isDarkTheme ? 'border-gray-700' : 'border-gray-200';

  return (
    <footer className={`p-10 text-center border-t mt-10 ${borderColor}`}>
      <p className={`m-0 ${textColor}`}>
        {text}
      </p>
      {links.length > 0 && (
        <div className="mt-5 space-x-5">
          {links.map((link: Record<string, unknown>, index: number) => (
            <a 
              key={index}
              href={(link.url as string) || '#'} 
              className={`no-underline hover:underline ${textColor}`}
            >
              {(link.text as string) || ''}
            </a>
          ))}
        </div>
      )}
    </footer>
  );
};

export default Footer;