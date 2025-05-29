import React, { useEffect, useState } from 'react';
import { usePatients } from '../context/PatientContext';
import Layout from '../components/layout/Layout';
import Card from '../components/ui/Card';
import { PatientWithDischarges } from '../services/api';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/outline';

const Discharges: React.FC = () => {
  const { patientsWithDischarges, loadPatientsWithDischarges } = usePatients();
  const [expandedPatient, setExpandedPatient] = useState<number | null>(null);

  useEffect(() => {
    loadInternedPatients();
  }, []);

  const loadInternedPatients = async () => {
    try {
      await loadPatientsWithDischarges();
    } catch (error) {
      console.error('Error loading interned patients with discharges:', error);
    }
  };

  const togglePatient = (patientId: number) => {
    setExpandedPatient(expandedPatient === patientId ? null : patientId);
  };

  const calculateTotals = (patient: PatientWithDischarges) => {
    const totalDischarges = patient.descargos?.length || 0;
    const totalAmount = patient.descargos?.reduce((sum, discharge) => sum + discharge.total, 0) || 0;
    return { totalDischarges, totalAmount };
  };

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Pacientes Internados con Descargos</h1>
        <p className="mt-1 text-sm text-gray-500">Lista de pacientes internados con descargos registrados.</p>
      </div>
      <Card className="mb-6">
        {patientsWithDischarges.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {patientsWithDischarges.map((patient) => {
              const { totalDischarges, totalAmount } = calculateTotals(patient);
              const isExpanded = expandedPatient === patient.id;

              return (
                <li key={patient.id} className="py-4">
                  <div
                    className="flex items-center justify-between cursor-pointer hover:bg-gray-50 p-3 rounded-lg transition-colors duration-200"
                    onClick={() => togglePatient(patient.id)}
                  >
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <h3 className="text-lg font-semibold text-gray-900">{patient.nombre_completo}</h3>
                        <span className="text-sm text-gray-500">(ID: {patient.id})</span>
                      </div>
                      <div className="mt-1 flex space-x-4 text-sm">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {totalDischarges} Descargo{totalDischarges !== 1 ? 's' : ''}
                        </span>
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          Total: ${totalAmount.toFixed(2)}
                        </span>
                      </div>
                    </div>
                    <div>
                      {isExpanded ? (
                        <ChevronUpIcon className="h-5 w-5 text-gray-500" />
                      ) : (
                        <ChevronDownIcon className="h-5 w-5 text-gray-500" />
                      )}
                    </div>
                  </div>
                  {isExpanded && (
                    <div className="mt-2 pl-6 transition-all duration-300 ease-in-out">
                      <ul className="space-y-2">
                        {patient.descargos?.map((discharge) => (
                          <li
                            key={discharge.id}
                            className="text-sm text-gray-600 bg-gray-50 p-3 rounded-md"
                          >
                            <span className="font-medium">Descargo #{discharge.id}</span> - Total: $
                            {discharge.total.toFixed(2)} - Fecha:{' '}
                            {new Date(discharge.fecha).toLocaleDateString()}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        ) : (
          <p className="text-gray-500 text-center py-4">No hay pacientes internados con descargos.</p>
        )}
      </Card>
    </Layout>
  );
};

export default Discharges;