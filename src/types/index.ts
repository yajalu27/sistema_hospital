export type PatientStatus = 'active' | 'discharged' | 'inTreatment';

export interface Patient {
  id: number;
  nombre_completo: string;
  fecha_ingreso: string;
  fecha_alta?: string;
  afeccion: string;
  enfermedades?: string;
  alergias?: string;
  estado: string;
}

export interface Discharge {
  id: number;
  patientId: number;
  date: string;
  reason: string;
  notes?: string;
}

export interface Product {
  id: string;
  name: string;
  category: string;
  price: number; // Added price field
}

export interface Service {
  id: string;
  name: string;
  category: string;
  price: number; // Added price field
}



export interface Invoice {
  id: string;
  dischargeId: string;
  patientId: string;
  date: string;
  items: {
    description: string;
    quantity: number;
    unitPrice: number;
    total: number;
  }[];
  subtotal: number;
  tax: number;
  total: number;
  status: 'pending' | 'paid' | 'cancelled';
}