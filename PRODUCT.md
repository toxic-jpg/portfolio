# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

static HTML/CSS/JS (single-page portfolio, no build step)

## Users

**Primary:**
- Recruiters and hiring managers looking for junior/entry-level software developers, interns, or new grads. They arrive from LinkedIn, GitHub, or direct application links. They scan for: real shipped code, tech stack match, communication clarity, and "can this person do the job?" They need to decide in 30-60 seconds.

- Freelance clients and small-business owners looking to hire for fixed-price projects ($20–$300). They arrive from r/forhire, Upwork, or direct referral. They scan for: relevant project examples, pricing transparency, communication reliability, and "will this person deliver?" They need proof of working deliverables.

**Secondary:**
- Peer developers and collaborators who might refer work or collaborate on open source. They arrive from GitHub. They scan for: code quality, project depth, technical curiosity.

## Product Purpose

A single-page portfolio that proves Heart Lawrence Candelario ships real, working applications — not homework, not snippets — and makes it dead-simple for the right visitor to hire or contract them.

Success = a qualified inquiry (recruiter reaches out, freelance client requests a quote, peer refers work).

## Positioning

The BSIT student who already builds production-grade software. Not "learning to code" — already coding for real clients, real users, real deployments. The portfolio itself is evidence: every project card links to a working demo or source. The "$20–$300" pricing line is a filter, not a plea.

Neighboring products (other student portfolios) cannot truthfully claim: 8 working demos with live links, a published CLI tool with zero dependencies, a FastAPI + Tkinter desktop app with 33 tests, a React + Socket.io real-time expense tracker, a WordPress plugin handling 7→Sheets sync with zero WP dependencies.

## Operating Context

- Viewed on desktop (recruiter workflow) and mobile (quick scan from LinkedIn/email)
- Philippines-based (GMT+8) — time zone matters for async clients
- Remote-first; all collaboration is async (GitHub, email, chat)
- No design system — single page, hand-authored CSS variables
- No CMS — content lives in HTML, updated manually
- Deployed to GitHub Pages via push to main

## Capabilities and Constraints

**Confirmed:**
- Single HTML file + CSS + vanilla JS (nav toggle only)
- All project demos are subfolders in the same repo (relative links)
- Contact = mailto + GitHub link (no form backend)
- SEO: meta title, description, semantic HTML
- Accessibility: skip link, focus-visible, ARIA labels, prefers-reduced-motion, semantic landmarks

**Constraints:**
- No build step, no framework, no server — must stay static
- GitHub Pages hosting (HTTPS, custom domain possible)
- Content updates = edit HTML/CSS directly
- No analytics/tracking currently

**Undecided:**
- Whether to add a contact form (would need Netlify Functions or similar)
- Whether to add blog/writing section
- Whether to migrate to a framework (Astro, Next.js) for scale

## Brand Commitments

- Name: Heart Lawrence Candelario (goes by "Heart")
- Handle: toxic-jpg (GitHub)
- Email: heartlawrencecandelario@gmail.com
- Location: Philippines (GMT+8)
- Voice: Direct, honest, builder-first. "I ship working code, not just snippets." No buzzword padding.
- Pricing transparency: "$20–$300" fixed-price freelance — stated upfront

## Evidence on Hand

**Working demos (all live in repo subfolders):**
- ScholarOS/ — FastAPI + Tkinter desktop app, 1,180 LOC, 33 tests
- BuddySplit/ — React + Node + PostgreSQL + Socket.io expense tracker
- pennypinch/ — Pure-stdlib Python CLI finance tracker
- python-csv-cleaner_20261024_1555/ — pandas + openpyxl data cleaner
- wp-contact-form-7-google-sheets_20261024_1555/ — PHP WordPress plugin
- test_shopify_demo/ — HTML/CSS/JS/Liquid Shopify section builder
- forhire-1xcb5t2/ — Flask + SQLite freelance delivery ($50 fixed)
- js-bug-fix-demo/ — [NEEDS REVIEW: broken card, local path in description]

**Absences (do not fabricate):**
- No client testimonials yet
- No case studies with metrics (revenue saved, users, etc.)
- No team/collaboration evidence (all solo work shown)
- No open-source contribution graph beyond own repos

## Product Principles

1. **Ship the proof.** Every claim links to a working demo or source. No "coming soon," no placeholder images.
2. **Price the work.** Transparent freelance pricing filters tire-kickers and signals professionalism.
3. **Respect the visitor's time.** Scannable, honest, no fluff. Recruiters decide in seconds.
4. **Own the student identity.** BSIT student is a fact, not a weakness — the work proves capability beyond coursework.
5. **Stay static, stay simple.** No build step, no framework debt. The portfolio is a tool, not a project.

## Accessibility & Inclusion

- WCAG AA target for contrast (currently fails on primary button hover states)
- Semantic HTML landmarks throughout
- Keyboard-navigable with visible focus states
- Reduced-motion respected
- Color is not the only information carrier (icons + text)
- Text scale responsive via clamp()