"use client";

import React, { useEffect, useState, useCallback } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopHeader } from "@/components/layout/TopHeader";
import { BottomNav } from "@/components/layout/BottomNav";
import { UnitHeader } from "@/components/path/UnitHeader";
import { SkillNode } from "@/components/path/SkillNode";
import { PathConnector } from "@/components/path/PathConnector";
import { LessonModal } from "@/components/path/LessonModal";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { getLearnerProfile, getCourseTree } from "@/lib/api";
import { LearnerProfile, CourseTree, SkillNode as SkillNodeType } from "@/lib/types";
import { RightRail } from "@/components/layout/RightRail";
import { AlertCircle } from "lucide-react";

export default function LearningPathPage() {
  const [profile, setProfile] = useState<LearnerProfile | null>(null);
  const [tree, setTree] = useState<CourseTree | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSkill, setSelectedSkill] = useState<SkillNodeType | null>(null);

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

  // Skill offsets to create classic winding path
  const pathOffsets = [0, 45, 60, 45, 0, -45, -60, -45];

  return (
    <div className="min-h-screen bg-white dark:bg-[#131f24] flex transition-colors">
      {/* Desktop Navigation Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex-1 md:ml-64 flex flex-col min-h-screen pb-20 md:pb-8">
        <TopHeader
          stats={profile?.stats || null}
          onStatsUpdated={loadData}
        />

        <main className="flex-1 max-w-5xl mx-auto w-full px-4 sm:px-6 py-6 flex flex-col lg:flex-row gap-8">
          {/* Central Learning Path Stream */}
          <div className="flex-1 max-w-xl mx-auto w-full">
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
                {tree.units.map((unit) => (
                  <section key={unit.id} className="mb-12">
                    <UnitHeader
                      orderIndex={unit.order_index}
                      title={unit.title}
                      description={unit.description}
                      hexColor={unit.hex_color}
                    />

                    {/* Stepping Stones Path */}
                    <div className="flex flex-col items-center py-4 relative">
                      {unit.skills.map((skill, sIdx) => {
                        const offset = pathOffsets[sIdx % pathOffsets.length];
                        const nextSkill = unit.skills[sIdx + 1];
                        const nextOffset = nextSkill
                          ? pathOffsets[(sIdx + 1) % pathOffsets.length]
                          : 0;

                        return (
                          <React.Fragment key={skill.id}>
                            <SkillNode
                              skill={skill}
                              unitColor={unit.hex_color}
                              offset={offset}
                              onClick={() => setSelectedSkill(skill)}
                            />
                            {nextSkill && (
                              <PathConnector
                                fromOffset={offset}
                                toOffset={nextOffset}
                                isUnlocked={skill.status === "completed"}
                              />
                            )}
                          </React.Fragment>
                        );
                      })}
                    </div>
                  </section>
                ))}
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
    </div>
  );
}
