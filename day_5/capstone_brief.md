# Day 5 — Capstone

**This is your chance to build something you'd actually want to use.**

You've spent four days learning how to build AI systems: chat loops and the Agents SDK on Day 1, tools and memory on Day 2, multi-agent orchestration on Day 3, and RAG on Day 4. Today you put it together — your way.

The goal is simple: by the end of the day, you have a working AI system of your own design that you can demo to the class in five minutes.

You can choose your shape (single-agent, multi-agent, or RAG), your domain (anything that interests you), and your scope (ambitious or focused). The only requirements are that it works, that it shows what you've learned, and that it produces something demoable.

---

## What you have available

Everything from the week is yours to reuse:

- **The chat loop and Agents SDK** from Day 1 — agent, tools, structured outputs, sessions
- **The `agent_workshop` package** from Day 2 — pre-built tools (crypto, currency, gold, weather, search, file I/O) and the assistant agent factories
- **The orchestration patterns** from Day 3 — Manager, Handoff, Python orchestration
- **The `rag_workshop` package** from Day 4 — ingestion, retrieval, citation validation, evaluation
- **Tracing, guardrails, and structured outputs** from across the week
- **Your own code** from the labs

You don't have to build everything from scratch. The best capstones reuse existing tools and patterns and add something new on top.

---

## Choose your shape

Pick the architectural shape that fits your idea.

### 🧰 Tool-heavy single agent

One agent, several tools, a session for memory. The work is in choosing the right tools and writing instructions that make the agent reliable.

**Project ideas:**

- **Personal briefing agent** — combines weather, crypto, news, and a calendar tool into a "morning brief" with a structured output
- **Code review buddy** — reads a code file from disk and flags issues (style, bugs, naming) with severity
- **Interview prep coach** — generates technical questions for a chosen role, scores your answers, tracks weak areas across the session
- **Recipe assistant** — remembers dietary preferences, suggests substitutions, plans meals for the week
- **Study session timer** — tracks topics you cover during a study session and generates a summary you can keep
- **Personal librarian** — reads your bookshelf (text file), recommends what to read next based on mood, remembers preferences

### 🤝 Multi-agent system

Several specialist agents coordinated by one of Day 3's patterns. The work is in defining roles clearly and choosing the right orchestration.

**Project ideas:**

- **Trip planner** (Manager pattern) — flight finder + hotel finder + activities specialists synthesised into a structured itinerary, saved as a markdown trip brief
- **University helpdesk** (Handoff pattern) — triage agent routes between academic advisor, IT support, library, and student records specialists
- **Job application coach** (Manager pattern) — job parser + CV reviewer + cover letter writer that produces a tailored application package
- **Research report builder** (Python orchestration) — outline → research → draft → review pipeline producing a markdown report
- **Stock or crypto briefing service** (Manager pattern) — market data + news + sentiment agents producing a structured morning briefing per ticker
- **Customer support simulator** (Handoff pattern) — triage agent routes between billing, technical support, refunds, and account recovery specialists

### 📚 RAG system

A knowledge base plus an agent that grounds answers in it. The work is in choosing good source material and verifying answers stay grounded.

**Project ideas:**

