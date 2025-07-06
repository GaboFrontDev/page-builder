import React from 'react';
import { ComponentData } from '../types';

interface FooterProps {
  component: ComponentData;
  theme: string;
}

const Footer: React.FC<FooterProps> = ({ component, theme }) => {
  const { content, styles } = component;
  const text = content?.text || '';
  const links = content?.links || [];

  const footerStyles: React.CSSProperties = {
    padding: '40px 20px',
    textAlign: 'center',
    borderTop: '1px solid #eee',
    marginTop: '40px',
    ...styles
  };

  const textColor = theme === 'dark' || theme === 'modern' ? '#ccc' : '#666';

  return (
    <footer style={footerStyles}>
      <p style={{ 
        margin: '0', 
        color: textColor 
      }}>
        {text}
      </p>
      {links.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          {links.map((link: any, index: number) => (
            <a 
              key={index}
              href={link.url || '#'} 
              style={{ 
                marginRight: '20px', 
                textDecoration: 'none', 
                color: textColor 
              }}
            >
              {link.text || ''}
            </a>
          ))}
        </div>
      )}
    </footer>
  );
};

export default Footer;