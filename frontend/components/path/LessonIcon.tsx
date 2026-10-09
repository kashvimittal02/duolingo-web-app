"use client";

import React from "react";
import Image from "next/image";
import { MessageCircle, Coffee, Compass, Users, Star, Trophy, BookOpen } from "lucide-react";

export type LessonBadgeType =
  | "vocab"
  | "conversation"
  | "grammar"
  | "review"
  | "checkpoint"
  | "message-circle"
  | "coffee"
  | "compass"
  | "users"
  | "star"
  | "trophy";

interface LessonIconProps {
  name: string;
  size?: number;
  className?: string;
}

export const LessonIcon: React.FC<LessonIconProps> = ({
  name,
  size = 36,
  className = "",
}) => {
  const badgeMap: Record<string, string> = {
    vocab: "/images/lessons/vocab.svg",
    conversation: "/images/lessons/conversation.svg",
    "message-circle": "/images/lessons/conversation.svg",
    grammar: "/images/lessons/grammar.svg",
    compass: "/images/lessons/grammar.svg",
    review: "/images/lessons/review.svg",
    star: "/images/lessons/review.svg",
    checkpoint: "/images/lessons/checkpoint.svg",
    trophy: "/images/lessons/checkpoint.svg",
  };

  const svgSrc = badgeMap[name.toLowerCase()];

  if (svgSrc) {
    return (
      <div
        className={`relative inline-flex items-center justify-center shrink-0 ${className}`}
        style={{ width: size, height: size }}
      >
        <Image
          src={svgSrc}
          alt={`Badge ${name}`}
          width={size}
          height={size}
          className="w-full h-full object-contain pointer-events-none drop-shadow-sm"
        />
      </div>
    );
  }

  // Fallback to Lucide icon
  switch (name) {
    case "coffee":
      return <Coffee className={`w-8 h-8 stroke-[2.5] ${className}`} />;
    case "users":
      return <Users className={`w-8 h-8 stroke-[2.5] ${className}`} />;
    default:
      return <Star className={`w-8 h-8 stroke-[2.5] ${className}`} />;
  }
};
