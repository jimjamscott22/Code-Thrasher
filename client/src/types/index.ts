export type DifficultyLevel = "beginner" | "intermediate" | "advanced";
export type SubmissionStatus = "pending" | "completed" | "failed";

export interface User {
  id: number;
  username: string;
  email: string;
  total_score: number;
  streak: number;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: "bearer";
  user: User;
}

export interface LoginRequest {
  username_or_email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
}

export interface ExerciseListItem {
  id: number;
  title: string;
  difficulty_level: DifficultyLevel;
  category: Category | null;
}

export interface TestCase {
  id: number;
  input_data: string;
  expected_output: string;
  score_weight: number;
  is_hidden: boolean;
}

export interface ExerciseGuideBlock {
  kind: "nudge" | "pattern" | "checklist" | "snippet" | string;
  title: string;
  body: string;
  code?: string | null;
}

export interface ExerciseDetail {
  id: number;
  title: string;
  description: string;
  hint: string | null;
  guide: ExerciseGuideBlock[];
  has_solution: boolean;
  difficulty_level: DifficultyLevel;
  starter_code: string;
  category: Category | null;
  test_cases: TestCase[];
}

export interface TestCaseResult {
  test_case_id: number;
  passed: boolean;
  expected: string;
  actual: string;
  score_weight: number;
}

export interface SubmitResponse {
  submission_id: number;
  status: SubmissionStatus;
  score: number;
  stdout: string;
  stderr: string;
  time_taken_ms: number;
  test_results: TestCaseResult[];
}

export interface ExerciseSolution {
  exercise_id: number;
  code: string;
  explanation: string | null;
}
