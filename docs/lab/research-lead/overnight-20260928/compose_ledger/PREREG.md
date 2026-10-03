# PREREG: Persistent Cross-Query Missbits Ledger for Behavior-Contract Composition

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Step 0) strictly precedes all implementation.

## 1. Question

The hybrid battery (ledger C338, verdict HYBRID MATCHES BEST) left one
follow-up untested: missbits are per-query. The coverage knowledge a query
accumulates evaporates at the next query; only Amendment-2
success-recording persists. This battery makes the missbits ledger persist
across queries and tests two claims: (a) the FIRST query's missbits make a
LATER query faster (fewer tries) than a fresh ledger would; (b) the staleness
cost, when old missbits prime the wrong pairs, is bounded and never corrupts
correctness.

## 2. Frozen background (not under test)

- C319 SUBSUMPTION, C325 independent reproduction, C329 S2 pin (empty
  kind-set reads as universal {1,2} in all three admission positions;
  FROZEN, used here, not re-litigated).
- C333 WIDEN-COMP MIXED; C338 HYBRID MATCHES BEST (R1 coverage-selective
  WTRIG=2 + R2 blind backstop WTRIG=1, WBACK=1 observable).
- Shared semantics: S2-pinned admission; ordered trial execution (admitted
  singles in MAP-id order, then admitted pairs in (a,b) id order);
  end-to-end verification; Amendment-2 success-recording into contract masks;
  missbits[m][p] populated from FAILED trials only, every input a
  learner-observed probe_kind value; kinds 1=NODE, 2=NUM; one TRIAL = one
  single-MAP or one ordered-pair execution; 3/3 byte-identical runs per arm.
- The compose_hybrid lane is NOT modified. This lane copies its source and
  works only under compose_ledger/.

## 3. Persistent ledger design (frozen)

The ledger is learner-owned cross-query state: 32 bytes (4 MAPs x 2
positions x 4 bytes, bit 1<<(k-1) at (m,p)). It is carried verbatim from
query i to query i+1. The world (facts, MAPs, teaching) is re-presented
identically per query, so the ledger is the ONLY cross-query state; contract
growth from success-recording does not leak across queries.

### 3a. Exact update rule (frozen)

- U1 INIT: at learner init (before Q1) the ledger is all zero.
- U2 RECORD: every failed trial in any phase (primed, admitted, widened,
  backstop), for each observed (m,p,k): if kind k is not covered by m's
  taught contract mask at position p, set bit (m,p,k). This is the frozen
  miss_bit rule; lg_add is idempotent, so re-observation is a no-op.
