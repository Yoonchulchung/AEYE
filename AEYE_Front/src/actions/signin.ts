"use server";

import users from "@/database/users.json";
import { SigninSchema } from "@/types";
import { cookies } from "next/headers";

export const signin = async (values: SigninSchema) => {
  // JSON 파일에서 사용자 정보 가져오기
  const user = users.find((user) => user.email === values.email);

  // 이메일 확인
  if (!user) {
    return { error: "가입되어 있지 않은 메일입니다." };
  }

  // 비밀번호 확인
  if (user.password !== values.password) {
    return { error: "올바르지 않은 비밀번호입니다." };
  }

  // 로그인 성공 시 쿠키 설정
  cookies().set("AEYE_CU", user.email);
  cookies().set("AEYE_PI", user.profileImage);
  return { success: "성공적으로 로그인 되었습니다!" };
};
