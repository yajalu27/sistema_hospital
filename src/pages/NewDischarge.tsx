import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePatients } from '../context/PatientContext';
import Layout from '../components/layout/Layout';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Select from '../components/ui/Select';
import { Plus, Trash2, Save } from 'lucide-react';

const NewDischarge: React.FC = () => {
  const navigate = useNavigate();
  const { patients, services, products, createDischarge } = usePatients();

  const [patientId, setPatientId] = useState('');
  const [selectedItems, setSelectedItems] = useState<{
    type: 'product' | 'service';
    id: string;
    quantity: number;
    description?: string;
  }[]>([]);
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Filtrar pacientes activos (no dados de alta)
  const activePatients = patients.filter(p => p.estado === 'internado');
  const patientOptions = activePatients.map(patient => ({
    value: patient.id.toString(),
    label: patient.nombre_completo
  }));

  const productOptions = products.map(product => ({
    value: product.id.toString(),
    label: product.descripcion
  }));

  const serviceOptions = services.map(service => ({
    value: service.id.toString(),
    label: service.descripcion
  }));

  const addItem = (type: 'product' | 'service') => {
    setSelectedItems([
      ...selectedItems,
      { type, id: '', quantity: 1, description: type === 'service' ? '' : undefined }
    ]);
  };

  const updateItem = (index: number, field: string, value: string) => {
    const updatedItems = [...selectedItems];
    if (field === 'quantity') {
      updatedItems[index] = { ...updatedItems[index], [field]: Math.max(1, parseInt(value) || 1) };
    } else {
      updatedItems[index] = { ...updatedItems[index], [field]: value };
    }
    setSelectedItems(updatedItems);
  };

  const removeItem = (index: number) => {
    const updatedItems = [...selectedItems];
    updatedItems.splice(index, 1);
    setSelectedItems(updatedItems);
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!patientId) {
      newErrors.patientId = 'Debe seleccionar un paciente';
    }

    if (selectedItems.length === 0) {
      newErrors.general = 'Debe agregar al menos un producto o servicio';
    }

    selectedItems.forEach((item, index) => {
      if (!item.id) {
        newErrors[`item_${index}_id`] = `Seleccione un ${item.type === 'product' ? 'producto' : 'servicio'}`;
      }
      if (item.quantity <= 0) {
        newErrors[`item_${index}_quantity`] = 'La cantidad debe ser mayor a 0';
      }
      if (item.type === 'service' && !item.description) {
        newErrors[`item_${index}_description`] = 'Ingrese una descripción para el servicio';
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }

    try {
      const dischargeData = {
        paciente_id: parseInt(patientId),
        lineas: selectedItems.map(item => ({
          servicio_id: item.type === 'service' ? parseInt(item.id) : undefined,
          producto_id: item.type === 'product' ? parseInt(item.id) : undefined,
          cantidad: item.quantity,
          ...(item.type === 'service' && { descripcion: item.description })
        }))
      };

      await createDischarge(dischargeData);
      alert('Descargo registrado exitosamente');
      navigate('/discharges');
    } catch (error) {
      console.error('Error al registrar descargo:', error);
      alert('Hubo un error al registrar el descargo. Por favor, intenta de nuevo.');
    }
  };

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Generar Nuevo Consumo</h1>
        <p className="mt-1 text-sm text-gray-500">
          Registre un nuevo consumo o descargo para un paciente.
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        <Card className="mb-6">
          <Select
            label="Seleccionar Paciente"
            options={patientOptions}
            value={patientId}
            onChange={(value) => setPatientId(value)}
            error={errors.patientId}
            required
          />

          {errors.general && (
            <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-md text-sm">
              {errors.general}
            </div>
          )}

          <div className="mb-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">Items (Productos o Servicios)</h3>
              <div className="space-x-2">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => addItem('product')}
                  icon={<Plus size={16} />}
                >
                  Agregar Producto
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => addItem('service')}
                  icon={<Plus size={16} />}
                >
                  Agregar Servicio
                </Button>
              </div>
            </div>

            {selectedItems.length === 0 ? (
              <p className="text-sm text-gray-500 italic">No hay items seleccionados.</p>
            ) : (
              <div className="space-y-4">
                {selectedItems.map((item, index) => (
                  <div key={index} className="bg-gray-50 p-4 rounded-md">
                    <div className="flex justify-between items-start mb-3">
                      <h4 className="text-sm font-medium text-gray-700">
                        {item.type === 'product' ? `Producto ${index + 1}` : `Servicio ${index + 1}`}
                      </h4>
                      <Button
                        type="button"
                        variant="secondary"
                        size="sm"
                        onClick={() => removeItem(index)}
                        icon={<Trash2 size={16} />}
                      >
                        Eliminar
                      </Button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <Select
                        label={item.type === 'product' ? 'Producto' : 'Servicio'}
                        options={item.type === 'product' ? productOptions : serviceOptions}
                        value={item.id}
                        onChange={(value) => updateItem(index, 'id', value)}
                        error={errors[`item_${index}_id`]}
                      />
                      <Input
                        type="number"
                        label="Cantidad"
                        min="1"
                        value={item.quantity.toString()}
                        onChange={(e) => updateItem(index, 'quantity', e.target.value)}
                        error={errors[`item_${index}_quantity`]}
                      />
                      {item.type === 'service' && (
                        <Input
                          label="Descripción"
                          placeholder="Descripción del servicio aplicado"
                          value={item.description || ''}
                          onChange={(e) => updateItem(index, 'description', e.target.value)}
                          error={errors[`item_${index}_description`]}
                        />
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="flex justify-end pt-4 border-t border-gray-200">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              icon={<Save size={18} />}
            >
              Guardar Descargo
            </Button>
          </div>
        </Card>
      </form>
    </Layout>
  );
};

export default NewDischarge;