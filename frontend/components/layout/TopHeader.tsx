"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import Image from "next/image";
import { useRouter } from "next/navigation";
import {
  Plus,
  Sparkles,
  ChevronDown,
  Check,
  ShoppingBag,
  CheckCircle2,
  Flame,
} from "lucide-react";
import { RewardIcon } from "@/components/rewards/RewardIcon";
import { LearnerStats } from "@/lib/types";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import { refillHearts } from "@/lib/api";

interface TopHeaderProps {
  stats: LearnerStats | null;
  onStatsUpdated?: () => void;
}

// Authentic Spain Flag SVG for the active Spanish course
const SpainFlag: React.FC<{ className?: string }> = ({ className = "w-6 h-4" }) => (
  <span
    className={`inline-block relative overflow-hidden rounded-[4px] shadow-xs border border-black/15 shrink-0 ${className}`}
    style={{ aspectRatio: "3 / 2" }}
    aria-label="Flag of Spain"
    role="img"
  >
    <svg viewBox="0 0 750 500" className="w-full h-full block">
      {/* Top red stripe */}
      <rect width="750" height="125" fill="#c60b1e" />
      {/* Middle yellow stripe (double height: 250px) */}
      <rect width="750" height="250" y="125" fill="#ffc400" />
      {/* Bottom red stripe */}
      <rect width="750" height="125" y="375" fill="#c60b1e" />
      {/* Iconic Spanish coat of arms silhouette */}
      <g transform="translate(240, 250) scale(0.7)">
        <path
          d="M-36 -50 h72 v60 c0 30 -36 50 -36 50 c0 0 -36 -20 -36 -50 z"
          fill="#c60b1e"
          stroke="#850814"
          strokeWidth="6"
        />
        <circle cx="0" cy="-6" r="16" fill="#ffc400" />
        <path d="M-22 -65 h44 v12 h-44 z" fill="#f59e0b" />
      </g>
    </svg>
  </span>
);

