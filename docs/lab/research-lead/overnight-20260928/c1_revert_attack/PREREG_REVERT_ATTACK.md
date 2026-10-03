# PREREGISTRATION: C1 Law-Revert Attack

Status: FROZEN PREREG. Committed alone before any implementation,
freeze, world generation, or evaluation. Any change requires a dated
amendment committed alone before the changed code runs.

Date: 2026-09-30 UTC
Worker: C1 Law-Revert Attacker
Owned path: docs/lab/research-lead/overnight-20260928/c1_revert_attack/

## 1. Mandate and mechanism model under attack

C1-CLEAN-PASS (b2b1ec415) reported a deterministic law-revert miss in
exploratory hard world H0: query L3 expected "ttxy", got "tyxt", on all
3 reps, while H1 scored 4/4 on its own revert query. The old 63/63 wave
is EXPLORATORY / GOVERNANCE-VOID / NOT CANONICAL; only the C1-CLEAN
chain is canonical evidence.

Post-hoc white-box analysis of the frozen contestant source and the H0
run state (hypothesis, not evidence) produced the mechanism model under
attack:

- M1: ingest_law supersedes (sup 0 to 1) every demo of the named proc.
  It is monotonic: a second notice never restores sup to 0.
- M2: at H0 L3 time the sup=0 demo set was exactly the two post-revert
  demos ("afaf" to "fafa", "djdh" to "hdjd"). Detection (the revert
  notice was ingested) and diagnosis (stale demos superseded, fresh
  demos kept) both behaved correctly in the white-box trace.
- M3: ans_proc tries rule classes in fixed priority: char map,
  reversal, duplication, rotation, then nearest-demo fallback. Both
  post-revert demos were simultaneously rotation-consistent AND
  reversal-consistent (rev("afaf")="fafa"; rev("djdh")="hdjd"), so the
  reversal class fired before rotation and produced rev("txyt")="tyxt".
- M4: the hypothesized failure is therefore APPLICATION-level:
  inference from correctly revised evidence, under demo ambiguity and
  fixed class priority. The revert-specific gap is that the mechanism
  cannot restore the original-law demos (which would have disambiguated
  reversal vs rotation); the reverted law is re-learned from the fresh
  demos only.

This prereg tests M1-M4 on fresh sealed worlds. Section 1 is hypothesis
until the kill bars below pass.

## 2. Attack world design (minimal, sealed)

New pure-Zag generator world_gen_revert.zag builds minimal
law/revision worlds. Same turn/reply JSON protocol and tool semantics
as C1-CLEAN. Same demo regime as the C1-CLEAN hard worlds: 4-char
inputs from 97+rnd(13), query inputs from 110+rnd(13), so the inference
classes face the same ambiguity profile.

Each world:
- Setup: 3 demos of pa under reversal (wg_rev); 3 demos of pb under
  rotation key kold (wg_rot, kold in 1..3).
- One of 4 frozen families, each ending with queries R1
  (post-first-change), R2 (post-revert or post-second-change; the
  attack query), R3 (pa retention control).

Families:
- F-A EXACT REVERT: law(pb); 2 demos pb under k2 (k2 in 1..3,
  k2 != kold); query R1 pb under k2; law(pb); 2 demos pb under kold;
  query R2 pb under kold; query R3 pa.
- F-B PARTIAL REVERT: law(pb); 2 demos pb under k2; R1 under k2;
  law(pb); 1 demo pb under kold; R2 under kold; R3 pa. "Partial" means
  the revert restores the original law with reduced re-evidence
  (1 demo instead of 2).
- F-C REVERT WITH CONFOUNDERS: law(pb); 2 demos pb under k2; R1 under
  k2; 300 noise obs interleaved; law(pb); 2 demos pb under kold;
  R2 under kold; R3 pa.
- F-D DOUBLE CHANGE A to B to C: law(pb); 2 demos pb under k2; R1
  under k2; law(pb); 2 demos pb under k3 (k3 in 1..3, k3 != kold,
  k3 != k2); R2 under k3; R3 pa.

8 fresh worlds per family (worldidx 0..7), 32 worlds total, each run
3/3 from fresh state (96 runs).

