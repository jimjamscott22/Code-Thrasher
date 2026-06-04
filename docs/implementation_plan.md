

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