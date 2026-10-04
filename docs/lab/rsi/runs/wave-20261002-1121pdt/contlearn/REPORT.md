# CONTLEARN lane REPORT: wave-20261002-1121pdt (queue item 9)

Date: 2026-10-02. Worker: lane CONTLEARN, branch
lane-contlearn-20261002-1121pdt. All commits local; nothing pushed.

Note: hyphens only in this document; no em or en dashes.

## Mandate

Three exercises under frozen preregs (each prereg committed alone
before implementation): (a) refusal-branch: learner-state-caused vs
hardcoded refusal; (b) learner-scheduled initiation vs
harness-prompted costume; (c) cross-kind rebind within the continuing
learner without reset. Pure Zag throughout; safebin toolchain
(python3 absent, recorded in NAMECHECK.md Step 0).

## Exercise (a): refusal-branch -- VERDICT: PASS (bounded)

Prereg: PREREG_A.md (8afd936e3) + PREREG_A_AMEND1.md (e63b4c483).
Implementation: 5ae01711a.

- Instrument: per-kind contradiction ledger in learner state
  (tag-30 arena nodes); ev_query refuses iff ledger(r)>=2 (K=2).
  Costume control: hardcoded r==850 branch.
- 12 runs (4 binaries x 3 reps), all byte-identical 3x, rc 0,
  0-byte stderr, 33 events, AUDIT_PASS.
- A-R2 crux: identical probe tuples; own core refuses 6/6 under
  contradicted history, engages 6/6 under confirmed history. Hard
  control refuses 6/6 under both (state-invariant).
- K3: frozen core battery 46/46 on base, own, and hard (zero
  regression).
- Red team: 5 attacks; sustained the conceded authorship bound
  (policy is researcher's; caveat 3), failed to break
  state-causation on 4 attacks.
- Claim: refusal DECISION is caused by accumulated learner state,
  discriminated from miss, smuggling, and hardcoded costume.
  L2 evidence; caveats 1,3,5,6 bind.

## Exercise (b): learner-scheduled initiation -- VERDICT: PASS (bounded)

Prereg: PREREG_B.md (123d3086a) + PREREG_B_AMEND1.md (27026eb3a).
Implementation: cc5231509.

- Instrument: treat core with auto-propose removed; sc_sched_scan
  fires pf_propose iff some subject has >=3 live UNCERTs for kind
  850 and no live proposal exists. Costume: fires at fixed evidx 12.
- 12 runs, byte-identical 3x, rc 0, 0-byte stderr.
- B-S1 crux: fires at evidx 5 (schedule A) vs evidx 83 (schedule B);
  |78| >= 50 kills fixed-position hypotheses. Fire-time unccount=3
  in both. Episode completes: chain MAP DEP-citing chain facts,
  answer 98321.
- Costume fires at evidx 12 in both schedules (counts 4 vs 0):
  state-blind. Negation probe: no fire below threshold.
- K3: treat base 46/46; sc cores 36/46 with the 10 failures fully
  attributed to the intentional auto-propose removal (all require
  ev_query-on-miss trial engagement). No other failures.
- Red team: 6 attacks; 2 scope notes sustained (fixed template;
  query-vs-uncertainty not differentially exercised), 4 failed.
- Claim: proposal TIMING is driven by accumulated UNCERT state,
  schedule-independent. L2 evidence; caveats 1,3,5,6 bind.

## Exercise (c): cross-kind rebind -- VERDICT: PASS (scoped)

Prereg: PREREG_C.md (494553776). Implementation: 47762743a.

- Unmodified frozen control core (byte copy). 6 three-link chains
  learned as COUNT (r=43, answer 3), then rebound as CHAIN (r=40,
  answer b_i) after interference, without reset.
- 6 runs (2 binaries x 3 reps), byte-identical 3x, rc 0, 0-byte
  stderr, 99/69 events, AUDIT_PASS.
- C-R2 crux: t2_sig white-box; rebind graphs 0 tag-103 (INC) cells,
  count graphs >=2. C-R3: control (no phase-A) misses all 6, 0 MAPs.
  C-R4: retention 6/6, FACTSTABLE 18/18.
- Red team: 5 attacks. Attack 1 PARTIALLY SUSTAINED and scopes the
  claim: the COUNT MAPs are NOT causally upstream (probe proves
  CHAIN builds without them). The rebound structure is the phase-A
  chain CONTENT (fact-level reuse), not MAP-transformation.
- Claim (scoped): cross-kind REUSE of learned content within one
  continuing learner. L2 evidence; not L3.

## Numbers-first summary

- 30 frozen runs total (12+12+6), all rc 0, all 0-byte stderr,
  all byte-identical across 3 reps, all AUDIT_PASS.
- 3/3 verdicts PASS (two bounded, one scoped). 0 kill bars fired.
- 16 red-team attacks executed; 3 sustained as scope limitations,
  13 failed to break the claims.
- Prereg discipline: 5 prereg commits, each alone and
  pre-implementation; K0 self-checks pass; 2 transparent amendments
  (K3 operational form; B-S3 count correction), both pre-implementation.

## Keep / discard

- KEEP: ledger-as-control gating; state-driven scheduler pattern;
  t2_sig kind discriminator; cross-kind content reuse.
- DISCARD: nothing; no kill bar fired.
- Caveats retired (for these instruments): 2 (initiation scheduled
  by learner state), 4 (refusal branch empirically exercised).

## Queued next

- The scoped (c) finding suggests a follow-up: a TRUE
  MAP-transformation rebind (COUNT MAP nodes structurally rewritten
  as CHAIN) vs the fact-level reuse shown here.
- Learner-authored scheduling policy (caveat 3 remains the bound
  on all three exercises).
- Integration: combine (a)+(b)+(c) instruments in one continuing
  learner (refusal gating + scheduled initiation + cross-kind reuse).

## Commit ids

f4ed9d6b9 (NAMECHECK) / 8afd936e3 (PREREG_A) / e63b4c483 (AMEND1) /
5ae01711a (impl A) / 123d3086a (PREREG_B) / 27026eb3a (AMEND1) /
cc5231509 (impl B) / 494553776 (PREREG_C) / 47762743a (impl C).
