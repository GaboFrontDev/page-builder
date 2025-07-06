import React from 'react';
import { ComponentRenderProps } from '../../types';

const Header: React.FC<ComponentRenderProps> = ({ component, theme }) => {
  const { content, styles } = component;
  const title = content?.title || '';
  const logo = content?.logo || '';
  const menu_items = content?.menu_items || [];

  const headerStyles: React.CSSProperties = {
    padding: '20px',
    borderBottom: '1px solid #eee',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    ...styles
  };

  const isDarkTheme = theme === 'dark' || theme === 'modern';
  const linkColor = isDarkTheme ? '#fff' : '#333';

  return (
    <header style={headerStyles}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        {logo && (
          <img 
            src={logo} 
            alt="Logo" 
            style={{ 
              height: '40px', 
              marginRight: '15px' 
            }} 
          />
        )}
        <h1 style={{ 
          margin: '0', 
          fontSize: '1.5rem',
          color: linkColor
        }}>
          {title}
        </h1>
      </div>
      {menu_items.length > 0 && (
        <nav style={{ display: 'inline-block' }}>
          {menu_items.map((item: any, index: number) => (
            <a 
              key={index}
              href={item.link || '#'} 
              style={{ 
                marginLeft: '20px', 
                textDecoration: 'none', 
                color: linkColor 
              }}
            >
              {item.text || ''}
            </a>
          ))}
        </nav>
      )}
    </header>
  );
};

export default Header;