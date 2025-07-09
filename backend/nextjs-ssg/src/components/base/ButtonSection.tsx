import React from 'react';
import { ComponentRenderProps } from '@/types';

const ButtonSection: React.FC<ComponentRenderProps> = ({ component, theme }) => {
  const { content } = component;
  const text = (content?.text as string) || 'Click me';
  const link = (content?.link as string) || '#';
  const variant = (content?.variant as string) || 'primary';

  const buttonVariants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-600 hover:bg-gray-700 text-white',
    outline: 'bg-transparent text-blue-600 border-2 border-blue-600 hover:bg-blue-600 hover:text-white'
  };

  const modernStyles = theme === 'modern' ? 'bg-white bg-opacity-20 text-white border border-white border-opacity-30 hover:bg-opacity-30' : '';
  const finalStyles = theme === 'modern' ? modernStyles : buttonVariants[variant as keyof typeof buttonVariants];

  return (
    <section className="py-5 text-center">
      <a 
        href={link} 
        className={`inline-block px-8 py-4 font-bold rounded transition-all duration-300 no-underline ${finalStyles}`}
      >
        {text}
      </a>
    </section>
  );
};

export default ButtonSection;