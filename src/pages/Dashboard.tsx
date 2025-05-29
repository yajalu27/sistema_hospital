import React, { useState, useEffect } from 'react';
import { usePatients } from '../context/PatientContext';
import Layout from '../components/layout/Layout';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Modal from '../pages/Modal';
import StatusBadge from '../components/ui/StatusBadge';
import { Search, UserPlus, UserCheck } from 'lucide-react';
import PatientForm from '../pages/PatientForm';

const Dashboard: React.FC = () => {
  const { patients, searchPatients, dischargePatient, createPatient } = usePatients();
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [filteredPatients, setFilteredPatients] = useState<any[]>([]);
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    const loadFilteredPatients = async () => {
      setIsLoading(true);
      try {
        const allPatients = await searchPatients(searchQuery);
        const internados = allPatients.filter(p => p.estado === 'internado');
        setFilteredPatients(internados);
      } catch (error) {
        console.error('Error filtering patients:', error);
        setFilteredPatients([]);
      } finally {
        setIsLoading(false);
      }
    };

    loadFilteredPatients();
  }, [searchQuery, patients]);

  const handleDischargePatient = async (id: number) => {
    if (window.confirm('¿Está seguro de dar de alta a este paciente?')) {
      try {
        await dischargePatient(id);
      } catch (error) {
        alert('Error al dar de alta al paciente');
      }
    }
  };

  const handleCreatePatient = async (patientData: any) => {
    try {
      await createPatient(patientData);
      setShowCreateModal(false);
    } catch (error) {
      alert('Error al crear el paciente');
    }
  };

  const formatDate = (dateString: string | undefined) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return 'N/A';
    }
  };

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Dashboard de Pacientes</h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Administre los pacientes activos, vea su estado y realice acciones.
        </p>
      </div>

      <Card className="mb-6 dark:bg-gray-800">
        <div className="flex flex-col md:flex-row md:space-x-4">
          <div className="flex-1 mb-4 md:mb-0">
            <Input
              placeholder="Buscar paciente por nombre o ID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              icon={<Search size={18} />}
            />
          </div>
          <div className="flex items-center">
            <Button
              onClick={() => setShowCreateModal(true)}
              icon={<UserPlus size={16} />}
            >
              Nuevo Paciente
            </Button>
          </div>
        </div>
      </Card>

      <div className="bg-white dark:bg-gray-800 shadow-sm rounded-lg overflow-hidden">
        {isLoading ? (
          <div className="p-8 text-center">
            <p className="text-gray-500 dark:text-gray-400">Cargando pacientes...</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Paciente</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Estado</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Fecha de admisión</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Afección</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {filteredPatients.length > 0 ? (
                  filteredPatients.map((patient) => (
                    <React.Fragment key={patient.id}>
                      <tr className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-150">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900 dark:text-gray-100">{patient.nombre_completo}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-500 dark:text-gray-400">{patient.id}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <StatusBadge status="active" />
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                          {formatDate(patient.fecha_ingreso)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                          {patient.afeccion}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleDischargePatient(patient.id)}
                            icon={<UserCheck size={16} />}
                          >
                            Dar de alta
                          </Button>
                        </td>
                      </tr>
                    </React.Fragment>
                  ))
                ) : (
                  <tr>
                    <td colSpan={6} className="px-6 py-4 text-center text-sm text-gray-500 dark:text-gray-400">
                      {searchQuery
                        ? "No se encontraron pacientes internados que coincidan con la búsqueda."
                        : "No hay pacientes internados actualmente."}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Registrar Nuevo Paciente holaa"
      >
        <PatientForm
          onSubmit={handleCreatePatient}
          onCancel={() => setShowCreateModal(false)}
        />
      </Modal>
    </Layout>
  );
};

export default Dashboard;