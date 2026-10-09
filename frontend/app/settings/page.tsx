"use client";

import React, { useEffect, useState } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopHeader } from "@/components/layout/TopHeader";
import { BottomNav } from "@/components/layout/BottomNav";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import { useTheme } from "@/lib/theme";
import { sounds, speakSpanish } from "@/lib/audio";
import { LingoMascot } from "@/components/mascot/LingoMascot";
import { getLearnerProfile } from "@/lib/api";
import { LearnerProfile } from "@/lib/types";
import {
  Settings,
  Volume2,
  VolumeX,
  Sun,
  Moon,
  Laptop,
  Globe,
  Clock,
  Sparkles,
  Check,
  Shield,
  Bell,
  Play,
} from "lucide-react";

export default function SettingsPage() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [profile, setProfile] = useState<LearnerProfile | null>(null);
  const [isMuted, setIsMuted] = useState(false);
  const [remindersEnabled, setRemindersEnabled] = useState(true);
  const [animationsEnabled, setAnimationsEnabled] = useState(true);
  const [saveToast, setSaveToast] = useState(false);

  useEffect(() => {
    setIsMuted(sounds.isMuted());
    getLearnerProfile()
      .then(setProfile)
      .catch(() => {});
  }, []);

  const handleToggleMute = () => {
    const next = !isMuted;
    sounds.setMuted(next);
    setIsMuted(next);
    if (!next) {
      sounds.playCorrect();
    }
  };

  const handleTestChime = () => {
    sounds.playCorrect();
  };

  const handleTestSpeech = () => {
    speakSpanish("¡Hola! Bienvenido a tu curso de español.");
  };

  const showSaveSuccess = () => {
    setSaveToast(true);
    setTimeout(() => setSaveToast(false), 2000);
  };

  return (
    <div className="min-h-screen bg-white dark:bg-[#131f24] flex transition-colors">
      <Sidebar />

      <div className="flex-1 md:ml-64 flex flex-col min-h-screen pb-20 md:pb-8">
        <TopHeader stats={profile?.stats || null} />

        <main className="flex-1 max-w-3xl mx-auto w-full px-4 sm:px-6 py-8">
          {/* Header */}
          <div className="mb-8 flex flex-col sm:flex-row items-center justify-between gap-4 p-6 rounded-3xl bg-gray-50 dark:bg-[#182830] border-2 border-gray-200 dark:border-[#2b3a42]">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-duo-blue/15 text-duo-blue rounded-2xl">
                <Settings className="w-8 h-8 stroke-[2.5]" />
              </div>
              <div>
                <h1 className="text-2xl sm:text-3xl font-black text-gray-800 dark:text-white">
                  Settings
                </h1>
                <p className="text-sm font-bold text-gray-500 dark:text-gray-400">
                  Manage your audio, visual theme, and learning preferences.
                </p>
              </div>
            </div>

            <LingoMascot expression="happy" size="sm" />
          </div>

          <div className="flex flex-col gap-6">
            {/* Section 1: Appearance & Theme */}
            <Card className="p-6 flex flex-col gap-4">
              <div className="flex items-center justify-between border-b border-gray-100 dark:border-[#283b44] pb-3">
                <div className="flex items-center gap-2">
                  <Sun className="w-5 h-5 text-amber-500" />
                  <h2 className="text-lg font-black text-gray-800 dark:text-white">
                    Appearance & Theme
                  </h2>
                </div>
                <span className="text-xs font-black text-gray-400 uppercase tracking-wider">
                  Active: {resolvedTheme}
                </span>
              </div>

              <p className="text-xs font-bold text-gray-500 dark:text-gray-400">
                Choose how LingoApp looks to you. Dark mode matches Duolingo&apos;s signature night palette.
              </p>

              <div className="grid grid-cols-3 gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setTheme("light");
                    showSaveSuccess();
                  }}
                  className={`flex flex-col items-center justify-center gap-2 p-4 rounded-2xl border-2 font-black text-xs transition-all ${
                    theme === "light"
                      ? "border-duo-blue bg-duo-blue-light/50 text-duo-blue shadow-[0_2px_0_0_#1899d6]"
                      : "border-gray-200 dark:border-[#2b3a42] text-gray-500 hover:bg-gray-50 dark:hover:bg-[#202f36]"
                  }`}
                >
                  <Sun className="w-6 h-6 text-amber-500" />
                  <span>Light</span>
                  {theme === "light" && <Check className="w-4 h-4 text-duo-blue" />}
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setTheme("dark");
                    showSaveSuccess();
                  }}
                  className={`flex flex-col items-center justify-center gap-2 p-4 rounded-2xl border-2 font-black text-xs transition-all ${
                    theme === "dark"
                      ? "border-duo-blue bg-duo-blue-light/50 dark:bg-[#1b3a4b] text-duo-blue dark:text-[#38bdf8] shadow-[0_2px_0_0_#1899d6]"
                      : "border-gray-200 dark:border-[#2b3a42] text-gray-500 hover:bg-gray-50 dark:hover:bg-[#202f36]"
                  }`}
                >
                  <Moon className="w-6 h-6 text-indigo-400" />
                  <span>Dark</span>
                  {theme === "dark" && <Check className="w-4 h-4 text-duo-blue dark:text-[#38bdf8]" />}
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setTheme("system");
                    showSaveSuccess();
                  }}
                  className={`flex flex-col items-center justify-center gap-2 p-4 rounded-2xl border-2 font-black text-xs transition-all ${
                    theme === "system"
                      ? "border-duo-blue bg-duo-blue-light/50 dark:bg-[#1b3a4b] text-duo-blue dark:text-[#38bdf8] shadow-[0_2px_0_0_#1899d6]"
                      : "border-gray-200 dark:border-[#2b3a42] text-gray-500 hover:bg-gray-50 dark:hover:bg-[#202f36]"
                  }`}
                >
                  <Laptop className="w-6 h-6 text-gray-400" />
                  <span>System</span>
                  {theme === "system" && <Check className="w-4 h-4 text-duo-blue dark:text-[#38bdf8]" />}
                </button>
              </div>
            </Card>

            {/* Section 2: Sound & Speech */}
            <Card className="p-6 flex flex-col gap-4">
              <div className="flex items-center justify-between border-b border-gray-100 dark:border-[#283b44] pb-3">
                <div className="flex items-center gap-2">
                  <Volume2 className="w-5 h-5 text-duo-blue" />
                  <h2 className="text-lg font-black text-gray-800 dark:text-white">
                    Sound & Audio Effects
                  </h2>
                </div>
                <span className="text-xs font-black text-gray-400 uppercase tracking-wider">
                  Web Audio API
                </span>
              </div>

              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 py-2 border-b border-gray-100 dark:border-[#283b44]">
                <div>
                  <h3 className="font-black text-sm text-gray-800 dark:text-white">
                    Lesson Sound Effects
                  </h3>
                  <p className="text-xs font-bold text-gray-400 dark:text-gray-400">
                    Audio chimes and victory fanfare synthesized in browser (no downloads).
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <Button
                    variant={isMuted ? "outline" : "green"}
                    size="sm"
                    onClick={handleToggleMute}
                    className="flex items-center gap-2"
                  >
                    {isMuted ? (
                      <>
                        <VolumeX className="w-4 h-4" />
                        <span>Muted</span>
                      </>
                    ) : (
                      <>
                        <Volume2 className="w-4 h-4" />
                        <span>Sound On</span>
                      </>
                    )}
                  </Button>

                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleTestChime}
                    title="Test chime sound"
                    disabled={isMuted}
                  >
                    <Play className="w-4 h-4" />
                    <span className="ml-1 text-xs">Test Chime</span>
                  </Button>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 py-2">
                <div>
                  <h3 className="font-black text-sm text-gray-800 dark:text-white">
                    Spanish Speech Synthesis (TTS)
                  </h3>
                  <p className="text-xs font-bold text-gray-400 dark:text-gray-400">
                    Native Web Speech API pronunciation for Spanish words and exercises.
                  </p>
                </div>

                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleTestSpeech}
                  className="flex items-center gap-2 shrink-0"
                >
                  <Volume2 className="w-4 h-4 text-duo-blue" />
                  <span>Listen to Sample</span>
                </Button>
              </div>
            </Card>

            {/* Section 3: Course & Curriculum Info */}
            <Card className="p-6 flex flex-col gap-4">
              <div className="flex items-center justify-between border-b border-gray-100 dark:border-[#283b44] pb-3">
                <div className="flex items-center gap-2">
                  <Globe className="w-5 h-5 text-emerald-500" />
                  <h2 className="text-lg font-black text-gray-800 dark:text-white">
                    Course Information
                  </h2>
                </div>
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 text-xs font-black">
                  Active
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-bold">
                <div className="p-3.5 rounded-2xl bg-gray-50 dark:bg-[#182830] border border-gray-200 dark:border-[#2b3a42] flex flex-col gap-1">
                  <span className="text-gray-400 uppercase tracking-wider text-[10px]">
                    Current Curriculum
                  </span>
                  <span className="text-sm font-black text-gray-800 dark:text-white">
                    Spanish (Español) A1
                  </span>
                  <span className="text-gray-400">CEFR Elementary Beginner</span>
                </div>

                <div className="p-3.5 rounded-2xl bg-gray-50 dark:bg-[#182830] border border-gray-200 dark:border-[#2b3a42] flex flex-col gap-1">
                  <span className="text-gray-400 uppercase tracking-wider text-[10px]">
                    Base / Native Language
                  </span>
                  <span className="text-sm font-black text-gray-800 dark:text-white">
                    English (US)
                  </span>
                  <span className="text-gray-400">Interface & Translation base</span>
                </div>

                <div className="p-3.5 rounded-2xl bg-gray-50 dark:bg-[#182830] border border-gray-200 dark:border-[#2b3a42] flex flex-col gap-1">
                  <span className="text-gray-400 uppercase tracking-wider text-[10px]">
                    Streak Rollover Timezone
                  </span>
                  <span className="text-sm font-black text-gray-800 dark:text-white flex items-center gap-1.5">
                    <Clock className="w-4 h-4 text-duo-orange" />
                    Asia/Kolkata (IST)
                  </span>
                  <span className="text-gray-400">Midnight reset evaluated on server</span>
                </div>

                <div className="p-3.5 rounded-2xl bg-gray-50 dark:bg-[#182830] border border-gray-200 dark:border-[#2b3a42] flex flex-col gap-1">
                  <span className="text-gray-400 uppercase tracking-wider text-[10px]">
                    Architecture & Security
                  </span>
                  <span className="text-sm font-black text-gray-800 dark:text-white flex items-center gap-1.5">
                    <Shield className="w-4 h-4 text-duo-green" />
                    Server-Authoritative
                  </span>
                  <span className="text-gray-400">FastAPI backend + SQLite WAL</span>
                </div>
              </div>
            </Card>

            {/* Section 4: Preferences & Toggles */}
            <Card className="p-6 flex flex-col gap-4">
              <div className="flex items-center justify-between border-b border-gray-100 dark:border-[#283b44] pb-3">
                <div className="flex items-center gap-2">
                  <Bell className="w-5 h-5 text-purple-500" />
                  <h2 className="text-lg font-black text-gray-800 dark:text-white">
                    Study Preferences
                  </h2>
                </div>
              </div>

              <div className="flex items-center justify-between py-2 border-b border-gray-100 dark:border-[#283b44]">
                <div>
                  <h3 className="font-black text-sm text-gray-800 dark:text-white">
                    Daily Practice Reminders
                  </h3>
                  <p className="text-xs font-bold text-gray-400">
                    Friendly reminders to maintain your habit and avoid losing streaks.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => {
                    setRemindersEnabled(!remindersEnabled);
                    showSaveSuccess();
                  }}
                  className={`w-12 h-7 rounded-full p-1 transition-colors ${
                    remindersEnabled ? "bg-duo-green" : "bg-gray-300 dark:bg-gray-600"
                  }`}
                >
                  <div
                    className={`w-5 h-5 rounded-full bg-white transition-transform ${
                      remindersEnabled ? "translate-x-5" : "translate-x-0"
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between py-2">
                <div>
                  <h3 className="font-black text-sm text-gray-800 dark:text-white">
                    Smooth Visual Animations
                  </h3>
                  <p className="text-xs font-bold text-gray-400">
                    Bouncing buttons, celebration confetti, and dynamic path transitions.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => {
                    setAnimationsEnabled(!animationsEnabled);
                    showSaveSuccess();
                  }}
                  className={`w-12 h-7 rounded-full p-1 transition-colors ${
                    animationsEnabled ? "bg-duo-green" : "bg-gray-300 dark:bg-gray-600"
                  }`}
                >
                  <div
                    className={`w-5 h-5 rounded-full bg-white transition-transform ${
                      animationsEnabled ? "translate-x-5" : "translate-x-0"
                    }`}
                  />
                </button>
              </div>
            </Card>

            {/* Save notification toast */}
            {saveToast && (
              <div className="fixed bottom-20 left-1/2 -translate-x-1/2 bg-gray-900 text-white dark:bg-white dark:text-gray-900 px-4 py-2 rounded-2xl font-black text-xs shadow-lg flex items-center gap-2 z-50 animate-fade-in">
                <Check className="w-4 h-4 text-duo-green" />
                <span>Preference saved</span>
              </div>
            )}
          </div>
        </main>
      </div>

      <BottomNav />
    </div>
  );
}
