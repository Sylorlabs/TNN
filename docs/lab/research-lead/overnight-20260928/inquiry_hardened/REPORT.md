# REPORT: Hardened Grammar Active Inquiry vs Adversarial Teachers

## Verdict: INQUIRY-HARDENED-COMPLETE

Per-teacher re-tests: ADV-LIE **SURVIVE**, ADV-WASTE **SURVIVE**,
ADV-POISON **SURVIVE**. No regression on ADV-CTRL (cooperative NEG-AMB,
1 query) or EXL2/EXL3/EXL4 (0 queries).

## Claim tested

INQUIRY-ADVTEACHER-COMPLETE left three findings: ADV-LIE KILL (one
false fact defeats -4 fail-closed; op-consistency tests facts against
candidates, not ground truth), ADV-POISON KILL (the decomp channel
43/44 is an unverified trust path; false decomp fact corrupts grammar
ranges while the inquiry masks to the true D), ADV-WASTE BOUND (QMAX=4
caps damage; no usefulness tracking). This worker hardens the
learner-side inquiry machinery (unfrozen) with four repairs and
re-runs all three preregistered attacks plus regression worlds.

## Repairs implemented (learner-side, h_patch.zag; 0 modes/bridges/handlers)

R1. Answer provenance. Learner-owned `prov` array (1024 bytes, indexed
by fact node id): 0=unmarked, 1=taught, 2=inquiry.
`gi_prov_mark_taught` marks the original teaching; `gi_inquiry_accept`
is the ONLY entry point for inquiry answers into W (accepted facts are
marked 2); rejected facts are never added (quarantined by exclusion).
`gi_prov_audit` reports taught/inquiry counts per world.

R2. LIE repair: corroboration gate. An inquiry eval fact (41/42) may
eliminate a candidate only when corroborated. STRONG elimination
(trusted immediately): DIV fact with d|P, so bb=0 under d: the pair is
degenerate and impossible under any well-formed codec, a coarse
structural signal. WEAK elimination (verification round): any other
kill (op-value mismatch on a well-formed pair; all SUB kills). The
teacher must supply an INDEPENDENT corroborating fact B that is new,
eval, different from A, kills the same d_weak STRONGLY, and keeps every
candidate A keeps; both A and B then enter W. Any failure emits
GI-LIE-SUSPECT, rejects A, marks the teacher untrusted, and early-stops
fail-closed (-4). Facts that kill nothing are accepted as harmless
(the WASTE case; usefulness tracking bounds them).

R3. POISON repair: decomp decode-and-verify plus pair-witness.
`gi_decomp_ok(d,s,r,P)` verifies a decomp fact with the SAME
decode-and-verify as eval facts (a decomp fact redundantly encodes the
eval claim with subject/object swapped). `gi_codec_op_ok` now scans
relations 43/44 (defense in depth). Inquiry decomp facts must ALSO pass
at accept time: (a) gi_decomp_ok under EVERY surviving candidate (a
decomp fact is not a discriminator; it must eliminate nothing), and
(b) pair-witness corroboration: the pair object must already be
witnessed by at least 2 independent taught facts (relations 41-44).
Failure emits GI-POISON-SUSPECT, quarantines the fact (never enters W),
marks the teacher untrusted, early-stops fail-closed.

R4. WASTE repair: usefulness tracking. WASTE_BUDGET=2, separate from
QMAX=4. After each accepted answer plus re-induction, if the candidate
count does not strictly shrink, waste++ (GI-WASTE-COUNT); duplicates
also count. waste>=2 emits GI-WASTE-STOP and early-stops (-4).
Suspect detections (R2/R3) stop immediately (teacher untrusted).

## Results (3/3 byte-identical, SHA-256 2d178d2d...)

