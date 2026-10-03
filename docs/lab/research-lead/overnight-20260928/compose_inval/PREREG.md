# PREREG: Contract Re-Teaching With Genuine Bit Invalidation

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Step 0) strictly precedes all implementation.

## 1. Question

C341 (PERSISTENT LEDGER HELPS (BOUNDED)) left one follow-up open: the Q3
staleness test used a different query (shift), not a changed world. The
unbounded-lifetime choice (U3: the ledger is never cleared while the MAP
table is stable) was never tested against a genuinely false bit. This
battery changes the WORLD mid-lifetime: after Q2 (where persistence helped),
MAP X (id2) is RE-TAUGHT with a changed contract, so the carried ledger bit
(m2,out,1) becomes GENUINELY FALSE. The test: does the persistent ledger
adapt, poison future queries, or sit inert? Does any mechanism correct the
false bit? Can the learner detect its staleness?

## 2. Frozen background (not under test)

- C338 HYBRID MATCHES BEST (R1 coverage-selective WTRIG=2 + R2 blind
  backstop WTRIG=1); C341 PERSISTENT LEDGER HELPS (BOUNDED): Q1 seed
  2/6/1/2/44, Q2 transfer P 2/3/1/3/44 vs N 2/6/1/2/44, Q3 staleness P
  2/4/1/3/-1 vs N 2/1/0/0/-1; ledger ends (m2,out,1) carried verbatim.
- C319 SUBSUMPTION, C325 independent reproduction, C329 S2 pin (empty
  kind-set reads as universal {1,2} in all three admission positions;
  FROZEN, used here, not re-litigated).
- Shared semantics: S2-pinned admission; ordered trial execution; end to
  end verification; Amendment-2 success-recording into contract masks;
  missbits[m][p] populated from FAILED trials only; kinds 1=NODE, 2=NUM;
  3/3 byte-identical runs per arm.
- The U1-U5 persistent-ledger rules are FROZEN and copied verbatim: U1 zero
  at init; U2 idempotent lg_add on failed trials; U3 never cleared between
  queries; U4 priming of filter-rejected, untried, carried-ledger-justified
  pairs (WTRIG=3) before admitted singles; U5 R1/R2 unchanged with WTRIG
  precedence 3 > 2 > 1 > 0.
- The compose_ledger lane is NOT modified. This lane copies its source and
  works only under compose_inval/.

## 3. Invalidation protocol (frozen)

### 3a. World change: setup_d5x (contract re-teach)

setup_d5x = setup_d5 facts and teaching, PLUS one added teaching step for
MAP X (id2, WALK on rel 81):

  teach(A,2,41,44)

Under D5 facts, X(41) walks 41->42->43->44 and 44 IS a subject (facts
(44,83,441),(44,83,442) exist), so the added teaching observes in-kind NODE
(41 is a subject) and out-kind NODE (44 is a subject). X's taught contract
changes from inmask {1}, outmask {2} to inmask {1}, outmask {1,2}.
Facts are unchanged; only the teaching (the contract) changes.

### 3b. Why the carried bit becomes genuinely false

The ledger bit (m2,out,1) records the standing claim "X emitted kind NODE
at out outside its taught contract". Under D5 this was true: X's outmask
was {2} and X(41)=44 emitted NODE. Under D5X, X's outmask is {1,2}: NODE at
out is WITHIN the taught contract. The bit's claim is now false as a
standing behavioral fact about X. The ledger still carries it verbatim (U3);
no rule re-validates carried bits at query start.

### 3c. Query sequence (frozen)

- Q1 SEED: D5, s=41, kin=1, kout=2, exp=2, nm=4. Reproduces C341 Q1.
- Q2 TRANSFER: D5, s=42, kin=1, kout=2, exp=2, nm=4. Reproduces C341 Q2
  (persistence helps while the bit is true).
- Q3P INVALIDATION: D5X, s=42, kin=1, kout=2, exp=2, nm=4. Same start and
  shape as Q2, so the ONLY difference from Q2 is the re-taught contract.
  Q3P touches the invalidated MAP directly: the m2 single trial that
  recorded the bit in Q1 is tried again under the new contract.

Arms: P (persistent ledger, U1-U5, ledger carried Q1->Q2->Q3P verbatim) and
N (frozen hybrid control, fresh ledger per query), same as C341.

### 3d. Frozen structural derivation: contract-growth invalidation is self-shielding under U4

Claim: on D5X, the false bit (m2,out,1) CANNOT prime any pair.

