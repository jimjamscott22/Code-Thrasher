This file is a merged representation of the entire codebase, combined into a single document by Repomix.
The content has been processed where line numbers have been added, content has been compressed (code blocks are separated by ⋮---- delimiter).

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Line numbers have been added to the beginning of each line
- Content has been compressed - code blocks are separated by ⋮---- delimiter
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.claude/
  settings.local.json
client/
  src/
    api/
      client.ts
    components/
      editor/
        CodeEditor.tsx
      exercise/
        ExerciseGuidePanel.tsx
      layout/
        Footer.tsx
        Navbar.tsx
    pages/
      Dashboard.tsx
      ExerciseDetail.tsx
    services/
      pyodide.ts
    store/
      useProgressStore.ts
    types/
      index.ts
    App.tsx
    index.css
    main.tsx
  .eslintrc.cjs
  index.html
  package.json
  postcss.config.js
  tailwind.config.js
  tsconfig.json
  tsconfig.node.json
  vite.config.ts
docs/
  agent_prompt.md
  code-thrasher-scrnsht.png
  implementation_plan.md
  spec.md
server/
  alembic/
    versions/
      0001_initial_schema.py
      0003_make_submission_user_id_nullable.py
      0004_add_exercise_guides.py
      71d51bde7666_add_missing_indexes.py
    env.py
    script.py.mako
  app/
    api/
      v1/
        endpoints/
          __init__.py
          exercises.py
          progress.py
          submit.py
        __init__.py
      __init__.py
    core/
      __init__.py
      config.py
    db/
      __init__.py
      database.py
    models/
      __init__.py
      models.py
    schemas/
      __init__.py
      schemas.py
    services/
      __init__.py
    __init__.py
    main.py
  tests/
    __init__.py
    conftest.py
    test_exercises.py
    test_progress.py
    test_submit.py
  alembic.ini
  Dockerfile
  pyproject.toml
  seed.py
