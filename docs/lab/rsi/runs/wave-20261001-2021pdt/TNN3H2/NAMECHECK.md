# NAMECHECK: TNN3H2 (H2 prereg: writing only)

Lane: TNN3H2, wave-20261001-2021pdt. Task: write PREREG_H2.md (fresh prereg for H2, learner-asserted derivation direction) with mandatory substrate verification. No implementation, no computation, no binaries.

## Step 0: Worker toolchain guard (Micah's governance ruling, 2026-09-30)

- Safebin setup: ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh` at wave start. Result: SAFEBIN-READY, `/home/hatch/safebin`, 36 tools linked, znc OK, setup script self-verified python3 absent from safebin PATH.
- PATH during all work: `/home/hatch/safebin` (exported in every exec call; exec sessions do not persist env between calls, so each command re-exports).
- Toolchain verification: `export PATH="$HOME/safebin"; which python3` prints NOTHING (exit 1). `which python` prints NOTHING (exit 1). Guard satisfied.
- PURE ZAG observed trivially: this lane is WRITING ONLY. No implementation files written, no znc invocations, no computational research operations performed. The only shell use is git status reads, file greps on source docs, and SHA-256 verification of the frozen build (read-only inspection).

## Step 1: Identity and scope

- Worker is a research worker for the TNN RSI loop wave wave-20261001-2021pdt, lane TNN3H2.
- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab (confirmed via git).
- Write ONLY inside docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H2/. New files only: NAMECHECK.md (this file), PREREG_H2.md. No implementation files. No commits (coordinator commits). Never push. No git reset --hard, no rebase.

## Step 2: Hypothesis grounding

- H2 read directly from docs/lab/rsi/runs/wave-20261001-1721pdt/TNN3/HYPOTHESES.md (section "H2. Learner-asserted derivation direction (invertible learner links)"): learner may assert derivation links in either direction over structures it created, including cells whose guard tests an output slot and whose set writes an input slot; inversion becomes a construction the learner expresses with the generic LINK affordance; forward-only assumption deleted from the assemblers; generic LINK operation no longer direction-restricted by researcher code; capability-source delta net negative (deletion only, zero lines added).
- H1 context: H1 was KILLED this wave by sealed evaluation (zero learner-created names) and an independent red team rendered a presentation-level FABRICATION verdict (REDTEAM_FABRICATION.md, TNN3H1 lane) plus a confirmed PREREG-DESIGN FAILURE: PREREG_H1.md asserted a naming affordance (tag 904, NAME edges) never verified against the frozen substrate while freezing a "0 added lines" deletion plan; the frozen tnn2.zag never contained the affordance, so the test was vacuous and the builder's dev harness constructed the signature it then verified. Lesson carried into this lane: PREREG_H2.md must verify its substrate (LINK operation existence and forward-only restriction) against the frozen tnn2.zag BEFORE freezing bars, or the prereg is VOID.
- Frozen substrate: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag, expected SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd (hash to be verified by the worker, not trusted from this file).

## Step 3: Deliverables

- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H2/NAMECHECK.md (this file)
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H2/PREREG_H2.md (frozen prereg with substrate verification section 2, frozen kill bars, sealed family requirements, three-valued verdict rule, architecture bars)
- Final report to parent: substrate verification result with quoted evidence, and the frozen bar list.

## Step 4: Documentation rule

- No em-dashes anywhere in lane documentation.
