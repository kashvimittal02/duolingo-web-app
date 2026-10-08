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
      className="w-full rounded-2xl p-5 mb-8 text-white shadow-md relative overflow-hidden"
      style={{ backgroundColor: hexColor || "#58cc02" }}
    >
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-xl sm:text-2xl font-black uppercase tracking-wide mb-1">
            {title}
          </h2>
          {description && (
            <p className="text-sm sm:text-base font-semibold text-white/90 max-w-md">
              {description}
            </p>
          )}
        </div>
        <div className="p-3 bg-white/20 rounded-xl backdrop-blur-xs flex items-center justify-center">
          <BookOpen className="w-6 h-6 stroke-[2.5]" />
        </div>
      </div>
    </div>
  );
};
