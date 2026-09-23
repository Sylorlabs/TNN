# worker_repr.md — representation-sector sweep worker notes (2026-09-22 ~07:15 PDT)

Chunk: `chunks/chunk_repr.tsv` — 40 rows (1 P0 memory verdict sheet + 39 P2 representation rows).
All rows moved in-progress → done. No grok-4.7 calls used (native review sufficed; 5-call budget unused).

## 1. GROK47_OVERNIGHT/memory/VERDICT_SHEET.md (P0) — REVIEW: complete
- Rounds 1–7 fully documented with results + red-team adjudications; nothing remained to document.
- R1: pin-kill CONFIRM (fixture-scope; multi-victim = 3 kills at revelation, not 1), ContextGate REFUTE as stated
  (5+1 promotes — mechanism plain reading), TombRevive REFUTE as stated (1-verify revives; terminology error),
  FreezeLeak CONFIRM. Red-team A1–A15 adjudicated, scope caveats recorded.
- R2: ctx32 silent-drop (1<<32=0, NOT aliasing); **ctx31 → popcnt(INT_MIN) HANG (exit 124, build-qualified
  to znc_linux_x86_64_abed8aa1)**; revive-cost: 1 verify permanently closes condemn path (ver==0 gate);
  frozen gate promotes 8+1/6+1+1 impostors, strict per-context-≥2 rejects them (probe-only).
- R3 recall organ: read-only CONFIRMED (structural zero-write grep); greedy NOT minimum-cardinality
  (order-dependent); reuse blindness (no detach path, slot recall-invisible for RcState lifetime); unanimity veto.
- R4 MA4 churn: strict `v > vicv` CONFIRMED; non-atomic kill-then-admit noted (no rollback on add failure).
- R5 P1 struct-promote: unanimous dominance, inclusive ≥, one-arm veto, transactional rollback — all CONFIRM.
- R6: **kill bar for "P0 is fine" FAILED; P2 (corroborated-revive) strictly dominates** — matches P0 on A
  byte-for-byte, blocks single-verify resurrection on B. Frozen psm.zag untouched (proposal only).
- R7: **O3 revive→consolidate dead-end CONFIRMED** (rc 312; repair Q1 narrowed-refusal works, guards preserved).
- grok-4.7 HARD DOWN 2026-09-21 23:31 (429 insufficient_credits, −$0.02); sol fallback then fully native.
  Coordinator cron `grok47-recovery-probe` owns re-probing; this sector exempt from self-probing.
- Noted gap vs task brief: "scale S2 flaw-coverage / scale_learner.zag [0,n/4) gap" items were NOT in this sheet
  (belong to another chunk; grep across my rows confirms zero hits).

## 2. L2 jsonl legs (11) — all parse (single-line `METRIC_JSON ` prefixed), schema metrics-v1
- m1-1x-code: recall/boundary 100.0, 148678 units, id_probe PASS, id_changes 0 — PASS.
- m2-t2-code / m2-t2-prose: ep0 0.0 (no leak), final recall/boundary 100.0 — PASS.
- m2-t3-1x: + m9 fast-then-flat, takeoff ep1 — PASS.
- m3-1x: survival/fresh 100.0, mgmt 9053, weaken 50/50, freeze CLEAR — PASS.
- m4-1x-prose: rev boundary/content 100.0, kill 0.0, audit xepoch recalls 200/400, misses 0 — PASS.
- m5-1x: 84731 units, 5.42MB learned, slot table 23.35MB, ledger 5.49MB/85738 entries — PASS.
- m5-baseline: {"m5_baseline":"ready"} placeholder only, no metrics by design — PASS.
- m6-p2c-1x: rec/bnd/rev/indomain 100.0, tax 0.0, bumps 15 — PASS.
- m7-1x: hit 100.0, reuse 2.0, dedup 50.0, cell PASS, round2_revised 848 — PASS.
- memctrl-c2p-1x: transfer 82.2 > in-domain 27.4 (drop −54.8) — parses; counterintuitive memorizer-control
  value recorded as measured; flag for program interpretation, not a parse issue.

## 3. scorecard_assemble_l2.py / scorecard_assemble_y3.py — REVIEW: PASS both
- L2: rc=0, 2 runs byte-identical, handles METRIC_JSON prefix, merges 17 legs incl. memctrl; m1_id_probe PASS
  both corpora; m7 provisional flag.
- Y3: deterministic, byte-identical reruns; rerun byte-matches committed `scorecard_y3_r1_1x.json` exactly;
  m1_id_probe marked PROVISIONAL-PENDING-FREEZE (coordinator correction: shared b64 script must not be used unchanged).

