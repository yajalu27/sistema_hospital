import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { 
  fetchPatients, 
  searchPatients as apiSearchPatients, 
  dischargePatient as apiDischargePatient,
  createPatient as apiCreatePatient,
  fetchInternedPatientsWithDischarges,
  getPatientDischarges,
  fetchServices,
  fetchProducts,
  createDischarge,
  fetchClients,
  createClient as apiCreateClient,
  fetchInvoices,
  fetchInvoice,
  downloadInvoicePDF,
  createInvoice,
  fetchDischargedPatientsWithUnbilledDischarges,
  Patient,
  PatientWithDischarges,
  Discharge,
  Service,
  Product,
  DescargoCreate,
  Client,
  Invoice
} from '../services/api';

interface PatientContextType {
  patients: Patient[];
  services: Service[];
  products: Product[];
  clients: Client[];
  invoices: Invoice[];
  patientsWithDischarges: PatientWithDischarges[];
  loadPatients: () => Promise<void>;
  searchPatients: (query: string) => Promise<Patient[]>;
  dischargePatient: (id: number) => Promise<void>;
  createPatient: (patientData: any) => Promise<void>;
  loadPatientsWithDischarges: () => Promise<void>;
  getPatientDischarges: (patientId: number) => Promise<Discharge[]>;
  loadServices: () => Promise<void>;
  loadProducts: () => Promise<void>;
  createDischarge: (dischargeData: DescargoCreate) => Promise<Discharge>;
  loadClients: () => Promise<void>;
  createClient: (clientData: Omit<Client, 'id'>) => Promise<Client>;
  loadInvoices: () => Promise<void>;
  fetchInvoice: (invoiceId: number) => Promise<Invoice>;
  downloadInvoicePDF: (invoiceId: number) => Promise<Blob>;
  createInvoice: (pacienteId: number, clienteId: number) => Promise<Invoice>;
  dischargedPatientsWithUnbilledDischarges: PatientWithDischarges[];
  loadDischargedPatientsWithUnbilledDischarges: () => Promise<void>;

}

const PatientContext = createContext<PatientContextType | undefined>(undefined);

export const usePatients = () => {
  const context = useContext(PatientContext);
  if (!context) {
    throw new Error('usePatients must be used within a PatientProvider');
  }
  return context;
};

export const PatientProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [services, setServices] = useState<Service[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [clients, setClients] = useState<Client[]>([]);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [patientsWithDischarges, setPatientsWithDischarges] = useState<PatientWithDischarges[]>([]);
  const [dischargedPatientsWithUnbilledDischarges, setDischargedPatientsWithUnbilledDischarges] = useState<PatientWithDischarges[]>([]);
  
  const loadDischargedPatientsWithUnbilledDischarges = async () => {
    try {
      const data = await fetchDischargedPatientsWithUnbilledDischarges();
      setDischargedPatientsWithUnbilledDischarges(data);
    } catch (error) {
      console.error('Error loading discharged patients with unbilled discharges:', error);
    }
  };
  
  const loadPatients = async () => {
    try {
      const data = await fetchPatients();
      setPatients(data);
    } catch (error) {
      console.error('Error loading patients:', error);
    }
  };

  const loadPatientsWithDischarges = async () => {
    try {
      const data = await fetchInternedPatientsWithDischarges();
      setPatientsWithDischarges(data);
    } catch (error) {
      console.error('Error loading patients with discharges:', error);
    }
  };

  const loadServices = async () => {
    try {
      const data = await fetchServices();
      setServices(data);
    } catch (error) {
      console.error('Error loading services:', error);
    }
  };

  const loadProducts = async () => {
    try {
      const data = await fetchProducts();
      setProducts(data);
    } catch (error) {
      console.error('Error loading products:', error);
    }
  };

  const loadClients = async () => {
    try {
      const data = await fetchClients();
      setClients(data);
    } catch (error) {
      console.error('Error loading clients:', error);
    }
  };

  const createClient = async (clientData: Omit<Client, 'id'>) => {
    try {
      const newClient = await apiCreateClient(clientData);
      await loadClients(); // Actualizar la lista de clientes
      return newClient;
    } catch (error) {
      console.error('Error creating client:', error);
      throw error;
    }
  };

  const loadInvoices = async () => {
    try {
      const data = await fetchInvoices();
      setInvoices(data);
    } catch (error) {
      console.error('Error loading invoices:', error);
    }
  };

  const searchPatients = async (query: string) => {
    try {
      return await apiSearchPatients(query || '');
    } catch (error) {
      console.error('Error searching patients:', error);
      return [];
    }
  };

  const dischargePatient = async (id: number) => {
    try {
      await apiDischargePatient(id);
      await loadPatients();
      await loadPatientsWithDischarges();
    } catch (error) {
      console.error('Error discharging patient:', error);
      throw error;
    }
  };

  const createPatient = async (patientData: any) => {
    try {
      await apiCreatePatient(patientData);
      await loadPatients();
    } catch (error) {
      console.error('Error creating patient:', error);
      throw error;
    }
  };

  useEffect(() => {
    loadPatients();
    loadPatientsWithDischarges();
    loadDischargedPatientsWithUnbilledDischarges();
    loadServices();
    loadProducts();
    loadClients();
    loadInvoices();
  }, []);

  return (
    <PatientContext.Provider value={{
      patients,
      services,
      products,
      clients,
      invoices,
      patientsWithDischarges,
      loadPatients,
      searchPatients,
      dischargePatient,
      createPatient,
      loadPatientsWithDischarges,
      getPatientDischarges,
      loadServices,
      loadProducts,
      createDischarge,
      loadClients,
      createClient,
      loadInvoices,
      fetchInvoice,
      downloadInvoicePDF,
      createInvoice,
      dischargedPatientsWithUnbilledDischarges,
      loadDischargedPatientsWithUnbilledDischarges,
    }}>
      {children}
    </PatientContext.Provider>
  );
};