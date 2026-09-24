# WORKSTREAM A: M1 vs M2 SEPARATION BATTERY (H4) — Frozen Prereg

Date: 2026-09-23. Operator: Muse (subagent, depth 2/2).
Status: FROZEN. Committed alone before any battery code exists.
Branch: `tnn-native-lab` (sylorlabs/TNN).
Dir (lab-relative): `training_paradigms/scaffold_release/forks/gl_worldchange/m1m2_separation/`

## 0. Lineage and question

H4 (world-changed vs lied-to) ended with M1 (dedicated `TN_OP_SUPERSEDE`
primitive) and M2 (general classifier + ledger-derived temporal index, no
substrate change) tied on every frozen bar (KB-WC1, KB-WC2, KB-HIST, KB-COST,
m_distinguish). M2 was named winner on figure-it-out-wins-ties (Micah's law).
Micah's verdict: "that's rough — separate them on efficiency or edge-case
toughness." Standing directive (2026-09-23): M1/M2 ties on intelligence get
broken by speed/compute; look for edge cases where one is tougher.

This workstream: (1) rebuild both targets natively in pure Zag against the
frozen H4 curriculum, verify the intelligence tie on the rebuild; (2) run an
efficiency battery (episodes/sec, ops per update, peak memory, ≥3
byte-identical reruns); (3) run a preregistered edge-case hunt designed to
split them. Verdict rule in §5.

Prior synthesis commit: `5908526e` (tnn-native-lab).

## 1. Mechanism facts (grounded in the committed sources, not assumed)

Sources: `training_paradigms/scaffold_release/forks/gl_worldchange/targets/m1|m2/`
(`gl_substrate_m1.zag`, `gl_substrate_m2.zag`, `m1_harness.zag`,
`m2_harness.zag`, `wc_mech.zag`, `wc_streams.zag`).

- Arenas (identical both targets, MODULES.md): main store 128×3 words,
  quarantine 64×3 words, audit ledger 2048×16 B, per-key state 8 keys,
  single pending-announcement slot, 8 held world readings, history index
  16 entries, 8 counters. Audit entry = step,op,slot1,aux (16 B).
- M1 completion (W2: world corroborates pending UPDATE): emits one
  `TN_OP_SUPERSEDE` (19), writes the history entry from LIVE KEY-STATE
  (`ks.TEP`, `ks.CORR` of the old binding) — O(1), everything in hand.
- M2 completion (W2): emits one `TN_OP_COMMIT` (13) with aux
  `WC_V_SUPERSEDE`, writes the history entry with the interval start from
  `m2_derive_taught`: a scan of the IMMUTABLE AUDIT LEDGER for the
  EARLIEST `(EPISODE(TEACH|UPDATE,k) immediately followed by TEACH(old))`
  pair — O(ledger) per completion. If no pair: BAD.
- Everything else is shared logic: establishment gate `wc_est_gate`
  (ack + teacher-taught + corr ≥ WC_EST_THETA=3), conditional time-indexed
  vindication, W1/W2/W3 world-evidence authentication (window 2, pending
  TTL 4), pending-overwrite on re-announcement, W3 eliminative path.
  M1's W3 COMMIT carries aux=ACT_CONTEST (no verdict); M2's carries the
  classifier verdict (WC_V_LIE / WC_V_WORLD_REPLACE) and bumps SPARE on LIE.
- Consequence: per-episode AUDITED op counts are identical on identical
  streams (SUPERSEDE vs COMMIT = 1 op each). The cost difference, if any,
  is M2's unaudited ledger-scan derivation work.

## 2. Rebuild and the intelligence-tie premise

- Vendor the six committed sources above byte-identical into the workdir
  (checksums recorded). Write only NEW main drivers; no mechanism edits.
- PARITY GATE (void-result gate, checked first): my rebuild driving sids
  0–4 with emission must reproduce the committed `m1_run1.txt` /
  `m2_run1.txt` byte-identically. Fail → stop, rebuild is not the H4 targets.
- Intelligence bars re-checked on the rebuild: KB-WC1 (sid 3: no false
  history, trust <0), KB-WC2 (sid 4: trust ≥0, q_now=B), KB-HIST (sid 1:
  q_asof(E5)=101, q_now=102), KB-COST (update-path audit entries ≤ re-teach
  price). Expectation: all PASS, both targets (the tie premise).

## 3. Efficiency battery

Identical episode streams for M1 and M2. Zero RNG. Each binary runs ≥3×;
stdout must be byte-identical across runs (sha256 recorded).

- E1 CURRICULUM THROUGHPUT: frozen sids 0–4, R=2000 reps, quiet mode (no
  per-episode emission; one summary line: total episodes, total audit
  entries, completions, GFAIL, rolling state checksum). Metric m_eps =
  episodes / wall-second (wall from `/usr/bin/time`; binary prints no
  timing, preserving byte-identity).
- E2 CHAIN SCALING: one key: TEACH(A)+3×WORLD(A), then T chained
  supersessions (T=1..14; history cap is 16), each UPDATE followed by
  WORLD(new)+3×WORLD(new) (3 corroborations needed: the gate requires
  corr≥3 at every announcement). Fresh arenas per T. Binary takes T and
  reps from `_zag_arg` (read unconditionally; argc is 0). Per T, R=300:
  wall time per update, audited ops per update (audit-entry delta across
  the update window), and M2's ledger-scan reads per update — counted by
  an exact replay of `m2_derive_taught` over the actual produced ledger
  (the binary executed precisely this scan; the replay only makes the
  count explicit).
- E3 STRESS: 7 keys × (TEACH+3×WORLD + 2 chained updates each with
  3×WORLD) = 98 episodes, 14 supersessions (under the 16-entry cap),
  R=2000: m_eps and peak memory.
- m_peakmem: computed from the arena table (deterministic; all
  allocations fixed-size; CAL scratch is alloc/free per episode so peak =
  base arenas + one CAL scratch set). Reported per target with the
  arithmetic shown.

Frozen predictions:
- P-E1: audited ops per update IDENTICAL; peak memory IDENTICAL (same
  arena table, same CAL path). m_eps within noise on the frozen
  curriculum (the scan is small there).
- P-E2: M1 per-update cost flat O(1); M2 per-update ledger-scan reads
  grow linearly with ledger length (O(T²) total over the chain) and
  per-update wall time grows with T.
- Efficiency winner criterion: if intelligence ties, the winner is the
  target with lower asymptotic per-update cost AND lower measured
  per-update wall time at T=14. If per-update wall times are within ±5%
  at every T, efficiency is a TIE.

## 4. Edge-case hunt

Custom deterministic streams in a new main-free module `ec_streams.zag`
(driven through the real `m1_step`/`m2_step`). Key k1=1; values
A=101,B=102,C=103,D=104,E=105. "Established" = taught + 3×WORLD
(corr=3 meets the gate). Per EC, per target: PASS/FAIL + trace excerpt.
A FAIL must include a concrete failing trace (episode audit excerpt + the
wrong query answer).

- EC1 DEEP-CHAIN (5 deep): establish A; UPDATE A→B, WORLD(B)+3×WORLD(B);
  UPDATE B→C … through E (5 supersessions). Criteria: no BAD; q_now=E;
  q_asof correct for every reign; trust delta 0. Prediction: TIE
  (distinct values → M2's earliest-match finds the unique teach).
- EC2 CONFLICT-ORDERS: establish A. Order1: UPDATE(A→B)@e,
  UPDATE(A→C)@e+1, WORLD(B)@e+2, WORLD(C)@e+3. Order2: UPDATE(A→C)@e,
  UPDATE(A→B)@e+1, WORLD(C)@e+2, WORLD(B)@e+3. Criteria: latest
  announcement wins (order1→C, order2→B); no false history for the loser;
  trust 0; q_now = latest-announced value. Prediction: TIE (shared
  single-slot pending logic: re-announcement overwrites).
- EC3 QUARANTINE: establish A; WORLD(B)@e, WORLD(B)@e+1 (W3 authenticates
  → eliminative revocation, B installed corr=1); then UPDATE(B→C)@e+2.
  Criteria: no BAD/crash; the update is NOT superseded (gate correctly
  refuses: corr=1<3) — contest/lie path; trust follows frozen §5.
  Prediction: TIE.
- EC4 NO-PRIOR: (a) UPDATE(k2, aux=999→101) on never-taught k2: cur<0 →
  binds directly as teach. Criteria: no BAD; behavior documented
  (shared quirk: phantom UPDATE installs as teach). (b) UPDATE(k1,
  aux=999→102) on established A=101: ack fails → lie path, no
  supersession, no history entry, GFAIL++. Prediction: TIE both.
- EC5 MID-DELIBERATION (stale-pending desync): UPDATE(A→B)@e (pending);
  WORLD(C)@e+1, WORLD(C)@e+2 (W3 authenticates contradiction while B
  pending → eliminative revocation of A, C installed); WORLD(B)@e+3
  (stale pending completes). Criteria: no BAD; full trace recorded;
  post-hoc audit must expose the desync (sid-35 class). Prediction: TIE —
  informational: documents the stale-pending hazard identically in both.
- EC6 FLIP-FLOP: establish A@1–4; UPDATE(A→B)@5, WORLD(B)@6,
  WORLD(B)@7–9; UPDATE(B→A)@10, WORLD(A)@11, WORLD(A)@12–14;
  UPDATE(A→B)@15, WORLD(B)@16, WORLD(B)@17–19. Criteria: no BAD;
  trust 0; q_asof correct for ALL FOUR reigns (A:[1,5), B:[5,10),
  A:[10,15), B:[15,now)). Prediction: SPLIT — M1 PASS (interval
  endpoints from live key-state: second A-reign [10,15)); M2 FAIL:
  `m2_derive_taught` returns the EARLIEST teach of A (ep 1), so the
  second A-interval is [1,15), covering B's first reign; newest-wins
  then answers A for q_asof(6..9) where B was true.
- EC7 STALE-ECHO RACE: establish A; UPDATE(A→B)@e, WORLD(B)@e+1
  (completes); WORLD(A)@e+2, WORLD(A)@e+3 (old value echoes twice inside
  the window → W3 authenticates → eliminative revocation of just-
  installed B). Criteria: no BAD; trace recorded; does the revocation
  history falsify B's reign? Prediction: TIE with an ugly trace —
  documents W3-vs-supersession tension (informational).

## 5. Overall verdict rule (frozen)

1. If intelligence bars tie (expected): efficiency decides (§3 criterion).
2. If efficiency ties: edge-case toughness decides (more EC PASSes).
3. A correctness SPLIT (wrong q_asof, false history, honest-teacher trust
   damage, crash/BAD) outranks any efficiency margin.
4. If all three tie: report TIE plainly with the evidence.

## 6. Staffing / consultation notes

- Sol consulted 2× via UnoRouter (`sol.py`): both returned
  `choices:null`, 0 completion tokens — the known provider-backend
  failure mode (~/AGENTS.md), not a prompt problem. grok-4.6 consulted
  1×: socket timeout (known outage). No second-opinion voice available.
  EC7 is the mechanism-derived extra filling the Sol slot; the remaining
  ECs are mechanism-derived from source analysis.
- Native subagents unavailable at depth 2/2 (`can_spawn=no`) — same
  constraint the H4 crew recorded.
- Determinism: zero RNG in any decision path; ≥3 byte-identical reruns
  per binary (sha256 of stdout); audit ledgers are hash-chained
  (step+op per entry; final state digest printed).

## 7. znc build discipline (from ~/AGENTS.md)

Toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Read `_zag_arg(n)` unconditionally (argc==0); no slice >2^25 B; i32
struct fields at 8-B stride (WcEp=40 B via `wc_ep_alloc`); dot-prefixed
struct literals; no `try` identifier; no `};`; no bare blocks; build
from `src/` cwd (`@import` resolves relative to cwd); helper `i64s()`
strips the trailing newline for printing; no binaries or `.zagd` in
commits; TMPDIR=~/workspace/tmp_commit for commit tooling.

## 8. Commits (frozen plan)

- C1: this prereg alone.
- C2: vendored sources (verbatim) + new drivers + efficiency results.
- C3: edge-case results + final verdict.
Via `~/workspace/commit_racefree.py`, lab-relative paths, no binaries,
no `.zagd` files.
