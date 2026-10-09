"use client";

import React from "react";
import Image from "next/image";
import { Lock, Check, Trophy, Sparkles, Shield } from "lucide-react";
import { LessonNode } from "@/lib/types";

interface CheckpointNodeProps {
  lesson: LessonNode;
  isUnlocked?: boolean;
  onStart: () => void;
}

export const CheckpointNode: React.FC<CheckpointNodeProps> = ({
  lesson,
  isUnlocked = false,
  onStart,
}) => {
  const isCompleted = lesson.status === "completed";
  const isAvailable = isUnlocked && !isCompleted;
  const isLocked = !isUnlocked || lesson.status === "locked";
  const displayTitle = "Section 1 Checkpoint Challenge";

  return (
    <div className="w-full max-w-md mx-auto my-10 px-4 select-none">
      <div
        className={`
          relative rounded-3xl p-6 text-center border-4 transition-all duration-200
          ${
            isLocked
              ? "bg-gray-100 dark:bg-[#1a2c35] border-gray-300 dark:border-[#2a3c46] shadow-[0_6px_0_0_#cbd5e1] dark:shadow-[0_6px_0_0_#14232b]"
              : isCompleted
              ? "bg-amber-50 dark:bg-amber-950/30 border-amber-400 dark:border-amber-500 shadow-[0_8px_0_0_#d97706]"
              : "bg-gradient-to-b from-red-500 to-rose-600 border-red-700 shadow-[0_8px_0_0_#991b1b] text-white"
          }
        `}
      >
        {/* Top Eyebrow Tag */}
        <div className="flex justify-center -mt-9 mb-3">
          <div
            className={`
              inline-flex items-center gap-1.5 px-4 py-1 rounded-full text-xs font-black uppercase tracking-wider border-2 shadow-md
              ${
                isLocked
                  ? "bg-gray-300 dark:bg-gray-700 text-gray-600 dark:text-gray-300 border-white dark:border-gray-800"
                  : isCompleted
                  ? "bg-amber-400 text-amber-950 border-white"
                  : "bg-white text-red-600 border-red-600 animate-bounce"
              }
            `}
          >
            {isCompleted ? (
              <>
                <Check className="w-4 h-4 stroke-[3]" />
                <span>SECTION 1 MASTERED</span>
              </>
            ) : isAvailable ? (
              <>
                <Sparkles className="w-4 h-4 fill-red-500 text-red-500" />
                <span>CHECKPOINT CHALLENGE</span>
              </>
            ) : (
              <>
                <Lock className="w-3.5 h-3.5" />
                <span>SECTION CHECKPOINT</span>
              </>
            )}
          </div>
        </div>

        {/* Castle Badge Stepping Stone Button */}
        <div className="flex justify-center my-2">
          <button
            type="button"
            disabled={isLocked}
            onClick={onStart}
            className={`
              relative w-24 h-24 sm:w-28 sm:h-28 rounded-full border-4 flex items-center justify-center transition-all duration-150
              ${
                isLocked
                  ? "bg-gray-200 dark:bg-[#202f36] border-gray-300 dark:border-[#37464f] opacity-75 cursor-not-allowed shadow-[0_6px_0_0_#cbd5e1] dark:shadow-[0_6px_0_0_#182329]"
                  : isCompleted
                  ? "bg-amber-400 border-amber-500 text-white shadow-[0_8px_0_0_#b45309] hover:brightness-105 active:translate-y-[2px] active:shadow-none cursor-pointer"
                  : "bg-white dark:bg-[#1f2f38] border-red-600 text-red-600 shadow-[0_8px_0_0_#991b1b] hover:brightness-105 active:translate-y-[2px] active:shadow-none cursor-pointer animate-pulse-subtle"
              }
            `}
            title={displayTitle}
            aria-label="Start Section 1 Checkpoint Challenge"
          >
            {isLocked ? (
              <div className="flex flex-col items-center gap-1 text-gray-400 dark:text-gray-500">
                <Lock className="w-10 h-10 stroke-[2.5]" />
              </div>
            ) : (
              <div className="w-16 h-16 sm:w-20 sm:h-20 relative">
                <Image
                  src="/images/lessons/checkpoint.svg"
                  alt="Checkpoint Castle"
                  width={80}
                  height={80}
                  className="w-full h-full object-contain pointer-events-none"
                />
              </div>
            )}
          </button>
        </div>

        {/* Title & XP Reward */}
        <h3
          className={`
            text-xl font-black mt-3 mb-1
            ${isLocked ? "text-gray-500 dark:text-gray-400" : isCompleted ? "text-amber-950 dark:text-amber-200" : "text-white"}
          `}
        >
          {displayTitle}
        </h3>
        <p
          className={`
            text-xs font-bold max-w-xs mx-auto mb-4
            ${isLocked ? "text-gray-400 dark:text-gray-500" : isCompleted ? "text-amber-700 dark:text-amber-400" : "text-red-100"}
          `}
        >
          {isLocked
            ? "Complete all preceding lessons in Section 1 to unlock the Checkpoint Challenge!"
            : isCompleted
            ? "You proved your mastery of Rookie Basics! Section 2: Daily Life is unlocked."
            : "Pass this comprehensive challenge to unlock Section 2: Daily Life!"}
        </p>

        {/* Action Button */}
        <button
          type="button"
          disabled={isLocked}
          onClick={onStart}
          className={`
            w-full py-3 px-6 rounded-2xl font-black text-sm uppercase tracking-wider transition-all duration-150 border-2
            ${
              isLocked
                ? "bg-gray-200 dark:bg-gray-800 text-gray-400 border-gray-300 dark:border-gray-700 cursor-not-allowed"
                : isCompleted
                ? "bg-amber-400 text-amber-950 border-amber-500 hover:brightness-105 shadow-[0_4px_0_0_#b45309] active:translate-y-[2px]"
                : "bg-white text-red-600 border-white hover:bg-red-50 shadow-[0_4px_0_0_rgba(0,0,0,0.2)] active:translate-y-[2px]"
            }
          `}
        >
          {isCompleted ? "Review Checkpoint (+5 XP)" : isAvailable ? "Jump to Challenge (+50 XP)" : "Locked"}
        </button>
      </div>
    </div>
  );
};
