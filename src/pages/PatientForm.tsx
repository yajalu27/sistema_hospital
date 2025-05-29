// src/pages/PatientForm.tsx
import React, { useState } from 'react';
import Button from '../components/ui/Button';

interface PatientFormProps {
  onSubmit: (patientData: any) => Promise<void>;
  onCancel: () => void;
}

const PatientForm: React.FC<PatientFormProps> = ({ onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    nombre_completo: '',
    afeccion: '',
    enfermedades: '',
    alergias: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Limpiar error si existe
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.nombre_completo.trim()) {
      newErrors.nombre_completo = 'El nombre completo es obligatorio';
    }
    
    if (!formData.afeccion.trim()) {
      newErrors.afeccion = 'La afección es obligatoria';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validate()) return;
    
    setIsSubmitting(true);
    try {
      const trimmedData = {
        nombre_completo: formData.nombre_completo.trim(),
        afeccion: formData.afeccion.trim(),
        enfermedades: formData.enfermedades.trim(),
        alergias: formData.alergias.trim(),
      };
      await onSubmit(trimmedData);
    } catch (error) {
      console.error('Error al crear paciente:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Nombre Completo *
        </label>
        <input
          type="text"
          name="nombre_completo"
          value={formData.nombre_completo}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-gray-100"
          disabled={isSubmitting}
          required
        />
        {errors.nombre_completo && (
          <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.nombre_completo}</p>
        )}
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Afección *
        </label>
        <input
          type="text"
          name="afeccion"
          value={formData.afeccion}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-gray-100"
          disabled={isSubmitting}
          required
        />
        {errors.afeccion && (
          <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.afeccion}</p>
        )}
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Enfermedades (opcional)
        </label>
        <input
          type="text"
          name="enfermedades"
          value={formData.enfermedades}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-gray-100"
          disabled={isSubmitting}
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Alergias (opcional)
        </label>
        <input
          type="text"
          name="alergias"
          value={formData.alergias}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-gray-100"
          disabled={isSubmitting}
        />
      </div>

      <div className="flex justify-end space-x-3 mt-6">
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancelar
        </Button>
        <Button
          type="submit"
          variant="primary"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Creando...' : 'Crear Paciente'}
        </Button>
      </div>
    </form>
  );
};

export default PatientForm;