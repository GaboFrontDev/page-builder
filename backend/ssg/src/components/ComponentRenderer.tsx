import React from 'react';
import { ComponentData } from '../types';
import Hero from './Hero';
import TextSection from './TextSection';
import ImageSection from './ImageSection';
import ButtonSection from './ButtonSection';
import Header from './Header';
import Footer from './Footer';

interface ComponentRendererProps {
  component: ComponentData;
  theme: string;
}

const ComponentRenderer: React.FC<ComponentRendererProps> = ({ component, theme }) => {
  if (!component.is_visible) return null;

  switch (component.type) {
    case 'hero':
      return <Hero component={component} theme={theme} />;
    case 'text':
      return <TextSection component={component} theme={theme} />;
    case 'image':
      return <ImageSection component={component} theme={theme} />;
    case 'button':
      return <ButtonSection component={component} theme={theme} />;
    case 'header':
      return <Header component={component} theme={theme} />;
    case 'footer':
      return <Footer component={component} theme={theme} />;
    default:
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