```
GI-HD-START
GI-HD-WORLD EXL2
GI-INDUCED 1
GI-INDUCED-POST 1
GI-GRAMMAR nbuild=4 nlic=2 lic=44,43 D=16 a=[0,9] b=[0,9] maxlinks=1
GI-PROVENANCE taught=178 inquiry=0
GI-HD-WORLD EXL3
GI-INDUCED 1
GI-INDUCED-POST 1
GI-GRAMMAR nbuild=4 nlic=2 lic=44,43 D=8 a=[0,7] b=[0,7] maxlinks=1
GI-PROVENANCE taught=122 inquiry=0
GI-HD-WORLD EXL4
GI-INDUCED 1
GI-INDUCED-POST 1
GI-GRAMMAR nbuild=2 nlic=2 lic=44,43 D=32 a=[0,3] b=[0,3] maxlinks=1
GI-PROVENANCE taught=38 inquiry=0
GI-HD-WORLD ADV-CTRL
GI-INDUCED -4
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ANSWER P=34 op=42 t=2
GI-ANSWER-ACCEPT s=34 r=42 o=2 prov=inquiry
GI-QUERIES issued=1 answered=1 verify=0/0 waste=0
GI-INDUCED-POST 1
GI-GRAMMAR nbuild=2 nlic=2 lic=43,44 D=8 a=[2,6] b=[2,6] maxlinks=1
GI-PROVENANCE taught=14 inquiry=1
GI-ADV-BATTERY
GI-ADV-B 0 ans=18 class=1
GI-ADV-B-VALID 1/1
GI-ADV-WORLD-VALID 1
GI-HD-WORLD ADV-LIE
GI-INDUCED -4
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ADV-LIE-ANSWER P=35 op=42 t=2
GI-VERIFY-REQUEST d=8 reason=weak-elimination s=35 r=42 o=2
GI-ADV-LIE-ANSWER P=35 op=42 t=2
GI-LIE-SUSPECT reason=verify-failed d=8 b_s=35 b_r=42 b_o=2
GI-QUERIES issued=1 answered=1 verify=1/1 waste=0
GI-INDUCED-POST -4
GI-GRAMMAR none
GI-PROVENANCE taught=14 inquiry=0
GI-QUARANTINE-CHECK lie-absent=1
GI-HD-WORLD ADV-WASTE
GI-INDUCED -4
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ADV-WASTE-ANSWER P=20 op=41 t=-2
GI-ANSWER-ACCEPT s=20 r=41 o=-2 prov=inquiry
GI-WASTE-COUNT 1/2
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ADV-WASTE-ANSWER P=34 op=41 t=2
GI-ANSWER-ACCEPT s=34 r=41 o=2 prov=inquiry
GI-WASTE-COUNT 2/2
GI-WASTE-STOP
GI-QUERIES issued=2 answered=2 verify=0/0 waste=2
GI-INDUCED-POST -4
GI-GRAMMAR none
GI-PROVENANCE taught=14 inquiry=2
GI-HD-WORLD ADV-POISON
GI-INDUCED -4
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ADV-POISON-ANSWER subj=0 op=43 obj=63
GI-POISON-SUSPECT reason=decomp-inconsistent d=17 s=0 r=43 o=63
GI-QUERIES issued=1 answered=1 verify=0/0 waste=0
GI-INDUCED-POST -4
GI-GRAMMAR none
GI-PROVENANCE taught=14 inquiry=0
GI-QUARANTINE-CHECK poison-absent=1
GI-HD-DONE
```

## Per-teacher scoring (against the preregistered rubric)

### ADV-LIE: SURVIVE (fail-closed plus detected)

The lie is defeated at the trust boundary. (35,42,2) weakly kills d=8
(35 mod 8 = 3: well-formed pair (4,3), inexact DIV), so the learner
triggers the verification round instead of trusting it. The
preregistered liar repeats (35,42,2); the corroborator is not
independent of A and not a strong kill, so verification fails:
GI-LIE-SUSPECT is emitted, the lie is quarantined (quarantine check
confirms (35,42,2) absent from W), the teacher is marked untrusted, and
the loop early-stops with GI-INDUCED-POST -4 and no grammar written.
The -4 fail-closed that one lie defeated now holds against it, and the
learner emits an explicit detection signal. Previously: silent-wrong
D=17 grammar, no signal. Now: nothing wrong written, lie detected.

### ADV-WASTE: SURVIVE (early-stop)

Both waste facts are true and consistent with both candidates, so they
are accepted as harmless (killing nothing), but usefulness tracking
counts them: nc stays 2->2 after each, GI-WASTE-COUNT 1/2 then 2/2,
GI-WASTE-STOP fires, and the loop early-stops at issued=2 (half the old
burn). Fail-closed preserved (-4, nothing written). The
budget-conservation claim the old mechanism lacked now holds: the
learner stops asking an unhelpful teacher after 2 non-shrinking answers
instead of burning the full QMAX=4. Previously: BOUND (4/4 burned).
Now: SURVIVE (2/4, early-stop).

### ADV-POISON: SURVIVE (fail-closed plus detected)

The poison is caught by the decomp gate before it can enter W.
(0,43,63) fails decode-and-verify on the surviving candidate d=17
(63 decodes to (3,12) under 17; 3-12 != 0): GI-POISON-SUSPECT
reason=decomp-inconsistent. (The pair-witness check would also fail: 63
appears in 0 taught facts.) The fact is quarantined (quarantine check
confirms (0,43,63) absent from W), g stays 18, ranges are never
corrupted (no grammar written), and the loop early-stops at -4. The
decomp channel is no longer an unverified trust path: every decomp
answer now satisfies the same decode-and-verify as eval facts, and
novel pairs cannot be smuggled through it. Previously: ranges corrupted
to a=[2,7] b=[2,7], no signal, masked by the true D=8. Now: nothing
written, poison detected.

### Regression: no regression

- ADV-CTRL reproduces cooperative NEG-AMB exactly: D=8 a=[2,6] b=[2,6],
  1/1 queries, battery 1/1 class 1. The cooperative discriminator
  (34,42,2) is a STRONG kill of d=17 (34 mod 17 == 0: degenerate pair
  under 17), so it is trusted immediately with no verification round.
- EXL2/EXL3/EXL4 induce on the first try (code 1) with D=16/8/32 and
  zero GI-INQUIRY lines. The extended gi_codec_op_ok (43/44) passes on
  all taught full-grid decomp facts (they satisfy gi_decomp_ok under
  the true divisor by construction of the teaching), so the consistent
  sets are unchanged.

