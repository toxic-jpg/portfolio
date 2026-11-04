# BuddySplit — Kanban Task Board

> Layer: `B` = backend, `F` = frontend, `D` = database, `T` = testing, `C` = infra/config
> Priority: **CRITICAL** → **HIGH** → **MEDIUM** → **LOW**

---

## CRITICAL — MVP Core

| ID | Title | Layer | Assignee | Dependencies | Est. LOC |
|----|-------|-------|----------|--------------|----------|
| C-01 | Project scaffolding — monorepo structure, package.json, tsconfig, vite.config, ESLint, Prettier | C | dev | — | 50 |
| C-02 | Prisma schema — User, Group, Member, Expense, Split, Settlement, InviteToken models + initial migration | D | dev | C-01 | 180 |
| C-03 | Auth: register endpoint (bcrypt + JWT access token) + login endpoint | B | auth | C-01, C-02 | 120 |
| C-04 | Auth: refresh token flow — /auth/refresh endpoint using httpOnly cookie | B | auth | C-03 | 80 |
| C-05 | Middleware: auth guard (JWT verify), Zod request validation, global error handler | B | infra | C-01, C-02 | 100 |
| C-06 | Groups: POST /groups (create), GET /groups/me (my groups), DELETE /groups/:id | B | groups | C-02, C-03, C-05 | 150 |
| C-07 | Invite tokens: POST /groups/:id/invite (generate), accept via GET /invite/:token (join group) | B | groups | C-06 | 120 |
| C-08 | Expense CRUD: POST /groups/:id/expenses, GET /groups/:id/expenses, PATCH, DELETE | B | expenses | C-06, C-05 | 200 |
| C-09 | Split calculator — equal, percentage, custom split types per expense | B | expenses | C-08 | 150 |
| C-10 | Balance engine — compute per-member net balance from all expenses in a group | B | settle | C-09 | 120 |
| C-11 | Frontend scaffold — Vite + React Router v6 + Tailwind + context providers | F | ui | C-01 | 80 |
| C-12 | Auth pages — Login, Register, protected route wrapper, AuthContext | F | ui | C-03, C-04, C-11 | 280 |
| C-13 | API client — fetch wrapper with auto-refresh-token logic | F | api | C-03, C-04 | 60 |
| C-14 | Group page — list my groups, create group form | F | ui | C-06, C-11 | 180 |
| C-15 | Expense list page — table of expenses for a group, add/edit/delete forms | F | ui | C-08, C-09, C-11 | 320 |
| C-16 | Dashboard — balance summary, who-owes-whom, total spent | F | ui | C-10, C-11 | 220 |

---

## HIGH — Essential Features

| ID | Title | Layer | Assignee | Dependencies | Est. LOC |
|----|-------|--------|----------|--------------|----------|
| H-01 | Settlement minimization algorithm — graph-based to minimize transaction count | B | settle | C-10 | 180 |
| H-02 | Settlement display — "A pays B $X" output on dashboard | F | ui | H-01 | 100 |
| H-03 | Category system — expense categories (food, transport, etc.) stored in DB | D | dev | C-02 | 40 |
| H-04 | Expense history — filter by date range, category, member; server-side pagination | B | expenses | H-03, C-08 | 160 |
| H-05 | Expense history UI — filter bar + paginated table | F | ui | H-04 | 180 |
| H-06 | Receipt upload — POST /expenses/:id/receipt, store to /public/uploads, link in DB | B | expenses | C-08 | 100 |
| H-07 | Receipt image served via GET /uploads/:filename | B | infra | H-06 | 30 |
| H-08 | Socket.io setup — server init, room-per-group, emit on expense mutations | B | ws | C-01, C-08 | 90 |
| H-09 | WebSocket hook — useGroupEvents hook that subscribes to group room | F | ws | H-08, C-13 | 80 |
| H-10 | CSV export — GET /groups/:id/export/csv, stream response | B | exports | C-08 | 70 |
| H-11 | Role-based access — admin vs member permissions (create expense, delete group, manage invites) | B | groups | C-06 | 80 |
| H-12 | Responsive mobile-first layout — navigation drawer, card-based expense view on small screens | F | ui | C-11 | 150 |

---

## MEDIUM — Quality of Life

