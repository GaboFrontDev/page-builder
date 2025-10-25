import React from 'react';
import { ComponentData } from '../types';
import Hero from './base/Hero';
import Header from './base/Header';
import TextSection from './base/TextSection';
import ImageSection from './base/ImageSection';
import ButtonSection from './base/ButtonSection';
import Footer from './base/Footer';

interface ComponentRendererProps {
  component: ComponentData;
  theme: string;
  isPreview?: boolean;
}

const ComponentRenderer: React.FC<ComponentRendererProps> = ({
  component,
  theme,
  isPreview = false
}) => {
  if (!component.is_visible) return null;

  const componentProps = { component, theme, isPreview };

  switch (component.type) {
    case 'hero':
      return <Hero {...componentProps} />;
    case 'header':
      return <Header {...componentProps} />;
    case 'text':
      return <TextSection {...componentProps} />;
    case 'image':
      return <ImageSection {...componentProps} />;
    case 'button':
      return <ButtonSection {...componentProps} />;
    case 'footer':
      return <Footer {...componentProps} />;
    default:
      if (isPreview) {
        return (
          <div className="p-5 border-2 border-dashed border-gray-300 m-2 text-gray-600">
            Componente no implementado: {component.type}
          </div>
        );
      }
      return (
        <div style={{
          padding: '20px',
          border: '1px dashed #ccc',
          margin: '10px 0',
          color: theme === 'dark' || theme === 'modern' ? '#fff' : '#333'
        }}>
          Componente no implementado: {component.type}
        </div>
      );
  }
};

export default ComponentRenderer;