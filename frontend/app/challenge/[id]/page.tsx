"use client";

import React, { useEffect, useState, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import confetti from "canvas-confetti";
import {
  Timer,
  AlertTriangle,
  Award,
  Sparkles,
  RotateCcw,
  Volume2,
  VolumeX,
  X,
  CheckCircle2,
} from "lucide-react";
import {
  startChallenge,
  getChallenge,
  submitChallengeAnswer,
  completeChallenge,
} from "@/lib/api";
import {
  ChallengeStartResponse,
  ChallengeStatusResponse,
  ChallengeAnswerResponse,
  ChallengeCompletionResponse,
  SafeExercise,
} from "@/lib/types";
import { MultipleChoice } from "@/components/lesson/exercises/MultipleChoice";
import { WordBank } from "@/components/lesson/exercises/WordBank";
import { MatchPairs } from "@/components/lesson/exercises/MatchPairs";
import { FillBlank } from "@/components/lesson/exercises/FillBlank";
import { TypeAnswer } from "@/components/lesson/exercises/TypeAnswer";
import { FeedbackBar } from "@/components/lesson/FeedbackBar";
import { AudioButton } from "@/components/ui/AudioButton";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { sounds } from "@/lib/audio";

export default function ChallengePage() {
  const params = useParams();
  const router = useRouter();
  const lessonId = Number(params?.id);

  const [loading, setLoading] = useState(true);
  const [initError, setInitError] = useState<string | null>(null);
  const [challenge, setChallenge] = useState<ChallengeStartResponse | null>(null);

  // Exercise Navigation State
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState<any>(null);
  const [feedbackStatus, setFeedbackStatus] = useState<
    "idle" | "correct" | "incorrect"
  >("idle");
  const [feedbackSolution, setFeedbackSolution] = useState("");
  const [submitting, setSubmitting] = useState(false);

  // Timer State (Server-synchronized)
  const [remainingSeconds, setRemainingSeconds] = useState(90);
  const [isTimedOut, setIsTimedOut] = useState(false);
  const [isExitModalOpen, setIsExitModalOpen] = useState(false);
  const [completionData, setCompletionData] =
    useState<ChallengeCompletionResponse | null>(null);

  // Audio mute state
  const [isMuted, setIsMuted] = useState(() => sounds.isMuted());

  // Initialize Challenge Session
  useEffect(() => {
    if (!lessonId) return;

    let mounted = true;
    const init = async () => {
      try {
        setLoading(true);
        setInitError(null);
        const data = await startChallenge(lessonId);
        if (mounted) {
          setChallenge(data);
          setRemainingSeconds(data.remaining_seconds);
          setCurrentIndex(0);
        }
      } catch (err: any) {
        if (mounted) {
          setInitError(err.message || "Failed to start challenge session");
        }
      } finally {
        if (mounted) setLoading(false);
      }
    };

    init();
    return () => {
      mounted = false;
    };
  }, [lessonId]);

  // Server-Synchronized Countdown Timer Interval
  useEffect(() => {
    if (!challenge || isTimedOut || completionData) return;

    const interval = setInterval(() => {
      setRemainingSeconds((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          handleTimeExpired();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [challenge, isTimedOut, completionData]);

  // Handle local timeout and verify with server
  const handleTimeExpired = async () => {
    setIsTimedOut(true);
    sounds.playIncorrect();
    if (challenge) {
      try {
        await getChallenge(challenge.challenge_token);
      } catch {
        // Ignored
      }
    }
  };

  const handleToggleSound = () => {
    const next = sounds.toggleMute();
    setIsMuted(next);
  };

  const currentExercise: SafeExercise | null =
    challenge && challenge.exercises[currentIndex]
      ? challenge.exercises[currentIndex]
      : null;

  const canSubmit = Boolean(
    userAnswer !== null &&
      userAnswer !== "" &&
      (Array.isArray(userAnswer) ? userAnswer.length > 0 : true)
  );

  // Handle Answer Submission
  const handleSubmit = async () => {
    if (!challenge || !currentExercise || !canSubmit || submitting || isTimedOut)
      return;

    try {
      setSubmitting(true);
      const res: ChallengeAnswerResponse = await submitChallengeAnswer(
        challenge.challenge_token,
        {
          exercise_id: currentExercise.id,
          answer: userAnswer,
        }
      );

      // Sync server authoritative time
      setRemainingSeconds(res.remaining_seconds);

      if (res.challenge_status === "timed_out" || res.is_expired) {
        handleTimeExpired();
        return;
      }

      if (res.is_correct) {
        setFeedbackStatus("correct");
        setFeedbackSolution("");
        sounds.playCorrect();
      } else {
        setFeedbackStatus("incorrect");
        setFeedbackSolution(res.correct_solution);
        sounds.playIncorrect();
      }
    } catch (err: any) {
      const msg = err.message || "";
      if (msg.toLowerCase().includes("expired") || msg.toLowerCase().includes("timed out")) {
        handleTimeExpired();
      }
    } finally {
      setSubmitting(false);
    }
  };

  // Continue to next exercise or complete
  const handleContinue = async () => {
    if (!challenge || isTimedOut) return;

    sounds.playTap();
    const nextIndex = currentIndex + 1;

    if (nextIndex < challenge.exercises.length) {
      setCurrentIndex(nextIndex);
      setUserAnswer(null);
      setFeedbackStatus("idle");
      setFeedbackSolution("");
    } else {
      // Completed all exercises - call completeChallenge
      try {
        setSubmitting(true);
        const comp = await completeChallenge(challenge.challenge_token);
        setCompletionData(comp);
        sounds.playLessonComplete();
        try {
          confetti({
            particleCount: 100,
            spread: 80,
            origin: { y: 0.6 },
          });
        } catch {}
      } catch (err: any) {
        const msg = err.message || "";
        if (msg.toLowerCase().includes("expired") || msg.toLowerCase().includes("timed out")) {
          handleTimeExpired();
        }
      } finally {
        setSubmitting(false);
      }
    }
  };

  const formatTimer = (totalSec: number) => {
    const mins = Math.floor(totalSec / 60);
    const secs = totalSec % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  // Loading State
  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 text-white flex flex-col items-center justify-center p-4">
        <div className="w-12 h-12 border-4 border-duo-purple border-t-transparent rounded-full animate-spin mb-4" />
        <p className="font-extrabold text-sm uppercase tracking-wider text-purple-300">
          Preparing Legendary Challenge...
        </p>
      </div>
    );
  }

  // Error State
  if (initError || !challenge || !currentExercise) {
    return (
      <div className="min-h-screen bg-white dark:bg-[#131f24] flex flex-col items-center justify-center p-6 text-center">
        <div className="w-16 h-16 rounded-2xl bg-red-100 dark:bg-red-950/60 flex items-center justify-center mb-4 text-duo-red">
          <AlertTriangle className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-black text-gray-800 dark:text-white mb-2">
          Challenge Unavailable
        </h2>
        <p className="text-sm font-bold text-gray-500 dark:text-gray-400 mb-6 max-w-sm">
          {initError || "Could not start the challenge. Complete previous lessons first."}
        </p>
        <Button variant="purple" onClick={() => router.push("/")}>
          Return to Learning Path
        </Button>
      </div>
    );
  }

  const timerPercent = (remainingSeconds / challenge.time_limit_seconds) * 100;
  const isUrgent = remainingSeconds <= 15;
  const isWarning = remainingSeconds <= 30 && remainingSeconds > 15;

  return (
    <div className="min-h-screen bg-[#faf5ff] dark:bg-[#13101c] flex flex-col transition-colors select-none">
      {/* Legendary Challenge Top Bar */}
      <header className="w-full max-w-3xl mx-auto py-3 px-4 flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsExitModalOpen(true)}
            className="text-gray-400 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-200 p-1.5 rounded-full hover:bg-purple-100 dark:hover:bg-purple-950/50 transition-colors"
            aria-label="Quit challenge"
            title="Quit challenge"
          >
            <X className="w-6 h-6 stroke-[2.5]" />
          </button>

          <button
            type="button"
            onClick={handleToggleSound}
            className={`p-1.5 rounded-full transition-colors ${
              isMuted
                ? "text-gray-400 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-200"
                : "text-duo-purple hover:text-purple-600 hover:bg-purple-50 dark:hover:bg-purple-950/40"
            }`}
            aria-label={isMuted ? "Unmute sounds" : "Mute sounds"}
            title={isMuted ? "Unmute sounds" : "Mute sounds"}
          >
            {isMuted ? (
              <VolumeX className="w-5 h-5 stroke-[2.2]" />
            ) : (
              <Volume2 className="w-5 h-5 stroke-[2.2]" />
            )}
          </button>
        </div>

        {/* Prominent Server Countdown Timer */}
        <div
          className={`flex items-center gap-2 px-3 py-1.5 rounded-2xl border-2 transition-all ${
            isUrgent
              ? "bg-red-100 dark:bg-red-950/70 border-red-400 text-duo-red animate-pulse shadow-md"
              : isWarning
              ? "bg-amber-50 dark:bg-amber-950/60 border-amber-400 text-amber-700 dark:text-amber-300"
              : "bg-purple-100 dark:bg-purple-950/70 border-purple-400 text-purple-800 dark:text-purple-300"
          }`}
        >
          <Timer className="w-5 h-5" />
          <span className="font-black text-lg tracking-wider tabular-nums font-mono">
            {formatTimer(remainingSeconds)}
          </span>
        </div>

        {/* Exercise Progress Counter */}
        <div className="text-xs font-black uppercase text-purple-700 dark:text-purple-300 bg-purple-100 dark:bg-purple-950/60 border border-purple-300 dark:border-purple-800 px-3 py-1 rounded-full">
          {currentIndex + 1} / {challenge.total_exercises}
        </div>
      </header>

      {/* Visual Timer Depletion Track */}
      <div className="w-full max-w-3xl mx-auto px-4 mb-2">
        <div className="w-full bg-purple-200 dark:bg-purple-950/80 h-2 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all duration-300 rounded-full ${
              isUrgent
                ? "bg-duo-red"
                : isWarning
                ? "bg-amber-400"
                : "bg-gradient-to-r from-purple-500 to-indigo-500"
            }`}
            style={{ width: `${Math.max(0, timerPercent)}%` }}
          />
        </div>
      </div>

      {/* Main Exercise Area */}
      <main className="flex-1 max-w-2xl mx-auto w-full px-4 sm:px-6 py-6 flex flex-col justify-center">
        {/* Prompt Header */}
        <div className="mb-8 text-center sm:text-left">
          <div className="flex items-center justify-between sm:justify-start gap-3 mb-1">
            <h2 className="text-2xl sm:text-3xl font-black text-gray-800 dark:text-white leading-tight">
              {currentExercise.prompt}
            </h2>
            <AudioButton
              text={currentExercise.prompt}
              size="md"
              label="Listen to prompt"
            />
          </div>
          {currentExercise.prompt_translation && (
            <p className="text-sm sm:text-base font-bold text-gray-400 dark:text-gray-400">
              {currentExercise.prompt_translation}
            </p>
          )}
        </div>

        {/* Dynamic Exercise Component */}
        <div className="w-full mb-16">
          {currentExercise.exercise_type === "multiple_choice" && (
            <MultipleChoice
              exercise={currentExercise}
              selectedAnswer={userAnswer}
              onSelect={setUserAnswer}
              disabled={feedbackStatus !== "idle" || isTimedOut}
            />
          )}

          {currentExercise.exercise_type === "word_bank" && (
            <WordBank
              exercise={currentExercise}
              selectedAnswer={userAnswer}
              onSelect={setUserAnswer}
              disabled={feedbackStatus !== "idle" || isTimedOut}
            />
          )}

          {currentExercise.exercise_type === "match_pairs" && (
            <MatchPairs
              exercise={currentExercise}
              selectedAnswer={userAnswer}
              onSelect={setUserAnswer}
              disabled={feedbackStatus !== "idle" || isTimedOut}
            />
          )}

          {currentExercise.exercise_type === "fill_blank" && (
            <FillBlank
              exercise={currentExercise}
              selectedAnswer={userAnswer}
              onSelect={setUserAnswer}
              disabled={feedbackStatus !== "idle" || isTimedOut}
            />
          )}

          {currentExercise.exercise_type === "type_answer" && (
            <TypeAnswer
              exercise={currentExercise}
              selectedAnswer={userAnswer || ""}
              onSelect={setUserAnswer}
              disabled={feedbackStatus !== "idle" || isTimedOut}
            />
          )}
        </div>
      </main>

      {/* Slide-Up Feedback Bottom Drawer */}
      <FeedbackBar
        status={feedbackStatus}
        solution={feedbackSolution}
        canSubmit={canSubmit && !isTimedOut}
        onSubmit={handleSubmit}
        onContinue={handleContinue}
        loading={submitting}
      />

      {/* Timeout / Failure Modal */}
      <Modal
        isOpen={isTimedOut && !completionData}
        onClose={() => router.push("/")}
        showCloseButton={false}
        maxWidth="sm"
      >
        <div className="flex flex-col items-center text-center p-3">
          <div className="w-20 h-20 rounded-full bg-red-100 dark:bg-red-950/60 flex items-center justify-center mb-4">
            <Timer className="w-12 h-12 text-duo-red stroke-[2.5]" />
          </div>

          <h2 className="text-2xl font-black text-gray-800 dark:text-white mb-2">
            Time Expired!
          </h2>

          <p className="text-sm font-bold text-gray-500 dark:text-gray-400 mb-6">
            The 90-second server limit elapsed before all 5 exercises were completed.
          </p>

          <div className="flex flex-col gap-3 w-full">
            <Button
              variant="purple"
              fullWidth
              onClick={() => window.location.reload()}
            >
              <div className="flex items-center justify-center gap-2">
                <RotateCcw className="w-4 h-4" />
                <span>Try Again</span>
              </div>
            </Button>
            <Button
              variant="outline"
              fullWidth
              onClick={() => router.push("/")}
            >
              <span>Return to Learning Path</span>
            </Button>
          </div>
        </div>
      </Modal>

      {/* Legendary Triumph Celebration Modal */}
      <Modal
        isOpen={Boolean(completionData)}
        onClose={() => router.push("/")}
        showCloseButton={false}
        maxWidth="md"
      >
        <div className="flex flex-col items-center text-center p-3">
          <div className="w-24 h-24 rounded-full bg-purple-100 dark:bg-purple-950/70 border-2 border-purple-300 dark:border-purple-600 flex items-center justify-center mb-4 animate-bounce-subtle">
            <Sparkles className="w-14 h-14 text-duo-purple fill-purple-400" />
          </div>

          <h2 className="text-2xl sm:text-3xl font-black text-gray-800 dark:text-white mb-1">
            Legendary Triumph!
          </h2>

          <p className="text-sm font-bold text-gray-500 dark:text-gray-400 mb-6">
            {completionData?.is_first_completion
              ? "Incredible speed! You conquered the timed challenge."
              : "Great practice! You conquered the timed challenge again."}
          </p>

          <div className="grid grid-cols-2 gap-3 w-full mb-6">
            <div className="bg-purple-50 dark:bg-[#201830] border-2 border-purple-200 dark:border-purple-800 rounded-2xl p-3 flex flex-col items-center">
              <span className="text-xs font-black text-purple-700 dark:text-purple-300 uppercase mb-1">
                Reward
              </span>
              <span className="text-xl font-black text-purple-900 dark:text-purple-200">
                +{completionData?.xp_awarded} XP
              </span>
            </div>

            <div className="bg-purple-50 dark:bg-[#201830] border-2 border-purple-200 dark:border-purple-800 rounded-2xl p-3 flex flex-col items-center">
              <span className="text-xs font-black text-purple-700 dark:text-purple-300 uppercase mb-1">
                Time Taken
              </span>
              <span className="text-xl font-black text-purple-900 dark:text-purple-200">
                {completionData?.time_taken_seconds}s
              </span>
            </div>
          </div>

          <Button
            variant="purple"
            size="lg"
            fullWidth
            onClick={() => router.push("/")}
          >
            Continue
          </Button>
        </div>
      </Modal>

      {/* Quit Challenge Confirmation Modal */}
      <Modal
        isOpen={isExitModalOpen}
        onClose={() => setIsExitModalOpen(false)}
        title="Abandon Challenge?"
        maxWidth="sm"
      >
        <div className="text-center p-2">
          <p className="text-sm font-bold text-gray-500 dark:text-gray-400 mb-6">
            Are you sure? The 90-second server clock keeps running in the background.
          </p>
          <div className="flex flex-col gap-3">
            <Button
              variant="red"
              fullWidth
              onClick={() => router.push("/")}
            >
              Quit Challenge
            </Button>
            <Button
              variant="outline"
              fullWidth
              onClick={() => setIsExitModalOpen(false)}
            >
              Keep Going
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
