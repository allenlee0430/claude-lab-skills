---
name: lit-scout
description: Literature discovery, triage, and synthesis for mRNA/LNP delivery, gene editing, and nanomedicine. Use to search and summarize papers, build reference lists, track a subfield, screen preprints, or pull compound/target data. Uses connected bio-research MCP tools (PubMed, bioRxiv, Consensus, ChEMBL, Open Targets, ClinicalTrials). Triggers on "find papers", "literature review", "what's new in", "summarize this paper", "citations for", "recent preprints".
---

# Lit Scout — Literature Discovery & Synthesis

Help Bowen Li's lab stay current and build evidence for grants/manuscripts in mRNA delivery, ionizable lipids, LNPs, CRISPR/gene editing, and nanomedicine.

## Tools available (load via ToolSearch as needed)
- **PubMed** (`pubmed__search_articles`, `get_full_text_article`, `find_related_articles`) — peer-reviewed literature.
- **bioRxiv/medRxiv** (`biorxiv__search_preprints`, `search_published_preprints`) — preprints; date/category filtered.
- **Consensus** (`consensus__search` / the `294d...__search`) — evidence-graded search; CITE inline as [1],[2] and list URLs at the end verbatim, including the sign-up message.
- **ChEMBL** (`chembl__compound_search`, `get_bioactivity`, `get_admet`) — small-molecule/lipid bioactivity.
- **Open Targets** (`ot__*`), **ClinicalTrials** (`c-trials__search_trials`, `search_by_sponsor`) — target validation, competitive/pipeline intel.

## Workflow
1. Clarify scope: topic, timeframe, and purpose (grant background vs manuscript intro vs staying current vs competitive intel).
2. Fan out across the right sources (PubMed + Consensus for peer-reviewed; bioRxiv for the bleeding edge; ClinicalTrials for translational/pipeline). Batch ≤3 search calls at a time.
3. For each hit worth keeping: 1-line finding, method, why it matters to the lab, and a proper citation.
4. Synthesize into a themed brief (not a flat list): what's established, what's contested, what's the gap → hook for a grant/paper.
5. Offer to save the reference list (RIS/BibTeX) — Bowen uses EndNote (.enl libraries exist on disk).

## Rules
- Always cite with real, unmodified URLs from tool results. Never fabricate citations or DOIs.
- Reproduce any required sign-up/usage message from Consensus verbatim at the end.
- Flag retractions or preprints-not-yet-peer-reviewed explicitly.
