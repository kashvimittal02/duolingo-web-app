import React from "react";

interface PathConnectorProps {
  fromOffset: number;
  toOffset: number;
  isUnlocked?: boolean;
}

export const PathConnector: React.FC<PathConnectorProps> = ({
  fromOffset,
  toOffset,
  isUnlocked = false,
}) => {
  const startX = 140 + fromOffset;
  const endX = 140 + toOffset;
  const height = 40;
  const midY = height / 2;

  return (
    <div className="flex justify-center w-full -my-1 pointer-events-none z-0 select-none">
      <svg
        width="280"
        height={height}
        viewBox={`0 0 280 ${height}`}
        className="overflow-visible"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d={`M ${startX} 0 C ${startX} ${midY}, ${endX} ${midY}, ${endX} ${height}`}
          stroke="currentColor"
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray="4 10"
          className={
            isUnlocked
              ? "text-duo-green opacity-90"
              : "text-gray-200 dark:text-[#24353e]"
          }
        />
      </svg>
    </div>
  );
};
