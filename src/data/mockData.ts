import { Patient, Discharge, Product, Service, Invoice } from '../types';

export const patients: Patient[] = [
  {
    id: '1',
    name: 'María García',
    status: 'active',
    identificationNumber: 'P-001',
    admissionDate: '2023-10-15',
    lastUpdate: '2023-11-28',
  },
  {
    id: '2',
    name: 'Juan Rodríguez',
    status: 'discharged',
    identificationNumber: 'P-002',
    admissionDate: '2023-09-05',
    lastUpdate: '2023-11-20',
  },
  {
    id: '3',
    name: 'Ana Martínez',
    status: 'inTreatment',
    identificationNumber: 'P-003',
    admissionDate: '2023-11-10',
    lastUpdate: '2023-11-25',
  },
  {
    id: '4',
    name: 'Carlos López',
    status: 'active',
    identificationNumber: 'P-004',
    admissionDate: '2023-10-20',
    lastUpdate: '2023-11-22',
  },
  {
    id: '5',
    name: 'Laura Fernández',
    status: 'inTreatment',
    identificationNumber: 'P-005',
    admissionDate: '2023-11-05',
    lastUpdate: '2023-11-27',
  },
];

export const products: Product[] = [
  { id: '1', name: 'Analgésico', category: 'Medicamentos', price: 15.50 },
  { id: '2', name: 'Vendaje', category: 'Material', price: 8.75 },
  { id: '3', name: 'Antibiótico', category: 'Medicamentos', price: 45.00 },
  { id: '4', name: 'Jeringa', category: 'Material', price: 2.50 },
  { id: '5', name: 'Solución salina', category: 'Soluciones', price: 12.25 },
];

export const services: Service[] = [
  { id: '1', name: 'Consulta general', category: 'Consultas', price: 50.00 },
  { id: '2', name: 'Terapia física', category: 'Terapias', price: 75.00 },
  { id: '3', name: 'Radiografía', category: 'Diagnóstico', price: 120.00 },
  { id: '4', name: 'Análisis de sangre', category: 'Laboratorio', price: 85.00 },
  { id: '5', name: 'Cambio de vendaje', category: 'Enfermería', price: 35.00 },
];

export const discharges: Discharge[] = [
  {
    id: '1',
    patientId: '1',
    date: '2023-11-28',
    products: [
      { productId: '1', productName: 'Analgésico', quantity: 2, unit: 'tabletas', price: 15.50 },
      { productId: '2', productName: 'Vendaje', quantity: 1, unit: 'rollo', price: 8.75 },
    ],
    services: [
      { serviceId: '1', serviceName: 'Consulta general', description: 'Revisión de herida', price: 50.00 },
    ],
    observations: 'Paciente presenta mejoría, continuar con medicación',
    invoiced: true
  },
  {
    id: '2',
    patientId: '3',
    date: '2023-11-25',
    products: [
      { productId: '3', productName: 'Antibiótico', quantity: 1, unit: 'ampolla', price: 45.00 },
      { productId: '5', productName: 'Solución salina', quantity: 1, unit: 'bolsa', price: 12.25 },
    ],
    services: [
      { serviceId: '5', serviceName: 'Cambio de vendaje', description: 'Limpieza y aplicación', price: 35.00 },
    ],
    observations: 'Se requiere seguimiento en 3 días',
    invoiced: false
  },
  {
    id: '3',
    patientId: '2',
    date: '2023-11-20',
    products: [
      { productId: '1', productName: 'Analgésico', quantity: 4, unit: 'tabletas', price: 15.50 },
    ],
    services: [
      { serviceId: '2', serviceName: 'Terapia física', description: 'Ejercicios de rehabilitación', price: 75.00 },
      { serviceId: '3', serviceName: 'Radiografía', description: 'Control de fractura', price: 120.00 },
    ],
    observations: 'Alta médica, continuar con ejercicios en casa',
    invoiced: true
  },
];

export const invoices: Invoice[] = [
  {
    id: '1',
    dischargeId: '1',
    patientId: '1',
    date: '2023-11-28',
    items: [
      { description: 'Analgésico (2 tabletas)', quantity: 2, unitPrice: 15.50, total: 31.00 },
      { description: 'Vendaje (1 rollo)', quantity: 1, unitPrice: 8.75, total: 8.75 },
      { description: 'Consulta general', quantity: 1, unitPrice: 50.00, total: 50.00 },
    ],
    subtotal: 89.75,
    tax: 14.36,
    total: 104.11,
    status: 'paid'
  },
  {
    id: '2',
    dischargeId: '3',
    patientId: '2',
    date: '2023-11-20',
    items: [
      { description: 'Analgésico (4 tabletas)', quantity: 4, unitPrice: 15.50, total: 62.00 },
      { description: 'Terapia física', quantity: 1, unitPrice: 75.00, total: 75.00 },
      { description: 'Radiografía', quantity: 1, unitPrice: 120.00, total: 120.00 },
    ],
    subtotal: 257.00,
    tax: 41.12,
    total: 298.12,
    status: 'pending'
  }
];