"use client";

import React from "react";
import { useRouter } from "next/navigation";
import {
  BookOpen,
  CheckCircle2,
  Lock,
  Play,
  ArrowRight,
  Sparkles,
  Layers,
  Award,
} from "lucide-react";
import { UnitNode } from "@/lib/types";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";

interface UnitDetailsModalProps {
  unit: UnitNode | null;
  isOpen: boolean;
  onClose: () => void;
  activeLessonId?: number | null;
  isUnlocked?: boolean;
}

// Curriculum vocabulary & phrase highlights for Spanish A1 units
const UNIT_HIGHLIGHTS: Record<number, { goals: string[]; vocab: string[] }> = {
  1: {
    goals: [
      "Greet people and make polite introductions",
      "Master essential Spanish greetings & courteous expressions",
    ],
    vocab: [
      "¡Hola! (Hello)",
      "Buenos días (Good morning)",
      "Adiós (Goodbye)",
      "Por favor (Please)",
      "Gracias (Thank you)",
      "Sí / No (Yes / No)",
    ],
  },
  2: {
    goals: [
      "Order food and beverages politely",
      "Identify common table essentials",
    ],
    vocab: [
      "El agua (The water)",
      "El pan (The bread)",
      "La leche (The milk)",
      "La manzana (The apple)",
      "El café (The coffee)",
      "Yo como / Yo bebo",
    ],
  },
  3: {
    goals: [
      "Identify household objects and places around town",
      "Use basic location prepositions and articles",
    ],
    vocab: [
      "La casa (The house)",
      "El libro (The book)",
      "La mesa (The table)",
      "El parque (The park)",
      "La tienda (The shop)",
      "Aquí / Allí (Here / There)",
    ],
  },
  4: {
    goals: [
      "Talk about family members",
      "Describe people using colors and adjectives",
    ],
    vocab: [
      "La madre (The mother)",
      "El padre (The father)",
      "El hermano (The brother)",
      "Grande / Pequeño (Big / Small)",
      "Rojo / Azul (Red / Blue)",
    ],
  },
  5: {
    goals: [
      "Conjugate common present tense verbs",
      "Form complete sentences describing daily actions",
    ],
    vocab: [
      "Yo hablo (I speak)",
      "Tú vives (You live)",
      "Nosotros comemos (We eat)",
      "Ellos escriben (They write)",
      "Siempre / Nunca",
    ],
  },
  6: {
    goals: [
      "Comprehensive Section 1 Checkpoint Challenge",
      "Demonstrate mastery of Rookie Basics to unlock Section 2",
    ],
    vocab: [
      "Review: Greetings & Politeness",
      "Review: Food & Household",
      "Review: Family & Descriptions",
      "Review: Action Verbs",
    ],
  },
  7: {
    goals: [
      "Navigate restaurants, menus, and market shopping",
      "Ask for prices and make purchases in Spanish",
    ],
    vocab: [
      "El restaurante (The restaurant)",
      "La cuenta (The bill)",
      "El menú (The menu)",
      "¿Cuánto cuesta? (How much?)",
      "La fruta (The fruit)",
      "El pescado (The fish)",
    ],
  },
  8: {
    goals: [
      "Describe daily morning and evening routines",
      "Express habits, schedules, and times of day",
    ],
    vocab: [
      "Por la mañana (In the morning)",
      "Por la noche (At night)",
      "Despertarse (To wake up)",
      "El trabajo (Work)",
      "La escuela (School)",
      "Temprano / Tarde",
    ],
  },
};

