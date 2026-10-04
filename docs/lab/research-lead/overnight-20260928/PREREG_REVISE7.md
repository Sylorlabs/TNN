# PREREG H-REVISE7 FROZEN

Date (UTC): 2026-09-29 (preregistered before any H-REVISE7 implementation)
Branch: tnn-native-lab
Hypothesis: H-REVISE7
Parent: H-REVISE6 (builder prereg 1743ca053; builder result 400463112;
  independent red team: adversary result 310fdabc6, VERDICT SURVIVES)

## Background (frozen facts)

1. H-REVISE6 SURVIVES all 66/66 frozen builder checks and the independent red
   team. Classification: bounded L2+ revision, NOT L3.
2. The red team CONFIRMED the known residual X-RV5-1 / X-RV6-1 as a fundamental
   limit, not a new kill: an adversarially correlated or mislabeled fail2 is
   observationally underdetermined from the learner's view. Any gate that
   appends on the evidence available must either append wrongly or withhold
   everything, including the genuine Phase C cases. No observation-only gate can
   detect it at append time. This impossibility stands and is NOT re-litigated.
3. Red-team robustness wart (disclosed, unreachable in shipped main): the v6
   gate can panic if called directly with nn<=0, because all six call sites
   guard nn<0 before entry. H-REVISE7 adds a defense-in-depth guard.

## Frontier idea (frozen)

H-REVISE7 stops trying to detect the undetectable and instead bounds the
aftermath. New principle: REVISIONS ARE HYPOTHESES. Second-order revision,
the learner revises its own revisions, which is a concrete step toward the
Level E correction/revision requirement.

Continuing protocol, applied to every new labeled input after a revision exists:

  (a) Every appended revision enters as PROVISIONAL, because the append-time
      evidence (propose from fail1 plus three-condition corroboration on fail2)
      is the minimum evidence, and the X-RV5-1 impossibility means it can be
      wrong through no fault of the gate.
  (b) On each new labeled input: if VS predicts correctly, a PROVISIONAL
      revision fired, and the pre-revision policy P0 would have mispredicted,
      the revision earns CONFIRMATION and is promoted to ACTIVE.
  (c) On each new labeled input: if VS mispredicts and the most-recent firing
      revision would not have fired-but-P0-was-right, the revision overrode a
      correct prediction and is contradicted: a PROVISIONAL revision is
      ROLLED BACK after 1 contradiction; an ACTIVE revision is DEMOTED to
      PROVISIONAL after 1 contradiction (needs 2 total to be rolled back).
  (d) Rollback is NON-DESTRUCTIVE (status tombstone, bytes retained). If a
      later fresh diagnosis re-derives the same (cpos,cval), vs3_revise
      REACTIVATES the tombstoned slot instead of appending a duplicate.
  (e) Rollback gives EXACT RESTORATION: vs3_apply skips rolled-back slots, so
      behavior returns bit-identically to the pre-revision policy.

What this does NOT do (frozen non-goals):
  N1. It does NOT detect X-RV5-1 / X-RV6-1 at append time. The gate still
      returns 1 on the adversarial fixture. That is the honest, expected
      outcome, frozen below.
  N2. It does NOT distinguish a forged contradiction (label crafted to equal
      the P0 output) from a genuine one. An adversary holding the label source
      can always roll back any revision. The protocol bounds honest-label
      mistakes and makes adversarial cost explicit; it does not authenticate
      the label channel.
  N3. It does NOT detect duplicate appends when propose re-derives the
      (cpos,cval) of an ACTIVE revision (known gap, documented in the result).
  N4. diagnose_propose, capacity 4, AMBIGUOUS, VS3FULL, and the three
      corroboration conditions are UNCHANGED.

## Implementation plan (pure Zag, no Python anywhere)

File: docs/lab/research-lead/overnight-20260928/revise7.zag (copied from
revise6.zag, then edited in Zag only).

R1. Slot size 60 -> 64 bytes. Byte at so+60 holds revision STATUS:
      0 = ROLLED_BACK (tombstone), 1 = PROVISIONAL, 2 = ACTIVE.
    vs3_revise sets status=1 on every append/reactivation and emits one
    EVIDENCE line. vs3_apply and vs3_firing_slot skip slots with status 0.
    vs3_dump prints st=RB/PROV/ACT.
R2. New: vs3_status(VS,s) -> i32; vs3_firing_slot(VS,inp) -> i32 (1-based slot
    that vs3_apply would use, 0 if none); vs3_apply_skip(VS,inp,skip) -> seq
    (identical to vs3_apply except slot `skip` is ignored); vs3_apply_p0
    (unchanged P0 broadcast-last reference).
R3. New: diagnose_rollback_check(VS, inp, true_out) -> i32. Caller contract:
    call only after vs3_apply mispredicted `true_out`. Logic: s =
    vs3_firing_slot; if s==0 return 0; if status(s)==1: if
    vs3_apply_skip(VS,inp,s)==true_out: set status 0, emit ROLLBACK line,
    return 1; else return 0. If status(s)==2: same skip-test; on match set
    status 1, emit DEMOTE line, return 2; else return 0.
R4. New: diagnose_confirm_check(VS, inp, true_out) -> i32. Caller contract:
    call only after vs3_apply predicted `true_out` correctly. Logic: s =
    vs3_firing_slot; if s==0 return 0; if status(s)!=1 return 0; if
    vs3_apply_p0(inp)!=true_out: set status 2, emit CONFIRM line, return 1;
    else return 0.
R5. vs3_revise reactivation: before appending, scan for a slot with status 0
    and identical (cpos,cval). If found: set status 1, overwrite the stored
    program bytes and nn, emit REACTIVATE line, return the slot. No vcount
    change, no duplicate slot.