Proof. The carried ledger holds only (m2,out,1). Priming (U4) admits a
pair (x,y) only if it is filter-rejected (admit_pair(x,y,kin,kout)==0) AND
justified by the carried ledger under p_justified. With only (m2,out,1)
set, justification is possible only for x=2 via the first disjunct
(missbits[2][out] intersects u_eff(y.inmask) nonempty; the second disjunct
needs missbits[2][in] nonempty, which is empty) . For such a pair,
p_justified's preconditions give k_has(inmask_2,kin)=1 and
k_has(outmask_y,kout)=1, and justification gives kind 1 in u_eff(y.inmask),
i.e. y.inmask covers 1 (or is empty, which the S2 pin reads as {1,2}).
The re-teach gives outmask_2 covering 1. Hence
k_inter(outmask_2, inmask_y) is nonzero on kind 1 (both masks nonzero, or
the S2 pin applies), so admit_pair(2,y,kin,kout)=1: the pair is
filter-ADMITTED, and U4 excludes it from priming. Therefore priming admits
nothing on Q3P; the false bit is structurally inert. The same argument
covers every future query until some further world change alters the masks.

Corollary: no correction exists either. The only ledger write in the frozen
code is lg_add (idempotent set); there is no lg_del, no clear, no decay,
and U3 forbids clearing. A false bit persists verbatim forever; it can
neither be corrected nor, by the Claim, prime while its falsifying contract
growth stands.

## 4. Frozen predictions

Format: ANS / TRIES / WIDEN / WTRIG / INTER ; WBACK in parentheses for P.

| Query | P (persistent) | N (control) |
|-------|----------------|-------------|
| Q1 | 2/6/1/2/44 (0) | 2/6/1/2/44 |
| Q2 | 2/3/1/3/44 (0) | 2/6/1/2/44 |
| Q3P | 2/7/0/0/44 (0) | 2/7/0/0/44 |

Derivations (frozen):
- Q1/Q2 both arms: byte-identical to the C341 Q1/Q2 blocks (same code,
  same world, same labels). P-Q2 priming fires on the TRUE bit (WTRIG=3,
  WADD=2,0 / 2,1 / 2,3); N-Q2 re-derives via R1 (WTRIG=2).
- Q3P P: priming admits NOTHING (Section 3d Claim): no WIDEN line,
  WTRIG=0. Admitted singles in id order: m0 try 1 (A(42)=-2), m1 try 2
  (B(42)=-2), m2 try 3 (X(42)=44, INTER=44; out-kind NODE now COVERED by
  outmask {1,2}: miss_bit returns 0, no new miss, no R1; this is the
  invalidation signature), m3 try 4 (Y(42)=-2). Admitted pairs: only
  (2,0),(2,1),(2,3) are filter-admitted on D5X (X.outmask {1,2} now meets
  every inmask {1}; all other pairs still junction-rejected): try 5 (2,0)
  v1=44 v2=A(44)=-2 (44 has no rel-82 facts), no miss; try 6 (2,1) v1=44
  v2=B(44)=-2, no miss; try 7 (2,3) v1=44 v2=Y(44)=2=exp SUCCESS, INTER=44.
  TRIES=7, WIDEN=0, WTRIG=0, WBACK=0.
- Q3P N: fresh ledger, no priming by construction; identical trace to P:
  2/7/0/0/44. The re-teach costs +4 tries versus P-Q2 (answer path moves
  from primed pairs to admitted pairs), but P and N pay it equally: the
  ledger confers no advantage and no penalty.

Ledger predictions (exact):
- P after Q1: m2 out=1, all else 0. After Q2: unchanged. After Q3P:
  UNCHANGED (Q3P records nothing; the false bit persists verbatim).
- N at every report: all zero (fresh ledger per query; Q3P records
  nothing).

CENSUS predictions Q3P (both arms, identical): m0 inmask=1 outmask=2 n=2
(teach + success observe); m1 1/2/1; m2 inmask=1 outmask=3 n=3 (two
teachings + success observe); m3 1/2/2 (teach + success observe).

Invalidation-detection prediction (frozen): the Q3P trace CONTAINS the
detectable staleness signal (m2 single trial INTER=44, NODE at out, zero
new misses, zero WADD/R1 lines) while the carried bit claims NODE-at-out
is outside contract; the composer takes NO action on it (no flag, no
clear, LEDGER block after Q3P byte-identical to after Q2). Detection
machinery does not exist under frozen U1-U5; the signal is present and
unacted upon.

## 5. Frozen kill bars

- K1 SEED FIDELITY: P-Q1 and N-Q1 blocks byte-identical to the
  compose_ledger lane Q1 blocks; P-Q2 = 2/3/1/3/44 (0) with WTRIG=3 and
  WADD=2,0 / 2,1 / 2,3; N-Q2 = 2/6/1/2/44 with WTRIG=2. 3/3.
