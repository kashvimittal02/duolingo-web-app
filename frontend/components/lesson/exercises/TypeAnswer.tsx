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

// Language-specific special character sets
const LANGUAGE_SPECIAL_CHARACTERS: Record<string, string[]> = {
  es: ["á", "é", "í", "ó", "ú", "ü", "ñ", "¿", "¡"],
  fr: ["é", "à", "è", "ù", "â", "ê", "î", "ô", "û", "ç", "ë", "ï", "ü", "œ", "æ"],
  de: ["ä", "ö", "ü", "ß"],
  it: ["à", "è", "é", "ì", "ò", "ó", "ù"],
  pt: ["á", "â", "ã", "à", "ç", "é", "ê", "í", "ó", "ô", "õ", "ú"],
  en: [],
};

function resolveLanguage(exercise: SafeExercise): { code: string; name: string } {
  // 1. Explicit target_lang on exercise
  const rawLang =
    exercise.target_lang ||
    exercise.payload?.target_lang ||
    exercise.payload?.language;

  if (typeof rawLang === "string" && rawLang.trim()) {
    const l = rawLang.toLowerCase().trim();
    if (l.startsWith("es") || l === "spanish") return { code: "es", name: "Spanish" };
    if (l.startsWith("fr") || l === "french") return { code: "fr", name: "French" };
    if (l.startsWith("de") || l === "german") return { code: "de", name: "German" };
    if (l.startsWith("it") || l === "italian") return { code: "it", name: "Italian" };
    if (l.startsWith("pt") || l === "portuguese") return { code: "pt", name: "Portuguese" };
    if (l.startsWith("en") || l === "english") return { code: "en", name: "English" };
  }

  // 2. Infer from prompt text
  const prompt = (exercise.prompt || "").toLowerCase();
  if (prompt.includes("in spanish") || prompt.includes("en español") || prompt.includes("al español")) {
    return { code: "es", name: "Spanish" };
  }
  if (prompt.includes("in french") || prompt.includes("en français")) {
    return { code: "fr", name: "French" };
  }
  if (prompt.includes("in german") || prompt.includes("auf deutsch")) {
    return { code: "de", name: "German" };
  }
  if (prompt.includes("in italian") || prompt.includes("in italiano")) {
    return { code: "it", name: "Italian" };
  }
  if (prompt.includes("in portuguese") || prompt.includes("em português")) {
    return { code: "pt", name: "Portuguese" };
  }
  if (prompt.includes("in english") || prompt.includes("en inglés")) {
    return { code: "en", name: "English" };
  }

  // 3. Infer from special character usage in prompt or prompt translation
  if (/[áéíóúüñ¿¡]/i.test(exercise.prompt || "") || /[áéíóúüñ¿¡]/i.test(exercise.prompt_translation || "")) {
    return { code: "es", name: "Spanish" };
  }

  // 4. Default to Spanish (curriculum primary target language)
  return { code: "es", name: "Spanish" };
}

export const TypeAnswer: React.FC<TypeAnswerProps> = ({
  exercise,
  selectedAnswer,
  onSelect,
  disabled = false,
}) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const selectionRef = useRef<{ start: number; end: number }>({
    start: 0,
    end: 0,
  });

  const langInfo = resolveLanguage(exercise);
  const specialChars = LANGUAGE_SPECIAL_CHARACTERS[langInfo.code] || [];
  const placeholderText = langInfo.name
    ? `Type in ${langInfo.name}...`
    : "Type your answer...";

  // Continuously record selection range on any user interaction
  const syncSelection = () => {
    if (inputRef.current) {
      const start = inputRef.current.selectionStart ?? 0;
      const end = inputRef.current.selectionEnd ?? start;
      selectionRef.current = { start, end };
    }
  };

  const handleInsertChar = (char: string) => {
    if (disabled) return;
    sounds.playTap();

    const currentText = selectedAnswer || "";
    const input = inputRef.current;

    // Use current live selection if available and valid, otherwise fallback to tracked ref
    let start = currentText.length;
    let end = currentText.length;

    if (input && typeof input.selectionStart === "number") {
      start = input.selectionStart;
      end = input.selectionEnd ?? start;
    } else {
      start = selectionRef.current.start;
      end = selectionRef.current.end;
    }

    // Clamp bounds to prevent out-of-range slicing
    start = Math.max(0, Math.min(start, currentText.length));
    end = Math.max(start, Math.min(end, currentText.length));

    // Splice character at cursor position, preserving text before and after
    const before = currentText.slice(0, start);
    const after = currentText.slice(end);
    const nextText = before + char + after;
    const nextCursorPos = start + char.length;

    // Update tracked selection ref
    selectionRef.current = { start: nextCursorPos, end: nextCursorPos };

    // Emit updated answer to parent
    onSelect(nextText);

    // Keep cursor positioned immediately after inserted character
    requestAnimationFrame(() => {
      if (inputRef.current) {
        inputRef.current.focus();
        inputRef.current.setSelectionRange(nextCursorPos, nextCursorPos);
      }
    });
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
          onChange={(e) => {
            onSelect(e.target.value);
            syncSelection();
          }}
          onSelect={syncSelection}
          onKeyUp={syncSelection}
          onClick={syncSelection}
          placeholder={placeholderText}
          aria-label={`Type answer in ${langInfo.name}`}
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="none"
          spellCheck="false"
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

      {/* Language-Aware Special Character Toolbar */}
      {specialChars.length > 0 && !disabled && (
        <div
          role="toolbar"
          aria-label={`${langInfo.name} special character keyboard`}
          className="flex flex-wrap items-center justify-center gap-1.5 sm:gap-2 select-none"
        >
          {specialChars.map((char) => (
            <button
              key={char}
              type="button"
              tabIndex={0}
              onMouseDown={(e) => e.preventDefault()}
              onClick={() => handleInsertChar(char)}
              aria-label={`Insert ${char}`}
              className="w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-gray-100 hover:bg-gray-200 active:bg-gray-300 text-gray-800 font-extrabold text-base sm:text-lg border border-gray-300 shadow-sm active:translate-y-[1px] flex items-center justify-center transition-all select-none touch-manipulation focus:outline-none focus-visible:ring-2 focus-visible:ring-duo-blue dark:bg-[#202f36] dark:border-[#37464f] dark:text-gray-100 dark:hover:bg-[#283b44] dark:active:bg-[#2e434e] dark:shadow-none"
            >
              {char}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
