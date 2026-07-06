---
name: organize-research-files
description: Audit, classify, and safely organize Bowen Li's Desktop, Downloads, and research-document folders using a numbered filing scheme with dry runs, move manifests, and undo scripts. Use when asked to clean up files, organize Desktop or Downloads, locate misfiled research documents, review ambiguous files, or repeat inbox-zero filing.
---

# Organize research files

Use `${CLAUDE_SKILL_DIR}/scripts/organize_files.py` for deterministic classification and reversible moves.

## Workflow

1. Run a dry run first:
   `python3 ${CLAUDE_SKILL_DIR}/scripts/organize_files.py ~/Desktop ~/Downloads`
2. Review counts and every proposed move. Treat personal, legal, financial, medical, unpublished, and partner-confidential files as sensitive.
3. Apply only when the user asked for organization:
   `python3 ${CLAUDE_SKILL_DIR}/scripts/organize_files.py ~/Desktop ~/Downloads --apply`
4. Verify that the category folders exist, loose files are gone, and manifests plus undo scripts were written.
5. Report moved counts, ambiguous files left for review, and exact undo paths.

## Rules

- Keep `00_Active_Now` untouched unless the user explicitly asks to archive it.
- Preserve project folders as units; do not scatter their internal contents.
- During second-pass auditing, move only high-confidence misclassifications.
- Never delete duplicates or installers automatically.
- Never move `60_Personal_Legal_Finance` into a synced or shared location without explicit approval.
- Prefer `90_Archive_To_Review` over a confident-looking guess.

Read `references/filing-scheme.md` when extending categories or classifier rules.