export const TopHeader: React.FC<TopHeaderProps> = ({ stats, onStatsUpdated }) => {
  const router = useRouter();
  const [isHeartModalOpen, setIsHeartModalOpen] = useState(false);
  const [isGemModalOpen, setIsGemModalOpen] = useState(false);
  const [isStreakModalOpen, setIsStreakModalOpen] = useState(false);
  const [isCourseDropdownOpen, setIsCourseDropdownOpen] = useState(false);
  const [courseNotice, setCourseNotice] = useState<string | null>(null);

  const [refillLoading, setRefillLoading] = useState(false);
  const [modalMessage, setModalMessage] = useState<string | null>(null);

  const courseDropdownRef = useRef<HTMLDivElement>(null);

  // Close course dropdown on outside click or Escape key
  useEffect(() => {
    if (!isCourseDropdownOpen) return;

    const handleClickOutside = (event: MouseEvent) => {
      if (
        courseDropdownRef.current &&
        !courseDropdownRef.current.contains(event.target as Node)
      ) {
        setIsCourseDropdownOpen(false);
        setCourseNotice(null);
      }
    };

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setIsCourseDropdownOpen(false);
        setCourseNotice(null);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isCourseDropdownOpen]);

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

  const handlePractice = () => {
    if (stats.hearts >= stats.max_hearts) {
      setModalMessage("Hearts are already full!");
      return;
    }
    setIsHeartModalOpen(false);
    router.push("/practice");
  };

  return (
    <>
      <header className="sticky top-0 z-40 shrink-0 bg-white dark:bg-[#131f24] border-b-2 border-gray-200 dark:border-[#2b3a42] px-4 py-2.5 flex items-center justify-between shadow-sm transition-colors">
        {/* Mobile App Brand Logo with standalone mascot */}
        <div className="flex items-center gap-2 md:hidden">
          <Link
            href="/"
            className="flex items-center gap-2.5 select-none hover:opacity-95 transition-opacity"
            aria-label="LingoApp Home"
          >
            <div className="w-[42px] h-[42px] shrink-0 flex items-center justify-center">
              <Image
                src="/images/mascot/mascot-happy.svg"
                alt="LingoApp Mascot"
                width={42}
                height={42}
                className="w-full h-full object-contain pointer-events-none"
                priority
              />
            </div>
            <span className="text-xl font-black text-duo-green tracking-wider uppercase">
              LingoApp
            </span>
          </Link>
        </div>

        {/* Right-aligned Top-Bar Controls (Far Right) */}
        <div className="ml-auto flex items-center gap-2 sm:gap-3.5">
          {/* 1. Course Flag Selector */}
          <div className="relative" ref={courseDropdownRef}>
            <button
              type="button"
              onClick={() => {
                setIsCourseDropdownOpen((prev) => !prev);
                setCourseNotice(null);
              }}
              className="flex items-center gap-1.5 p-1.5 rounded-xl hover:bg-gray-100 dark:hover:bg-[#1a2c35] border border-transparent hover:border-gray-200 dark:hover:border-[#2b3a42] transition-colors cursor-pointer select-none"
              title="Course: Spanish. Click to switch course."
              aria-label="Course selector: Spanish"
              aria-expanded={isCourseDropdownOpen}
              aria-haspopup="true"
            >
              <SpainFlag className="w-6 h-4" />
              <ChevronDown
                className={`w-3.5 h-3.5 text-gray-500 dark:text-gray-400 transition-transform ${
                  isCourseDropdownOpen ? "rotate-180" : ""
                }`}
              />
            </button>

            {/* Course Selector Dropdown */}
            {isCourseDropdownOpen && (
              <div
                className="absolute right-0 mt-2 w-64 bg-white dark:bg-[#131f24] border-2 border-gray-200 dark:border-[#2b3a42] rounded-2xl shadow-xl p-3 z-50 select-none animate-in fade-in zoom-in-95 duration-100"
                role="menu"
              >
                <div className="px-2 py-1 text-[11px] font-black uppercase tracking-wider text-gray-400 dark:text-gray-500">
                  MY COURSES
                </div>

                {/* Selected Active Course (Spanish) */}
                <div
                  className="flex items-center justify-between p-2.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border-2 border-duo-green text-emerald-900 dark:text-emerald-100 my-1 cursor-default"
                  role="menuitem"
                >
                  <div className="flex items-center gap-3">
                    <SpainFlag className="w-7 h-5" />
                    <div>
                      <p className="text-sm font-black leading-tight text-gray-800 dark:text-white">
                        Spanish
                      </p>
                      <p className="text-[10px] font-extrabold text-duo-green">
                        Active Course
                      </p>
                    </div>
                  </div>
                  <Check className="w-4 h-4 stroke-[3] text-duo-green" />
                </div>

                {/* Inline Notice if Add Course clicked */}
                {courseNotice && (
                  <div className="my-2 p-2 rounded-xl bg-blue-50 dark:bg-[#1b3a4b] border border-blue-200 dark:border-[#2c5a73] text-xs font-bold text-duo-blue dark:text-[#38bdf8] text-center">
                    {courseNotice}
                  </div>
                )}

                {/* Add a new course option */}
                <button
                  type="button"
                  onClick={() => {
                    setCourseNotice("Coming soon! More language courses are under development.");
                  }}
                  className="w-full mt-1 flex items-center gap-3 p-2.5 rounded-xl text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-[#1a2c35] text-left transition-colors cursor-pointer text-xs font-black uppercase tracking-wider"
                  role="menuitem"
                >
                  <div className="w-7 h-5 rounded-[4px] border-2 border-dashed border-gray-300 dark:border-gray-600 flex items-center justify-center text-gray-400">
                    <Plus className="w-3.5 h-3.5" />
                  </div>
                  <span>Add a new course</span>
                </button>
              </div>
            )}
          </div>

          {/* 2. Streak / Fire Counter Button */}
          <button
            type="button"
            onClick={() => setIsStreakModalOpen(true)}
            className="flex items-center gap-1.5 font-extrabold text-duo-orange hover:bg-orange-50 dark:hover:bg-orange-950/30 p-1.5 rounded-xl transition-colors cursor-pointer select-none"
            title={`${stats.streak} day streak. Click for details.`}
            aria-label={`${stats.streak} day streak`}
          >
            <RewardIcon name="fire" size={24} animate />
            <span className="text-base">{stats.streak}</span>
          </button>

          {/* 3. Gems Counter Button */}
          <button
            type="button"
            onClick={() => setIsGemModalOpen(true)}
            className="flex items-center gap-1.5 font-extrabold text-duo-blue hover:bg-blue-50 dark:hover:bg-blue-950/30 p-1.5 rounded-xl transition-colors cursor-pointer select-none"
            title={`${stats.gems} gems. Click for details.`}
            aria-label={`${stats.gems} gems available`}
          >
            <RewardIcon name="gem" size={24} animate />
            <span className="text-base">{stats.gems}</span>
          </button>

          {/* 4. Hearts Counter Button */}
          <button
            type="button"
            onClick={() => {
              setModalMessage(null);
              setIsHeartModalOpen(true);
            }}
            className="flex items-center gap-1.5 font-extrabold text-duo-red hover:bg-red-50 dark:hover:bg-red-950/30 p-1.5 rounded-xl transition-colors cursor-pointer select-none"
            title={`${stats.hearts} hearts. Manage hearts & refills.`}
            aria-label={`${stats.hearts} hearts out of ${stats.max_hearts}`}
          >
            <RewardIcon name="heart" size={24} animate />
            <span className="text-base">{stats.hearts}</span>
            {stats.hearts < stats.max_hearts && (
              <span className="bg-duo-red text-white p-0.5 rounded-full ml-0.5">
                <Plus className="w-3 h-3 stroke-[3]" />
              </span>
            )}
          </button>

          {/* 5. Theme / Settings Button */}
          <ThemeToggle variant="icon" />
        </div>
      </header>

      {/* 1. Streak Details Modal */}
      <Modal
        isOpen={isStreakModalOpen}
        onClose={() => setIsStreakModalOpen(false)}
        title="Daily Streak"
      >
        <div className="flex flex-col items-center text-center">
          <div className="w-20 h-20 rounded-full bg-orange-100 dark:bg-orange-950/40 flex items-center justify-center mb-4">
            <RewardIcon name="fire" size={48} animate />
          </div>

          <h3 className="text-2xl font-black text-gray-800 dark:text-gray-100 mb-1">
            {stats.streak} Day Streak!
          </h3>

          <p className="text-sm text-gray-500 dark:text-gray-400 mb-5 max-w-xs">
            Complete at least one lesson each day to build your streak and keep your learning momentum going strong!
          </p>

          {/* Activity status derived from authoritative learner data */}
          {stats.daily_xp > 0 ? (
            <div className="w-full p-3.5 mb-5 rounded-2xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 flex items-center gap-3 text-left">
              <CheckCircle2 className="w-5 h-5 text-duo-green shrink-0" />
              <div>
                <p className="text-xs font-black text-emerald-800 dark:text-emerald-300 uppercase tracking-wide">
                  Active for Today
                </p>
                <p className="text-xs font-bold text-emerald-700 dark:text-emerald-400">
                  You earned {stats.daily_xp} XP today. Your streak is safe!
                </p>
              </div>
            </div>
          ) : (
            <div className="w-full p-3.5 mb-5 rounded-2xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 flex items-center gap-3 text-left">
              <Flame className="w-5 h-5 text-amber-500 shrink-0" />
              <div>
                <p className="text-xs font-black text-amber-800 dark:text-amber-300 uppercase tracking-wide">
                  Practice Needed Today
                </p>
                <p className="text-xs font-bold text-amber-700 dark:text-amber-400">
                  Complete a lesson today to keep your streak burning!
                </p>
              </div>
            </div>
          )}

          <Button
            variant="green"
            fullWidth
            onClick={() => setIsStreakModalOpen(false)}
          >
            <span>Got It</span>
          </Button>
        </div>
      </Modal>

      {/* 2. Gems Details Modal */}
      <Modal
        isOpen={isGemModalOpen}
        onClose={() => setIsGemModalOpen(false)}
        title="Gems"
      >
        <div className="flex flex-col items-center text-center">
          <div className="w-20 h-20 rounded-full bg-blue-100 dark:bg-blue-950/40 flex items-center justify-center mb-4">
            <RewardIcon name="gem" size={48} animate />
          </div>

          <h3 className="text-2xl font-black text-gray-800 dark:text-gray-100 mb-1">
            {stats.gems} Gems
          </h3>

          <p className="text-sm text-gray-500 dark:text-gray-400 mb-6 max-w-xs">
            Gems are your reward currency earned by completing lessons, maintaining streaks, and conquering challenges. Spend them in the shop!
          </p>

          <div className="w-full flex flex-col gap-3">
            <Button
              variant="blue"
              fullWidth
              onClick={() => {
                setIsGemModalOpen(false);
                router.push("/shop");
              }}
            >
              <div className="flex items-center justify-center gap-2">
                <ShoppingBag className="w-4 h-4" />
                <span>Visit Shop</span>
              </div>
            </Button>

            <Button
              variant="outline"
              fullWidth
              onClick={() => setIsGemModalOpen(false)}
            >
              <span>Close</span>
            </Button>
          </div>
        </div>
      </Modal>

      {/* 3. Hearts Recovery & Refill Modal (Existing Logic Preserved) */}
      <Modal
        isOpen={isHeartModalOpen}
        onClose={() => setIsHeartModalOpen(false)}
        title="Hearts"
      >
        <div className="flex flex-col items-center text-center">
          <div className="w-20 h-20 rounded-full bg-red-100 dark:bg-red-950/40 flex items-center justify-center mb-4">
            <RewardIcon name="heart" size={48} animate />
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
              disabled={stats.hearts >= stats.max_hearts}
              onClick={handlePractice}
            >
              <div className="flex items-center justify-center gap-2">
                <RewardIcon name="heart" size={20} />
                <span>
                  {stats.hearts >= stats.max_hearts
                    ? "Hearts Full"
                    : "Practice to Earn 1 Heart"}
                </span>
              </div>
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
};
