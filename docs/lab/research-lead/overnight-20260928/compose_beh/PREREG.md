# PREREG: Behavior-Change Invalidation, the True Poison Flavor

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Step 0) strictly precedes all implementation.

## 1. Question

C345 (compose_inval, CONTRACT RE-TEACHING LEAVES AN INERT STALE BIT
(SELF-SHIELDING)) showed that contract-growth invalidation cannot poison:
the same mask growth that falsifies the bit opens the admission junction,
so U4 priming structurally cannot fire on the false bit (poison cost 0
tries). The open follow-up, explicitly not covered by that shielding
argument, is behavior-change invalidation: the MAP contracts (kinds, masks)
stay UNCHANGED while the emission facts change, so a previously-true ledger
bit becomes genuinely false with the admission structure intact. The frozen
prediction: priming SHOULD fire on the false bit at the primed-set try
cost, with no correction (the bit persists). This battery measures the
poison cost exactly and determines whether the unbounded-lifetime choice
(U3) needs an invalidation rule.

## 2. Frozen background (not under test)

- C338 HYBRID MATCHES BEST; C341 PERSISTENT LEDGER HELPS (BOUNDED);
  C345 CONTRACT RE-TEACHING LEAVES AN INERT STALE BIT (SELF-SHIELDING)
  with its Section 3d shielding derivation.
- C319 SUBSUMPTION, C325 independent reproduction, C329 S2 pin (empty
  kind-set reads as universal {1,2} in all three admission positions;
  FROZEN, used here, not re-litigated).
- Shared semantics: S2-pinned admission; ordered trial execution; end to
  end verification; Amendment-2 success-recording into contract masks;
  missbits[m][p] populated from FAILED trials only; kinds 1=NODE, 2=NUM;
  3/3 byte-identical runs per arm.
- The U1-U5 persistent-ledger rules are FROZEN and copied verbatim from
  the ledger lane. The compose_ledger and compose_inval lanes are NOT
  modified. This lane copies the ledger lane source and works only under
  compose_beh/.

## 3. Invalidation protocol (frozen)

### 3a. World change: setup_d5b (behavior change, contract unchanged)

setup_d5b = setup_d5 facts with two changes:

- REMOVE (44,83,441) and (44,83,442): node 44 is no longer a subject.
- ADD (42,82,421) and (42,82,422): A(42) now counts 2.

Teaching is identical to D5: teach(A,0,70,2); teach(A,1,75,2);
teach(A,2,11,14); teach(A,3,60,2). Every MAP keeps inmask {1}, outmask
{2}. No re-teaching. The contract is UNCHANGED; only emission facts
change.

### 3b. Why the carried bit becomes genuinely false

The bit (m2,out,1) records the standing claim "X emitted kind NODE at out
outside its taught contract". Under D5B, X(42)=44 still walks to 44, but
44 is no longer a subject, so X emits NUM (kind 2) at out, which is WITHIN
the unchanged taught outmask {2}. The emission fact changed; the contract
did not. On D5B, X never emits NODE on any input (walk targets 14 and 44
are both non-subjects), so the bit's standing behavioral claim is
thoroughly false.

The admission structure is unchanged (all masks identical to D5), so all
12 ordered pairs remain filter-rejected and the carried bit still
junction-justifies (2,0),(2,1),(2,3) under the frozen predicate. The
compose_inval Section 3d shielding argument does not apply: outmask_2 is
still {2}, so k_inter(outmask_2, inmask_y)=0, the pairs stay
filter-rejected, and U4 priming CAN fire on the false bit.

The old answer path is gone: Y(44)=-2 on D5B (the 83-facts at 44 are
removed), so the (2,3) pair that answered Q2 now fails. The relocated
answer is the admitted single A(42)=2 (new 82-facts at 42), reachable
without any widening.

### 3c. Query sequence (frozen)

- Q1 SEED: D5, s=41, kin=1, kout=2, exp=2, nm=4. Reproduces C341/C345 Q1.
- Q2 TRANSFER: D5, s=42, kin=1, kout=2, exp=2, nm=4. Reproduces C341/C345
  Q2 (the bit is true and helpful here).
- Q3B BEHAVIOR-CHANGE: D5B, s=42, kin=1, kout=2, exp=2, nm=4. Same start
  and shape as Q2; the ONLY difference from Q2 is the changed emission
  facts. Q3B touches the invalidated MAP directly and relocates the
  answer to an admitted single.

