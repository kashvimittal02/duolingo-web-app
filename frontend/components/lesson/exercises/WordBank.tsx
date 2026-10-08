"use client";

import React, { useState, useEffect } from "react";
import { SafeExercise } from "@/lib/types";
import { AudioButton } from "@/components/ui/AudioButton";
import { sounds, speakSpanish } from "@/lib/audio";

interface WordBankProps {
  exercise: SafeExercise;
  selectedAnswer: string[] | null;
  onSelect: (answer: string[]) => void;
  disabled?: boolean;
}

interface BankToken {
  id: string;
  text: string;
  used: boolean;
}

export const WordBank: React.FC<WordBankProps> = ({
  exercise,
  selectedAnswer,
  onSelect,
  disabled = false,
}) => {
  const initialTokens: Array<{ id: string; text: string }> =
    exercise.payload.tokens || [];

  const [bank, setBank] = useState<BankToken[]>(() =>
    initialTokens.map((t, idx) => ({
      id: t.id || `wb_${idx}`,
      text: t.text,
      used: false,
    }))
  );

  const [sentence, setSentence] = useState<BankToken[]>([]);

  // Reset when exercise changes
  useEffect(() => {
    const fresh = initialTokens.map((t, idx) => ({
      id: t.id || `wb_${idx}`,
      text: t.text,
      used: false,
    }));
    setBank(fresh);
    setSentence([]);
  }, [exercise.id]);

  const handleSelectToken = (token: BankToken) => {
    if (disabled || token.used) return;

    sounds.playTap();
    speakSpanish(token.text);

    // Mark as used in bank
    const updatedBank = bank.map((b) =>
      b.id === token.id ? { ...b, used: true } : b
    );
    const updatedSentence = [...sentence, token];

    setBank(updatedBank);
    setSentence(updatedSentence);
    onSelect(updatedSentence.map((t) => t.text));
  };

  const handleRemoveToken = (indexToRemove: number) => {
    if (disabled) return;

    sounds.playTap();

    const tokenToRemove = sentence[indexToRemove];
    const updatedSentence = sentence.filter((_, idx) => idx !== indexToRemove);
    const updatedBank = bank.map((b) =>
      b.id === tokenToRemove.id ? { ...b, used: false } : b
    );

    setBank(updatedBank);
    setSentence(updatedSentence);
    onSelect(updatedSentence.map((t) => t.text));
  };

  return (
    <div className="w-full flex flex-col gap-8 max-w-xl mx-auto">
      {/* Assembled Sentence Area */}
      <div className="flex items-center gap-3">
        <div className="flex-1 min-h-[90px] p-4 bg-gray-50 dark:bg-[#182830] border-b-2 border-t-2 border-gray-200 dark:border-[#37464f] flex flex-wrap items-center gap-2 rounded-2xl">
          {sentence.length === 0 ? (
            <span className="text-gray-400 dark:text-gray-500 font-bold text-sm italic select-none">
              Tap the word tiles below to form the sentence...
            </span>
          ) : (
            sentence.map((token, idx) => (
              <button
                key={`${token.id}_${idx}`}
                disabled={disabled}
                onClick={() => handleRemoveToken(idx)}
                className="px-4 py-2 bg-white dark:bg-[#202f36] text-gray-800 dark:text-gray-100 font-extrabold text-base rounded-2xl border-2 border-gray-300 dark:border-[#37464f] shadow-[0_3px_0_0_#d1d5db] dark:shadow-[0_3px_0_0_#131d22] active:translate-y-[1px] active:shadow-none hover:border-gray-400 dark:hover:border-[#4b5b66] select-none animate-scale-in"
              >
                {token.text}
              </button>
            ))
          )}
        </div>
        {sentence.length > 0 && (
          <AudioButton
            text={sentence.map((t) => t.text).join(" ")}
            size="md"
            label="Listen to constructed sentence"
          />
        )}
      </div>

      {/* Available Word Bank Tiles */}
      <div className="flex flex-wrap items-center justify-center gap-2.5">
        {bank.map((token) => (
          <button
            key={token.id}
            disabled={disabled || token.used}
            onClick={() => handleSelectToken(token)}
            className={`
              px-4 py-2.5 rounded-2xl font-extrabold text-base border-2 select-none transition-all duration-100
              ${
                token.used
                  ? "bg-gray-200 dark:bg-[#1c282e] text-transparent border-gray-200 dark:border-[#1c282e] shadow-none cursor-default"
                  : "bg-white dark:bg-[#202f36] text-gray-800 dark:text-gray-100 border-gray-200 dark:border-[#37464f] shadow-[0_3px_0_0_#e5e7eb] dark:shadow-[0_3px_0_0_#182329] hover:bg-gray-50 dark:hover:bg-[#283b44] hover:border-gray-300 dark:hover:border-[#4b5b66] active:translate-y-[2px] active:shadow-none cursor-pointer"
              }
            `}
          >
            {token.text}
          </button>
        ))}
      </div>
    </div>
  );
};