.env.example
.gitignore
CLAUDE.md
docker-compose.yml
LICENSE
README.md
```

# Files

## File: client/src/components/editor/CodeEditor.tsx
````typescript
import Editor from "@monaco-editor/react";
⋮----
interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  height?: string;
  readOnly?: boolean;
}
⋮----
export default function CodeEditor({
  value,
  onChange,
  height = "400px",
  readOnly = false,
}: CodeEditorProps)
⋮----
onChange=
````

## File: client/src/components/exercise/ExerciseGuidePanel.tsx
````typescript
import { useEffect, useMemo, useState } from "react";
import api from "@/api/client";
import type { ExerciseGuideBlock, ExerciseSolution } from "@/types";
⋮----
type ExerciseGuidePanelProps = {
  exerciseId: number;
  guide: ExerciseGuideBlock[];
  fallbackHint: string | null;
  hasSolution: boolean;
};
⋮----
function getKindClasses(kind: string)
⋮----
function toggleBlock(index: number)
⋮----
async function revealSolution()
````

## File: client/src/components/layout/Footer.tsx
````typescript
export default function Footer()
````

## File: client/src/services/pyodide.ts
````typescript
// Loads Pyodide from CDN and runs Python code in the browser.
// The first call to runPython triggers a ~10 MB download; all subsequent calls are instant.
⋮----
interface PyodideInstance {
  runPythonAsync(code: string): Promise<unknown>;
  setStdout(options: { batched: (text: string) => void }): void;
  setStderr(options: { batched: (text: string) => void }): void;
}
⋮----
runPythonAsync(code: string): Promise<unknown>;
setStdout(options:
setStderr(options:
⋮----
interface Window {
    loadPyodide(config: { indexURL: string }): Promise<PyodideInstance>;
  }
⋮----
loadPyodide(config:
⋮----
export interface RunResult {
  stdout: string;
  stderr: string;
  durationMs: number;
}
⋮----
function injectScript(src: string): Promise<void>
⋮----
export function getPyodide(): Promise<PyodideInstance>
⋮----
export async function runPython(code: string): Promise<RunResult>
⋮----
// Run in a fresh namespace so repeated calls don't share state
⋮----
// Restore defaults so stray output doesn't accumulate
````

## File: client/src/store/useProgressStore.ts
````typescript
import { create } from "zustand";
import api from "@/api/client";
⋮----
export interface ExerciseProgress {
  best_score: number;
  attempts: number;
  solved: boolean;
}
⋮----
interface ProgressState {
  totalExercises: number;
  completedCount: number;
  exercises: Record<number, ExerciseProgress>;
  loaded: boolean;
  fetch: () => Promise<void>;
}
````

## File: client/src/index.css
````css
@tailwind base;
@tailwind components;
@tailwind utilities;
⋮----
@layer base {
⋮----
body {
⋮----
::-webkit-scrollbar {
::-webkit-scrollbar-track {
⋮----
@apply bg-gray-900;
⋮----
::-webkit-scrollbar-thumb {
````

## File: client/src/main.tsx
````typescript
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
````

## File: client/.eslintrc.cjs
````javascript

````

## File: client/index.html
````html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Code Thrasher</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap"
      rel="stylesheet"
    />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
````

## File: client/postcss.config.js
````javascript

````

## File: client/tailwind.config.js
````javascript
/** @type {import('tailwindcss').Config} */
````

## File: client/tsconfig.json
````json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
````

## File: client/tsconfig.node.json
````json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}
````

## File: docs/agent_prompt.md
````markdown
# Project Code-Thrasher: AI Implementation Prompt

**Role:** Senior Full-Stack Software Engineer & Architect  
**Project Name:** Code-Thrasher  
**Primary Objective:** Build a web-based platform for bite-sized Python coding exercises tailored for learners of all levels.  

---

## 1. Context & Vision
**Code-Thrasher** is a modern, gamified learning platform designed to help users master Python through small, focused challenges. Unlike massive bootcamps, this application focuses on "bite-sized" success—quick wins that build momentum. 

The system must allow users to:
- View exercise descriptions and requirements.
- Write code in a secure, syntax-highlighted editor.
- Run code instantly (or submit for grading).
- Receive immediate feedback (Pass/Fail) with test case results.
- Track progress across different difficulty levels.

**Target Audience:** Beginners to Intermediate developers who want practical, hands-on practice without overwhelming complexity.

---

## 2. Technical Stack & Architecture
You must strictly adhere to the following technology preferences:

### Backend (Python)
- **Framework:** FastAPI (preferred for type safety and auto-docs) or Flask if legacy constraints apply. *Decision: Use FastAPI.*
- **Data Validation:** Pydantic V2.
- **Database:** PostgreSQL (production-ready schema design).
- **ORM:** SQLAlchemy 2.0+ with Alembic for migrations.
- **Code Execution Sandbox:** You must architect a secure execution environment. Do not run user code directly on the main service process. Recommendation: Use Docker-based containers or a restricted VM approach for evaluating submissions to prevent filesystem access or command injection.
- **Testing:** Pytest (Backend unit tests).

### Frontend (React)
- **Core:** React 18+ with Vite.
- **Language:** TypeScript (strict mode enabled).
- **UI Framework:** Tailwind CSS for utility-first styling.
- **Code Editor:** Monaco Editor (VS Code engine) or Ace Editor (if licensing is a concern). *Decision: Use Monaco.*
- **State Management:** Zustand (lightweight, no Redux overhead).
- **Routing:** React Router DOM v6+.
- **HTTP Client:** Axios or TanStack Query.

### Infrastructure & DevOps
- **Containerization:** Docker & Docker Compose for local development.
- **Deployment Target:** Conceptualize for cloud (AWS/Heroku/DigitalOcean) but keep initial deployment agnostic.
- **Security Headers:** Implement CSP, Helmet-equivalent middleware on FastAPI.

---

## 3. Functional Requirements (MVP Scope)

### A. User Interface
1.  **Dashboard:** Display available exercises categorized by topic (e.g., "Loops", "Data Structures").
2.  **Exercise Detail Page:** 
    - Problem description.
    - Input/Output examples.
    - Hint system (collapsible).
3.  **Code Editor:** Integrated Monaco editor with line numbers, auto-indentation, and syntax highlighting for Python.
4.  **Terminal/Output:** A read-only terminal pane to display stdout/stderr from code execution.
5.  **Submission Form:** "Run" button that sends code to the backend for evaluation.

### B. Backend API
1.  **Authentication:** JWT-based auth (register/login) to track user progress.
2.  **Exercise Management:** CRUD endpoints to manage exercise content and test cases.
3.  **Evaluation Endpoint:** `POST /api/submit` 
    - Receives: Exercise ID + User Code.
    - Executes: Code in isolated sandbox.
    - Returns: Score, Output, Errors, Time Taken.
4.  **Progress Tracking:** Store user submissions and scores per exercise.

### C. Data Model (Core Entities)
- `User`: id, username, email, total_score, streak.
- `Exercise`: id, title, description, difficulty_level, category_id.
- `Solution`: id, user_id, exercise_id, status (completed/pending), timestamp.
- `TestCase`: id, input_data, expected_output, score_weight.

---

## 4. Constraints & Guidelines

### Security (Critical)
- **Sandboxing:** User-submitted Python code **MUST NOT** have access to the host filesystem or network. You must implement a timeout mechanism (e.g., `signal.timeout` or container kill switch).
- **Input Validation:** All API inputs must be sanitized. SQL Injection is forbidden.
- **Rate Limiting:** Implement rate limiting on submission endpoints to prevent DoS attacks via code execution loops.

### Code Quality
- **Type Safety:** Enforce strict typing in TypeScript and Pydantic models.
- **Logging:** Use `logging` module with structured JSON logs for debugging (but do not log sensitive user data).
- **Error Handling:** Return standardized error responses (`HTTPException` in FastAPI) with descriptive messages, not stack traces to the client.

### UX/UI
- **Responsiveness:** Mobile-first design using Tailwind breakpoints.
- **Feedback:** Visual cues for success (green glow), errors (red shake), and loading states.
- **Accessibility:** Ensure sufficient color contrast and keyboard navigability (WCAG 2.1 AA).

---

## 5. Initial Tasks & Action Plan

**Task 1: Project Initialization**
- Initialize the monorepo structure (e.g., `client/` and `server/`).
- Set up `pyproject.toml` for Python dependencies.
- Set up `package.json` with Vite, React, and Tailwind.
- Create a `.docker-compose.yml` file to spin up Postgres and the API service locally.

**Task 2: Database Schema Definition**
- Write SQLAlchemy models for `User`, `Exercise`, and `Submission`.
- Create Alembic migration scripts for the initial schema.

**Task 3: Backend Core Development**
- Set up FastAPI app structure (routers, dependencies).
- Implement Authentication endpoints (`/register`, `/login`).
- Build the Evaluation Endpoint with a mock execution logic first, then prepare for sandbox integration.

**Task 4: Frontend Shell**
- Configure Vite and React router.
- Create the main layout with Navbar and Footer.
- Scaffold the `ExerciseDetail` component with Monaco Editor placeholder.

---

## 6. Output Guidelines

When generating code or solutions, you must:
1.  **Explain your logic:** Briefly describe *why* you chose a specific architecture or library.
2.  **Use Comments:** Add docstrings for Python functions and JSDoc comments for React components.
3.  **Security Checks:** Before writing execution logic, explicitly mention the security measures taken (e.g., "I am using a subprocess with timeout").
4.  **File Paths:** Provide clear file paths (e.g., `server/app/routes/submit.py`).

**Immediate Question for You:**  
Before we begin coding Task 1, please confirm that you understand the sandboxing requirement for Python execution and outline your strategy for implementing it securely without requiring complex infrastructure setup immediately.
````

## File: docs/implementation_plan.md
````markdown
# Code-Thrasher Implementation Plan

**Project:** Code-Thrasher  
**Role:** Senior Software Engineer  
**Goal:** Build a Minimum Viable Product (MVP) for a bite-sized Python coding exercise platform.  
**Timeline Estimate:** 10-12 Weeks  
**Tech Stack:** React (Next.js), FastAPI, PostgreSQL, Docker, Monaco Editor.

---

## 1. Executive Summary
Code-Thrasher is a web-based platform designed to help beginners learn Python through gamified, bite-sized coding challenges. The MVP must prioritize security (sandboxed code execution), user engagement (progress tracking), and developer experience (code editor). This plan outlines the build phases, technical architecture, and resource requirements to launch a functional MVP within 3 months.

---

## 2. Technical Architecture Overview
*   **Frontend:** Next.js 14+ (React) with TypeScript for type safety. Uses Monaco Editor (VS Code engine) for the IDE experience.
*   **Backend:** FastAPI (Python) for high-performance async API handling.
*   **Database:** PostgreSQL (managed via Supabase or self-hosted AWS RDS) for user data and progress tracking.
*   **Code Execution:** Secure Dockerized Python sandboxes. We will spin up ephemeral containers for each submission to prevent Remote Code Execution (RCE).
*   **Authentication:** FastAPI Security with JWT tokens + NextAuth adapter.
*   **Infrastructure:** AWS or DigitalOcean (Container Registry + ECS/Kubernetes-lite).

---

## 3. Phased Implementation Plan

### Phase 1: Project Setup & Core Architecture (Weeks 1-2)
**Goal:** Establish the development environment, database schema, and security baseline.

*   **Tasks:**
    *   Initialize Git repository and GitHub Actions CI/CD pipelines.
    *   Set up FastAPI backend structure (Routers, Pydantic models).
    *   Design PostgreSQL schema: `Users`, `Exercises`, `Submissions`, `TestCases`.
    *   Implement Authentication: User Registration/Login, JWT issuance.
    *   **Security First:** Design the Sandbox Execution architecture. Define timeout limits and memory caps for running user code.
*   **Deliverable:** A "Hello World" API endpoint where a logged-in user can view their profile.

### Phase 2: Backend Logic & Data Management (Weeks 3-5)
**Goal:** Manage content (exercises) and handle the core submission workflow.

*   **Tasks:**
    *   Create Admin Dashboard endpoints for adding/editing exercises (JSON-based exercise definitions).
    *   Implement `Exercise` API: Fetch list, fetch details, verify user eligibility.
    *   Develop `Submission` API: Receive code snippet, validate syntax, queue execution.
    *   **Test Suite Logic:** Backend logic to compare user output against expected test cases (assertions).
    *   Handle Execution Failures: Graceful handling of crashes, timeouts, and memory errors without leaking data.
*   **Deliverable:** A backend that accepts code, runs it in a sandbox, returns Pass/Fail status with error logs.

### Phase 3: Frontend Development & UI (Weeks 6-9)
**Goal:** Build the user interface for solving problems and viewing progress.

*   **Tasks:**
    *   **Project Shell:** Setup Next.js with Tailwind CSS for styling.
    *   **Dashboard:** User profile view, progress bars, completed challenges list.
    *   **Editor Component:** Integrate Monaco Editor with custom themes (Dark Mode). Configure linting and auto-completion.
    *   **Submission Flow:** "Run" button triggering API call, loading state handling, result display (Success/Fail/Error).
    *   **Feedback View:** Display test case output (e.g., "Expected 5, got 3").
*   **Deliverable:** A functional web app where a user can see an exercise, write code, click run, and see results.

### Phase 4: Execution Security & Optimization (Week 10)
**Goal:** Harden the system against abuse and improve performance.

*   **Tasks:**
    *   Implement strict input sanitization on the client side to prevent injection.
    *   Optimize Docker sandbox spin-up time (use pre-baked container images).
    *   Add rate limiting to API endpoints to prevent DoS attacks via code execution requests.
    *   Implement a "Retry" mechanism for flaky test cases.
*   **Deliverable:** A secure system that can handle concurrent users without crashing or exposing the backend.

### Phase 5: Deployment & MVP Launch (Weeks 11-12)
**Goal:** Deploy to production and gather initial feedback.

*   **Tasks:**
    *   Configure CI/CD for automated testing before deployment.
    *   Setup Logging/Monitoring (Sentry for errors, Datadog/New Relic for metrics).
    *   Perform Load Testing (simulate 100 concurrent submissions).
    *   Write Documentation: User Guide, Developer Guide, Admin Guide.
    *   Soft Launch to a closed beta group for bug fixes.
*   **Deliverable:** `codethrasher.com` live with public access.

---

## 4. Key Milestones & Acceptance Criteria

| Milestone | Description | Success Criteria |
| :--- | :--- | :--- |
| **M1: Foundation** | Repo, DB, Auth, Editor setup | User can login and see a placeholder UI. |
| **M2: Backend Core** | Exercise data & Submission API | API accepts code, returns JSON with pass/fail status. |
| **M3: Frontend Integration** | Monaco Editor connected to API | Editor highlights syntax; results render correctly. |
| **M4: Security Audit** | Sandbox isolation verified | No user code executes on the main server process. |
| **M5: MVP Launch** | Public Access & Monitoring | System stable under load; error reporting active. |

---

## 5. Required Resources

### A. Human Resources (Internal Team)
*   **1 Backend Engineer:** Focus on FastAPI, DB Schema, and Sandbox Security.
*   **1 Frontend Engineer:** Focus on Next.js, State Management, UI/UX.
*   **1 DevOps/SRE:** Responsible for Docker orchestration, CI/CD, and Serverless infrastructure (initially can be handled by the Backend Lead).

### B. Infrastructure & Tools
*   **Cloud Provider:** AWS (EC2/ECS) or DigitalOcean App Platform.
*   **Container Registry:** Docker Hub or GitHub Container Registry.
*   **Database:** PostgreSQL (Managed Service).
*   **Monitoring:** Sentry (Error Tracking), Prometheus/Grafana (Metrics).
*   **Testing:** Pytest (Python), Jest (JS/TS), Playwright (E2E Testing).

### C. Content Requirements (Pre-MVP)
*   **Exercise Database:** At least 50 Python exercises (Basic to Intermediate) with JSON definitions including:
    *   Problem Statement.
    *   Input/Output examples.
    *   Test Cases logic.
    *   Difficulty Level (Easy/Medium/Hard).

---

## 6. Critical Risk Mitigation Strategy

| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| **Code Execution Attack** | High | **Mandatory:** All user code runs in isolated Docker containers with network isolation and strict CPU/Memory limits (cgroups). Never execute in the main process. |
| **Slow Sandbox Spin-up** | Medium | Use pre-built base images; utilize a task queue (Celery/Redis) to handle execution asynchronously so the UI doesn't hang. |
| **Database Bloat** | Medium | Implement database migrations and archive old `Submission` logs quarterly. |
| **Content Maintenance** | Medium | Create an Admin API or Dashboard for adding new exercises easily without code deployment. |

---

## 7. Senior Engineer Notes (Implementation Tips)

1.  **Sandboxing is Non-Negotiable:** Do not use `subprocess.call` to run Python directly from the main web process. Use a Docker container per request or a dedicated worker pool with strict resource limits (`ulimit`).
2.  **Async/Concurrency:** Code execution takes time. The API should return immediately (HTTP 200) with a job ID, then poll for results using WebSockets or SSE (Server-Sent Events), OR use Celery to push the result back via WebSocket. Do not block the main thread waiting for code to compile/run.
3.  **Monaco Configuration:** Configure Monaco Editor to disable certain APIs if you want to prevent users from trying to upload files or access external libraries (unless they are pre-approved).
4.  **Error Handling:** If a user's code throws a syntax error, your UI must display the *first line* of the traceback clearly, not a generic "500 Error". Use `try/except` blocks in your execution wrapper to catch exceptions before returning them to the frontend.

---

**Next Step:** Initialize the Git repository and create the `docker-compose.yml` for local development (Backend + DB) to begin Phase 1 tasks immediately.
````

## File: docs/spec.md
````markdown
# Project Specification Document: Code-Thrasher

| **Project Name** | Code-Thrasher |
| :--- | :--- |
| **Version** | 1.0 |
| **Status** | Draft |
| **Complexity Level** | Medium |
| **Primary Tech Stack** | Python (FastAPI), React, PostgreSQL, Redis |

---

## 1. Overview
Code-Thrasher is a web-based interactive platform designed to accelerate Python proficiency through bite-sized, gamified coding challenges. Unlike traditional long-form tutorials or competitive algorithm platforms that require deep dives into complex systems design, Code-Thrasher focuses on high-frequency, low-time-commitment exercises (5-15 minutes). The platform bridges the gap between "learning theory" and "practical application" by providing immediate feedback loops and a streamlined interface for writing and testing Python code within a secure sandbox environment.

## 2. Problem Statement
*   **Engagement Friction:** Beginners often lose momentum after starting a course because the tasks are too large or the feedback is delayed (e.g., "Submit Assignment" after a week of videos).
*   **Feedback Void:** Traditional IDEs require complex setups. Online platforms often lack immediate validation for syntax and logic errors without deep integration.
*   **Boredom/Drudgery:** Standard coding exercises can feel like homework. The platform needs to make Python feel accessible, engaging, and "thrilling" (hence the name).
*   **Security of Execution:** Running user-submitted code on a shared web server is a significant security risk. A robust sandboxing strategy is required.

## 3. Goals
1.  **Educational Efficiency:** Deliver core Python concepts (syntax, loops, functions, basic OOP) through practical snippets within 10 minutes per session.
2.  **Immediate Feedback:** Provide instant validation on code correctness and performance, reducing the "wait time" for results.
3.  **Accessibility:** Offer a browser-based code editor that requires zero local installation (Python runtime handled by the backend or WebAssembly).
4.  **Gamification of Learning:** Utilize streaks, points, and levels to maintain user retention and motivation.
5.  **Scalability:** Architect the system to handle concurrent code execution requests without compromising server security.

## 4. Target Users
*   **Absolute Beginners:** Self-taught individuals looking for a low-barrier entry into Python.
*   **Career Switchers:** Professionals needing upskilling in data science or automation who want quick wins.
*   **Intermediate Learners:** Users looking to reinforce syntax knowledge without revisiting heavy textbooks.
*   **Exclusion:** Advanced algorithm experts (Code-Thrasher is not for LeetCode-level Hard problems initially) or users requiring complex local IDE configurations.

## 5. Core Features
1.  **Interactive Code Editor:** A Monaco-based editor with Python syntax highlighting, line numbers, and real-time linting hints.
2.  **Sandboxed Execution Engine:** Securely runs user code in isolated containers to prevent server compromise and resource exhaustion.
3.  **Problem Feed:** Curated list of "Bite-Sized" challenges categorized by concept (e.g., "Variables," "Loops," "List Comprehension").
4.  **Instant Validation:** Automated checks for syntax errors, expected output matching, and runtime exceptions.
5.  **User Dashboard:** Tracks progress, completed badges, streaks, and XP score.
6.  **Hint System:** Contextual hints revealed upon request to prevent total blocking by a user.

## 6. Non-Goals (Out of Scope for MVP/Phase 1)
*   **Video Content:** Text-based explanations only; video integration is too heavy for the initial scope.
*   **Real-time Collaboration:** No multiplayer coding rooms or pair programming features.
*   **Complex Data Structures:** Initial focus is on standard library Python, not advanced NumPy/Pandas libraries (to reduce sandbox complexity).
*   **Mobile Native App:** Web-first approach; mobile responsiveness is required, but PWA is the target over native iOS/Android apps.
*   **Advanced Authentication:** Basic OAuth (Google/GitHub) is preferred over complex enterprise SSO for MVP.

## 7. MVP Scope
The Minimum Viable Product will focus on the core loop: *View Challenge -> Write Code -> Run -> Review*.

**Functional Requirements:**
1.  **User Auth:** Sign up/Login via Email or OAuth (Google).
2.  **Challenge Management:** CRUD for problems (Title, Description, Test Cases, Expected Output).
3.  **Code Submission:** User inputs Python code; backend executes it against hidden test cases.
4.  **Result Display:** Pass/Fail status with error messages and execution time.
5.  **Progress Tracking:** Simple "Problem Completed" counter per user.

**Technical Constraints for MVP:**
*   Execution timeout: Max 30 seconds per request.
*   Memory limit: 256MB per container.
*   Database: Single PostgreSQL instance with Redis for task queueing.

## 8. Data Model (Schema)

### Core Entities

| Entity | Attributes | Description |
| :--- | :--- | :--- |
| **User** | `id`, `username`, `email`, `xp_score`, `streak`, `last_login` | User profile and gamification stats. |
| **Problem** | `id`, `title`, `description`, `difficulty`, `category`, `tags` | Challenge metadata. |
| **TestCase** | `id`, `problem_id`, `input_str`, `expected_output` | Test cases attached to a problem. |
| **Submission** | `id`, `user_id`, `problem_id`, `code_hash`, `status`, `duration_ms`, `created_at` | Record of code run and result. |
| **Badge** | `id`, `name`, `criteria_type`, `target_value` | Gamification milestones (e.g., "First Solve"). |

**Relationships:**
*   User : Submissions (1:N)
*   Problem : TestCases (1:N)
*   Submission : Status (Enum: `SUCCESS`, `ERROR`, `TIMEOUT`)

## 9. API Plan (RESTful with Async Support)

The backend will expose a clean REST API. All responses are JSON.

### Base URL
`/api/v1/`

### Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| **GET** | `/problems` | List all available challenges (paginated). | Optional |
| **GET** | `/problems/{id}` | Fetch specific problem details and test cases. | Optional |
| **POST** | `/submissions` | Submit code snippet for execution. Returns result. | Required |
| **GET** | `/user/profile` | Fetch user stats (XP, Streak, Level). | Required |
| **GET** | `/user/progress/{problem_id}` | Check completion status for a specific problem. | Required |

### Execution Endpoint Specification (`POST /submissions`)
*   **Request Body:** `{ "problem_id": int, "code": string }`
*   **Response 200 (Success):** `{"passed": true, "output": "...", "time_ms": 120}`
*   **Response 400 (Error):** `{"passed": false, "error": "SyntaxError: invalid syntax"}`
*   **Response 504 (Timeout):** Code execution exceeded server limit.

### Security Headers & Middleware
*   CORS enabled for React frontend domain.
*   Rate limiting on `/submissions` to prevent resource hogging.
*   Input sanitization on `code` field (prevent shell injection).

## 10. Architectural Decisions & Tech Stack

### Backend: Python (FastAPI)
*   **Reasoning:** FastAPI offers high performance for async tasks. It integrates natively with Python types, making it easier to type-hint the execution logic. It supports `asyncio` out of the box, which is critical for handling multiple concurrent code executions efficiently.

### Frontend: React (TypeScript + Vite)
*   **Reasoning:** Standard industry choice for web apps. TypeScript ensures type safety for the complex state required by the editor and form validation.

### Code Execution Strategy (Critical Risk Mitigation)
We will not run Python directly on the main application server threads to avoid blocking I/O.
*   **Queue System:** Requests are pushed to a Redis Queue.
*   **Workers:** A set of worker processes consume the queue, spin up isolated Docker containers for each execution, run the code, and return the result.
*   **Sandboxing:** Using `Docker` with resource limits (CPU/RAM) per container. If a user writes an infinite loop, it hits the timeout/container limit and is killed safely.

### Database: PostgreSQL + Redis
*   **PostgreSQL:** Relational integrity for users, problems, and submissions.
*   **Redis:** Caching problem metadata and managing the job queue (`Celery` or native `FastAPI Workers`).

## 11. Risks & Mitigation Strategies

| Risk | Impact | Probability | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Code Injection / Jailbreak** | High | Medium | Run all code in isolated Docker containers with restricted filesystem permissions (no access to host `/etc` or `socket`). Use a restricted Python environment (standard library only). |
| **Infinite Loops / CPU Hogging** | High | Medium | Implement hard timeouts (e.g., 10s) at the OS level. Monitor container resource usage and kill if >80% CPU for >5s. |
| **Slow Execution Latency** | Medium | High | Use Redis Queue to decouple request from execution. Only show "Running..." status immediately. Optimize test cases (limit count per problem). |
| **Content Maintenance** | Medium | Low | Build an Admin Panel (Django Admin or custom) for educators to upload new problems without touching the codebase. |
| **Browser Security (CSP)** | Low | High | Configure Content Security Policy headers strictly to prevent XSS, especially when executing scripts in the backend. |

## 12. Success Metrics (KPIs)
To validate the project post-launch:
1.  **Completion Rate:** % of users who finish a challenge after starting it (Target >60%).
2.  **Time-to-First-Solve:** Average time from registration to first successful submission (Target <15 mins).
3.  **Retention:** Weekly Active Users (WAU) / Monthly Active Users (MAU) ratio.
4.  **Error Rate:** Percentage of submissions failing due to server-side errors vs. user code errors.

---
**Approvals:**
*   *Lead Architect:* _____________________
*   *Product Owner:* _____________________
````

## File: server/alembic/versions/0001_initial_schema.py
````python
"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-01-01 00:00:00.000000

"""
⋮----
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
⋮----
def upgrade() -> None
⋮----
difficulty_enum = sa.Enum(
⋮----
status_enum = sa.Enum("pending", "completed", "failed", name="submissionstatus")
⋮----
def downgrade() -> None
````

## File: server/alembic/versions/0003_make_submission_user_id_nullable.py
````python
"""make_submission_user_id_nullable

Revision ID: 0003
Revises: 71d51bde7666
Create Date: 2026-05-20 00:00:00.000000

"""
⋮----
revision: str = '0003'
down_revision: Union[str, None] = '71d51bde7666'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
⋮----
def upgrade() -> None
⋮----
def downgrade() -> None
````

## File: server/alembic/versions/0004_add_exercise_guides.py
````python
"""add_exercise_guides

Revision ID: 0004
Revises: 0003
Create Date: 2026-06-04 22:38:00.000000

"""
⋮----
revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
⋮----
def upgrade() -> None
⋮----
def downgrade() -> None
````

## File: server/alembic/versions/71d51bde7666_add_missing_indexes.py
````python
"""add_missing_indexes

Revision ID: 71d51bde7666
Revises: 0001
Create Date: 2026-05-20 01:13:29.168538

"""
⋮----
revision: str = '71d51bde7666'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
⋮----
def upgrade() -> None
⋮----
# ### commands auto generated by Alembic - please adjust! ###
⋮----
# ### end Alembic commands ###
⋮----
def downgrade() -> None
````

## File: server/alembic/env.py
````python
# noqa: F401 — import models so metadata is populated
import app.models.models  # noqa: F401
⋮----
config = context.config
⋮----
target_metadata = Base.metadata
⋮----
def run_migrations_offline() -> None
⋮----
def do_run_migrations(connection):  # type: ignore[no-untyped-def]
⋮----
async def run_migrations_online() -> None
⋮----
connectable = async_engine_from_config(
````

## File: server/alembic/script.py.mako
````
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
````

## File: server/app/api/v1/endpoints/__init__.py
````python

````

## File: server/app/api/v1/endpoints/progress.py
````python
router = APIRouter(prefix="/progress", tags=["progress"])
⋮----
@router.get("/", response_model=ProgressResponse)
async def get_progress(db: AsyncSession = Depends(get_db)) -> ProgressResponse
⋮----
total: int = (
⋮----
rows = (
⋮----
exercises = {
````

## File: server/app/api/v1/__init__.py
````python

````

## File: server/app/api/__init__.py
````python

````

## File: server/app/core/__init__.py
````python

````

## File: server/app/core/config.py
````python
class Settings(BaseSettings)
⋮----
model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
⋮----
DATABASE_URL: str = "postgresql+asyncpg://codethrasher:codethrasher@localhost:5432/codethrasher"
SECRET_KEY: str = "change-me-in-production-use-a-long-random-string"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
⋮----
# Sandbox limits
SANDBOX_TIMEOUT_SECONDS: int = 5
SANDBOX_MAX_MEMORY_MB: int = 64
SANDBOX_MAX_OUTPUT_BYTES: int = 10_000
⋮----
settings = Settings()
````

## File: server/app/db/__init__.py
````python

````

## File: server/app/db/database.py
````python
engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
⋮----
class Base(DeclarativeBase)
⋮----
async def get_db() -> AsyncGenerator[AsyncSession, None]
````

## File: server/app/models/__init__.py
````python

````

## File: server/app/schemas/__init__.py
````python

````

## File: server/app/services/__init__.py
````python

````

## File: server/app/__init__.py
````python

````

## File: server/tests/__init__.py
````python

````

## File: server/tests/conftest.py
````python
TEST_DB_URL = "sqlite+aiosqlite:///./test.db"
⋮----
engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSession = async_sessionmaker(engine, expire_on_commit=False)
⋮----
async def override_get_db()
⋮----
@pytest_asyncio.fixture(autouse=True)
async def setup_db()
⋮----
@pytest_asyncio.fixture
async def client()
````

## File: server/tests/test_progress.py
````python
async def test_progress_empty(client: AsyncClient)
⋮----
r = await client.get("/api/v1/progress/")
⋮----
data = r.json()
⋮----
async def test_progress_after_solved_submission(client: AsyncClient)
⋮----
ex = (
ex_id = ex["id"]
⋮----
ex_progress = data["exercises"][str(ex_id)]
⋮----
async def test_progress_tracks_best_score(client: AsyncClient)
⋮----
ex_id = (
⋮----
# First attempt: 50%
⋮----
# Second attempt: also 50% (different test passing)
⋮----
async def test_progress_unsolved_does_not_count(client: AsyncClient)
⋮----
async def test_progress_total_exercises_count(client: AsyncClient)
````

## File: server/tests/test_submit.py
````python
@pytest.fixture
async def exercise_id(client: AsyncClient)
⋮----
r = await client.post(
⋮----
def _result(tc_id: int, passed: bool, weight: float = 1.0)
⋮----
async def test_submit_all_pass(client: AsyncClient, exercise_id: int)
⋮----
data = r.json()
⋮----
async def test_submit_partial_pass(client: AsyncClient, exercise_id: int)
⋮----
async def test_submit_all_fail(client: AsyncClient, exercise_id: int)
⋮----
async def test_submit_weighted_scoring(client: AsyncClient, exercise_id: int)
⋮----
# Two tests: first has weight 1, second has weight 3. Only first passes.
# Expected score: 1/4 * 100 = 25.0
⋮----
async def test_submit_exercise_not_found(client: AsyncClient)
⋮----
async def test_submit_empty_code_rejected(client: AsyncClient, exercise_id: int)
````

## File: server/alembic.ini
````ini
[alembic]
script_location = alembic
prepend_sys_path = .
sqlalchemy.url = postgresql+asyncpg://codethrasher:codethrasher@localhost:5432/codethrasher

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
````

## File: server/Dockerfile
````
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir uv && uv pip install --system -e ".[dev]"

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
````

## File: .env.example
````
POSTGRES_USER=codethrasher
POSTGRES_PASSWORD=codethrasher
POSTGRES_DB=codethrasher
SECRET_KEY=change-me-in-production-use-a-long-random-string
ACCESS_TOKEN_EXPIRE_MINUTES=60
````

## File: LICENSE
````
Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
````

## File: .claude/settings.local.json
````json
{
  "permissions": {
    "allow": [
      "Bash(Get-ChildItem -Recurse -Directory)",
      "Bash(Select-Object -ExpandProperty FullName)",
      "Bash(Head-20)",
      "Bash(Remove-Item \"d:\\\\Code\\\\Python\\\\PythonApps\\\\Code-Thrasher\\\\server\\\\app\\\\api\\\\v1\\\\endpoints\\\\auth.py\" -Force)",
      "Bash(Remove-Item \"d:\\\\Code\\\\Python\\\\PythonApps\\\\Code-Thrasher\\\\server\\\\app\\\\api\\\\dependencies.py\" -Force)",
      "Bash(Remove-Item \"d:\\\\Code\\\\Python\\\\PythonApps\\\\Code-Thrasher\\\\server\\\\app\\\\core\\\\security.py\" -Force)",
      "Bash(Remove-Item \"d:\\\\Code\\\\Python\\\\PythonApps\\\\Code-Thrasher\\\\client\\\\src\\\\store\\\\useAuthStore.ts\" -Force)",
      "Bash(Remove-Item \"d:\\\\Code\\\\Python\\\\PythonApps\\\\Code-Thrasher\\\\client\\\\src\\\\pages\\\\Login.tsx\" -Force)",
      "Bash(docker compose *)"
    ]
  },
  "enabledMcpjsonServers": [
    "python-sdk",
    "docker",
    "postgresql",
    "memory-bank",
    "sequential-thinking"
  ],
  "disabledMcpjsonServers": [
    "jupyter",
    "opik",
    "brave-search",
    "google-maps",
    "deep-graph"
  ]
}
````

## File: client/src/api/client.ts
````typescript
import axios from "axios";
````

## File: client/src/components/layout/Navbar.tsx
````typescript
import { Link } from "react-router-dom";
⋮----
export default function Navbar()
````

## File: client/src/pages/Dashboard.tsx
````typescript
import { useEffect } from "react";
import { Link } from "react-router-dom";
import api from "@/api/client";
import { useProgressStore } from "@/store/useProgressStore";
import type { ExerciseListItem, DifficultyLevel } from "@/types";
import { useState } from "react";
⋮----
fetchProgress().catch(() => {/* progress is non-critical */});
````

## File: client/src/App.tsx
````typescript
import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import Dashboard from "@/pages/Dashboard";
import ExerciseDetail from "@/pages/ExerciseDetail";
⋮----
export default function App()
````

## File: client/package.json
````json
{
  "name": "code-thrasher-client",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@monaco-editor/react": "^4.7.0",
    "axios": "^1.17.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.30.4",
    "zustand": "^4.5.7"
  },
  "devDependencies": {
    "@types/react": "^18.3.30",
    "@types/react-dom": "^18.3.7",
    "@typescript-eslint/eslint-plugin": "^7.18.0",
    "@typescript-eslint/parser": "^7.18.0",
    "@vitejs/plugin-react": "^4.7.0",
    "autoprefixer": "^10.5.0",
    "eslint": "^8.57.1",
    "eslint-plugin-react-hooks": "^4.6.2",
    "eslint-plugin-react-refresh": "^0.4.26",
    "postcss": "^8.5.15",
    "tailwindcss": "^3.4.19",
    "typescript": "^5.9.3",
    "vite": "^5.4.21"
  }
}
````

## File: client/vite.config.ts
````typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
````

## File: server/app/api/v1/endpoints/exercises.py
````python
router = APIRouter(prefix="/exercises", tags=["exercises"])
⋮----
stmt = select(Exercise).options(selectinload(Exercise.category))
⋮----
stmt = stmt.where(Exercise.difficulty_level == difficulty)
⋮----
stmt = stmt.where(Exercise.category_id == category_id)
result = await db.execute(stmt)
⋮----
@router.get("/{exercise_id}", response_model=ExerciseDetail)
async def get_exercise(exercise_id: int, db: AsyncSession = Depends(get_db)) -> Exercise
⋮----
result = await db.execute(
exercise = result.scalar_one_or_none()
⋮----
result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
⋮----
exercise = Exercise(**payload.model_dump())
⋮----
# reload with relationships
````

## File: server/tests/test_exercises.py
````python
@pytest.fixture
def new_exercise()
⋮----
async def test_list_exercises_empty(client: AsyncClient)
⋮----
r = await client.get("/api/v1/exercises/")
⋮----
async def test_create_exercise(client: AsyncClient, new_exercise)
⋮----
r = await client.post("/api/v1/exercises/", json=new_exercise)
⋮----
data = r.json()
⋮----
async def test_list_exercises_after_create(client: AsyncClient, new_exercise)
⋮----
async def test_get_exercise_by_id(client: AsyncClient, new_exercise)
⋮----
created = (await client.post("/api/v1/exercises/", json=new_exercise)).json()
ex_id = created["id"]
⋮----
r = await client.get(f"/api/v1/exercises/{ex_id}")
⋮----
async def test_get_exercise_solution_requires_reveal(client: AsyncClient, new_exercise)
⋮----
guide = [
created = (
⋮----
detail = await client.get(f"/api/v1/exercises/{created['id']}")
⋮----
detail_data = detail.json()
⋮----
solution = await client.get(f"/api/v1/exercises/{created['id']}/solution")
⋮----
async def test_get_exercise_solution_not_available(client: AsyncClient, new_exercise)
⋮----
r = await client.get(f"/api/v1/exercises/{created['id']}/solution")
⋮----
async def test_get_exercise_not_found(client: AsyncClient)
⋮----
r = await client.get("/api/v1/exercises/999")
⋮----
async def test_list_exercises_filter_by_difficulty(client: AsyncClient, new_exercise)
⋮----
r = await client.get("/api/v1/exercises/?difficulty=beginner")
⋮----
results = r.json()
````

## File: server/pyproject.toml
````toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "code-thrasher-api"
version = "0.1.0"
description = "Code-Thrasher backend API"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "sqlalchemy[asyncio]>=2.0.0",
    "alembic>=1.13.0",
    "asyncpg>=0.29.0",
    "pydantic[email]>=2.7.0",
    "pydantic-settings>=2.3.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.9",
    "slowapi>=0.1.9",
    "structlog>=24.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=5.0.0",
    "httpx>=0.27.0",
    "black>=24.0.0",
    "isort>=5.13.0",
    "mypy>=1.10.0",
    "flake8>=7.0.0",
]

[tool.hatch.build.targets.wheel]
packages = ["app"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "--cov=app --cov-report=term-missing"

[tool.black]
line-length = 88

[tool.isort]
profile = "black"

[tool.mypy]
strict = true
ignore_missing_imports = true

[dependency-groups]
dev = [
    "aiosqlite>=0.22.1",
    "httpx>=0.28.1",
    "pytest-asyncio>=1.3.0",
    "pytest-cov>=7.1.0",
]
````

## File: CLAUDE.md
````markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Code-Thrasher is a Python learning platform where users solve bite-sized coding challenges in a Monaco editor. Code execution happens **client-side in the browser via Pyodide** (WebAssembly Python), not server-side — the backend only records submission results that the client reports.

## Development Commands

### Backend (`server/`)

```bash
cd server

