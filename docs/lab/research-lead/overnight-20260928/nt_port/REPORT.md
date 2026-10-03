# REPORT: NT-PORT -- D1+D2 ported to the shared continuing-learner substrate

## Verdict

**PORT-PASS** per the frozen verdict mapping (PREREG Section 7). K1,
K2, K3, K4, K5 all hold. This is the preregistered directional
prediction (PORT-PASS), and -- like NT-D2 before it -- EVERY frozen
numeric prediction matched exactly, including both full eviction
histograms (MAIN 7-bin, ABL 12-bin). The D1+D2 rules transfer from
the minimal surrogate to the shared continuing-learner substrate:
the NT1 selective-retention pattern survives capacity pressure on
the production substrate with both rules, and the NT2 failure
signature (eviction preempts revision; contradicted subjects
forgotten) reproduces on the same substrate with the rules removed.

## Frozen results (3/3 byte-identical)

- Run digest: `5852f8546fbb6c9704bc59d28f4358f8a06f4a79c80dc891f165bfbadc2bce9b`
- Binary digest: `a81dcf99e520ae5ead96775e81f676573e2ff4b2d86abe0ebb1f999077322914`
- Source digest: `419425039ed11d56b0b28e89780c23aeeea12ece3c2241d96410a18f3a441771`

```
NTPORT MAIN ttc=2 probe1=16 nevict=20
NTPORT MAIN RET c=6 k=4 u=6 npres=4 forget=0
NTPORT MAIN EVHIST 123=3 124=3 125=3 126=3 127=3 128=3 129=2
NTPORT ABL ttc=2 probe1=16 nevict=20
NTPORT ABL RET c=0 k=4 u=6 npres=10 forget=6
NTPORT ABL EVHIST 100=3 101=2 102=2 103=2 104=2 105=2 124=1 125=1 126=1 127=1 128=1 129=2
NTPORT K1=1 K2=1 K3=1 K4=1 K5=1
NTPORT VERDICT=PORT-PASS
```

Prediction vs actual: NO misses. MAIN nevict 20 = 20; c 6/6; k 4/4;
u 6/6; forget 0; histogram bins 123..128 = 3 each, 129 = 2, all other
subjects (in particular all of 100..115) at 0. ABL nevict 20 = 20;
c 0/6; k 4/4; u 6/6; forget 6; histogram bins exactly as traced
(100=3, 101..105=2, 124..128=1, 129=2). The prereg hand-traces
(Sections 4.1, 4.2) reproduced the binary exactly, bin for bin, on
both arms.

## Kill-bar evaluation (forget regime stated explicitly)

- K1 (learning intact under capacity): PASS. TTC1 2/2, probe1
  16/16 on both arms. Capacity itself does not break learning; no
  VOID.
- K2 (eviction minimal, no churn, FORGET = 0 regime): PASS.
  nevict_main = 20 = the frozen port minimum (18 pigeonhole lower
  bound under FORGET = 0, +2 traced revolving-door overhead in
  passes 2 and 3). All 20 victims are N subjects (123..129); zero
  phase-1 subjects evicted in any pass.
- K3 (uncontested retention survives): PASS. K_OK = 4/4, U_OK = 6/6.
  Untouched subjects are never eviction candidates: staleness is
  protective under LIFO, never punished -- on the production
  substrate, not just the surrogate.
- K4 (revision survives pressure, FORGET = 0 regime): PASS. C_VB =
  6/6 (revision completes in pass 3: ref accumulates across eviction
  boundaries via D1 restore, invisible to the D2 comparator) AND
  FORGET = 0.
- K5 (discriminative validity): PASS. The ABL arm (same substrate,
  D1+D2 removed, NT2 comparator) reproduces the NT2 failure
  signature exactly as traced: c_vb_abl = 0/6, forget_abl = 6,
  u_abl = 6/6, nevict_abl = 20. MAIN and ABL have the SAME eviction
  count (20) with OPPOSITE victim sets (novel subjects vs
  contradicted subjects): the count was never the measure; the
  victim set is. The apparatus discriminates; PASS is allowed.

## What this establishes

