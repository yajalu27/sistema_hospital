import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePatients } from '../context/PatientContext';
import Layout from '../components/layout/Layout';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { Eye } from 'lucide-react';

const Invoices: React.FC = () => {
  const navigate = useNavigate();
  const { invoices, loadInvoices } = usePatients();

  useEffect(() => {
    loadInvoices();
  }, []);

  return (
    <Layout>
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Facturas</h1>
          <p className="mt-1 text-sm text-gray-500">Lista de todas las facturas generadas.</p>
        </div>
        <Button
          variant="primary"
          size="md"
          onClick={() => navigate('/invoices/new')}
        >
          Generar Nueva Factura
        </Button>
      </div>

      <Card>
        {invoices.length === 0 ? (
          <p className="text-sm text-gray-500 italic">No hay facturas disponibles.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nº Factura</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Paciente</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha Ingreso</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total sin IVA</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total con IVA</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {invoices.map((invoice) => (
                  <tr key={invoice.factura.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{invoice.factura.numero_factura}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{invoice.paciente.nombre_completo}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{new Date(invoice.paciente.fecha_ingreso).toLocaleDateString()}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${invoice.factura.subtotal.toFixed(2)}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${invoice.factura.total_general.toFixed(2)}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{invoice.factura.estado_pago}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => navigate(`/invoices/${invoice.factura.id}`)}
                        icon={<Eye size={16} />}
                      >
                        Ver Factura
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </Layout>
  );
};

export default Invoices;