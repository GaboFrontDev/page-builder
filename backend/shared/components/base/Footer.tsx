import React from 'react';
import { ComponentRenderProps } from '../../types';

const Footer: React.FC<ComponentRenderProps> = ({ component, theme }) => {
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

  const isDarkTheme = theme === 'dark' || theme === 'modern';
  const textColor = isDarkTheme ? '#ccc' : '#666';

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