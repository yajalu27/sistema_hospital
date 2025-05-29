import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
  paciente_id: number;
  fecha: string;
  total: number;
  lineas?: DischargeLine[];
}

export interface DischargeLine {
  id: number;
  descripcion: string;
  subtotal_sin_iva: number;
  cantidad: number;
  servicio_id?: number;
  producto_id?: number;
}

export interface PatientWithDischarges extends Patient {
  descargos?: Discharge[];
}

export interface Service {
  id: number;
  tipo: string;
  precio_base: number;
  descripcion: string;
}

export interface Product {
  id: number;
  tipo: string;
  precio_base: number;
  descripcion: string;
}

export interface LineaDescargoCreate {
  servicio_id?: number;
  producto_id?: number;
  cantidad: number;
}

export interface DescargoCreate {
  paciente_id: number;
  lineas: LineaDescargoCreate[];
}

export interface Client {
  id: number;
  nombre: string;
  direccion: string;
  telefono: string;
  correo: string;
}

export interface InvoiceLine {
  descripcion: string;
  cantidad: number;
  precio_unitario?: number;
  subtotal_sin_iva: number;
  iva: number;
  total_con_iva: number;
}

export interface Invoice {
  factura: {
    id: number;
    numero_factura: string;
    fecha_emision: string;
    subtotal: number;
    impuesto: number;
    total_general: number;
    estado_pago: string;
    paciente_id: number;
    cliente_id: number;
    terminos_condiciones?: string;
  };
  paciente: {
    id: number;
    nombre_completo: string;
    fecha_ingreso: string;
    fecha_alta?: string;
    afeccion: string;
  };
  cliente: Client;
  lineas: InvoiceLine[];
  hospital?: {
    nombre: string;
    direccion: string;
    telefono: string;
    email: string;
    web: string;
    representante: string;
  };
}

export const fetchPatients = async (): Promise<Patient[]> => {
  const response = await api.get('/pacientes/listar_pacientes/');
  return response.data;
};

export const searchPatients = async (query: string): Promise<Patient[]> => {
  const response = await api.get('/pacientes/buscar_paciente/', {
    params: { search: query }
  });
  return response.data;
};

export const dischargePatient = async (id: number): Promise<Patient> => {
  const response = await api.patch(`/pacientes/daralta_paciente/${id}/alta`);
  return response.data;
};

export const createPatient = async (patientData: any): Promise<Patient> => {
  const response = await api.post('/pacientes/crear_paciente/', patientData);
  return response.data;
};

export const fetchInternedPatientsWithDischarges = async (): Promise<PatientWithDischarges[]> => {
  const response = await api.get('/pacientes/internados-con-descargos/');
  return response.data;
};

export const fetchDischargedPatientsWithDischarges = async (): Promise<PatientWithDischarges[]> => {
  const response = await api.get('/descargos/alta-con-descargos/');
  return response.data;
};

export const getPatientDischarges = async (patientId: number): Promise<Discharge[]> => {
  const response = await api.get(`/descargos/paciente/${patientId}`);
  return response.data;
};

export const fetchServices = async (): Promise<Service[]> => {
  const response = await api.get('/servicios/');
  return response.data;
};

export const fetchProducts = async (): Promise<Product[]> => {
  const response = await api.get('/productos/');
  return response.data;
};

export const createDischarge = async (dischargeData: DescargoCreate): Promise<Discharge> => {
  const response = await api.post('/descargos/', dischargeData);
  return response.data;
};

export const fetchClients = async (): Promise<Client[]> => {
  const response = await api.get('/clientes/');
  return response.data;
};

export const createClient = async (clientData: Omit<Client, 'id'>): Promise<Client> => {
  const response = await api.post('/clientes/', clientData);
  return response.data;
};

export const fetchInvoices = async (): Promise<Invoice[]> => {
  const response = await api.get('/facturas/');
  return response.data;
};

export const fetchInvoice = async (invoiceId: number): Promise<Invoice> => {
  const response = await api.get(`/facturas/${invoiceId}`);
  return response.data;
};

export const downloadInvoicePDF = async (invoiceId: number): Promise<Blob> => {
  const response = await api.get(`/facturas/${invoiceId}/pdf`, {
    responseType: 'blob'
  });
  return response.data;
};

export const createInvoice = async (pacienteId: number, clienteId: number): Promise<Invoice> => {
  const response = await api.post(`/facturas/generar/${pacienteId}/${clienteId}`);
  return response.data;
};

export const fetchDischargedPatientsWithUnbilledDischarges = async (): Promise<PatientWithDischarges[]> => {
  const response = await api.get('/pacientes/alta-con-descargos-no-facturados/');
  return response.data;
};