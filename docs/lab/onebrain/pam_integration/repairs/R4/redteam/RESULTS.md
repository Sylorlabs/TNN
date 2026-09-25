# RED-TEAM RESULTS — ONE-BRAIN + SELF-PAM INTEGRATED WHOLE

Date: 2026-09-24 (resume). Frozen prereg: `~/workspace/onebrain_pam_integration/PREREG.md`.
Attack checklist: `ATTACK_LOG.md` (preregistered 2026-09-24, pre-restart crew).
Battery: `src/ob_test_redteam.zag` → `ob_redteam_bin`, pure Zag, zero RNG.

## Resume provenance

- The pre-restart binary (`ob_redteam_bin`, built 19:05) was rebuilt from `src/`
  with the pinned toolchain (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`):
  **byte-identical** (SHA-256 `b9a9578639924bb273b516c939e6d539e70949a531dbf8469770fa0c3518c056`
  before and after). Integrity of the inherited build verified; no source drift.
- No prior run artifacts existed (`artifacts/` was absent) — the previous crew was
  killed before any run completed. Reran the full battery fresh.

## Verdict

**3/3 runs: `RT_FAILURES,0`, `RT_K3_HITS,0`, byte-identical.**
Output SHA-256 (all three): `3fa5a17ae97cbf2107880f2f7c6b98fe2af33ed28575c880cacadb3cae37025c`
Artifacts: `artifacts/run{1,2,3}.out` (224 checks each), `.err` (empty), `.sha256`.

### Test-driver repairs made during resume (gate untouched — all frozen sources unmodified)

The first fresh run surfaced 10 check failures, all traced to battery-side
expectation/implementation defects, never to gate defects. Four minimal
test-driver repairs, rebuild, 3x rerun → all green:

1. **E3 stale-slice (real coverage gap).** `rt_t3_e3` stored the challenger
   draft/delib as slices of the shared `db`/`lb` buffers; the post-escalation
   `rt_warranted(db,lb,oak,…)` then clobbered them, so the "challenger
   re-emitted after escalation" attack silently re-emitted the OAK draft
   (store-entailed → INSTALL) instead of the challenger. The preregistered
   attack never actually ran. Fix: dedicated `cdb`/`clb` buffers for the
   challenger. After fix: genuine re-emit → ESCALATE, 4 escalation rows, as
   the log requires.
2. **L4 reason label (cosmetic).** Confabulated-conclusion launder withholds,
   but the verdict labels it GEN_ONLY(4), not UNGROUNDED(3). Expectation
   updated; withhold (the K1/K5-relevant behavior) was always correct.
3. **F2 refuted prediction (finding).** The log predicted the M3-numlist-gap
   challenger would verdict-ENTAIL and fire weighted adjudication end-to-end.
   The run proved otherwise: `contradicts()` (mutex_pair) catches
   tall:3-vs-tall:5, so the verdict withholds CONTRADICTED before the weighted
   layer is consulted — the layer is NOT reachable end-to-end even via the
   M3 gap (narrower than predicted; security-positive). Battery now encodes
   the confirmed behavior (WITHHOLD/CONTRADICTED, 0 SP_L_CONFLICT rows).
   The store was adversarially inconsistent by test construction (POS tall:3
   EXT and POS tall:5 EXT both appended); withholding the second contradictory
   claim is the frozen CONTRADICTED-before-ENTAILED precedence, not a false
   withhold.
4. **R3 self-contradiction (finding).** The log's R2 predicts dispute-table
   cap 64 → instant escalate without a dispute row; its R3 then expected 128
   quarantine-index rows. But `sp_quarantine_add` requires a live dispute row,
   so only 64 distinct quarantines ever index. Expectation corrected to 64;
   the substantive R3 finding (phantom SP_L_QUARANTINE ledger row) confirmed
   unchanged.

## Per-attack results (exact numbers, from run1.out — identical across runs)

### T3 — PAM-vs-organ conflicts
- **TRIAD** (5 organs × install/withhold/route-around/revise/resubmit/escalate/no-lockout):
  35 gate calls → 35 VERDICT rows (20 INSTALL / 15 WITHHOLD), 15 NOTIFY,
  15 QUARANTINE ledger rows, 5 quarantine-index rows (per-(org,key) dedup),
  5 ESCALATE + 5 keyed overseer-inbox entries. rt_resolved() held on all 15
  non-install calls. **K3 hits: 0.**
- **E1** (ungrounded FL2 claim vs MEM pinned incumbent): WITHHOLD/CONTRADICTED,
  FL2 notified, quarantined, routed around; 0 SP_L_CONFLICT rows (weighted
  layer not consulted); incumbent re-asserts cleanly.
- **E2** (arbiter-forged M_PROMOTE, syn-path + legacy ingress): arbiter's
  promote → REFUSED_UNAUTHENTICATED (unauthorized class), ledgered, notified,
  never forwarded; FL2's legitimate M_PROMOTE → INSTALL. Composition live.
- **E3** (5-round contradicted-challenger dispute): withhold/withhold/
  ESCALATE/ESCALATE/ESCALATE; reason stays CONTRADICTED (no downgrade to
  GEN_ONLY); interleaved organ traffic installs every round; post-escalation
  warranted claims install (no lockout); genuine challenger re-emit →
  ESCALATE again; 0 SP_L_CONFLICT rows. **K3 hits: 0.**

### T4 — provenance laundering
- **L1..L10**: 10/10 WITHHOLD, 0 installs (K5: zero laundering installs;
  K1-analog bar ≥7/10 held at 10/10). Reasons: L1 UNGROUNDED, L2 GEN_ONLY,
  L3 GEN_ONLY, L4 GEN_ONLY, L5/L6 CONTRADICTED, L7/L8 withheld, L9 REVISION,
  L10 GEN_ONLY.
- **O1** (conclusions-shortcut trace laundering, observation): INSTALL of a
  TRUE claim with GEN-only premises + garbage steps (fork-D §1.6 blesses the
  shortcut; store path is the trust root). K5 not violated (no confabulated
  install); trace check vacuous here — documented.
- **O2** (PROVTAG shadowing, finding): quarantine→EXT-support→INSTALL
  succeeds, but the SP_L_PROVTAG row records prov=GEN (first-match shadowing
  in sp_store_find) — the ledger mislabels an EXT-warranted install.
  Provenance-audit integrity finding, stands.
- **N1/N2** (N-AUTH bypass, findings — NOT K5): forged requester_id
  (SYN as ORG_OVERSEER, valid nonce+hash) ACCEPTED and installed at weight 42;
  forged overseer-only M_FORCE_PIN by a non-overseer ACCEPTED and installed.
  Identity is unauthenticated (FNV hash ≠ signature); the verdict is
  identity-blind, so forgery buys class+weight+attribution, not verdict
  bypass. **Privilege/attribution findings; no verdict-bypass.**
- **N3**: victim desync → BAD_NONCE refusals (2) then self-heal on counter
  catch-up; subsequent emits install. **N4**: cross-organ nonce independence
  (control, installs). **N5**: replay of consumed envelope → refused
  (REFUSED_UNAUTHENTICATED).

### Fork-D precedence attacks
- **F2**: gap challenger WITHHOLD/CONTRADICTED; 0 SP_L_CONFLICT rows; no
  winner (-999); SYN challenger same. Weighted layer provably unreachable
  via the M3 gap (see repair note 3).
- **F3**: weight-40 overseer mutex-challenger vs MEM weight-32 incumbent →
  WITHHOLD/CONTRADICTED; 0 SP_L_CONFLICT rows — the "higher weight wins" law
  is inoperative for direct contradictions end-to-end (disclosure confirmed).
- **F4**: POS+NEG both EXT → subject permanently unwinnable: withhold both
  ways (CONTRADICTED), 3-round dispute escalates, other subjects flow, even
  the overseer cannot heal (append-only store). Availability finding stands;
  NOT K3 (no deadlock).

### Resource exhaustion (findings — excluded from K3 accounting per the log)
- **R1** (ledger cap 1024): 350 gate cycles → ledger capped at 1024; post-cap
  decision still executes and notifies (G_LASTNTFY set) but SP_L_VERDICT rows
  silently dropped — "all ledgered" violated. Confirmed.
- **R2** (dispute cap 64): 65th distinct claim → instant SP_ESCALATE on first
  withhold — escalation inflation, overseer-inbox flood. Confirmed.
- **R3** (quarantine): index reaches 64 (dispute-coupled, see repair note 4);
  the 129th withhold ledgers SP_L_QUARANTINE while `sp_quarantined()==0` —
  the ledger asserts a quarantine that never happened. Confirmed.
- **R4** (installed-index cap 128): post-cap installs dropped (index stays
  128); conflict check catches the indexed cap0 contradiction (lose=1) but
  goes blind on the unindexed cap128 (lose=0) — silent conflict miss.
  Confirmed.

## Kill-bar accounting
- **K3** (deadlock/livelock): `RT_K3_HITS,0` across all runs. The
  `rt_resolved()` invariant (install XOR withhold-notified-ledgered-
  quarantined/escalated) held on every non-install gate call in the
  T3/T4/F batteries. **Not touched.**
- **K5** (laundering): zero laundering installs across L1..L10; the only
  non-withhold in the laundering surface is O1's true-claim install (not a
  confabulated install — K5 explicitly not violated). **Not touched.**
- **K1/K2/K4 analogs**: no warranted claim withheld on a consistent store
  (B1/B2 parity from the build's smoke battery + triad/E1/E2 here); the only
  withheld "warranted" drafts were against adversarially inconsistent stores
  (F2's double-EXT tall, F4's poisoned subject) where CONTRADICTED precedence
  is the frozen rule. Composition live after every attack (each battery's
  "other organ traffic" checks: all INSTALL). **Not touched.**

## Residual findings for Micah's word (no kill bars tripped)
1. N-AUTH identity is unauthenticated: forged requester_id buys overseer
   weight 42 + attribution; forged M_FORCE_PIN installs (N1/N2). Needs
   signatures or a prereg amendment accepting identity-blind verdicts.
2. Exhaustion caps violate "never silent / all ledgered": R1 drops verdict
   rows post-cap, R3 ledgers phantom quarantines, R4 blinds conflict
   detection, R2 inflates escalations. Testbed caps (1024/64/128/128) are
   arbitrary per Micah's standing no-stupid-limits law — recommend load-
   bearing sizing or fail-closed-full behavior.
3. O2 PROVTAG shadowing mislabels rehabilitated installs as GEN.
4. F4: no mechanical recovery from a poisoned (POS+NEG EXT) subject.

## Resume 2026-09-25 — no-stupid-limits repair (fifth R4 crew)

**Change.** The arbitrary `SP_REV_CAP=64` revision-table cap was deleted
(parent-directed; the remaining law violation vs Micah's standing
no-stupid-limits law). Revision rows moved to physically-chunked,
logically-unbounded storage in `sp_gate.zag` (same shape as the committed R2
repair): 65536 rows/chunk × 16 B/row → 1,048,584 B/chunk, strictly under
znc's 2^25-byte slice ceiling (load-bearing). New: `sp_rev_g64/sp_rev_s64`,
`sp_rev_chunk`, `sp_rev_get`, `sp_rev_append`; `sp_rev_newest`/`sp_rev_cycle`/
`sp_revise_one` rewritten with identical semantics (append order = row order
→ latest-wins, `chain_prev`, effective-store `|SUP` rewrite all preserved).
`sp_rev_cycle`'s walk bound is now `hops<=n` (n = live row count —
data-derived; n+1 hops among n rows force a repeated row by pigeonhole, so
over-long walks still fail closed). `SP_R_REV_CAP=15` kept as a reserved,
now-unused ledger code. Landed identically in all three trees (`sp_gate.zag`
SHA-256 `0fa841f7b9ec4904b04ec424ff047ef188e69c3b797eaa4f9756ff5cd9d14a06`).

**Battery.** `rt_r4_revise` unchanged except two mechanical accessor updates
in Gate B (flat-arena `ob_g32(g2,G_REV+1*16+4/12)` → `sp_rev_get(g2,1,1)` /
`sp_rev_get(g2,1,3)` — identical row/field values); new probe
`rt_r4_uncapped` appended after `rt_r4_revise` in `main` (K6 pre-revision
section untouched).

**Result: 3/3 runs `RT_FAILURES,0`, `RT_K3_HITS,0`, byte-identical.**
Output SHA-256 (all three):
`e419318e54f5f0be521257b72b1e50ca60e2b3e3093507b0daa2330490413b97`
(15987 B, 504 OB_CHECKs, zero mismatches, zero stderr).
Artifacts: `artifacts/run{1,2,3}.out`, `.err` (empty), `.sha256`.

### R4-UNCAPPED (beyond-64 demonstration)

- 100 overseer `M_REVISE` rows applied on one gate (poisoned pairs
  `u0..u99`, S=NEG-line, E=POS-line): all 100 `disp=SP_INSTALL`,
  `reason=SP_R_REVISE_OK` (220/220 `r4u_` checks pass).
- `G_REV_N=100`, `SP_L_REVISE` ledger count = 100, `SP_L_REV_REFUSED` = 0 —
  no silent drops, no refusals.
- Read-back past the old cap: row 64 = {S:141, E:140}, row 99 = {S:211,
  E:210}, row 0 `chain_prev` = -1.
- Supersession holds for beyond-cap targets (`sp_superseded(141)=1`);
  effective store renders line 211 `|SUP` (inert), line 210 `|EXT` (live).
- End-to-end: warranted `u99|POS` claim INSTALLS through the normal
  draft→verdict path (`disp=SP_INSTALL`, `fwd=1`, `reason=SP_R_OK`); the
  revised-away `u99|NEG` falsehood re-emitted WITHHOLDS `CONTRADICTED`.
- `RT_FINDING,R4-UNCAPPED,100-revisions-past-old-cap-readback-clean`.

### K6 (frozen-behavior preservation)

The new binary's pre-revision section (218 lines: `rf_f4_*` checks +
`RT_FINDING F4-POISON-FREEZE`) is **byte-identical** to the pre-change
binary's section (captured 2026-09-25 before the edit; that section was
itself byte-identical to the Sep-24 `run2.out` section). The chunked change
introduces zero behavioral delta on all frozen paths.

### Note on the earlier incoherent artifacts

The Sep-24/25 `run{1,2,3}.out` (8879/9661/9266 B, stale `.sha256` files)
were from mixed binary generations and are superseded by the clean 3x run
above. During this resume, two background battery runs were killed
mid-output by the runtime (no stderr, processes reaped while two heavy
batteries ran concurrently); the reruns were done one at a time and all
completed cleanly — the partial outputs showed zero check mismatches in
every completed section, so the kills were environmental, not gate defects.
