"use client";

import React, { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { startLesson, submitAnswer, completeLesson } from "@/lib/api";
import {
  LessonStartResponse,
  SafeExercise,
  AnswerFeedbackResponse,
  LessonCompletionResponse,
} from "@/lib/types";
import { LessonHeader } from "@/components/lesson/LessonHeader";
import { FeedbackBar } from "@/components/lesson/FeedbackBar";
import { LessonFailedModal } from "@/components/lesson/LessonFailedModal";
import { LessonCompleteModal } from "@/components/lesson/LessonCompleteModal";
import { MultipleChoice } from "@/components/lesson/exercises/MultipleChoice";
import { WordBank } from "@/components/lesson/exercises/WordBank";
import { MatchPairs } from "@/components/lesson/exercises/MatchPairs";
import { FillBlank } from "@/components/lesson/exercises/FillBlank";
import { TypeAnswer } from "@/components/lesson/exercises/TypeAnswer";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";
import { AudioButton } from "@/components/ui/AudioButton";
import { AlertCircle, HelpCircle } from "lucide-react";

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

export default function LessonSessionPage() {
  const params = useParams();
  const router = useRouter();
  const lessonId = Number(params.id);

  // Session State
  const [session, setSession] = useState<LessonStartResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [initError, setInitError] = useState<string | null>(null);

  // Exercise & Progression State
  const [currentIndex, setCurrentIndex] = useState(0);
  const [currentHearts, setCurrentHearts] = useState(5);
  const [userAnswer, setUserAnswer] = useState<any>(null);

  // Feedback State
  const [feedbackStatus, setFeedbackStatus] = useState<"idle" | "correct" | "incorrect">("idle");
  const [feedbackSolution, setFeedbackSolution] = useState<string>("");
  const [submitting, setSubmitting] = useState(false);

  // End State Modals
  const [isExitModalOpen, setIsExitModalOpen] = useState(false);
  const [isFailedModalOpen, setIsFailedModalOpen] = useState(false);
  const [completionData, setCompletionData] = useState<LessonCompletionResponse | null>(null);

  // Initialize Lesson Session
  useEffect(() => {
    if (!lessonId) return;

    let mounted = true;
    const initSession = async () => {
      try {
        setLoading(true);
        setInitError(null);
        const data = await startLesson(lessonId);
        if (mounted) {
          setSession(data);
          setCurrentHearts(data.current_hearts);
          setCurrentIndex(0);
        }
      } catch (err: any) {
        if (mounted) {
          setInitError(err.message || "Failed to start lesson session");
        }
      } finally {
        if (mounted) setLoading(false);
      }
    };

    initSession();

    return () => {
      mounted = false;
    };
  }, [lessonId]);

  const currentExercise: SafeExercise | null =
    session && session.exercises[currentIndex] ? session.exercises[currentIndex] : null;

  // Determine if answer is populated enough to enable submit button
  const canSubmit = Boolean(
    userAnswer !== null &&
      userAnswer !== "" &&
      (Array.isArray(userAnswer) ? userAnswer.length > 0 : true)
  );

  // Handle Answer Submission
  const handleSubmit = async () => {
    if (!session || !currentExercise || !canSubmit || submitting) return;

    try {
      setSubmitting(true);
      const res: AnswerFeedbackResponse = await submitAnswer(session.session_token, {
        exercise_id: currentExercise.id,
        answer: userAnswer,
      });

      // Update remaining hearts authoritative from backend response
      setCurrentHearts(res.remaining_hearts);

      if (res.is_correct) {
        setFeedbackStatus("correct");
        setFeedbackSolution("");
      } else {
        setFeedbackStatus("incorrect");
        setFeedbackSolution(res.correct_solution);

        // Check if session failed (0 hearts)
        if (res.session_status === "failed") {
          setIsFailedModalOpen(true);
        }
      }
    } catch (err: any) {
      alert(`Submission error: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  // Handle Continue to next exercise or complete lesson
  const handleContinue = async () => {
    if (!session) return;

    // If session failed, do not advance
    if (currentHearts <= 0) {
      setIsFailedModalOpen(true);
      return;
    }

    const nextIndex = currentIndex + 1;

    if (nextIndex < session.exercises.length) {
      // Advance to next exercise
      setCurrentIndex(nextIndex);
      setUserAnswer(null);
      setFeedbackStatus("idle");
      setFeedbackSolution("");
    } else {
      // Completed all exercises! Call completion endpoint
      try {
        setSubmitting(true);
        const comp = await completeLesson(session.session_token);
        setCompletionData(comp);
      } catch (err: any) {
        alert(`Completion error: ${err.message}`);
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
          Preparing Lesson...
        </h3>
      </div>
    );
  }

  if (initError || !session || !currentExercise) {
    return (
      <div className="min-h-screen bg-white dark:bg-[#131f24] flex flex-col items-center justify-center p-6 text-center max-w-md mx-auto transition-colors">
        <div className="w-16 h-16 rounded-full bg-red-100 dark:bg-red-950/40 flex items-center justify-center mb-4 text-duo-red">
          <AlertCircle className="w-10 h-10" />
        </div>
        <h2 className="text-2xl font-black text-gray-800 dark:text-white mb-2">Lesson Unavailable</h2>
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
        hearts={currentHearts}
        onClose={() => setIsExitModalOpen(true)}
      />

      {/* Main Exercise Interaction View */}
      <main className="flex-1 max-w-2xl mx-auto w-full px-4 sm:px-6 py-6 flex flex-col justify-center">
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

        {/* Dynamic Exercise Component by exercise_type */}
        <div className="w-full mb-16">
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

      {/* Slide-Up Feedback Bottom Drawer */}
      <FeedbackBar
        status={feedbackStatus}
        solution={feedbackSolution}
        canSubmit={canSubmit}
        onSubmit={handleSubmit}
        onContinue={handleContinue}
        loading={submitting}
      />

      {/* Confirmation modal when clicking close (X) */}
      <Modal
        isOpen={isExitModalOpen}
        onClose={() => setIsExitModalOpen(false)}
        title="Quit Lesson?"
        maxWidth="sm"
      >
        <div className="text-center p-2">
          <p className="text-sm font-bold text-gray-500 dark:text-gray-400 mb-6">
            Are you sure you want to quit? Your progress in this lesson will be lost.
          </p>
          <div className="flex flex-col gap-3">
            <Button
              variant="red"
              fullWidth
              onClick={() => router.push("/")}
            >
              Quit Lesson
            </Button>
            <Button
              variant="outline"
              fullWidth
              onClick={() => setIsExitModalOpen(false)}
            >
              Keep Learning
            </Button>
          </div>
        </div>
      </Modal>

      {/* 0 Hearts Failure Modal */}
      <LessonFailedModal
        isOpen={isFailedModalOpen}
        userGems={500}
        onRecovered={() => router.push("/")}
      />

      {/* Lesson Complete Celebration Modal */}
      <LessonCompleteModal
        isOpen={Boolean(completionData)}
        completionData={completionData}
      />
    </div>
  );
}
