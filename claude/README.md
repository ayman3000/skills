# Claude Skills

This directory contains skills specifically designed for the Claude desktop application.

## How to Upload a Skill

To import any of these skills into your Claude Desktop application:
1. Open the Claude Desktop app.
2. Select **"Create Skill"** from the sidebar or settings.
3. Choose **"Upload a skill"**.
4. Select the desired `.skill` file from this directory.

---

## PDF Course Creator Skill
**File:** `pdf-course-skill.skill`

Use this skill whenever the user wants to create a polished, publication-ready PDF book, manual, guide, or course material. Covers the full pipeline: Markdown authoring with LaTeX headers, pandoc compilation, flowchart rendering from Mermaid diagrams, and a premium minimal cover page rendered via Playwright. Also use when the user asks to create a cover page for a PDF, build a multi-chapter book or guide, render Mermaid diagrams to PNG for embedding, or produce a final ZIP deliverable containing the PDF and all source files. Trigger on any request like "create a PDF book", "make a course PDF", "build a technical guide", "generate a manual", "create a book with cover", or any mention of producing a professional PDF document with chapters. This skill is general-purpose — it works for ANY topic, not just courses.
