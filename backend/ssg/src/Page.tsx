import React from 'react';
import { PageData, themes, ComponentRenderer } from '@shared/index';
import './index.css';

interface PageProps {
  pageData: PageData;
}

const Page: React.FC<PageProps> = ({ pageData }) => {
  const theme = pageData.config?.theme || 'default';
  const themeConfig = themes[theme] || themes.default;

  // Sort components by position
  const sortedComponents = [...pageData.components].sort((a, b) => a.position - b.position);

  // Minimal global styles that don't conflict with Tailwind
  const globalStyles = `
    /* Custom styles that complement Tailwind */
  `;

  return (
    <>
      <style dangerouslySetInnerHTML={{ __html: globalStyles }} />
      <div>
        <main>
          {sortedComponents.map((component) => (
            <ComponentRenderer
              key={component.id}
              component={component}
              theme={theme}
            />
          ))}
        </main>
        
        <script dangerouslySetInnerHTML={{
          __html: `console.log('Página generada: ${pageData.slug}');`
        }} />
      </div>
    </>
  );
};

export default Page;