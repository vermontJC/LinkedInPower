import { useEffect, useState } from 'react';

function App() {
  const [msg, setMsg] = useState('Cargando…');
  // Toma la URL de la API de la variable de entorno o el localhost en desarrollo
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetch(`${apiUrl}/api/hello`)
      .then(res => res.json())
      .then(data => setMsg(data.message))
      .catch(() => setMsg('Error al conectar'));
  }, [apiUrl]);

  return (
    <div style={{ textAlign: 'center', marginTop: '2rem' }}>
      <h1>{msg}</h1>
    </div>
  );
}

export default App;
