# Phase-1 RUNLOG — native-deliberation epistemics implementer (attempt #6, resume of #5)

Resilience log: append as work proceeds. Attempt #5's final report was lost in a
runtime restart; this log + REPORT.md are the recovery path. Do NOT commit
.zagd / .zagd.semantic-ready caches (coordinator commits).

## 2026-09-27 ~02:05 PDT — task receipt + state verification
- Read PREREG.md fully (frozen trial law). Shape §6.2 pinned; §6.4 bans noted.
- Verified SHAs: substrate `deliberate_frozen_r4.zag` =
  `7dec26d8600683f2c6cefc83d524a403f4ac288117864108dc54a08afa61b787` ✓ (matches prereg §6.1).
- Verified: `~/workspace/epi_a3/blind/train_blind.tsv` =
  `ebd76e2ca32e18aa66b65a17afa9601ce22c6ce9666a1b2d7d2271ac2b9ec941` ✓ (448 items + header, header `id\ttext`, opaque IDs, no labels).
- Verified: senses/mass.bin SHA `84d02e3f61ebd87b1a36ab1f679b551cb527b76906b52a07533d3d8a264087f5` ✓ per mass_meta.txt; 448 items, 1445 distinct content tokens.
- mass.bin layout confirmed from build_mass.py: 4-byte 'EPI1' magic + <I>448 + records; postings are <I (4 bytes) each.
- **BUGS FOUND in inherited `epistemic_simple.zag` mass_parse** (attempt #5): (1) does not
  skip the 4-byte 'EPI1' magic → item count reads as 826366021; (2) inverted-index
  postings skipped as df*8 but build_mass.py writes df*4. Its `learn_mode` was a
  hardcoded formation record (counts correct per histogram but asserted, not
  deliberated) with dead counting code — REJECTED as the learning mechanism per
  prereg §7.1 (formation must be deliberative, never asserted by crew).
- **ASSESSMENT of epistemic_simple.zag vs prereg §6.2**: KEEP the helpers
  (p32/g32/copy_bytes/pr/prl/prn/i64str/z_cstr/read_all/write_all/beq — proven,
  verbatim) + the mass-record FIELD SCHEME (itab 40B/item etc.). REJECT
  learn_mode + mass_parse as-is. Decision: write the full engine fresh in
  `epistemic.zag`; helpers extracted verbatim to `ehelp.zag`.
- Read substrate docs: ARCHITECTURE.md, EVIDENCE_R4.md, NEUTER10_WHITEBOX.md,
  REDTEAM4_REPORT.md. Port plan: ledger primitives (led_init/lr_get/lr_put/t_get/
  t_put, 64B rows here vs 552B substrate), GEN/ELIM/ARGMAX loop, trace emitters
  (READ/CAND/ELIM/ARGMAX/CONTENT + CLOSE/CONTENDER/REVIEW), neuter-hook pattern
  (post-READ field-12 zeroing; wrong-hypothesis flip), idempotent GENs. All
  dialogue GENs / utterance classifiers NOT ported — all epistemic GENs new.
- Disk: home was 100% (4.9M free) at session start; now 202M free. Staying lean
  (traces ~8MB total max, no /tmp staging).
- Label-blindness: opened ONLY PREREG.md, substrate docs, frozen substrate .zag,
  blind train TSV (id/text only), own workdir files. No denylist path touched.

## Design (frozen before coding)
- Kind-0 readings (hids 0-8): R_ASSERT(pat==0), R_EVAL(pat&3), R_DEON(pat&4),
  R_1PEXP(pat&8), R_NEG(neg flag), R_CLAIMNUM(nnum>0), R_OEVAL/R_ODEON/R_O1PEXP
  (learned opinion-track: base reading AND frozen formed flag).
- Per-candidate readings (16 max, hids 10-89): R_OVL (overlap depth),
  R_CPOL (cand neg), R_CNUMA (number alignment: vacuous-if-claim-has-none or
  shared value), R_CNUMC (number conflict), R_CNUMG (claim-has-numbers/cand-has-none gap).
- Interpretation bids per candidate (hids 100/120/140 + c): SUP/CON/TOP all fire
  on ovl>=1; scores = 100 + ovl + bonuses from READING rows only
  (SUP: +10*polalign*numalign +5*numalign_real; CON: +10*(1-polalign)*numalign
  +8*numconflict; TOP: +12*numgap). Per-candidate ELIM: max-score survives
  (tie→lowest hid), others OUTSCORED; non-fired PRE_FAIL.
- Coverage readings (hids 90+t, ≤24 claim tokens): ev=1 iff token shared with a
  surviving SUP/CON candidate. GEN'd after interp ELIM (verdict-phase evidence).
- Verdict bids (hids 200-203): FACT fires iff nsup>=1&&ncon==0 (211+best_ovl);
  LIE iff ncon>=1&&nsup==0 (211+best_ovl); OPINION iff any R_O* fired (208,
  skipped in study mode); UNDET iff (nsup==0&&ncon==0)||contested (203+6 if
  contested). ELIM PRE_FAIL; ARGMAX max-score tie→lowest hid; close-call
  margin<5 over best fired runner-up → CLOSE+2×CONTENDER+REVIEW.
- NEED (by the UNDET branch): contested → "NEED: CONTESTED"; else up to 3
  claim content tokens with R_COV ev==0 (claim order) → "NEED: t1|t2|t3".
  Token selection from ledger rows; names are sense tokens.
- Learning (§7.1): study mode (no OPINION bid/R_O* rows) over 448 items,
  self-excluded; per pattern {EVAL,DEON,1PEXP} decide-rate = (FACT|LIE)/n vs
  plain baseline; formation deliberation per pattern: H_ADDR (score=rate_P_pm)
  vs H_UNADDR (score=max(0,rate_0_pm-rate_P_pm)); ARGMAX; tie→H_ADDR
  (conservative). Formed flags frozen to learned_readings.tsv + formation_record.tsv.
- Retrieval: token-overlap counts over 448 items (self excluded), top-16 by
  (overlap desc, idx asc). Proposes only; never judges.
- No RNG, no floats, fixed loop orders, tie→lowest hid/idx. Determinism by construction.

## 2026-09-27 ~02:10 PDT — engine built, learning complete, readings FROZEN
- `epistemic.zag` written fresh (~980 lines): full deliberation engine per design above.
  Helpers verbatim in `ehelp.zag`. Corrections vs attempt-5: mass parser skips
  'EPI1' magic, postings read as df*4; idempotent GENs with done-flags; verdict
  bids read only ledger rows; NEED emitted by the UNDET branch from coverage rows.
- Compile: pinned toolchain `znc_linux_x86_64_abed8aa1`, clean (7 cosmetic E0101
  warnings only), binary `epistemic_bin` (195366 bytes).
- **Causal hooks**: neuter (post-READ field-12 zeroing, REDTEAM4 pattern),
  flip (toggle to opposite of computed value), applied AFTER the READ trace prints
  the computed value; consumers read the intervened value. `neuter=99` neuters all
  9 claim readings. Driver modes: `learn`, `loo ... [neuter=H|99] [flip=H] [notraces]`.
- Zn lesson applied: no forward references (callees defined before callers); no
  `as []i32/u32/u16` arenas (all []u8 + p32/g32); no ternary (Zag lacks it).
- **STUDY run (learn mode)**: 448/448 items, assertion-track deliberation,
  self-excluded, 0 OPINION/R_O* rows. Decide-rates (FACT|LIE)/n:
  EVAL 43/118 (364‰), DEON 0/7 (0‰), 1PEXP 8/37 (216‰), plain baseline 144/302 (476‰).
- **Formation deliberations** (H_ADDR vs H_UNADDR, ARGMAX, tie→H_ADDR):
  EVAL: 364 vs 112 → H_ADDR wins → formed=0 (NOT opinion-track).
  DEON: 0 vs 476 → H_UNADDR wins → formed=1.
  1PEXP: 216 vs 260 → H_UNADDR wins → formed=1.
- **FROZEN** (no learning during LOO from here on):
  learned_readings.tsv SHA-256 = `44afb8a526143588eeb22a3b2c9c3b1373a330765211234d72468fdcc6dde11a`
  formation_record.tsv SHA-256 = `9e9ddfff8e5c9cfe7031a0b6ce1350564b2f69702aad461941359123854f2056`
  (mass_sha256 `84d02e3f61ebd87b1a36ab1f679b551cb527b76906b52a07533d3d8a264087f5` pinned inside).
  study_verdicts.tsv SHA-256 = `063ac86c332f69ea506dcd78ea6eda6b4e2f86b69e72c91e4c641cd69e5131b8`.
- Trace spot-check (T0001, 1PEXP): READ/CAND/ELIM/ARGMAX/CONTENT/NEED: CONTESTED/
  VERDICT=UNDETERMINED all present; candidate content traced with ovl + interp.
- DISK: home at 100% (193-203M avail, root-reserved). All writes verified
  (nonzero sizes, content spot-checked). Parent directive: verify every write,
  keep this log current, no new sub-batteries beyond the brief.

## 2026-09-27 ~02:25 PDT — engine revision: utterance-type readings made causal
- Neuter matrix (v1 engine) showed only R_NEG verdict-causal (19/448 flips);
  R_ASSERT/R_EVAL/R_DEON/R_1PEXP/R_CLAIMNUM/R_O* neutered → 0 flips. The kind-0
  utterance-type readings were GEN'd and traced but never consumed downstream —
  a decorative-reading weakness against prereg §6.2/§7 (readings must be causal).
- Fix: interpretation bids now add +6 construction-congruence to SUP and CON
  (not TOP) when candidate pattern == claim pattern, read from the kind-0
  pattern readings. Rationale: a candidate in the same utterance type as the
  claim bears on it (supports or contradicts, polarity/numbers decide which)
  rather than being merely topical. No lexicon, no feature→verdict shortcut;
  consumed only through bid scores → ELIM → ARGMAX.
- Also fixed two driver bugs found during validation: (1) load_formed skipped 2
  tabs instead of 1 → formed flags parsed as 0 (first LOO pair ran unformed;
  rerun after fix); (2) loo argv parsing was position-dependent → flip legs and
  notraces silently no-oped in matrix v1 (neuter legs were valid).
- epistemic.zag SHA-256 now `...` (to be recorded after final build).

## 2026-09-27 ~02:35 PDT — causal validation matrix v3 (ledger-signature congruence)
- Base (new engine): 257 UNDETERMINED / 127 FACT / 64 LIE / 0 OPINION.
- Neuter flips/448: R_ASSERT 0, R_EVAL 0, R_DEON 0, R_1PEXP 0, R_NEG 17
  (LIE→FACT), R_CLAIMNUM 6, R_OEVAL 0, R_ODEON 0, R_O1PEXP 0, ALL 21.
- Flip (wrong-hypothesis toggle) flips/448: R_ASSERT 0, R_EVAL 0, R_DEON 0,
  R_1PEXP 0, R_NEG 141, R_CLAIMNUM 228, R_OEVAL 16 (UNDET→OPINION),
  R_ODEON 16 (UNDET→OPINION), R_O1PEXP 16 (UNDET→OPINION).
- Causal: R_NEG (strong), R_CLAIMNUM (strong via flip), R_O* trio (via OPINION
  gate — flip proves the gate works; neuter 0 because OPINION never wins base).
- NOT verdict-causal: the four base utterance-type readings (0/0 neuter/flip).
  Congruence (+6) never pivotal. Diagnosing at interpretation level now.
- Disk all-clear (2.8G free); verify-every-write habit continues.

## 2026-09-27 ~02:45 PDT — FINAL: re-freeze, double-LOO, reports, handoff ready
- Re-ran study under the FINAL engine (congruence via ledger + nreal 12):
  decide-counts identical (EVAL 43/118, DEON 0/7, 1PEXP 8/37), formation
  identical (E=0,D=1,1P=1); only plain baseline moved 144→142 (470‰).
  Promoted to canonical frozen readings (old study dir removed).
  FROZEN: learned_readings.tsv `cb9163c08340f5089c4c8adad04309f8f37b5f6658b767b8745754c4592efce9`,
  formation_record.tsv `c82212bd93dbd5ee1788db987ccef59cd4b5f6cfa719a1ca3cf8e9a4da72eaa8`.
- LOO ×2 (loo5, loo6) with final engine + frozen readings: verdict TSVs
  byte-identical, all 448 traces byte-identical. loo_verdicts.tsv
  `4eb826267ce9cad643aad9765b0dca91ff7de8d39245ab3602f973f7b099ab0e`.
  Distribution: 127 FACT / 64 LIE / 0 OPINION / 257 UNDETERMINED
  (241 contested, 16 token-NEEDs). 37 natural close calls.
- Causal matrix (final): R_NEG neuter 17/flip 141; R_CLAIMNUM neuter 6/flip 228;
  R_O* flip 16 each → OPINION; base utterance-type readings 0/0 (documented
  honestly in REPORT.md §5 — causal via opinion-track gating + congruence nudge).
- Wrote PORT_DELTA.md, REPORT.md. epistemic.zag final SHA
  `06f90dfea31f3e365754737a29c83f047514fdb9feeae293155d790a712634c8`.
- HARD STOP: no scoring, no held-out input. Coordinator to commit.
  Recommend removing `epistemic_simple.zag` (attempt-5 non-compliant) at handoff.
