"use client";

import React from "react";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { signin } from "@/actions/signin";
import { SigninSchema } from "@/types";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

const SigninForm = () => {
  const router = useRouter();
  return (
    <div className="flex w-fit min-w-[410px] flex-col gap-[3.875rem]">
      <div className="flex flex-col">
        <h1 className="text-4xl font-semibold leading-[56px] tracking-tight text-[#2B3674]">
          Sign In
        </h1>
        <p className="text-base text-[#A3AED0]">
          이메일과 비밀번호를 입력하여 로그인하세요.
        </p>
      </div>
      <form
        className="w-full"
        action={async (formData: FormData) => {
          const email = formData.get("email");
          const password = formData.get("password");

          const res = await signin({ email, password } as SigninSchema);
          if (res.error) {
            toast.error(res.error, { richColors: true });
            return;
          } else router.push("/");
        }}
      >
        <Label
          htmlFor="email"
          className="mb-[12px] inline-block text-sm tracking-tight text-[#2B3674]"
        >
          Email*
        </Label>
        <Input
          id="email"
          name="email"
          className="h-[50px] rounded-2xl border-[#E0E5F2] px-6 py-4 text-sm placeholder:text-[#A3AED0] focus-visible:border-primary focus-visible:ring-0"
          type="email"
          placeholder="mail@simmmple.com"
        />
        <div className="h-6" />
        <Label
          htmlFor="password"
          className="mb-[12px] inline-block text-sm tracking-tight text-[#2B3674]"
        >
          Password*
        </Label>
        <Input
          id="password"
          name="password"
          className="h-[50px] rounded-2xl border-[#E0E5F2] px-6 py-4 text-sm placeholder:text-[#A3AED0] focus-visible:border-primary focus-visible:ring-0"
          type="password"
          placeholder="Min. 8 characters"
        />
        <div className="h-6" />
        <Button className="h-[54px] w-full bg-[#FF776F] hover:bg-[#fa6860]">
          로그인
        </Button>
      </form>
    </div>
  );
};

export default SigninForm;
