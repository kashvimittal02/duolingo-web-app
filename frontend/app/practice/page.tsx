"use client";

import React, { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import confetti from "canvas-confetti";
import {
  Heart,
  AlertCircle,
  Sparkles,
  ArrowRight,
  X,
  CheckCircle2,
} from "lucide-react";
import {
  startPracticeSession,
  submitPracticeAnswer,
  completePracticeSession,
} from "@/lib/api";
import {
  PracticeStartResponse,
  SafeExercise,
  AnswerFeedbackResponse,
  PracticeCompletionResponse,
} from "@/lib/types";
import { LessonHeader } from "@/components/lesson/LessonHeader";
import { FeedbackBar } from "@/components/lesson/FeedbackBar";
import { LingoMascot } from "@/components/mascot/LingoMascot";
import { RewardIcon } from "@/components/rewards/RewardIcon";
import { MultipleChoice } from "@/components/lesson/exercises/MultipleChoice";
import { WordBank } from "@/components/lesson/exercises/WordBank";
import { MatchPairs } from "@/components/lesson/exercises/MatchPairs";
import { FillBlank } from "@/components/lesson/exercises/FillBlank";
import { TypeAnswer } from "@/components/lesson/exercises/TypeAnswer";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";
import { AudioButton } from "@/components/ui/AudioButton";
import { sounds } from "@/lib/audio";

function extractSpanishPromptText(prompt: string): string | null {
  if (!prompt) return null;
  if (/[áéíóúñ¿¡]/.test(prompt) && !/^(Select|Translate|Type|What|How|Tap)/i.test(prompt)) {
    return prompt;
  }
  const quoteMatch = prompt.match(/'([^']+)'/);
  if (quoteMatch && /[áéíóúñ]/.test(quoteMatch[1])) {
    return quoteMatch[1];
  }
  return null;
}

