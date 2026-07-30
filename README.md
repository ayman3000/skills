# AI Agent Skills

A centralized collection of reusable [Agent Skills](https://agentskills.io) for compatible AI agents. Each skill follows the portable `skill-name/SKILL.md` format with YAML metadata and Markdown instructions. Skills simplify repetitive work, enforce quality standards, and can be installed in supported tools such as Claude Code, Codex, and GitHub Copilot.

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

## Install in supported agents

Copy the complete skill directory—not only `SKILL.md`—to a location scanned by your agent:

| Agent | Personal skills | Project skills |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/<skill-name>/` | `.claude/skills/<skill-name>/` |
| Codex | `~/.agents/skills/<skill-name>/` | `.agents/skills/<skill-name>/` |
| GitHub Copilot | `~/.copilot/skills/<skill-name>/` or `~/.agents/skills/<skill-name>/` | `.github/skills/<skill-name>/`, `.claude/skills/<skill-name>/`, or `.agents/skills/<skill-name>/` |

Other tools can use these skills if they implement the open Agent Skills specification or let you load Markdown instruction files manually. Compatibility is not automatic for every agent product; consult the tool's skill or instruction-file documentation.

## Validation

Both skills pass the official reference validator:

```bash
uvx --from skills-ref agentskills validate path/to/skill
```

## License

MIT