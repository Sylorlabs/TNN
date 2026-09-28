# H5 §12 Amendment (2026-09-23) — harness adaptive rule + item encoding

**Authority:** H5 program coordinator sign-off (amendment task, 2026-09-23).
DEPTH_DEF.md v1 and PREREG_H5.md v1 are **UNCHANGED** — spec v1 stands as
frozen. This amendment brings the harness into compliance with the frozen
spec and builds the missing input bridge. Per DEPTH_DEF §12: (a) coordinator
sign-off ✓ (this document's authority), (b) version bumps ✓
(`harness_v2/`, `encoding/` v1, `results_v2/`), (c) re-measurement of all
affected legs ✓ (the full matrix is re-run under this amendment; no
measurement was ever taken under the old rule, so nothing is invalidated).

## Background

Crew 5 (execution, commit `bca4caf32179fd6aec343738ad2981c302ebd770`)
verified every frozen input blob-for-blob and re-proved harness
determinism — but measurement was BLOCKED on two defects:

1. **Integration defect:** the frozen harness rejects all 877
   battery/red-team items (no `input.hypotheses`, no weighted evidence
   objects, ground truths outside the id charset, int-only JSON).
   `results/RESULTS_H5.md` §2.
2. **Rule defect:** the frozen harness's adaptive rule is not DEPTH_DEF
   §6 verbatim. `results/RESULTS_H5.md` §5 ("Secondary finding").

## Amendment 1 — adaptive rule brought to §6 verbatim

**Old rule** (`harness/dlb_delib.zag`, frozen): after round r, stop iff
`r ≥ adaptive_min_rounds`, `r ≥ stability_window`,
`confidence ≥ conf_threshold`, the leader is unchanged over the last
`stability_window` rounds, **and**
`margin[r] − margin[r−stability_window] < epsilon`
(cumulative margin gain over the window; a margin *drop* counts as settled).

**New rule** (`harness_v2/dlb_delib.zag`): per-round absolute confidence
gains `g_i = |c_i − c_{i−1}|` with `c_0 := c_1` (so `g_1 = 0`); after round
r, stop iff `r ≥ k` and `g_{r−k+1} … g_r` are **all** `< ε`; hard cap →
stop with cap recorded. Drops never count as settled (unanimous §2.3.4
finding: a confidence drop is deliberation at its most productive).
Earliest stop: round k = 3.

**Diff, precisely:**
- `dlb_stable()` (leader-stability helper): deleted — §6 has no
  leader-stability condition.
- The `mode==2` stop block: replaced. Old: min-rounds + conf-threshold +
  leader-stability + cumulative window margin-gain. New: cap check, then
  the §6 k-consecutive-`|gain|<ε` test over a new per-round confidence
  history arena `hist_c` (`c_0 := c_1` recorded at slot 0).
- `conf_threshold` / `stability_window` config keys: retained as required
  keys (format stability) but **ignored** by the §6 rule in v2; documented
  in `harness_v2/CONFIG_FORMAT_V2.md`.
- Ancillary (non-rule) addition: the ledger `VERDICT` detail now carries
  `cap=0/1` so the prereg §3 censoring check is directly auditable.
- Everything else (evidence mechanics, elimination, refutation test,
  confidence formula = clamped margin in thousandths, ledger chaining,
  record fields): byte-for-byte unchanged logic.
- Rebuilt with the pinned znc
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`);
  determinism re-proved byte-identical (see
  `harness_v2/DETERMINISM_V2.md`). New binary hash recorded there; the
  old binary hash is superseded, not deleted from history.

**Config values (frozen per prereg §1 / DEPTH_DEF §5 — the amendment uses
them, it does not change them):** `adaptive_min_rounds = 3` (= k, the
§6 window and earliest stop round), `adaptive_max_rounds = 16` (= cap =
`rounds_deep`, invariant enforced), `epsilon = 20` (= 0.02 in
thousandths), `rounds_shallow = 2`, `rounds_deep = 16`,
`elim_margin = 900`, `refute_threshold = 600`, `evidence_cap = 64`
(Phase-1 harness-frozen values, unchanged). Crew 5's `proposed/`
configs were never approved and are not used.

## Amendment 2 — frozen item encoding (input bridge)

`encoding/ITEM_ENCODING_SPEC.md` v1 (frozen with this amendment):
a mechanical, deterministic translation of the 877 frozen items into the
harness item format — hypotheses from structural fields, evidence as
weighted supports/attacks by fixed rules (fixed constants or fixed
scalings of payload numbers; never hand-authored per-item weights),
ground truths charset-mapped (mapping: `/`→`_`, space→`_`, verified
collision-free). Fidelity gates F1–F4 (100% GT re-derivation, 10%
independent spot re-derivation, 877/877 harness parse, 877/877
deep-16 convergence, 100% trap-gate pre-check) are part of the frozen
spec. Translated batteries: `items_v2/`.

**Recorded limitation (carried into RESULTS_H5.md v2):** the base
batteries (admit/revoke/logic) encode program verdicts the harness
cannot re-derive (gate policy text, kill-bar definitions, multi-step
logic inference are not mechanically recoverable); their curves measure
harness convergence, expected flat and high. The depth signal lives in
the trap battery (shallow answer wrong by construction); the cost
signal in the cost battery. The knee is read per-battery and pooled,
per prereg §3.

## What this amendment does NOT do

- Does not change DEPTH_DEF.md v1 or PREREG_H5.md v1 (no version bump
  needed on either; this file is the §12 record).
- Does not tune ε/k or any other parameter post-data (values are the
  prereg's frozen ones; the matrix runs after this commit).
- Does not alter the confidence formula (harness-frozen clamped margin),
  the record schema, or the ledger format beyond the `cap=` detail flag.
