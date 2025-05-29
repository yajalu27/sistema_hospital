// components/NewInvoice.tsx

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePatients } from '../context/PatientContext';
import Layout from '../components/layout/Layout';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Select from '../components/ui/Select';
import { Save } from 'lucide-react';
import axios from 'axios';

const NewInvoice: React.FC = () => {
  const navigate = useNavigate();
  const { 
    dischargedPatientsWithUnbilledDischarges, 
    invoices, 
    createInvoice, 
    createClient,
    loadDischargedPatientsWithUnbilledDischarges 
  } = usePatients();

  const [pacienteId, setPacienteId] = useState('');
  const [clientData, setClientData] = useState({
    nombre: '',
    direccion: '',
    telefono: '',
    correo: ''
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);

  // Cargar los pacientes al montar el componente
  useEffect(() => {
    const loadData = async () => {
      await loadDischargedPatientsWithUnbilledDischarges();
      setLoading(false);
    };
    loadData();
  }, [loadDischargedPatientsWithUnbilledDischarges]);

  // Preparar las opciones para el Select
  const patientOptions = dischargedPatientsWithUnbilledDischarges.map(patient => ({
    value: patient.id.toString(),
    label: patient.nombre_completo
  }));

  const handleClientChange = (field: keyof typeof clientData, value: string) => {
    setClientData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!pacienteId) {
      newErrors.pacienteId = 'Debe seleccionar un paciente';
    }

    if (!clientData.nombre) {
      newErrors.nombre = 'El nombre del cliente es obligatorio';
    }

    if (!clientData.direccion) {
      newErrors.direccion = 'La dirección del cliente es obligatoria';
    }

    if (!clientData.telefono) {
      newErrors.telefono = 'El teléfono del cliente es obligatorio';
    }

    if (!clientData.correo) {
      newErrors.correo = 'El correo del cliente es obligatorio';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(clientData.correo)) {
      newErrors.correo = 'El correo no es válido';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    try {
      // Crear el cliente
      const newClient = await createClient(clientData);
      let clientId;
      
      if ('data' in newClient && typeof newClient.data === 'object' && 'id' in newClient.data) {
        clientId = newClient.data.id;
      } else if ('id' in newClient) {
        clientId = newClient.id;
      } else {
        throw new Error('La respuesta de creación del cliente no contiene un ID válido');
      }

      // Generar la factura con el cliente recién creado
      await createInvoice(Number(pacienteId), clientId);
      alert('Factura generada exitosamente');
      navigate('/invoices');
    } catch (error) {
      console.error('Error al generar factura:', error);
      if (axios.isAxiosError(error) && error.response) {
        alert(`Error al generar la factura: ${error.response.data.detail || 'Error desconocido'}`);
      } else {
        alert('Error al generar la factura. Por favor, intenta de nuevo.');
      }
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <p>Cargando pacientes...</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Generar Nueva Factura</h1>
        <p className="mt-1 text-sm text-gray-500">
          Seleccione un paciente con descargos no facturados y registre los datos del cliente.
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        <Card className="mb-6">
          <Select
            label="Seleccionar Paciente"
            options={patientOptions}
            value={pacienteId}
            onChange={setPacienteId}
            error={errors.pacienteId}
            required
          />

          {patientOptions.length === 0 && (
            <div className="mt-4 p-3 bg-yellow-50 text-yellow-700 rounded-md text-sm">
              No hay pacientes con descargos pendientes de facturación.
            </div>
          )}

          <div className="mt-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Datos del Cliente</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Nombre</label>
                <input
                  type="text"
                  value={clientData.nombre}
                  onChange={(e) => handleClientChange('nombre', e.target.value)}
                  className={`mt-1 block w-full border-gray-300 rounded-md shadow-sm ${errors.nombre ? 'border-red-500' : ''}`}
                  required
                />
                {errors.nombre && <p className="mt-1 text-sm text-red-600">{errors.nombre}</p>}
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Dirección</label>
                <input
                  type="text"
                  value={clientData.direccion}
                  onChange={(e) => handleClientChange('direccion', e.target.value)}
                  className={`mt-1 block w-full border-gray-300 rounded-md shadow-sm ${errors.direccion ? 'border-red-500' : ''}`}
                  required
                />
                {errors.direccion && <p className="mt-1 text-sm text-red-600">{errors.direccion}</p>}
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Teléfono</label>
                <input
                  type="text"
                  value={clientData.telefono}
                  onChange={(e) => handleClientChange('telefono', e.target.value)}
                  className={`mt-1 block w-full border-gray-300 rounded-md shadow-sm ${errors.telefono ? 'border-red-500' : ''}`}
                  required
                />
                {errors.telefono && <p className="mt-1 text-sm text-red-600">{errors.telefono}</p>}
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Correo</label>
                <input
                  type="email"
                  value={clientData.correo}
                  onChange={(e) => handleClientChange('correo', e.target.value)}
                  className={`mt-1 block w-full border-gray-300 rounded-md shadow-sm ${errors.correo ? 'border-red-500' : ''}`}
                  required
                />
                {errors.correo && <p className="mt-1 text-sm text-red-600">{errors.correo}</p>}
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-gray-200">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              icon={<Save size={18} />}
              disabled={patientOptions.length === 0}
            >
              Generar Factura
            </Button>
          </div>
        </Card>
      </form>
    </Layout>
  );
};

export default NewInvoice;