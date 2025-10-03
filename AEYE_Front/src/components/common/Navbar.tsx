import Image from "next/image";
import Link from "next/link";
import React from "react";

import Avatar from "./Avatar";

const Navbar = () => {
  return (
    <header className="m-auto w-full">
      <nav className="m-auto flex w-full max-w-[1440px] items-center justify-between px-8 py-5">
        <div className="relative aspect-[276/65] w-[100px] cursor-pointer">
          <Link href="/patients">
            <Image src="/images/logo-compound-horizontal.png" alt="로고" fill />
          </Link>
        </div>
        <Avatar />
      </nav>
    </header>
  );
};

export default Navbar;
