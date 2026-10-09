"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { HeartCrack, Sparkles, Heart } from "lucide-react";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { LingoMascot } from "@/components/mascot/LingoMascot";
import { RewardIcon } from "@/components/rewards/RewardIcon";
import { refillHearts } from "@/lib/api";

interface LessonFailedModalProps {
  isOpen: boolean;
  userGems: number;
  onRecovered?: () => void;
}

export const LessonFailedModal: React.FC<LessonFailedModalProps> = ({
  isOpen,
  userGems,
  onRecovered,
}) => {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const handleRefill = async () => {
    try {
      setLoading(true);
      await refillHearts();
      if (onRecovered) onRecovered();
      router.push("/");
    } catch (err: any) {
      setMessage(err.message || "Could not refill hearts");
    } finally {
      setLoading(false);
    }
  };

  const handlePractice = () => {
    router.push("/practice");
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={() => router.push("/")}
      showCloseButton={false}
      maxWidth="md"
    >
      <div className="flex flex-col items-center text-center p-2">
        <LingoMascot
          expression="sad"
          size="lg"
          speechBubble="¡No te rindas! Practice to regain hearts"
          bubblePosition="top"
          className="mb-2"
        />

        <h2 className="text-2xl sm:text-3xl font-black text-gray-800 dark:text-white mb-2">
          You ran out of hearts!
        </h2>

        <p className="text-sm font-bold text-gray-500 dark:text-gray-400 mb-6 max-w-sm">
          Keep going by refilling your hearts with gems, or practice older lessons to earn a heart back.
        </p>

        {message && (
          <div className="w-full p-3 mb-4 rounded-xl bg-red-50 dark:bg-red-950/40 text-duo-red text-xs font-bold border border-red-200 dark:border-red-900/60">
            {message}
          </div>
        )}

        <div className="w-full flex flex-col gap-3">
          <Button
            variant="blue"
            fullWidth
            disabled={userGems < 350 || loading}
            onClick={handleRefill}
          >
            <div className="flex items-center justify-center gap-2">
              <Sparkles className="w-5 h-5" />
              <span>Refill Hearts (350 Gems)</span>
            </div>
          </Button>

          <Button
            variant="outline"
            fullWidth
            disabled={loading}
            onClick={handlePractice}
          >
            <div className="flex items-center justify-center gap-2">
              <RewardIcon name="heart" size={20} />
              <span>Practice to Recover 1 Heart</span>
            </div>
          </Button>

          <Button
            variant="ghost"
            fullWidth
            onClick={() => router.push("/")}
          >
            Return to Learning Path
          </Button>
        </div>
      </div>
    </Modal>
  );
};
