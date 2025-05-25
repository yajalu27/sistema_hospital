export type PatientStatus = 'active' | 'discharged' | 'inTreatment';

export interface Patient {
  id: string;
  name: string;
  status: PatientStatus;
  identificationNumber: string;
  admissionDate: string;
  lastUpdate: string;
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

export interface Discharge {
  id: string;
  patientId: string;
  date: string;
  products: {
    productId: string;
    productName: string;
    quantity: number;
    unit: string;
    price: number; // Added price field
  }[];
  services: {
    serviceId: string;
    serviceName: string;
    description: string;
    price: number; // Added price field
  }[];
  observations: string;
  invoiced: boolean; // Added invoiced field
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