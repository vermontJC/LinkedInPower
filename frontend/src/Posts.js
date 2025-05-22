// frontend/src/Posts.js

import React, { useEffect, useState } from 'react';

function Posts() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Define aquí la URL de tu API; en producción pon la URL completa de Cloud Run
  const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

  useEffect(() => {
    fetch(`${API_URL}/api/posts`)
      .then(res => {
        if (!res.ok) throw new Error(`Error ${res.status}`);
        return res.json();
      })
      .then(data => {
        setPosts(data);
      })
      .catch(err => {
        console.error('Fetch error:', err);
      })
      .finally(() => setLoading(false));
  }, [API_URL]);

  if (loading) {
    return <p>Cargando posts…</p>;
  }

  if (!posts.length) {
    return <p>No se encontraron posts .</p>;
  }

  return (
    <div>
      <h2>Últimos posts</h2>
      {posts.map(post => (
        <article 
          key={post.id} 
          style={{ 
            borderBottom: '1px solid #ccc', 
            padding: '1rem 0' 
          }}
        >
          <header style={{ marginBottom: '.5rem' }}>
            <strong>{post.author}</strong>{' '}
            <em style={{ color: '#666' }}>
              {new Date(post.scraped_at).toLocaleString()}
            </em>
          </header>
          <p>{post.content}</p>
          <footer style={{ fontSize: '.9rem', color: '#444' }}>
            👍 {post.reactions}  |  💬 {post.comments}
          </footer>
        </article>
      ))}
    </div>
  );
}

export default Posts;
