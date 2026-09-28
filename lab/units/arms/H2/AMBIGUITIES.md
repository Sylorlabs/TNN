# H2 AMBIGUITIES.md — recorded, not reinterpreted

All ambiguities encountered during the H2 continuation (attempt 2, 2026-09-21).
Each is documented with the choice taken and why. Nothing here changes a frozen
rule; rule changes need Micah's re-approval.

## A1. Kill wording: "reuse advantage" vs "reuse hit rate"

The H2 binding kill says "reuse advantage over baseline < 5 absolute points".
H1's corresponding text says "reuse hit rate". M7 therefore treats the
**hit-rate advantage** (H2 hit rate − fixed-64B baseline hit rate) as the
primary prong-1 metric, and reports the ID-stable reuse advantage
(H2 ID-stable reuse − baseline ID-stable reuse) as a companion.
Both are computed on both corpora; neither interpretation is tripped
(prose +80.4 / code +74.9 hit-rate points; +84.4 ID-stable both).

## A2. Kill scope: "both corpora" vs "either corpus"

The kill does not say whether "reuse advantage < 5" must hold on both
corpora jointly or on either corpus alone. M7 reports both:
`m7_h2_kill_reuse_both` (kill iff BOTH corpora < +5, matching the existing
`kill_all` convention) and `m7_h2_kill_reuse_either` (stricter: kill iff
EITHER corpus < +5). Neither is tripped. No silent choice was made.

## A3. Boundary fidelity is not independently measured

`h2_verify` recalls each unit through its recorded (offset,length) span and
byte-compares against the source corpus. A wrong recorded span would fail the
byte comparison, so boundary fidelity is folded into the same pass/fail as
content recall. M1 reports `m1_boundary_tenths` equal to `m1_recall_tenths`
(100.0/100.0). This is a measurement-scope note, not a separate bar.

## A4. Which r1 corpus round

Two r1 rounds exist on disk: `~/workspace/tnn-lab/corpora/r1/` (prose
5,638,480 B) and `units/arms/harness/corpora/r1/` (prose 5,422,721 B).
The H2 1x battery uses `~/workspace/tnn-lab/corpora/r1/`, consistent with the
on-disk state of this continuation (prior H2 crew's tinytest used the 5.6 MB
pg100) and with that round's MANIFEST carrying the §6 `sep10_format` for 10x.
The choice is recorded; results are round-scoped.

## A5. 10x construction conflict (not exercised)

Frozen §6: "10x = 10× the corpus by concatenation with deterministic
separators". Harness CORPORA.md: 10x = verbatim 10-fold tiling, "no tags or
markers" (and `build_10x.py` implements verbatim tiling). These conflict.
The 10x leg was NOT run: the binding kill tripped at 1x, and the protocol
gates 10x on every 1x bar passing. If a 10x leg is ever ordered, the
separator-vs-verbatim construction must be resolved first (recommend §6,
the frozen prereg, over the harness doc).

## A6. Corpus A / corpus B naming

Corpus A = prose (Shakespeare), corpus B = code (sqlite3.c), per the H2
declaration text: "budget starvation on complex windows (code with dense
structure) — predicts H2's fallback rate spikes on corpus B vs corpus A".

## A7. `t_m5baseline` is dead code

`t_m5baseline` (empty-slot-table RSS baseline, b64 precedent) exists in
`cl/arm.zag` but is never called by the dispatcher (`m5-1x` dispatches only
`t_m5`). The M5 bars (≤1.5× source bytes; ≤10 audit entries/KB) are measured
directly by `t_m5` and pass (0.42×; 4.7/KB). The baseline comparison was not
exercised. Not rebuilt mid-battery to fix: no bar depends on it.

## A8. M8 starve / freelist-rev perturbations

The arm performs no entropy/clock reads anywhere (verified by source
inspection: no RNG, no time syscalls in any AI decision path or harness
path), so the `starve` perturbation is accepted and documented as a provable
no-op. Slot placement (`h2_alloc_slot`) is a pure function of chunk ID with
deterministic tie-breaks (lowest free index; weakest-strength eviction,
ties → lowest index), so `freelist-rev` is likewise a documented no-op.
Both still run as full M8 regimes with byte-identical artifact comparison.

## A9. M9 learning-curve learner

M9 (learning curve / time-to-mastery) uses `h2_learn` (cutting-mode segmenter
+ strengthen path) as the learner under test. This is a deliberate harness
choice documented in the source; the reported shape (fast-then-flat,
takeoff ep 1, 100.0 steepness) is scoped to that choice.

## A10. ID-remap probe is PROVISIONAL-PENDING-FREEZE

The M1 64-unit ID swap probe passes 64/64, but ID semantics belong to the
pending ID arm freeze; the probe is reported as provisional, not as a bar.

## A11. The fallback-rate kill is tautological under frozen B=8/C=16

With C=16 selected candidates and B=8 evaluations per window, the budget
binds in EVERY window with ≥9 evaluable candidates. On dense corpora
(prose/code) that is ~100% of windows (measured: 100.0% prose, 99.9% code;
exactly 8.0 bulk-refused per fallback window). The >40% kill bar is therefore
tripped by construction of the frozen parameters, not by an empirical
surprise. The verdict applies the kill mechanically (it is binding), but
records that the parameter pair — not the deliberation's quality — is what
fails. Any change to B, C, or the kill bar needs Micah's re-approval.

## A12. "Windows" denominator

Fallback rate = `m1_fallback_win / m1_windows`, where `m1_windows` counts
every `h2_window` call including the final partial window
(prose 1377 = ⌈5638480/4096⌉; code 2324 = ⌈9515341/4096⌉). Literal reading
of "> 40% of windows".
