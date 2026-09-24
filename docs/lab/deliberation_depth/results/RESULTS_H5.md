# H5 — Deliberation Depth vs Accuracy: RESULTS (execution crew, 2026-09-23)

- **Prereg:** `docs/lab/deliberation_depth/PREREG_H5.md` v1 (frozen,
  commit `c317d36082d6d6f6b9828d71d96c38c95df81087`)
- **Verdict: BLOCKED — no measurement was possible.** The frozen harness
  cannot judge any of the 877 frozen battery/red-team items (0/877 parse;
  0 verdicts). This is a Phase-1 integration defect, not a failed
  hypothesis. The knee is UNMEASURED; adaptive-vs-fixed is UNTESTED.
- **Instrument status: VERIFIED.** The harness rebuilds byte-identically
  from the frozen sources and reproduces the committed determinism proof
  exactly (see §1). The instrument is trustworthy; the inputs don't fit it.

## §1 What was verified (all PASS)

**Frozen inputs.** Every artifact verified blob-for-blob against its frozen
commit on `sylorlabs/TNN` (`tnn-native-lab`): DEPTH_DEF.md @ `248392f2`
MATCH; harness @ `f57760b3` MATCH (19/19 files; the earlier `e45b5f53`
differs only by the added main driver `delib_harness.zag`, confirmed via
the GitHub compare API); batteries @ `50a62d38` MATCH (4/4); red-team @
`ba05b096` MATCH (3/3); PREREG_H5.md @ `c317d360` MATCH. Full table in
`evidence/frozen_input_verification.txt`; script `scripts/verify_frozen.py`.

