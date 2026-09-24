# PREREG — ROUND-C CHEAP PROBES (frozen before build)

Date: 2026-09-24. Crew: H-C (PAM round-2 swarm, hypothesis crew).
Status: FROZEN BEFORE BUILD. Committed ALONE before any probe code is written or run.

## 0. Purpose

Cheap falsification probes (D5-style) for H-PAM-29..34. One pure-Zag binary,
`roundc_probe.zag`, `argv[1]` selects the mode. Zero RNG. Deterministic fixtures by
closed-form formulas. 3 runs per mode, byte-identical stdout (SHA-compare).
Toolchain: pinned `znc_linux_x86_64_abed8aa1`. Scratch: `~/workspace/pam_roundc/`
(never /tmp). No binaries committed.

Shared fixture model: percept = (id, conf, meas, label), label 1=true / 0=false.
Honest cluster (mirrors F5 Box A exemplar): conf in [700,730], meas in [2600,2650].
The gate under test NEVER sees `label` (that is the point). The probe harness sees it
for scoring. The "adversary" is a deterministic hill-climb/search standing in for the
red team's blind-quadrant shopping: it queries the gate function and emits bytes.

Toy hash: FNV-1a 64-bit (`toyhash`). Explicitly a stand-in for structure, not crypto;
the real hash chain is H-OB-4's. Where the probe needs an information asymmetry
(adversary pre-run vs principal during run), the probe harness holds a NONCE that the
adversary function is not passed — this models "the principal is not a deterministic
function of the transcript" (true of a human principal). The transcript records all
verdicts; replay is byte-identical. This is NOT a mechanism secret.

## 1. Modes, gates, adversaries, bars

### sep — Separation Lemma demo (H-PAM-29 core)
- Gate G_sep: ADMIT iff conf in [690,740] and meas in [2590,2660] and a confirm
  re-read (second sample: conf2 = conf + ((id*37) mod 11) - 5, meas2 likewise with
  mod 13) also in-box. Gate G_sep2 (same mode, second gate): ADMIT iff in-box AND
  |meas-2625| + |conf-715| < 60 (diamond, smaller region).
- Fixtures: 60 honest (id=1000+j, label=1, conf=700+(j*7 mod 31), meas=2600+(j*11 mod 51));
  60 attack (id=2000+j, label=0).
- Adversary: hill-climb from the honest fixture: step (conf,meas) by ±1..3, keep
  label=0, objective = admitted. Budget 2000 steps per fixture (deterministic order).
- Bars: honest admitted 60/60 both gates (sanity, else gate vacuous). Attack admitted
  ≥54/60 on EACH gate → Lemma mechanism demonstrated on a fresh gate (any non-empty
  admit region is searchable; shrinking the region does not help).
- Predicted: 60/60 honest admitted; 60/60 attack admitted both gates.

