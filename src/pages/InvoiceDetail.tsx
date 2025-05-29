import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { usePatients } from '../context/PatientContext';
import Layout from '../components/layout/Layout';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { Download } from 'lucide-react';

const InvoiceDetail: React.FC = () => {
  const { invoiceId } = useParams<{ invoiceId: string }>();
  const navigate = useNavigate();
  const { fetchInvoice, downloadInvoicePDF } = usePatients();
  const [invoice, setInvoice] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadInvoice = async () => {
      try {
        const data = await fetchInvoice(Number(invoiceId));
        setInvoice(data);
        setLoading(false);
      } catch (error) {
        console.error('Error loading invoice:', error);
        alert('Error al cargar la factura.');
        navigate('/invoices');
      }
    };
    loadInvoice();
  }, [invoiceId, fetchInvoice, navigate]);

  const handleDownloadPDF = async () => {
    try {
      const pdfBlob = await downloadInvoicePDF(Number(invoiceId));
      const url = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `factura_${invoice.factura.numero_factura}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading PDF:', error);
      alert('Error al descargar el PDF.');
    }
  };

  if (loading) {
    return <div className="text-center py-10">Cargando...</div>;
  }

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Detalles de la Factura #{invoice.factura.numero_factura}</h1>
        <p className="mt-1 text-sm text-gray-500">Información detallada de la factura.</p>
      </div>

      <Card className="mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Información de la Factura</h3>
            <p><strong>Número de Factura:</strong> {invoice.factura.numero_factura}</p>
            <p><strong>Fecha de Emisión:</strong> {new Date(invoice.factura.fecha_emision).toLocaleDateString()}</p>
            <p><strong>Subtotal:</strong> ${invoice.factura.subtotal.toFixed(2)}</p>
            <p><strong>Impuesto:</strong> ${invoice.factura.impuesto.toFixed(2)}</p>
            <p><strong>Total General:</strong> ${invoice.factura.total_general.toFixed(2)}</p>
            <p><strong>Estado de Pago:</strong> {invoice.factura.estado_pago}</p>
            <p><strong>Términos y Condiciones:</strong> {invoice.factura.terminos_condiciones || 'N/A'}</p>
          </div>
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Información del Paciente</h3>
            <p><strong>Nombre:</strong> {invoice.paciente.nombre_completo}</p>
            <p><strong>Fecha de Ingreso:</strong> {new Date(invoice.paciente.fecha_ingreso).toLocaleDateString()}</p>
            <p><strong>Fecha de Alta:</strong> {invoice.paciente.fecha_alta ? new Date(invoice.paciente.fecha_alta).toLocaleDateString() : 'N/A'}</p>
            <p><strong>Afección:</strong> {invoice.paciente.afeccion}</p>
          </div>
        </div>

        <div className="mt-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Información del Cliente</h3>
          <p><strong>Nombre:</strong> {invoice.cliente.nombre}</p>
          <p><strong>Dirección:</strong> {invoice.cliente.direccion}</p>
          <p><strong>Teléfono:</strong> {invoice.cliente.telefono}</p>
          <p><strong>Correo:</strong> {invoice.cliente.correo}</p>
        </div>

        <div className="mt-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Líneas de Factura</h3>
          {invoice.lineas.length === 0 ? (
            <p className="text-sm text-gray-500 italic">No hay líneas de factura.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descripción</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cantidad</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Precio Unitario</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subtotal sin IVA</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">IVA</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total con IVA</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {invoice.lineas.map((linea: any, index: number) => (
                    <tr key={index}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{linea.descripcion}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{linea.cantidad}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${linea.precio_unitario?.toFixed(2) || (linea.subtotal_sin_iva / linea.cantidad).toFixed(2)}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${linea.subtotal_sin_iva.toFixed(2)}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${linea.iva.toFixed(2)}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${linea.total_con_iva.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div className="mt-6 flex justify-end">
          <Button
            variant="primary"
            size="lg"
            onClick={handleDownloadPDF}
            icon={<Download size={18} />}
          >
            Descargar PDF
          </Button>
        </div>
      </Card>
    </Layout>
  );
};

export default InvoiceDetail;