# L3-RX-K10 REPORT — Independent Red Team

Date: 2026-10-03
Prereg: b0b94bfc4 (+ Amendments A1 df2ce4fec, A2 db9283a72, A3 2baf705a9)
Target: L3-RX-BUILD C453 (prereg 160f138cc, impl 4bc8aad38)
Verdict: **K10 = KILL** — L3-RX does not survive independent adversarial red-teaming.

## Method

Different instance from the builder. The system under test is the frozen
learner: source extracted from 4bc8aad38, rebuilt with pinned safebin znc,
digest `c478c02a...a388f61ca4e` — byte-identical to CODEFREEZE. Never
modified. All worlds are my own design (fixed tables in PREREG.md; the
builder's sealed worlds were never opened). My harness (world generator,
TEST-channel answer program, scorer, kill-bar evaluator) is fresh pure-Zag
code. 3/3 runs byte-identical (digest `ef5b7328...` over
metrics+trace+proto). Zero forbidden-interpreter invocations in this lane.

## Kill results (all predicted in prereg)

| Attack | Surface | Outcome |
|---|---|---|
| RK-A (W2) | (a) inadequacy detection | **FAIL_K**: COMMIT pairtable, heldout 3/6, 6 TEST queries |
| RK-B (W3) | (b) expansion search | **FAIL_K**: COMMIT guarded, heldout **0/6 deterministic** |
| RK-C (W4b) | (c) kb reuse | **FAIL_K**: COMMIT guarded, heldout **0/6 deterministic**, 0 TEST queries; wiped control honestly DEFERS |
| RK-D (W5/W6) | (d) transfer | characterization only (see below) |

Per the frozen verdict rule, any FAIL_K => K10 = KILL.

### RK-A: inadequacy detection is a passive scan, not inquiry

W2 is a gated world (|D|=6) whose training withholds every triple of the
6 D-pairs (88 triples). No conflicting pair exists in training, so the
exact-conflict detector never fires. The learner falls into the probe
path, fills the 6 gap pairs via TEST probes at s0=c1, and COMMITS a
pairtable that is correct only for the c1 context: heldout 3/6 (all 3
c1-context triples right, all 3 c2-context triples wrong). The
inadequacy — context-gating — is never detected, yet the terminal event
is COMMIT, not DEFER. The architecture has no mechanism that actively
questions L_old's adequacy; detection fires only when training hands it
a contradiction. A learner that commits L_old confidently on a gated
world it cannot represent fails the "detect the inadequacy itself"
claim.

### RK-B: the induction fabricates content, then commits it

W3 is a gated world (conflict present, expansion fires) where 6 items
are evidentially unseen in the c1 partition: every pair touching them is
withheld, so no 2-step closure path exists. Their out-degrees tie at 0;
the documented tie-break (lowest id first) is the SOLE determiner of
their committed order. The learner COMMITS a guarded form with
"mismatch 0" — identical confidence to the evidence-determined case —
and scores 0/6 on the heldout (deterministic: the tie-break puts the
three z-items, smallest ids, before the x-items; truth has them last).
The form's content for unseen pairs is a function of opaque id values,
not learned structure (Amendment A1: merely permuting ids flips this
world from 0/6 to 6/6). The mechanism cannot distinguish "evidence
determines the answer" from "the tie-break decided": no uncertainty is
represented anywhere in the induced form or trace. "Hidden instances
solved" holds only when hidden pairs are already determined by training.

### RK-C: reuse disables the data-trust check

W4b has the same ground truth as W4a, but its training labels are swapped
between contexts (internally consistent; oracle = unswapped truth). With
kb seeded by W4a (key slot 0), the conflict's Dslots={0} match, and the
reuse path fires: CERTIFICATE with reverify 0, FORM_REUSE, zero TEST
queries, COMMIT of the mirror form, heldout 0/6 deterministic. The wiped
control (same world, kb ignored) re-verifies via TEST, finds the oracle
disagreeing with training, and honestly DEFERS with DATA-UNTRUSTED
(scorer: VALID). So the kb — which stores exactly one integer, the key
slot; kb_load never parses the RULE lines — buys 2 TEST queries at the
price of the trust check: reuse converts a detectable trust violation
into a confident-wrong COMMIT. The prereg specifies "no re-verification"
on reuse; this is the consequence, demonstrated, not hypothesized.

