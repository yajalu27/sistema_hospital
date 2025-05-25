import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Discharges from './pages/Discharges';
import NewDischarge from './pages/NewDischarge';
import Invoices from './pages/Invoices';
import NewInvoice from './pages/NewInvoice';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/discharges" element={<Discharges />} />
      <Route path="/new-discharge" element={<NewDischarge />} />
      <Route path="/invoices" element={<Invoices />} />
      <Route path="/new-invoice/:dischargeId" element={<NewInvoice />} />
    </Routes>
  );
}

export default App;