"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Compass, Trophy, Target, ShoppingBag, User, MoreHorizontal } from "lucide-react";

export const BottomNav: React.FC = () => {
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
    <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-white dark:bg-[#131f24] border-t-2 border-gray-200 dark:border-[#2b3a42] px-2 py-1.5 flex items-center justify-around shadow-lg transition-colors">
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = pathname === item.href;

        return (
          <Link
            key={item.href}
            href={item.href}
            className={`
              flex flex-col items-center gap-0.5 p-1 rounded-xl transition-all
              ${isActive ? "text-duo-blue font-black" : "text-gray-500 dark:text-gray-400 font-bold"}
            `}
          >
            <div
              className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                isActive ? "bg-duo-blue-light dark:bg-[#1b3a4b]" : item.bg
              }`}
            >
              <Icon
                className={`w-4.5 h-4.5 ${item.color} ${
                  isActive ? "stroke-[2.5]" : "stroke-2"
                }`}
              />
            </div>
            <span className="text-[10px] uppercase tracking-wider">
              {item.label}
            </span>
          </Link>
        );
      })}
    </nav>
  );
};
