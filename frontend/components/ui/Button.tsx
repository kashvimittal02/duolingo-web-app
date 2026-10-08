import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "green" | "blue" | "red" | "purple" | "outline" | "gray" | "ghost";
  size?: "sm" | "md" | "lg";
  fullWidth?: boolean;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = "green",
  size = "md",
  fullWidth = false,
  className = "",
  disabled = false,
  children,
  ...props
}) => {
  const baseStyles =
    "font-bold uppercase tracking-wide rounded-2xl transition-all duration-100 flex items-center justify-center select-none active:translate-y-[2px]";

  const sizeStyles = {
    sm: "py-2 px-4 text-xs shadow-[0_3px_0_0]",
    md: "py-3 px-6 text-sm shadow-[0_4px_0_0]",
    lg: "py-4 px-8 text-base shadow-[0_5px_0_0]",
  };

  const disabledStyle =
    "bg-gray-200 dark:bg-[#202f36] text-gray-400 dark:text-[#55656e] border-2 border-gray-300 dark:border-[#37464f] shadow-[0_4px_0_0_#d1d5db] dark:shadow-[0_4px_0_0_#182329] cursor-not-allowed active:translate-y-0";

  const variantStyles = {
    green: disabled
      ? disabledStyle
      : "bg-duo-green text-white border-2 border-duo-green-dark shadow-[0_4px_0_0_#46a302] hover:brightness-105 active:shadow-none",
    blue: disabled
      ? disabledStyle
      : "bg-duo-blue text-white border-2 border-duo-blue-dark shadow-[0_4px_0_0_#1899d6] hover:brightness-105 active:shadow-none",
    red: disabled
      ? disabledStyle
      : "bg-duo-red text-white border-2 border-duo-red-dark shadow-[0_4px_0_0_#ea2b2b] hover:brightness-105 active:shadow-none",
    purple: disabled
      ? disabledStyle
      : "bg-duo-purple text-white border-2 border-duo-purple-dark shadow-[0_4px_0_0_#a560cc] hover:brightness-105 active:shadow-none",
    outline: disabled
      ? disabledStyle
      : "bg-white dark:bg-[#202f36] text-gray-700 dark:text-gray-200 border-2 border-gray-200 dark:border-[#37464f] shadow-[0_4px_0_0_#e5e7eb] dark:shadow-[0_4px_0_0_#182329] hover:bg-gray-50 dark:hover:bg-[#283b44] active:shadow-none",
    gray: "bg-gray-200 dark:bg-[#2b3a42] text-gray-600 dark:text-gray-300 border-2 border-gray-300 dark:border-[#37464f] shadow-[0_4px_0_0_#cbd5e1] dark:shadow-[0_4px_0_0_#182329] hover:bg-gray-300 dark:hover:bg-[#344650] active:shadow-none",
    ghost:
      "bg-transparent text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-[#283b44] shadow-none border-0 active:translate-y-0",
  };

  return (
    <button
      disabled={disabled}
      className={`
        ${baseStyles}
        ${sizeStyles[size]}
        ${variantStyles[variant]}
        ${fullWidth ? "w-full" : ""}
        ${className}
      `}
      {...props}
    >
      {children}
    </button>
  );
};