export const UnitDetailsModal: React.FC<UnitDetailsModalProps> = ({
  unit,
  isOpen,
  onClose,
  activeLessonId,
  isUnlocked = true,
}) => {
  const router = useRouter();

  if (!unit) return null;

  const highlights = UNIT_HIGHLIGHTS[unit.order_index] || {
    goals: ["Master key vocabulary and conversational patterns"],
    vocab: ["Essential core vocabulary"],
  };

  const totalLessons = unit.skills.reduce((acc, s) => acc + s.lessons.length, 0);
  const completedLessons = unit.skills.reduce(
    (acc, s) => acc + s.lessons.filter((l) => l.status === "completed").length,
    0
  );
  const percentComplete = totalLessons > 0 ? Math.round((completedLessons / totalLessons) * 100) : 0;

  const handleContinue = () => {
    onClose();
    if (activeLessonId) {
      router.push(`/lesson/${activeLessonId}`);
    } else {
      // Find first available or first lesson in unit
      const firstAvailable = unit.skills
        .flatMap((s) => s.lessons)
        .find((l) => l.status === "available");
      if (firstAvailable) {
        router.push(`/lesson/${firstAvailable.id}`);
      } else {
        router.push("/");
      }
    }
  };

  const handleViewAllSections = () => {
    onClose();
    router.push("/sections");
  };

  const isCheckpoint = unit.is_checkpoint || unit.order_index === 6;
  const displayUnitNumber =
    unit.section_index === 2 && unit.order_index >= 7
      ? unit.order_index - 6
      : unit.order_index;
  const modalTitle = isCheckpoint
    ? "Section 1 Checkpoint Challenge"
    : `${unit.section_title || (unit.section_index === 2 ? "Daily Life" : "Rookie Basics")} • Unit ${displayUnitNumber}`;
  const bannerBadge = isCheckpoint
    ? "Section 1 • Checkpoint Challenge"
    : `Section ${unit.section_index || 1}: ${unit.section_title || (unit.section_index === 2 ? "Daily Life" : "Rookie Basics")} • Unit ${displayUnitNumber}`;
  const displayUnitTitle = isCheckpoint
    ? "Section 1 Checkpoint Challenge"
    : unit.title.replace(/^Unit \d+:\s*/, (match) =>
        unit.section_index === 2 ? `Unit ${displayUnitNumber}: ` : match
      );

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={modalTitle}
      maxWidth="md"
    >
      <div className="flex flex-col gap-5 pt-1">
        {/* Banner Card */}
        <div
          className="rounded-2xl p-5 text-white shadow-sm relative overflow-hidden"
          style={{ backgroundColor: unit.hex_color || "#58cc02" }}
        >
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-black/20 text-white text-[11px] font-black uppercase tracking-wider mb-2">
            <span>{bannerBadge}</span>
          </div>
          <h3 className="text-xl font-black uppercase tracking-wide leading-tight mb-1">
            {displayUnitTitle}
          </h3>
          {unit.description && (
            <p className="text-xs sm:text-sm font-bold text-white/90 leading-relaxed">
              {unit.description}
            </p>
          )}

          <div className="mt-4 pt-3 border-t border-white/20 flex items-center justify-between text-xs font-bold">
            <span className="flex items-center gap-1.5">
              <Layers className="w-4 h-4" />
              <span>{unit.skills.length} Skills • {totalLessons} Lessons</span>
            </span>
            <span className="bg-white/25 px-2 py-0.5 rounded-full font-black">
              {percentComplete}% Complete
            </span>
          </div>
        </div>

        {/* Lock Warning if applicable */}
        {!isUnlocked && (
          <div className="p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/40 border-2 border-amber-200 dark:border-amber-800 text-amber-900 dark:text-amber-300 text-xs font-bold flex items-center gap-3">
            <Lock className="w-5 h-5 shrink-0 text-amber-600 dark:text-amber-400" />
            <div>
              <p className="font-extrabold uppercase tracking-wide">Unit Locked</p>
              <p className="text-amber-700 dark:text-amber-300/80">
                Complete all prerequisite lessons in{" "}
                {unit.order_index === 7
                  ? "Section 1 (including the Checkpoint Challenge)"
                  : unit.order_index === 6
                  ? "Section 1 (Units 1–5)"
                  : `Unit ${displayUnitNumber - 1}`}{" "}
                to unlock this unit.
              </p>
            </div>
          </div>
        )}

        {/* Learning Goals */}
        <div>
          <h4 className="text-xs font-black uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-2.5 flex items-center gap-1.5">
            <Award className="w-4 h-4 text-duo-yellow-dark dark:text-duo-yellow" />
            <span>Unit Goals & Objectives</span>
          </h4>
          <ul className="space-y-1.5">
            {highlights.goals.map((goal, idx) => (
              <li
                key={idx}
                className="text-xs font-bold text-gray-700 dark:text-gray-200 flex items-start gap-2 bg-gray-50 dark:bg-[#1a2c35] p-2.5 rounded-xl border border-gray-100 dark:border-[#2b3a42]"
              >
                <CheckCircle2 className="w-4 h-4 text-duo-green shrink-0 mt-0.5" />
                <span>{goal}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Vocabulary Preview */}
        <div>
          <h4 className="text-xs font-black uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-2 flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-duo-blue" />
            <span>Key Vocabulary Preview</span>
          </h4>
          <div className="flex flex-wrap gap-1.5">
            {highlights.vocab.map((word, idx) => (
              <span
                key={idx}
                className="px-2.5 py-1 rounded-xl bg-blue-50 dark:bg-[#1b3a4b] border border-blue-200 dark:border-[#2c5a73] text-duo-blue-dark dark:text-[#38bdf8] text-xs font-extrabold"
              >
                {word}
              </span>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="pt-2 flex flex-col sm:flex-row gap-3">
          {isUnlocked ? (
            <Button
              variant="green"
              fullWidth
              onClick={handleContinue}
            >
              <div className="flex items-center justify-center gap-2">
                <Play className="w-4 h-4 fill-white" />
                <span>Continue Lesson</span>
              </div>
            </Button>
          ) : (
            <Button
              variant="outline"
              fullWidth
              disabled
            >
              <div className="flex items-center justify-center gap-2 text-gray-400">
                <Lock className="w-4 h-4" />
                <span>Locked Section</span>
              </div>
            </Button>
          )}

          <Button
            variant="outline"
            fullWidth
            onClick={handleViewAllSections}
          >
            <span>View All Sections</span>
          </Button>
        </div>
      </div>
    </Modal>
  );
};
