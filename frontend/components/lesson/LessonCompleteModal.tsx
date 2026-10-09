"use client";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import confetti from "canvas-confetti";
import { Zap, Flame, Crown, Award, CheckCircle } from "lucide-react";
import { LessonCompletionResponse } from "@/lib/types";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { LingoMascot } from "@/components/mascot/LingoMascot";
import { RewardIcon } from "@/components/rewards/RewardIcon";
import { sounds } from "@/lib/audio";

interface LessonCompleteModalProps {
  isOpen: boolean;
  completionData: LessonCompletionResponse | null;
}

export const LessonCompleteModal: React.FC<LessonCompleteModalProps> = ({
  isOpen,
  completionData,
}) => {
  const router = useRouter();

  useEffect(() => {
    if (isOpen) {
      // Play celebratory triumph fanfare
      sounds.playLessonComplete();

      // Fire festive celebration confetti
      try {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 },
        });
      } catch {
        // Fallback if canvas-confetti is unavailable
      }
    }
  }, [isOpen]);

  if (!completionData) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={() => router.push("/")}
      showCloseButton={false}
      maxWidth="md"
    >
      <div className="flex flex-col items-center text-center p-2">
        <LingoMascot
          expression="cheering"
          size="lg"
          speechBubble={`¡Increíble! +${completionData.xp_awarded} XP`}
          bubblePosition="top"
          className="mb-2 animate-bounce-subtle"
        />

        <h2 className="text-2xl sm:text-3xl font-black text-gray-800 dark:text-white mb-1">
          Lesson Completed!
        </h2>

        <p className="text-sm font-bold text-gray-500 dark:text-gray-400 mb-6">
          {completionData.is_replay
            ? "Great practice session! You reinforced your vocabulary."
            : "Superb! You advanced your Spanish language skills."}
        </p>

        {/* Stats Summary Grid */}
        <div className="grid grid-cols-3 gap-3 w-full mb-6">
          {/* XP */}
          <div className="bg-amber-50 dark:bg-[#182830] border-2 border-amber-200 dark:border-amber-800/60 rounded-2xl p-3 flex flex-col items-center">
            <span className="text-xs font-black text-amber-700 dark:text-amber-400 uppercase mb-1 flex items-center gap-1">
              <RewardIcon name="star" size={18} />
              XP
            </span>
            <span className="text-xl font-black text-amber-900 dark:text-amber-300">
              +{completionData.xp_awarded}
            </span>
          </div>

          {/* Streak */}
          <div className="bg-orange-50 dark:bg-[#182830] border-2 border-orange-200 dark:border-orange-800/60 rounded-2xl p-3 flex flex-col items-center">
            <span className="text-xs font-black text-orange-700 dark:text-orange-400 uppercase mb-1 flex items-center gap-1">
              <RewardIcon name="fire" size={18} />
              Streak
            </span>
            <span className="text-xl font-black text-orange-950 dark:text-orange-300">
              {completionData.streak} {completionData.streak === 1 ? "day" : "days"}
            </span>
          </div>

          {/* Crowns */}
          <div className="bg-emerald-50 dark:bg-[#182830] border-2 border-emerald-200 dark:border-emerald-800/60 rounded-2xl p-3 flex flex-col items-center">
            <span className="text-xs font-black text-emerald-700 dark:text-emerald-400 uppercase mb-1 flex items-center gap-1">
              <RewardIcon name="trophy" size={18} />
              Crowns
            </span>
            <span className="text-xl font-black text-emerald-950 dark:text-emerald-300">
              {completionData.crowns}
            </span>
          </div>
        </div>

        {/* Achievements Unlocked Alert */}
        {completionData.achievements_unlocked &&
          completionData.achievements_unlocked.length > 0 && (
            <div className="w-full bg-purple-50 dark:bg-purple-950/40 border-2 border-purple-200 dark:border-purple-800 rounded-2xl p-3 mb-6 flex flex-col items-center">
              <div className="flex items-center gap-1.5 text-xs font-black text-purple-700 dark:text-purple-300 uppercase mb-1">
                <Award className="w-4 h-4 text-purple-600" />
                <span>Achievement Unlocked!</span>
              </div>
              {completionData.achievements_unlocked.map((ach, idx) => (
                <span
                  key={idx}
                  className="text-sm font-extrabold text-purple-950 dark:text-purple-200"
                >
                  🎉 {ach}
                </span>
              ))}
            </div>
          )}

        <Button
          variant="green"
          size="lg"
          fullWidth
          onClick={() => router.push("/")}
        >
          Continue
        </Button>
      </div>
    </Modal>
  );
};
