// frontend/src/App.js

import React from 'react';
import Posts from './Posts';

function App() {
  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '2rem' }}>
      <header style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1>LinkedIn Scraper Dashboard</h1>
      </header>

      <main>
        <Posts />
      </main>
    </div>
  );
}

export default App;
