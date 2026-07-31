# AI Agent Skills

Reusable skills for Claude, Codex, GitHub Copilot, and other tools that implement the open [Agent Skills specification](https://agentskills.io).

## Architecture

The repository keeps one canonical source for each skill and generates ready-to-install copies for every supported agent:

```text
skills/
├── canonical/                         # Source of truth — edit here
│   ├── pdf-course-skill/
│   │   └── SKILL.md
│   ├── trustworthy-app-principles/
│   │   └── SKILL.md
│   └── README.md
├── claude/                            # Generated distribution
│   ├── pdf-course-skill/
│   ├── trustworthy-app-principles/
│   └── README.md
├── codex/                             # Generated distribution
│   ├── pdf-course-skill/
│   ├── trustworthy-app-principles/
│   └── README.md
├── copilot/                           # Generated distribution
│   ├── pdf-course-skill/
│   ├── trustworthy-app-principles/
│   └── README.md
├── scripts/
│   └── sync-skills.py
└── .github/workflows/
    └── validate-skills.yml
```

Do not edit skill files under `claude/`, `codex/`, or `copilot/`. Edit `canonical/<skill-name>/`, then run the synchronization script.

## Available skills

### PDF Course Creator

Produces publication-ready PDF books, manuals, guides, and course materials. Covers content authoring, diagrams, cover generation, PDF assembly, and source packaging.

### Trustworthy Application Principles

Ten stack-agnostic principles for building and auditing trustworthy desktop and web applications. Covers responsiveness, honest failure, cancellation, persistence, safe actions, and clear decision UX. Includes a 12-item audit checklist and 12 common violations.

## Install

Download or copy a complete skill directory from the folder for your agent:

- **Claude:** use a directory under `claude/`
- **Codex:** use a directory under `codex/`
- **GitHub Copilot:** use a directory under `copilot/`

Then place it in a location scanned by the tool:

- **Claude Code:** `~/.claude/skills/<skill-name>/` or `.claude/skills/<skill-name>/`
- **Codex:** `~/.agents/skills/<skill-name>/` or `.agents/skills/<skill-name>/`
- **GitHub Copilot:** `~/.copilot/skills/<skill-name>/`, `~/.agents/skills/<skill-name>/`, `.github/skills/<skill-name>/`, or `.agents/skills/<skill-name>/`

## Maintain

After changing a canonical skill, regenerate all distributions:

```bash
python3 scripts/sync-skills.py
```

Verify that generated copies are current:

```bash
python3 scripts/sync-skills.py --check
```

Validate a skill against the open specification:

```bash
uvx --from skills-ref agentskills validate canonical/<skill-name>
```

CI checks synchronization and validates every canonical and generated skill package on pushes and pull requests.

## License

MIT
