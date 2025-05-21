import { useEffect, useState } from 'react';

function App() {
  const [msg, setMsg] = useState('Cargando…');

  useEffect(() => {
    fetch('http://localhost:8000/api/hello')
      .then(res => res.json())
      .then(data => setMsg(data.message))
      .catch(() => setMsg('Error al conectar'));
  }, []);

  return (
    <div style={{ textAlign: 'center', marginTop: '2rem' }}>
      <h1>{msg}</h1>
    </div>
  );
}

export default App;
