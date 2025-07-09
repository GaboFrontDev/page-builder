import React from 'react';
import { ComponentRenderProps, ThemeName } from '../../types';

interface HeroProps extends ComponentRenderProps {
  isPreview?: boolean;
}

const Hero: React.FC<HeroProps> = ({ component, theme, isPreview = false }) => {
  const { content, styles } = component;
  const title = content?.title || '';
  const subtitle = content?.subtitle || '';
  const image = content?.image || '';
  const cta_text = content?.cta_text || '';
  const cta_link = content?.cta_link || '#';

  // Use Tailwind classes for both preview and SSG
  const themeClasses = {
    modern: 'bg-gradient-to-br from-blue-500 to-purple-600 text-white',
    dark: 'bg-gray-900 text-white',
    minimal: 'bg-gray-50 text-gray-900',
    default: 'bg-white text-gray-900'
  };

  return (
    <section className={`text-center py-20 px-5 ${themeClasses[theme as keyof typeof themeClasses] || themeClasses.default}`}>
      {image && (
        <img 
          src={image} 
          alt="Hero" 
          className="max-w-full h-auto mb-8 mx-auto"
        />
      )}
      <h1 className="text-4xl md:text-5xl font-bold mb-5">
        {title}
      </h1>
      <p className="text-lg md:text-xl mb-8 opacity-90">
        {subtitle}
      </p>
      {cta_text && (
        <a 
          href={cta_link} 
          className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-8 rounded transition-colors duration-300"
        >
          {cta_text}
        </a>
      )}
    </section>
  );
};

export default Hero;