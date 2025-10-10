"use client";

import { signout } from "@/actions/signout";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import useUser from "@/hooks/useUser";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { FormEventHandler } from "react";
import { toast } from "sonner";

const Avatar = () => {
  const router = useRouter();
  const user = useUser();
  if (!user) {
    toast.error("로그인 세션이 만료되었습니다. 다시 로그인해주세요.");
    router.replace("/signin");
    return null;
  }

  const onSignOut: FormEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();
    await signout();
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <div className="relative aspect-square w-[46px] cursor-pointer overflow-hidden rounded-full border">
          <Image
            src={user.profileImage}
            alt="아바타"
            className="object-cover"
            fill
          />
        </div>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-48">
        <DropdownMenuLabel>내 계정: {user.email}</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem asChild>
          <form onSubmit={onSignOut} className="w-full">
            <button className="flex w-full justify-between">
              로그아웃
              <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut>
            </button>
          </form>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

export default Avatar;
