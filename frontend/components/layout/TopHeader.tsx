"use client";

import React, { useState } from "react";
import { Flame, Gem, Heart, Plus, Sparkles } from "lucide-react";
import { LearnerStats } from "@/lib/types";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import { refillHearts, practiceEarnHeart } from "@/lib/api";

interface TopHeaderProps {
  stats: LearnerStats | null;
  onStatsUpdated?: () => void;
}

export const TopHeader: React.FC<TopHeaderProps> = ({ stats, onStatsUpdated }) => {
  const [isHeartModalOpen, setIsHeartModalOpen] = useState(false);
  const [refillLoading, setRefillLoading] = useState(false);
  const [practiceLoading, setPracticeLoading] = useState(false);
  const [modalMessage, setModalMessage] = useState<string | null>(null);

  if (!stats) return null;

  const handleRefill = async () => {
    try {
      setRefillLoading(true);
      setModalMessage(null);
      const res = await refillHearts();
      setModalMessage(res.message);
      if (onStatsUpdated) onStatsUpdated();
    } catch (err: any) {
      setModalMessage(err.message || "Could not refill hearts");
    } finally {
      setRefillLoading(false);
    }
  };

  const handlePractice = async () => {
    try {
      setPracticeLoading(true);
      setModalMessage(null);
      const res = await practiceEarnHeart();
      setModalMessage(res.message);
      if (onStatsUpdated) onStatsUpdated();
    } catch (err: any) {
      setModalMessage(err.message || "Could not earn heart from practice");
    } finally {
      setPracticeLoading(false);
    }
  };

  return (
    <>
      <header className="sticky top-0 z-40 bg-white dark:bg-[#131f24] border-b-2 border-gray-200 dark:border-[#2b3a42] px-4 py-3 flex items-center justify-between shadow-sm transition-colors">
        <div className="flex items-center gap-2">
          <span className="text-xl font-extrabold text-duo-green tracking-wider uppercase md:hidden">
            Lingo
          </span>
        </div>

        {/* Gamification Stats Bar & Theme Toggle */}
        <div className="flex items-center gap-3 sm:gap-5">
          {/* Streak */}
          <div
            className="flex items-center gap-1.5 font-extrabold text-duo-orange cursor-default select-none"
            title={`${stats.streak} day streak`}
          >
            <Flame className="w-6 h-6 fill-duo-orange text-duo-orange" />
            <span className="text-base">{stats.streak}</span>
          </div>

          {/* Gems */}
          <div
            className="flex items-center gap-1.5 font-extrabold text-duo-blue cursor-default select-none"
            title={`${stats.gems} gems available`}
          >
            <Gem className="w-6 h-6 fill-duo-blue text-duo-blue" />
            <span className="text-base">{stats.gems}</span>
          </div>

          {/* Hearts */}
          <button
            onClick={() => {
              setModalMessage(null);
              setIsHeartModalOpen(true);
            }}
            className="flex items-center gap-1.5 font-extrabold text-duo-red hover:bg-red-50 dark:hover:bg-red-950/30 p-1.5 rounded-xl transition-colors cursor-pointer select-none"
            title="Manage hearts & refills"
          >
            <Heart className="w-6 h-6 fill-duo-red text-duo-red animate-pulse" />
            <span className="text-base">{stats.hearts}</span>
            {stats.hearts < stats.max_hearts && (
              <span className="bg-duo-red text-white p-0.5 rounded-full ml-0.5">
                <Plus className="w-3 h-3 stroke-[3]" />
              </span>
            )}
          </button>

          {/* Quick Theme Toggle */}
          <ThemeToggle variant="icon" />
        </div>
      </header>

      {/* Hearts Recovery & Refill Modal */}
      <Modal
        isOpen={isHeartModalOpen}
        onClose={() => setIsHeartModalOpen(false)}
        title="Hearts"
      >
        <div className="flex flex-col items-center text-center">
          <div className="w-20 h-20 rounded-full bg-red-100 dark:bg-red-950/40 flex items-center justify-center mb-4">
            <Heart className="w-12 h-12 fill-duo-red text-duo-red" />
          </div>

          <h3 className="text-2xl font-black text-gray-800 dark:text-gray-100 mb-1">
            {stats.hearts} / {stats.max_hearts} Hearts
          </h3>

          <p className="text-sm text-gray-500 dark:text-gray-400 mb-6 max-w-xs">
            Hearts keep you going! Answer exercises carefully to preserve your hearts, or refill when you run out.
          </p>

          {modalMessage && (
            <div className="w-full p-3 mb-4 rounded-xl bg-blue-50 dark:bg-[#1b3a4b] border border-blue-200 dark:border-[#2c5a73] text-duo-blue dark:text-[#38bdf8] text-sm font-bold">
              {modalMessage}
            </div>
          )}

          <div className="w-full flex flex-col gap-3">
            {/* Refill with Gems */}
            <Button
              variant="blue"
              fullWidth
              disabled={stats.hearts >= stats.max_hearts || stats.gems < 350 || refillLoading}
              onClick={handleRefill}
            >
              <div className="flex items-center justify-center gap-2">
                <Sparkles className="w-5 h-5" />
                <span>
                  {stats.hearts >= stats.max_hearts
                    ? "Hearts Full"
                    : "Refill (350 Gems)"}
                </span>
              </div>
            </Button>

            {/* Practice to recover 1 heart */}
            <Button
              variant="outline"
              fullWidth
              disabled={stats.hearts >= stats.max_hearts || practiceLoading}
              onClick={handlePractice}
            >
              <div className="flex items-center justify-center gap-2">
                <Heart className="w-5 h-5 text-duo-red fill-duo-red" />
                <span>Practice to Earn 1 Heart</span>
              </div>
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
};
