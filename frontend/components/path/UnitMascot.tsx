"use client";

import React from "react";
import Image from "next/image";

interface UnitMascotProps {
  orderIndex: number;
  isUnlocked: boolean;
  isCompleted: boolean;
  side?: "left" | "right";
  className?: string;
}

export const UnitMascot: React.FC<UnitMascotProps> = ({
  orderIndex,
  isUnlocked,
  isCompleted,
  side,
  className = "",
}) => {
  // Units alternate sides: odd units on right, even units on left
  const resolvedSide: "left" | "right" =
    side || ([1, 3, 5, 8].includes(orderIndex) ? "right" : "left");

  // Determine character pose per unit and completion status
  const getAsset = (): { src: string; alt: string; flip: boolean } => {
    // Completed units: full colour celebratory pose (mascot-cheering.svg)
    if (isCompleted) {
      return {
        src: "/images/mascot/mascot-cheering.svg",
        alt: `Unit ${orderIndex} Mastered - Cheering Mascot`,
        flip: resolvedSide === "left",
      };
    }

    // Different appropriate character expressions per unit
    switch (orderIndex % 4) {
      case 1:
        // Unit 1 / Unit 5: Classic happy mascot
        return {
          src: "/images/mascot/mascot-happy.svg",
          alt: `Unit ${orderIndex} Mascot - Happy`,
          flip: resolvedSide === "left",
        };
      case 2:
        // Unit 2: Cheering mascot
        return {
          src: "/images/mascot/mascot-cheering.svg",
          alt: `Unit ${orderIndex} Mascot - Cheering`,
          flip: resolvedSide === "left",
        };
      case 3:
        // Unit 3 / Unit 7: Happy mascot facing inwards
        return {
          src: "/images/mascot/mascot-happy.svg",
          alt: `Unit ${orderIndex} Mascot - Learning`,
          flip: resolvedSide === "left",
        };
      case 0:
      default:
        // Unit 4 / Unit 8: Cozy resting mascot
        return {
          src: "/images/mascot/mascot-sleeping.svg",
          alt: `Unit ${orderIndex} Mascot - Resting`,
          flip: resolvedSide === "left",
        };
    }
  };

  const asset = getAsset();

  // Positioning:
  // Placed beside the path node row on the alternating open side
  const positionClass =
    resolvedSide === "right"
      ? "right-2 sm:right-6 lg:right-10"
      : "left-2 sm:left-6 lg:left-10";

  return (
    <aside
      aria-hidden="true"
      className={`absolute ${positionClass} top-1/2 -translate-y-1/2 z-10 pointer-events-none select-none flex flex-col items-center ${className}`}
    >
      {/* Mascot Graphic with bobbing animation only when unlocked */}
      <div
        className={`relative ${
          isUnlocked ? "animate-mascot-idle" : ""
        } ${asset.flip ? "scale-x-[-1]" : ""}`}
      >
        <div
          className={`relative w-[68px] h-[68px] sm:w-[88px] sm:h-[88px] transition-all duration-300 ${
            !isUnlocked
              ? "grayscale brightness-[0.65] dark:brightness-[0.38] contrast-[0.85] opacity-40 dark:opacity-45"
              : "filter drop-shadow-md"
          }`}
        >
          <Image
            src={asset.src}
            alt={asset.alt}
            width={88}
            height={88}
            priority={orderIndex <= 2}
            className="w-full h-full object-contain pointer-events-none select-none"
          />
        </div>
      </div>

      {/* Ground Shadow matching reference styling */}
      <div
        className={`w-14 sm:w-18 h-3 rounded-full mx-auto -mt-2 transition-all duration-300 ${
          !isUnlocked
            ? "bg-black/10 dark:bg-black/25 blur-[1px]"
            : "bg-black/15 dark:bg-black/35 blur-[0.5px]"
        }`}
      />
    </aside>
  );
};
