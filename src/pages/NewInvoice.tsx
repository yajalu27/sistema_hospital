import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { Save, ArrowLeft } from 'lucide-react';
import { discharges, patients, invoices } from '../data/mockData';
import { Discharge } from '../types';

const NewInvoice: React.FC = () => {
  const { dischargeId } = useParams<{ dischargeId: string }>();
  const navigate = useNavigate();
  const [discharge, setDischarge] = useState<Discharge | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const foundDischarge = discharges.find(d => d.id === dischargeId);
    setDischarge(foundDischarge || null);
    setLoading(false);
  }, [dischargeId]);

  const getPatientName = (patientId: string) => {
    const patient = patients.find(p => p.id === patientId);
    return patient ? patient.name : 'Paciente desconocido';
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR'
    }).format(amount);
  };

  const calculateTotals = () => {
    if (!discharge) return { subtotal: 0, tax: 0, total: 0 };

    const productsTotal = discharge.products.reduce((sum, product) => 
      sum + (product.price * product.quantity), 0);
    
    const servicesTotal = discharge.services.reduce((sum, service) => 
      sum + service.price, 0);

    const subtotal = productsTotal + servicesTotal;
    const tax = subtotal * 0.16; // 16% tax rate
    const total = subtotal + tax;

    return { subtotal, tax, total };
  };

  const handleCreateInvoice = () => {
    if (!discharge) return;

    const { subtotal, tax, total } = calculateTotals();

    const newInvoice = {
      id: `${invoices.length + 1}`,
      dischargeId: discharge.id,
      patientId: discharge.patientId,
      date: new Date().toISOString().split('T')[0],
      items: [
        ...discharge.products.map(product => ({
          description: `${product.productName} (${product.quantity} ${product.unit})`,
          quantity: product.quantity,
          unitPrice: product.price,
          total: product.price * product.quantity
        })),
        ...discharge.services.map(service => ({
          description: service.serviceName,
          quantity: 1,
          unitPrice: service.price,
          total: service.price
        }))
      ],
      subtotal,
      tax,
      total,
      status: 'pending' as const
    };

    // In a real application, this would be handled by the backend
    // For now, we'll just show a success message and navigate back
    alert('Factura generada exitosamente');
    navigate('/invoices');
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </Layout>
    );
  }

  if (!discharge) {
    return (
      <Layout>
        <div className="text-center">
          <h2 className="text-lg font-medium text-gray-900">Descargo no encontrado</h2>
          <p className="mt-1 text-sm text-gray-500">El descargo solicitado no existe o ha sido eliminado.</p>
          <Button
            variant="outline"
            className="mt-4"
            onClick={() => navigate('/invoices')}
            icon={<ArrowLeft size={18} />}
          >
            Volver a Facturas
          </Button>
        </div>
      </Layout>
    );
  }

  const { subtotal, tax, total } = calculateTotals();

  return (
    <Layout>
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">Generar Nueva Factura</h1>
          <Button
            variant="outline"
            onClick={() => navigate('/invoices')}
            icon={<ArrowLeft size={18} />}
          >
            Volver
          </Button>
        </div>
        <p className="mt-1 text-sm text-gray-500">
          Genere una nueva factura para el descargo seleccionado.
        </p>
      </div>

      <Card>
        <div className="mb-6">
          <h2 className="text-lg font-medium text-gray-900">Detalles del Paciente</h2>
          <p className="mt-2 text-sm text-gray-600">
            <strong>Paciente:</strong> {getPatientName(discharge.patientId)}
          </p>
          <p className="mt-1 text-sm text-gray-600">
            <strong>Fecha del descargo:</strong> {discharge.date}
          </p>
        </div>

        <div className="mb-6">
          <h3 className="text-md font-medium text-gray-900 mb-4">Productos y Servicios</h3>
          <div className="bg-gray-50 rounded-lg p-4">
            <table className="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descripción</th>
                  <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Cantidad</th>
                  <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Precio Unit.</th>
                  <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {discharge.products.map((product, index) => (
                  <tr key={`product-${index}`}>
                    <td className="px-4 py-2 text-sm text-gray-900">{product.productName}</td>
                    <td className="px-4 py-2 text-sm text-gray-900 text-right">{product.quantity} {product.unit}</td>
                    <td className="px-4 py-2 text-sm text-gray-900 text-right">{formatCurrency(product.price)}</td>
                    <td className="px-4 py-2 text-sm text-gray-900 text-right">{formatCurrency(product.price * product.quantity)}</td>
                  </tr>
                ))}
                {discharge.services.map((service, index) => (
                  <tr key={`service-${index}`}>
                    <td className="px-4 py-2 text-sm text-gray-900">{service.serviceName}</td>
                    <td className="px-4 py-2 text-sm text-gray-900 text-right">1</td>
                    <td className="px-4 py-2 text-sm text-gray-900 text-right">{formatCurrency(service.price)}</td>
                    <td className="px-4 py-2 text-sm text-gray-900 text-right">{formatCurrency(service.price)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="border-t border-gray-200 pt-4">
          <div className="flex justify-end">
            <div className="w-64">
              <div className="flex justify-between py-2">
                <span className="text-sm font-medium text-gray-500">Subtotal:</span>
                <span className="text-sm text-gray-900">{formatCurrency(subtotal)}</span>
              </div>
              <div className="flex justify-between py-2">
                <span className="text-sm font-medium text-gray-500">IVA (16%):</span>
                <span className="text-sm text-gray-900">{formatCurrency(tax)}</span>
              </div>
              <div className="flex justify-between py-2 border-t border-gray-200">
                <span className="text-base font-medium text-gray-900">Total:</span>
                <span className="text-base font-medium text-gray-900">{formatCurrency(total)}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 flex justify-end">
          <Button
            variant="primary"
            size="lg"
            onClick={handleCreateInvoice}
            icon={<Save size={18} />}
          >
            Generar Factura
          </Button>
        </div>
      </Card>
    </Layout>
  );
};

export default NewInvoice;