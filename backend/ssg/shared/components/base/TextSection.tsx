import React from 'react';
import { ComponentRenderProps } from '../../types';

const TextSection: React.FC<ComponentRenderProps> = ({ component, theme }) => {
  const { content, styles } = component;
  const text = content?.text || '';
  const alignment = content?.alignment || 'left';

  const sectionStyles: React.CSSProperties = {
    padding: '40px 20px',
    textAlign: alignment as any,
    ...styles
  };

  const isDarkTheme = theme === 'dark' || theme === 'modern';

  return (
    <section style={sectionStyles}>
      <div style={{ 
        maxWidth: '800px', 
        margin: '0 auto',
        color: isDarkTheme ? '#fff' : '#333'
      }}>
        <div dangerouslySetInnerHTML={{ __html: text }} />
      </div>
    </section>
  );
};

export default TextSection;