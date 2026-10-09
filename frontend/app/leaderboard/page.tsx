"use client";

import React, { useEffect, useState } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopHeader } from "@/components/layout/TopHeader";
import { BottomNav } from "@/components/layout/BottomNav";
import { Card } from "@/components/ui/Card";
import { LingoMascot } from "@/components/mascot/LingoMascot";
import { getLeaderboard, getLearnerProfile } from "@/lib/api";
import { LeaderboardResponse, LearnerProfile } from "@/lib/types";
import { Trophy, Medal, Sparkles, AlertCircle } from "lucide-react";

export default function LeaderboardPage() {
  const [leaderboard, setLeaderboard] = useState<LeaderboardResponse | null>(null);
  const [profile, setProfile] = useState<LearnerProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const [lbData, pData] = await Promise.all([
          getLeaderboard(),
          getLearnerProfile(),
        ]);
        setLeaderboard(lbData);
        setProfile(pData);
      } catch (err: any) {
        setError(err.message || "Failed to load leaderboard");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getRankBadge = (rank: number) => {
    switch (rank) {
      case 1:
        return (
          <div className="w-8 h-8 rounded-full bg-amber-400 text-white font-black flex items-center justify-center shadow-sm">
            🥇
          </div>
        );
      case 2:
        return (
          <div className="w-8 h-8 rounded-full bg-slate-300 text-white font-black flex items-center justify-center shadow-sm">
            🥈
          </div>
        );
      case 3:
        return (
          <div className="w-8 h-8 rounded-full bg-amber-700 text-white font-black flex items-center justify-center shadow-sm">
            🥉
          </div>
        );
      default:
        return (
          <span className="w-8 text-center font-black text-gray-500 text-sm">
            {rank}
          </span>
        );
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-[#131f24] flex transition-colors">
      <Sidebar />

      <div className="flex-1 md:ml-64 flex flex-col min-h-screen pb-20 md:pb-8">
        <TopHeader stats={profile?.stats || null} />

        <main className="flex-1 max-w-3xl mx-auto w-full px-4 sm:px-6 py-8">
          <div className="flex flex-col items-center text-center mb-8">
            <LingoMascot
              expression="cheering"
              size="md"
              speechBubble="Compete for the top spot!"
              className="mb-4"
            />
            <h1 className="text-2xl sm:text-3xl font-black text-gray-800 dark:text-white mb-1">
              Weekly Leaderboard
            </h1>
            <p className="text-sm font-bold text-gray-500 dark:text-gray-400 max-w-sm">
              Earn XP by completing lessons. Top learners advance each week!
            </p>
          </div>

          {loading ? (
            <div className="flex flex-col items-center justify-center py-16 gap-3">
              <div className="w-10 h-10 border-4 border-duo-green border-t-transparent rounded-full animate-spin" />
              <p className="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-wider">
                Loading Rankings...
              </p>
            </div>
          ) : error ? (
            <div className="p-6 rounded-2xl bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/60 text-center text-duo-red font-bold text-sm">
              {error}
            </div>
          ) : leaderboard ? (
            <div className="flex flex-col gap-2">
              {leaderboard.rankings.map((entry) => {
                const isCurrentUser = entry.is_current_user;

                return (
                  <div
                    key={entry.rank}
                    className={`
                      p-4 rounded-2xl border-2 flex items-center justify-between transition-all select-none
                      ${
                        isCurrentUser
                          ? "bg-duo-blue-light/70 dark:bg-[#1b3a4b] border-duo-blue shadow-[0_3px_0_0_#1899d6]"
                          : "bg-white dark:bg-[#202f36] border-gray-100 dark:border-[#37464f] hover:border-gray-200 dark:hover:border-[#4b5b66] shadow-sm"
                      }
                    `}
                  >
                    <div className="flex items-center gap-4">
                      {getRankBadge(entry.rank)}

                      <div className="w-11 h-11 rounded-full bg-gray-200 dark:bg-[#283b44] border-2 border-white dark:border-[#202f36] shadow-sm flex items-center justify-center font-black text-gray-600 dark:text-gray-200 text-base">
                        {entry.display_name.charAt(0)}
                      </div>

                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-extrabold text-base text-gray-800 dark:text-white">
                            {entry.display_name}
                          </span>
                          {isCurrentUser && (
                            <span className="px-2 py-0.5 bg-duo-blue text-white text-[10px] font-black uppercase rounded-full tracking-wider">
                              You
                            </span>
                          )}
                        </div>
                        <span className="text-xs font-bold text-gray-400 dark:text-gray-500">
                          @{entry.username}
                        </span>
                      </div>
                    </div>

                    <div className="text-right">
                      <span className="font-black text-base text-gray-700 dark:text-gray-200">
                        {entry.xp} XP
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : null}
        </main>
      </div>

      <BottomNav />
    </div>
  );
}
