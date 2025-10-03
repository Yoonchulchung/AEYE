import localFont from "next/font/local";

const Pretendard = localFont({
  src: [
    {
      path: "../../public/fonts/PretendardVariable.woff2",
    },
  ],
  display: "swap",
  variable: "--font-pretendard",
});

export default Pretendard;
