# AI Agent Skills

A centralized collection of custom skills for AI agents like Claude and Codex. Each skill is a reusable, documented workflow that simplifies repetitive tasks, enforces quality standards, and enhances productivity.

## Structure

```
skills/
├── claude/
│   ├── pdf-course-skill/
│   │   └── SKILL.md                  # PDF book/manual/course generator
│   └── trustworthy-app-principles/
│       └── SKILL.md                  # 10 principles + audit checklist for app trust
└── codex/                            # (Currently empty)
```

## Claude Skills

### PDF Course Creator

**Directory:** `claude/pdf-course-skill/`

Generates polished, publication-ready PDF books, manuals, guides, and course materials. Handles Markdown authoring with LaTeX headers, pandoc compilation, Mermaid diagram rendering, and minimal cover pages via Playwright. General-purpose — works for any topic.

### Trustworthy Application Principles

**Directory:** `claude/trustworthy-app-principles/`

Ten stack-agnostic principles for building and auditing applications that users can trust — desktop or web. Covers responsiveness, honest failure, cancellation, persistence, safe actions, and clear decision UX. Includes a 12-item audit checklist and a 12-entry common violations catalog.

**The ten principles:**

1. Responsiveness is the product
2. Render first, refine in the background
3. Retry transient failures, fail fast on deterministic ones
4. Never fail silently
5. Honesty over completion
6. Warn before irreversible or outward-facing actions
7. Long work is cancellable
8. State is the source of truth, not the UI
9. Persistence is a feature, not an afterthought
10. Present numbered options with a recommended choice

## How to Add Claude Skills

To import a skill into your Claude Desktop application:
1. Open the Claude Desktop app.
2. Select **"Create Skill"**.
3. Choose **"Upload a Skill"** and select the `SKILL.md` from the desired skill directory.

## License

MIT