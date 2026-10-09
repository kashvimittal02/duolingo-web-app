"use client";

import React from "react";
import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { Compass, Trophy, Target, ShoppingBag, User, MoreHorizontal } from "lucide-react";

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  const navItems = [
    {
      label: "Learn",
      href: "/",
      icon: Compass,
      color: "text-duo-green dark:text-emerald-400",
      bg: "bg-emerald-100 dark:bg-emerald-950/60",
    },
    {
      label: "Leaderboard",
      href: "/leaderboard",
      icon: Trophy,
      color: "text-amber-500 dark:text-amber-400",
      bg: "bg-amber-100 dark:bg-amber-950/60",
    },
    {
      label: "Quests",
      href: "/quests",
      icon: Target,
      color: "text-purple-500 dark:text-purple-400",
      bg: "bg-purple-100 dark:bg-purple-950/60",
    },
    {
      label: "Shop",
      href: "/shop",
      icon: ShoppingBag,
      color: "text-duo-orange dark:text-orange-400",
      bg: "bg-orange-100 dark:bg-orange-950/60",
    },
    {
      label: "Profile",
      href: "/profile",
      icon: User,
      color: "text-duo-blue dark:text-sky-400",
      bg: "bg-blue-100 dark:bg-blue-950/60",
    },
    {
      label: "More",
      href: "/more",
      icon: MoreHorizontal,
      color: "text-pink-500 dark:text-pink-400",
      bg: "bg-pink-100 dark:bg-pink-950/60",
    },
  ];

  return (
    <aside className="hidden md:flex flex-col w-64 h-screen fixed left-0 top-0 bg-white dark:bg-[#131f24] border-r-2 border-gray-200 dark:border-[#2b3a42] p-4 z-50 transition-colors">
      {/* Brand Logo */}
      <Link
        href="/"
        className="flex items-center gap-3 px-4 py-3.5 mb-4 select-none hover:opacity-95 transition-opacity"
        aria-label="LingoApp Home"
      >
        <div className="w-[52px] h-[52px] shrink-0 flex items-center justify-center">
          <Image
            src="/images/mascot/mascot-happy.svg"
            alt="LingoApp Mascot"
            width={52}
            height={52}
            className="w-full h-full object-contain pointer-events-none"
            priority
          />
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
                flex items-center gap-3.5 px-3.5 py-2.5 rounded-2xl font-black uppercase text-sm tracking-wider
                transition-all duration-150 select-none
                ${
                  isActive
                    ? "bg-duo-blue-light dark:bg-[#1b3a4b] text-duo-blue dark:text-[#38bdf8] border-2 border-duo-blue shadow-[0_2px_0_0_#1899d6]"
                    : "text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-[#202f36] border-2 border-transparent"
                }
              `}
            >
              <div
                className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 transition-colors ${
                  isActive ? "bg-white/80 dark:bg-[#132733]" : item.bg
                }`}
              >
                <Icon
                  className={`w-5 h-5 ${item.color} ${
                    isActive ? "stroke-[2.5]" : "stroke-2"
                  }`}
                />
              </div>
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer Info */}
      <div className="pt-3 border-t border-gray-100 dark:border-[#2b3a42] flex flex-col gap-1">
        <div className="text-xs text-gray-400 dark:text-gray-500 font-extrabold text-center uppercase tracking-wider">
          Spanish A1
        </div>
      </div>
    </aside>
  );
};
