"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Compass, Trophy, Target, ShoppingBag, User, MoreHorizontal } from "lucide-react";

export const BottomNav: React.FC = () => {
  const pathname = usePathname();

  const navItems = [
    { label: "Learn", href: "/", icon: Compass },
    { label: "Leaderboard", href: "/leaderboard", icon: Trophy },
    { label: "Quests", href: "/quests", icon: Target },
    { label: "Shop", href: "/shop", icon: ShoppingBag },
    { label: "Profile", href: "/profile", icon: User },
    { label: "More", href: "/more", icon: MoreHorizontal },
  ];

  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-white dark:bg-[#131f24] border-t-2 border-gray-200 dark:border-[#2b3a42] px-4 py-2 flex items-center justify-around shadow-lg transition-colors">
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = pathname === item.href;

        return (
          <Link
            key={item.href}
            href={item.href}
            className={`
              flex flex-col items-center gap-1 p-2 rounded-xl transition-all
              ${isActive ? "text-duo-blue" : "text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300"}
            `}
          >
            <Icon className={`w-6 h-6 ${isActive ? "stroke-[2.5]" : "stroke-2"}`} />
            <span className="text-[10px] font-extrabold uppercase tracking-wider">
              {item.label}
            </span>
          </Link>
        );
      })}
    </nav>
  );
};
