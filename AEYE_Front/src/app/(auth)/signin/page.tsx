import SigninForm from "@/components/auth/SigninForm";
import Image from "next/image";
import React from "react";

const SigninPage = () => {
  return (
    <main className="flex h-full min-w-full">
      <section className="flex h-full flex-1 shrink-0 items-center justify-center">
        <SigninForm />
      </section>
      <section className="flex flex-1 shrink-0 items-center justify-center rounded-bl-[12.5rem] bg-[linear-gradient(135deg,_rgba(207,232,255,1)_0%,_rgba(255,255,255,1)_100%)]">
        <div className="flex flex-col items-center">
          <div className="relative mb-[32px] aspect-[276/65] w-[210px]">
            <Image src="/images/logo-compound-horizontal.png" alt="로고" fill />
          </div>
          <p className="text-xl font-semibold text-[#2B3674]">
            진료 데이터의 새로운 눈, AEYE
          </p>
          <div className="relative mt-[68px] aspect-[693.78/553.75] w-[450.78px]">
            <Image src="/images/docs.png" alt="랜딩 이미지" fill />
          </div>
        </div>
      </section>
    </main>
  );
};

export default SigninPage;
