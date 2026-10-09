"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { LingoMascot } from "@/components/mascot/LingoMascot";
import { RewardIcon } from "@/components/rewards/RewardIcon";
import { getLeaderboard } from "@/lib/api";
import { LearnerProfile, LeaderboardResponse } from "@/lib/types";
import {
  Flame,
  Zap,
  Trophy,
  Award,
  Target,
  ArrowRight,
  Sparkles,
  ChevronRight,
} from "lucide-react";

interface RightRailProps {
  profile: LearnerProfile | null;
}

export const RightRail: React.FC<RightRailProps> = ({ profile }) => {
  const [leaderboard, setLeaderboard] = useState<LeaderboardResponse | null>(null);

  useEffect(() => {
    getLeaderboard()
      .then(setLeaderboard)
      .catch(() => {});
  }, []);

  const stats = profile?.stats;
  const streak = stats?.streak ?? 0;
  const dailyXp = stats?.daily_xp ?? 0;
  const dailyGoal = stats?.daily_xp_goal ?? 50;
  const dailyPercent = Math.min(100, Math.round((dailyXp / dailyGoal) * 100));

  // Top 3 competitors preview
  const topUsers = leaderboard?.rankings.slice(0, 3) || [];
  const userEntry = leaderboard?.rankings.find((r) => r.is_current_user);
  const userRank = userEntry?.rank;

  return (
    <aside className="hidden lg:flex flex-col gap-5 w-80 shrink-0 select-none lg:h-full lg:min-h-0 lg:overflow-y-auto lg:overflow-x-hidden lg:pr-2 lg:pb-16 custom-scrollbar overscroll-contain">
      {/* 1. Daily XP Goal Progress Card */}
      {stats && (
        <Card className="flex flex-col gap-3 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="p-2 bg-amber-100 dark:bg-amber-950/60 rounded-2xl shrink-0 flex items-center justify-center">
                <RewardIcon name="star" size={26} animate />
              </div>
              <div>
                <h3 className="font-black text-sm text-gray-800 dark:text-white">
                  Daily XP Goal
                </h3>
                <p className="text-xs font-bold text-gray-400 dark:text-gray-400">
                  {dailyPercent >= 100 ? "Goal completed!" : "Daily progress"}
                </p>
              </div>
            </div>
            <span className="text-sm font-black text-amber-900 dark:text-amber-300">
              {dailyXp} / {dailyGoal} XP
            </span>
          </div>

          <div className="w-full bg-gray-100 dark:bg-[#283b44] h-3 rounded-full overflow-hidden border border-gray-200 dark:border-[#37464f]">
            <div
              className="bg-duo-yellow h-full transition-all duration-300 rounded-full"
              style={{ width: `${dailyPercent}%` }}
            />
          </div>

          <div className="flex items-center justify-between text-xs pt-1">
            <Link
              href="/quests"
              className="text-duo-blue font-black hover:underline flex items-center gap-1"
            >
              <Target className="w-3.5 h-3.5" />
              <span>View Quests</span>
            </Link>
            <span className="text-gray-400 font-bold">
              {dailyPercent >= 100 ? "100%" : `${Math.max(0, dailyGoal - dailyXp)} XP remaining`}
            </span>
          </div>
        </Card>
      )}

      {/* 2. Streak Keeper Card */}
      {stats && (
        <Card className="flex flex-col gap-3 p-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-orange-100 dark:bg-orange-950/60 rounded-2xl shrink-0 flex items-center justify-center">
              <RewardIcon name="fire" size={28} />
            </div>
            <div>
              <h3 className="font-black text-base text-gray-800 dark:text-white">
                {streak} Day Streak
              </h3>
              <p className="text-xs font-bold text-gray-400 dark:text-gray-400">
                {streak > 0
                  ? "Practice daily to keep your streak burning!"
                  : "Complete a lesson today to ignite your streak!"}
              </p>
            </div>
          </div>
        </Card>
      )}

      {/* 3. Leaderboard League Preview Card */}
      <Card className="flex flex-col gap-3 p-4">
        <div className="flex items-center justify-between pb-2 border-b border-gray-100 dark:border-[#283b44]">
          <div className="flex items-center gap-2">
            <RewardIcon name="trophy" size={20} />
            <h3 className="font-black text-sm text-gray-800 dark:text-white">
              {leaderboard ? leaderboard.league_name : "Weekly League"}
            </h3>
          </div>
          {userRank && (
            <span className="text-xs font-black px-2 py-0.5 rounded-full bg-blue-100 dark:bg-[#1b3a4b] text-duo-blue dark:text-[#38bdf8]">
              Rank #{userRank}
            </span>
          )}
        </div>

        {/* Competitor rows */}
        <div className="flex flex-col gap-2">
          {topUsers.map((user) => {
            const isSelf = user.is_current_user;
            return (
              <div
                key={user.rank}
                className={`flex items-center justify-between px-2.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                  isSelf
                    ? "bg-duo-green-light dark:bg-[#0e3a22] text-duo-green-dark dark:text-emerald-300 font-black border border-duo-green"
                    : "text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-[#1c2c34]"
                }`}
              >
                <div className="flex items-center gap-2">
                  <span
                    className={`w-4 text-center font-black ${
                      user.rank === 1
                        ? "text-amber-500"
                        : user.rank === 2
                        ? "text-gray-400"
                        : user.rank === 3
                        ? "text-amber-700"
                        : "text-gray-400"
                    }`}
                  >
                    {user.rank}
                  </span>
                  <span className="truncate max-w-[130px]">{user.display_name}</span>
                </div>
                <span className="font-black">{user.xp} XP</span>
              </div>
            );
          })}
        </div>

        <Link href="/leaderboard" className="pt-1">
          <Button variant="ghost" size="sm" className="w-full text-xs font-black text-duo-blue flex items-center justify-center gap-1">
            <span>View Full Leaderboard</span>
            <ChevronRight className="w-4 h-4" />
          </Button>
        </Link>
      </Card>

      {/* 4. Daily Quests Preview Card */}
      <Card className="flex flex-col gap-3 p-4">
        <div className="flex items-center justify-between pb-1 border-b border-gray-100 dark:border-[#283b44]">
          <div className="flex items-center gap-2">
            <div className="p-1.5 bg-purple-100 dark:bg-purple-950/60 rounded-xl text-purple-600 dark:text-purple-400">
              <Target className="w-4 h-4 stroke-[2.5]" />
            </div>
            <h3 className="font-black text-sm text-gray-800 dark:text-white">
              Daily Quests
            </h3>
          </div>
          <Link
            href="/quests"
            className="text-xs font-black text-duo-blue hover:underline uppercase tracking-wide"
          >
            View All
          </Link>
        </div>

        <div className="flex flex-col gap-2 pt-1">
          <div className="flex items-center justify-between text-xs font-bold text-gray-700 dark:text-gray-200">
            <span>Earn {dailyGoal} XP today</span>
            <span className="font-black text-duo-green">{dailyXp}/{dailyGoal} XP</span>
          </div>
          <div className="w-full bg-gray-100 dark:bg-[#283b44] h-2.5 rounded-full overflow-hidden border border-gray-200 dark:border-[#37464f]">
            <div
              className="bg-duo-green h-full transition-all duration-300 rounded-full"
              style={{ width: `${dailyPercent}%` }}
            />
          </div>
        </div>
      </Card>

      {/* 5. Mascot Encouragement Banner */}
      <div className="p-4 rounded-3xl bg-gradient-to-br from-emerald-500/10 to-teal-500/10 dark:from-emerald-950/20 dark:to-teal-950/20 border-2 border-emerald-500/20 dark:border-emerald-500/30 flex flex-col items-center text-center gap-2">
        <LingoMascot
          expression={stats?.hearts === 0 ? "sad" : "happy"}
          size="md"
          speechBubble={stats?.hearts === 0 ? "Need hearts?" : "¡Tú puedes!"}
          bubblePosition="top"
        />
        <div className="flex flex-col gap-0.5 mt-1">
          <span className="text-xs font-black text-duo-green uppercase tracking-wider">
            Daily Motivation
          </span>
          <p className="text-xs font-bold text-gray-700 dark:text-gray-300">
            ¡Sigue practicando! Consistency is key to mastery.
          </p>
        </div>
      </div>
    </aside>
  );
};
