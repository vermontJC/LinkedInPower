// frontend/src/Posts.js

import React, { useEffect, useState } from 'react';

export default function Posts() {
  const [posts, setPosts] = useState(null);
  const [error, setError] = useState(null);

  const API_URL = process.env.REACT_APP_API_URL || '';

  useEffect(() => {
    // Si no hay API_URL, salimos
    if (!API_URL) {
      setError('No REACT_APP_API_URL definido');
      setPosts([]);
      return;
    }
    fetch(`${API_URL}/api/posts`)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => setPosts(data))
      .catch(err => {
        console.error(err);
        setError(err.message);
        setPosts([]);
      });
  }, [API_URL]);

  if (posts === null) return <p>Cargando…</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;
  if (!posts.length) return <p>No hay posts disponibles.</p>;

  return (
    <div>
      {posts.map(p => (
        <div key={p.id} style={{ marginBottom: '1rem' }}>
          <strong>{p.author}</strong> ({new Date(p.scraped_at).toLocaleString()})
          <p>{p.content}</p>
        </div>
      ))}
    </div>
  );
}
