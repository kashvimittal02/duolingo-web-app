"use client";

import React from "react";
import { SafeExercise } from "@/lib/types";
import { AudioButton } from "@/components/ui/AudioButton";
import { sounds, speakSpanish } from "@/lib/audio";

interface FillBlankProps {
  exercise: SafeExercise;
  selectedAnswer: string | null;
  onSelect: (answer: string) => void;
  disabled?: boolean;
}

export const FillBlank: React.FC<FillBlankProps> = ({
  exercise,
  selectedAnswer,
  onSelect,
  disabled = false,
}) => {
  const options: Array<{ id: string; text: string }> =
    exercise.payload.options || [];

  const template: string = exercise.payload.template || exercise.prompt;

  const handleSelectOption = (text: string) => {
    if (disabled) return;
    sounds.playTap();
    speakSpanish(text);
    onSelect(text);
  };

  const sentenceToSpeak =
    template.includes("___") && selectedAnswer
      ? template.replace("___", selectedAnswer)
      : template.replace(/___+/g, " ");

  // Render sentence with dynamic filled blank
  const renderSentence = () => {
    const parts = template.split("___");
    if (parts.length < 2) {
      return (
        <span className="text-xl sm:text-2xl font-black text-gray-800 dark:text-gray-100">
          {template}
        </span>
      );
    }

    return (
      <div className="flex flex-wrap items-center justify-center gap-2 text-xl sm:text-2xl font-black text-gray-800 dark:text-gray-100 text-center leading-relaxed">
        <span>{parts[0]}</span>
        <span
          className={`
            inline-flex items-center justify-center min-w-[100px] px-3 py-1 rounded-xl border-2 font-black transition-all
            ${
              selectedAnswer
                ? "bg-duo-blue-light border-duo-blue text-duo-blue shadow-sm dark:bg-[#1b3a4b] dark:border-duo-blue dark:text-[#38bdf8]"
                : "bg-gray-100 border-dashed border-gray-400 text-transparent min-h-[38px] dark:bg-[#202f36] dark:border-gray-600"
            }
          `}
        >
          {selectedAnswer || "blank"}
        </span>
        <span>{parts[1]}</span>
      </div>
    );
  };

  return (
    <div className="w-full max-w-xl mx-auto flex flex-col items-center gap-8">
      {/* Template sentence area */}
      <div className="p-6 bg-gray-50 border-2 border-gray-200 rounded-3xl w-full flex items-center justify-between gap-4 min-h-[120px] dark:bg-[#182830] dark:border-[#37464f]">
        <AudioButton
          text={sentenceToSpeak}
          size="md"
          label="Listen to sentence"
        />
        <div className="flex-1 flex justify-center">
          {renderSentence()}
        </div>
      </div>

      {/* Selectable Options */}
      <div className="flex flex-wrap items-center justify-center gap-3 w-full">
        {options.map((opt, idx) => {
          const isSelected = selectedAnswer === opt.text;

          return (
            <button
              key={opt.id || idx}
              disabled={disabled}
              onClick={() => handleSelectOption(opt.text)}
              className={`
                px-5 py-3 rounded-2xl font-extrabold text-base border-2 select-none transition-all duration-100
                shadow-[0_3px_0_0] active:translate-y-[2px] active:shadow-none
                ${
                  isSelected
                    ? "bg-duo-blue-light border-duo-blue text-duo-blue shadow-[0_3px_0_0_#1899d6] dark:bg-[#1b3a4b] dark:border-duo-blue dark:text-[#38bdf8] dark:shadow-[0_3px_0_0_#0f5a7a]"
                    : "bg-white border-gray-200 text-gray-700 shadow-[0_3px_0_0_#e5e7eb] hover:bg-gray-50 dark:bg-[#202f36] dark:border-[#37464f] dark:text-gray-200 dark:shadow-[0_3px_0_0_#182329] dark:hover:bg-[#283b44]"
                }
                ${disabled ? "cursor-not-allowed opacity-60" : "cursor-pointer"}
              `}
            >
              {opt.text}
            </button>
          );
        })}
      </div>
    </div>
  );
};
