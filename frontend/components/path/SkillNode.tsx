"use client";

import React from "react";
import { Lock, Crown, Check, Star } from "lucide-react";
import { SkillNode as SkillNodeType } from "@/lib/types";
import { LessonIcon } from "./LessonIcon";

interface SkillNodeProps {
  skill: SkillNodeType;
  unitColor: string;
  onClick: () => void;
  offset?: number; // horizontal displacement for path curvature
  isCurrentLesson?: boolean;
}

export const SkillNode: React.FC<SkillNodeProps> = ({
  skill,
  unitColor,
  onClick,
  offset = 0,
  isCurrentLesson = false,
}) => {
  const isLocked = skill.status === "locked";
  const isCompleted = skill.status === "completed";
  const isAvailable = skill.status === "available";

  // Stepping stone 3D button styling with rich tactile depths
  const getButtonStyle = () => {
    if (isLocked) {
      return "bg-gray-200 dark:bg-[#202f36] border-gray-300 dark:border-[#37464f] text-gray-400 dark:text-[#55656e] shadow-[0_6px_0_0_#cbd5e1] dark:shadow-[0_6px_0_0_#182329] cursor-not-allowed";
    }
    if (isCompleted) {
      return "bg-duo-yellow border-duo-yellow-dark text-white shadow-[0_6px_0_0_#e5a400] hover:brightness-105 active:translate-y-[2px] active:shadow-[0_2px_0_0_#e5a400] cursor-pointer";
    }
    // Available / In progress
    return "bg-duo-green border-duo-green-dark text-white shadow-[0_7px_0_0_#46a302] hover:brightness-105 active:translate-y-[2px] active:shadow-[0_2px_0_0_#46a302] cursor-pointer animate-bounce-subtle";
  };

  return (
    <div
      className="flex flex-col items-center my-4 transition-transform duration-300 select-none"
      style={{ transform: `translateX(${offset}px)` }}
    >
      <div className="relative">
        {/* Floating START Bubble for active skill */}
        {isAvailable && (
          <div className="absolute -top-10 left-1/2 -translate-x-1/2 z-20 pointer-events-none whitespace-nowrap animate-bounce flex flex-col items-center">
            <span className="bg-white dark:bg-[#1a2c35] text-duo-green border-2 border-duo-green px-3.5 py-0.5 rounded-xl text-xs font-black uppercase tracking-wider shadow-md">
              START
            </span>
            <div className="w-0 h-0 border-l-[5px] border-l-transparent border-r-[5px] border-r-transparent border-t-[5px] border-t-duo-green -mt-[1px]" />
          </div>
        )}

        {/* Circular Progress Ring for active skill */}
        {isAvailable && (
          <svg className="absolute -top-2 -left-2 w-[96px] h-[96px] -rotate-90 pointer-events-none" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="45"
              className="text-gray-200/90 dark:text-[#25363f]"
              strokeWidth="5"
              stroke="currentColor"
              fill="transparent"
            />
            {skill.crowns > 0 && (
              <circle
                cx="50"
                cy="50"
                r="45"
                className="text-duo-yellow"
                strokeWidth="5"
                strokeDasharray={282.74}
                strokeDashoffset={282.74 * (1 - (skill.crowns / Math.max(1, skill.total_crown_levels)))}
                strokeLinecap="round"
                stroke="currentColor"
                fill="transparent"
              />
            )}
          </svg>
        )}

        {/* Crown Badge */}
        {!isLocked && (
          <div className="absolute -top-2 -right-2 z-10 flex items-center gap-0.5 bg-duo-yellow border-2 border-white dark:border-[#131f24] px-2 py-0.5 rounded-full shadow-sm text-xs font-black text-amber-900">
            <Crown className="w-3.5 h-3.5 fill-amber-500 text-amber-700" />
            <span>{skill.crowns}</span>
          </div>
        )}

        {/* Circular 3D Stepping Stone Button */}
        <button
          type="button"
          disabled={isLocked}
          onClick={onClick}
          className={`
            w-20 h-20 rounded-full border-4 flex items-center justify-center transition-all duration-100 select-none relative
            ${getButtonStyle()}
          `}
          aria-label={skill.title}
        >
          {isLocked ? (
            <Lock className="w-8 h-8 stroke-[2.5]" />
          ) : isCompleted ? (
            <Check className="w-10 h-10 stroke-[3.5]" />
          ) : (
            <LessonIcon name={skill.icon_name} size={40} />
          )}
        </button>
      </div>

      {/* Skill Label */}
      <span className="mt-2 text-sm font-black text-gray-700 dark:text-gray-200 max-w-[130px] text-center leading-tight">
        {skill.title}
      </span>
    </div>
  );
};
