"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Compass, Trophy, ShoppingBag, User, Sparkles } from "lucide-react";
import { ThemeToggle } from "@/components/ui/ThemeToggle";

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  const navItems = [
    { label: "Learn", href: "/", icon: Compass },
    { label: "Leaderboard", href: "/leaderboard", icon: Trophy },
    { label: "Shop", href: "/shop", icon: ShoppingBag },
    { label: "Profile", href: "/profile", icon: User },
  ];

  return (
    <aside className="hidden md:flex flex-col w-64 h-screen fixed left-0 top-0 bg-white dark:bg-[#131f24] border-r-2 border-gray-200 dark:border-[#2b3a42] p-4 z-50 transition-colors">
      {/* Brand Logo */}
      <Link href="/" className="flex items-center gap-2 px-4 py-4 mb-4 select-none">
        <div className="w-10 h-10 rounded-2xl bg-duo-green flex items-center justify-center shadow-[0_3px_0_0_#46a302]">
          <Sparkles className="w-6 h-6 text-white stroke-[2.5]" />
        </div>
        <span className="text-2xl font-black text-duo-green tracking-wider uppercase">
          LingoApp
        </span>
      </Link>

      {/* Nav Menu */}
      <nav className="flex flex-col gap-2 flex-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`
                flex items-center gap-4 px-4 py-3 rounded-2xl font-extrabold uppercase text-sm tracking-wider
                transition-all duration-150 select-none
                ${
                  isActive
                    ? "bg-duo-blue-light dark:bg-[#1b3a4b] text-duo-blue dark:text-[#38bdf8] border-2 border-duo-blue shadow-[0_2px_0_0_#1899d6]"
                    : "text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-[#202f36] dark:hover:text-gray-200 border-2 border-transparent"
                }
              `}
            >
              <Icon
                className={`w-6 h-6 ${isActive ? "text-duo-blue stroke-[2.5]" : "text-gray-400 dark:text-gray-400 stroke-2"}`}
              />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Theme Control & Footer Info */}
      <div className="pt-3 border-t border-gray-100 dark:border-[#2b3a42] flex flex-col gap-3">
        <ThemeToggle variant="segmented" />
        <div className="text-xs text-gray-400 dark:text-gray-500 font-bold text-center">
          Spanish A1 • SDE Fullstack
        </div>
      </div>
    </aside>
  );
};