Arms: P (persistent ledger, U1-U5, ledger carried Q1->Q2->Q3B verbatim)
and N (frozen hybrid control, fresh ledger per query), same as C341/C345.

## 4. Frozen predictions

Format: ANS / TRIES / WIDEN / WTRIG / INTER ; WBACK in parentheses for P.

| Query | P (persistent) | N (control) |
|-------|----------------|-------------|
| Q1 | 2/6/1/2/44 (0) | 2/6/1/2/44 |
| Q2 | 2/3/1/3/44 (0) | 2/6/1/2/44 |
| Q3B | 2/4/1/3/-1 (0) | 2/1/0/0/-1 |

Derivations (frozen):
- Q1/Q2 both arms: byte-identical to the compose_inval Q1/Q2 blocks (same
  composer fns, same D5 world, same labels). P-Q2 priming fires on the
  TRUE bit (WTRIG=3, WADD=2,0 / 2,1 / 2,3); N-Q2 re-derives via R1
  (WTRIG=2).
- Q3B P: priming admits (2,0),(2,1),(2,3) from the carried FALSE bit:
  WIDEN=1, WTRIG=3, WADD=2,0 / 2,1 / 2,3 in scan order, before any INTER
  line. Try 1: (2,0) v1=44 INTER=44, v2=A(44)=-2; X out-kind NUM is
  covered by outmask {2}, no new miss, no R1. Try 2: (2,1) v1=44
  INTER=44, v2=B(44)=-2, no new miss. Try 3: (2,3) v1=44 INTER=44,
  v2=Y(44)=-2 (83-facts gone), no new miss. Admitted singles in id order:
  m0 try 4: A(42)=2=exp SUCCESS, INTER=-1. TRIES=4, WIDEN=1, WTRIG=3,
  WBACK=0.
- Q3B N: fresh ledger, no priming; m0 try 1: A(42)=2=exp SUCCESS.
  TRIES=1, WIDEN=0, WTRIG=0, WBACK=0, INTER=-1.
- Poison cost: P_Q3B TRIES (4) minus N_Q3B TRIES (1) = 3 tries, exactly
  the primed-set size.

Ledger predictions (exact):
- P after Q1: m2 out=1, all else 0. After Q2: unchanged. After Q3B:
  UNCHANGED (Q3B records nothing; the false bit persists verbatim; no
  correction path exists under frozen U1-U5).
