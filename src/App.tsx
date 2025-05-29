import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Discharges from './pages/Discharges';
import NewDischarge from './pages/NewDischarge';
import Invoices from './pages/Invoices';
import NewInvoice from './pages/NewInvoice';
import InvoiceDetail from './pages/InvoiceDetail';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/discharges" element={<Discharges />} />
      <Route path="/new-discharge" element={<NewDischarge />} />
      <Route path="/invoices" element={<Invoices />} />
      <Route path="/invoices/:invoiceId" element={<InvoiceDetail />} />
      <Route path="/invoices/new" element={<NewInvoice />} />
    </Routes>
  );
}

export default App;