# Install all dependencies (including dev)
uv pip install -e ".[dev]"

# Start DB only (then run API locally)
docker compose -f ../docker-compose.yml up db -d

# Run API with live reload
uvicorn app.main:app --reload

# Apply migrations
alembic upgrade head

# Create a new migration after changing models
alembic revision --autogenerate -m "describe change"

# Seed exercises
python seed.py
```

Tests use an in-memory SQLite database (`aiosqlite`) — no running Postgres needed:

```bash
pytest              # all tests
pytest -v -x        # verbose, stop on first failure
pytest -k "test_name"
uv run pytest       # use if pytest is not on PATH; uv creates/uses server/.venv
```

### Frontend (`client/`)

```bash
cd client
npm install
npm run dev         # Vite dev server at http://localhost:5173
npm run typecheck   # tsc --noEmit
npm run lint        # ESLint
npm run build       # type-check + Vite production build
```

### Full Stack (Docker)

```bash
docker compose up --build
# First run: docker compose exec api alembic upgrade head
```

## Architecture

### Code Execution Flow

The key non-obvious design: **user code runs in the browser**, not the server.

1. `client/src/services/pyodide.ts` — lazy-loads Pyodide (~10 MB) from CDN, runs Python in a fresh namespace via `exec()`, captures stdout/stderr
2. `ExerciseDetail.tsx` — runs each test case through Pyodide, compares output to `expected_output`, builds `TestCaseResult[]`
3. The frontend calls `POST /api/v1/submit/` with the pre-evaluated results (scores already computed)
4. `server/app/api/v1/endpoints/submit.py` — trusts the client's `test_results`, calculates final score, persists `Submission`

This means the server-side `SANDBOX_*` config settings in `app/core/config.py` are currently unused — there is no server-side execution.

### Backend Structure

- `app/main.py` — FastAPI app, CORS (localhost:5173 only), rate limiting via slowapi, security headers
- `app/core/config.py` — `Settings` loaded from `.env` via pydantic-settings
- `app/db/database.py` — async SQLAlchemy engine + `get_db` dependency
- `app/models/models.py` — ORM models: `User`, `Category`, `Exercise`, `TestCase`, `Submission`
- `app/schemas/schemas.py` — Pydantic v2 request/response schemas
- `app/api/v1/endpoints/` — three routers: `exercises`, `submit`, `progress`
- `app/api/v1/endpoints/exercises.py` — exercise list/detail plus explicit `GET /exercises/{id}/solution`; default detail responses include `guide` + `has_solution`, never solution text
- `alembic/` — migration history; `alembic.ini` points to `server/` as base dir

There is no auth middleware wired into endpoints yet — `user_id` on `Submission` is nullable and the submit endpoint does not require a JWT.

### Frontend Structure

- `src/App.tsx` — two routes: `/` (Dashboard) and `/exercise/:id` (ExerciseDetail)
- `src/api/client.ts` — Axios instance with `baseURL: "/api/v1"` (proxied by Vite)
- `src/store/useProgressStore.ts` — Zustand store, fetches `GET /progress/` to track completion
- `src/services/pyodide.ts` — singleton Pyodide loader; first call downloads ~10 MB
- `src/components/editor/CodeEditor.tsx` — Monaco Editor wrapper
- `src/components/exercise/ExerciseGuidePanel.tsx` — progressive guide cards, snippets, and deliberate solution reveal without overwriting editor code

### Data Model

`Exercise` has many `TestCase`s. Each `TestCase` has `input_data`, `expected_output`, `score_weight`, and `is_hidden`. Submissions store the final `score` (0–100) and `status` (`completed` = 100, `failed` = anything less).

`Exercise` keeps legacy `hint`, plus structured `guide` JSON and optional `solution_code` / `solution_explanation`; expose answers only through the solution reveal endpoint.

## Key Constraints

- **Vite proxy**: The `vite.config.ts` proxies `/api` to `http://localhost:8000`. The CORS allow-list in `app/main.py` is hardcoded to `http://localhost:5173`.
- **Test isolation**: `server/tests/conftest.py` overrides `get_db` with an async SQLite session; every test gets a fresh schema via `autouse` fixture.
- **`asyncio_mode = "auto"`** is set in `pyproject.toml` — all test functions can be `async def` without decorators.
- **Guidance reveal**: solution reveal is currently anonymous because auth is not wired into exercise endpoints; future per-user reveal tracking should wait for auth.
- **Frontend validation**: `npm run lint` requires `client/.eslintrc.cjs`; `npm run build` may emit TypeScript build artifacts if not ignored/cleaned.
````