### irrev — naive irreversible-action gate death (H-PAM-29, direction (a) naive)
- Gate G_irrev: on percept P=(id,conf,meas,pred): action a = (id*101+conf) mod 8;
  world state W (u64, starts W0=0x12345678): W' = W | (1 << a) (irreversible: bits
  only set, never cleared); consequence c = (meas * (a+1) + (W' mod 1000)) mod 4096;
  ADMIT iff pred == c AND in-box (G_sep box). The consequence is transcript-computable
  by construction.
- Fixtures/adversary: 60 honest (label=1, pred computed honestly), 60 attack
  (label=0); adversary computes pred = c via the known formulas (it simulates W).
- Bars: honest 60/60 (sanity). Attack admitted ≥54/60 → naive (a) DEAD:
  irreversibility adds nothing when the consequence is transcript-computable.
  The surviving form (consequence through a channel the adversary doesn't author)
  is H-PAM-33/34 territory, explicitly out of this mode's scope.
- Predicted: 60/60 attack admitted.

### mepoch — naive multi-epoch consistency death (H-PAM-29, direction (b) naive)
- Gate G_mepoch: percepts arrive in triples (id, id+1, id+2), same content id cid;
  ADMIT the triple iff all three in-box (G_sep) AND pairwise |conf_i-conf_j| ≤ 5
  AND |meas_i-meas_j| ≤ 20.
- Fixtures: 20 honest triples (label=1), 20 attack triples (label=0, authored
  consistently by the adversary: conf/meas within the bounds by construction).
- Bars: honest triples admitted 20/20 (sanity). Attack triples admitted ≥18/20 →
  naive (b) DEAD: a table covers any finite consistent epoch pattern the author
  anticipates. Surviving form (trainer-interleaved) is H-PAM-34.
- Predicted: 20/20 attack admitted.

### pow — proof-of-work death (H-PAM-29, direction (c) naive; PoW ban decision)
- Gate G_pow: percept carries (nonce, phash=toyhash(id,nonce)); ADMIT iff in-box
  AND phash mod 1024 < 16 (difficulty 1/64) .
- Fixtures: 60 honest (label=1, nonce found by grinding), 60 attack (label=0,
  nonce found by grinding with the IDENTICAL procedure).
- Bars: honest 60/60 (sanity). Attack admitted ≥54/60 AND grind-cost ratio
  adversary/honest in [0.9, 1.1] → PoW DEAD as admission criterion: symmetric
  compute under determinism proves nothing about truth. DECISION preregistered:
  PoW BANNED as a PAM admission criterion (the surviving cost-asymmetry is
  harness-enforced scarcity, H-PAM-32).
- Predicted: 60/60 attack admitted; cost ratio ≈ 1.0.

### trmod — trainer-MODULE variant death (H-PAM-30 narrowing)
- Trainer module M: verdict(P) = CONTRADICT iff conf in [770,830] AND meas in
  [2185,2215] (the H-PAM-20 known-false rectangle as a blocklist); else CORROBORATE.
  Composed gate: ADMIT iff G_sep admits AND M corroborates.
- Fixtures/adversary: 60 honest (in-box, outside rectangle, label=1), 60 attack
  (label=0); adversary hill-climbs for (in-box AND outside-rectangle AND label=0).
- Bars: honest 60/60 (sanity). Attack admitted ≥54/60 → the MODULE-trainer variant
  of H-PAM-30 is DEAD (author searches the module's blind spots); H-PAM-30
  NARROWS to real-principal-only. LLM-judge variants do not transfer
  (author-queryable — recorded, not tested here).
- Predicted: 60/60 attack admitted.

### tror — oracle-trainer composition sanity (H-PAM-30 bound)
- Oracle O: verdict = CORROBORATE iff label=1. Composed: ADMIT iff G_sep admits
  AND O corroborates.
- Fixtures: 60 honest (label=1), 60 attack (label=0, in-box).
- Bars: attack admitted 0/60; honest admitted 60/60. This does NOT prove H-PAM-30;
  it bounds it: the composition is EXACTLY as good as its trainer, no better.
  Any real-principal build inherits this bound with the principal's measured
  discrimination in place of the oracle's.
- Predicted: 0/60 attack, 60/60 honest.

### tier — tier-boundary mechanics (H-PAM-31)
- Fixtures: 120 Class-H-like attacks (label=0, false, deviant features:
  conf=700+(j mod 31), meas=6000+(j mod 21)*50, i.e. the RT-H complexity shape),
  120 honest (label=1): 60 LOW-stake, 60 HIGH-stake (harness-labeled; the adversary
  does not choose the stake of honest fixtures).
- Routing: LOW → low tier (admitted, INERT). HIGH → oracle trainer → high tier iff
  corroborated. Inertness enforced in code: `act_fn` and `premise_fn` (the
  downstream action / belief-premise consumers) read ONLY the high tier; a
  promotion path low→high exists but requires oracle corroboration.
- Red team: all 120 attacks labeled LOW (adversary takes the cheap route —
  CONCEDED), plus 40 attacks labeled HIGH (adversary tries the expensive route).
- Bars: (a) high-stake harm events from the 120 LOW attacks = 0, where harm =
  act_fn fired on attack content OR premise_fn consumed attack content OR attack
  promoted to high tier; (b) HIGH attacks admitted to high tier = 0/40;
  (c) honest HIGH admitted 60/60; honest LOW admitted (inert) 60/60.
  Any (a)>0 or (b)>0 → the tier boundary as implemented is rideable → hypothesis
  needs repair (recorded, not a pass). This mode uses the ORACLE to isolate tier
  mechanics; the trainer residual is H-PAM-30's problem.
- Predicted: (a) 0, (b) 0/40, (c) 60/60 and 60/60.

### bond — claimant-bond dynamics (H-PAM-32)
- Synthetic ledger (no fixtures needed beyond ids): claimants A_adv (emits 100
  percepts, all label=0, all eventually revoked) and A_hon (emits 200 percepts,
  4 label=0 (2% noise), rest label=1, never revoked). Emission order interleaved
  deterministically. Bond B0=100 each; slash 10 per revoked false; bond ≤ 0 →
  auto-withhold all further percepts from that claimant. Percepts are admitted
  (provisional) at emission, revoked later (the D2 model).
- Bars: (a) A_adv admitted falses before ruin ≤ 15 → bounded quantity
  demonstrated; (b) A_hon bond at end ≥ 40 → honest survives noise
  (200×0.02×10 = 40 slashed → 60 left); (c) A_hon true percepts admitted
  196/196 and 0 true percepts revoked (honest-loss); (d) single-critical-lie:
  A_adv variant spending its whole bond on 1 lie → admitted — RECORDED as
  residual (bonds bound quantity, not the one critical lie; must compose with
  H-PAM-30/31), not a pass/fail.
- Predicted: (a) 10, (b) 60, (c) 196/196, (d) admitted (residual).

### chan — win-condition shift (H-PAM-33)
- Toy sensor chain: percept = (id, conf, meas, label, prev, hash=toyhash(id,conf,meas,prev)).
  Endorsed chain: generated by the PROBE HARNESS (not the adversary fn) — 20 honest
  percepts, label=1, chained.
- Attacks: (A) adversary mints its OWN valid chain of 20 false percepts (it knows
  toyhash) and presents it on the unendorsed channel; (B) adversary tampers with
  the endorsed chain (H-OB-39-style re-parent: percept k's prev rewritten to
  point at k-2).
- Gates: content gate G_c = G_sep on (conf,meas) ignoring chain fields; channel
  gate G_ch: ADMIT iff chain verifies (recompute all hashes, check linkage) AND
  channel endorsed (harness flag).
- Bars: (a) G_c on attack A: admitted ≥18/20 → content can't tell a minted chain;
  (b) G_ch on attack A: admitted 0/20; (c) G_ch on attack B: admitted 0/20
  (tamper detected); (d) G_ch on intact endorsed chain: 20/20 (sanity).
  (a)∧(b)∧(c)∧(d) → win-condition shift demonstrated: the adversary must escalate
  from "write bytes" to "get on the endorsed channel" (harness-enforced).
- Predicted: (a) 20/20, (b) 0/20, (c) 0/20, (d) 20/20.

### mepoch_tr — table coverage gap (H-PAM-34)
- N=200 percepts (100 label=1, 100 label=0, in-box), K=3 epochs. Trainer (harness
  side): verdict(p,e) = CORROBORATE iff label=1, flipped iff toyhash(id,e,NONCE)
  mod 8 == 0 (run-private quirk; NONCE not passed to the adversary fn).
- Adversary: pre-run table predicting verdict(p,e) for all p,e from (id,e,label)
  only; best strategy = predict label.
- Bars: per-verdict accuracy reported (sanity: ≈ 0.875 — the trainer is mostly
  label-following, NOT random); FULL-SEQUENCE accuracy (all K verdicts correct
  per percept) ≤ 0.75 → coverage gap demonstrated: the table cannot COVER the
  trainer's future (any single unexpected CONTRADICT withholds the attacked
  percept; the adversary cannot identify which percepts are safe).
  Predicted: per-verdict ≈ 0.875, full-sequence ≈ 0.67.
- Explicit non-claim: the NONCE models "the principal is not a deterministic
  function of the transcript" (true of a human principal); it is not a mechanism
  secret (verdicts are recorded; replay is byte-identical).

## 2. Global bars

- Every mode: 3 runs, stdout SHA-256 identical across runs, else the mode is
  VOID (rerun, do not interpret).
- Any mode whose honest-sanity bar fails is VOID (the gate is vacuous or the
  fixture generator is broken — fix and rerun, do not interpret as a kill).
- Predicted outcomes above are the crew's; a mode FIRES its kill/narrowing bar
  mechanically on the measured numbers regardless of prediction.
- No mode builds a full mechanism. Probes only. Build crews come next.

## 3. Interpretation map (preregistered)

- sep fires → H-PAM-29 Lemma mechanism demonstrated on a fresh gate.
- irrev fires → naive (a) dead. mepoch fires → naive (b) dead. pow fires →
  naive (c) dead, PoW ban decided.
- trmod fires → H-PAM-30 module variant dead; narrows to real-principal-only.
- tror passes → H-PAM-30 bounded by trainer discrimination (not proved).
- tier passes → H-PAM-31 tier-boundary mechanics validated (oracle-isolated).
- bond passes → H-PAM-32 dynamics validated; residual (d) recorded.
- chan passes → H-PAM-33 win-condition shift demonstrated.
- mepoch_tr passes → H-PAM-34 coverage gap demonstrated.
