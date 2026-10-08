"use client";

import React, { useRef } from "react";
import { SafeExercise } from "@/lib/types";
import { AudioButton } from "@/components/ui/AudioButton";
import { sounds } from "@/lib/audio";

interface TypeAnswerProps {
  exercise: SafeExercise;
  selectedAnswer: string;
  onSelect: (answer: string) => void;
  disabled?: boolean;
}

export const TypeAnswer: React.FC<TypeAnswerProps> = ({
  exercise,
  selectedAnswer,
  onSelect,
  disabled = false,
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const specialChars = ["á", "é", "í", "ó", "ú", "ñ", "¿", "¡"];

  const handleInsertChar = (char: string) => {
    if (disabled) return;
    sounds.playTap();
    const nextText = selectedAnswer + char;
    onSelect(nextText);
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto flex flex-col gap-6">
      {/* Text Input */}
      <div className="relative w-full flex items-center">
        <input
          ref={inputRef}
          type="text"
          disabled={disabled}
          value={selectedAnswer}
          onChange={(e) => onSelect(e.target.value)}
          placeholder="Type in Spanish..."
          className={`
            w-full p-4 pr-14 text-lg sm:text-xl font-bold rounded-2xl border-2
            focus:outline-none transition-all
            ${
              disabled
                ? "bg-gray-50 border-gray-200 text-gray-500 cursor-not-allowed dark:bg-[#182830] dark:border-[#37464f] dark:text-gray-500"
                : "bg-white text-gray-800 border-gray-300 focus:border-duo-blue shadow-[0_3px_0_0_#e5e7eb] focus:shadow-[0_3px_0_0_#1899d6] dark:bg-[#202f36] dark:border-[#37464f] dark:text-gray-100 dark:shadow-[0_3px_0_0_#182329] dark:focus:border-duo-blue dark:focus:shadow-[0_3px_0_0_#0f5a7a] dark:placeholder-gray-500"
            }
          `}
          autoFocus
        />
        {selectedAnswer.trim().length > 0 && (
          <div className="absolute right-3">
            <AudioButton
              text={selectedAnswer}
              size="sm"
              label="Listen to your typed answer"
            />
          </div>
        )}
      </div>

      {/* Quick Accent Keyboard */}
      {!disabled && (
        <div className="flex flex-wrap items-center justify-center gap-1.5">
          {specialChars.map((char) => (
            <button
              key={char}
              type="button"
              onClick={() => handleInsertChar(char)}
              className="w-10 h-10 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-extrabold text-base border border-gray-300 shadow-sm active:translate-y-[1px] flex items-center justify-center transition-all select-none dark:bg-[#202f36] dark:border-[#37464f] dark:text-gray-200 dark:hover:bg-[#283b44] dark:shadow-none"
            >
              {char}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
