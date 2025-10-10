import { NextRequest, NextResponse } from "next/server";
import patients from "@/database/patients.json";
import { Patient } from "@/types";

export async function GET(req: NextRequest): Promise<NextResponse<Patient[]>> {
  try {
    return NextResponse.json(patients as Patient[]);
  } catch (error) {
    console.error(
      "환자 데이터 리스트를 불러오는 도중 에러가 발생했습니다. :",
      error
    );
    return NextResponse.json(
      { error: "환자 데이터 리스트를 불러오는 도중 에러가 발생했습니다" },
      { status: 500 }
    ) as unknown as NextResponse<Patient[]>;
  }
}
