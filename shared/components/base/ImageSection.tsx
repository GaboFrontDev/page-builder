import React from 'react';
import { ComponentRenderProps } from '../../types';

const ImageSection: React.FC<ComponentRenderProps> = ({ component, theme }) => {
  const { content, styles } = component;
  const src = content?.src || '';
  const alt = content?.alt || '';
  const caption = content?.caption || '';

  const isDarkTheme = theme === 'dark' || theme === 'modern';
  const captionColor = isDarkTheme ? 'text-gray-300' : 'text-gray-600';

  return (
    <section className="py-10 px-5 text-center">
      <img
        src={src}
        alt={alt}
        className="max-w-full h-auto rounded-lg mx-auto"
      />
      {caption && (
        <p className={`mt-4 italic ${captionColor}`}>
          {caption}
        </p>
      )}
    </section>
  );
};

export default ImageSection;