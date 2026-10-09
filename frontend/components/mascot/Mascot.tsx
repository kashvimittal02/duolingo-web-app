"use client";

import React from "react";
import Image from "next/image";

export type MascotExpression =
  | "happy"
  | "cheering"
  | "sad"
  | "sleeping"
  | "encouraging"
  | "concerned";

interface MascotProps {
  expression?: MascotExpression;
  size?: "sm" | "md" | "lg" | "xl";
  speechBubble?: string;
  bubblePosition?: "left" | "top";
  className?: string;
  interactive?: boolean;
}

export const Mascot: React.FC<MascotProps> = ({
  expression = "happy",
  size = "md",
  speechBubble,
  bubblePosition = "left",
  className = "",
  interactive = true,
}) => {
  // Normalize expression to the 4 canonical states matching reference image
  let normalizedExpr: "happy" | "cheering" | "sad" | "sleeping" = "happy";
  if (expression === "cheering" || expression === "encouraging") {
    normalizedExpr = "cheering";
  } else if (expression === "sad" || expression === "concerned") {
    normalizedExpr = "sad";
  } else if (expression === "sleeping") {
    normalizedExpr = "sleeping";
  } else {
    normalizedExpr = "happy";
  }

  const sizePixelMap = {
    sm: 64,
    md: 96,
    lg: 128,
    xl: 160,
  };

  const px = sizePixelMap[size];

  const isVertical = bubblePosition === "top";

  return (
    <div
      className={`inline-flex items-center gap-2.5 select-none ${
        isVertical ? "flex-col justify-center" : "flex-row justify-center"
      } ${className}`}
    >
      {/* Speech bubble if present */}
      {speechBubble && (
        <div
          className={`relative px-3 py-1.5 sm:px-3.5 sm:py-2 bg-white dark:bg-[#1a2c35] border-2 border-gray-200 dark:border-[#2b3a42] rounded-2xl shadow-sm text-xs sm:text-sm font-black text-gray-700 dark:text-gray-200 animate-fade-in ${
            isVertical ? "max-w-[200px] text-center mb-1.5" : "max-w-[180px] sm:max-w-xs"
          }`}
        >
          <span>{speechBubble}</span>
          {isVertical ? (
            /* Tail pointing DOWN towards mascot */
            <>
              <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-0 h-0 border-l-[6px] border-l-transparent border-r-[6px] border-r-transparent border-t-[8px] border-t-gray-200 dark:border-t-[#2b3a42]" />
              <div className="absolute -bottom-[6px] left-1/2 -translate-x-1/2 w-0 h-0 border-l-[5px] border-l-transparent border-r-[5px] border-r-transparent border-t-[6px] border-t-white dark:border-t-[#1a2c35]" />
            </>
          ) : (
            /* Tail pointing RIGHT towards mascot */
            <>
              <div className="absolute top-1/2 -right-2 -translate-y-1/2 w-0 h-0 border-t-[6px] border-t-transparent border-b-[6px] border-b-transparent border-l-[8px] border-l-gray-200 dark:border-l-[#2b3a42]" />
              <div className="absolute top-1/2 -right-[6px] -translate-y-1/2 w-0 h-0 border-t-[5px] border-t-transparent border-b-[5px] border-b-transparent border-l-[6px] border-l-white dark:border-l-[#1a2c35]" />
            </>
          )}
        </div>
      )}

      {/* Vector Mascot Graphic */}
      <div
        className={`relative shrink-0 transition-transform duration-200 ${
          interactive ? "hover:scale-105 active:scale-95 cursor-pointer" : ""
        }`}
        style={{ width: px, height: px }}
      >
        <Image
          src={`/images/mascot/mascot-${normalizedExpr}.svg`}
          alt={`Lingo Mascot - ${normalizedExpr}`}
          width={px}
          height={px}
          priority
          className="w-full h-full object-contain filter drop-shadow-md select-none pointer-events-none"
        />
      </div>
    </div>
  );
};
