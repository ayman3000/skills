# AI Agent Skills

Reusable skills for Claude, Codex, and GitHub Copilot. Every skill follows the open [Agent Skills specification](https://agentskills.io): a directory containing a `SKILL.md` file with YAML metadata and Markdown instructions.

## Repository structure

```text
skills/
├── claude/
│   ├── pdf-course-skill/
│   │   └── SKILL.md
│   ├── trustworthy-app-principles/
│   │   └── SKILL.md
│   └── README.md
├── codex/
│   ├── pdf-course-skill/
│   │   └── SKILL.md
│   ├── trustworthy-app-principles/
│   │   └── SKILL.md
│   └── README.md
└── copilot/
    ├── pdf-course-skill/
    │   └── SKILL.md
    ├── trustworthy-app-principles/
    │   └── SKILL.md
    └── README.md
```

Each agent directory contains the same portable skills so users can download the directory intended for their tool without reorganizing files.

## Available skills

### PDF Course Creator

Generates polished PDF books, manuals, guides, and course materials. Covers Markdown authoring, LaTeX and Pandoc compilation, Mermaid diagram rendering, cover production, PDF merging, and source packaging.

### Trustworthy Application Principles

Ten stack-agnostic principles for building and auditing trustworthy desktop and web applications. Covers responsiveness, honest failure, cancellation, persistence, safe actions, and clear decision UX. Includes a 12-item audit checklist and 12 common violations.

## Install

Copy the complete skill directory—not only `SKILL.md`—to a location scanned by your agent.

- **Claude Code:** `~/.claude/skills/<skill-name>/` or `.claude/skills/<skill-name>/`
- **Codex:** `~/.agents/skills/<skill-name>/` or `.agents/skills/<skill-name>/`
- **GitHub Copilot:** `~/.copilot/skills/<skill-name>/`, `~/.agents/skills/<skill-name>/`, `.github/skills/<skill-name>/`, or `.agents/skills/<skill-name>/`

See the README inside each agent directory for tool-specific instructions.

## Validate

Both skills pass the official Agent Skills reference validator:

```bash
uvx --from skills-ref agentskills validate path/to/skill
```

## License

MIT
