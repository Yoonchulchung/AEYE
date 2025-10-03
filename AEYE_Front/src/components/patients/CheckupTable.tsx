"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { cn } from "@/lib/utils";
import { Checkup } from "@/types";
import Link from "next/link";

import { useRouter } from "next/navigation";
import { Dispatch, SetStateAction } from "react";

interface CheckupTableProps {
  checkups: Checkup[];
  activeId: Checkup["checkupId"];
  setActiveId: Dispatch<SetStateAction<Checkup["checkupId"]>>;
}

const CheckupTable = ({
  checkups,
  activeId,
  setActiveId,
}: CheckupTableProps) => {
  const router = useRouter();
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="text-left font-semibold">날짜</TableHead>
          <TableHead className="text-left font-semibold">증상</TableHead>
          <TableHead className="text-left font-semibold">심각도</TableHead>
          <TableHead className="text-left font-semibold">비고</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {checkups.map((checkup) => (
          <TableRow
            className={cn("cursor-pointer", {
              "bg-muted/50": activeId === checkup.checkupId,
            })}
            key={checkup.checkupId}
            onClick={() => {
              setActiveId(checkup.checkupId);
            }}
          >
            <TableCell className="font-medium">{checkup.date}</TableCell>
            <TableCell>{checkup.symptom}</TableCell>
            <TableCell className="">{checkup.status}</TableCell>
            <TableCell className="">
              <Link
                href={`/patients/${checkup.patientId}/checkups/${checkup.checkupId}`}
              >
                <span className="hover:underline hover:underline-offset-1">
                  상세보기
                </span>
              </Link>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
      <TableFooter>
        <TableRow>
          <TableCell colSpan={3}>Total</TableCell>
          <TableCell className="text-left">{checkups.length}</TableCell>
        </TableRow>
      </TableFooter>
    </Table>
  );
};

export default CheckupTable;
