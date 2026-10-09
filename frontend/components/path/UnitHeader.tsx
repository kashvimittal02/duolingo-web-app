import React from "react";
import { BookOpen } from "lucide-react";

interface UnitHeaderProps {
  orderIndex: number;
  title: string;
  description: string | null;
  hexColor: string;
}

export const UnitHeader: React.FC<UnitHeaderProps> = ({
  orderIndex,
  title,
  description,
  hexColor,
}) => {
  return (
    <div
      className="w-full rounded-3xl p-6 mb-8 text-white shadow-[0_6px_0_0_rgba(0,0,0,0.15)] relative overflow-hidden border-2 border-white/20 select-none transition-all"
      style={{ backgroundColor: hexColor || "#58cc02" }}
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          {/* Unit Eyebrow Badge */}
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-black/20 text-white/95 text-xs font-black tracking-widest uppercase mb-2">
            <span>Unit {orderIndex}</span>
          </div>

          <h2 className="text-xl sm:text-2xl font-black uppercase tracking-wide mb-1 leading-tight">
            {title}
          </h2>

          {description && (
            <p className="text-sm font-bold text-white/90 max-w-md leading-relaxed">
              {description}
            </p>
          )}
        </div>

        {/* Guidebook Button */}
        <div
          className="flex items-center gap-2 bg-white/20 hover:bg-white/30 border border-white/30 px-3.5 py-2.5 rounded-2xl backdrop-blur-xs font-black text-xs uppercase tracking-wider transition-all cursor-pointer shrink-0 shadow-[0_2px_0_0_rgba(0,0,0,0.1)] active:translate-y-0.5"
          title={`Unit ${orderIndex} Guidebook`}
        >
          <BookOpen className="w-5 h-5 stroke-[2.5]" />
          <span className="hidden sm:inline">Guidebook</span>
        </div>
      </div>
    </div>
  );
};