- K2 TRANSFER REPRO: P-Q2 strictly fewer tries than N-Q2 (3 < 6),
  ANS=2 both. Confirms the bit was genuinely true and helpful before
  invalidation. 3/3.
- K3 INVALIDATION INERT: P-Q3P = 2/7/0/0/44 (0) and N-Q3P = 2/7/0/0/44,
  byte-identical modulo the ARM label; ZERO WADD lines in both Q3P blocks;
  WTRIG=0 in both. Poison cost exactly 0 tries. 3/3.
- K4 STALE BIT PERSISTS: P LEDGER block after Q3P byte-identical to P
  LEDGER after Q2 (m2 out=1, all else 0); N LEDGER all zero after Q3P.
  The false bit is never corrected. 3/3.
- K5 NO DETECTION: the Q3P block shows the m2 single trial with INTER=44
  and no WADD/R1 lines anywhere in the Q3P block, AND the post-Q3P LEDGER
  block is byte-identical to the post-Q2 LEDGER block (signal present,
  machinery absent). 3/3.
- K6 DETERMINISM: 3/3 byte-identical whole-output per arm; sha256 recorded.
- K7 HYGIENE: zero em/en dash bytes in all docs (byte-verified); safebin
  guard attested in NAMECHECK.md Step 0 (which python3/python return
  NOTHING); pure Zag for all scientific computation; pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1; compose_ledger lane
  untouched (verified via git status); all new files under compose_inval/;
  no mode/policy identifier in the composer (grep over non-comment lines).

## 6. Frozen verdict mapping

- K1-K7 all PASS: CONTRACT RE-TEACHING LEAVES AN INERT STALE BIT
  (SELF-SHIELDING). The genuinely-false bit persists verbatim forever (no
  correction path exists under U1-U5) but cannot prime: U4's
  filter-rejected gate and the justification predicate jointly exclude it
  (Section 3d derivation verified exactly). Poison cost is 0 tries. The
  unbounded-lifetime choice survives contract-growth invalidation; the
  residual cost is latent ledger pollution, not active harm. The learner
  cannot detect the staleness (K5): the signal is in the trace, the
  machinery is absent.
- K3 fails with P worse than N on Q3P, or any WADD/WTRIG=3 in a Q3P
  block: LEDGER POISONS UNDER RE-TEACHING, or the Section 3d derivation is
  wrong; diagnose, do not claim.
- K4 fails (bit cleared, altered, or corrected): an undeclared correction
  path exists; diagnose, do not claim.
- K5 fails the other way (a staleness flag/clearing appears): detection
  machinery exists undeclared; diagnose.
- K1/K2 fail: implementation bug; diagnose, do not claim.
- VOID is terminal (toolchain violation, non-determinism, sealed-world
  inspection, or compose_ledger modified).

## 7. Honest boundaries (pre-declared)

- One re-teach flavor: contract GROWTH falsifying the bit at the
  justifying position. The symmetric "vice versa" case (a bit becoming
  true, or a bit falsified by changed emission facts with the contract
  unchanged) is NOT covered here; the Section 3d shielding argument does
  not apply to behavior-change invalidation, which remains the open
  follow-up.
- Three queries on one world family discriminate the mechanism; they do
  not establish generality of invalidation behavior.
- Expected-answer verification still used (canonical boundary).
- Behaviors are installed as previously-learned MAPs (canonical standing).

## 8. Implementation plan (frozen order)

1. i_base.zag: byte-copy of compose_ledger/l_base.zag plus setup_d5x
   (D5 facts and teaching, plus teach(A,2,41,44)).
2. i_pers.zag: byte-copy of compose_ledger/l_pers.zag with main() changed
   to Q1(D5)/Q2(D5)/Q3P(D5X, s=42); composer fns untouched (U1-U5 frozen).
3. i_ctrl.zag: byte-copy of compose_ledger/l_ctrl.zag with main() changed
   the same way; n_solve untouched.
4. Assemble with cat (i_base+i_pers -> i_full_P.zag; i_base+i_ctrl ->
   i_full_N.zag), compile with the pinned znc, run 3x per arm, record
   sha256.
5. REPORT.md with verdict per the Section 6 mapping.

Zag pitfalls: u8-backed z_alloc; dynamic content formatted into one buffer
with cursor helpers and a single raw-syscall flush (no _zag_print for
dynamic content); if-nesting at most 3; no !(A && B) in while conditions;
as []f64 / as []i64 do not rescale .len.
