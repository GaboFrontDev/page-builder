import React from 'react';
import { ComponentData } from '../types';

interface HeroProps {
  component: ComponentData;
  theme: string;
}

const Hero: React.FC<HeroProps> = ({ component, theme }) => {
  const { content, styles } = component;
  const title = content?.title || '';
  const subtitle = content?.subtitle || '';
  const image = content?.image || '';
  const cta_text = content?.cta_text || '';
  const cta_link = content?.cta_link || '#';

  const heroStyles: React.CSSProperties = {
    textAlign: 'center',
    padding: '80px 20px',
    ...styles
  };

  if (theme === 'modern') {
    heroStyles.background = 'rgba(255,255,255,0.1)';
    heroStyles.backdropFilter = 'blur(10px)';
    heroStyles.borderRadius = '20px';
    heroStyles.margin = '20px';
  }

  const buttonStyles: React.CSSProperties = {
    background: theme === 'modern' ? 'rgba(255,255,255,0.2)' : '#007bff',
    color: 'white',
    padding: '15px 30px',
    textDecoration: 'none',
    borderRadius: '5px',
    fontWeight: 'bold',
    display: 'inline-block',
    border: theme === 'modern' ? '1px solid rgba(255,255,255,0.3)' : 'none',
    transition: 'all 0.3s ease'
  };

  return (
    <section style={heroStyles}>
      {image && (
        <img 
          src={image} 
          alt="Hero" 
          style={{ 
            maxWidth: '100%', 
            height: 'auto', 
            marginBottom: '30px' 
          }} 
        />
      )}
      <h1 style={{ 
        fontSize: '3rem', 
        marginBottom: '20px', 
        color: theme === 'dark' || theme === 'modern' ? '#fff' : '#333' 
      }}>
        {title}
      </h1>
      <p style={{ 
        fontSize: '1.2rem', 
        marginBottom: '30px', 
        color: theme === 'dark' || theme === 'modern' ? '#ccc' : '#666' 
      }}>
        {subtitle}
      </p>
      {cta_text && (
        <a href={cta_link} style={buttonStyles}>
          {cta_text}
        </a>
      )}
    </section>
  );
};

export default Hero;