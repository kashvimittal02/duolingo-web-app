"use client";

import React from "react";
import Image from "next/image";

export type RewardType =
  | "chest-closed"
  | "chest-open"
  | "gem"
  | "star"
  | "trophy"
  | "fire"
  | "heart";

interface RewardIconProps {
  name: RewardType;
  size?: "sm" | "md" | "lg" | "xl" | number;
  className?: string;
  animate?: boolean;
}

export const RewardIcon: React.FC<RewardIconProps> = ({
  name,
  size = "md",
  className = "",
  animate = false,
}) => {
  const sizeMap: Record<string, number> = {
    sm: 24,
    md: 36,
    lg: 48,
    xl: 64,
  };

  const dim = typeof size === "number" ? size : sizeMap[size] || 36;

  return (
    <div
      className={`relative inline-flex items-center justify-center shrink-0 select-none ${
        animate ? "hover:scale-110 active:scale-95 transition-transform" : ""
      } ${className}`}
      style={{ width: dim, height: dim }}
    >
      <Image
        src={`/images/rewards/${name}.svg`}
        alt={`Reward: ${name}`}
        width={dim}
        height={dim}
        className="w-full h-full object-contain pointer-events-none drop-shadow-sm"
      />
    </div>
  );
};
