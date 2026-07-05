---
name: downloads-triage
description: Sort and file loose documents in ~/Downloads (and Desktop) into Bowen Li's numbered filing scheme. Use to repeat the auto-organization, file new arrivals, find a misfiled document, or clean up. Triggers on "organize my downloads", "clean up files", "sort my desktop", "file these", "where did X go".
---

# Downloads Triage — Repeatable Filing

Keeps `~/Downloads` and `~/Desktop` sorted into one consistent scheme so nothing is ever lost in a 2,000-file pile again.

## The filing scheme (same on Desktop and Downloads)
| Folder | Contents |
|--------|----------|
| `10_Research_Manuscripts` | papers, drafts, reviews, figures, SI, reviewer comments |
| `20_Grants_Awards` | grant apps, LOIs, budgets, fellowships, awards, calls-for-proposals |
| `30_Presentations` | slide decks (.pptx/.key) |
| `40_Data_Protocols_Images` | data, screenshots, images, protocols, raw exports, spreadsheets, zips |
| `50_Lab_Admin_Procurement` | invoices, quotes, POs, receipts, reimbursements |
| `60_Personal_Legal_Finance` | visa, PR, SIN, passport, tax, insurance, medical, personal IDs |
| `70_Code_Automation` | scripts, notebooks, .tex, .cdxml |
| `80_Software_Installers` | .dmg/.pkg/.app installers |
| `90_Archive_To_Review` | ambiguous / needs human eyes |

## How to run
1. The classifier script lives at `~/.claude/skills/downloads-triage/organize.py`. It classifies by filename keyword + extension, checking sensitive/personal first.
2. **Always dry-run first**: `python3 organize.py` (prints counts + samples, moves nothing).
3. Apply: `python3 organize.py --apply` — creates category folders, moves items, writes `_ORGANIZE_MANIFEST.csv` and `_UNDO.sh` for full reversibility.
4. To undo: `bash ~/Downloads/_UNDO.sh`.
5. Point it at a different folder by editing the `DL` path, or extend keyword lists in `cat_for()` as new document types appear.

## Rules
- Never move items in `60_Personal_Legal_Finance` to a shared or synced location without asking — these contain SIN, passport, visa, and medical data.
- Preserve existing project subfolders (move them whole; don't scatter their contents).
- When unsure, send to `90_Archive_To_Review` rather than guessing into a specific bucket.
