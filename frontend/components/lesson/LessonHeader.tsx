import React, { useState } from "react";
import { X, Heart, Volume2, VolumeX } from "lucide-react";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { sounds } from "@/lib/audio";

interface LessonHeaderProps {
  progress: number;
  hearts: number;
  onClose: () => void;
}

export const LessonHeader: React.FC<LessonHeaderProps> = ({
  progress,
  hearts,
  onClose,
}) => {
  const [isMuted, setIsMuted] = useState(() => sounds.isMuted());

  const handleToggleSound = () => {
    const nextMuted = sounds.toggleMute();
    setIsMuted(nextMuted);
  };

  return (
    <header className="w-full max-w-3xl mx-auto py-4 px-4 flex items-center justify-between gap-4">
      <div className="flex items-center gap-1.5">
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-200 p-1.5 rounded-full hover:bg-gray-100 dark:hover:bg-[#202f36] transition-colors"
          aria-label="Exit lesson"
          title="Exit lesson"
        >
          <X className="w-6 h-6 stroke-[2.5]" />
        </button>

        <button
          type="button"
          onClick={handleToggleSound}
          className={`p-1.5 rounded-full transition-colors ${
            isMuted
              ? "text-gray-400 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-[#202f36]"
              : "text-duo-blue hover:text-duo-blue-dark hover:bg-blue-50 dark:hover:bg-[#1b3a4b]"
          }`}
          aria-label={isMuted ? "Unmute sound effects" : "Mute sound effects"}
          title={isMuted ? "Unmute sound effects" : "Mute sound effects"}
        >
          {isMuted ? (
            <VolumeX className="w-5 h-5 stroke-[2.2]" />
          ) : (
            <Volume2 className="w-5 h-5 stroke-[2.2]" />
          )}
        </button>
      </div>

      {/* Progress Bar */}
      <div className="flex-1 px-2">
        <ProgressBar progress={progress} color="green" />
      </div>

      {/* Hearts Counter */}
      <div className="flex items-center gap-1.5 font-black text-duo-red select-none">
        <Heart className="w-6 h-6 fill-duo-red text-duo-red" />
        <span className="text-lg">{hearts}</span>
      </div>
    </header>
  );
};
