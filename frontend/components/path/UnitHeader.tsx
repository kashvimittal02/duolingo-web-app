import React from "react";
import { useRouter } from "next/navigation";
import { BookOpen, ArrowLeft, ArrowRight, Play } from "lucide-react";

interface UnitHeaderProps {
  orderIndex: number;
  sectionIndex?: number;
  sectionTitle?: string;
  isCheckpoint?: boolean;
  title: string;
  description: string | null;
  hexColor: string;
  onBack?: () => void;
  onNext?: () => void;
  onSeeDetails?: () => void;
  onContinue?: () => void;
  hasPreviousSection?: boolean;
  hasNextSection?: boolean;
}

export const UnitHeader: React.FC<UnitHeaderProps> = ({
  orderIndex,
  sectionIndex = 1,
  sectionTitle = "Rookie Basics",
  isCheckpoint = false,
  title,
  description,
  hexColor,
  onBack,
  onNext,
  onSeeDetails,
  onContinue,
  hasPreviousSection = false,
  hasNextSection = false,
}) => {
  const router = useRouter();

  const handleBack = () => {
    if (onBack) {
      onBack();
    } else if (hasPreviousSection) {
      const prevElement = document.getElementById(`unit-${orderIndex - 1}`);
      if (prevElement) {
        prevElement.scrollIntoView({ behavior: "smooth" });
      } else {
        router.push("/sections");
      }
    } else {
      router.push("/sections");
    }
  };

  const handleNext = () => {
    if (onNext) {
      onNext();
    } else if (hasNextSection) {
      const nextElement = document.getElementById(`unit-${orderIndex + 1}`);
      if (nextElement) {
        nextElement.scrollIntoView({ behavior: "smooth" });
      }
    }
  };

  const handleSeeDetails = () => {
    if (onSeeDetails) {
      onSeeDetails();
    } else {
      router.push(`/sections?unit=${orderIndex}`);
    }
  };

  const displayUnitNumber =
    sectionIndex === 2 && orderIndex >= 7 ? orderIndex - 6 : orderIndex;
  const displayTitle = isCheckpoint
    ? "Section 1 Checkpoint Challenge"
    : title.replace(/^Unit \d+:\s*/, (match) =>
        sectionIndex === 2 ? `Unit ${displayUnitNumber}: ` : match
      );

  return (
    <div
      className="w-full rounded-2xl p-4 sm:p-5 mb-5 text-white shadow-[0_4px_0_0_rgba(0,0,0,0.15)] relative overflow-hidden border border-white/20 select-none transition-all"
      style={{ backgroundColor: hexColor || "#58cc02" }}
    >
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          {/* Top-Left Back Arrow */}
          <button
            type="button"
            onClick={handleBack}
            className="p-1.5 rounded-xl bg-black/20 hover:bg-black/35 text-white/95 transition-all cursor-pointer shrink-0 shadow-sm active:translate-y-0.5 flex items-center justify-center"
            title={hasPreviousSection ? "Previous section" : "View all course sections"}
            aria-label={hasPreviousSection ? "Go to previous section" : "View all course sections"}
          >
            <ArrowLeft className="w-4 h-4 stroke-[2.5]" />
          </button>

          <div>
            {/* Eyebrow Badge & Optional Forward Arrow */}
            <div className="flex items-center gap-2 mb-1">
              <div className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-black/20 text-white/95 text-[10px] font-black tracking-widest uppercase">
                <span>
                  {isCheckpoint
                    ? "Section Checkpoint"
                    : `${sectionTitle} • Unit ${displayUnitNumber}`}
                </span>
              </div>

              {hasNextSection && (
                <button
                  type="button"
                  onClick={handleNext}
                  className="p-0.5 rounded-full bg-black/20 hover:bg-black/35 text-white/95 transition-all cursor-pointer shadow-xs active:translate-y-0.5"
                  title="Go to next section"
                  aria-label="Go to next section"
                >
                  <ArrowRight className="w-3 h-3 stroke-[2.5]" />
                </button>
              )}
            </div>

            <h2 className="text-lg sm:text-xl font-black uppercase tracking-wide leading-tight">
              {displayTitle}
            </h2>

            {description && (
              <p className="text-xs font-bold text-white/90 max-w-md line-clamp-2 mt-0.5">
                {description}
              </p>
            )}
          </div>
        </div>

        {/* Right Action Controls: See Details & Continue */}
        <div className="flex items-center gap-2 self-end sm:self-center shrink-0">
          {/* See Details Button */}
          <button
            type="button"
            onClick={handleSeeDetails}
            className="flex items-center gap-1.5 bg-white/20 hover:bg-white/30 border border-white/30 px-3 py-1.5 rounded-xl backdrop-blur-xs font-black text-xs uppercase tracking-wider transition-all cursor-pointer shrink-0 shadow-xs active:translate-y-0.5 text-white"
            title={isCheckpoint ? "Checkpoint Details" : `Unit ${displayUnitNumber} Details`}
            aria-label={isCheckpoint ? "See Details for Checkpoint" : `See Details for Unit ${displayUnitNumber}`}
          >
            <BookOpen className="w-3.5 h-3.5 stroke-[2.5]" />
            <span>See Details</span>
          </button>

          {/* Continue Button if active lesson is available */}
          {onContinue && (
            <button
              type="button"
              onClick={onContinue}
              className="flex items-center gap-1.5 bg-white text-gray-900 hover:bg-gray-100 px-3.5 py-1.5 rounded-xl font-black text-xs uppercase tracking-wider transition-all cursor-pointer shadow-sm active:translate-y-0.5"
              title="Continue to next lesson"
              aria-label="Continue to next lesson"
            >
              <Play className="w-3 h-3 fill-gray-900 text-gray-900" />
              <span>Continue</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
