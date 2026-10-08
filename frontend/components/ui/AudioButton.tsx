"use client";

import React, { useState } from "react";
import { Volume2 } from "lucide-react";
import { speakSpanish } from "@/lib/audio";

interface AudioButtonProps {
  text: string;
  size?: "sm" | "md" | "lg";
  className?: string;
  label?: string;
}

export const AudioButton: React.FC<AudioButtonProps> = ({
  text,
  size = "md",
  className = "",
  label,
}) => {
  const [isPlaying, setIsPlaying] = useState(false);

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    e.preventDefault();
    setIsPlaying(true);
    speakSpanish(text);
    setTimeout(() => {
      setIsPlaying(false);
    }, 1200);
  };

  // Dimensions based on size prop
  const sizeClasses = {
    sm: "w-8 h-8 min-w-[32px]",
    md: "w-10 h-10 min-w-[40px]",
    lg: "w-12 h-12 min-w-[48px]",
  }[size];

  const iconSizes = {
    sm: "w-4 h-4",
    md: "w-5 h-5",
    lg: "w-6 h-6",
  }[size];

  const accessibleLabel = label || `Pronounce "${text}" in Spanish`;

  return (
    <button
      type="button"
      onClick={handleClick}
      aria-label={accessibleLabel}
      title={accessibleLabel}
      className={`
        inline-flex items-center justify-center rounded-2xl border-2 transition-all duration-150 select-none
        ${sizeClasses}
        ${
          isPlaying
            ? "bg-duo-blue-light dark:bg-[#1b3a4b] border-duo-blue text-duo-blue dark:text-[#38bdf8] scale-105 shadow-none"
            : "bg-white dark:bg-[#202f36] border-blue-200 dark:border-[#2c5a73] text-duo-blue dark:text-[#38bdf8] hover:bg-blue-50 dark:hover:bg-[#1b3a4b] hover:border-blue-300 dark:hover:border-[#38bdf8] shadow-[0_2px_0_0_#93c5fd] dark:shadow-[0_2px_0_0_#182329] active:translate-y-[2px] active:shadow-none"
        }
        ${className}
      `}
    >
      <Volume2
        className={`${iconSizes} transition-transform ${
          isPlaying ? "scale-110" : ""
        }`}
      />
    </button>
  );
};
