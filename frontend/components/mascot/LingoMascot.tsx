"use client";

import React from "react";

export type MascotExpression = "happy" | "cheering" | "sad" | "sleeping";

interface LingoMascotProps {
  expression?: MascotExpression;
  size?: "sm" | "md" | "lg" | "xl";
  speechBubble?: string;
  className?: string;
}

export const LingoMascot: React.FC<LingoMascotProps> = ({
  expression = "happy",
  size = "md",
  speechBubble,
  className = "",
}) => {
  const sizeMap = {
    sm: "w-16 h-16",
    md: "w-24 h-24",
    lg: "w-32 h-32",
    xl: "w-40 h-40",
  };

  const dimensionMap = {
    sm: 64,
    md: 96,
    lg: 128,
    xl: 160,
  };

  const dim = dimensionMap[size];

  return (
    <div className={`inline-flex items-center gap-3 select-none ${className}`}>
      {/* Speech bubble if present */}
      {speechBubble && (
        <div className="relative px-3.5 py-2 bg-white dark:bg-[#1a2c35] border-2 border-gray-200 dark:border-[#2b3a42] rounded-2xl shadow-sm text-sm font-extrabold text-gray-700 dark:text-gray-200 animate-fade-in">
          <span>{speechBubble}</span>
          {/* Bubble tail pointing right towards mascot */}
          <div className="absolute top-1/2 -right-2 -translate-y-1/2 w-0 h-0 border-t-[6px] border-t-transparent border-b-[6px] border-b-transparent border-l-[8px] border-l-gray-200 dark:border-l-[#2b3a42]" />
          <div className="absolute top-1/2 -right-[6px] -translate-y-1/2 w-0 h-0 border-t-[5px] border-t-transparent border-b-[5px] border-b-transparent border-l-[6px] border-l-white dark:border-l-[#1a2c35]" />
        </div>
      )}

      {/* SVG Mascot Character - "Pepito" the Green Language Critter */}
      <div className={`relative ${sizeMap[size]} shrink-0 transition-transform duration-200 hover:scale-105`}>
        <svg
          viewBox="0 0 120 120"
          width={dim}
          height={dim}
          className="w-full h-full drop-shadow-md"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Shadow underneath */}
          <ellipse cx="60" cy="112" rx="36" ry="6" fill="#000000" fillOpacity="0.12" />

          {/* Ears */}
          {/* Left Ear */}
          <path
            d={
              expression === "sad"
                ? "M 32 46 Q 16 60 12 70 Q 24 66 38 56 Z" // Drooped
                : "M 28 50 Q 16 14 36 22 Q 44 32 46 48 Z" // Perky
            }
            fill="#58cc02"
            stroke="#46a302"
            strokeWidth="3.5"
            strokeLinejoin="round"
          />
          {/* Left Inner Ear */}
          <path
            d={
              expression === "sad"
                ? "M 30 50 Q 20 62 18 68 Q 24 65 34 56 Z"
                : "M 30 46 Q 22 22 36 28 Q 40 36 42 46 Z"
            }
            fill="#ffb3ba"
          />

          {/* Right Ear */}
          <path
            d={
              expression === "sad"
                ? "M 88 46 Q 104 60 108 70 Q 96 66 82 56 Z" // Drooped
                : "M 92 50 Q 104 14 84 22 Q 76 32 74 48 Z" // Perky
            }
            fill="#58cc02"
            stroke="#46a302"
            strokeWidth="3.5"
            strokeLinejoin="round"
          />
          {/* Right Inner Ear */}
          <path
            d={
              expression === "sad"
                ? "M 90 50 Q 100 62 102 68 Q 96 65 86 56 Z"
                : "M 90 46 Q 98 22 84 28 Q 80 36 78 46 Z"
            }
            fill="#ffb3ba"
          />

          {/* Head & Body Base */}
          <rect
            x="24"
            y="32"
            width="72"
            height="72"
            rx="36"
            fill="#58cc02"
            stroke="#46a302"
            strokeWidth="4"
          />

          {/* Cheeks / Belly patch (pale soft cream/mint) */}
          <ellipse cx="60" cy="74" rx="26" ry="22" fill="#e5f9db" />

          {/* Cute Rosy Cheek Blush */}
          <ellipse cx="36" cy="68" rx="5" ry="3.5" fill="#ff9aa2" opacity="0.75" />
          <ellipse cx="84" cy="68" rx="5" ry="3.5" fill="#ff9aa2" opacity="0.75" />

          {/* EXPRESSION SPECIFIC DETAILS */}

          {/* 1. HAPPY */}
          {expression === "happy" && (
            <g>
              {/* Left Eye: Curved smiling arc */}
              <path
                d="M 40 56 Q 46 50 52 56"
                stroke="#1e3a12"
                strokeWidth="4"
                strokeLinecap="round"
                fill="none"
              />
              {/* Right Eye: Curved smiling arc */}
              <path
                d="M 68 56 Q 74 50 80 56"
                stroke="#1e3a12"
                strokeWidth="4"
                strokeLinecap="round"
                fill="none"
              />
              {/* Cute little button nose */}
              <ellipse cx="60" cy="63" rx="3.5" ry="2.5" fill="#1e3a12" />
              {/* Wide content smile */}
              <path
                d="M 52 68 Q 60 76 68 68"
                stroke="#1e3a12"
                strokeWidth="3.5"
                strokeLinecap="round"
                fill="none"
              />
            </g>
          )}

          {/* 2. CHEERING */}
          {expression === "cheering" && (
            <g>
              {/* Sparkling star-eyes or celebratory round eyes */}
              <circle cx="46" cy="54" r="6" fill="#1e3a12" />
              <circle cx="44" cy="52" r="2.2" fill="#ffffff" />
              <circle cx="48" cy="55" r="1.2" fill="#ffffff" />

              <circle cx="74" cy="54" r="6" fill="#1e3a12" />
              <circle cx="72" cy="52" r="2.2" fill="#ffffff" />
              <circle cx="76" cy="55" r="1.2" fill="#ffffff" />

              {/* Nose */}
              <ellipse cx="60" cy="61" rx="3.5" ry="2.5" fill="#1e3a12" />
              {/* Big open happy mouth */}
              <path
                d="M 52 66 Q 60 80 68 66 Z"
                fill="#d82c20"
                stroke="#1e3a12"
                strokeWidth="2.5"
                strokeLinejoin="round"
              />
              <path d="M 55 72 Q 60 77 65 72" fill="#ff8da1" />

              {/* Raised celebrating paws */}
              <ellipse cx="22" cy="46" rx="6" ry="8" fill="#58cc02" stroke="#46a302" strokeWidth="2.5" />
              <ellipse cx="98" cy="46" rx="6" ry="8" fill="#58cc02" stroke="#46a302" strokeWidth="2.5" />

              {/* Sparkles / Stars around */}
              <path d="M 16 28 L 18 33 L 23 35 L 18 37 L 16 42 L 14 37 L 9 35 L 14 33 Z" fill="#ffc800" />
              <path d="M 104 28 L 106 33 L 111 35 L 106 37 L 104 42 L 102 37 L 97 35 L 102 33 Z" fill="#ffc800" />
            </g>
          )}

          {/* 3. SAD */}
          {expression === "sad" && (
            <g>
              {/* Drooped sorrowful eyebrows */}
              <path d="M 40 48 Q 46 52 52 50" stroke="#1e3a12" strokeWidth="2.5" strokeLinecap="round" />
              <path d="M 68 50 Q 74 52 80 48" stroke="#1e3a12" strokeWidth="2.5" strokeLinecap="round" />

              {/* Big glossy tearful eyes */}
              <circle cx="46" cy="58" r="5" fill="#1e3a12" />
              <circle cx="44.5" cy="56" r="2" fill="#ffffff" />

              <circle cx="74" cy="58" r="5" fill="#1e3a12" />
              <circle cx="72.5" cy="56" r="2" fill="#ffffff" />

              {/* Tear drop on right cheek */}
              <path
                d="M 83 66 C 83 64 86 61 86 61 C 86 61 89 64 89 66 C 89 68 87.5 69.5 86 69.5 C 84.5 69.5 83 68 83 66 Z"
                fill="#2b70c9"
              />

              {/* Nose */}
              <ellipse cx="60" cy="65" rx="3.5" ry="2.5" fill="#1e3a12" />
              {/* Gentle frown */}
              <path
                d="M 54 74 Q 60 69 66 74"
                stroke="#1e3a12"
                strokeWidth="3.5"
                strokeLinecap="round"
                fill="none"
              />
            </g>
          )}

          {/* 4. SLEEPING */}
          {expression === "sleeping" && (
            <g>
              {/* Peaceful closed resting eyes */}
              <path
                d="M 40 57 Q 46 62 52 57"
                stroke="#1e3a12"
                strokeWidth="3.5"
                strokeLinecap="round"
                fill="none"
              />
              <path
                d="M 68 57 Q 74 62 80 57"
                stroke="#1e3a12"
                strokeWidth="3.5"
                strokeLinecap="round"
                fill="none"
              />

              {/* Nose */}
              <ellipse cx="60" cy="64" rx="3.5" ry="2.5" fill="#1e3a12" />
              {/* Sweet calm little smile */}
              <path
                d="M 56 70 Q 60 73 64 70"
                stroke="#1e3a12"
                strokeWidth="2.5"
                strokeLinecap="round"
                fill="none"
              />

              {/* Floating "Z z z" bubbles */}
              <text x="84" y="34" fill="#1cb0f6" fontSize="12" fontWeight="900" fontFamily="sans-serif">
                Z
              </text>
              <text x="96" y="24" fill="#1cb0f6" fontSize="10" fontWeight="900" fontFamily="sans-serif">
                z
              </text>
              <text x="105" y="15" fill="#1cb0f6" fontSize="8" fontWeight="900" fontFamily="sans-serif">
                z
              </text>
            </g>
          )}

          {/* Cute Yellow Bandana / Collar */}
          <path
            d="M 38 90 Q 60 98 82 90 Q 60 106 38 90 Z"
            fill="#ffc800"
            stroke="#e5a500"
            strokeWidth="2.5"
            strokeLinejoin="round"
          />
          {/* Collar Gem/Star */}
          <circle cx="60" cy="97" r="3.5" fill="#ffffff" />
        </svg>
      </div>
    </div>
  );
};
