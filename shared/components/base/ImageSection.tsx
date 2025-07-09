import React from 'react';
import { ComponentRenderProps } from '@shared/index';

const ImageSection: React.FC<ComponentRenderProps> = ({ component, theme }) => {
  const { content, styles } = component;
  const src = content?.src || '';
  const alt = content?.alt || '';
  const caption = content?.caption || '';

  const sectionStyles: React.CSSProperties = {
    padding: '40px 20px',
    textAlign: 'center',
    ...styles
  };

  const isDarkTheme = theme === 'dark' || theme === 'modern';

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
          color: isDarkTheme ? '#ccc' : '#666' 
        }}>
          {caption}
        </p>
      )}
    </section>
  );
};

export default ImageSection;