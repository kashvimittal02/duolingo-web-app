import React, { useEffect } from "react";
import { CheckCircle2, XCircle } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { AudioButton } from "@/components/ui/AudioButton";
import { LingoMascot } from "@/components/mascot/LingoMascot";
import { sounds } from "@/lib/audio";

interface FeedbackBarProps {
  status: "idle" | "correct" | "incorrect";
  solution?: string;
  canSubmit: boolean;
  onSubmit: () => void;
  onContinue: () => void;
  loading?: boolean;
}

export const FeedbackBar: React.FC<FeedbackBarProps> = ({
  status,
  solution,
  canSubmit,
  onSubmit,
  onContinue,
  loading = false,
}) => {
  useEffect(() => {
    if (status === "correct") {
      sounds.playCorrect();
    } else if (status === "incorrect") {
      sounds.playIncorrect();
    }
  }, [status]);

  if (status === "idle") {
    return (
      <div className="fixed bottom-0 left-0 right-0 bg-white dark:bg-[#131f24] border-t-2 border-gray-200 dark:border-[#2b3a42] py-4 px-4 sm:px-8 z-30 transition-colors">
        <div className="max-w-2xl mx-auto flex items-center justify-end">
          <Button
            variant="green"
            size="lg"
            disabled={!canSubmit || loading}
            onClick={onSubmit}
            className="w-full sm:w-44"
          >
            {loading ? "Checking..." : "Check"}
          </Button>
        </div>
      </div>
    );
  }

  const isCorrect = status === "correct";

  return (
    <div
      className={`
        fixed bottom-0 left-0 right-0 py-6 px-4 sm:px-8 z-30 border-t-2 transition-all duration-200 animate-slide-up
        ${
          isCorrect
            ? "bg-duo-green-light dark:bg-[#0e3a22] border-duo-green text-emerald-900 dark:text-emerald-100"
            : "bg-duo-red-light dark:bg-[#3d181c] border-duo-red text-red-950 dark:text-red-100"
        }
      `}
    >
      <div className="max-w-2xl mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        {/* Status Message & Mascot */}
        <div className="flex items-center gap-3">
          <LingoMascot
            expression={isCorrect ? "cheering" : "sad"}
            size="sm"
            className="hidden sm:inline-flex shrink-0"
          />

          <div className="flex items-start gap-3">
            {isCorrect ? (
              <div className="p-1 bg-white dark:bg-[#131f24] rounded-full text-duo-green shrink-0">
                <CheckCircle2 className="w-8 h-8 fill-duo-green text-white" />
              </div>
            ) : (
              <div className="p-1 bg-white dark:bg-[#131f24] rounded-full text-duo-red shrink-0">
                <XCircle className="w-8 h-8 fill-duo-red text-white" />
              </div>
            )}

            <div>
              <h3 className="text-xl font-black mb-0.5">
                {isCorrect ? "Nicely done!" : "Incorrect"}
              </h3>
              {!isCorrect && solution && (
                <div className="flex items-center gap-2 mt-1">
                  <p className="text-sm font-bold text-red-900/80 dark:text-red-200/90">
                    Correct solution:{" "}
                    <span className="font-extrabold text-red-950 dark:text-white">{solution}</span>
                  </p>
                  <AudioButton
                    text={solution}
                    size="sm"
                    label="Listen to correct solution"
                  />
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Action Button */}
        <Button
          variant={isCorrect ? "green" : "red"}
          size="lg"
          onClick={onContinue}
          className="w-full sm:w-44"
        >
          Continue
        </Button>
      </div>
    </div>
  );
};