## File: docker-compose.yml
````yaml
services:
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-codethrasher}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-codethrasher}
      POSTGRES_DB: ${POSTGRES_DB:-codethrasher}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-codethrasher}"]
      interval: 5s
      timeout: 5s
      retries: 5

  api:
    build:
      context: ./server
      dockerfile: Dockerfile
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER:-codethrasher}:${POSTGRES_PASSWORD:-codethrasher}@db:5432/${POSTGRES_DB:-codethrasher}
      SECRET_KEY: ${SECRET_KEY:-change-me-in-production-use-a-long-random-string}
      ALGORITHM: HS256
      ACCESS_TOKEN_EXPIRE_MINUTES: 60
    ports:
      - "8000:8000"
    volumes:
      - ./server:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:
````

## File: server/app/api/v1/endpoints/submit.py
````python
router = APIRouter(prefix="/submit", tags=["submit"])
⋮----
exercise = await db.get(Exercise, payload.exercise_id)
⋮----
total_weight = sum(r.score_weight for r in payload.test_results)
earned_weight = sum(r.score_weight for r in payload.test_results if r.passed)
score = round((earned_weight / total_weight) * 100, 2) if total_weight else 0.0
sub_status = SubmissionStatus.completed if score == 100.0 else SubmissionStatus.failed
⋮----
submission = Submission(
````

## File: server/app/models/models.py
````python
class DifficultyLevel(str, enum.Enum)
⋮----
beginner = "beginner"
intermediate = "intermediate"
advanced = "advanced"
⋮----
class SubmissionStatus(str, enum.Enum)
⋮----
pending = "pending"
completed = "completed"
failed = "failed"
⋮----
class User(Base)
⋮----
__tablename__ = "users"
⋮----
id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
total_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
created_at: Mapped[datetime] = mapped_column(
updated_at: Mapped[datetime] = mapped_column(
⋮----
submissions: Mapped[list["Submission"]] = relationship(back_populates="user")
⋮----
class Category(Base)
⋮----
__tablename__ = "categories"
⋮----
name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
⋮----
exercises: Mapped[list["Exercise"]] = relationship(back_populates="category")
⋮----
class Exercise(Base)
⋮----
__tablename__ = "exercises"
⋮----
title: Mapped[str] = mapped_column(String(200), nullable=False)
description: Mapped[str] = mapped_column(Text, nullable=False)
hint: Mapped[str | None] = mapped_column(Text)
guide: Mapped[list[dict[str, str]]] = mapped_column(JSON, default=list, nullable=False)
difficulty_level: Mapped[DifficultyLevel] = mapped_column(
category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), index=True)
starter_code: Mapped[str] = mapped_column(Text, default="")
solution_code: Mapped[str | None] = mapped_column(Text)
solution_explanation: Mapped[str | None] = mapped_column(Text)
⋮----
category: Mapped["Category | None"] = relationship(back_populates="exercises")
test_cases: Mapped[list["TestCase"]] = relationship(back_populates="exercise")
submissions: Mapped[list["Submission"]] = relationship(back_populates="exercise")
⋮----
@property
    def has_solution(self) -> bool
⋮----
class TestCase(Base)
⋮----
__tablename__ = "test_cases"
⋮----
exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"), nullable=False, index=True)
input_data: Mapped[str] = mapped_column(Text, default="")
expected_output: Mapped[str] = mapped_column(Text, nullable=False)
score_weight: Mapped[float] = mapped_column(Float, default=1.0)
is_hidden: Mapped[bool] = mapped_column(default=False)
⋮----
exercise: Mapped["Exercise"] = relationship(back_populates="test_cases")
⋮----
class Submission(Base)
⋮----
__tablename__ = "submissions"
__table_args__ = (
⋮----
# Covers "all submissions for a user" and "user's attempt on a specific exercise"
⋮----
user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"), nullable=False)
code: Mapped[str] = mapped_column(Text, nullable=False)
status: Mapped[SubmissionStatus] = mapped_column(
score: Mapped[float] = mapped_column(Float, default=0.0)
stdout: Mapped[str] = mapped_column(Text, default="")
stderr: Mapped[str] = mapped_column(Text, default="")
time_taken_ms: Mapped[int] = mapped_column(Integer, default=0)
⋮----
user: Mapped["User"] = relationship(back_populates="submissions")
exercise: Mapped["Exercise"] = relationship(back_populates="submissions")
````

## File: server/app/main.py
````python
limiter = Limiter(key_func=get_remote_address)
⋮----
app = FastAPI(
⋮----
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]
⋮----
allow_origins=["http://localhost:5173"],  # Vite dev server
⋮----
@app.middleware("http")
async def security_headers(request: Request, call_next):  # type: ignore[no-untyped-def]
⋮----
response = await call_next(request)
⋮----
@app.get("/api/health")
async def health() -> dict[str, str]
````

## File: .gitignore
````
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[codz]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#   Usually these files are written by a python script from a template
#   before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py.cover
.hypothesis/
.pytest_cache/
cover/
*.db
*.db-journal

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
# Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
 uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
# poetry.lock
# poetry.toml

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#   pdm recommends including project-wide configuration in pdm.toml, but excluding .pdm-python.
#   https://pdm-project.org/en/latest/usage/project/#working-with-version-control
# pdm.lock
# pdm.toml
.pdm-python
.pdm-build/

# pixi
#   Similar to Pipfile.lock, it is generally recommended to include pixi.lock in version control.
# pixi.lock
#   Pixi creates a virtual environment in the .pixi directory, just like venv module creates one
#   in the .venv directory. It is recommended not to include this directory in version control.
.pixi

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# Redis
*.rdb
*.aof
*.pid

# RabbitMQ
mnesia/
rabbitmq/
rabbitmq-data/

# ActiveMQ
activemq-data/

# SageMath parsed files
*.sage.py

# Environments
.env
.envrc
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#   JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#   be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#   and can be added to the global gitignore or merged into this file.  For a more nuclear
#   option (not recommended) you can uncomment the following to ignore the entire idea folder.
# .idea/

# Abstra
#   Abstra is an AI-powered process automation framework.
#   Ignore directories containing user credentials, local state, and settings.
#   Learn more at https://abstra.io/docs
.abstra/

# Visual Studio Code
#   Visual Studio Code specific template is maintained in a separate VisualStudioCode.gitignore 
#   that can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
#   and can be added to the global gitignore or merged into this file. However, if you prefer, 
#   you could uncomment the following to ignore the entire vscode folder
# .vscode/
# Temporary file for partial code execution
tempCodeRunnerFile.py

# Ruff stuff:
.ruff_cache/

# PyPI configuration file
.pypirc

# Marimo
marimo/_static/
marimo/_lsp/
__marimo__/

# Streamlit
.streamlit/secrets.toml

/client/node_modules/*
/client/.vite/*
/client/.vite/*
````

## File: README.md
````markdown
# Code-Thrasher

Code-Thrasher is a web-based platform designed to help beginners learn Python through gamified, bite-sized coding challenges.

Users register, browse exercises filtered by difficulty or category, write Python solutions in an in-browser Monaco editor, and submit them for instant automated feedback. Correct submissions earn points, building a running score and daily streak that motivate continued practice.

---

![Screenshot of code-thrasher](docs/code-thrasher-scrnsht.png)

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, Monaco Editor, Zustand |
| Backend | FastAPI (Python 3.12), SQLAlchemy 2 (async), Alembic, Pydantic v2 |
| Database | PostgreSQL 16 |
| Auth | JWT (python-jose + passlib/bcrypt) |
| Code execution | Sandboxed subprocess with AST pre-scan and resource limits |
| Containerisation | Docker + Docker Compose |

---

## Features

- **User accounts** — register, log in, and track personal score and streak
- **Exercise library** — filterable by difficulty (`beginner`, `intermediate`, `advanced`) and category
- **In-browser code editor** — Monaco Editor with Python syntax highlighting and starter code
- **In-browser Python execution** — user code runs client-side in Pyodide; the backend records reported submission results
- **Progressive challenge guidance** — each exercise can provide staged guide cards, small snippets, and an explicit full-solution reveal
- **Automated test cases** — submissions are scored against hidden and visible test cases; partial credit is supported via per-case score weights
- **Interactive dashboard** — lists all exercises with completion status and score breakdown
- **Rate limiting** — API endpoints are protected with slowapi to prevent abuse
- **Interactive API docs** — Swagger UI at `/api/docs`, ReDoc at `/api/redoc`

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Node.js](https://nodejs.org/) 20+ and npm (for local frontend development)
- [Python](https://www.python.org/) 3.12+ and [uv](https://github.com/astral-sh/uv) (for local backend development)

---

## Quick Start (Docker)

The fastest way to run the full stack is with Docker Compose, which starts PostgreSQL and the API together.

```bash
# 1. Clone the repo
git clone https://github.com/your-username/Code-Thrasher.git
cd Code-Thrasher

# 2. Copy the environment file and set a strong SECRET_KEY
cp .env.example .env

# 3. Start the database and API
docker compose up --build

# 4. Apply database migrations (first run only)
docker compose exec api alembic upgrade head
```

The API is now available at `http://localhost:8000`.

Start the frontend development server separately:

```bash
cd client
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## Local Development Setup

### Backend

```bash
cd server

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies (including dev extras)
uv pip install -e ".[dev]"

# Copy environment variables
cp ../.env.example ../.env      # edit as needed

# Start a local PostgreSQL instance (or use Docker Compose for just the db)
docker compose -f ../docker-compose.yml up db -d

# Run database migrations
alembic upgrade head

# Start the API with live reload
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`.

### Frontend

```bash
cd client
npm install
npm run dev
```

The React app runs at `http://localhost:5173` and proxies API requests to `http://localhost:8000`.

---

## Environment Variables

Copy `.env.example` to `.env` and configure the values before running:

| Variable | Default | Description |
| --- | --- | --- |
| `POSTGRES_USER` | `codethrasher` | PostgreSQL username |
| `POSTGRES_PASSWORD` | `codethrasher` | PostgreSQL password |
| `POSTGRES_DB` | `codethrasher` | PostgreSQL database name |
| `SECRET_KEY` | *(change this)* | Secret used to sign JWTs — use a long random string in production |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | JWT token lifetime in minutes |

---

## Database Migrations

Migrations are managed with Alembic inside the `server/` directory.

```bash
# Apply all pending migrations
alembic upgrade head

# Create a new migration after changing models
alembic revision --autogenerate -m "describe your change"

# Roll back the last migration
alembic downgrade -1
```

---

## Running Tests

```bash
cd server
uv run pytest       # run all tests with coverage
uv run pytest -v    # verbose output
uv run pytest -x    # stop on first failure
uv run pytest --cov-report=html   # generate HTML coverage report in htmlcov/
```

---

## Code Quality

```bash
cd server

black .             # format code
isort .             # sort imports
flake8              # lint
mypy src/           # type check
```

---

## Project Structure

```text
Code-Thrasher/
├── client/                  # React frontend
│   └── src/
│       ├── api/             # Axios API client
│       ├── components/      # Reusable UI components
│       ├── pages/           # Route-level pages
│       ├── store/           # Zustand auth store
│       └── types/           # Shared TypeScript types
├── server/                  # FastAPI backend
│   ├── alembic/             # Database migrations
│   └── app/
│       ├── api/v1/endpoints # Route handlers (auth, exercises, submit)
│       ├── core/            # Config and JWT security
│       ├── db/              # Async SQLAlchemy session
│       ├── models/          # ORM models
│       ├── schemas/         # Pydantic request/response schemas
│       └── services/        # Sandbox execution engine
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## API Reference

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/api/v1/auth/register` | Register a new user |
| `POST` | `/api/v1/auth/login` | Log in and receive a JWT |
| `GET` | `/api/v1/exercises` | List exercises (filter by `difficulty`, `category_id`) |
| `GET` | `/api/v1/exercises/{id}` | Get exercise details and visible test cases |
| `GET` | `/api/v1/exercises/{id}/solution` | Reveal the reference solution for an exercise |
| `POST` | `/api/v1/exercises` | Create an exercise (admin) |
| `POST` | `/api/v1/submit/` | Submit code for evaluation |
| `GET` | `/api/health` | Health check |

Full interactive documentation is available at `http://localhost:8000/api/docs`.

---

## Next

- Track guide and solution reveals per user once authentication is wired into exercise endpoints.

---

## License

[MIT](LICENSE)
````

## File: client/src/types/index.ts
````typescript
export type DifficultyLevel = "beginner" | "intermediate" | "advanced";
export type SubmissionStatus = "pending" | "completed" | "failed";
⋮----
export interface Category {
  id: number;
  name: string;
  slug: string;
}
⋮----
export interface ExerciseListItem {
  id: number;
  title: string;
  difficulty_level: DifficultyLevel;
  category: Category | null;
}
⋮----
export interface TestCase {
  id: number;
  input_data: string;
  expected_output: string;
  score_weight: number;
  is_hidden: boolean;
}
⋮----
export interface ExerciseGuideBlock {
  kind: "nudge" | "pattern" | "checklist" | "snippet" | string;
  title: string;
  body: string;
  code?: string | null;
}
⋮----
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
⋮----
export interface TestCaseResult {
  test_case_id: number;
  passed: boolean;
  expected: string;
  actual: string;
  score_weight: number;
}
⋮----
export interface SubmitResponse {
  submission_id: number;
  status: SubmissionStatus;
  score: number;
  stdout: string;
  stderr: string;
  time_taken_ms: number;
  test_results: TestCaseResult[];
}
⋮----
export interface ExerciseSolution {
  exercise_id: number;
  code: string;
  explanation: string | null;
}
````

## File: server/app/schemas/schemas.py
````python
# ── Categories ────────────────────────────────────────────────────────────────
⋮----
class CategoryOut(BaseModel)
⋮----
id: int
name: str
slug: str
⋮----
model_config = {"from_attributes": True}
⋮----
# ── Exercises ─────────────────────────────────────────────────────────────────
⋮----
class TestCaseOut(BaseModel)
⋮----
input_data: str
expected_output: str
score_weight: float
is_hidden: bool
⋮----
class ExerciseListItem(BaseModel)
⋮----
title: str
difficulty_level: DifficultyLevel
category: CategoryOut | None
⋮----
class ExerciseGuideBlock(BaseModel)
⋮----
kind: str
⋮----
body: str
code: str | None = None
⋮----
class ExerciseDetail(BaseModel)
⋮----
description: str
hint: str | None
guide: list[ExerciseGuideBlock] = Field(default_factory=list)
has_solution: bool = False
⋮----
starter_code: str
⋮----
test_cases: list[TestCaseOut]
⋮----
class ExerciseSolution(BaseModel)
⋮----
exercise_id: int
code: str
explanation: str | None = None
⋮----
class ExerciseCreate(BaseModel)
⋮----
title: Annotated[str, Field(min_length=1, max_length=200)]
⋮----
hint: str | None = None
⋮----
difficulty_level: DifficultyLevel = DifficultyLevel.beginner
category_id: int | None = None
starter_code: str = ""
solution_code: str | None = None
solution_explanation: str | None = None
⋮----
# ── Submissions ───────────────────────────────────────────────────────────────
⋮----
class TestCaseResult(BaseModel)
⋮----
test_case_id: int
passed: bool
expected: str
actual: str
⋮----
class SubmitRequest(BaseModel)
⋮----
code: Annotated[str, Field(max_length=50_000)]
test_results: list[TestCaseResult]
time_taken_ms: int = 0
⋮----
@field_validator("code")
@classmethod
    def code_not_empty(cls, v: str) -> str
⋮----
class SubmitResponse(BaseModel)
⋮----
submission_id: int
status: SubmissionStatus
score: float
stdout: str
stderr: str
time_taken_ms: int
⋮----
class SubmissionHistory(BaseModel)
⋮----
created_at: datetime
⋮----
# ── Progress ──────────────────────────────────────────────────────────────────
⋮----
class ExerciseProgress(BaseModel)
⋮----
best_score: float
attempts: int
solved: bool
⋮----
class ProgressResponse(BaseModel)
⋮----
total_exercises: int
completed_count: int
exercises: dict[int, ExerciseProgress]
````

## File: server/seed.py
````python
#!/usr/bin/env python3
"""Seed the database with initial categories and exercises.

Run from the server/ directory:
    python seed.py
"""
⋮----
CATEGORIES = [
⋮----
# All exercises produce deterministic output (no stdin needed); test cases verify stdout.
# Exercises are therefore deterministic programs; test cases verify the expected output.
EXERCISES = [
⋮----
EXERCISE_GUIDES = {
⋮----
EXERCISE_SOLUTIONS = {
⋮----
async def seed() -> None
⋮----
# Upsert categories and build a slug → model map
category_map: dict[str, Category] = {}
⋮----
result = await db.execute(select(Category).where(Category.slug == cat_data["slug"]))
cat = result.scalar_one_or_none()
⋮----
cat = Category(**cat_data)
⋮----
# Insert exercises and refresh guide content for rows seeded before guides existed.
⋮----
title = ex_data["title"]
guide = EXERCISE_GUIDES.get(title, [])
solution = EXERCISE_SOLUTIONS.get(title, {})
⋮----
result = await db.execute(select(Exercise).where(Exercise.title == ex_data["title"]))
existing_exercise = result.scalar_one_or_none()
⋮----
tc_list = ex_data["test_cases"]
cat_slug = ex_data["category_slug"]
exercise_data = {
⋮----
exercise = Exercise(
````

## File: client/src/pages/ExerciseDetail.tsx
````typescript
import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import api from "@/api/client";
import CodeEditor from "@/components/editor/CodeEditor";
import ExerciseGuidePanel from "@/components/exercise/ExerciseGuidePanel";
import { getPyodide, runPython } from "@/services/pyodide";
import { useProgressStore } from "@/store/useProgressStore";
import type {
  ExerciseDetail as ExerciseDetailType,
  ExerciseListItem,
  SubmitResponse,
  TestCaseResult,
} from "@/types";
⋮----
// Kick off Pyodide download in the background while the user reads the problem
⋮----
.catch(() => {/* will surface as error on submit */});
⋮----
// eslint-disable-next-line react-hooks/exhaustive-deps
⋮----
function goToExercise(exerciseId: number | undefined)
⋮----
async function handleSubmit()
⋮----
{/* Left — problem description */}
⋮----
{/* Right — editor + submit */}
⋮----
{/* Result panel */}
````
