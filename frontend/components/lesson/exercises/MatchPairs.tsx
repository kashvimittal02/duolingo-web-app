"use client";

import React, { useState, useEffect } from "react";
import { SafeExercise } from "@/lib/types";
import { sounds, speakSpanish } from "@/lib/audio";

interface MatchPairsProps {
  exercise: SafeExercise;
  selectedAnswer: Array<{ left: string; right: string }> | null;
  onSelect: (answer: Array<{ left: string; right: string }> | null) => void;
  disabled?: boolean;
}

interface Item {
  id: string;
  text: string;
}

export const MatchPairs: React.FC<MatchPairsProps> = ({
  exercise,
  selectedAnswer,
  onSelect,
  disabled = false,
}) => {
  const leftItems: Item[] = exercise.payload.left_items || [];
  const rightItems: Item[] = exercise.payload.right_items || [];

  const [selectedLeft, setSelectedLeft] = useState<string | null>(null);
  const [selectedRight, setSelectedRight] = useState<string | null>(null);

  // Map of left item text -> right item text
  const [pairs, setPairs] = useState<Record<string, string>>({});

  useEffect(() => {
    setSelectedLeft(null);
    setSelectedRight(null);
    setPairs({});
  }, [exercise.id]);

  const handleLeftClick = (item: Item) => {
    if (disabled) return;

    sounds.playTap();
    speakSpanish(item.text);

    // If already paired, unpair it
    if (pairs[item.text]) {
      const next = { ...pairs };
      delete next[item.text];
      setPairs(next);
      notifyUpdate(next);
      return;
    }

    if (selectedLeft === item.text) {
      setSelectedLeft(null);
      return;
    }

    if (selectedRight) {
      // Pair with currently selected right
      const next = { ...pairs, [item.text]: selectedRight };
      setPairs(next);
      setSelectedLeft(null);
      setSelectedRight(null);
      notifyUpdate(next);
    } else {
      setSelectedLeft(item.text);
    }
  };

  const handleRightClick = (item: Item) => {
    if (disabled) return;

    sounds.playTap();

    // Check if right item is already paired with any left item
    const existingLeft = Object.keys(pairs).find((l) => pairs[l] === item.text);
    if (existingLeft) {
      const next = { ...pairs };
      delete next[existingLeft];
      setPairs(next);
      notifyUpdate(next);
      return;
    }

    if (selectedRight === item.text) {
      setSelectedRight(null);
      return;
    }

    if (selectedLeft) {
      // Pair with currently selected left
      const next = { ...pairs, [selectedLeft]: item.text };
      setPairs(next);
      setSelectedLeft(null);
      setSelectedRight(null);
      notifyUpdate(next);
    } else {
      setSelectedRight(item.text);
    }
  };

  const notifyUpdate = (currentPairs: Record<string, string>) => {
    const totalPairsNeeded = Math.min(leftItems.length, rightItems.length);
    const pairList = Object.entries(currentPairs).map(([left, right]) => ({
      left,
      right,
    }));

    if (pairList.length === totalPairsNeeded && totalPairsNeeded > 0) {
      onSelect(pairList);
    } else {
      onSelect(null); // Not all pairs are matched yet, disable submit
    }
  };

  const isLeftPaired = (text: string) => Boolean(pairs[text]);
  const isRightPaired = (text: string) =>
    Object.values(pairs).includes(text);

  return (
    <div className="w-full max-w-xl mx-auto flex flex-col gap-4">
      <div className="grid grid-cols-2 gap-4">
        {/* Left Column */}
        <div className="flex flex-col gap-3">
          {leftItems.map((item) => {
            const paired = isLeftPaired(item.text);
            const isSelected = selectedLeft === item.text;

            return (
              <button
                key={item.id}
                disabled={disabled}
                onClick={() => handleLeftClick(item)}
                className={`
                  p-4 rounded-2xl border-2 font-bold text-base text-center transition-all select-none
                  ${
                    paired
                      ? "bg-emerald-50 border-emerald-400 text-emerald-800 shadow-none cursor-pointer dark:bg-emerald-950/40 dark:border-emerald-600 dark:text-emerald-300"
                      : isSelected
                      ? "bg-duo-blue-light border-duo-blue text-duo-blue shadow-[0_3px_0_0_#1899d6] scale-102 dark:bg-[#1b3a4b] dark:border-duo-blue dark:text-[#38bdf8] dark:shadow-[0_3px_0_0_#0f5a7a]"
                      : "bg-white border-gray-200 text-gray-700 shadow-[0_3px_0_0_#e5e7eb] hover:bg-gray-50 active:translate-y-[2px] active:shadow-none dark:bg-[#202f36] dark:border-[#37464f] dark:text-gray-200 dark:shadow-[0_3px_0_0_#182329] dark:hover:bg-[#283b44]"
                  }
                  ${disabled ? "cursor-not-allowed opacity-60" : ""}
                `}
              >
                {item.text}
              </button>
            );
          })}
        </div>

        {/* Right Column */}
        <div className="flex flex-col gap-3">
          {rightItems.map((item) => {
            const paired = isRightPaired(item.text);
            const isSelected = selectedRight === item.text;

            return (
              <button
                key={item.id}
                disabled={disabled}
                onClick={() => handleRightClick(item)}
                className={`
                  p-4 rounded-2xl border-2 font-bold text-base text-center transition-all select-none
                  ${
                    paired
                      ? "bg-emerald-50 border-emerald-400 text-emerald-800 shadow-none cursor-pointer dark:bg-emerald-950/40 dark:border-emerald-600 dark:text-emerald-300"
                      : isSelected
                      ? "bg-duo-blue-light border-duo-blue text-duo-blue shadow-[0_3px_0_0_#1899d6] scale-102 dark:bg-[#1b3a4b] dark:border-duo-blue dark:text-[#38bdf8] dark:shadow-[0_3px_0_0_#0f5a7a]"
                      : "bg-white border-gray-200 text-gray-700 shadow-[0_3px_0_0_#e5e7eb] hover:bg-gray-50 active:translate-y-[2px] active:shadow-none dark:bg-[#202f36] dark:border-[#37464f] dark:text-gray-200 dark:shadow-[0_3px_0_0_#182329] dark:hover:bg-[#283b44]"
                  }
                  ${disabled ? "cursor-not-allowed opacity-60" : ""}
                `}
              >
                {item.text}
              </button>
            );
          })}
        </div>
      </div>

      <div className="text-center text-xs text-gray-400 dark:text-gray-400 font-bold mt-2">
        {Object.keys(pairs).length} of {Math.min(leftItems.length, rightItems.length)} pairs matched
      </div>
    </div>
  );
};
