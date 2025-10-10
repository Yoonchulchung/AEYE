"use client";

import React, { useState } from "react";
import ImageUploader from "./ImageUploader";
import { Button } from "../ui/button";
import AIDiagnosis from "./AIDiagnosis";
import { MultiStepLoader as Loader } from "../ui/multi-step-loader";
import { Checkup } from "@/types";
import { Report } from "@/types";
import Image from "next/image";

const loadingStates = [
  {
    text: "AI 서버에 연결중이에요...",
  },
  {
    text: "사진을 분석중이에요...",
  },
  {
    text: "사진을 토대로 진단을 내리는 중이에요...",
  },
  {
    text: "거의 다 왔어요..!",
  },
  {
    text: "AI 진단이 완료되었어요!",
  },
];
interface PatientReportProps {
  checkup: Checkup;
}

function getRandomDiagnosis() {
  const diagnoses: Report[] = [
    { diagnosis: "Glaucoma", probability: "85%" },
    { diagnosis: "Diabetic Retinopathy", probability: "78%" },
    { diagnosis: "Retinal Detachment", probability: "92%" },
    { diagnosis: "Cataract", probability: "88%" },
    { diagnosis: "Conjunctivitis", probability: "70%" },
    { diagnosis: "Keratoconus", probability: "80%" },
    { diagnosis: "Dry Eye Syndrome", probability: "75%" },
    { diagnosis: "Uveitis", probability: "82%" },
    { diagnosis: "Optic Neuritis", probability: "65%" },
    { diagnosis: "Age-Related Macular Degeneration (AMD)", probability: "90%" },
    { diagnosis: "Central Serous Retinopathy", probability: "76%" },
    { diagnosis: "Myopia", probability: "60%" },
    { diagnosis: "Hyperopia", probability: "62%" },
    { diagnosis: "Astigmatism", probability: "74%" },
    { diagnosis: "Retinitis Pigmentosa", probability: "68%" },
  ];

  const randomIndex = Math.floor(Math.random() * diagnoses.length);
  return diagnoses[randomIndex];
}

const PatientReport = ({ checkup }: PatientReportProps) => {
  const [newReport, setNewReport] = useState<{
    diagnosis: string;
    probability: string;
  } | null>(null);
  const [isLoading, setLoading] = useState(false);

  /**
   * @description 5초의 로딩 후 AI 진단을 내리는 목 서버 역할 함수
   */
  const mockServerLoading = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
    }, 5000);
    setTimeout(() => {
      const newReport = getRandomDiagnosis();
      setNewReport(newReport);
    }, 5000);
  };

  const handleClickStartDiagnosis = () => {
    /** @TODO imageUploader에서 업로드한 이미지 2장을 가지고 서버에 보내서 AI newReport를 받아온다. */
    mockServerLoading();
  };

  return (
    <>
      <div className="flex w-full gap-5">
        <ImageUploader initialSrc={checkup.ultrasoundImages[0]} />
        <ImageUploader initialSrc={checkup.ultrasoundImages[0]} />
      </div>
      <div className="h-10" />
      <Button onClick={handleClickStartDiagnosis}>
        <div className="flex items-center gap-2">
          <Image src="/images/ai.png" width={16} height={16} alt="ai 아이콘" />
          <p>AI 진단 시작하기</p>
        </div>
      </Button>
      <div className="h-10" />
      <div className="rounded-lg border p-10">
        <AIDiagnosis initialReport={checkup.report.ai} newReport={newReport} />
        <br />
        <h3 className="text-lg font-semibold text-gray-800">
          {"Doctor's Diagnosis: "}
        </h3>
        <p className="text-gray-600">{checkup?.report.doctor.diagnosis}</p>
      </div>
      <Loader
        loadingStates={loadingStates}
        loading={isLoading}
        duration={1000}
      />
    </>
  );
};

export default PatientReport;
