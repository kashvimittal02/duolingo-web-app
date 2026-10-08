import React from "react";

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  hoverable?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = "",
  onClick,
  hoverable = false,
}) => {
  return (
    <div
      onClick={onClick}
      className={`
        bg-white dark:bg-[#202f36] rounded-2xl border-2 border-gray-200 dark:border-[#37464f] p-4 shadow-[0_3px_0_0_#e5e7eb] dark:shadow-[0_3px_0_0_#182329]
        ${hoverable ? "cursor-pointer hover:border-gray-300 dark:hover:border-[#4b5b66] hover:shadow-[0_4px_0_0_#d1d5db] dark:hover:shadow-[0_4px_0_0_#131d22] active:translate-y-[1px] active:shadow-[0_1px_0_0_#d1d5db] transition-all" : ""}
        ${className}
      `}
    >
      {children}
    </div>
  );
};
