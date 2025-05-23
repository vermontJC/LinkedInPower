// frontend/src/App.js

import React from 'react';
import Posts from './Posts';

function App() {
  return (
    <div style={{ maxWidth: 800, margin: '2rem auto' }}>
      <h1 style={{ textAlign: 'center' }}>LinkedIn Scraper Dashboard</h1>
      <Posts />
    </div>
  );
}

export default App;