R6. diagnose_corroborate_v6: if nn1<=0, emit a clean WITHHOLD line and
    return 0. No panic. (Defense in depth; all shipped call sites still guard.)

Main: banner renamed to H-REVISE7; new Phase N1..N5 after existing Phases
A..I (which are byte-preserved from revise6.zag). Total expected CHECK lines:
66 existing + 32 new (N1:11, N2:4, N3:9, N4:7, N5:1) = 98.

## Frozen fixtures and kill bars

Phase N1. X-RV5-1 replay with rollback bound (11 new CHECKs).
  P0 = broadcast-last. Passing fixtures D_J/pdJ = {abc,def,ghi,jkl}.
  fail1 = ("zqy"->"zzz") honest. fail2 = ("zab"->"zzz") mislabeled (red-team fixture).
  K-RV7-1 (frozen): diagnose_propose must equal (0,122); nn from discover of
    fail1 must be 3 (broadcast-first); gate must return 1 (frozen expectation:
    detection is NOT claimed; a 0 here is a fixture error, not a pass);
    vs3_revise appends slot 1 with status PROVISIONAL. On new labeled
    ("zbq"->"qqq") with VS mispredicting ("zzz"): diagnose_rollback_check must
    return 1; slot status must become ROLLED_BACK; vs3_apply("zbq") must equal
    "qqq" (exact restoration); vs3_apply("abc") must equal "ccc" (passing
    intact); vs3_apply("zqy") must equal "yyy" (the honestly-labeled fail1
    resurfaces as a genuine P0 failure, not silently absorbed).
Phase N2. Non-interference (4 new CHECKs).
  Store: slot 1 = (0,120)->broadcast-first, PROVISIONAL (honest Phase C
  fixture: fail1 ("xqw"->"xxx"), passing abc/def/ghi/jkl).
  New labeled ("yzb"->"yyy") (no x anywhere; revision cannot fire).
  K-RV7-2 (frozen): VS must mispredict ("bbb"); diagnose_rollback_check must
  return 0; status stays PROVISIONAL; vcount stays 1.
Phase N3. Adversarial rollback is dual-use; re-admission bounds it (9 CHECKs).
  Same store as N2. Forged ("xqw"->"www") (label crafted to equal P0 output).
  K-RV7-3 (frozen): VS mispredicts; diagnose_rollback_check must return 1 and
  status becomes ROLLED_BACK. This is the FROZEN DUAL-USE DISCLOSURE: the rule
  cannot tell forged labels from genuine P0-consistent labels, and the bar
  requires the honest behavior anyway. Then genuine ("xqw"->"xxx"): VS
  mispredicts via P0; diagnose_rollback_check must return 0. Fresh
  diagnose_propose on ("xqw"->"xxx") must equal (0,120); fresh discover plus
  gate with fail2 ("xab"->"xxx") must return 1; vs3_revise must REACTIVATE slot
  1 (vcount stays 1, status PROVISIONAL, no duplicate slot); vs3_apply("xqw")
  must equal "xxx".
Phase N4. Promotion and graded contradiction (7 CHECKs).
  Store: slot 1 = (0,120)->broadcast-first, PROVISIONAL.
  Confirming ("xqp"->"xxx") (VS correct via revision; P0 gives "ppp").
  K-RV7-4 (frozen): diagnose_confirm_check must return 1; status becomes
  ACTIVE. Forged ("xqw"->"www"): VS mispredicts; diagnose_rollback_check must
  return 2 (DEMOTE, not rollback); status becomes PROVISIONAL. Forged
  ("xab"->"bbb"): VS mispredicts; diagnose_rollback_check must return 1;
  status becomes ROLLED_BACK. Bound documented: 1 contradiction fells a
  provisional revision, 2 fell a confirmed one.
Phase N5. nn<=0 defense in depth (1 CHECK + 3/3 determinism of the guard).
  K-RV7-5 (frozen): diagnose_corroborate_v6 called with nn1=0 must return 0
  with a clean WITHHOLD line and no panic, 3/3.
K-RV7-6 (frozen regression): all 66 existing named CHECK lines byte-identical
  in REVISE7_RAW.txt. The only allowed raw differences versus REVISE6_RAW.txt
  are documented in advance: banner renames H-REVISE6 -> H-REVISE7;
  vs3_revise EVIDENCE lines (exactly 4, in Phases C, G, H, I); vs3_dump
  " st=PROV" fields; the new Phase N block. Verified by diff; zero other
  differences.
K-RV7-7 (frozen determinism): 3/3 runs byte-identical, cmp-verified.

## Verdict rules (frozen)

- ALL of K-RV7-1 .. K-RV7-7 pass -> H-REVISE7 SURVIVES.
- ANY ONE fails -> H-REVISE7 KILLED. There is no downgrade path; the bars are
  binary by construction.
- The X-RV5-1 residual remains a CONFIRMED RESIDUAL (still undetectable at
  append time); H-REVISE7 bounds its aftermath, it does not remove it.
- Classification target: bounded L2+ revision with self-correction protocol,
  NOT L3. L3 requires representational invention; this work invents no
  representation.

## Commit lineage (to be filled after execution)

- Prereg commit: (this file, committed alone, before any implementation)
- Implementation + raw evidence: revise7.zag, REVISE7_RAW.txt (+ 2 rerun raws)
- Result: REVISE7_RESULT.md

## Governance

Pure Zag. No Python in implementation, fixtures, evidence, analysis, or
editing of these artifacts. No em dashes in loop documentation. On any
index.lock race, wait for the live lock; never remove it while workers may be
active. Commit only owned paths under
docs/lab/research-lead/overnight-20260928/ (PREREG_REVISE7.md, revise7.zag,
REVISE7_RAW*.txt, REVISE7_RESULT.md).
