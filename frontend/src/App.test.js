import { render, screen } from '@testing-library/react';
import App from './App';

test('muestra mensaje de carga inicial', () => {
  render(<App />);
  expect(screen.getByText(/Cargando…/i)).toBeInTheDocument();
});
