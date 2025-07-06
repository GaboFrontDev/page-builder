import React from 'react';
import { PageData, themes, ComponentRenderer } from '@shared/index';

interface PageProps {
  pageData: PageData;
}

const Page: React.FC<PageProps> = ({ pageData }) => {
  const theme = pageData.config?.theme || 'default';
  const themeConfig = themes[theme] || themes.default;

  // Sort components by position
  const sortedComponents = [...pageData.components].sort((a, b) => a.position - b.position);

  // Create global styles
  const globalStyles = `
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      transition: all 0.3s ease;
    }
    
    a {
      color: #007bff;
      text-decoration: none;
    }
    
    a:hover {
      text-decoration: underline;
    }
    
    .btn {
      display: inline-block;
      padding: 12px 24px;
      border-radius: 6px;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      border: none;
      transition: all 0.3s ease;
    }
    
    .btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .text-center {
      text-align: center;
    }
    
    .mb-4 {
      margin-bottom: 2rem;
    }
    
    .mt-4 {
      margin-top: 2rem;
    }
    
    @media (max-width: 768px) {
      .container {
        padding: 0 15px !important;
      }
      
      h1 {
        font-size: 2rem !important;
      }
      
      .hero h1 {
        font-size: 2.5rem !important;
      }
    }
  `;

  return (
    <>
      <style dangerouslySetInnerHTML={{ __html: globalStyles }} />
      <div style={themeConfig.styles.body}>
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