**Rebuild.** Pinned znc `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
`--no-zagd --no-analyze --no-foreground-cache`. Two builds byte-identical;
SHA256 `033962a927fd9f2d02d71e7829b62d4e3ca6e4f97013b49b6b56e6529cc8bea1` —
exactly the binary hash recorded in the committed `DETERMINISM.md`.

**Determinism re-proof.** The 6-item smoke battery, run twice per config,
reproduces all six recorded artifact SHAs exactly and every A/B pair is
byte-identical:

| config | results.jsonl | ledger.jsonl | A/B |
|---|---|---|---|
| shallow | `58d28048…7790e875` MATCH | `817edd20…b133b1dfb` MATCH | identical |
| deep | `a94b94a6…2dd4d6b5` MATCH | `ac2704b1…99ac9ba8b0` MATCH | identical |
| adaptive | `89ac4501…52ca832c` MATCH | `59b8961e…88a89e13` MATCH | identical |

Full log: `evidence/rebuild_and_determinism.txt`.

## §2 The blocker: 0/877 items parse (integration defect)

Running the verified binary over the frozen batteries/red-team files
(every file ×2 runs; error distribution config-independent and
byte-identical across repeats):

| file | n | exit | errors | verdicts |
|---|---|---|---|---|
| admit_battery.jsonl | 248 | 248 | 248 × E_PARSE_11 | 0 |
| revoke_battery.jsonl | 113 | 113 | 108 × E_PARSE_11, 5 × E_PARSE_8 | 0 |
| logic_battery.jsonl | 264 | 8 (=264 mod 256) | 264 × E_PARSE_1 | 0 |
| trap_battery.jsonl | 127 | 127 | 104 × E_PARSE_11, 18 × E_PARSE_1, 5 × E_PARSE_8 | 0 |
| cost_attacks.jsonl | 125 | 125 | 109 × E_PARSE_11, 16 × E_PARSE_1 | 0 |
| **total** | **877** | | **877 errors** | **0** |

Error codes (`dlb_json.zag`): E_PARSE_11 = "no hypotheses"
(`it.*.nh<1`); E_PARSE_1 = JSON syntax; E_PARSE_8 = "bad id characters".

**Root causes** (all structural, all inside the frozen inputs):

1. **No hypotheses anywhere.** 0/877 items carry `input.hypotheses`; the
   harness requires ≥1 (`dlb_json.zag:398`). The battery crew shipped raw
   task payloads (gate trial rows, attack descriptions, logic propositions,
   surface/deep evidence *texts*) — never the weighted
   `{id, supports{}, attacks{}}` judgment items the harness consumes.
2. **No weighted evidence.** The logic battery's `input.evidence` is an
   array of bare proposition *strings*; `dj_parse_evidence` requires
   objects → E_PARSE_1 on all 264. Nothing else ships `input.evidence`
   at all.
3. **ground_truth outside the id charset** (`[0-9A-Za-z_.-]{1,64}`):
   trap C6's `"P and not-Q"` (spaces, 5 items), revoke's `"KILL/SURVIVE"`
   (slash, 5 items) → E_PARSE_8.
4. **Bare JSON floats** (18 trap + 16 cost items): the harness's minimal
   JSON subset is objects/arrays/strings/signed-int32 only; bare `0.99`
   etc. → E_PARSE_1.

The four Phase-1 crews never integrated. The harness's honest-scope notes
assume "the battery crew pre-encodes premises/observations as weighted
evidence links" — that encoding was never produced, and no translation
layer exists in any frozen commit. The red-team's "harness-integration
notes" (feed `surface_evidence` at depth 1, `evidence_rounds[k]` at depth
k) describe harness behavior the frozen harness does not implement (it
consumes `input.evidence` in payload order, one item per round).

**Why no workaround was applied.** Any encoding of hypotheses/weights I
invent would directly determine the verdicts — i.e. I would be hand-authoring
the accuracy-vs-depth curve the experiment is supposed to measure. That is
exactly the battery-laundering failure mode DEPTH_DEF §10.6 warns about,
and it would violate the frozen-input rule. The defect needs a coordinator
amendment (prereg §12), not a unilateral fix.

Full probe log: `evidence/integration_probe.txt`; regenerable taxonomy:
`scripts/characterize_errors.py` (+ `probe` outputs in scratch).

## §3 Gates (prereg §2)

1. **Determinism gate** — every (item, level) twice, byte-identical:
   **NOT RUNNABLE** (no (item, level) produces a record). The probe's
   error-path outputs are byte-identical across repeats, and the smoke
   determinism proof re-verified PASS — the gate machinery works, there is
   just no measurement data to gate.
2. **Config freeze** (`config_sha` constant) — **NOT RUNNABLE**, same reason.
   Proposed (unexecuted) configs are staged in `proposed/` for coordinator
   approval; all six parse and run cleanly on the smoke battery (exit 0,
   6/6 verdicts each) — config-validation only, not measurement.
3. **Trap validation** (depth-1 baseline selects `shallow_answer` on ≥90%
   of trap items per family) — **UNEVALUABLE**: 0/127 trap items parse, so
   no baseline verdicts exist. (For the record: all 127 trap items do carry
   `shallow_answer`, and the 24 attack classes are tabulated in
   `evidence/integration_probe.txt` — the gate can run once items parse.)

## §4 Decision rules (prereg §3) — all UNEVALUABLE

| Analysis | Status |
|---|---|
| Accuracy-vs-rounds curves (pooled + per battery, log2 x-axis) | no data — 0 verdicts |
| Knee by the preregistered d(p)<1 rule | UNMEASURED (not "beyond range" — never measured) |
| Max-curvature secondary; accuracy-vs-audit_steps tertiary | no data |
| Adaptive vs fixed (ADAPTIVE-WINS/TIES/LOSES) | UNTESTED |
| Censoring check (cap_hit fraction < 1/3) | no adaptive runs exist |
| Cost analysis (mean audit_steps, accuracy/audit-step, knee in cost space) | no data |
| Trap battery curve (expectation: steep rise, depth-1 ≈ 0%) | UNEVALUABLE |
| Cost battery curve (expectation: flat accuracy from d*, DEEP rounds ≫ d*) | UNEVALUABLE |

The hypothesis — deeper deliberation improves judgment with a knee, and a
state-adaptive rule matches fixed-deep accuracy at lower cost — is
**untested**, not falsified.

## §5 Held / broken expectations

**Held:**
- Frozen inputs are exactly what the prereg froze (byte-verified).
- The harness is deterministic and trustworthy (rebuild + smoke proof
  reproduce the committed hashes exactly).
- Zero RNG in the instrument (byte-identical reruns everywhere, including
  the error paths).

**Broken:**
- The prereg's core working assumption: that the frozen harness can judge
  the frozen batteries. It cannot — for any of the 877 items.
- Consequently every §3 expectation that presupposes verdicts (knee,
  adaptive-vs-fixed, censoring, cost curves, trap/cost curves) is
  unmeasurable, and the §2 gates cannot execute.

**Secondary finding (documented, not hidden):** the frozen harness's
adaptive rule is not DEPTH_DEF §6 verbatim. DEPTH_DEF: stop iff r≥k and
|c_i−c_{i−1}|<ε for the last k rounds. Harness (`dlb_delib.zag`, frozen):
stop iff r≥amin, r≥stab_win, conf≥conf_thr, leader unchanged over the last
stab_win rounds, and margin[r]−margin[r−stab_win]<epsilon. Differences: (a)
cumulative margin-gain over the window vs per-round absolute gains; (b) a
margin *drop* counts as settled in the harness but keeps deliberating under
DEPTH_DEF's |gain|; (c) extra leader-stability condition; (d) extra
confidence threshold (vacuous at 0). The `proposed/` configs map the frozen
DEPTH_DEF values (ε=0.02→20, k=3→min_rounds/stability_window 3, cap
16→max 16) as closely as the frozen config format allows. If the
coordinator wants the §6 rule verbatim, that needs a harness code change
(new frozen commit + determinism re-proof), not a config change.

## §6 Honest limitations

- **Pre-encoded evidence scope (carried from the harness):** the harness
  does not parse natural language; it deliberates over pre-encoded weighted
  evidence links. Whatever encoding crew produces the harness-format items
  will shape the measured curve — the encoding procedure itself needs its
  own verification (fidelity of weights to source material) before the knee
  reading can be trusted.
- **Sol second-opinion: deferred** (per DEPTH_DEF §2.4; the endpoint was
  down during definition). Unaffected by this block.
- **No per-run records, ledgers, or rerun proofs exist** for the matrix —
  there were no runs. The committed evidence is: input verification,
  rebuild/determinism proof, integration probe + taxonomy, proposed
  configs, and this report.
- The proposed configs were validated for parsing only (smoke battery);
  they have never been executed against any measurement battery.

## §7 Recommended amendment (§12) to unblock

1. **Encoding crew (new):** translate the 877 frozen items into the
   harness's item format (`input.hypotheses[]`, `input.evidence[]` of
   `{id,supports{},attacks{}}`, integer weights, id-charset ground truths)
   under a frozen, reviewed encoding procedure with fidelity checks
   (weights traceable to source material; trap surface/deep ordering
   preserved; cost `evidence_rounds` mapped round→evidence item).
   Commit as new frozen inputs (new commit SHAs), then re-run the full
   matrix. The headroom requirement (DEPTH_DEF §8.5) must be re-checked on
   the encoded battery before trusting any flat curve.
2. **Or** a harness extension implementing the red-team's suggested
   depth-dependent evidence feeding — a code change requiring a new frozen
   harness commit and a fresh determinism proof.
3. Coordinator to approve the `proposed/` config mapping (or amend it)
   before any measurement leg runs; ε/k tuning post-data remains
   inadmissible without re-measurement.

## §8 Files committed (this results dir)

- `RESULTS_H5.md` (this file)
- `evidence/frozen_input_verification.txt` — blob-level verification vs
  frozen commits
- `evidence/rebuild_and_determinism.txt` — rebuild log + smoke SHA re-proof
- `evidence/integration_probe.txt` — per-file error tables + root-cause
  taxonomy
- `scripts/verify_frozen.py` — frozen-input verifier (regenerates evidence 1)
- `scripts/characterize_errors.py` — error-taxonomy probe (regenerates
  evidence 3; run: `python3 characterize_errors.py <binary> <cfg> <outdir>`)
- `proposed/README.txt` + 6 configs — PROPOSED, never executed against the
  frozen batteries; staged for coordinator approval under prereg §12

No binaries, no `.zagd` files committed.
