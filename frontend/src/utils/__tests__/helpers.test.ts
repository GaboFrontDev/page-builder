// Tests for utility functions
describe('Utility Functions', () => {
  it('should validate email format', () => {
    const isValidEmail = (email: string): boolean => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    };

    expect(isValidEmail('test@example.com')).toBe(true);
    expect(isValidEmail('invalid-email')).toBe(false);
    expect(isValidEmail('test@')).toBe(false);
    expect(isValidEmail('@example.com')).toBe(false);
  });

  it('should format dates correctly', () => {
    const formatDate = (dateString: string): string => {
      const date = new Date(dateString);
      return date.toLocaleDateString('es-ES');
    };

    expect(formatDate('2023-01-01T00:00:00Z')).toBeTruthy();
  });

  it('should validate password strength', () => {
    const isStrongPassword = (password: string): boolean => {
      return password.length >= 6;
    };

    expect(isStrongPassword('password123')).toBe(true);
    expect(isStrongPassword('12345')).toBe(false);
    expect(isStrongPassword('')).toBe(false);
  });

  it('should generate slug from title', () => {
    const generateSlug = (title: string): string => {
      return title
        .toLowerCase()
        .replace(/[^a-z0-9]/g, '-')
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '');
    };

    expect(generateSlug('My Page Title')).toBe('my-page-title');
    expect(generateSlug('Test & Page')).toBe('test-page');
    expect(generateSlug('   Multiple   Spaces   ')).toBe('multiple-spaces');
  });

  it('should handle API error messages', () => {
    const handleError = (error: any): string => {
      if (error?.response?.data?.detail) {
        return error.response.data.detail;
      }
      if (error?.message) {
        return error.message;
      }
      return 'Ocurrió un error inesperado';
    };

    expect(handleError({ response: { data: { detail: 'Custom error' } } })).toBe('Custom error');
    expect(handleError({ message: 'Network error' })).toBe('Network error');
    expect(handleError({})).toBe('Ocurrió un error inesperado');
    expect(handleError(null)).toBe('Ocurrió un error inesperado');
  });
});