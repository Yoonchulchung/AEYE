import PatientTable from "@/components/patients/PatientTable";
import React from "react";

const fetchPatients = async () => {
  const response = await fetch(`http://localhost:3000/api/patients`, {
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error("Failed to fetch patients");
  }
  return response.json();
};

const PatientPage = async () => {
  const patients = await fetchPatients();
  return (
    <main className="m-auto max-w-[1440px] px-8 pb-10">
      <PatientTable patients={patients} />
    </main>
  );
};

export default PatientPage;