1. **The D1+D2 rules transfer.** The port is minimal (PREREG Section
   2.1: slot fields, evidence update, D1 checkpoint/restore, D2
   LIFO -- nothing else), the substrate is the shared
   continuing-learner skeleton (associative instance memory,
   sequential lifetime phases, no resets, no task labels), and the
   workload is a realistic continuing-learning sequence (early
   experience -> world change with contradictions -> novel
   experience -> untouched old knowledge, 1.3x pressure), not the
   NT2 battery. The full NT1 selective-retention pattern survives:
   revision completes, uncontested knowledge is retained, nothing
   needlessly forgotten, evictions at the traced minimum.
2. **The NT2 failure mode is substrate-independent.** With D1+D2
   removed, the same substrate, workload, and update rule reproduce
   NT2's signature bin-for-bin in structure: lowest-net eviction
   preempts revision (contradicted subjects evicted at net=1 before
   ref can accumulate), the six contradicted subjects are forgotten,
   and the victim set is the entries current experience is about.
   The rules are doing the work, not the substrate or the workload.
3. **The victim-set moral replicates.** NT-D2's finding -- churn is
   not pathology, churning the wrong entries is -- holds on the
   production substrate: MAIN and ABL both evict 20 times; MAIN's 20
   victims are all re-taught-every-pass novel subjects (forget-free
   churn), ABL's 20 include all six contradicted subjects (revision
   preempted, FORGET = 6).
4. **Protection without protection rules, again.** No phase-1
   subject is ever evicted in MAIN, yet the implementation contains
   no protection flag, no task identity, no "don't evict" logic --
   only installation order. The D2 comparator remains as generic as
   the lowest-net rule it replaces.

## Honest boundaries (from PREREG Section 8, unchanged)

- The port covers the continuing learner's associative instance
  memory only. contlearn2's schema discovery/verify/retire
  machinery was not ported (orthogonal capability); whether D1+D2
  interact well with schema formation is untested. H-CONTLIFE-1's
  hash-table memory was not ported (would require inventing evidence
  machinery -- a redesign, not a port).
- Subjects are memorized (subj,rel)->obj associations; no L2/L3
  claim. The experiment measures retention/revision/eviction
  dynamics only.
- Single capacity point (CAP=20, 1.3x over capacity); single
  contradiction magnitude; pressure-ratio scaling and graded
  contradiction out of scope (preregistered follow-up).
- The eviction histogram is measurement-only; the checkpoint table
  and `ins` are learner state (own prior evidence / own installation
  order), containing no oracle/task information.
- LIFO was selected by NT-D2's preregistered necessity argument
  (temporal metadata is required; FIFO is the anti-D2), not by
  fitting this workload. Whether LIFO's tenure principle holds when
  novel subjects are NOT re-taught every pass remains the
  preregistered open boundary.

## Recommended follow-up (preregistered, PREREG Section 9)

- Scale the pressure ratio (1.3x -> higher) with the same bars and
  the forget regime stated explicitly.
- Probe the "genuinely low-value" boundary: novel subjects NOT
  re-taught every pass -- does LIFO still pick the right victims,
  or does tenure-protection become a liability?
- Port D1+D2 toward H-CONTLIFE-1's hash-table memory if an
  evidence-machinery design can be made minimal rather than a
  redesign; test interaction with schema discovery/retire.

## Provenance

- Prereg frozen alone: commit `edd03b062` (PREREG.md + NAMECHECK.md
  only), strictly before implementation. Commit-order self-check:
  verified below (prereg commit strictly precedes this commit).
- Implementation + results: this commit. Pure Zag, safebin-only PATH,
  pinned znc 2026.07.0-dev (same build as NT2/H1/H3/D1/D2). Zero
  forbidden-executable invocations.
- Source: `nt_port_full.zag`, written to PREREG Section 2 (port of
  the NT-D2 rule set onto the continuing-learner skeleton; the
  continuing-learner substrate skeleton follows
  `continuing_learner/contlearn2.zag`). One self-caught display bug
  fixed pre-report: the `nevict=` emit field read arena offset 8
  (ins_seq) instead of offset 4 (nevict), printing 40/0 instead of
  20/20; the kill-bar logic always read the correct offset, and the
  frozen binary was built only from the corrected source.
- Build: `znc nt_port_full.zag -o nt_port_bin` (exit 0; benign
  zagd-unavailable warning only); 3/3 runs byte-identical (cmp),
  exit 0, zero stderr.
- Audit grep for protection/task-label/importance logic: clean.
- Commits local only, explicit pathspecs, never pushed.
