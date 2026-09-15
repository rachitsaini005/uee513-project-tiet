# UEE513 — Electrical System Design

Laboratory and assignment work for **UEE513 (Electrical System Design)**,
B.E. Electrical Engineering, 6th Semester — Thapar Institute of Engineering
& Technology, Patiala.

**Author:** Rachit Saini (102304007), Subgroup 3D11
**Faculty:** Dr. Sourav Ganguli, EIED

## Contents

- **[`Report`](./UEE513_Report_102304007.pdf)** — full report covering:
  - Experiments 1–4 (EI-core inductor fabrication, buck-converter inductor design,
    single-phase transformer construction, 125 kVA transformer core/window design)
  - Laboratory Assignment 1 (transformer cooling-tube design; a Python transformer
    design program validated against A.K. Sawhney's worked example)
  - Laboratory Assignment 2 (separately-excited DC motor design, 3-phase induction
    motor design, PV boost converter with PI control)
  - Solved practice problems (quizzes and class tests)

- **`code/`** — the design/simulation programs referenced in the report:

  | File | Language | What it does |
  |---|---|---|
  | `transformer_design.py` | Python | Full transformer design (core → window → yoke → windings → losses/efficiency), following A.K. Sawhney's design-sheet method. Validated against a 25 kVA reference example. |
  | `buck_inductor_design.m` | MATLAB | Analytical design of a buck-converter inductor by the area-product method, including a core-family sweep (ETD29–ETD49) that trades core size against copper loss. |
  | `pv_boost_converter.m` | MATLAB | State-space averaged model, PI voltage-controller design, and switching-level simulation of a PV boost converter (24–40 V → 72 V). Requires the MATLAB Control System Toolbox (`ss`, `tf`, `margin`, `stepinfo`). |

## Running the code

**Python** (no dependencies beyond the standard library):
```bash
python3 code/transformer_design.py
```
It prompts for each design input interactively — the report's Section on Laboratory
Assignment 1, Q2 lists the exact input values used for the validation run.

**MATLAB:**
```matlab
run('code/buck_inductor_design.m')
run('code/pv_boost_converter.m')
```
Both run end-to-end with no user input required and print a full design summary
to the console, plus generate the plots shown in the report.

## Note on academic use

This repository documents coursework submitted for UEE513. If you're taking this
course yourself, please treat it as a worked reference rather than something to
submit as your own — check your institution's academic integrity policy before
reusing any of it directly.
