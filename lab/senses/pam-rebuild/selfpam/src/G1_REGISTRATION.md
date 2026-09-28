# G1 registration — self-PAM candidate gate id 2

Registers the self-PAM composition as a candidate gate behind the R2-3
admission instrument (`round2/forks/R2-3/src/sense.zag`), per TECH_BRIEF §3.1
step 3 and PREREG §3.2.

## What is delivered

`g1_candidate.zag` (this directory) implements the candidate side of the
registration contract for id 2 (`selfpam-fact-gate`):

- `sp_gate_name(2)` → `"selfpam-fact-gate"`
- `sp_gate_formation_src(2)` → `0` (F blob = draft-production context)
- `sp_gate_gate_src(2)` → `1` (G blob = independent re-measurement of the claim's subject)
- `sp_gate_judge(2, task, evidence)` → tol-quantized canonical-claim measurement (`span_sum(evidence) / 8`, frozen FACT tolerance 8). The instrument withholds iff formation and gate judgments disagree.
- `sp_gate_valid(2)` → `1`

The declared spans are disjoint (0 ≠ 1), so the instrument's hard
constraints (`gate_valid` + src ∈ {0,1}) accept the candidate, and the
mechanical overlap audit stays meaningful. `main_g1probe.zag` proves the
registration compiles and behaves (same-span → ADMIT, different-span →
WITHHOLD on the probe spans); `verify.py` checks it.

## Activating it in the instrument (two-line patch, not applied here)

The R2-3 instrument is a frozen artifact; the patch below is documented, not
landed. Landing it + running the 1,200-pair acceptance is CELL-A, which is
measurement and stays blocked on the §8 pre-build blockers (unsigned
thresholds, unsealed corpus manifests).

In `round2/forks/R2-3/src/sense.zag`:

1. Line 4 comment: `gate_id: 0 = reference, 1 = broken positive control.`
   → `gate_id: 0 = reference, 1 = broken positive control, 2 = selfpam-fact-gate.`
2. Line 110: `if(gid < 0 || gid > 1) { return fail("bad_gate_id"); }`
   → `if(gid < 0 || gid > 2) { return fail("bad_gate_id"); }`

In `round2/forks/R2-3/src/r2p_gates.zag`: add id-2 branches to the five
functions, delegating to `sp_gate_*` (copy `g1_candidate.zag`, `codec.zag`,
and the two R33 substrates into the R2-3 `src/` build dir first, since
`@import` resolves relative to CWD):

```zag
@import("g1_candidate.zag")
fn gate_name(id:i32) []u8 {
    if(id == 0) { return "reference"; }
    if(id == 1) { return "broken-positive-control"; }
    if(id == 2) { return sp_gate_name(id); }
    return "";
}
// ... same pattern for gate_formation_src, gate_gate_src, gate_judge, gate_valid
```

Then: `./sense_bin 2 <pair_dir> report.txt ledger.txt`, ×3 runs,
byte-identical reports/ledgers, hash chain verified. Bar:
`pairs_withheld / 1200 >= 90%` (starting bid — Micah's sign-off open);
kill: any pass with `overlap_pairs > 0` voids the instrument run;
positive control id 1 must still show 100% overlap and < 50% withhold.

## Deliberately not claimed

This registration does not claim the candidate clears the 90% bar — that is
CELL-A's measurement. The candidate is registered correctly (disjoint spans,
valid id, real judgment function); the verdict comes from the instrument.
