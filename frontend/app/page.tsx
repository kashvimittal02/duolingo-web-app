"use client";

import React, { useEffect, useState, useCallback, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopHeader } from "@/components/layout/TopHeader";
import { BottomNav } from "@/components/layout/BottomNav";
import { UnitHeader } from "@/components/path/UnitHeader";
import { LessonPathNode } from "@/components/path/LessonPathNode";
import { PathConnector } from "@/components/path/PathConnector";
import { CheckpointNode } from "@/components/path/CheckpointNode";
import { UnitMascot } from "@/components/path/UnitMascot";
import { LessonModal } from "@/components/path/LessonModal";
import { UnitDetailsModal } from "@/components/path/UnitDetailsModal";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { getLearnerProfile, getCourseTree } from "@/lib/api";
import { LearnerProfile, CourseTree, SkillNode as SkillNodeType, UnitNode } from "@/lib/types";
import { RightRail } from "@/components/layout/RightRail";
import { AlertCircle, Compass, Lock } from "lucide-react";

function LearningPathContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [profile, setProfile] = useState<LearnerProfile | null>(null);
  const [tree, setTree] = useState<CourseTree | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSkill, setSelectedSkill] = useState<SkillNodeType | null>(null);
  const [selectedUnitDetails, setSelectedUnitDetails] = useState<UnitNode | null>(null);

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
    } catch (err: any) {
      setError(err.message || "Failed to load learning path from server");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Handle direct navigation to specific section anchor (e.g. /?section=2)
  useEffect(() => {
    const sectionParam = searchParams.get("section");
    if (sectionParam && tree) {
      const el = document.getElementById(`unit-${sectionParam}`);
      if (el) {
        setTimeout(() => {
          el.scrollIntoView({ behavior: "smooth" });
        }, 150);
      }
    }
  }, [searchParams, tree]);

  // Winding path offsets: alternating centre (0), left (-48), centre (0), right (48), centre (0)
  const pathOffsets = [0, -48, 0, 48, 0];

  return (
    <div className="min-h-screen bg-white dark:bg-[#131f24] flex transition-colors">
      {/* Desktop Navigation Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex-1 md:ml-64 flex flex-col min-h-screen lg:h-screen lg:overflow-hidden pb-20 lg:pb-0">
        <TopHeader
          stats={profile?.stats || null}
          onStatsUpdated={loadData}
        />

        <main className="flex-1 min-h-0 max-w-5xl mx-auto w-full px-4 sm:px-6 py-6 flex flex-col lg:flex-row gap-8 lg:overflow-hidden">
          {/* Central Learning Path Stream */}
          <div className="flex-1 max-w-xl mx-auto w-full lg:h-full lg:min-h-0 lg:overflow-y-auto lg:overflow-x-hidden lg:pr-3 lg:pb-16 custom-scrollbar overscroll-contain">
            {loading ? (
              <div className="flex flex-col items-center justify-center py-24 gap-4">
                <div className="w-12 h-12 border-4 border-duo-green border-t-transparent rounded-full animate-spin" />
                <p className="text-gray-400 dark:text-gray-500 font-extrabold text-sm uppercase tracking-wider">
                  Loading Learning Path...
                </p>
              </div>
            ) : error ? (
              <div className="p-6 rounded-3xl bg-red-50 dark:bg-red-950/40 border-2 border-red-200 dark:border-red-900/60 text-center flex flex-col items-center gap-3">
                <AlertCircle className="w-10 h-10 text-duo-red" />
                <h3 className="text-lg font-black text-gray-800 dark:text-white">Connection Error</h3>
                <p className="text-sm font-bold text-gray-500 dark:text-gray-400 max-w-sm">{error}</p>
                <Button variant="outline" size="sm" onClick={loadData}>
                  Try Again
                </Button>
              </div>
            ) : tree ? (
              <div className="flex flex-col">
                {tree.units.map((unit, uIdx) => {
                  const hasPreviousSection = uIdx > 0;
                  const hasNextSection = uIdx < tree.units.length - 1;
                  const isFirstUnitOfSection2 =
                    unit.section_index === 2 &&
                    (uIdx === 0 || (tree.units[uIdx - 1]?.section_index ?? 1) !== 2);

                  // Find lessons in this unit
                  const allLessons = unit.skills.flatMap((s) => s.lessons);
                  const isUnitCompleted =
                    allLessons.length > 0 && allLessons.every((l) => l.status === "completed");
                  const nextAvailableLesson = allLessons.find((l) => l.status === "available");
                  const continueLesson = unit.is_unlocked
                    ? nextAvailableLesson || (isUnitCompleted ? allLessons[0] : undefined)
                    : undefined;

                  const handleBackNavigation = () => {
                    if (uIdx > 0) {
                      // Navigate to previous section
                      const prevUnit = tree.units[uIdx - 1];
                      const prevEl = document.getElementById(`unit-${prevUnit.order_index}`);
                      if (prevEl) {
                        prevEl.scrollIntoView({ behavior: "smooth" });
                      } else {
                        router.push("/sections");
                      }
                    } else {
                      // Section 1 back arrow: returns to parent Sections Overview
                      router.push("/sections");
                    }
                  };

                  const handleNextNavigation = () => {
                    if (uIdx < tree.units.length - 1) {
                      const nextUnit = tree.units[uIdx + 1];
                      const nextEl = document.getElementById(`unit-${nextUnit.order_index}`);
                      if (nextEl) {
                        nextEl.scrollIntoView({ behavior: "smooth" });
                      }
                    }
                  };

                  const checkpointLesson = unit.is_checkpoint ? unit.skills[0]?.lessons[0] : null;

                  return (
                    <React.Fragment key={unit.id}>
                      {/* Section 2 Divider Banner */}
                      {isFirstUnitOfSection2 && (
                        <div className="w-full my-6 p-5 sm:p-6 rounded-2xl bg-gradient-to-r from-teal-500 via-emerald-600 to-green-600 text-white shadow-md border border-emerald-400 relative overflow-hidden select-none">
                          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                            <div className="flex items-center gap-3.5">
                              <div className="w-12 h-12 rounded-xl bg-white/20 backdrop-blur-xs flex items-center justify-center shrink-0 border border-white/30 shadow-inner">
                                {unit.is_unlocked ? (
                                  <Compass className="w-7 h-7 text-white" />
                                ) : (
                                  <Lock className="w-7 h-7 text-white/90" />
                                )}
                              </div>
                              <div>
                                <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-black/25 text-white text-[10px] font-black uppercase tracking-wider mb-1">
                                  <span>SECTION 2 • DAILY LIFE</span>
                                </div>
                                <h3 className="text-lg sm:text-xl font-black">
                                  {unit.is_unlocked ? "Section 2: Daily Life" : "Section 2: Locked"}
                                </h3>
                                <p className="text-xs sm:text-sm font-bold text-white/90">
                                  {unit.is_unlocked
                                    ? "Advance your Spanish with food, ordering, and daily routines."
                                    : "Pass the Section 1 Checkpoint Challenge above to unlock Section 2."}
                                </p>
                              </div>
                            </div>
                            <div className="shrink-0">
                              <span
                                className={`px-3.5 py-1 rounded-full text-xs font-black uppercase tracking-wider shadow-xs ${
                                  unit.is_unlocked
                                    ? "bg-white text-emerald-700"
                                    : "bg-black/30 text-white/90"
                                }`}
                              >
                                {unit.is_unlocked ? "Available" : "Locked"}
                              </span>
                            </div>
                          </div>
                        </div>
                      )}

                      <section
                        id={`unit-${unit.order_index}`}
                        className="mb-8 scroll-mt-20"
                      >
                        <UnitHeader
                          orderIndex={unit.order_index}
                          sectionIndex={unit.section_index || (unit.order_index >= 7 ? 2 : 1)}
                          sectionTitle={
                            unit.section_title ||
                            (unit.order_index >= 7 ? "Daily Life" : "Rookie Basics")
                          }
                          isCheckpoint={unit.is_checkpoint || false}
                          title={unit.title}
                          description={unit.description}
                          hexColor={unit.hex_color}
                          hasPreviousSection={hasPreviousSection}
                          hasNextSection={hasNextSection}
                          onBack={handleBackNavigation}
                          onNext={hasNextSection ? handleNextNavigation : undefined}
                          onSeeDetails={() => setSelectedUnitDetails(unit)}
                          onContinue={
                            continueLesson
                              ? () => router.push(`/lesson/${continueLesson.id}`)
                              : undefined
                          }
                        />

                        {/* If this is the Section Checkpoint Challenge */}
                        {unit.is_checkpoint && checkpointLesson ? (
                          <div className="py-2">
                            <CheckpointNode
                              lesson={checkpointLesson}
                              isUnlocked={unit.is_unlocked ?? false}
                              onStart={() => router.push(`/lesson/${checkpointLesson.id}`)}
                            />
                          </div>
                        ) : (
                          /* Winding Sequence of Individual Lesson Nodes */
                          <div className="flex flex-col items-center py-2 relative w-full">
                            {allLessons.map((lesson, lIdx) => {
                              const offset = pathOffsets[lIdx % pathOffsets.length];
                              const nextLesson = allLessons[lIdx + 1];
                              const nextOffset = nextLesson
                                ? pathOffsets[(lIdx + 1) % pathOffsets.length]
                                : 0;
                              const isCurrent = lesson.id === nextAvailableLesson?.id;

                              // Alternating mascot position:
                              // Units 1, 3, 5, 8 on the right (beside lesson 1, where path curves left)
                              // Units 2, 4, 7 on the left (beside lesson 3, where path curves right)
                              const unitSide: "left" | "right" = [1, 3, 5, 8].includes(unit.order_index)
                                ? "right"
                                : "left";
                              const mascotTargetIdx = Math.min(
                                unitSide === "right" ? 1 : 3,
                                Math.max(0, allLessons.length - 1)
                              );
                              const shouldRenderMascot = lIdx === mascotTargetIdx;

                              return (
                                <React.Fragment key={lesson.id}>
                                  <div className="relative w-full flex justify-center">
                                    <LessonPathNode
                                      lesson={lesson}
                                      unitColor={unit.hex_color}
                                      offset={offset}
                                      isCurrent={isCurrent}
                                      onLaunch={() => router.push(`/lesson/${lesson.id}`)}
                                    />
                                    {shouldRenderMascot && (
                                      <UnitMascot
                                        orderIndex={unit.order_index}
                                        isUnlocked={unit.is_unlocked ?? false}
                                        isCompleted={isUnitCompleted}
                                        side={unitSide}
                                      />
                                    )}
                                  </div>
                                  {nextLesson && (
                                    <PathConnector
                                      fromOffset={offset}
                                      toOffset={nextOffset}
                                      isUnlocked={lesson.status === "completed"}
                                    />
                                  )}
                                </React.Fragment>
                              );
                            })}
                          </div>
                        )}
                      </section>
                    </React.Fragment>
                  );
                })}
              </div>
            ) : null}
          </div>

          {/* Right Sidebar Widgets (Desktop only) */}
          <RightRail profile={profile} />
        </main>
      </div>

      {/* Mobile Bottom Navigation */}
      <BottomNav />

      {/* Lesson Selection Modal */}
      <LessonModal
        skill={selectedSkill}
        isOpen={Boolean(selectedSkill)}
        onClose={() => setSelectedSkill(null)}
        userHearts={profile?.stats.hearts ?? 5}
      />

      {/* Unit / Section Details Modal */}
      {selectedUnitDetails && (
        <UnitDetailsModal
          unit={selectedUnitDetails}
          isOpen={Boolean(selectedUnitDetails)}
          onClose={() => setSelectedUnitDetails(null)}
          activeLessonId={
            selectedUnitDetails.skills
              .flatMap((s) => s.lessons)
              .find((l) => l.status === "available")?.id || null
          }
          isUnlocked={
            selectedUnitDetails.is_unlocked ??
            (selectedUnitDetails.order_index === 1 ||
            (tree?.units[selectedUnitDetails.order_index - 2]?.skills.every(
              (s) => s.status === "completed"
            ) ?? true))
          }
        />
      )}
    </div>
  );
}

export default function LearningPathPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-white dark:bg-[#131f24] flex items-center justify-center">
          <div className="w-10 h-10 border-4 border-duo-green border-t-transparent rounded-full animate-spin" />
        </div>
      }
    >
      <LearningPathContent />
    </Suspense>
  );
}
