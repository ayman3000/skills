# Codex Skills

Ready-to-install Agent Skills for OpenAI Codex.

> These skill directories are generated from `canonical/`. Do not edit their `SKILL.md` files directly. Update the canonical skill and run `python3 scripts/sync-skills.py` from the repository root.

## Install

Copy a complete skill directory to one of these locations:

- Personal: `~/.agents/skills/<skill-name>/`
- Project: `.agents/skills/<skill-name>/`

Codex loads skill metadata for discovery and reads the complete `SKILL.md` after selecting a skill. Restart Codex if a newly added skill does not appear.

## Available skills

### PDF Course Creator

**Directory:** `pdf-course-skill/`

Produces publication-ready PDF books, manuals, guides, and course materials. Includes content authoring, diagrams, cover generation, PDF assembly, and source packaging.

### Trustworthy Application Principles

**Directory:** `trustworthy-app-principles/`

Provides ten stack-agnostic principles for trustworthy desktop and web applications, a 12-item audit checklist, and 12 common violations.
