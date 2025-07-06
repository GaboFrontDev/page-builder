import React from 'react';
import { ComponentData } from '../types';

interface TextSectionProps {
  component: ComponentData;
  theme: string;
}

const TextSection: React.FC<TextSectionProps> = ({ component, theme }) => {
  const { content, styles } = component;
  const text = content?.text || '';
  const alignment = content?.alignment || 'left';

  const sectionStyles: React.CSSProperties = {
    padding: '40px 20px',
    textAlign: alignment as any,
    ...styles
  };

  return (
    <section style={sectionStyles}>
      <div style={{ 
        maxWidth: '800px', 
        margin: '0 auto',
        color: theme === 'dark' || theme === 'modern' ? '#fff' : '#333'
      }}>
        <div dangerouslySetInnerHTML={{ __html: text }} />
      </div>
    </section>
  );
};

export default TextSection;