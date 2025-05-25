import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePatients } from '../context/PatientContext';
import Layout from '../components/layout/Layout';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Select from '../components/ui/Select';
import { products, services } from '../data/mockData';
import { Discharge } from '../types';
import { Plus, Trash2, Save } from 'lucide-react';

const NewDischarge: React.FC = () => {
  const navigate = useNavigate();
  const { patients, addDischarge } = usePatients();
  
  const [patientId, setPatientId] = useState('');
  const [selectedProducts, setSelectedProducts] = useState<{
    productId: string;
    quantity: number;
    unit: string;
  }[]>([]);
  const [selectedServices, setSelectedServices] = useState<{
    serviceId: string;
    description: string;
  }[]>([]);
  const [observations, setObservations] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});

  const activePatients = patients.filter(p => p.status !== 'discharged');
  const patientOptions = activePatients.map(patient => ({
    value: patient.id,
    label: `${patient.name} (${patient.identificationNumber})`
  }));

  const productOptions = products.map(product => ({
    value: product.id,
    label: product.name
  }));

  const serviceOptions = services.map(service => ({
    value: service.id,
    label: service.name
  }));

  const addProduct = () => {
    setSelectedProducts([
      ...selectedProducts,
      { productId: '', quantity: 1, unit: '' }
    ]);
  };

  const updateProduct = (index: number, field: string, value: string | number) => {
    const updatedProducts = [...selectedProducts];
    updatedProducts[index] = { 
      ...updatedProducts[index], 
      [field]: value 
    };
    setSelectedProducts(updatedProducts);
  };

  const removeProduct = (index: number) => {
    const updatedProducts = [...selectedProducts];
    updatedProducts.splice(index, 1);
    setSelectedProducts(updatedProducts);
  };

  const addService = () => {
    setSelectedServices([
      ...selectedServices,
      { serviceId: '', description: '' }
    ]);
  };

  const updateService = (index: number, field: string, value: string) => {
    const updatedServices = [...selectedServices];
    updatedServices[index] = { 
      ...updatedServices[index], 
      [field]: value 
    };
    setSelectedServices(updatedServices);
  };

  const removeService = (index: number) => {
    const updatedServices = [...selectedServices];
    updatedServices.splice(index, 1);
    setSelectedServices(updatedServices);
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!patientId) {
      newErrors.patientId = 'Debe seleccionar un paciente';
    }

    if (selectedProducts.length === 0 && selectedServices.length === 0) {
      newErrors.general = 'Debe agregar al menos un producto o servicio';
    }

    selectedProducts.forEach((product, index) => {
      if (!product.productId) {
        newErrors[`product_${index}_id`] = 'Seleccione un producto';
      }
      if (!product.unit) {
        newErrors[`product_${index}_unit`] = 'Ingrese una unidad';
      }
      if (product.quantity <= 0) {
        newErrors[`product_${index}_quantity`] = 'La cantidad debe ser mayor a 0';
      }
    });

    selectedServices.forEach((service, index) => {
      if (!service.serviceId) {
        newErrors[`service_${index}_id`] = 'Seleccione un servicio';
      }
      if (!service.description) {
        newErrors[`service_${index}_description`] = 'Ingrese una descripción';
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }

    const formattedProducts = selectedProducts.map(product => {
      const productInfo = products.find(p => p.id === product.productId);
      return {
        productId: product.productId,
        productName: productInfo?.name || '',
        quantity: product.quantity,
        unit: product.unit
      };
    });

    const formattedServices = selectedServices.map(service => {
      const serviceInfo = services.find(s => s.id === service.serviceId);
      return {
        serviceId: service.serviceId,
        serviceName: serviceInfo?.name || '',
        description: service.description
      };
    });

    const newDischarge: Omit<Discharge, 'id'> = {
      patientId,
      date: '',  // This will be set in the context
      products: formattedProducts,
      services: formattedServices,
      observations
    };

    addDischarge(newDischarge);
    alert('Descargo registrado exitosamente');
    navigate('/discharges');
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
            onChange={setPatientId}
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
              <h3 className="text-lg font-medium text-gray-900">Productos</h3>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={addProduct}
                icon={<Plus size={16} />}
              >
                Agregar Producto
              </Button>
            </div>

            {selectedProducts.length === 0 ? (
              <p className="text-sm text-gray-500 italic">No hay productos seleccionados.</p>
            ) : (
              <div className="space-y-4">
                {selectedProducts.map((product, index) => (
                  <div key={index} className="bg-gray-50 p-4 rounded-md">
                    <div className="flex justify-between items-start mb-3">
                      <h4 className="text-sm font-medium text-gray-700">Producto {index + 1}</h4>
                      <Button
                        type="button"
                        variant="secondary"
                        size="sm"
                        onClick={() => removeProduct(index)}
                        icon={<Trash2 size={16} />}
                      >
                        Eliminar
                      </Button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <Select
                        label="Producto"
                        options={productOptions}
                        value={product.productId}
                        onChange={(value) => updateProduct(index, 'productId', value)}
                        error={errors[`product_${index}_id`]}
                      />
                      <Input
                        type="number"
                        label="Cantidad"
                        min="1"
                        value={product.quantity.toString()}
                        onChange={(e) => updateProduct(index, 'quantity', parseInt(e.target.value) || 0)}
                        error={errors[`product_${index}_quantity`]}
                      />
                      <Input
                        label="Unidad"
                        placeholder="ej: tabletas, ampollas, etc."
                        value={product.unit}
                        onChange={(e) => updateProduct(index, 'unit', e.target.value)}
                        error={errors[`product_${index}_unit`]}
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="mb-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">Servicios</h3>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={addService}
                icon={<Plus size={16} />}
              >
                Agregar Servicio
              </Button>
            </div>

            {selectedServices.length === 0 ? (
              <p className="text-sm text-gray-500 italic">No hay servicios seleccionados.</p>
            ) : (
              <div className="space-y-4">
                {selectedServices.map((service, index) => (
                  <div key={index} className="bg-gray-50 p-4 rounded-md">
                    <div className="flex justify-between items-start mb-3">
                      <h4 className="text-sm font-medium text-gray-700">Servicio {index + 1}</h4>
                      <Button
                        type="button"
                        variant="secondary"
                        size="sm"
                        onClick={() => removeService(index)}
                        icon={<Trash2 size={16} />}
                      >
                        Eliminar
                      </Button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <Select
                        label="Servicio"
                        options={serviceOptions}
                        value={service.serviceId}
                        onChange={(value) => updateService(index, 'serviceId', value)}
                        error={errors[`service_${index}_id`]}
                      />
                      <Input
                        label="Descripción"
                        placeholder="Descripción del servicio aplicado"
                        value={service.description}
                        onChange={(e) => updateService(index, 'description', e.target.value)}
                        error={errors[`service_${index}_description`]}
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="mb-4">
            <label htmlFor="observations" className="block text-sm font-medium text-gray-700 mb-1">
              Observaciones
            </label>
            <textarea
              id="observations"
              rows={4}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              placeholder="Ingrese observaciones relevantes sobre este descargo..."
              value={observations}
              onChange={(e) => setObservations(e.target.value)}
            />
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