- N: m2 out=1 after Q1 and Q2 (each query's own miss); all zero after
  Q3B (fresh ledger; Q3B records nothing).

CENSUS predictions Q3B (both arms, identical): m0 inmask=1 outmask=2 n=2
(teach + success observe); m1/m2/m3 inmask=1 outmask=2 n=1. The masks
verify the contract is unchanged under D5B.

Contract-unchanged check (frozen): the Q3B CENSUS masks equal the Q2
CENSUS masks for both arms (all inmask {1}, outmask {2}); the ONLY world
difference is emission facts.

## 5. Frozen kill bars

- K1 SEED FIDELITY: P-Q1 and N-Q1 blocks byte-identical to the
  compose_inval lane Q1 blocks (same ARM/PROB labels); P-Q2 =
  2/3/1/3/44 (0) with WTRIG=3 and WADD=2,0 / 2,1 / 2,3; N-Q2 =
  2/6/1/2/44 with WTRIG=2. 3/3.
- K2 TRANSFER REPRO: P-Q2 strictly fewer tries than N-Q2 (3 < 6), ANS=2
  in both. Confirms the bit was genuinely true and helpful before
  invalidation. 3/3.
- K3 POISON FIRES: P-Q3B = 2/4/1/3/-1 (0) with WIDEN=1, WTRIG=3, and
  exactly the lines WADD=2,0 / WADD=2,1 / WADD=2,3 in scan order before
  any INTER line; N-Q3B = 2/1/0/0/-1 with zero WADD lines and WTRIG=0.
  3/3.
- K4 BIT PERSISTS: P LEDGER block after Q3B byte-identical to P LEDGER
  after Q2 (m2 out=1, all else 0; verified by cmp); N LEDGER all zero
  after Q3B. The false bit is never corrected. 3/3.
- K5 POISON BOUNDED: P_Q3B TRIES minus N_Q3B TRIES equals exactly 3;
  ANS=2 in both Q3B blocks; WBACK=0 in both Q3B blocks; P_Q3B TRIES <= 6.
  No wrong answer, no backstop, no runaway. 3/3.
- K6 DETERMINISM: 3/3 byte-identical whole-output per arm; sha256
  recorded.
- K7 HYGIENE: zero em/en dash bytes in all docs (byte-verified); safebin
  guard attested in NAMECHECK.md Step 0 (which python3/python return
  NOTHING); pure Zag for all scientific computation; pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1; compose_ledger and
  compose_inval lanes untouched (verified via git status); all new files
  under compose_beh/; no mode/policy identifier in the composer (grep
  over non-comment lines).

## 6. Frozen verdict mapping

- K1-K7 all PASS: BEHAVIOR-CHANGE INVALIDATION POISONS (BOUNDED).
  Priming fires on the genuinely-false bit (WTRIG=3, exactly the primed
  set) at exactly the primed-set try cost (+3 tries vs the fresh ledger),
  with no correction (the false bit persists verbatim). This is the true
  poison flavor, and it contrasts exactly with C345: contract-growth
  invalidation is self-shielding (0 tries); behavior-change invalidation
  actively misleads (+3 tries). The cost is bounded by the primed-set
  size, never corrupts the answer, and triggers no runaway. Implication
  for the unbounded-lifetime choice: a stale bit imposes a real,
  recurring tax whenever its primed pairs miss, so U3 without an
  invalidation rule is not free; but the tax is bounded and small, so the
  governance question is whether +primed-set tries per stale bit warrants
  a learner-observable invalidation rule (for example, a carried bit whose
  justifying emission repeatedly fails to re-occur on direct trial), not
  whether the ledger is catastrophically unsafe.
- K3 fails (no WADD/WTRIG=3 on P-Q3B, or different try counts): the
  non-shielding analysis is wrong or the implementation diverged;
  diagnose, do not claim.
- K4 fails (bit cleared, altered, or corrected): an undeclared correction
  path exists; diagnose, do not claim.
- K5 fails (cost != 3, wrong ANS, WBACK=1, or P_Q3B TRIES > 6): POISON
  UNBOUNDED or answer corruption; report exactly, do not claim
  boundedness.
- K1/K2 fail: implementation bug; diagnose, do not claim.
- VOID is terminal (toolchain violation, non-determinism, sealed-world
  inspection, or compose_ledger/compose_inval modified).

## 7. Honest boundaries (pre-declared)

- One behavior-change flavor: emission-kind flip (NODE to NUM at X's out)
  with the answer relocated to an admitted single. The symmetric "vice
  versa" case (a bit becoming true), partial flips, and cyclic changes
  are NOT covered here.
- The D5B answer relocation (A(42)=2 via new 82-facts) is
  researcher-installed to keep the query answerable with the same shape;
  the poison measurement is P-vs-N on the same changed world, so the
  relocation does not confound the comparison.
- Three queries on one world family discriminate the mechanism; they do
  not establish generality of invalidation behavior.
- Expected-answer verification still used (canonical boundary).
- Behaviors are installed as previously-learned MAPs (canonical standing).

## 8. Implementation plan (frozen order)

1. b_base.zag: byte-copy of compose_ledger/l_base.zag plus setup_d5b (D5
   facts minus the two 44,83 facts plus the two 42,82 facts; teaching
   identical to D5).
2. b_pers.zag: byte-copy of compose_ledger/l_pers.zag with main() changed
   to Q1(D5)/Q2(D5)/Q3B(D5B, s=42); composer fns untouched (U1-U5 frozen).
3. b_ctrl.zag: byte-copy of compose_ledger/l_ctrl.zag with main() changed
   the same way; n_solve untouched.
4. Assemble with cat (b_base+b_pers -> b_full_P.zag; b_base+b_ctrl ->
   b_full_N.zag), compile with the pinned znc, run 3x per arm, record
   sha256.
5. REPORT.md with verdict per the Section 6 mapping.

Zag pitfalls: u8-backed z_alloc; dynamic content formatted into one buffer
with cursor helpers and a single raw-syscall flush (no _zag_print for
dynamic content); if-nesting at most 3; no !(A && B) in while conditions;
as []f64 / as []i64 do not rescale .len.
