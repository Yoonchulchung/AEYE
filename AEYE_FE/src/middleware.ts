import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const protectedRoutes = ["/patients"];
const users = ["test@test.com", "mole@naver.com"];
export function middleware(request: NextRequest) {
  const isLoggedIn = !!cookies().get("AEYE_CU")?.value;
  const isProtected = protectedRoutes.includes(request.nextUrl.pathname);

  if (!isLoggedIn && isProtected) {
    console.log("redireting to signin page");
    return NextResponse.redirect("http://localhost:3000/signin");
  }

  if (request.nextUrl.pathname === "/") {
    const url = request.nextUrl.clone();
    url.pathname = "/patients";
    return NextResponse.redirect(url);
  } else NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|.*\\.png$).*)"],
};
