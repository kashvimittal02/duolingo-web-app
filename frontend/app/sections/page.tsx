"use client";

import React, { useEffect, useState, useCallback, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopHeader } from "@/components/layout/TopHeader";
import { BottomNav } from "@/components/layout/BottomNav";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { UnitDetailsModal } from "@/components/path/UnitDetailsModal";
import { LingoMascot } from "@/components/mascot/LingoMascot";
import { getLearnerProfile, getCourseTree } from "@/lib/api";
import { LearnerProfile, CourseTree, UnitNode } from "@/lib/types";
import {
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  Lock,
  Play,
  Layers,
  Sparkles,
  AlertCircle,
  ChevronRight,
} from "lucide-react";

function SectionsContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const unitParam = searchParams.get("unit");

  const [profile, setProfile] = useState<LearnerProfile | null>(null);
  const [tree, setTree] = useState<CourseTree | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedUnit, setSelectedUnit] = useState<UnitNode | null>(null);
  const [lockedNotice, setLockedNotice] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const [pData, tData] = await Promise.all([
        getLearnerProfile(),
        getCourseTree(),
      ]);
      setProfile(pData);
      setTree(tData);

      // Auto-open modal if unit param provided
      if (unitParam && tData) {
        const target = tData.units.find((u) => u.order_index === Number(unitParam));
        if (target) {
          setSelectedUnit(target);
        }
      }
    } catch (err: any) {
      setError(err.message || "Failed to load course sections");
    } finally {
      setLoading(false);
    }
  }, [unitParam]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Determine section status and active lesson for each unit
  const getSectionMetadata = (unit: UnitNode, idx: number, allUnits: UnitNode[]) => {
    const isFirstUnit = idx === 0;
    const prevUnit = isFirstUnit ? null : allUnits[idx - 1];

    // Section is unlocked based on authoritative backend is_unlocked flag, falling back to progression check
    const prevUnitCompleted = prevUnit
      ? prevUnit.skills.every((s) => s.status === "completed")
      : true;
    const isUnlocked = unit.is_unlocked ?? (isFirstUnit || prevUnitCompleted);

    // Find first playable lesson in this unit
    const allLessons = unit.skills.flatMap((s) => s.lessons);
    const activeLesson = allLessons.find((l) => l.status === "available") || allLessons.find((l) => l.status !== "locked");

    const totalLessons = allLessons.length;
    const completedLessons = allLessons.filter((l) => l.status === "completed").length;
    const isCompleted = totalLessons > 0 && completedLessons === totalLessons;

    return {
      isUnlocked,
      isCompleted,
      activeLessonId: activeLesson ? activeLesson.id : null,
      totalLessons,
      completedLessons,
    };
  };

  return (
    <div className="min-h-screen bg-white dark:bg-[#131f24] flex transition-colors">
      <Sidebar />

      <div className="flex-1 md:ml-64 flex flex-col min-h-screen pb-20 md:pb-8">
        <TopHeader
          stats={profile?.stats || null}
          onStatsUpdated={loadData}
        />

        <main className="flex-1 max-w-3xl mx-auto w-full px-4 sm:px-6 py-8">
          {/* Back to Learning Path Button */}
          <div className="mb-6">
            <button
              type="button"
              onClick={() => router.push("/")}
              className="inline-flex items-center gap-2 px-3 py-1.5 rounded-2xl bg-gray-100 hover:bg-gray-200 dark:bg-[#1a2c35] dark:hover:bg-[#243a45] text-gray-700 dark:text-gray-200 text-xs font-black uppercase tracking-wider transition-colors cursor-pointer"
            >
              <ArrowLeft className="w-4 h-4 stroke-[2.5]" />
              <span>Back to Learning Path</span>
            </button>
          </div>

          {/* Page Header */}
          <div className="flex flex-col items-center text-center mb-8">
            <LingoMascot
              expression="happy"
              size="md"
              speechBubble="Explore Spanish course sections!"
              className="mb-4"
            />
            <h1 className="text-2xl sm:text-3xl font-black text-gray-800 dark:text-white mb-2">
              Course Sections
            </h1>
            <p className="text-sm font-bold text-gray-500 dark:text-gray-400 max-w-md">
              Select a section to view its curriculum overview, continue lessons, or check your skill progress.
            </p>
          </div>

          {/* Locked Notice Alert if triggered */}
          {lockedNotice && (
            <div className="mb-6 p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/40 border-2 border-amber-300 dark:border-amber-700 text-amber-900 dark:text-amber-200 text-xs font-bold flex items-center justify-between gap-3 animate-fade-in">
              <div className="flex items-center gap-2.5">
                <Lock className="w-5 h-5 shrink-0 text-amber-600 dark:text-amber-400" />
                <span>{lockedNotice}</span>
              </div>
              <button
                type="button"
                onClick={() => setLockedNotice(null)}
                className="text-amber-700 hover:text-amber-900 dark:text-amber-300 font-extrabold uppercase text-[10px]"
              >
                Dismiss
              </button>
            </div>
          )}

          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 gap-4">
              <div className="w-10 h-10 border-4 border-duo-green border-t-transparent rounded-full animate-spin" />
              <p className="text-gray-400 font-extrabold text-sm uppercase">Loading Sections...</p>
            </div>
          ) : error ? (
            <div className="p-6 rounded-3xl bg-red-50 dark:bg-red-950/40 border-2 border-red-200 dark:border-red-900/60 text-center flex flex-col items-center gap-3">
              <AlertCircle className="w-10 h-10 text-duo-red" />
              <h3 className="text-lg font-black text-gray-800 dark:text-white">Unable to Load Sections</h3>
              <p className="text-sm font-bold text-gray-500 dark:text-gray-400">{error}</p>
              <Button variant="outline" size="sm" onClick={loadData}>
                Try Again
              </Button>
            </div>
          ) : tree ? (
            <div className="flex flex-col gap-6">
              {tree.units.map((unit, idx) => {
                const {
                  isUnlocked,
                  isCompleted,
                  activeLessonId,
                  totalLessons,
                  completedLessons,
                } = getSectionMetadata(unit, idx, tree.units);

                const isCheckpoint = unit.is_checkpoint || unit.order_index === 6;
                const displayUnitNumber =
                  unit.section_index === 2 && unit.order_index >= 7
                    ? unit.order_index - 6
                    : unit.order_index;
                const cardBadge = isCheckpoint
                  ? "Section 1 • Checkpoint Challenge"
                  : `Section ${unit.section_index || 1}: ${unit.section_title || (unit.order_index >= 7 ? "Daily Life" : "Rookie Basics")} • Unit ${displayUnitNumber}`;
                const cardTitle = isCheckpoint
                  ? "Section 1 Checkpoint Challenge"
                  : unit.title.replace(/^Unit \d+:\s*/, (match) =>
                      unit.section_index === 2 ? `Unit ${displayUnitNumber}: ` : match
                    );

                const lockedMessage =
                  unit.order_index === 7
                    ? "Section 2 is locked! Complete all Section 1 lessons and the Checkpoint Challenge first."
                    : unit.order_index === 6
                    ? "The Checkpoint Challenge is locked! Complete all Section 1 lessons (Units 1–5) first."
                    : `Unit ${displayUnitNumber} is locked! Complete Unit ${displayUnitNumber - 1} lessons first.`;

                const handleCardClick = () => {
                  if (!isUnlocked) {
                    setLockedNotice(lockedMessage);
                    return;
                  }
                  setSelectedUnit(unit);
                };

                const handleContinue = (e: React.MouseEvent) => {
                  e.stopPropagation();
                  if (!isUnlocked) {
                    setLockedNotice(lockedMessage);
                    return;
                  }
                  if (activeLessonId) {
                    router.push(`/lesson/${activeLessonId}`);
                  } else {
                    router.push(`/?section=${unit.order_index}`);
                  }
                };

                const handleOpenPath = (e: React.MouseEvent) => {
                  e.stopPropagation();
                  router.push(`/?section=${unit.order_index}`);
                };

                const handleDetailsClick = (e: React.MouseEvent) => {
                  e.stopPropagation();
                  setSelectedUnit(unit);
                };

                return (
                  <Card
                    key={unit.id}
                    className={`
                      overflow-hidden border-2 transition-all cursor-pointer select-none
                      ${
                        isUnlocked
                          ? "hover:border-duo-blue/50 dark:hover:border-duo-blue/40 shadow-sm"
                          : "opacity-80 bg-gray-50/50 dark:bg-[#131f24]/50"
                      }
                    `}
                    onClick={handleCardClick}
                  >
                    {/* Section Card Banner */}
                    <div
                      className="p-5 text-white flex items-start justify-between gap-4"
                      style={{
                        backgroundColor: isUnlocked ? unit.hex_color || "#58cc02" : "#777777",
                      }}
                    >
                      <div>
                        <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-black/25 text-white text-[10px] font-black uppercase tracking-wider mb-2">
                          <span>{cardBadge}</span>
                        </div>
                        <h2 className="text-xl sm:text-2xl font-black uppercase tracking-wide leading-tight">
                          {cardTitle}
                        </h2>
                      </div>

                      <div className="shrink-0">
                        {isCompleted ? (
                          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-emerald-950/40 text-emerald-100 text-xs font-black uppercase">
                            <CheckCircle2 className="w-4 h-4 text-white" />
                            <span>Done</span>
                          </span>
                        ) : isUnlocked ? (
                          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-black/25 text-white text-xs font-black uppercase">
                            <span>In Progress</span>
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-black/40 text-white text-xs font-black uppercase">
                            <Lock className="w-3.5 h-3.5" />
                            <span>Locked</span>
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Section Body */}
                    <div className="p-5 flex flex-col gap-4">
                      {unit.description && (
                        <p className="text-xs sm:text-sm font-bold text-gray-600 dark:text-gray-300 leading-relaxed">
                          {unit.description}
                        </p>
                      )}

                      {/* Skills List */}
                      <div className="flex flex-col gap-2">
                        <span className="text-[11px] font-black uppercase tracking-wider text-gray-400">
                          Included Skills ({unit.skills.length})
                        </span>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                          {unit.skills.map((skill) => (
                            <div
                              key={skill.id}
                              className="flex items-center justify-between p-2.5 rounded-xl bg-gray-50 dark:bg-[#1a2c35] border border-gray-100 dark:border-[#2b3a42] text-xs font-bold"
                            >
                              <span className="text-gray-800 dark:text-gray-200 truncate">
                                {skill.title}
                              </span>
                              <span className="text-amber-500 font-black shrink-0 text-[11px]">
                                👑 {skill.crowns}/{skill.total_crown_levels}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Locked Notice inside card if locked */}
                      {!isUnlocked && (
                        <div className="p-3 rounded-xl bg-gray-100 dark:bg-[#1a2c35] text-gray-500 dark:text-gray-400 text-xs font-bold flex items-center gap-2">
                          <Lock className="w-4 h-4 shrink-0" />
                          <span>
                            Prerequisite:{" "}
                            {unit.order_index === 7
                              ? "Complete all Section 1 lessons and the Checkpoint Challenge to unlock Section 2."
                              : unit.order_index === 6
                              ? "Complete all Section 1 lessons (Units 1–5) to unlock the Checkpoint Challenge."
                              : `Complete all lessons in Unit ${displayUnitNumber - 1} to unlock this unit.`}
                          </span>
                        </div>
                      )}

                      {/* Action Buttons */}
                      <div className="pt-2 flex flex-col sm:flex-row items-center justify-between gap-3 border-t border-gray-100 dark:border-[#2b3a42]">
                        <div className="text-xs font-extrabold text-gray-400">
                          {completedLessons} of {totalLessons} lessons completed
                        </div>

                        <div className="flex items-center gap-2 w-full sm:w-auto">
                          {/* See Details Button */}
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={handleDetailsClick}
                            className="flex-1 sm:flex-initial"
                          >
                            <BookOpen className="w-4 h-4" />
                            <span>See Details</span>
                          </Button>

                          {/* Open Path Button */}
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={handleOpenPath}
                            className="flex-1 sm:flex-initial"
                          >
                            <span>Open Path</span>
                          </Button>

                          {/* Continue Button */}
                          {isUnlocked ? (
                            <Button
                              variant="green"
                              size="sm"
                              onClick={handleContinue}
                              className="flex-1 sm:flex-initial"
                            >
                              <Play className="w-3.5 h-3.5 fill-white" />
                              <span>Continue</span>
                            </Button>
                          ) : (
                            <Button
                              variant="outline"
                              size="sm"
                              disabled
                              className="flex-1 sm:flex-initial opacity-60"
                            >
                              <Lock className="w-3.5 h-3.5" />
                              <span>Locked</span>
                            </Button>
                          )}
                        </div>
                      </div>
                    </div>
                  </Card>
                );
              })}
            </div>
          ) : null}
        </main>
      </div>

      <BottomNav />

      {/* Selected Unit Details Modal */}
      {selectedUnit && (
        <UnitDetailsModal
          unit={selectedUnit}
          isOpen={Boolean(selectedUnit)}
          onClose={() => setSelectedUnit(null)}
          activeLessonId={
            tree?.units
              .find((u) => u.id === selectedUnit.id)
              ?.skills.flatMap((s) => s.lessons)
              .find((l) => l.status === "available")?.id || null
          }
          isUnlocked={
            selectedUnit.is_unlocked ??
            (selectedUnit.order_index === 1 ||
            (tree?.units[selectedUnit.order_index - 2]?.skills.every((s) => s.status === "completed") ?? true))
          }
        />
      )}
    </div>
  );
}

export default function SectionsPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-white dark:bg-[#131f24] flex items-center justify-center">
          <div className="w-10 h-10 border-4 border-duo-green border-t-transparent rounded-full animate-spin" />
        </div>
      }
    >
      <SectionsContent />
    </Suspense>
  );
}
