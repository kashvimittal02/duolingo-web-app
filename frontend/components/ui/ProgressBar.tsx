import React from "react";

interface ProgressBarProps {
  progress: number; // 0 to 100
  color?: "green" | "blue" | "red" | "yellow";
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  color = "green",
  className = "",
}) => {
  const clampedProgress = Math.min(100, Math.max(0, progress));

  const colorMap = {
    green: "bg-duo-green",
    blue: "bg-duo-blue",
    red: "bg-duo-red",
    yellow: "bg-duo-yellow",
  };

  return (
    <div
      className={`h-4 w-full bg-gray-200 dark:bg-[#2b3a42] rounded-full overflow-hidden p-0.5 relative ${className}`}
    >
      <div
        className={`h-full rounded-full transition-all duration-300 ease-out relative ${colorMap[color]}`}
        style={{ width: `${clampedProgress}%` }}
      >
        {/* Shiny highlight bar */}
        <div className="absolute top-0.5 left-1 right-1 h-1 bg-white/30 rounded-full" />
      </div>
    </div>
  );
};
