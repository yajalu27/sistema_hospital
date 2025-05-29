import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

// Enable future flags for React Router
const routerConfig = {
  future: {
    v7_startTransition: true,
  },
};

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter {...routerConfig}>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);