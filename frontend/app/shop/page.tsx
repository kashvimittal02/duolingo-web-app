"use client";

import React, { useEffect, useState } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopHeader } from "@/components/layout/TopHeader";
import { BottomNav } from "@/components/layout/BottomNav";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { getLearnerProfile, refillHearts, practiceEarnHeart } from "@/lib/api";
import { LearnerProfile } from "@/lib/types";
import { Heart, Gem, Sparkles, ShoppingBag } from "lucide-react";

export default function ShopPage() {
  const [profile, setProfile] = useState<LearnerProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const fetchProfile = async () => {
    try {
      const data = await getLearnerProfile();
      setProfile(data);
    } catch {
      // Ignored
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleRefill = async () => {
    try {
      setActionLoading(true);
      setStatusMessage(null);
      const res = await refillHearts();
      setStatusMessage(res.message);
      await fetchProfile();
    } catch (err: any) {
      setStatusMessage(err.message || "Failed to refill hearts");
    } finally {
      setActionLoading(false);
    }
  };

  const handlePractice = async () => {
    try {
      setActionLoading(true);
      setStatusMessage(null);
      const res = await practiceEarnHeart();
      setStatusMessage(res.message);
      await fetchProfile();
    } catch (err: any) {
      setStatusMessage(err.message || "Failed to practice");
    } finally {
      setActionLoading(false);
    }
  };

  const stats = profile?.stats;

  return (
    <div className="min-h-screen bg-white dark:bg-[#131f24] flex transition-colors">
      <Sidebar />

      <div className="flex-1 md:ml-64 flex flex-col min-h-screen pb-20 md:pb-8">
        <TopHeader stats={stats || null} onStatsUpdated={fetchProfile} />

        <main className="flex-1 max-w-3xl mx-auto w-full px-4 sm:px-6 py-8">
          <div className="flex flex-col items-center text-center mb-8">
            <div className="w-20 h-20 rounded-3xl bg-blue-100 dark:bg-blue-950/60 flex items-center justify-center mb-4 shadow-sm">
              <ShoppingBag className="w-12 h-12 text-duo-blue" />
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-gray-800 dark:text-white mb-1">
              Shop & Inventory
            </h1>
            <p className="text-sm font-bold text-gray-500 dark:text-gray-400 max-w-sm">
              Use your mock gems to refill hearts and keep learning without pause.
            </p>
          </div>

          {statusMessage && (
            <div className="p-4 mb-6 rounded-2xl bg-blue-50 dark:bg-[#1b3a4b] border-2 border-blue-200 dark:border-[#2c5a73] text-duo-blue dark:text-[#38bdf8] font-bold text-sm text-center">
              {statusMessage}
            </div>
          )}

          <div className="flex flex-col gap-4">
            {/* Heart Refill Card */}
            <Card className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-2xl bg-red-100 dark:bg-red-950/40 flex items-center justify-center shrink-0">
                  <Heart className="w-10 h-10 fill-duo-red text-duo-red" />
                </div>
                <div>
                  <h3 className="text-lg font-black text-gray-800 dark:text-white">
                    Full Heart Refill
                  </h3>
                  <p className="text-xs sm:text-sm font-bold text-gray-500 dark:text-gray-400">
                    Fully restore your hearts back to 5. Never wait for passive regeneration!
                  </p>
                </div>
              </div>

              <div className="shrink-0">
                <Button
                  variant="blue"
                  disabled={
                    !stats ||
                    stats.hearts >= stats.max_hearts ||
                    stats.gems < 350 ||
                    actionLoading
                  }
                  onClick={handleRefill}
                >
                  <div className="flex items-center gap-1.5">
                    <Gem className="w-4 h-4 fill-white" />
                    <span>350 Gems</span>
                  </div>
                </Button>
              </div>
            </Card>

            {/* Practice Recovery Card */}
            <Card className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-2xl bg-emerald-100 dark:bg-emerald-950/40 flex items-center justify-center shrink-0">
                  <Sparkles className="w-10 h-10 text-duo-green" />
                </div>
                <div>
                  <h3 className="text-lg font-black text-gray-800 dark:text-white">
                    Practice Session
                  </h3>
                  <p className="text-xs sm:text-sm font-bold text-gray-500 dark:text-gray-400">
                    Earn 1 heart by reviewing previously completed vocabulary (Free, 0 XP).
                  </p>
                </div>
              </div>

              <div className="shrink-0">
                <Button
                  variant="outline"
                  disabled={!stats || stats.hearts >= stats.max_hearts || actionLoading}
                  onClick={handlePractice}
                >
                  <span>Practice Free</span>
                </Button>
              </div>
            </Card>
          </div>
        </main>
      </div>

      <BottomNav />
    </div>
  );
}
