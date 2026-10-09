import {
  LearnerProfile,
  RefillHeartsResponse,
  PracticeHeartResponse,
  CourseTree,
  LessonStatus,
  LessonStartResponse,
  SubmitAnswerRequest,
  AnswerFeedbackResponse,
  LessonCompletionResponse,
  LeaderboardResponse,
  ChallengeStartResponse,
  ChallengeStatusResponse,
  ChallengeAnswerResponse,
  ChallengeCompletionResponse,
  PracticeStartResponse,
  PracticeCompletionResponse,
} from "./types";

function getApiBase(): string {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  // When running in the browser, route through the Next.js proxy
  if (typeof window !== "undefined") {
    return "/api/v1";
  }
  // When running server-side (SSR / build), route to the internal backend URL
  const rawBackend =
    process.env.BACKEND_INTERNAL_URL || "http://127.0.0.1:8000";
  const internalBackend =
    rawBackend.startsWith("http://") || rawBackend.startsWith("https://")
      ? rawBackend
      : `https://${rawBackend}`;
  return `${internalBackend}/api/v1`;
}

const API_BASE = getApiBase();

export class ApiError extends Error {
  status: number;
  data: any;

  constructor(message: string, status: number, data?: any) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

async function fetchJson<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  try {
    const res = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
      ...options,
    });

    if (!res.ok) {
      let errorMsg = `API request failed with status ${res.status}`;
      let errorData: any = null;
      try {
        errorData = await res.json();
        if (errorData?.detail) {
          errorMsg = errorData.detail;
        }
      } catch {
        // Response was not JSON
      }
      throw new ApiError(errorMsg, res.status, errorData);
    }

    return (await res.json()) as T;
  } catch (err: any) {
    if (err instanceof ApiError) {
      throw err;
    }
    throw new ApiError(
      err?.message || "Network error. Could not connect to backend server.",
      0
    );
  }
}

// Learner API
export async function getLearnerProfile(): Promise<LearnerProfile> {
  return fetchJson<LearnerProfile>("/learner/me");
}

export async function refillHearts(): Promise<RefillHeartsResponse> {
  return fetchJson<RefillHeartsResponse>("/learner/refill-hearts", {
    method: "POST",
  });
}

export async function practiceEarnHeart(): Promise<PracticeHeartResponse> {
  return fetchJson<PracticeHeartResponse>("/learner/practice-heart", {
    method: "POST",
  });
}

// Learning Path / Course API
export async function getCourseTree(): Promise<CourseTree> {
  return fetchJson<CourseTree>("/courses/active/tree");
}

export async function getLessonStatus(lessonId: number): Promise<LessonStatus> {
  return fetchJson<LessonStatus>(`/lessons/${lessonId}/status`);
}

// Lesson Session Engine API
export async function startLesson(lessonId: number): Promise<LessonStartResponse> {
  return fetchJson<LessonStartResponse>(`/lessons/${lessonId}/start`, {
    method: "POST",
  });
}

export async function submitAnswer(
  sessionToken: string,
  payload: SubmitAnswerRequest
): Promise<AnswerFeedbackResponse> {
  return fetchJson<AnswerFeedbackResponse>(
    `/lessons/sessions/${sessionToken}/answer`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    }
  );
}

export async function completeLesson(
  sessionToken: string
): Promise<LessonCompletionResponse> {
  return fetchJson<LessonCompletionResponse>(
    `/lessons/sessions/${sessionToken}/complete`,
    {
      method: "POST",
    }
  );
}

// Leaderboard API
export async function getLeaderboard(): Promise<LeaderboardResponse> {
  return fetchJson<LeaderboardResponse>("/leaderboard");
}

// Legendary Timed Challenge Mode API
export async function startChallenge(lessonId: number): Promise<ChallengeStartResponse> {
  return fetchJson<ChallengeStartResponse>(`/challenges/${lessonId}/start`, {
    method: "POST",
  });
}

export async function getChallenge(challengeToken: string): Promise<ChallengeStatusResponse> {
  return fetchJson<ChallengeStatusResponse>(`/challenges/sessions/${challengeToken}`);
}

export async function submitChallengeAnswer(
  challengeToken: string,
  payload: { exercise_id: number; answer: any }
): Promise<ChallengeAnswerResponse> {
  return fetchJson<ChallengeAnswerResponse>(
    `/challenges/sessions/${challengeToken}/answer`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    }
  );
}

export async function completeChallenge(
  challengeToken: string
): Promise<ChallengeCompletionResponse> {
  return fetchJson<ChallengeCompletionResponse>(
    `/challenges/sessions/${challengeToken}/complete`,
    {
      method: "POST",
    }
  );
}

// Practice Mode API
export async function startPracticeSession(lessonId?: number): Promise<PracticeStartResponse> {
  return fetchJson<PracticeStartResponse>("/practice/start", {
    method: "POST",
    body: JSON.stringify(lessonId ? { lesson_id: lessonId } : {}),
  });
}

export async function submitPracticeAnswer(
  sessionToken: string,
  payload: { exercise_id: number; answer: any }
): Promise<AnswerFeedbackResponse> {
  return fetchJson<AnswerFeedbackResponse>(
    `/practice/sessions/${sessionToken}/answer`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    }
  );
}

export async function completePracticeSession(
  sessionToken: string
): Promise<PracticeCompletionResponse> {
  return fetchJson<PracticeCompletionResponse>(
    `/practice/sessions/${sessionToken}/complete`,
    {
      method: "POST",
    }
  );
}