| ID | Title | Layer | Assignee | Dependencies | Est. LOC |
|----|-------|--------|----------|--------------|----------|
| M-01 | Activity feed — log of all expense add/edit/delete events per group | B | expenses | C-08 | 100 |
| M-02 | Activity feed UI — timeline component on dashboard | F | ui | M-01 | 120 |
| M-03 | Edit receipt — PUT /expenses/:id, update description/category/split | B | expenses | C-08 | 60 |
| M-04 | Delete confirmation — soft-delete expenses with reason | B | expenses | C-08 | 40 |
| M-05 | Expense search — text search across descriptions | B | expenses | H-04 | 50 |
| M-06 | Bulk delete — select multiple expenses and delete at once | F | ui | C-08 | 80 |
| M-07 | Group settings — rename group, change icon, leave group (member), kick member (admin) | B | groups | C-06 | 120 |
| M-08 | Member management UI — list members, role controls, leave/kick actions | F | ui | M-07 | 100 |
| M-09 | Empty states — meaningful copy and illustrations for no-expenses, no-groups views | F | ui | C-11 | 60 |
| M-10 | Toast notifications — success/error feedback on all mutations | F | ui | C-11 | 70 |

---

## LOW — Polish & Testing

| ID | Title | Layer | Assignee | Dependencies | Est. LOC |
|----|-------|--------|----------|--------------|----------|
| L-01 | Vitest setup + config | T | test | C-01 | 30 |
| L-02 | Backend unit tests — auth, split calculation, balance engine, settlement | T | test | C-09, C-10, H-01 | 250 |
| L-03 | Frontend unit tests — API client, formatters, hooks | T | test | C-13, H-09 | 120 |
| L-04 | Playwright E2E — register/login flow | T | test | C-03, C-04 | 100 |
| L-05 | Playwright E2E — create group, add expense, view balance | T | test | C-06, C-08, C-10 | 150 |
| L-06 | Playwright E2E — settlement display, CSV export | T | test | H-01, H-10 | 100 |
| L-07 | Health check endpoint — GET /health | B | infra | C-01 | 20 |
| L-08 | Docker Compose — backend + SQLite + adminer for local dev | C | infra | C-01, C-02 | 60 |
| L-09 | README — setup instructions, env vars, project structure | C | dev | C-01 | 80 |
| L-10 | GitHub Actions CI — lint, test, build on push | C | infra | L-01 | 60 |

---

## Estimated Totals

| Layer | Est. LOC |
|-------|----------|
| Backend | ~2,150 |
| Frontend | ~2,200 |
| Database / Schema | ~220 |
| Testing | ~800 |
| Infra / Config | ~270 |
| **Total** | **~5,640** |

> Note: LOC estimate includes comments and test code. Core app logic is ~2,800 LOC; remaining is scaffolding, tests, and config. Actual may vary ±30%.

---

## Task Dependency Graph (key paths)

```
C-01 ──→ C-02 ──→ C-03 ──→ C-05 ──→ C-06 ──→ C-08 ──→ C-09 ──→ C-10 ──→ H-01 ──→ H-02
                                    │                                    │
                                    └──→ C-07                            └──→ M-01 ──→ M-02
                                                                          (activity feed)
                                    ┌──→ H-03 ──→ H-04 ──→ H-05
                                    │                              (history)
C-11 ──→ C-12 ──→ C-13 ──→ C-14 ──→ C-15 ──→ C-16
              │         │         │          │
              └──→ H-08 ──→ H-09 (real-time)
                     │
              H-06 ──→ H-07 (receipts)
                     │
              H-10 (export)

L-01 ──→ L-02 ──→ L-04 ──→ L-05 ──→ L-06
L-01 ──→ L-03
L-07 (health) → L-08 (docker)
L-08 → L-09 (README)
L-01 → L-10 (CI)
```

---

## Suggested Build Order

1. **Week 1:** C-01, C-02, C-03, C-04, C-05, C-11 (foundation)
2. **Week 2:** C-06, C-07, C-08, C-09, C-10, C-12, C-13, C-14 (core data)
3. **Week 3:** C-15, C-16, H-01, H-02, H-03, H-04, H-05, H-06, H-07 (MVP complete)
4. **Week 4:** H-08, H-09, H-10, H-11, H-12, M-01–M-10 (features + polish)
5. **Week 5:** L-01–L-10 (testing + deployment prep)
