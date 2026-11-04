# BuddySplit

Group expense tracker with real-time updates, settlement minimization, CSV export, and receipt uploads.

## Quick start

```bash
npm install
npm run dev
# backend :4000 · frontend :5173
```

## Scripts

| Script | What |
|--------|------|
| `npm run dev` | Concurrent backend + frontend (VSCode “Start Debugging”) |
| `npm run build` | Type-check backend; Vite build frontend |
| `npm test` | Unit + integration tests |
| `npm run lint` | ESLint + Prettier |
| `npm run test:e2e` | Playwright E2E (needs browsers) |

## Env vars

| Var | Default | Purpose |
|-----|---------|---------|
| `PORT` | `4000` | HTTP port |
| `DATABASE_URL` | `buddysplit.db` | SQLite file path |
| `JWT_ACCESS_SECRET` | `dev-access-secret-change-me` | Access token signing |
| `JWT_REFRESH_SECRET` | `dev-refresh-secret-change-me` | Refresh token signing |
| `NODE_ENV` | `development` | Switches error details / cookie secure |
| `VITE_API_URL` | `/api` | API base (for production) |
| `VITE_SOCKET_URL` | `` | Socket.io URL (omit for proxy) |

## Docker Compose

Start backend + Adminer (SQLite inspector) on `http://localhost:8080`:

```bash
docker compose up -d
```

## Project structure

```
backend/src
├── index.ts          # HTTP server init
├── routes/           # Express routers
└── lib/              # Prisma schema · split · balance · settlement · auth · ws
frontend/src
├── pages/            # Group, Expense, Dashboard, Auth, Invite
├── lib/              # API client · auth · ws · format · toast
└── App.tsx
```

License: MIT