## 4. Y5_10X_VERDICT_REPORT.md — REVIEW: claims consistent
- 1x gate 15/15 PASS, M8 50/50 byte-identical; 10x N=5: m1–m7, m6 legs all PASS (recall 100.0, ETC=1, kill 0.0,
  hit 100.0/reuse 3.1); M3=0 per prereg §5 — FROZEN-UNDER-PRESSURE fired (mgmt 0 <700 threshold) is an
  audit-logging scale issue, NOT an actual freeze (fresh recall 100.0, survival 100.0, weaken 50/50); arm NOT
  disqualified; M8-10x 25/25 PASS (hashes recorded).
- Notable: `nio_read_at` seek bug found+fixed during run (lseek returns offset, not 0; fix `!=off`);
  1x SHAs unchanged post-fix confirming 1x paths untouched.

## 5. Y6 jsonl (3) — PASS
- m3-1x: survival/fresh 100.0, mgmt 8050, ledger 14050 entries, checker_rc 0.
- m5-1x: 84731 units, slot table 4.75MB (vs L2's 23.35MB — different table sizing), ledger 5.49MB/85731, checker_rc 0.
- m7-1x: hit 100.0 (5-field metric file).

## 6. R0 formal spec + R3/R5 recommendations — REVIEW: consistent
- FORMAL_SPEC_R3_R4_R5.md: verbatim sed extracts; consistent with signed outcomes (ε 25/1000, ratio 1.15;
  R-4 drawdown-from-running-max ≤25/1000; R-5 strict 8/8).
- R3_RECOMMENDATION: ε≤25/1000 + ratio≥1.15, both legs PASS (1.417/1.195); ratio 1.2 would fail leg1 — the
  knife-edge is the manifest's pre-registered leg-1 role, not the numbers; judgment disclosed; matches signed.
- R5_RECOMMENDATION: strict 8/8 clean + zero contested recruitments; margin dropped (under determinism 7/8 is
  unreachable — margin is exercisable only by bugs); e=1 measures abstention discipline; matches signed.
- VERDICT_SHEET.md (harness): build byte-identical, selftest/r1test 0 fails byte-identical, M8 gates PASS;
  4 flagged ambiguities incl. stale "PROPOSED — NOT FROZEN" text in local prereg copy and METRICS.md vs
  ARM_INTERFACE.md schema conflict (needs Micah's ruling — structural, surfaced).

## 7. R3/R4 formal verdicts + leg evidence — REVIEW: consistent; ONE FINDING
- FORMAL_VERDICT_R3/R4: 6/6 byte-identical reruns, numbers reproduced (|dual-raw|=0, ratios 1.417/1.195;
  dose flat 950, drop 0); both correctly UNDECIDED pending Micah's numeric amendment (now signed).
  FORMAL_VERDICT_R4 notes one background worker killed mid-run (leg-0 repeated-p0 @4000) — re-executed
  from scratch, no partial outputs used.
- b_t2_leg1.md: numbers consistent with formal verdict; descriptive PASS; M8 6/6 byte-identical.
- **FINDING — b_t3_leg1.md dose table corrupted:** the table body contains only a Python repr of the M8
  perturb labels (`[('0','baseline'),...]`) instead of the 250→8000 dose rows. Values exist in
  FORMAL_VERDICT_R4.md (950 flat all doses), but this evidence file's table is an empty generator artifact.
  Needs regeneration by the ablation crew.

## 8. Dynamics verdicts — REVIEW: FAIL stands, supersession honored
- VERDICT_B5_DYNAMICS.md (PASS): the file itself is honest — split+merge fired on SEPARATE contexts;
  B5-F1 documents the prefix-shadow dedup wart (tombstoned prefix record blocks re-promotion of the prefix;
  whole-span re-promotes as new id). Filed ZNC-2026-09-21-002 (slice-as-*u8). Its PASS claim is explicitly
  SUPERSEDED by the roundtrip verdict.
- VERDICT_BT5_ROUNDTRIP.md (FAIL): same-material split→remerge fails in 0/2 argument orders on both legs;
  merge gate requires both inputs live but split tombstones the parent → no merged chunk; 8-byte divergence
  measured. RT-3 merge-alone control OK (merge op sound; the FAIL is composition). Determinism manifest:
  59 lines byte-identical across perturbations, logs MD5'd.

## 9. Fork exhaustion — REVIEW: PASS; maps reproduced exactly
- fork_exhaustion.py ran rc=0: no RNG (no `random` import, all data literal); R4 grid reproduces
  R4_SENSITIVITY_MAP cell-for-cell (F1×25 = unique zero-mismatch; `<` boundary → 4 mismatches); R5 grid
  reproduces R5_SENSITIVITY_MAP cell-for-cell (W1/W4a/W7 × C1 = unique 0 cells). Cosmetic: dead
  `r4_mismatches` defined but never called (`r4_mm` used). Writes only tiny /tmp/r0_fork.
- R4 map: F1 drawdown-running-max ≤25/1000 CONFIRM strengthened — 18 curves, bleed loophole has 3 instances
  (S3b, A4, A7); materiality line at exactly 25 (one span's occurrence budget).
- R5 map: (W1/W4a/W7 × C1) unique survivors — provable equivalence (pooled-100% ⟺ per-exposure 8/8);
  every margin/average/outcome-only/contested-lenient fork killed by named scenarios (D1–D15 + M0).

## 10. B-T1 tournament — REVIEW: FAIL stands; scorers verified
- VERDICT_SHEET.md (01:42): PASS claim UNREPRODUCIBLE — superseded by closeout addendum (see below).
  Section champions recorded per standing rule: capability 0.919, compression, retrieval →
  predictive_surprise; grounded-consistency → fixed_window_64.
- CLOSEOUT_ADDENDUM.md: independent reproduction DISCREPANT — measured differs substantially (surprise
  0.9558 vs claimed 0.6843 prose); binding FAIL: raw_micro rank 7/10, not dead last; grounded_adaptive_mdl
  crashed (heap SIGSEGV, GROUNDED_BUG.md). 01:42 numbers have no surviving provenance.
- Mechanistic read of FAIL (artifact-driven): the hard leg XORs every 7th byte (mod-7 defect); wide
  fixed windows (_8/_16/_64) collapse on grounded_hard (fw64 prose: vocab 0, hard 0.0) while raw_micro
  (1-byte chunks) is resilient — so raw_micro outranks three wide-window arms. Consistent with the task
  brief's "artifact-driven XOR L=7" note.
- bt1_score.py: self-test on synthetic SEG — rc=0, tiling+reconstruction gates fire, composite computed.
  Zero RNG, deterministic. Note: my first synthetic attempt failed only on `END` needing a trailing space
  (parser is `startswith("END ")`); file-format quirk, not a bug.
- bt1_scorecards.py: 10 cards written, exact 29-key normative list, flags-as-strings, tournament-external
  metrics honestly null with m7_na_reason. Matches harness schema precedent.
- PROBE_MANIFEST.md (closeout): frozen; documents Python-scorer scope decision (measurement code, xcheck
  precedent — pure-Zag law governs the arms, not the scorer); METRICS vs ARM_INTERFACE conflict flagged.
- RUN_MANIFEST.md (closeout): 22 arm×corpus pairs byte-identical (r1==r2 sha256); grounded_adaptive_mdl seg
  files absent (crash); cosmetic tail artifact: `gen_manifest.sh: line 28: fail: unbound variable`.
- READBACK.md / READBACK_CLOSEOUT.md: all six probes PASS (12/12 MDL row-for-row incl. from-scratch
  reimplementation, hand FNV-1a ids, surprise cut-rule on "AB", 70/70 smoke goldens, probe_stores P1–P4
  bad=0); source canary clean (only syscall-0 stdin reads).
- RUN_MANIFEST_REPAIRED.md: grounded_adaptive_mdl heap overflow FIXED (candidate-rank histogram indexing
  + small-table O(G) rescan; byte-identical vs repair-1 on 100KB); all 11 arms × 2 corpora byte-identical
  vs closeout goldens (10/10 MATCH); `rank_table_repaired.json` still records binding_verdict: FAIL
  (raw_micro rank 8/11 incl. informational; order_ok true, dead_last_ok false) — repair changes the crash,
  not the FAIL.

## 11. teachers/arm3/varC/evidence/EVIDENCE_INDEX.md — REVIEW: PASS
- varC battery: N=5 byte-identical; 8/8 heap perturbations; 19 hostile §P histories (exits 1–6,8,9,10;
  forged proposal → 21); §C clean/smuggle/vocab probes; E vs independent Python reference (24/12/28/24
  events); selfcheck recorded==recomputed on A/B/adopt14/reject12. All PASS.

## Blocked / open items
- b_t3_leg1.md dose table needs regeneration (generator artifact; numbers exist in FORMAL_VERDICT_R4.md).
- Stale PREREG text ("PROPOSED — NOT FROZEN") in the local R0 prereg copy contradicts the signed-freeze
  instruction; the harness VERDICT_SHEET flags it — prereg not edited (needs Micah's structural word).
- METRICS.md vs ARM_INTERFACE.md scorecard schema conflict (flags as strings vs JSON booleans, m2_etc keys)
  — flagged by harness and B-T1, needs Micah's ruling.
- grok-4.7 hard down (429 insufficient_credits since 2026-09-21 23:31; org −$0.02) — coordinator cron owns
  re-probing; needs Micah's top-up (spending — not attempted).
- No other rows blocked. Nothing committed, no MANIFEST_ITEMS.tsv edits, no cron jobs, no external contact.