export default function PracticeSessionPage() {
  const router = useRouter();

  // Session State
  const [session, setSession] = useState<PracticeStartResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [initError, setInitError] = useState<string | null>(null);
  const [heartsFull, setHeartsFull] = useState(false);

  // Exercise Navigation State
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState<any>(null);

  // Feedback State
  const [feedbackStatus, setFeedbackStatus] = useState<"idle" | "correct" | "incorrect">("idle");
  const [feedbackSolution, setFeedbackSolution] = useState<string>("");
  const [submitting, setSubmitting] = useState(false);

  // Modals
  const [isExitModalOpen, setIsExitModalOpen] = useState(false);
  const [completionData, setCompletionData] = useState<PracticeCompletionResponse | null>(null);

  // Initialize Practice Session
  useEffect(() => {
    let mounted = true;
    const initSession = async () => {
      try {
        setLoading(true);
        setInitError(null);
        setHeartsFull(false);
        const data = await startPracticeSession();
        if (mounted) {
          setSession(data);
          setCurrentIndex(0);
        }
      } catch (err: any) {
        if (mounted) {
          const errMsg = err.message || "Failed to start practice session";
          setInitError(errMsg);
          if (errMsg.toLowerCase().includes("already full")) {
            setHeartsFull(true);
          }
        }
      } finally {
        if (mounted) setLoading(false);
      }
    };

    initSession();

    return () => {
      mounted = false;
    };
  }, []);

  const currentExercise: SafeExercise | null =
    session && session.exercises[currentIndex] ? session.exercises[currentIndex] : null;

  // Determine if answer can be submitted
  const canSubmit = Boolean(
    userAnswer !== null &&
      userAnswer !== "" &&
      (Array.isArray(userAnswer) ? userAnswer.length > 0 : true)
  );

  const handleSubmit = async () => {
    if (!session || !currentExercise || !canSubmit || submitting) return;

    try {
      setSubmitting(true);
      const res: AnswerFeedbackResponse = await submitPracticeAnswer(
        session.session_token,
        {
          exercise_id: currentExercise.id,
          answer: userAnswer,
        }
      );

      setFeedbackStatus(res.is_correct ? "correct" : "incorrect");
      setFeedbackSolution(res.correct_solution || "");
    } catch (err: any) {
      alert(`Answer submission error: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleContinue = async () => {
    if (!session) return;

    const nextIndex = currentIndex + 1;
    if (nextIndex < session.total_exercises) {
      // Advance to next practice exercise
      setCurrentIndex(nextIndex);
      setUserAnswer(null);
      setFeedbackStatus("idle");
      setFeedbackSolution("");
    } else {
      // Completed all exercises! Call practice completion endpoint
      try {
        setSubmitting(true);
        const comp = await completePracticeSession(session.session_token);
        setCompletionData(comp);
        sounds.playLessonComplete();
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 },
        });
      } catch (err: any) {
        alert(`Practice completion error: ${err.message}`);
      } finally {
        setSubmitting(false);
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-white dark:bg-[#131f24] flex flex-col items-center justify-center p-4 transition-colors">
        <div className="w-12 h-12 border-4 border-duo-green border-t-transparent rounded-full animate-spin mb-4" />
        <h3 className="text-gray-700 dark:text-gray-200 font-black text-lg uppercase tracking-wider">
          Preparing Practice Session...
        </h3>
      </div>
    );
  }

  // Hearts already full screen
  if (heartsFull) {
    return (
      <div className="min-h-screen bg-white dark:bg-[#131f24] flex flex-col items-center justify-center p-6 text-center max-w-md mx-auto transition-colors">
        <LingoMascot
          expression="sleeping"
          size="lg"
          speechBubble="Hearts are full! Take a break!"
          bubblePosition="top"
          className="mb-4"
        />
        <h2 className="text-2xl font-black text-gray-800 dark:text-white mb-2">Hearts Already Full!</h2>
        <p className="text-sm font-bold text-gray-500 dark:text-gray-400 mb-6">
          You already have 5/5 hearts! Practice is only needed when you need to recover lost hearts.
        </p>
        <Button variant="green" fullWidth onClick={() => router.push("/")}>
          Return to Learning Path
        </Button>
      </div>
    );
  }

  if (initError || !session || !currentExercise) {
    return (
      <div className="min-h-screen bg-white dark:bg-[#131f24] flex flex-col items-center justify-center p-6 text-center max-w-md mx-auto transition-colors">
        <div className="w-16 h-16 rounded-full bg-red-100 dark:bg-red-950/40 flex items-center justify-center mb-4 text-duo-red">
          <AlertCircle className="w-10 h-10" />
        </div>
        <h2 className="text-2xl font-black text-gray-800 dark:text-white mb-2">Practice Unavailable</h2>
        <p className="text-sm font-bold text-gray-500 dark:text-gray-400 mb-6">{initError}</p>
        <Button variant="green" fullWidth onClick={() => router.push("/")}>
          Return to Learning Path
        </Button>
      </div>
    );
  }

  const progressPercent = (currentIndex / session.total_exercises) * 100;

  return (
    <div className="min-h-screen bg-white dark:bg-[#131f24] flex flex-col justify-between select-none transition-colors">
      {/* Top Header */}
      <LessonHeader
        progress={progressPercent}
        hearts={session.current_hearts}
        onClose={() => setIsExitModalOpen(true)}
      />

      {/* Main Exercise View */}
      <main className="flex-1 max-w-2xl mx-auto w-full px-4 sm:px-6 py-6 flex flex-col justify-center">
        {/* Practice Eyebrow Badge */}
        <div className="mb-4 text-center sm:text-left">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 dark:bg-emerald-950/60 text-duo-green text-xs font-black uppercase tracking-wider border border-emerald-300 dark:border-emerald-700">
            <Heart className="w-3.5 h-3.5 fill-duo-red text-duo-red" />
            <span>Practice Session • Earn 1 Heart</span>
          </span>
        </div>

        {/* Exercise Prompt */}
        {(() => {
          const spanishPromptAudio = extractSpanishPromptText(currentExercise.prompt);
          return (
            <div className="mb-8 text-center sm:text-left">
              <div className="flex items-center justify-between sm:justify-start gap-3 mb-1">
                <h2 className="text-2xl sm:text-3xl font-black text-gray-800 dark:text-white leading-tight">
                  {currentExercise.prompt}
                </h2>
                {spanishPromptAudio && (
                  <AudioButton
                    text={spanishPromptAudio}
                    size="md"
                    label="Listen to prompt"
                  />
                )}
              </div>
              {currentExercise.prompt_translation && (
                <p className="text-sm sm:text-base font-bold text-gray-400 dark:text-gray-400">
                  {currentExercise.prompt_translation}
                </p>
              )}
            </div>
          );
        })()}

        {/* Exercise Component by Type */}
        <div className="w-full flex-1 flex flex-col justify-center">
          {currentExercise.exercise_type === "multiple_choice" && (
            <MultipleChoice
              exercise={currentExercise}
              selectedAnswer={userAnswer}
              onSelect={setUserAnswer}
              disabled={feedbackStatus !== "idle"}
            />
          )}

          {currentExercise.exercise_type === "word_bank" && (
            <WordBank
              exercise={currentExercise}
              selectedAnswer={userAnswer}
              onSelect={setUserAnswer}
              disabled={feedbackStatus !== "idle"}
            />
          )}

          {currentExercise.exercise_type === "match_pairs" && (
            <MatchPairs
              exercise={currentExercise}
              selectedAnswer={userAnswer}
              onSelect={setUserAnswer}
              disabled={feedbackStatus !== "idle"}
            />
          )}

          {currentExercise.exercise_type === "fill_blank" && (
            <FillBlank
              exercise={currentExercise}
              selectedAnswer={userAnswer}
              onSelect={setUserAnswer}
              disabled={feedbackStatus !== "idle"}
            />
          )}

          {currentExercise.exercise_type === "type_answer" && (
            <TypeAnswer
              exercise={currentExercise}
              selectedAnswer={userAnswer || ""}
              onSelect={setUserAnswer}
              disabled={feedbackStatus !== "idle"}
            />
          )}
        </div>
      </main>

      {/* Bottom Feedback Bar */}
      <FeedbackBar
        status={feedbackStatus}
        solution={feedbackSolution}
        canSubmit={canSubmit}
        onSubmit={handleSubmit}
        onContinue={handleContinue}
        loading={submitting}
      />

      {/* Exit Confirmation Modal */}
      <Modal
        isOpen={isExitModalOpen}
        onClose={() => setIsExitModalOpen(false)}
        title="Quit Practice Session?"
      >
        <div className="flex flex-col items-center text-center p-2">
          <LingoMascot
            expression="sad"
            size="md"
            speechBubble="Don't quit now!"
            bubblePosition="top"
            className="mb-3"
          />
          <h3 className="text-xl font-black text-gray-800 dark:text-white mb-2">
            Are you sure you want to quit?
          </h3>
          <p className="text-sm font-bold text-gray-500 dark:text-gray-400 mb-6 max-w-xs">
            If you leave now, your practice progress will be lost and you will not recover a heart.
          </p>
          <div className="w-full flex flex-col gap-3">
            <Button
              variant="green"
              fullWidth
              onClick={() => setIsExitModalOpen(false)}
            >
              Keep Practicing
            </Button>
            <Button
              variant="ghost"
              fullWidth
              onClick={() => router.push("/")}
            >
              Quit Session
            </Button>
          </div>
        </div>
      </Modal>

      {/* Practice Completion Modal */}
      {completionData && (
        <Modal
          isOpen={true}
          onClose={() => router.push("/")}
          showCloseButton={false}
          maxWidth="md"
        >
          <div className="flex flex-col items-center text-center p-4">
            <LingoMascot
              expression="cheering"
              size="lg"
              speechBubble="¡+1 Corazón ganado!"
              bubblePosition="top"
              className="mb-3 animate-bounce-subtle"
            />

            <h2 className="text-2xl sm:text-3xl font-black text-gray-800 dark:text-white mb-2">
              Practice Complete!
            </h2>

            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-2xl bg-red-100 dark:bg-red-950/60 border-2 border-red-300 dark:border-red-800 mb-4 animate-scale-in">
              <RewardIcon name="heart" size={28} animate />
              <span className="text-lg font-black text-duo-red">
                {completionData.heart_awarded ? "+1 Heart Recovered!" : "Hearts Full!"}
              </span>
            </div>

            <p className="text-sm font-bold text-gray-500 dark:text-gray-400 mb-4 max-w-sm">
              Great job practicing! You answered all exercises and your heart balance is now{" "}
              <span className="text-gray-800 dark:text-white font-extrabold">{completionData.hearts} / 5</span>.
            </p>

            <div className="w-full p-4 rounded-2xl bg-gray-50 dark:bg-[#1a2c35] border border-gray-200 dark:border-[#2b3a42] mb-6 flex items-center justify-around">
              <div className="flex flex-col items-center">
                <span className="text-xs font-black uppercase text-gray-400">Current Hearts</span>
                <div className="flex items-center gap-1.5 text-base font-black text-duo-red mt-1">
                  <RewardIcon name="heart" size={20} />
                  <span>{completionData.hearts} / 5</span>
                </div>
              </div>
              <div className="h-8 w-px bg-gray-200 dark:bg-[#2b3a42]" />
              <div className="flex flex-col items-center">
                <span className="text-xs font-black uppercase text-gray-400">XP Awarded</span>
                <span className="text-base font-black text-duo-yellow-dark dark:text-duo-yellow mt-1">0 XP (Practice)</span>
              </div>
            </div>

            <Button
              variant="green"
              size="lg"
              fullWidth
              onClick={() => router.push("/")}
            >
              Continue Learning
            </Button>
          </div>
        </Modal>
      )}
    </div>
  );
}
