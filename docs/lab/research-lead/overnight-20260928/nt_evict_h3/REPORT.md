# REPORT: NT-EVICT-H3 -- evidence-preserving revision under capacity pressure

## Verdict

**FAIL** per the frozen verdict mapping (PREREG Section 7). K1, K3, K5
hold; K2 and K4 fail. This is the preregistered directional prediction,
and it arrived in the strongest possible form: the H3 run output is
BYTE-IDENTICAL to NT2's frozen output (cmp clean; identical sha256).

## Frozen results (3/3 byte-identical; byte-identical to NT2)

- Run digest: `3d33f8333e31e91a6fb8188a5d442da13896fdc4d6eb18624472ca73bcd32644`
  (identical to NT2's frozen run digest)
- Binary digest: `241a47faa363bcba680e35159fd46de3c1e837522b93cb672ddff8bdda4721dd`
- Source digest: `1b05435faa8ae91021aaa2081e14a54a0de707433a94a261f1c66454bc6ed6a5`

```
NT2 ML1 CTRLA ttc=2 acc=24 nevict=0
NT2 ML1 CTRLB ttc=2 pc=1 acc=24 nevict=0
NT2 ML1 SEQ ttcA=2 accA=24 accB=18 nevict=41 nentries=30
NT2 ML1 RETEST c_vb=0 nc=6 u=12 forget=6
NT2 ML1 EVHIST 100=6 101=5 102=5 103=5 104=5 105=5 134=1 135=1 136=1 137=1 138=1 139=5
NT2 ML0 ABL ttcA=2 accB=24 nevict=0 nalias=12 nentries=24
NT2 ML0 RETEST c_vb=6 nc=6 u=0 forget=12
NT2 K1=1 K2=0 K3=1 K4=0 K5=1
NT2 VERDICT=FAIL
```

Every frozen numeric prediction matched exactly, including the
byte-identity prediction of PREREG Section 4/5.

## Kill-bar evaluation

- K1 (learning intact under capacity): PASS. Unchanged from NT2.
- K2 (eviction minimal, no churn): FAIL. nevict_seq = 41, not 6.
- K3 (uncontested retention survives): PASS. NC_OK = 6/6, U_OK = 12/12.
- K4 (revision completes under pressure): FAIL. c_vb = 0/6 (bar
  required 6/6), forget = 6 (bar required 0).
- K5 (discriminative validity): PASS. ML0 signature unchanged
  (u_abl=0/12, nevict_abl=0, nalias_abl=12) and distinct from ML1.

## What this establishes

1. **The H3 revision rule never fires in the ML1 arms.** The
   byte-identity with NT2 is not a coincidence: under NT2's lowest-net
   eviction, no key ever reaches ref > sup (pass 1: ref=1/sup=2; pass 2:
   ref=2/sup=2, then evicted; passes 3+: keys inserted fresh and evicted
   the same pass). Deleting the sup reset therefore changes no state
   transition. The preregistered mechanism trace (PREREG Section 4) is
   confirmed exactly.
2. **The parent "evidence reset" diagnosis is falsified for the
   net-eviction regime.** The tasking held that "the breaking
   interaction is the evidence reset, not the comparator." H3 removed
   the revision reset, and nothing changed -- because the reset was
   never the interaction point. The breaking interaction is EVICTION
   PREEMPTING REVISION: contradiction depresses net to the insertion
   baseline (sup=2, ref=1 -> net=1 = fresh key) BEFORE ref can exceed
   sup, so the key is removed mid-revision and re-inserted fresh. The
   reset that matters is the eviction-reinsertion reset (fresh
   sup=1, ref=0), which H3 was barred from touching ("only the revision
   rule changes").
3. **H1 and NT2 fail at different interaction points.** H1's total-
   evidence eviction let revision fire and then punished the reset
   entry; NT2's net-eviction never lets revision fire at all. "The
   evidence reset" is therefore not one breaking interaction but two
   different ones, and fixing the revision reset addresses only H1's.
   A hypothesis framed as the common fix cannot work: there is no
   single revision-rule change that fixes both, because in NT2's regime
   the revision rule is dead code.
4. **K2's "correct" bar (nevict==6) is unreachable jointly with K3+K4.**
   Worth recording for the deeper rethink: 36 distinct keys are active
   in phase B (24 A-keys must be retained, 12 novel taught per pass)
   against 30 slots, so at least 6 novel keys are absent and
   re-inserted every pass -- a minimum of 36 evictions over 6 passes
   even in the best case. The preregistered "correct" (6 evictions AND
   U_OK=12/12 AND forget=0) is arithmetically impossible; any future
   bar must be derived from this pigeonhole bound, not from
   "12 novel minus 6 free slots".

## Recommended follow-up (the deeper rethink)

H3's null result redirects the search. Candidate directions, each
needing its own preregistration:

- (D1) Preserve evidence across EVICTION/re-insertion (not revision):
  a re-inserted key resumes its old (sup, ref) instead of (1, 0). This
  is the reset that actually fires in NT2's regime. Note it changes the
  insertion rule, which H3 froze.
- (D2) A comparator that does not punish contradiction: eviction must
  distinguish "low evidence because new" from "low net because
  contested". H1's total-evidence tried this and failed via the reset;
  combined with H3's preserved revision it might behave differently --
  but that is a two-change hypothesis (H1+H3), not H3.
- (D3) A faster revision trigger (e.g. ref >= sup): revision would fire
  in pass 2 (ref=2 >= sup=2) before the novel-phase evictions. This
  changes the revision TRIGGER, which H3 froze.
- (D4) Re-derive the kill bars from the pigeonhole bound (minimum 36
  evictions under K3+K4) before testing any of the above; otherwise the
  next hypothesis will fail K2 on arithmetic, not mechanism.

## Honest boundaries (from PREREG Section 9, unchanged)

- Minimal surrogates, not TNN's production substrate; characterizes the
  rule-set only.
- L1 memorization substrate; no L2/L3 claim.
- Single capacity point (CAP=30); single contradiction magnitude;
  histogram is measurement-only.
- Opaque identifiers throughout.
- H1's PREREG/REPORT were not found in the workspace; H1's mechanism is
  taken from the parent tasking's summary (see NAMECHECK Step 1). If
  that summary misstates H1, the H1-vs-NT2 comparison in "What this
  establishes" (item 3) should be re-checked against H1's actual files.

## Provenance

- Prereg frozen alone: commit `0b8561c` (PREREG.md + NAMECHECK.md only),
  strictly before implementation.
- Implementation + results: this commit. Pure Zag, safebin-only PATH,
  pinned znc 2026.07.0-dev (same build as NT2). Zero forbidden-
  executable invocations.
- Source change vs NT2: exactly one line (deleted the sup reset in the
  revision action) plus header comment; `diff` verified.
- Build: `znc nt3_full.zag -o nt3_bin`; 3/3 runs byte-identical (cmp);
  output additionally cmp-identical to NT2's frozen `nt2_run1.txt`.
- Commits local only, explicit pathspecs, never pushed.
