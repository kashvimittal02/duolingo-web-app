"use client";

import React from "react";
import { Mascot, MascotExpression } from "./Mascot";

export type { MascotExpression };

interface LingoMascotProps {
  expression?: MascotExpression;
  size?: "sm" | "md" | "lg" | "xl";
  speechBubble?: string;
  bubblePosition?: "left" | "top";
  className?: string;
}

export const LingoMascot: React.FC<LingoMascotProps> = ({
  expression = "happy",
  size = "md",
  speechBubble,
  bubblePosition = "left",
  className = "",
}) => {
  return (
    <Mascot
      expression={expression}
      size={size}
      speechBubble={speechBubble}
      bubblePosition={bubblePosition}
      className={className}
    />
  );
};
