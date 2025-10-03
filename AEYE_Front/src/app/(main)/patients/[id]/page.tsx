import { Patient } from "@/types";
import { notFound } from "next/navigation";
import Image from "next/image";
import CheckupList from "@/components/patients/CheckupList";
import { type Metadata } from "next";

export async function generateStaticParams() { 

  if (process.env.NODE_ENV === "production") {
    return [];
  }

  try {
    const patients: Patient[] = await fetch("http://localhost:3000/api/patients")
      .then((res) => {
        if (!res.ok) {
          throw new Error('Failed to fetch');
        }
        return res.json();  // 여기에서 반환된 JSON 데이터를 반환
      });

    return patients.map((patient) => ({
      id: patient.id.toString(),
    }));

  } catch (error) {
    console.error("Error fetching patients:", error);
    // 에러가 발생할 경우 빈 배열을 반환
    return [];
  }
}
  

const fetchPatientById = async (id: string): Promise<Patient | null> => {
  const res = await fetch(`http://localhost:3000/api/patients/${id}`);
  if (!res.ok) {
    return null;
  }
  return res.json();
};

// Metadata를 동적으로 생성
export async function generateMetadata({
  params,
}: {
  params: { id: string };
}): Promise<Metadata> {
  const patient = await fetchPatientById(params.id);
  return {
    title: patient ? `${patient.name} - 대시보드` : "404",
    description: "진료 데이터의 새로운 눈, AEYE",
  };
}

const PatientDetailPage = async ({ params }: { params: { id: string } }) => {
  const patient = await fetchPatientById(params.id);

  if (!patient) {
    notFound();
  }
  return (
    <main className="m-auto max-w-[1440px] px-8 pb-10">
      <section>
        <h1 className="mb-12 text-3xl font-semibold">{`${patient.name} 님의 진료 기록`}</h1>
        <div className="flex h-40 w-full gap-10 rounded-xl border p-5">
          <div className="relative size-28 overflow-hidden rounded-full">
            <Image
              src={patient.profileImage}
              alt="환자 사진"
              fill
              className="object-cover"
            />
          </div>
          <div className="flex h-full flex-col justify-start gap-1">
            <h2 className="mt-2 text-xl font-semibold text-gray-600">
              {patient.name}
            </h2>
            <p className="text-gray-400">{patient.DOB}</p>
            <p className="text-gray-400">{`${patient.numberOfVisits}번째 내원`}</p>
          </div>
          <p className="ml-40 self-center text-right text-lg">
            {patient.status}
          </p>
        </div>
      </section>
      <div className="h-20" />
      <section>
        <h2 className="mb-8 text-xl">날짜별 진료기록</h2>
        <CheckupList checkups={patient.checkups} />
      </section>
    </main>
  );
};

export default PatientDetailPage;
