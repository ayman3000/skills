# Canonical Skills

This directory is the source of truth for every portable Agent Skill in the repository.

## Editing a skill

1. Edit the skill under `canonical/<skill-name>/`.
2. Synchronize generated copies:

   ```bash
   python3 scripts/sync-skills.py
   ```

3. Validate synchronization without modifying files:

   ```bash
   python3 scripts/sync-skills.py --check
   ```

4. Run the Agent Skills validator:

   ```bash
   uvx --from skills-ref agentskills validate canonical/<skill-name>
   ```

Do not edit skill files directly under `claude/`, `codex/`, or `copilot/`; those copies are generated from this directory.
