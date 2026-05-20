export type DifficultyLevel = "beginner" | "intermediate" | "advanced";
export type SubmissionStatus = "pending" | "completed" | "failed";

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
}

export interface ExerciseDetail {
  id: number;
  title: string;
  description: string;
  hint: string | null;
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
