"use client";

import { Checkup } from "@/types";
import React, { useState } from "react";
import CheckupTable from "./CheckupTable";
import Image from "next/image";

interface CheckupListProps {
  checkups: Checkup[];
}

const CheckupList = ({ checkups }: CheckupListProps) => {
  const [activeId, setActiveId] = useState(checkups[0].checkupId);
  const activeCheckup = checkups.find(
    (checkup) => checkup.checkupId === activeId
  );
  return (
    <div className="flex flex-col gap-10">
      <div className="flex gap-20">
        <div className="flex-1">
          <CheckupTable
            checkups={checkups}
            activeId={activeId}
            setActiveId={setActiveId}
          />
        </div>
        <div className="flex flex-1 gap-4">
          <div className="relative aspect-square size-48 overflow-hidden rounded-md">
            <Image
              src={activeCheckup?.ultrasoundImages[0] ?? ""}
              alt="환자 초음파 사진1"
              fill
              className="object-cover"
            />
          </div>
          <div className="relative aspect-square size-48 overflow-hidden rounded-md">
            <Image
              src={activeCheckup?.ultrasoundImages[1] ?? ""}
              alt="환자 초음파 사진2"
              fill
              className="object-cover"
            />
          </div>
        </div>
      </div>
      <div className="rounded-lg border p-10">
        <h3 className="text-gray-600">
          {"AI Diagnosis: " + activeCheckup?.report.ai.diagnosis}
        </h3>
        <p className="text-gray-600">
          {"Probability: " + activeCheckup?.report.ai.probability}
        </p>
        <br />
        <h3 className="text-gray-600">
          {"Doctor's Diagnosis: " + activeCheckup?.report.doctor.diagnosis}
        </h3>
      </div>
    </div>
  );
};

export default CheckupList;
