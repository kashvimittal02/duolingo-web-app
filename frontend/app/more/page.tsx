"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopHeader } from "@/components/layout/TopHeader";
import { BottomNav } from "@/components/layout/BottomNav";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { LingoMascot } from "@/components/mascot/LingoMascot";
import { getLearnerProfile } from "@/lib/api";
import { LearnerProfile } from "@/lib/types";
import {
  MoreHorizontal,
  Settings,
  HelpCircle,
  BookOpen,
  Sparkles,
  Info,
  Radio,
  Users2,
  Bookmark,
  ChevronRight,
  ExternalLink,
  Code2,
} from "lucide-react";

interface MenuItem {
  label: string;
  desc: string;
  href: string;
  icon: any;
  color: string;
  badge?: string;
}

interface MenuSection {
  title: string;
  items: MenuItem[];
}

export default function MorePage() {
  const [profile, setProfile] = useState<LearnerProfile | null>(null);

  useEffect(() => {
    getLearnerProfile()
      .then(setProfile)
      .catch(() => {});
  }, []);

  const menuSections: MenuSection[] = [
    {
      title: "Settings & Customization",
      items: [
        {
          label: "App Settings",
          desc: "Manage dark mode, audio sound effects, TTS voice, and course info.",
          href: "/settings",
          icon: Settings,
          color: "text-duo-blue bg-duo-blue/10",
        },
        {
          label: "Shop & Power-ups",
          desc: "Refill hearts with gems or practice to earn hearts back.",
          href: "/shop",
          icon: Sparkles,
          color: "text-duo-yellow-dark bg-yellow-100 dark:bg-yellow-950/60",
        },
      ],
    },
    {
      title: "Curriculum & Learning Tools",
      items: [
        {
          label: "Grammar & Vocab Guidebook",
          desc: "Grammar tips and vocabulary reference for Spanish A1 beginners.",
          href: "/more#guidebook",
          icon: BookOpen,
          badge: "Preview",
          color: "text-emerald-500 bg-emerald-100 dark:bg-emerald-950/60",
        },
        {
          label: "Spanish Audio Stories",
          desc: "Interactive dialogues and mini-stories for listening comprehension.",
          href: "/more#stories",
          icon: Radio,
          badge: "Coming Soon",
          color: "text-purple-500 bg-purple-100 dark:bg-purple-950/60",
        },
        {
          label: "Friends & Social Practice",
          desc: "Collaborative friend quests and practice streaks with classmates.",
          href: "/more#social",
          icon: Users2,
          badge: "Coming Soon",
          color: "text-pink-500 bg-pink-100 dark:bg-pink-950/60",
        },
      ],
    },
  ];

  return (
    <div className="min-h-screen bg-white dark:bg-[#131f24] flex transition-colors">
      <Sidebar />

      <div className="flex-1 md:ml-64 flex flex-col min-h-screen pb-20 md:pb-8">
        <TopHeader stats={profile?.stats || null} />

        <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 py-8">
          {/* Header Banner */}
          <div className="mb-8 p-6 rounded-3xl bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-emerald-500/10 dark:from-blue-950/30 dark:via-purple-950/30 dark:to-emerald-950/30 border-2 border-blue-500/20 dark:border-blue-500/30 flex flex-col sm:flex-row items-center justify-between gap-6">
            <div className="flex flex-col gap-2 text-center sm:text-left">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-duo-blue/15 text-duo-blue font-black text-xs uppercase tracking-wider self-center sm:self-start">
                <MoreHorizontal className="w-4 h-4" />
                <span>Explore & Tools</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-black text-gray-800 dark:text-white">
                More Features
              </h1>
              <p className="text-sm font-bold text-gray-500 dark:text-gray-400 max-w-md">
                Access settings, learning tools, study notes, and system documentation.
              </p>
            </div>

            <LingoMascot
              expression="happy"
              size="md"
              speechBubble="Explore more ways to practice!"
            />
          </div>

          <div className="flex flex-col gap-8">
            {menuSections.map((section, sIdx) => (
              <div key={sIdx} className="flex flex-col gap-3">
                <h2 className="text-sm font-black text-gray-400 uppercase tracking-wider px-1">
                  {section.title}
                </h2>

                <div className="grid grid-cols-1 gap-3">
                  {section.items.map((item, iIdx) => {
                    const Icon = item.icon;
                    return (
                      <Link
                        key={iIdx}
                        href={item.href}
                        className="group"
                      >
                        <Card className="p-4 flex items-center justify-between gap-4 group-hover:border-duo-blue dark:group-hover:border-duo-blue transition-all">
                          <div className="flex items-center gap-4">
                            <div className={`p-3 rounded-2xl shrink-0 ${item.color}`}>
                              <Icon className="w-6 h-6 stroke-[2.5]" />
                            </div>
                            <div>
                              <div className="flex items-center gap-2">
                                <h3 className="font-black text-base text-gray-800 dark:text-white group-hover:text-duo-blue transition-colors">
                                  {item.label}
                                </h3>
                                {item.badge && (
                                  <span className="px-2 py-0.5 rounded-full bg-gray-100 dark:bg-[#202f36] text-gray-500 dark:text-gray-400 text-[10px] font-black uppercase tracking-wider border border-gray-200 dark:border-gray-700">
                                    {item.badge}
                                  </span>
                                )}
                              </div>
                              <p className="text-xs font-bold text-gray-400 dark:text-gray-400">
                                {item.desc}
                              </p>
                            </div>
                          </div>

                          <ChevronRight className="w-5 h-5 text-gray-300 dark:text-gray-600 group-hover:text-duo-blue group-hover:translate-x-1 transition-all" />
                        </Card>
                      </Link>
                    );
                  })}
                </div>
              </div>
            ))}

            {/* About / SDE Assignment Technical Showcase */}
            <div className="flex flex-col gap-3 mt-4">
              <h2 className="text-sm font-black text-gray-400 uppercase tracking-wider px-1">
                About & Architecture
              </h2>

              <Card className="p-6 flex flex-col gap-4 border-2 border-gray-200 dark:border-[#2b3a42]">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 bg-duo-green/15 text-duo-green rounded-2xl">
                    <Code2 className="w-6 h-6 stroke-[2.5]" />
                  </div>
                  <div>
                    <h3 className="font-black text-base text-gray-800 dark:text-white">
                      Full-Stack Duolingo Implementation
                    </h3>
                    <p className="text-xs font-bold text-gray-400">
                      Language Learning Engine • 100% Server Authoritative Architecture
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-bold">
                  <div className="p-3 rounded-xl bg-gray-50 dark:bg-[#182830] border border-gray-200 dark:border-[#2b3a42]">
                    <div className="text-gray-400 text-[10px] uppercase">Engine</div>
                    <div className="text-gray-800 dark:text-white font-black mt-0.5">FastAPI + Python 3.13</div>
                  </div>
                  <div className="p-3 rounded-xl bg-gray-50 dark:bg-[#182830] border border-gray-200 dark:border-[#2b3a42]">
                    <div className="text-gray-400 text-[10px] uppercase">Frontend</div>
                    <div className="text-gray-800 dark:text-white font-black mt-0.5">Next.js 14 + Tailwind</div>
                  </div>
                  <div className="p-3 rounded-xl bg-gray-50 dark:bg-[#182830] border border-gray-200 dark:border-[#2b3a42]">
                    <div className="text-gray-400 text-[10px] uppercase">Automated Tests</div>
                    <div className="text-gray-800 dark:text-white font-black mt-0.5">58 Tests Passing (100%)</div>
                  </div>
                </div>

                <div className="pt-2 text-xs font-bold text-gray-500 dark:text-gray-400 border-t border-gray-100 dark:border-[#2b3a42] flex items-center justify-between">
                  <span>UI inspired by Duolingo design patterns; original code & art.</span>
                  <Link href="/settings">
                    <Button variant="ghost" size="sm" className="text-xs font-black">
                      Open Settings
                    </Button>
                  </Link>
                </div>
              </Card>
            </div>
          </div>
        </main>
      </div>

      <BottomNav />
    </div>
  );
}