- **Course notes assistant** — RAG over your own lecture notes; answers questions with citations to specific lectures
- **Personal book recommender** — RAG over your reading history (books you've read, with notes); suggests similar reads with reasoning
- **University handbook bot** — RAG over the student handbook PDF; answers procedural questions ("how do I appeal a grade?")
- **API documentation assistant** — RAG over a library's docs; answers code questions with example snippets from the docs
- **Research paper summariser** — RAG over a paper you're reading; lets you ask follow-up questions grounded in the paper
- **Legal/policy explainer** — RAG over a public policy document (e.g. GDPR, university policy); explains rules with citations

---

## Or invent your own

These are starting points. If you have a different idea, build it. The strongest capstones are usually projects students *genuinely care about* — your own coursework, your hobby, a problem you've actually had.

A few rules of thumb for picking your own idea:

- **Useful to you personally.** If you'd actually use the result, you'll build something good. If you're building it just for the demo, motivation drops.
- **Buildable in a day.** Cut scope until you have something runnable by mid-afternoon. Polish what works rather than starting more.
- **Demoable in five minutes.** If you can't show the value in five minutes, the idea is too abstract or too big.

---

## Requirements

By the end of the day, your project must:

- **Run end-to-end.** A working demo students can see live.
- **Use at least one tool, agent, or RAG pattern from the week.** Reuse is the point — don't reinvent.
- **Produce a real artefact.** A markdown file, a structured output, a saved document, a conversation transcript — something visible.
- **Be inspectable.** Wrap your runs in `trace(...)` so you can show the trace dashboard if asked.
- **Live in a notebook.** A notebook version is sufficient. You can refactor to modules afterwards if you want.

Optional but recommended:

- **At least one guardrail** if you're building a multi-agent or RAG system
- **A small eval suite** (3-5 cases) if your domain has clear correctness criteria
- **Memory/sessions** if your agent benefits from remembering across turns

---

## The day's structure

| Time | What you're doing |
|---|---|
| **10:00 – 10:30** | Welcome and brief recap of what's available |
| **10:30 – 11:30** | Ideation and scoping — pick an idea, sketch the architecture, get instructor sign-off |
| **11:30 – 13:15** | Build (morning) — get something running end-to-end |
| **13:15 – 14:30** | Lunch |
| **14:30 – 16:30** | Build (afternoon) — polish, add features, prepare your demo |
| **16:30 – 18:00** | 5-minute demos to the class |

**By 13:00, you should have something runnable** — even if it's rough. The afternoon is for polish, not for getting the basics working. If you're still debugging the core flow at 14:30, cut scope.

---

## The demo

You'll have **5 minutes** to present. The class will be your audience. Here's a structure that works:

1. **What you built (30 seconds)** — One sentence on the project, one sentence on why you chose it
2. **Architecture (1 minute)** — Sketch the shape: single agent? multi-agent? RAG? Which orchestration pattern? Which tools?
3. **Live demo (3 minutes)** — Run it in front of everyone. Show the trace if there's something interesting in it.
4. **What you learned (30 seconds)** — One technical insight from building it. Could be a failure mode you didn't expect, a pattern that worked unexpectedly well, or a decision you'd make differently.

Be ready to take a question or two after.

**Demos are time-boxed.** Practise it once before you present — most people overrun on their first try.

---

## Tips for making it through the day

**Cut scope early, polish what works.** A small project that runs end-to-end beats an ambitious project that doesn't quite work. If you're behind at lunch, cut features, not corners.

**Get something running first, improve it second.** Build the dumbest version of your idea by 12:00 — even if it's ugly, hallucinates, and only handles one input. Then improve it.

**Test the demo, not just the code.** Run your demo flow at 16:00 — exactly as you'll show it. Catches the surprises you don't want to see live.

**Watch for these common pitfalls:**

- Building three things instead of finishing one
- Spending an hour on prompt tweaking before the basic flow works
- Adding a guardrail before the agent does anything useful
- Forgetting to test what happens when a tool errors
- Starting your demo presentation from cell 1 — show the *interesting* part

**When you're stuck, ask.** Your instructor is available all day. Most "I'm stuck" problems are fixable in a few minutes of pairing.

---

## What "done" looks like

By 16:30, your project should:

- Run from start to finish without manual intervention
- Show *something* interesting in the trace
- Produce an artefact (file, structured output, transcript) you can show
- Have a one-paragraph README in the notebook explaining what it does

It does not need to:

- Handle every edge case
- Be production-deployable
- Use every pattern from the week
- Have comprehensive tests

This is one day of work. The bar is *"a working prototype I can demo and be proud of"*, not *"a portfolio-ready product"*. If you want to polish further afterwards, that's a great way to spend the weekend.

---

## After the demos

Congratulations — you've built and demoed a working AI system in one day. That's a real accomplishment.

A few suggestions for what to do next:

- **Polish it for your portfolio.** Add a proper README, refactor to modules, push to GitHub. The notebook version is fine for the demo; a clean repo is fine for a CV.
- **Share it.** Write a short post about what you built — on LinkedIn, Medium, your personal site. AI engineering content gets read.
- **Extend it.** Pick one thing the demo couldn't do and add it. Each extension is a chance to practise what you learned.
- **Help someone else build theirs.** Find a friend who wants to learn AI engineering. Walk them through what you did. Teaching is the fastest way to consolidate.

Most importantly: **you now know enough to build real AI systems.** What you choose to build with that knowledge is up to you.

Good luck — and have fun building.
