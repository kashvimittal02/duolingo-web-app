"use client";

import React from "react";
import { Sun, Moon, Laptop } from "lucide-react";
import { useTheme, Theme } from "@/lib/theme";

interface ThemeToggleProps {
  variant?: "icon" | "segmented";
  className?: string;
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({
  variant = "icon",
  className = "",
}) => {
  const { theme, resolvedTheme, setTheme, toggleTheme } = useTheme();

  if (variant === "segmented") {
    const options: Array<{ value: Theme; label: string; icon: any }> = [
      { value: "light", label: "Light", icon: Sun },
      { value: "dark", label: "Dark", icon: Moon },
      { value: "system", label: "System", icon: Laptop },
    ];

    return (
      <div
        className={`flex items-center gap-1.5 p-1.5 bg-gray-100 dark:bg-[#182830] rounded-2xl border-2 border-gray-200 dark:border-[#37464f] ${className}`}
        role="group"
        aria-label="Theme preference"
      >
        {options.map((opt) => {
          const Icon = opt.icon;
          const isSelected = theme === opt.value;
          return (
            <button
              key={opt.value}
              type="button"
              onClick={() => setTheme(opt.value)}
              className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-xl font-extrabold text-xs uppercase tracking-wide transition-all select-none ${
                isSelected
                  ? "bg-white dark:bg-[#202f36] text-duo-blue shadow-sm border border-gray-200 dark:border-[#37464f]"
                  : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
              }`}
              aria-pressed={isSelected}
              aria-label={`${opt.label} theme`}
            >
              <Icon className="w-4 h-4 stroke-[2.5]" />
              <span>{opt.label}</span>
            </button>
          );
        })}
      </div>
    );
  }

  // Icon toggle button
  return (
    <button
      type="button"
      onClick={toggleTheme}
      className={`p-2 rounded-2xl border-2 border-gray-200 dark:border-[#37464f] bg-white dark:bg-[#202f36] text-gray-600 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-[#283b44] shadow-[0_2px_0_0_#e5e7eb] dark:shadow-[0_2px_0_0_#182329] active:translate-y-[1px] active:shadow-none transition-all flex items-center justify-center ${className}`}
      aria-label={`Switch to ${resolvedTheme === "dark" ? "light" : "dark"} mode`}
      title={`Switch to ${resolvedTheme === "dark" ? "light" : "dark"} mode`}
    >
      {resolvedTheme === "dark" ? (
        <Sun className="w-5 h-5 text-amber-400 stroke-[2.2]" />
      ) : (
        <Moon className="w-5 h-5 text-duo-blue stroke-[2.2]" />
      )}
    </button>
  );
};
