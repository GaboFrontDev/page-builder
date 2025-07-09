import React from 'react';
import { ComponentRenderProps } from '../../types';

const TextSection: React.FC<ComponentRenderProps> = ({ component, theme }) => {
  const { content, styles } = component;
  const text = content?.text || '';
  const alignment = content?.alignment || 'left';

  const isDarkTheme = theme === 'dark' || theme === 'modern';
  const alignmentClasses = {
    left: 'text-left',
    center: 'text-center',
    right: 'text-right'
  };
  const textColor = isDarkTheme ? 'text-white' : 'text-gray-900';

  return (
    <section className={`py-10 px-5 ${alignmentClasses[alignment as keyof typeof alignmentClasses] || alignmentClasses.left}`}>
      <div className={`max-w-4xl mx-auto ${textColor}`}>
        <div dangerouslySetInnerHTML={{ __html: text }} />
      </div>
    </section>
  );
};

export default TextSection;