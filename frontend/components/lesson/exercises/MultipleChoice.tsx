"use client";

import React from "react";
import { SafeExercise } from "@/lib/types";
import { AudioButton } from "@/components/ui/AudioButton";
import { sounds } from "@/lib/audio";

interface MultipleChoiceProps {
  exercise: SafeExercise;
  selectedAnswer: string | null;
  onSelect: (answer: string) => void;
  disabled?: boolean;
}

export const MultipleChoice: React.FC<MultipleChoiceProps> = ({
  exercise,
  selectedAnswer,
  onSelect,
  disabled = false,
}) => {
  const options: Array<{ id: string; text: string }> =
    exercise.payload.options || [];

  const handleSelect = (text: string) => {
    if (disabled) return;
    sounds.playTap();
    onSelect(text);
  };

  return (
    <div className="w-full flex flex-col gap-3 max-w-xl mx-auto">
      {options.map((opt, idx) => {
        const isSelected = selectedAnswer === opt.text;

        return (
          <div
            key={opt.id || idx}
            onClick={() => handleSelect(opt.text)}
            className={`
              w-full p-4 rounded-2xl border-2 text-left flex items-center justify-between select-none
              transition-all duration-100 shadow-[0_3px_0_0] active:translate-y-[2px] active:shadow-none
              ${
                isSelected
                  ? "bg-duo-blue-light dark:bg-[#1b3a4b] border-duo-blue text-duo-blue dark:text-[#38bdf8] shadow-[0_3px_0_0_#1899d6]"
                  : "bg-white dark:bg-[#202f36] border-gray-200 dark:border-[#37464f] text-gray-700 dark:text-gray-200 shadow-[0_3px_0_0_#e5e7eb] dark:shadow-[0_3px_0_0_#182329] hover:bg-gray-50 dark:hover:bg-[#283b44] hover:border-gray-300 dark:hover:border-[#4b5b66]"
              }
              ${disabled ? "cursor-not-allowed opacity-90 active:translate-y-0" : "cursor-pointer"}
            `}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                handleSelect(opt.text);
              }
            }}
          >
            <div className="flex items-center gap-4">
              <span
                className={`
                  w-8 h-8 rounded-xl border flex items-center justify-center font-black text-sm
                  ${
                    isSelected
                      ? "border-duo-blue text-duo-blue bg-white dark:bg-[#182830]"
                      : "border-gray-200 dark:border-[#37464f] text-gray-400 dark:text-gray-400 bg-gray-50 dark:bg-[#182830]"
                  }
                `}
              >
                {idx + 1}
              </span>
              <span className="text-base sm:text-lg font-bold">{opt.text}</span>
            </div>

            <AudioButton
              text={opt.text}
              size="sm"
              label={`Listen to "${opt.text}"`}
            />
          </div>
        );
      })}
    </div>
  );
};
