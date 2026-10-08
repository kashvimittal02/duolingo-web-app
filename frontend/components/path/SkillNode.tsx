import React from "react";
import { Lock, Crown, Check, MessageCircle, Coffee, Compass, Users, Star } from "lucide-react";
import { SkillNode as SkillNodeType } from "@/lib/types";

interface SkillNodeProps {
  skill: SkillNodeType;
  unitColor: string;
  onClick: () => void;
  offset?: number; // horizontal displacement for path curvature
}

const getIcon = (name: string) => {
  switch (name) {
    case "message-circle":
      return MessageCircle;
    case "coffee":
      return Coffee;
    case "compass":
      return Compass;
    case "users":
      return Users;
    default:
      return Star;
  }
};

export const SkillNode: React.FC<SkillNodeProps> = ({
  skill,
  unitColor,
  onClick,
  offset = 0,
}) => {
  const IconComponent = getIcon(skill.icon_name);
  const isLocked = skill.status === "locked";
  const isCompleted = skill.status === "completed";

  // Stepping stone 3D style
  const getButtonStyle = () => {
    if (isLocked) {
      return "bg-gray-200 dark:bg-[#202f36] border-gray-300 dark:border-[#37464f] text-gray-400 dark:text-[#55656e] shadow-[0_6px_0_0_#cbd5e1] dark:shadow-[0_6px_0_0_#182329] cursor-not-allowed";
    }
    if (isCompleted) {
      return "bg-duo-yellow border-duo-yellow-dark text-white shadow-[0_6px_0_0_#e5a400] hover:brightness-105 active:translate-y-[2px] active:shadow-none cursor-pointer";
    }
    return "bg-duo-green border-duo-green-dark text-white shadow-[0_6px_0_0_#46a302] hover:brightness-105 active:translate-y-[2px] active:shadow-none cursor-pointer animate-bounce-subtle";
  };

  return (
    <div
      className="flex flex-col items-center my-4 transition-transform duration-300"
      style={{ transform: `translateX(${offset}px)` }}
    >
      <div className="relative">
        {/* Crown Badge */}
        {!isLocked && (
          <div className="absolute -top-2 -right-2 z-10 flex items-center gap-0.5 bg-duo-yellow border-2 border-white dark:border-[#131f24] px-2 py-0.5 rounded-full shadow-sm text-xs font-black text-amber-900">
            <Crown className="w-3.5 h-3.5 fill-amber-500 text-amber-700" />
            <span>{skill.crowns}</span>
          </div>
        )}

        {/* Circular Stepping Stone */}
        <button
          disabled={isLocked}
          onClick={onClick}
          className={`
            w-20 h-20 rounded-full border-4 flex items-center justify-center transition-all duration-100 select-none
            ${getButtonStyle()}
          `}
          aria-label={skill.title}
        >
          {isLocked ? (
            <Lock className="w-8 h-8 stroke-[2.5]" />
          ) : isCompleted ? (
            <Check className="w-10 h-10 stroke-[3]" />
          ) : (
            <IconComponent className="w-9 h-9 stroke-[2.5]" />
          )}
        </button>
      </div>

      {/* Skill Label */}
      <span className="mt-2 text-sm font-black text-gray-700 dark:text-gray-200 max-w-[120px] text-center leading-tight">
        {skill.title}
      </span>
    </div>
  );
};
