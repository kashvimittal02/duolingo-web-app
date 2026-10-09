"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { CheckCircle2, Lock, Play, Zap, RotateCcw, Timer } from "lucide-react";
import { SkillNode, LessonNode } from "@/lib/types";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { RewardIcon } from "@/components/rewards/RewardIcon";

interface LessonModalProps {
  skill: SkillNode | null;
  isOpen: boolean;
  onClose: () => void;
  userHearts: number;
}

export const LessonModal: React.FC<LessonModalProps> = ({
  skill,
  isOpen,
  onClose,
  userHearts,
}) => {
  const router = useRouter();
  const [legendaryTargetLesson, setLegendaryTargetLesson] = useState<LessonNode | null>(null);

  if (!skill) return null;

  const handleStartLesson = (lessonId: number) => {
    onClose();
    router.push(`/lesson/${lessonId}`);
  };

  const handleStartLegendary = (lessonId: number) => {
    setLegendaryTargetLesson(null);
    onClose();
    router.push(`/challenge/${lessonId}`);
  };

  const firstPlayableLesson = skill.lessons.find((l) => l.status !== "locked") || skill.lessons[0];

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose} title={skill.title} maxWidth="md">
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 text-xs font-bold text-amber-900 dark:text-amber-300 rounded-2xl p-3">
            <span>Crown Level: {skill.crowns} / {skill.total_crown_levels}</span>
            <span>{skill.lessons.length} Lessons</span>
          </div>

          {/* Legendary Challenge Banner */}
          {skill.status !== "locked" && firstPlayableLesson && (
            <div className="bg-gradient-to-r from-purple-900 via-purple-800 to-indigo-900 border-2 border-purple-400/80 rounded-2xl p-3.5 text-white shadow-sm flex items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-purple-500/30 border border-purple-300/40 flex items-center justify-center shrink-0">
                  <Timer className="w-5 h-5 text-amber-300" />
                </div>
                <div>
                  <div className="flex items-center gap-1.5">
                    <span className="font-black text-xs sm:text-sm text-purple-100 uppercase tracking-wider">
                      Legendary Challenge
                    </span>
                    <span className="bg-amber-400 text-amber-950 text-[10px] font-black px-1.5 py-0.2 rounded-full uppercase">
                      Timed
                    </span>
                  </div>
                  <p className="text-[11px] sm:text-xs text-purple-200 font-bold">
                    Race the 90s server clock across 5 exercises!
                  </p>
                </div>
              </div>
              <Button
                size="sm"
                variant="purple"
                onClick={() => setLegendaryTargetLesson(firstPlayableLesson)}
              >
                <span>Challenge</span>
              </Button>
            </div>
          )}

          {userHearts <= 0 && (
            <div className="bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/60 text-duo-red p-3 rounded-xl text-xs font-bold text-center">
              You have 0 hearts! Practice or refill hearts from the top header to play lessons.
            </div>
          )}

          <div className="flex flex-col gap-3 max-h-[360px] overflow-y-auto pr-1">
            {skill.lessons.map((lesson) => {
              const isLocked = lesson.status === "locked";
              const isCompleted = lesson.status === "completed";
              const canStart = !isLocked && userHearts > 0;

              return (
                <div
                  key={lesson.id}
                  className={`
                    p-4 rounded-2xl border-2 flex items-center justify-between transition-all
                    ${
                      isLocked
                        ? "bg-gray-50 dark:bg-[#182830] border-gray-200 dark:border-[#2b3a42] text-gray-400 dark:text-[#55656e]"
                        : isCompleted
                        ? "bg-emerald-50/50 dark:bg-emerald-950/30 border-emerald-200 dark:border-emerald-800 text-gray-800 dark:text-gray-100"
                        : "bg-white dark:bg-[#202f36] border-duo-green-dark dark:border-[#37464f] shadow-sm text-gray-800 dark:text-gray-100"
                    }
                  `}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`
                        w-10 h-10 rounded-xl flex items-center justify-center font-black text-sm
                        ${
                          isLocked
                            ? "bg-gray-200 dark:bg-[#2b3a42] text-gray-400 dark:text-[#55656e]"
                            : isCompleted
                            ? "bg-duo-yellow text-amber-950"
                            : "bg-duo-green text-white"
                        }
                      `}
                    >
                      {isCompleted ? (
                        <CheckCircle2 className="w-5 h-5" />
                      ) : isLocked ? (
                        <Lock className="w-4 h-4" />
                      ) : (
                        lesson.order_index
                      )}
                    </div>

                    <div>
                      <h4 className="font-extrabold text-sm text-gray-800 dark:text-gray-100 leading-tight">
                        {lesson.title}
                      </h4>
                      <div className="flex items-center gap-2 mt-0.5 text-xs font-bold">
                        <span className="text-duo-yellow-dark flex items-center gap-1">
                          <RewardIcon name="star" size={14} animate />
                          {isCompleted ? "+5 XP (Replay)" : `+${lesson.xp_reward} XP`}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {!isLocked && (
                      <Button
                        size="sm"
                        variant="purple"
                        title="Start Legendary Timed Challenge"
                        onClick={() => setLegendaryTargetLesson(lesson)}
                      >
                        <Timer className="w-3.5 h-3.5" />
                      </Button>
                    )}

                    <Button
                      size="sm"
                      variant={isCompleted ? "outline" : "green"}
                      disabled={!canStart}
                      onClick={() => handleStartLesson(lesson.id)}
                    >
                      {isCompleted ? (
                        <div className="flex items-center gap-1 text-xs">
                          <RotateCcw className="w-3.5 h-3.5" />
                          <span>Replay</span>
                        </div>
                      ) : (
                        <div className="flex items-center gap-1 text-xs">
                          <Play className="w-3.5 h-3.5 fill-current" />
                          <span>Start</span>
                        </div>
                      )}
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </Modal>

      {/* Pre-Start Legendary Challenge Explanation Modal */}
      <Modal
        isOpen={Boolean(legendaryTargetLesson)}
        onClose={() => setLegendaryTargetLesson(null)}
        title="Legendary Challenge"
        maxWidth="sm"
      >
        <div className="flex flex-col items-center text-center p-2">
          <div className="w-16 h-16 rounded-2xl bg-purple-100 dark:bg-purple-950/60 border border-purple-300 dark:border-purple-700/60 flex items-center justify-center mb-4">
            <Timer className="w-9 h-9 text-duo-purple animate-pulse" />
          </div>

          <h3 className="text-xl font-black text-gray-800 dark:text-white mb-1">
            Ready for the Clock?
          </h3>

          <p className="text-xs font-bold text-gray-500 dark:text-gray-400 mb-4 max-w-xs">
            {legendaryTargetLesson?.title}
          </p>

          <div className="bg-purple-50 dark:bg-purple-950/40 border border-purple-200 dark:border-purple-800/60 rounded-2xl p-4 w-full text-left text-xs flex flex-col gap-2.5 mb-6">
            <div className="flex items-center gap-2 text-purple-900 dark:text-purple-200 font-bold">
              <span className="text-base">⏱️</span>
              <span><strong>90 Seconds</strong> server countdown — no pauses.</span>
            </div>
            <div className="flex items-center gap-2 text-purple-900 dark:text-purple-200 font-bold">
              <span className="text-base">🎯</span>
              <span><strong>5 Exercises</strong> from this lesson.</span>
            </div>
            <div className="flex items-center gap-2 text-purple-900 dark:text-purple-200 font-bold">
              <span className="text-base">🏆</span>
              <span><strong>+20 XP Bonus</strong> on first victory (0 XP on replay).</span>
            </div>
            <div className="flex items-center gap-2 text-purple-900 dark:text-purple-200 font-bold">
              <span className="text-base">🛡️</span>
              <span><strong>Zero hearts lost</strong> on mistakes.</span>
            </div>
          </div>

          <div className="flex flex-col gap-2.5 w-full">
            <Button
              variant="purple"
              fullWidth
              onClick={() => legendaryTargetLesson && handleStartLegendary(legendaryTargetLesson.id)}
            >
              <span>Start Timed Challenge</span>
            </Button>
            <Button
              variant="outline"
              fullWidth
              onClick={() => setLegendaryTargetLesson(null)}
            >
              <span>Cancel</span>
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
};

