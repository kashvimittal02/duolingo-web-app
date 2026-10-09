"use client";

import React from "react";
import { Lock, Check, Play } from "lucide-react";
import { LessonNode } from "@/lib/types";
import { LessonIcon } from "./LessonIcon";

interface LessonPathNodeProps {
  lesson: LessonNode;
  unitColor: string;
  offset?: number;
  isCurrent?: boolean;
  onLaunch: () => void;
}

// Map lesson title and order index to authentic lesson illustration
const getLessonBadgeName = (title: string, orderIndex: number): string => {
  const t = title.toLowerCase();
  if (t.includes("review") || t.includes("checkpoint") || orderIndex === 5) {
    return "review";
  }
  if (t.includes("grammar") || t.includes("courtesies") || t.includes("sentence") || orderIndex === 3) {
    return "grammar";
  }
  if (
    t.includes("conversation") ||
    t.includes("night") ||
    t.includes("day") ||
    t.includes("introductions") ||
    orderIndex % 2 === 0
  ) {
    return "conversation";
  }
  return "vocab";
};

export const LessonPathNode: React.FC<LessonPathNodeProps> = ({
  lesson,
  unitColor,
  offset = 0,
  isCurrent = false,
  onLaunch,
}) => {
  const isLocked = lesson.status === "locked";
  const isCompleted = lesson.status === "completed";
  const isAvailable = lesson.status === "available";

  const badgeName = getLessonBadgeName(lesson.title, lesson.order_index);

  // Stepping stone button styling
  const getButtonStyle = () => {
    if (isLocked) {
      return "bg-gray-200 dark:bg-[#202f36] border-gray-300 dark:border-[#37464f] text-gray-400 dark:text-[#55656e] shadow-[0_6px_0_0_#cbd5e1] dark:shadow-[0_6px_0_0_#182329] cursor-not-allowed opacity-90";
    }
    if (isCompleted) {
      return "bg-duo-yellow border-duo-yellow-dark text-white shadow-[0_6px_0_0_#e5a400] hover:brightness-105 active:translate-y-[2px] active:shadow-[0_2px_0_0_#e5a400] cursor-pointer";
    }
    // Available / Active
    return "bg-duo-green border-duo-green-dark text-white shadow-[0_7px_0_0_#46a302] hover:brightness-105 active:translate-y-[2px] active:shadow-[0_2px_0_0_#46a302] cursor-pointer animate-pulse-subtle";
  };

  return (
    <div
      className="flex flex-col items-center my-3.5 transition-transform duration-300 select-none"
      style={{ transform: `translateX(${offset}px)` }}
    >
      <div className="relative">
        {/* Prominent floating START indicator for currently available lesson */}
        {isCurrent && isAvailable && (
          <div className="absolute -top-11 left-1/2 -translate-x-1/2 z-20 pointer-events-none whitespace-nowrap animate-bounce flex flex-col items-center">
            <span className="bg-white dark:bg-[#1a2c35] text-duo-green border-2 border-duo-green px-3.5 py-0.5 rounded-xl text-xs font-black uppercase tracking-wider shadow-md">
              START
            </span>
            <div className="w-0 h-0 border-l-[5px] border-l-transparent border-r-[5px] border-r-transparent border-t-[5px] border-t-duo-green -mt-[1px]" />
          </div>
        )}

        {/* Circular active ring for current available lesson */}
        {isAvailable && (
          <div className="absolute -inset-2 rounded-full border-2 border-dashed border-duo-green/50 animate-spin-slow pointer-events-none" />
        )}

        {/* Completed Check Badge on top right of node */}
        {isCompleted && (
          <div className="absolute -top-1 -right-1 z-20 bg-emerald-500 text-white rounded-full p-1 shadow-md border-2 border-white dark:border-[#131f24] flex items-center justify-center">
            <Check className="w-3.5 h-3.5 stroke-[3.5]" />
          </div>
        )}

        {/* 3D Stepping Stone Circular Button */}
        <button
          type="button"
          disabled={isLocked}
          onClick={isLocked ? undefined : onLaunch}
          className={`
            w-18 h-18 sm:w-20 sm:h-20 rounded-full border-4 flex items-center justify-center transition-all duration-100 select-none relative
            ${getButtonStyle()}
          `}
          title={
            isLocked
              ? `${lesson.title} (Locked)`
              : `${lesson.title} (${isCompleted ? "Completed - Review" : "Start"})`
          }
          aria-label={`${lesson.title} - ${lesson.status}`}
        >
          {isLocked ? (
            <Lock className="w-7 h-7 sm:w-8 sm:h-8 stroke-[2.5]" />
          ) : isCompleted ? (
            <LessonIcon name={badgeName} size={38} className="brightness-105" />
          ) : (
            <LessonIcon name={badgeName} size={42} />
          )}
        </button>
      </div>

      {/* Lesson Name & Clear State Indicator */}
      <div className="flex flex-col items-center mt-2.5 max-w-[140px] text-center">
        <span className="text-xs font-black text-gray-800 dark:text-gray-200 leading-snug line-clamp-2">
          {lesson.title}
        </span>
        {!isCompleted && (
          <span
            className={`mt-1 text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full ${
              isAvailable
                ? "bg-green-100 dark:bg-green-950/60 text-green-800 dark:text-green-300 border border-green-300/60"
                : "bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-500 border border-gray-200 dark:border-gray-700"
            }`}
          >
            {isAvailable ? "Available" : "Locked"}
          </span>
        )}
      </div>
    </div>
  );
};
