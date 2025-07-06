import React from 'react';
import { ComponentData } from '../types';

interface ButtonSectionProps {
  component: ComponentData;
  theme: string;
}

const ButtonSection: React.FC<ButtonSectionProps> = ({ component, theme }) => {
  const { content, styles } = component;
  const text = content?.text || 'Click me';
  const link = content?.link || '#';
  const variant = content?.variant || 'primary';

  const buttonVariants = {
    primary: { background: '#007bff', color: 'white' },
    secondary: { background: '#6c757d', color: 'white' },
    outline: { background: 'transparent', color: '#007bff', border: '2px solid #007bff' }
  };

  const sectionStyles: React.CSSProperties = {
    padding: '20px',
    textAlign: 'center',
    ...styles
  };

  const buttonStyles: React.CSSProperties = {
    ...buttonVariants[variant as keyof typeof buttonVariants],
    padding: '15px 30px',
    textDecoration: 'none',
    borderRadius: '5px',
    fontWeight: 'bold',
    display: 'inline-block',
    transition: 'all 0.3s ease'
  };

  if (theme === 'modern') {
    buttonStyles.background = 'rgba(255,255,255,0.2)';
    buttonStyles.color = 'white';
    buttonStyles.border = '1px solid rgba(255,255,255,0.3)';
  }

  return (
    <section style={sectionStyles}>
      <a href={link} style={buttonStyles}>
        {text}
      </a>
    </section>
  );
};

export default ButtonSection;