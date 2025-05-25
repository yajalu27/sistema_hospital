import React, { useState } from 'react';
import { usePatients } from '../context/PatientContext';
import Layout from '../components/layout/Layout';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import { Search, ChevronDown, ChevronUp } from 'lucide-react';
import { Discharge } from '../types';

const Discharges: React.FC = () => {
  const { searchDischargesByPatient, patients } = usePatients();
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedDischarge, setExpandedDischarge] = useState<string | null>(null);

  const discharges = searchQuery ? searchDischargesByPatient(searchQuery) : [];

  const getPatientName = (patientId: string) => {
    const patient = patients.find(p => p.id === patientId);
    return patient ? patient.name : 'Paciente desconocido';
  };

  const toggleDischarge = (dischargeId: string) => {
    if (expandedDischarge === dischargeId) {
      setExpandedDischarge(null);
    } else {
      setExpandedDischarge(dischargeId);
    }
  };

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Descargos de Pacientes</h1>
        <p className="mt-1 text-sm text-gray-500">
          Busque y visualice los descargos realizados para cada paciente.
        </p>
      </div>

      <Card className="mb-6">
        <Input
          label="Buscar descargos por nombre de paciente o número de identificación"
          placeholder="Ingrese nombre o ID del paciente..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          icon={<Search size={18} />}
        />
      </Card>

      {searchQuery && discharges.length === 0 && (
        <div className="bg-white p-6 rounded-lg shadow-sm text-center">
          <p className="text-gray-500">No se encontraron descargos para el paciente buscado.</p>
        </div>
      )}

      {discharges.length > 0 && (
        <div className="space-y-4">
          {discharges.map((discharge) => (
            <Card key={discharge.id} className="transition-all duration-200">
              <div 
                className="flex justify-between items-center cursor-pointer"
                onClick={() => toggleDischarge(discharge.id)}
              >
                <div>
                  <h3 className="text-lg font-medium text-gray-900">
                    {getPatientName(discharge.patientId)}
                  </h3>
                  <p className="text-sm text-gray-500">Fecha: {discharge.date}</p>
                </div>
                <div>
                  {expandedDischarge === discharge.id ? 
                    <ChevronUp className="text-gray-400" /> : 
                    <ChevronDown className="text-gray-400" />
                  }
                </div>
              </div>

              {expandedDischarge === discharge.id && (
                <div className="mt-4 pt-4 border-t border-gray-200 animate-fadeIn">
                  {discharge.products.length > 0 && (
                    <div className="mb-4">
                      <h4 className="font-medium text-sm text-gray-700 mb-2">Productos utilizados:</h4>
                      <div className="bg-gray-50 p-3 rounded-md">
                        <ul className="divide-y divide-gray-200">
                          {discharge.products.map((product, index) => (
                            <li key={index} className="py-2 first:pt-0 last:pb-0">
                              <div className="flex justify-between">
                                <span className="text-sm font-medium">{product.productName}</span>
                                <span className="text-sm text-gray-500">{product.quantity} {product.unit}</span>
                              </div>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  {discharge.services.length > 0 && (
                    <div className="mb-4">
                      <h4 className="font-medium text-sm text-gray-700 mb-2">Servicios aplicados:</h4>
                      <div className="bg-gray-50 p-3 rounded-md">
                        <ul className="divide-y divide-gray-200">
                          {discharge.services.map((service, index) => (
                            <li key={index} className="py-2 first:pt-0 last:pb-0">
                              <div>
                                <span className="text-sm font-medium">{service.serviceName}</span>
                                <p className="text-sm text-gray-500 mt-1">{service.description}</p>
                              </div>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  <div>
                    <h4 className="font-medium text-sm text-gray-700 mb-2">Observaciones:</h4>
                    <div className="bg-gray-50 p-3 rounded-md">
                      <p className="text-sm text-gray-700">{discharge.observations || "Sin observaciones"}</p>
                    </div>
                  </div>
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </Layout>
  );
};

export default Discharges;