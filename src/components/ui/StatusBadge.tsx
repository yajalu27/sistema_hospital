import React from 'react';
import { PatientStatus } from '../../types';

interface StatusBadgeProps {
  status: PatientStatus;
}

const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  let bgColor = '';
  let textColor = '';
  let label = '';

  switch (status) {
    case 'active':
      bgColor = 'bg-green-100';
      textColor = 'text-green-800';
      label = 'Activo';
      break;
    case 'discharged':
      bgColor = 'bg-gray-100';
      textColor = 'text-gray-800';
      label = 'Dado de alta';
      break;
    case 'inTreatment':
      bgColor = 'bg-blue-100';
      textColor = 'text-blue-800';
      label = 'En tratamiento';
      break;
    default:
      bgColor = 'bg-gray-100';
      textColor = 'text-gray-800';
      label = 'Desconocido';
  }

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${bgColor} ${textColor}`}>
      {label}
    </span>
  );
};

export default StatusBadge;