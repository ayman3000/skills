# Claude Skills

This directory contains skills designed for the Claude desktop application.

## How to Upload a Skill

To import any of these skills into your Claude Desktop application:
1. Open the Claude Desktop app.
2. Select **"Create Skill"** from the sidebar or settings.
3. Choose **"Upload a Skill"**.
4. Select the `SKILL.md` file from the desired skill directory.

---

## PDF Course Creator Skill

**Directory:** `pdf-course-skill/`

Use this skill whenever the user wants to create a polished, publication-ready PDF book, manual, guide, or course material. Covers the full pipeline: Markdown authoring with LaTeX headers, pandoc compilation, flowchart rendering from Mermaid diagrams, and a premium minimal cover page rendered via Playwright. Also use when the user asks to create a cover page for a PDF, build a multi-chapter book or guide, render Mermaid diagrams to PNG for embedding, or produce a final ZIP deliverable containing the PDF and all source files. Trigger on any request like "create a PDF book", "make a course PDF", "build a technical guide", "generate a manual", "create a book with cover", or any mention of producing a professional PDF document with chapters. This skill is general-purpose — it works for ANY topic, not just courses.

---

## Trustworthy Application Principles

**Directory:** `trustworthy-app-principles/`

Ten stack-agnostic principles for building and auditing applications that users can trust — desktop or web. Derived from real AI-assisted development and audit work.

**When to use:**
- Before shipping a new feature
- When auditing an existing application for trust issues
- When reviewing changes that affect I/O, errors, state, permissions, or user actions
- When designing a screen, workflow, or recovery path
- When evaluating sensitive data handling, security-event logging, or retention

**The ten principles:**

1. **Responsiveness is the product** — every action receives prompt, meaningful feedback
2. **Render first, refine in the background** — show stable structure immediately and use accessible loading states
3. **Retry transient failures, fail fast on deterministic ones** — classify errors structurally
4. **Never fail silently** — every operation ends with a result or an actionable message
5. **Honesty over completion** — never invent data, fake success, or disguise taxonomy mismatches
6. **Warn before irreversible or outward-facing actions** — proportional confirmation with preview
7. **Long work is cancellable** — cancel must stop the work, not just hide the UI
8. **State is the source of truth, not the UI** — persist first, react second
9. **Persistence is a feature, not an afterthought** — user data survives crashes and reloads
10. **Present numbered options with a recommended choice** — decisions should be scannable and actionable

**Includes:**
- 12-item audit checklist
- 12-entry common violations catalog
