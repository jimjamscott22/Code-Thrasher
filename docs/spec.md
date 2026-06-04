

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