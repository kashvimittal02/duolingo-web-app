"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopHeader } from "@/components/layout/TopHeader";
import { BottomNav } from "@/components/layout/BottomNav";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { LingoMascot } from "@/components/mascot/LingoMascot";
import { RewardIcon } from "@/components/rewards/RewardIcon";
import { getLearnerProfile } from "@/lib/api";
import { LearnerProfile } from "@/lib/types";
import {
  Target,
  Zap,
  Flame,
  CheckCircle2,
  Trophy,
  Sparkles,
  Timer,
  ArrowRight,
  Gem,
} from "lucide-react";

export default function QuestsPage() {
  const [profile, setProfile] = useState<LearnerProfile | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchProfile = async () => {
    try {
      const data = await getLearnerProfile();
      setProfile(data);
    } catch {
      // Handled gracefully
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const stats = profile?.stats;
  const dailyXp = stats?.daily_xp ?? 0;
  const dailyGoal = stats?.daily_xp_goal ?? 50;
  const dailyPercent = Math.min(100, Math.round((dailyXp / dailyGoal) * 100));
  const dailyCompleted = dailyXp >= dailyGoal;

  const streakDays = stats?.streak ?? 0;
  const streakGoal = 7;
  const streakPercent = Math.min(100, Math.round((streakDays / streakGoal) * 100));

  return (
    <div className="min-h-screen bg-white dark:bg-[#131f24] flex transition-colors">
      <Sidebar />

      <div className="flex-1 md:ml-64 flex flex-col min-h-screen pb-20 md:pb-8">
        <TopHeader stats={profile?.stats || null} onStatsUpdated={fetchProfile} />

        <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 py-8">
          {/* Header Banner with Mascot */}
          <div className="mb-8 p-6 rounded-3xl bg-gradient-to-r from-emerald-500/10 via-teal-500/10 to-sky-500/10 dark:from-emerald-950/30 dark:via-teal-950/30 dark:to-sky-950/30 border-2 border-emerald-500/20 dark:border-emerald-500/30 flex flex-col sm:flex-row items-center justify-between gap-6">
            <div className="flex flex-col gap-2 text-center sm:text-left">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-duo-green/15 text-duo-green font-black text-xs uppercase tracking-wider self-center sm:self-start">
                <Target className="w-4 h-4" />
                <span>Daily & Weekly Goals</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-black text-gray-800 dark:text-white">
                Daily Quests
              </h1>
              <p className="text-sm font-bold text-gray-500 dark:text-gray-400 max-w-md">
                Complete quests every day to build language habits, level up your streak, and earn bonus rewards!
              </p>
            </div>

            <LingoMascot
              expression={dailyCompleted ? "cheering" : "happy"}
              size="md"
              speechBubble={
                dailyCompleted
                  ? "Quest complete! ¡Excelente!"
                  : `${Math.max(0, dailyGoal - dailyXp)} XP left today!`
              }
            />
          </div>

          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 gap-4">
              <div className="w-10 h-10 border-4 border-duo-green border-t-transparent rounded-full animate-spin" />
              <p className="text-gray-400 dark:text-gray-500 font-extrabold text-sm uppercase tracking-wider">
                Loading Quests...
              </p>
            </div>
          ) : (
            <div className="flex flex-col gap-5">
              {/* Quest 1: Daily XP Goal */}
              <Card className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-5 hover:border-amber-300 dark:hover:border-amber-700 transition-all">
                <div className="flex items-start gap-4 flex-1">
                  <div className="p-3.5 bg-amber-100 dark:bg-amber-950/60 rounded-2xl shrink-0 flex items-center justify-center">
                    <RewardIcon name="star" size={28} animate />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-black text-base text-gray-800 dark:text-white">
                        Earn {dailyGoal} XP Today
                      </h3>
                      {dailyCompleted && (
                        <span className="px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 text-xs font-black flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          Done
                        </span>
                      )}
                    </div>
                    <p className="text-xs font-bold text-gray-400 dark:text-gray-400 mb-3">
                      Complete lessons or practice sessions to hit your daily learning target.
                    </p>

                    {/* Progress Bar */}
                    <div className="w-full max-w-md bg-gray-100 dark:bg-[#283b44] h-3.5 rounded-full overflow-hidden border border-gray-200 dark:border-[#37464f]">
                      <div
                        className="bg-duo-yellow h-full transition-all duration-300 rounded-full"
                        style={{ width: `${dailyPercent}%` }}
                      />
                    </div>
                  </div>
                </div>

                <div className="flex sm:flex-col items-center justify-between sm:items-end w-full sm:w-auto shrink-0 pt-2 sm:pt-0 border-t sm:border-t-0 border-gray-100 dark:border-[#2b3a42]">
                  <span className="text-sm font-black text-amber-900 dark:text-amber-300">
                    {dailyXp} / {dailyGoal} XP
                  </span>
                  <div className="flex items-center gap-1 text-xs font-black text-gray-500 dark:text-gray-400 mt-1">
                    <RewardIcon name="gem" size={16} />
                    <span>+20 Gems</span>
                  </div>
                </div>
              </Card>

              {/* Quest 2: Streak Keeper Challenge */}
              <Card className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-5 hover:border-orange-300 dark:hover:border-orange-700 transition-all">
                <div className="flex items-start gap-4 flex-1">
                  <div className="p-3.5 bg-orange-100 dark:bg-orange-950/60 rounded-2xl shrink-0 flex items-center justify-center">
                    <RewardIcon name="fire" size={28} />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-black text-base text-gray-800 dark:text-white">
                        7-Day Streak Challenge
                      </h3>
                      {streakDays >= 7 && (
                        <span className="px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 text-xs font-black flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          Achieved
                        </span>
                      )}
                    </div>
                    <p className="text-xs font-bold text-gray-400 dark:text-gray-400 mb-3">
                      Maintain a daily practice streak to form consistent retention habits.
                    </p>

                    {/* Progress Bar */}
                    <div className="w-full max-w-md bg-gray-100 dark:bg-[#283b44] h-3.5 rounded-full overflow-hidden border border-gray-200 dark:border-[#37464f]">
                      <div
                        className="bg-duo-orange h-full transition-all duration-300 rounded-full"
                        style={{ width: `${streakPercent}%` }}
                      />
                    </div>
                  </div>
                </div>

                <div className="flex sm:flex-col items-center justify-between sm:items-end w-full sm:w-auto shrink-0 pt-2 sm:pt-0 border-t sm:border-t-0 border-gray-100 dark:border-[#2b3a42]">
                  <span className="text-sm font-black text-orange-900 dark:text-orange-300">
                    {streakDays} / 7 Days
                  </span>
                  <div className="flex items-center gap-1 text-xs font-black text-gray-500 dark:text-gray-400 mt-1">
                    <Sparkles className="w-3.5 h-3.5 text-duo-orange" />
                    <span>Streak Shield</span>
                  </div>
                </div>
              </Card>

              {/* Quest 3: Lesson Mastery */}
              <Card className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-5 hover:border-emerald-300 dark:hover:border-emerald-700 transition-all">
                <div className="flex items-start gap-4 flex-1">
                  <div className="p-3.5 bg-emerald-100 dark:bg-emerald-950/60 rounded-2xl shrink-0 flex items-center justify-center">
                    <RewardIcon name="trophy" size={28} />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-black text-base text-gray-800 dark:text-white">
                        Crown Collector
                      </h3>
                      {profile && profile.total_crowns >= 5 && (
                        <span className="px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 text-xs font-black flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          Mastered
                        </span>
                      )}
                    </div>
                    <p className="text-xs font-bold text-gray-400 dark:text-gray-400 mb-3">
                      Earn crowns by completing all skill levels in the Spanish curriculum.
                    </p>

                    <div className="w-full max-w-md bg-gray-100 dark:bg-[#283b44] h-3.5 rounded-full overflow-hidden border border-gray-200 dark:border-[#37464f]">
                      <div
                        className="bg-duo-green h-full transition-all duration-300 rounded-full"
                        style={{
                          width: `${Math.min(100, ((profile?.total_crowns || 0) / 10) * 100)}%`,
                        }}
                      />
                    </div>
                  </div>
                </div>

                <div className="flex sm:flex-col items-center justify-between sm:items-end w-full sm:w-auto shrink-0 pt-2 sm:pt-0 border-t sm:border-t-0 border-gray-100 dark:border-[#2b3a42]">
                  <span className="text-sm font-black text-emerald-900 dark:text-emerald-300">
                    {profile?.total_crowns || 0} / 10 Crowns
                  </span>
                  <div className="flex items-center gap-1 text-xs font-black text-gray-500 dark:text-gray-400 mt-1">
                    <RewardIcon name="trophy" size={16} />
                    <span>Mastery Badge</span>
                  </div>
                </div>
              </Card>

              {/* Quest 4: Legendary Timed Challenge Mode */}
              <Card className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-5 border-2 border-indigo-200 dark:border-indigo-800/80 bg-indigo-50/40 dark:bg-indigo-950/20 hover:border-indigo-400 dark:hover:border-indigo-600 transition-all">
                <div className="flex items-start gap-4 flex-1">
                  <div className="p-3.5 bg-indigo-100 dark:bg-indigo-900/60 rounded-2xl shrink-0">
                    <Timer className="w-7 h-7 text-indigo-600 dark:text-indigo-400 stroke-[2.5]" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-black text-base text-gray-800 dark:text-white">
                        Legendary Timed Challenge
                      </h3>
                      <span className="px-2 py-0.5 rounded-full bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 text-xs font-black uppercase tracking-wider">
                        90s Blitz
                      </span>
                    </div>
                    <p className="text-xs font-bold text-gray-500 dark:text-gray-400 mb-2">
                      Answer questions against the strict 90-second server countdown with zero strikes allowed. No hearts lost on failure!
                    </p>
                    <div className="flex items-center gap-3 text-xs font-black text-indigo-700 dark:text-indigo-300">
                      <span className="flex items-center gap-1">
                        <Zap className="w-3.5 h-3.5 fill-indigo-500" />
                        +20 Legendary XP
                      </span>
                      <span>•</span>
                      <span>No Hearts Lost</span>
                      <span>•</span>
                      <span>Server Authoritative</span>
                    </div>
                  </div>
                </div>

                <div className="w-full sm:w-auto shrink-0 pt-2 sm:pt-0">
                  <Link href="/">
                    <Button variant="blue" size="md" className="w-full sm:w-auto flex items-center justify-center gap-2">
                      <span>Go to Learn Path</span>
                      <ArrowRight className="w-4 h-4" />
                    </Button>
                  </Link>
                </div>
              </Card>
            </div>
          )}
        </main>
      </div>

      <BottomNav />
    </div>
  );
}
