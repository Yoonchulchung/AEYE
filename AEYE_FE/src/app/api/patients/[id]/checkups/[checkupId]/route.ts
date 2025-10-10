import { NextRequest, NextResponse } from "next/server";
import patients from "@/database/patients.json";

export async function GET(req: NextRequest) {
  const { pathname } = new URL(req.url);
  const pathParts = pathname.split("/");
  const checkupId = pathParts.pop(); // 마지막 부분은 checkupId
  pathParts.pop(); // 'checkups' 경로 부분 제거
  const patientId = pathParts.pop(); // 그 이전 부분은 patientId

  if (!patientId || !checkupId) {
    return NextResponse.json(
      { error: "Patient ID and Checkup ID are required" },
      { status: 400 }
    );
  }

  // 해당 환자 찾기
  const patient = patients.find((p) => p.id === parseInt(patientId, 10));

  if (!patient) {
    return NextResponse.json({ error: "Patient not found" }, { status: 404 });
  }

  // 해당 진료 기록 찾기
  const checkup = patient.checkups.find(
    (c) => c.checkupId === parseInt(checkupId, 10)
  );

  if (!checkup) {
    return NextResponse.json({ error: "Checkup not found" }, { status: 404 });
  }

  return NextResponse.json(checkup);
}
