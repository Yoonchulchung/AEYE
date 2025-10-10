"use client";

import React, { ChangeEvent, useRef, useState } from "react";
import Image from "next/image";

interface ImageUploaderProps {
  initialSrc?: string;
}

const ImageUploader = ({ initialSrc }: ImageUploaderProps) => {
  const [imageSrc, setImageSrc] = useState(initialSrc);
  const fileRef = useRef<HTMLInputElement>(null);
  const handleClickImage = () => {
    if (fileRef.current) {
      fileRef.current.click();
    }
  };

  const handleChangeFile = (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    const file = files?.[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setImageSrc(url);
    }
  };

  return (
    <>
      <div
        onClick={handleClickImage}
        className="relative aspect-square max-w-48 flex-1 cursor-pointer overflow-hidden rounded-xl after:absolute after:inset-0 after:flex after:size-full after:items-center  after:justify-center after:bg-black after:text-white after:opacity-0 after:transition-all after:content-['이미지_업로드'] hover:after:z-10 hover:after:opacity-80"
      >
        <Image
          src={imageSrc ?? ""}
          alt="환자 사진"
          fill
          className="object-cover"
        />
      </div>
      <input
        type="file"
        className="hidden size-0"
        ref={fileRef}
        accept="image/*"
        onChange={handleChangeFile}
      />
    </>
  );
};

export default ImageUploader;
