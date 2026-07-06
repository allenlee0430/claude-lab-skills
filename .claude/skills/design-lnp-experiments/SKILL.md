---
name: design-lnp-experiments
description: Design and critique AI-assisted LNP and RNA-delivery design-make-test-learn cycles for Bowen Li's research program. Use for candidate-library design, formulation-space selection, assay planning, active-learning rounds, barcoded in-vivo screens, multi-objective optimization, translational criteria, go/no-go decisions, and connecting experimental results back to computational models.
---

# Design LNP experiments

1. Define the therapeutic objective, target cell or tissue, cargo, route, disease model, constraints, and decision the experiment must enable.
2. Specify the learning objective before choosing candidates. Distinguish exploitation, exploration, mechanism testing, and model calibration.
3. Define the design space: lipid structures, component identities, molar ratios, process variables, dose, and cargo attributes. Record hard chemical, formulation, safety, and manufacturing constraints.
4. Select controls, replication, randomization, batch strategy, blinding where relevant, and predefined success thresholds.
5. Choose readouts that separate delivery, expression or editing, cell viability, innate immunity, biodistribution, endosomal escape, and durability.
6. Plan data capture so every sample maps unambiguously to structure, formulation, process, batch, assay, and outcome.
7. For active learning, state acquisition strategy, uncertainty treatment, diversity constraints, retraining trigger, and stopping rule.
8. Produce a decision table and next-round logic before results exist. Surface biosafety, animal ethics, clinical, and manufacturability gates.
9. Do not fabricate prior results or assume an unpublished claim is validated. Cite current primary sources for external facts.

Read `references/dmtl-checklist.md` for the minimum closed-loop specification.
