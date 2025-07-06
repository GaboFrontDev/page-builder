import { ComponentType, ComponentContent, ComponentStyles } from '../types';

export const getDefaultContent = (type: ComponentType): ComponentContent => {
  switch (type) {
    case 'hero':
      return {
        title: 'Título principal',
        subtitle: 'Subtítulo descriptivo',
        cta_text: 'Botón de acción',
        cta_link: '#'
      };
    case 'header':
      return {
        title: 'Mi Sitio Web',
        menu_items: [
          { text: 'Inicio', link: '#' },
          { text: 'Servicios', link: '#servicios' },
          { text: 'Contacto', link: '#contacto' }
        ]
      };
    case 'text':
      return {
        text: '<p>Contenido de texto. Puedes usar <strong>HTML</strong> aquí.</p>',
        alignment: 'left'
      };
    case 'image':
      return {
        src: 'https://via.placeholder.com/600x300',
        alt: 'Imagen de ejemplo',
        caption: 'Descripción de la imagen'
      };
    case 'button':
      return {
        text: 'Hacer clic aquí',
        link: '#',
        variant: 'primary'
      };
    case 'footer':
      return {
        text: '© 2024 Mi Sitio Web. Todos los derechos reservados.',
        links: [
          { text: 'Política de Privacidad', url: '#' },
          { text: 'Términos de Uso', url: '#' }
        ]
      };
    default:
      return {};
  }
};

export const getDefaultStyles = (type: ComponentType): ComponentStyles => {
  switch (type) {
    case 'hero':
      return {
        padding: '80px 20px',
        textAlign: 'center'
      };
    case 'header':
      return {
        padding: '20px',
        borderBottom: '1px solid #eee'
      };
    case 'text':
      return {
        padding: '40px 20px'
      };
    case 'image':
      return {
        padding: '40px 20px',
        textAlign: 'center'
      };
    case 'button':
      return {
        padding: '20px',
        textAlign: 'center'
      };
    case 'footer':
      return {
        padding: '40px 20px',
        textAlign: 'center',
        borderTop: '1px solid #eee',
        marginTop: '40px'
      };
    default:
      return {};
  }
};

export const componentTypes: ComponentType[] = [
  'header',
  'hero', 
  'text',
  'image',
  'button',
  'footer'
];

export const componentLabels: Record<ComponentType, string> = {
  hero: 'Hero',
  header: 'Encabezado',
  text: 'Texto',
  image: 'Imagen',
  button: 'Botón',
  footer: 'Pie de página'
};