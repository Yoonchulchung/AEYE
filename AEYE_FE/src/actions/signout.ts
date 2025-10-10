"use server";

import { cookies } from "next/headers";

export const signout = async () => {
  cookies().delete("AEYE_CU");
  cookies().delete("AEYE_PI");
};