- U3 LIFETIME: the ledger is never cleared, decayed, or evicted between
  queries. Lifetime choice: UNBOUNDED within a stable MAP table (the
  learner's lifetime).
- U4 PRIMING (the experimental manipulation): at query start, before any
  trial, admit every ordered pair (x,y), x != y, that is ALL of:
  (i) filter-rejected (admit_pair(x,y,kin,kout)==0),
  (ii) untried, (iii) kin in u_eff(x.inmask) and kout in u_eff(y.outmask),
  (iv) junction-justified by the CARRIED ledger under the frozen
  justification predicate: (missbits[x][out] INTERSECTS u_eff(y.inmask)
  nonempty) OR (missbits[y][in] INTERSECTS u_eff(x.outmask) nonempty).
  Log WIDEN=1 once, WTRIG=3 once, then WADD=x,y per admitted pair in scan
  order. Try the primed pairs in (x,y) id order with wom=1 BEFORE the
  admitted-single phase. Mark them in the wadmit mask so R1 never re-admits
  them.
- U5 R1/R2 UNCHANGED: the frozen hybrid rules fire exactly as in C338.
  WTRIG precedence, frozen: 3 (ledger-primed) over 2 (R1 selective) over 1
  (R2 backstop) over 0 (none); the first trigger in query order wins.

### 3b. Lifetime justification (why unbounded, not decaying or bounded)

1. A miss bit records a stable behavioral fact about a MAP ("m at position p
   emitted kind k outside its taught contract"). While the MAP table is
   unchanged, the fact stays true; no bit recorded in this battery ever
   becomes false. Staleness here is query-shift (the next query needs a
   different junction), not bit-rot, so decay would destroy true knowledge.
2. Precedent: Amendment-2 success-recording is already persistent and
   unbounded; the ledger is symmetric learner-owned knowledge.
3. Minimal researcher policy: decay or eviction needs a constant (after how
   many queries?) unjustifiable from learner-observable state; a magic
   number is rejected by standing governance.
4. The cost is bounded anyway: priming tries at most the justified-pair set
   (at most nm*(nm-1) pairs), and a wrong primed pair's own misses are
   honest observations, never ledger corruption. The Q3 staleness bar
   measures this bound exactly.

### 3c. Arms

- Arm P (persistent): frozen hybrid composer + U1-U5. Ledger carried across
  Q1/Q2/Q3 via save/restore of the 32-byte region between fresh arenas.
- Arm N (no-persistence control): the frozen hybrid composer unchanged
  (lg_clear per query, no priming), run on the same Q1/Q2/Q3 sequence. This
  is the C338 H arm with a new query sequence; its Q1 must reproduce the
  frozen D5 H values as a fidelity check.

## 4. Queries (frozen)

All three use the D5 world (setup_d5, frozen in the hybrid prereg): facts
(11,81,12),(12,81,13),(13,81,14); (70,82,71),(70,82,72); (75,84,751),
(75,84,752); (60,83,61),(60,83,62); (41,81,42),(42,81,43),(43,81,44);
(44,83,441),(44,83,442). MAPs: id0 A=COUNT(82), id1 B=COUNT(84),
id2 X=WALK(81), id3 Y=COUNT(83); every MAP taught to inmask {1}, outmask {2}
(11->14 ends at 14 which is not a subject, so X.outmask stays {2}; 44 IS a
subject, so a live X miss observes NODE). All 12 ordered pairs are
filter-rejected (outmask {2} vs inmask {1}); all four singles are admitted
for kin=1, kout=2.

- Q1 SEED: s=41, kin=1, kout=2, exp=2, nm=4. Identical to frozen D5.
  Predicted: both arms 2/6/1/2/44 WBACK=0; ledger ends with (m2,out,1); the
  Q1 trace is the persistence seed.
- Q2 TRANSFER: s=42, kin=1, kout=2, exp=2, nm=4. New start node, same query
  shape; X(42)=44 walks 42->43->44, Y(44)=2. Correct pair is again (X,Y) =
  (2,3). The carried bit (m2,out,1) junction-justifies (2,0),(2,1),(2,3)
  under the frozen predicate, exactly the pairs R1 admitted in Q1.
- Q3 STALENESS: s=70, kin=1, kout=2, exp=2, nm=4. A(70)=2, so the answer is
  the admitted single m0 on try 1 with a fresh ledger. The carried bit still
  justifies (2,0),(2,1),(2,3); X(70) walks nowhere (v1=-2), so all three
  primed pairs fail and the query falls through to the admitted singles.

## 5. Frozen predictions

Format: ANS / TRIES / WIDEN / WTRIG / INTER ; WBACK in parentheses for P.

| Query | P (persistent) | N (control) |
|-------|----------------|-------------|
| Q1 | 2/6/1/2/44 (0) | 2/6/1/2/44 |
| Q2 | 2/3/1/3/44 (0) | 2/6/1/2/44 |
| Q3 | 2/4/1/3/-1 (0) | 2/1/0/0/-1 |

Derivations (frozen):
- Q1 both arms: identical to frozen D5 H. m0 try 1 (-2), m1 try 2 (-2),
  m2 try 3 (X(41)=44, out-kind NODE misses outmask {2}, NEW bit (m2,out,1),
  R1 fires: WIDEN=1, WTRIG=2, WADD=(2,0),(2,1),(2,3)); (2,0) try 4 (v2=-2),
  (2,1) try 5 (v2=-2), (2,3) try 6 (Y(44)=2, success). Priming admits
  nothing on Q1 (ledger empty at init, U1).
- Q2 P: priming (U4) admits (2,0),(2,1),(2,3) from the carried bit:
  WIDEN=1, WTRIG=3, WADD=2,0 / 2,1 / 2,3, then tries 1-3: (2,0) INTER=44
  v2=-2 (bit already set, no new miss, no R1), (2,1) INTER=44 v2=-2,
  (2,3) INTER=44 v2=2 success. TRIES=3.
- Q2 N: fresh ledger; m0/m1 fail silent (-2); m2 try 3 re-observes the miss
  (NEW bit on the fresh ledger, R1 fires WTRIG=2, same three WADDs); tries
  4-6 as Q1; success at (2,3). TRIES=6.
- Q3 P: priming admits the same three pairs (WIDEN=1, WTRIG=3, same WADDs);
  tries 1-3: X(70)=-2, INTER=-2 each, no misses recorded (v1<0); admitted
  single m0 try 4: A(70)=2 success, INTER=-1. TRIES=4.
- Q3 N: m0 try 1 success. TRIES=1, no widening events.

Ledger predictions (exact):
- P after Q1: m2 out=1, all else 0. After Q2: unchanged (Q2's misses
  re-observe the known bit; success recording touches contracts, not the
  ledger). After Q3: unchanged (Q3 records nothing).
- N at every report: all zero (fresh ledger per query, lg_clear).

CENSUS spot predictions: Q1/Q2 (both arms): m2 inmask=1 outmask=3 n=2
(teach + success observe grows outmask with the NODE kind), m3 n=2, m0/m1
n=1. Q3 (both arms): m0 n=2, others n=1; all masks unchanged.

## 6. Frozen kill bars

- K1 SEED FIDELITY: P and N on Q1 are byte-identical to each other AND match
  the frozen D5 H block from the hybrid lane (modulo ARM label P/N vs H and
  PROB label Q1 vs D5), including CENSUS, LEDGER, INTER, and WADD lines.
  3/3.
- K2 PERSISTENCE HELPS: P on Q2 = 2/3/1/3/44 (0); N on Q2 = 2/6/1/2/44.
  P strictly fewer tries (3 < 6); ANS=2 in both. 3/3.
- K3 STALENESS BOUNDED: P on Q3 = 2/4/1/3/-1 (0); N on Q3 = 2/1/0/0/-1.
  Harm is exactly +3 tries (the primed-set size), ANS=2 in both; no wrong
  answer, no runaway. 3/3.
- K4 LEDGER ACCUMULATION: Section 5 ledger predictions hold exactly for
  both arms on all three queries. 3/3.
- K5 PRIMING EVENTS: on Q2 and Q3, P logs WIDEN=1, WTRIG=3, then exactly
  WADD=2,0 / WADD=2,1 / WADD=2,3 in that order, before any INTER line; on
  Q1 P logs no WADD and WTRIG=2. 3/3.
- K6 DETERMINISM: 3/3 byte-identical whole-output per arm; sha256 recorded.
- K7 HYGIENE: zero em/en dash bytes in all docs (byte-verified); safebin
  guard attested in NAMECHECK.md Step 0 (which python3/python return
  NOTHING); pure Zag for all scientific computation; pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1; compose_hybrid lane
  untouched (verified via git status); all new files under compose_ledger/;
  no mode/policy identifier in the composer (grep over non-comment lines).

## 7. Frozen verdict mapping

- K1-K7 all PASS: PERSISTENT LEDGER HELPS (BOUNDED). The carried missbits
  make Q2 faster (6 tries to 3) via ledger-primed selective admission; the
  staleness cost on Q3 is exactly +3 tries with no correctness loss; the
  ledger accumulates honestly and never corrupts.
- K2 fails (P Q2 not strictly fewer tries than N Q2): PERSISTENCE NO-HELP;
  report exactly why (e.g. priming misfires, justification mismatch).
- K3 fails (harm != +3, or wrong ANS on Q3): PERSISTENCE HARMS; the
  unbounded-lifetime choice is falsified and the bound in Section 3b is
  wrong.
- K1/K4/K5 fail: implementation bug; diagnose, do not claim.
- VOID is terminal (toolchain violation, non-determinism, sealed-world
  inspection, or compose_hybrid modified).

## 8. Honest boundaries (pre-declared)

- Three queries on one world discriminate the ledger mechanism; they do not
  establish generality of persistent coverage knowledge.
- The MAP table is stable across queries here; bit truth under contract
  re-teaching is untested.
- Expected-answer verification still used (canonical boundary).
- Behaviors are installed as previously-learned MAPs (canonical standing).

## 9. Implementation plan (frozen order)

1. l_base.zag: copy of compose_hybrid/h_base.zag (that lane is not
   touched) plus ledger_copy/ledger_restore (32-byte region at arena offset
   1024).
2. l_pers.zag: frozen hybrid composer fns (copy of h_hyb.zag) + p_justified
   (predicate identical to h_justified), p_prime_scan, p_prime_trial,
   p_solve (per-query reset, NO lg_clear, priming before admitted singles),
   main(): fresh arena per query, setup_d5, Q1/Q2/Q3 stashes, ledger
   save/restore between queries, ARM label P.
3. l_ctrl.zag: frozen hybrid composer fns (copy of h_hyb.zag) + n_solve
   (= h_solve with ARM label N) + main() with the Q1/Q2/Q3 sequence on
   fresh arenas.
4. Assemble with cat (l_base+l_pers -> l_full_P.zag; l_base+l_ctrl ->
   l_full_N.zag), compile with the pinned znc, run 3x per arm, record
   sha256.
5. REPORT.md with verdict per the Section 7 mapping.

Zag pitfalls: u8-backed z_alloc; dynamic content formatted into one buffer
with cursor helpers and a single raw-syscall flush (no _zag_print for
dynamic content); if-nesting at most 3; no !(A && B) in while conditions;
as []f64 / as []i64 do not rescale .len; 2-byte getter discipline where
applicable (no WAV I/O here).
