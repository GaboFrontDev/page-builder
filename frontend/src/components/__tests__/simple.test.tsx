import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

// Simple component for testing
const TestComponent: React.FC<{ title: string }> = ({ title }) => {
  return <h1>{title}</h1>;
};

describe('Simple Component Tests', () => {
  it('renders a simple component', () => {
    render(<TestComponent title="Hello World" />);
    expect(screen.getByText('Hello World')).toBeInTheDocument();
  });

  it('renders with different props', () => {
    render(<TestComponent title="Test Title" />);
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Test Title');
  });
});