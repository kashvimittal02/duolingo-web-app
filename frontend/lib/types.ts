// TypeScript interfaces strictly matching FastAPI Pydantic schemas

export interface Achievement {
  id: number;
  code: string;
  title: string;
  description: string;
  icon_name: string;
  is_unlocked: boolean;
  unlocked_at: string | null;
}

export interface LearnerStats {
  xp: number;
  hearts: number;
  max_hearts: number;
  gems: number;
  streak: number;
  has_practiced_today: boolean;
  next_heart_in_seconds: number | null;
  daily_xp: number;
  daily_xp_goal: number;
}

export interface LearnerProfile {
  id: number;
  username: string;
  display_name: string;
  avatar_url: string | null;
  created_at: string;
  stats: LearnerStats;
  total_crowns: number;
  achievements: Achievement[];
}

export interface RefillHeartsResponse {
  hearts: number;
  gems: number;
  message: string;
}

export interface PracticeHeartResponse {
  hearts: number;
  xp_awarded: number;
  message: string;
}

export type NodeStatus = "locked" | "available" | "completed";

export interface LessonNode {
  id: number;
  order_index: number;
  title: string;
  xp_reward: number;
  status: NodeStatus;
  is_completed: boolean;
  completion_count: number;
}

export interface SkillNode {
  id: number;
  unit_id: number;
  order_index: number;
  title: string;
  icon_name: string;
  status: NodeStatus;
  crowns: number;
  total_crown_levels: number;
  current_lesson_index: number;
  lessons: LessonNode[];
}

export interface UnitNode {
  id: number;
  course_id: number;
  section_index?: number;
  section_title?: string;
  order_index: number;
  title: string;
  description: string | null;
  hex_color: string;
  is_unlocked?: boolean;
  is_checkpoint?: boolean;
  skills: SkillNode[];
}

export interface CourseTree {
  course_id: number;
  code: string;
  title: string;
  target_lang: string;
  units: UnitNode[];
}

export interface LessonStatus {
  lesson_id: number;
  skill_id: number;
  skill_title: string;
  status: NodeStatus;
  can_start: boolean;
  rejection_reason: string | null;
}

export type ExerciseType =
  | "multiple_choice"
  | "word_bank"
  | "match_pairs"
  | "fill_blank"
  | "type_answer";

export interface SafeExercise {
  id: number;
  order_index: number;
  exercise_type: ExerciseType;
  prompt: string;
  prompt_translation: string | null;
  payload: Record<string, any>;
  target_lang?: string;
}

export interface LessonStartResponse {
  session_token: string;
  lesson_id: number;
  lesson_title: string;
  total_exercises: number;
  initial_hearts: number;
  current_hearts: number;
  exercises: SafeExercise[];
}

export interface SubmitAnswerRequest {
  exercise_id: number;
  answer: any;
}

export interface AnswerFeedbackResponse {
  is_correct: boolean;
  feedback_title: string;
  correct_solution: string;
  remaining_hearts: number;
  session_status: "in_progress" | "failed";
  is_duplicate: boolean;
  completed_exercises: number;
  total_exercises: number;
}

export interface LessonCompletionResponse {
  status: "completed";
  session_token: string;
  lesson_id: number;
  xp_awarded: number;
  total_xp: number;
  streak: number;
  is_replay: boolean;
  crowns: number;
  achievements_unlocked: string[];
  is_idempotent: boolean;
}

export interface LeaderboardEntry {
  rank: number;
  username: string;
  display_name: string;
  avatar_url: string | null;
  xp: number;
  is_current_user: boolean;
}

export interface LeaderboardResponse {
  league_name: string;
  days_remaining: number;
  rankings: LeaderboardEntry[];
}

export interface ChallengeStartResponse {
  challenge_token: string;
  lesson_id: number;
  lesson_title: string;
  time_limit_seconds: number;
  started_at: string;
  expires_at: string;
  remaining_seconds: number;
  total_exercises: number;
  exercises: SafeExercise[];
}

export interface ChallengeStatusResponse {
  challenge_token: string;
  lesson_id: number;
  lesson_title: string;
  status: "in_progress" | "completed" | "timed_out" | "failed";
  time_limit_seconds: number;
  remaining_seconds: number;
  is_expired: boolean;
  completed_exercises: number;
  total_exercises: number;
  current_exercise_index: number;
  exercises: SafeExercise[];
}

export interface ChallengeAnswerResponse {
  is_correct: boolean;
  feedback_title: string;
  correct_solution: string;
  challenge_status: "in_progress" | "completed" | "timed_out" | "failed";
  remaining_seconds: number;
  is_expired: boolean;
  is_duplicate: boolean;
  completed_exercises: number;
  total_exercises: number;
}

export interface ChallengeCompletionResponse {
  status: "completed" | "timed_out" | "failed";
  challenge_token: string;
  lesson_id: number;
  xp_awarded: number;
  total_xp: number;
  time_taken_seconds: number;
  is_first_completion: boolean;
  is_idempotent: boolean;
}

export interface PracticeStartResponse {
  session_token: string;
  lesson_id: number;
  lesson_title: string;
  total_exercises: number;
  exercises: SafeExercise[];
  current_hearts: number;
  max_hearts: number;
}

export interface PracticeCompletionResponse {
  status: string;
  session_token: string;
  hearts: number;
  heart_awarded: boolean;
  message: string;
  is_idempotent: boolean;
}

