# Claude Skills for a Research Lab (mRNA / LNP / Gene Editing)

A collection of six [Claude Code](https://docs.claude.com/en/docs/claude-code) **Skills** built for running an academic research lab — grant writing, manuscript revision, literature scouting, file organization, reimbursement tracking, and day-to-day PI operations. They were built for an mRNA / lipid-nanoparticle (LNP) delivery lab but are easy to adapt to any research group.

## What's inside

| Skill | What it does |
|-------|--------------|
| **grant-craft** | Draft, revise, and assemble grant applications (CIHR, NSERC, CFF, CDMRP/DoD, CFI, OICR, fellowships) — aims, significance/innovation, budgets, lay abstracts, response-to-review. |
| **manuscript-studio** | Draft & revise manuscripts, point-by-point reviewer rebuttals, and cover letters for Nature / Cell Press / ACS / Molecular Therapy. |
| **lit-scout** | Literature discovery & synthesis via connected research MCP tools (PubMed, bioRxiv, Consensus, ChEMBL, Open Targets, ClinicalTrials). |
| **downloads-triage** | Sort a messy `~/Downloads` / Desktop into a consistent numbered filing scheme. Ships with a reversible Python classifier. |
| **reimburse-tracker** | Turn receipt/invoice PDFs into a reimbursement spreadsheet + merged packet, with PO matching and grant-expenditure reporting. |
| **lab-pi-ops** | Recurring PI tasks: group-meeting decks, weekly trainee updates, recommendation letters, teaching materials, committee prep. |

## Install

Skills live in `~/.claude/skills/`. To install all six:

```bash
git clone https://github.com/allenlee0430/allenlee-lab-skills.git /tmp/lab-skills
mkdir -p ~/.claude/skills
cp -R /tmp/lab-skills/grant-craft \
      /tmp/lab-skills/manuscript-studio \
      /tmp/lab-skills/lit-scout \
      /tmp/lab-skills/downloads-triage \
      /tmp/lab-skills/reimburse-tracker \
      /tmp/lab-skills/lab-pi-ops \
      ~/.claude/skills/
```

Or install just one:

```bash
cp -R /tmp/lab-skills/grant-craft ~/.claude/skills/
```

Restart Claude Code (or start a new session). Each skill auto-activates when your request matches its description, or invoke it explicitly with `/grant-craft`, `/lit-scout`, etc.

## Customize for your own lab

Each `SKILL.md` contains a research-context block with a specific name, institution, funders, and research focus. **Search-and-replace those with your own details** so the skills speak to your work:

- Lab name / PI name / institution
- Target journals and funders
- Research keywords (used by `lit-scout` and `downloads-triage`'s classifier)

The `downloads-triage/organize.py` classifier is keyword-driven — edit the keyword lists in `cat_for()` to match your document types.

## Notes

- `lit-scout` relies on research MCP servers (PubMed, bioRxiv, Consensus, etc.) being connected in your Claude environment.
- `downloads-triage` always dry-runs first and writes an undo script — nothing is deleted, only moved.
- Writing skills pair well with the community `humanizer` skill to strip AI-generated tells from final prose.

## License

MIT — see [LICENSE](LICENSE). Use, modify, and share freely.