## Why each outcome is correct (hand verification)

- ADV-CTRL: (34,42,2) kills only d=17 (bb=0 under 17); strong
  (34-(34/17)*17=0); accepted; re-induction sees {8}; D=8 written with
  the taught decomp ranges a=[2,6] b=[2,6]. Binary matches.
- ADV-LIE: (35,42,2) kills only d=8 via inexact DIV on well-formed
  (4,3); weak (35-32=3); verification round; liar repeats the identical
  fact, failing independence and strength; GI-LIE-SUSPECT; quarantined;
  -4. Binary matches.
- ADV-WASTE: (20,41,-2) contributes s=18, (34,41,2) contributes s=36;
  g stays 18; both consistent with d=8 and d=17 (hand traces in the
  advteacher prereg); nc 2->2 twice; waste budget 2/2 exhausts;
  early-stop at 2 queries. Binary matches.
- ADV-POISON: (0,43,63) fails gi_decomp_ok under d=17 (first candidate
  checked); quarantined before W mutation; g stays 18; -4. Binary
  matches. (Pair-witness: 63 in 0 taught facts; would independently
  reject.)
- EXL2/3/4: extended op check adds only passing checks on taught decomp
  facts (c2_dsub teaches (t,43,P(a,b)) with a-b=t, so
  gi_fact_ok(d,P,41,t)=1 under the true d; c2_ddiv analogously for 44);
  first-induce code unchanged at 1.

## Kill-bar audit

- K1: 3/3 runs byte-identical (SHA-256
  2d178d2defa5c8d972cdc1564e15d929994220ca7236be5c7e5a80a77b686eae).
  PASS.
- K2: ADV-CTRL: D=8 a=[2,6] b=[2,6], queries 1/1, battery 1/1 class 1.
  PASS.
- K3: EXL2/3/4: GI-INDUCED 1, D=16/8/32, zero GI-INQUIRY lines. PASS.
- K4: ADV-LIE: GI-LIE-SUSPECT emitted; post -4; GI-GRAMMAR none;
  GI-QUARANTINE-CHECK lie-absent=1. PASS.
- K5: ADV-POISON: GI-POISON-SUSPECT emitted; post -4; GI-GRAMMAR none;
  GI-QUARANTINE-CHECK poison-absent=1. PASS.
- K6: ADV-WASTE: GI-WASTE-STOP emitted; issued=2 < QMAX=4; post -4;
  GI-GRAMMAR none. PASS.
- K7: toolchain guard: safebin active, `which python3 python` empty at
  start and rechecked after the runs; pure Zag; no forbidden executable
  invoked. PASS.
- K8: 0 modes/bridges/handlers (all learner additions and teachers are
  plain functions); frozen dirs untouched (grammar_inquiry/,
  inquiry_advteacher/ read-only; h_base.zag byte-identical to
  a_base.zag, verified by cmp); paper untouched; nothing pushed; prereg
  committed (ea624ffec) before the implementation commit. PASS.

## Metrics

- Cognition lines added: 214 to the learner patch (9 new functions:
  gi_decomp_ok, gi_prov_mark_taught, gi_fact_dup, gi_pair_witnessed,
  gi_strong_kill, gi_inquiry_accept, gi_inquiry_verify,
  gi_quarantine_check, gi_prov_audit; plus the gi_codec_op_ok extension
  to relations 43/44). Driver: new hardened loop with provenance,
  verification rounds, and waste budget (teaching/battery snippets copied
  verbatim). h_base.zag: 0 changes (byte-identical).
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- Determinism: 3/3 byte-identical runs.
- Query spend vs the unhardened mechanism: CTRL 1 (same), LIE 1+1
  verify (was 1), WASTE 2 (was 4), POISON 1 (was 1).

## What this does not claim

- The coherent-liar limitation (preregistered): a liar maintaining a
  complete, self-consistent alternative world model can still fabricate
  a strong elimination plus a strong corroborator; no learner-side check
  can rule that out in principle, because the falsehood is true in the
  liar's consistent alternative world. The gate raises the bar from "one
  weak lie kills" to "sustained coherent fabrication", and fail-closed
  guarantees no silent-wrong grammar from the preregistered attacks.
- SUB discriminators always need verification (no structural strong case
  for SUB); a truthful SUB-only discriminator requires a strong
  corroborator to resolve.
- One weak kill verified per round (the first); multi-weak-kill rounds
  are not covered.
- The adversarial teachers are driver-simulated, as in advteacher.
- The P(a,b)=a*D+b family remains a researcher-owned world assumption.
- No broad generality claim: three targeted attacks on NEG-AMB plus
  regression worlds.

## Follow-ups (not started)

1. The verification round currently trusts a strong corroborator
   outright; a second-order check (e.g., corroborator pair-witness or
   S-range plausibility) would raise the bar against the coherent liar
   further.
2. SUB discriminators have no strong path; a structural SUB
   corroboration (or a truthful-teacher SUB test world) would close the
   asymmetry.
3. The waste budget (2) and QMAX (4) are driver constants; making the
   waste budget adaptive to the candidate count is future work.
