import React, { createContext, useContext, useState, ReactNode } from 'react';
import { Patient, Discharge, PatientStatus } from '../types';
import { patients as initialPatients, discharges as initialDischarges } from '../data/mockData';

interface PatientContextType {
  patients: Patient[];
  discharges: Discharge[];
  searchPatients: (query: string, status?: PatientStatus) => Patient[];
  getPatientById: (id: string) => Patient | undefined;
  getDischargesByPatientId: (patientId: string) => Discharge[];
  searchDischargesByPatient: (query: string) => Discharge[];
  dischargePatient: (id: string) => void;
  addDischarge: (discharge: Omit<Discharge, 'id'>) => void;
}

const PatientContext = createContext<PatientContextType | undefined>(undefined);

export const PatientProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [patients, setPatients] = useState<Patient[]>(initialPatients);
  const [discharges, setDischarges] = useState<Discharge[]>(initialDischarges);

  const searchPatients = (query: string, status?: PatientStatus): Patient[] => {
    return patients.filter(
      (patient) => 
        (patient.name.toLowerCase().includes(query.toLowerCase()) || 
         patient.identificationNumber.toLowerCase().includes(query.toLowerCase())) &&
        (!status || patient.status === status)
    );
  };

  const getPatientById = (id: string): Patient | undefined => {
    return patients.find(patient => patient.id === id);
  };

  const getDischargesByPatientId = (patientId: string): Discharge[] => {
    return discharges.filter(discharge => discharge.patientId === patientId);
  };

  const searchDischargesByPatient = (query: string): Discharge[] => {
    // Find patients matching the query
    const matchedPatients = patients.filter(
      patient => 
        patient.name.toLowerCase().includes(query.toLowerCase()) || 
        patient.identificationNumber.toLowerCase().includes(query.toLowerCase())
    );

    // Get the IDs of matched patients
    const patientIds = matchedPatients.map(patient => patient.id);

    // Filter discharges that belong to those patients
    return discharges.filter(discharge => patientIds.includes(discharge.patientId));
  };

  const dischargePatient = (id: string) => {
    setPatients(patients.map(patient => 
      patient.id === id 
        ? { ...patient, status: 'discharged' as PatientStatus, lastUpdate: new Date().toISOString().split('T')[0] } 
        : patient
    ));
  };

  const addDischarge = (discharge: Omit<Discharge, 'id'>) => {
    const newDischarge = {
      ...discharge,
      id: `${discharges.length + 1}`,
      date: new Date().toISOString().split('T')[0]
    };
    
    setDischarges([...discharges, newDischarge]);

    // Update patient status to inTreatment if they were active
    setPatients(patients.map(patient => 
      patient.id === discharge.patientId && patient.status === 'active'
        ? { ...patient, status: 'inTreatment' as PatientStatus, lastUpdate: new Date().toISOString().split('T')[0] } 
        : patient
    ));
  };

  return (
    <PatientContext.Provider value={{
      patients,
      discharges,
      searchPatients,
      getPatientById,
      getDischargesByPatientId,
      searchDischargesByPatient,
      dischargePatient,
      addDischarge
    }}>
      {children}
    </PatientContext.Provider>
  );
};

export const usePatients = () => {
  const context = useContext(PatientContext);
  if (context === undefined) {
    throw new Error('usePatients must be used within a PatientProvider');
  }
  return context;
};