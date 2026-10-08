"use client";

import React, { useEffect, useState } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopHeader } from "@/components/layout/TopHeader";
import { BottomNav } from "@/components/layout/BottomNav";
import { Card } from "@/components/ui/Card";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import { getLearnerProfile } from "@/lib/api";
import { LearnerProfile } from "@/lib/types";
import {
  Flame,
  Zap,
  Crown,
  Gem,
  Heart,
  Calendar,
  Sparkles,
  Award,
  Settings,
} from "lucide-react";

export default function ProfilePage() {
  const [profile, setProfile] = useState<LearnerProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        setLoading(true);
        const data = await getLearnerProfile();
        setProfile(data);
      } catch (err: any) {
        setError(err.message || "Failed to load learner profile");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const formatDate = (isoString: string) => {
    try {
      const d = new Date(isoString);
      return d.toLocaleDateString("en-US", {
        month: "long",
        year: "numeric",
      });
    } catch {
      return "Recently";
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-[#131f24] flex transition-colors">
      <Sidebar />

      <div className="flex-1 md:ml-64 flex flex-col min-h-screen pb-20 md:pb-8">
        <TopHeader stats={profile?.stats || null} />

        <main className="flex-1 max-w-3xl mx-auto w-full px-4 sm:px-6 py-8">
          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 gap-3">
              <div className="w-10 h-10 border-4 border-duo-green border-t-transparent rounded-full animate-spin" />
              <p className="text-xs font-black text-gray-400 uppercase tracking-wider">
                Loading Profile...
              </p>
            </div>
          ) : error || !profile ? (
            <div className="p-6 rounded-2xl bg-red-50 dark:bg-red-950/40 text-duo-red text-center font-bold text-sm">
              {error || "Could not load profile"}
            </div>
          ) : (
            <div className="flex flex-col gap-8">
              {/* Profile Card */}
              <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6 p-6 rounded-3xl bg-gray-50 dark:bg-[#202f36] border-2 border-gray-200 dark:border-[#37464f]">
                <div className="w-24 h-24 rounded-full bg-duo-green text-white font-black text-4xl flex items-center justify-center shadow-[0_4px_0_0_#46a302] border-4 border-white dark:border-[#202f36]">
                  {profile.display_name.charAt(0)}
                </div>

                <div className="text-center sm:text-left flex-1">
                  <h1 className="text-2xl sm:text-3xl font-black text-gray-800 dark:text-white">
                    {profile.display_name}
                  </h1>
                  <p className="text-sm font-extrabold text-gray-400 dark:text-gray-400 mb-3">
                    @{profile.username}
                  </p>

                  <div className="flex items-center justify-center sm:justify-start gap-2 text-xs font-bold text-gray-500 dark:text-gray-400">
                    <Calendar className="w-4 h-4 text-gray-400" />
                    <span>Joined {formatDate(profile.created_at)}</span>
                  </div>
                </div>
              </div>

              {/* Preferences & Settings */}
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <Settings className="w-6 h-6 text-duo-blue" />
                  <h2 className="text-xl font-black text-gray-800 dark:text-white">
                    Preferences & Settings
                  </h2>
                </div>

                <Card className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6">
                  <div>
                    <h3 className="font-black text-base text-gray-800 dark:text-white">
                      Appearance Theme
                    </h3>
                    <p className="text-xs font-bold text-gray-500 dark:text-gray-400">
                      Choose your preferred color theme across the app.
                    </p>
                  </div>
                  <ThemeToggle variant="segmented" className="w-full sm:w-72" />
                </Card>
              </div>

              {/* Statistics Grid */}
              <div>
                <h2 className="text-xl font-black text-gray-800 dark:text-white mb-4">
                  Statistics
                </h2>

                <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                  {/* Total XP */}
                  <Card className="flex flex-col gap-2 p-4">
                    <div className="flex items-center gap-2 text-duo-yellow-dark">
                      <Zap className="w-5 h-5 fill-duo-yellow text-duo-yellow" />
                      <span className="text-xs font-black uppercase text-gray-500 dark:text-gray-400">
                        Total XP
                      </span>
                    </div>
                    <span className="text-2xl font-black text-gray-800 dark:text-white">
                      {profile.stats.xp}
                    </span>
                  </Card>

                  {/* Daily Streak */}
                  <Card className="flex flex-col gap-2 p-4">
                    <div className="flex items-center gap-2 text-duo-orange">
                      <Flame className="w-5 h-5 fill-duo-orange text-duo-orange" />
                      <span className="text-xs font-black uppercase text-gray-500 dark:text-gray-400">
                        Day Streak
                      </span>
                    </div>
                    <span className="text-2xl font-black text-gray-800 dark:text-white">
                      {profile.stats.streak}
                    </span>
                  </Card>

                  {/* Crowns */}
                  <Card className="flex flex-col gap-2 p-4">
                    <div className="flex items-center gap-2 text-amber-600">
                      <Crown className="w-5 h-5 fill-amber-400 text-amber-500" />
                      <span className="text-xs font-black uppercase text-gray-500 dark:text-gray-400">
                        Crowns
                      </span>
                    </div>
                    <span className="text-2xl font-black text-gray-800 dark:text-white">
                      {profile.total_crowns}
                    </span>
                  </Card>

                  {/* Gems */}
                  <Card className="flex flex-col gap-2 p-4">
                    <div className="flex items-center gap-2 text-duo-blue">
                      <Gem className="w-5 h-5 fill-duo-blue text-duo-blue" />
                      <span className="text-xs font-black uppercase text-gray-500 dark:text-gray-400">
                        Gems
                      </span>
                    </div>
                    <span className="text-2xl font-black text-gray-800 dark:text-white">
                      {profile.stats.gems}
                    </span>
                  </Card>

                  {/* Hearts */}
                  <Card className="flex flex-col gap-2 p-4">
                    <div className="flex items-center gap-2 text-duo-red">
                      <Heart className="w-5 h-5 fill-duo-red text-duo-red" />
                      <span className="text-xs font-black uppercase text-gray-500 dark:text-gray-400">
                        Hearts
                      </span>
                    </div>
                    <span className="text-2xl font-black text-gray-800 dark:text-white">
                      {profile.stats.hearts} / {profile.stats.max_hearts}
                    </span>
                  </Card>

                  {/* Practice Status */}
                  <Card className="flex flex-col gap-2 p-4">
                    <div className="flex items-center gap-2 text-duo-green">
                      <Sparkles className="w-5 h-5 text-duo-green" />
                      <span className="text-xs font-black uppercase text-gray-500 dark:text-gray-400">
                        Today
                      </span>
                    </div>
                    <span className="text-base font-black text-gray-800 dark:text-white">
                      {profile.stats.has_practiced_today
                        ? "Practiced ✅"
                        : "Ready! 🎯"}
                    </span>
                  </Card>
                </div>
              </div>

              {/* Achievements Section */}
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <Award className="w-6 h-6 text-duo-yellow-dark" />
                  <h2 className="text-xl font-black text-gray-800 dark:text-white">
                    Achievements
                  </h2>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {profile.achievements && profile.achievements.map((ach) => (
                    <Card
                      key={ach.id}
                      className={`flex items-start gap-4 p-4 transition-all ${
                        ach.is_unlocked
                          ? "bg-white dark:bg-[#202f36] border-amber-300 dark:border-amber-500/50 shadow-[0_3px_0_0_#fcd34d] dark:shadow-[0_3px_0_0_#78350f]"
                          : "bg-gray-50 dark:bg-[#182830] border-gray-200 dark:border-[#37464f] opacity-60"
                      }`}
                    >
                      <div
                        className={`w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 font-black text-xl shadow-sm ${
                          ach.is_unlocked
                            ? "bg-amber-100 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400"
                            : "bg-gray-200 dark:bg-[#2b3a42] text-gray-400 dark:text-gray-500"
                        }`}
                      >
                        {ach.is_unlocked ? "🏆" : "🔒"}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between gap-2">
                          <h3 className="font-extrabold text-base text-gray-800 dark:text-white leading-tight">
                            {ach.title}
                          </h3>
                          {ach.is_unlocked && (
                            <span className="text-[10px] font-black uppercase text-amber-700 dark:text-amber-300 bg-amber-100 dark:bg-amber-950/60 px-2 py-0.5 rounded-full shrink-0">
                              Unlocked
                            </span>
                          )}
                        </div>
                        <p className="text-xs font-bold text-gray-500 dark:text-gray-400 mt-0.5">
                          {ach.description}
                        </p>
                        {ach.is_unlocked && ach.unlocked_at && (
                          <span className="text-[10px] font-bold text-gray-400 dark:text-gray-500 mt-1 block">
                            Earned {formatDate(ach.unlocked_at)}
                          </span>
                        )}
                      </div>
                    </Card>
                  ))}
                </div>
              </div>
            </div>
          )}
        </main>
      </div>

      <BottomNav />
    </div>
  );
}
