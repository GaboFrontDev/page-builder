'use client';

import { PageData } from '@/types';
import Header from './base/Header';
import Hero from './base/Hero';
import TextSection from './base/TextSection';
import ImageSection from './base/ImageSection';
import Footer from './base/Footer';
import ButtonSection from './base/ButtonSection';

interface ComponentRendererProps {
  pageData: PageData;
}

const componentMap = {
  'header': Header,
  'hero': Hero,
  'text': TextSection,
  'image': ImageSection,
  'footer': Footer,
  'button': ButtonSection,
};

export default function ComponentRenderer({ pageData }: ComponentRendererProps) {
  const theme = pageData.config?.theme || 'default';
  
  return (
    <div className="min-h-screen">
      {pageData.components
        .filter(component => component.is_visible)
        .sort((a, b) => a.position - b.position)
        .map((component) => {
          const ComponentToRender = componentMap[component.type as keyof typeof componentMap];
          
          if (!ComponentToRender) {
            console.warn(`Component type "${component.type}" not found`);
            return null;
          }
          
          return (
            <ComponentToRender
              key={component.id}
              component={component}
              theme={theme}
            />
          );
        })}
    </div>
  );
}