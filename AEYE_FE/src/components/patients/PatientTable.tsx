"use client";

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Patient } from "@/types";
import Image from "next/image";
import { useRouter } from "next/navigation";

interface PatientTableProps {
  patients: Patient[];
}

const PatientTable = ({ patients }: PatientTableProps) => {
  const router = useRouter();
  return (
    <Table>
      <TableCaption>2024.06.01 ~ 2024.06.30 환자 리스트</TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead className="w-[100px]"></TableHead>
          <TableHead className="text-left font-semibold">이름</TableHead>
          <TableHead className="text-center font-semibold">
            최근 진료 날짜
          </TableHead>
          <TableHead className="text-center font-semibold">
            치료 진척도
          </TableHead>
          <TableHead className="text-right font-semibold">위험군</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {patients.map((patient) => (
          <TableRow
            className="cursor-pointer"
            key={patient.id}
            onClick={() => {
              router.push(`/patients/${patient.id}`);
            }}
          >
            <TableCell className="font-medium">
              <div className="relative size-10 overflow-hidden rounded-full">
                <Image
                  src={patient.profileImage}
                  alt="환자 사진"
                  fill
                  className="object-cover"
                />
              </div>
            </TableCell>
            <TableCell>
              {patient.name}
              <p className="text-sm text-gray-400">{patient.DOB}</p>
              <p className="text-sm text-gray-400">{`${patient.numberOfVisits}번째 내원`}</p>
              <p className="text-sm text-gray-400">{patient.symptom}</p>
            </TableCell>
            <TableCell className="text-center">
              {patient.recentVisitDate}
            </TableCell>
            <TableCell className="text-center">
              {patient.severityPercentage}
            </TableCell>
            <TableCell className="text-right">{patient.status}</TableCell>
          </TableRow>
        ))}
      </TableBody>
      <TableFooter>
        <TableRow>
          <TableCell colSpan={4}>Total</TableCell>
          <TableCell className="text-right">{patients.length}</TableCell>
        </TableRow>
      </TableFooter>
    </Table>
  );
};

export default PatientTable;
