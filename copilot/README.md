# GitHub Copilot Skills

Ready-to-install Agent Skills for GitHub Copilot.

> These skill directories are generated from `canonical/`. Do not edit their `SKILL.md` files directly. Update the canonical skill and run `python3 scripts/sync-skills.py` from the repository root.

## Install

Copy a complete skill directory to a supported location:

- Personal: `~/.copilot/skills/<skill-name>/` or `~/.agents/skills/<skill-name>/`
- Project: `.github/skills/<skill-name>/`, `.claude/skills/<skill-name>/`, or `.agents/skills/<skill-name>/`

Keep `SKILL.md` and any bundled resources together. Reload skills or restart Copilot if a newly added skill does not appear.

## Available skills

### PDF Course Creator

**Directory:** `pdf-course-skill/`

Produces publication-ready PDF books, manuals, guides, and course materials. Includes content authoring, diagrams, cover generation, PDF assembly, and source packaging.

### Trustworthy Application Principles

**Directory:** `trustworthy-app-principles/`

Provides ten stack-agnostic principles for trustworthy desktop and web applications plus an on-demand 12-item audit checklist with common red flags.