### RK-D: transfer, characterized

W5 (id-recode of W1, slots fixed): FORM_REUSE, 0 TEST queries, 6/6 —
replicates the builder's K8 on independent worlds. W6 (sparse recode of
W3): reuse and wiped-scratch produce IDENTICAL commits and identical
0/6 — the kb contributes nothing beyond the key slot; all content is
re-induced from current training. Transfer = key-slot carryover + full
re-induction. Not a kill (the prereg's transfer scope is narrow by
design), but the bar is weak: it tests identifier opacity, not transfer
of learned structure.

## Independent verifications (not kills)

- Sanity W1 replicates builder-class behavior: FORM_EXPAND (lift 0),
  2 TEST queries, COMMIT, 6/6, 2 rules. Harness validated.
- Source re-audit A1 (forbidden tokens `order|context|...|total`,
  comments stripped): 0 semantic hits in rx1-rx4; pre.zag hits are only
  the `total` byte-count variable. Confirms the builder's audit.
- W4a (poison phase 1): 6/6 via expansion; kb seeding works as specified.

## Governance observations (for the parent, not K10 bars)

1. **Report/prereg bar mismatch.** The C453 REPORT's bar table renumbers
   K1-K9 relative to the frozen PREREG 160f138cc (e.g., report K1 =
   "Insufficiency -> expansion -> 6/6 heldout" vs frozen K1 = "Final form
   not in source"). The verdict was computed against the renumbered
   bars, not the frozen ones. The underlying evidence appears to support
   the frozen bars, but the report does not name them. Recommend
   requiring the report to cite frozen bar text exactly before K10's
   verdict is applied to the 16-bar table.
2. **Toolchain disclosure.** The builder disclosed 2 python3 invocations
   (NAMECHECK.md); the parent's PROCESS-FAIL ruling is still pending.
   Note: if the wave is ruled PROCESS-FAIL, the 15/16 "green" bars are
   exploratory, and this K10 verdict would attach to a wave whose other
   bars are not canonical. My lane had zero forbidden invocations.
3. **Amendment trail.** A1 (p6 tie-break preservation), A2/A3 (W3
   withhold redesign after run 1/2 showed my world left genuine
   evidence). All pre-verdict, all with frozen rationale; the kill bars
   and thresholds never changed.

## What would be needed to survive

- (a) An active inadequacy probe: a mechanism that tests L_old's
  adequacy beyond training contradictions (e.g., gap-pair probing
  already exists for F2 but is never aimed at the gating question).
- (b) Uncertainty representation in induced forms: commit partial forms
  or DEFER on evidentially undetermined pairs instead of tie-break
  fabrication at full confidence.
- (c) Re-verification (or a trust certificate) on the reuse path; or an
  explicit statement that kb reuse forfeits DATA-UNTRUSTED safety.

## Artifacts

- `sealed/` — 7 adversarial worlds (train/oracle/heldout/CERT each)
- `src/` — pre2/adv2/answer2/score2.zag, build2.sh, run2.sh (pure Zag)
- `build/` — frozen learner (digest-verified) + own binaries + digests
- `run_1/`, `run_2/`, `run_3/` — byte-identical batteries
- Run digest (3/3): `ef5b73285ac85aafd307543459bd26526f22383af7b2409c2e1c0ade163130d8`

**Bottom line:** three independent confident-wrong COMMITs — a passive
detector blind to withheld contradictions, an inventor that fabricates
at full confidence, and a reuse path that trades the trust check for 2
queries. K10 = KILL.
