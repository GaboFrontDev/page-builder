import React from 'react';
import { ComponentData } from '../types';

interface ImageSectionProps {
  component: ComponentData;
  theme: string;
}

const ImageSection: React.FC<ImageSectionProps> = ({ component, theme }) => {
  const { content, styles } = component;
  const src = content?.src || '';
  const alt = content?.alt || '';
  const caption = content?.caption || '';

  const sectionStyles: React.CSSProperties = {
    padding: '40px 20px',
    textAlign: 'center',
    ...styles
  };

  return (
    <section style={sectionStyles}>
      <img 
        src={src} 
        alt={alt} 
        style={{ 
          maxWidth: '100%', 
          height: 'auto', 
          borderRadius: '8px' 
        }} 
      />
      {caption && (
        <p style={{ 
          marginTop: '15px', 
          fontStyle: 'italic', 
          color: theme === 'dark' || theme === 'modern' ? '#ccc' : '#666' 
        }}>
          {caption}
        </p>
      )}
    </section>
  );
};

export default ImageSection;