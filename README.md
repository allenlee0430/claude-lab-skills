# Claude Skills for a Research Lab

This repository packages eight [Claude Code](https://docs.claude.com/en/docs/claude-code) skills for an mRNA / LNP / gene-editing research program. It is laid out so Claude can discover the skills directly from `.claude/skills/` when you open the repo.

## What's inside

| Skill | What it does | Legacy alias |
|---|---|---|
| `organize-research-files` | Safely audit, classify, and organize Desktop / Downloads with dry runs, manifests, and undo scripts. | `downloads-triage` |
| `draft-research-grants` | Draft funder-aligned grants, fellowships, and supporting application materials. | `grant-craft` |
| `revise-manuscripts` | Revise manuscripts, rebuttals, cover letters, and submission packages. | `manuscript-studio` |
| `scan-nanomedicine-literature` | Track and synthesize nanomedicine, LNP, RNA, and gene-editing literature. | `lit-scout` |
| `run-pi-operations` | Handle recurring PI and lab-management workflows. | `lab-pi-ops` |
| `build-reimbursement-packets` | Reconcile receipts, invoices, and expense evidence into reimbursement packets. | `reimburse-tracker` |
| `manage-research-portfolio` | Maintain a PI-level command view of deadlines, decisions, risks, and project status. | new |
| `design-lnp-experiments` | Design closed-loop LNP / RNA delivery design-make-test-learn cycles. | new |

## Install in Claude Code

Open this repository in Claude Code and it will discover the skills under `.claude/skills/` automatically.

If you want a global install instead, copy the skill folders into your personal skills directory:

```bash
mkdir -p ~/.claude/skills
cp -R .claude/skills/* ~/.claude/skills/
```

Restart Claude Code, or start a new session, after adding new skills.

## Notes

- The top-level skill folders remain as legacy mirrors for backward compatibility.
- `organize-research-files` uses a bundled script, so it resolves the script path through `CLAUDE_SKILL_DIR`.
- `scan-nanomedicine-literature` relies on connected research sources being available in Claude.

## License

MIT — see [LICENSE](LICENSE). Use, modify, and share freely.
