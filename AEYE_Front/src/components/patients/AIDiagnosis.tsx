"use client";

import React from "react";
import { TextGenerateEffect } from "@/components/ui/text-generate-effect";
import { Report } from "@/types";

interface AIDiagnosisProps {
  initialReport?: Report;
  newReport: Report | null;
}

const AIDiagnosis = ({ initialReport, newReport }: AIDiagnosisProps) => {
  if (!initialReport) {
    return <p className="text-gray-600">{"AI 진단 기록이 아직 없습니다."}</p>;
  }

  if (initialReport && newReport === null) {
    return (
      <>
        <h3 className="text-lg font-semibold text-gray-800">{"AI Report: "}</h3>
        <p className="text-gray-600">
          {"Diagnosis: " + initialReport.diagnosis}
        </p>
        <p className="text-gray-600">
          {"Probability: " + initialReport.probability}
        </p>
      </>
    );
  } else if (newReport !== null) {
    return (
      <>
        <h3 className="text-lg font-semibold text-gray-800">{"AI Report: "}</h3>
        <TextGenerateEffect words={"Diagnosis: " + newReport.diagnosis} />
        <TextGenerateEffect words={"Probability: " + newReport.probability} />
      </>
    );
  } else return null;
};

export default AIDiagnosis;
