import type { Metadata } from "next";
import Pretendard from "@/styles/local-font";

import "@/styles/globals.css";
import Navbar from "@/components/common/Navbar";
import { CookiesProvider } from "next-client-cookies/server";

export const metadata: Metadata = {
  title: "AEYE",
  description: "진료 데이터의 새로운 눈, AEYE",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className={Pretendard.className}>
        <CookiesProvider>
          <Navbar />
          {children}
        </CookiesProvider>
      </body>
    </html>
  );
}