## 3. Frozen predictions

- P1 DETECTION: zero detection failures across all 96 runs. Every law
  notice is ingested; no pre-notice demo remains sup=0 at query time.
- P2 DIAGNOSIS: zero diagnosis failures across all 96 runs. The sup=0
  set at each query equals exactly the demos ingested after the most
  recent law notice for that proc (no stale demo live, no fresh
  demo dead).
- P3 APPLICATION: the independent frozen diag.zag re-implementation
  of the ans_proc class cascade predicts the actual answer for all 96
  R2 queries (and all R1/R3 queries): full agreement. Every miss is
  thereby located at APPLICATION: inference from correctly revised
  evidence under demo ambiguity (reversal-consistent demos firing the
  reversal class; rotation-inconsistent demos falling through to the
  nearest-demo fallback; periodic demos giving a consistent but wrong
  rotation key).
- P4 REVERT GAP: on F-A, the original-law demos are never restored
  (sup stays 1 through the revert) on all 24 runs; the reverted law is
  re-learned from the fresh demos only.
- P5 ORDERING (reported, small-n caveat): miss count F-B >= each of
  F-A, F-C, F-D, because one post-revert demo is class-ambiguous more
  often than a pair. F-C is predicted to behave like F-A (noise never
  touches D lines); F-D like F-A (a second change uses the same
  monotonic supersede path as a revert).

## 4. Diagnostic protocol (frozen)

Applied to every R2 query (and any R1/R3 miss), using the run's final
state.txt:

- D1 DETECTION: list D lines for pb. If any demo with turn earlier
  than the last law-notice turn has sup=0, record DETECTION failure.
- D2 DIAGNOSIS: if the sup=0 set is not exactly the demos with turn
  later than the last law-notice turn, record DIAGNOSIS failure.
- D3 APPLICATION: run frozen diag.zag on the sup=0 set. If its
  predicted answer equals the actual answer, record APPLICATION-level
  (inference from correctly revised evidence). Else UNCLASSIFIED.

## 5. Kill bars

- K1 ORDERING: this prereg committed alone before the freeze commit;
  the freeze commit (contestant hash, generator hash, sequencer hash,
  diag hash) strictly precedes any world generation; seeds are
  derived from /dev/urandom after the freeze (hashes recorded, values
  never viewed); each world is generated twice with byte-identical
  output. Ordering is verifiable from the commit graph and hash logs.
- K2 COVERAGE AND LOCATION: 4 families x 8 worlds x 3/3 reps all run;
  per-world replies byte-identical across reps; per-family scores
  reported against P1-P5; P1, P2, P4 hold exactly; P3 holds with full
  diag agreement; every miss is located by D1-D3 with zero
  UNCLASSIFIED misses.
- K3 PURITY AND DIAGNOSIS: pure Zag, zero Python (verified by find, no
  .py files); no em dashes (shell-only check_no_dash.sh); a
  mechanism-level diagnosis is delivered locating each miss in
  detection, diagnosis, or application.

## 6. Contestant

Byte-identical reuse of the C1-CLEAN frozen contestant binary, copied
into this owned path. sha256 must equal
8c7ccf308b46e193defeba137c701076cb5b7f7bed28f0393c314bf8bcaa48e4
(the C1-CLEAN FREEZE.md record). No recompilation, no modification. The
contestant is the measurement instrument, not an L3 claim.

## 7. Non-goals and claim discipline

- No L3 claim is made or tested. This is a mechanism-boundary attack.
- No LLM baseline; the serious LLM baseline remains PENDING.
- These are minimal attack worlds aimed at one mechanism; no claim is
  made about the full lifetime regime.

## 8. Governance

- Pure Zag for all race logic. Bash only sequences process
  invocations. No C, no other languages. No Python anywhere,
  including scratch, debugging, verification, and /tmp. Violation
  voids the wave.
- No em dashes in loop documentation.
- Commits local only on tnn-native-lab. Owned path
  docs/lab/research-lead/overnight-20260928/c1_revert_attack/ only.
  Explicit pathspec on every commit.
- Never edit, stage, or commit
  docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md.
- If a live .git/index.lock is hit, wait and retry; never remove it.
