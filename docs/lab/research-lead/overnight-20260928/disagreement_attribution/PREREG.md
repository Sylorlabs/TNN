# PREREG.md -- DISAGREEMENT-ATTRIBUTION (non-ledger)

Frozen preregistration. Committed alone (with NAMECHECK.md) before any
da_ implementation file exists. Adopted as frozen without modification.

## 1. Research question

INTEGRATION-COMBINED disclosed gap F4: trigger B (the do_query retry
loop) cannot attribute a learner-vs-oracle disagreement to its cause.
It invalidates every contributing coverage contract bluntly. This
battery asks: can a learner-owned probe attribute a disagreement to
BINDING-caused vs COVERAGE-caused on purpose-built collision worlds,
with evidence that discriminates attribution from guessing?

Hypothesis H-ATTR: a probe that (a) re-runs fresh try_family trials
against the executing family, and (b) re-runs the learned spec against
the generic on identical inputs, attributes 16/16 staged collisions
correctly, while a null (always-BINDING) probe scores at most 9/16.

## 2. Background (what is being built on, not redesigned)

The substrate is INTEGRATION-COMBINED (cb_): do_query retry loop
(max 3 attempts), trigger B via note_answer_disagree (invalidates all
contributing coverage contracts at 3000/3100/3200), B1 binding contracts
(tag to family, 2000+bi*100), B2 coverage contracts (rel routing,
3000/3100/3200), the plan-invalidation hook (M3, read-only, fires on
cached-fam vs live-bind_fam mismatch). The probe is ADDITIVE: it runs
inside do_query after a disagreement with spec versions used (vbuf
2/3/5) and BEFORE note_answer_disagree. Trigger B, the hook, the
contracts, and the retry bound are untouched. Self-healing behavior is
preserved exactly; the probe only reports attribution.

## 3. Probe design (frozen)

`attr_probe` (in da_learn.zag), called from do_query on
learner-ans != oracle-ans with specused=1 and att<3. Inputs: learner
state L/S, world A, goal G, vbuf (per-step versions), scratch buffers,
pmod. It NEVER reads the harness trial-cause ledger, the oracle, or any
staging label. It NEVER mutates contracts or plans (bind_fam and
u_check are read-only; spec/generic re-runs use scratch buffers);
it writes only telemetry cells S931 (cause), S933 (first cause),
S934 (evb), S935 (evc), S936 (latch).

For each plan step with vbuf in {2,3,5} (ret/vfy/cnt spec versions):
- Let F = plan-cached fam, T = need tag, ni = need index.
- E-bind: tf[f] = try_family(L,A,f,G,ni,...) for f in 0..2 (the
  learner's own trial mechanism); live = bind_fam(L,S,T) (read-only).
  bindbad = (tf[F]==0) OR (live>=0 AND live!=F).
- If not bindbad, E-cov: re-run the learned spec and the generic on
  the need's identical inputs (F=0: ret_spec vs ret_gen on (rel,obj);
  F=1: vfy_spec vs vfy_gen on the materialized chain, src<0 only;
  F=2: cnt_spec vs cnt_gen on (rel, subjects)). covbad = spec refused
  (-1) OR spec output != generic output.
- evb latches if any step is bindbad; evc latches if any step is
  covbad (and not bindbad).

Attribution: BIND if evb=1 (binding precedence: a misrouted family
makes its spec output meaningless); else COV if evc=1; else IND.
Emits: `ATTR trial=<t> cause=<BIND|COV|IND> evb=<0/1> evc=<0/1>
nspec=<k>` where t = sg(S,930) (harness-set trial id, label only).

Stability latch: S936=0 on first invocation per trial records S933 =
cause; a later invocation with a different cause emits
`ATTR-MISMATCH trial=<t> prev=<c> now=<c2>`.

Null probe (pmod=1): emits `ATTR trial=<t> cause=BIND evb=0 evc=0
nspec=0 null=1`, stashes cause 0, gathers no evidence. This is the
guessing control: a fixed-guess strategy with no attribution.

Learner-owned justification: every evidence item comes from the
learner's own machinery (trials, read-only contract checks, its own
spec and generic procedures, its own plan record). The oracle is used
only for disagreement DETECTION (as in trigger B), never for
attribution.

## 4. Purpose-built collision worlds (frozen trial table)

Each trial: fresh L/S (16384 bytes, zeroed), setup_worldA, 4 ret + 4
vfy + 4 cnt episodes, specialize all three families, then:

BIND trials (staged cause BINDING, t=0..7): tag-shape collision. A
need tag bound to family F is reused on a need shaped for family
F' != F. The binding contract is NOT revised, so the plan caches the
stale fam; the hook stays dormant (cached == live binding). The
misbound family's spec version runs and disagrees.
- kind 0 (t=0..3): tag bound to RET (fam 0) via baseline ret query;
  collision = COUNT-shaped need [tag,3,rel,1,subj] with rel in RET
  coverage {601,602} so ret_version=2 and ret_spec runs (returns 0
  subjects on obj=1); oracle_1cnt disagrees.
  t0: tag 821 rel 601 obj 623 subj 611
  t1: tag 822 rel 602 obj 625 subj 612
  t2: tag 823 rel 601 obj 621 subj 613
  t3: tag 824 rel 602 obj 622 subj 614
- kind 1 (t=4..7): tag bound to COUNT (fam 2) via baseline cnt query;
  collision = RET-shaped need [tag,2,rel2,obj2] with rel2 in CNT
  coverage {601,602,603} so cnt_version=5 and cnt_spec runs (0 on the
  unset subject slot); oracle_1ret disagrees.
  t4: tag 825 rel 601 subj 611 rel2 602 obj2 625
  t5: tag 826 rel 602 subj 612 rel2 603 obj2 620
  t6: tag 827 rel 603 subj 613 rel2 601 obj2 621
  t7: tag 828 rel 601 subj 614 rel2 602 obj2 632

COV trials (staged cause COVERAGE, t=8..15): binding correct (fresh
try_family agrees with cached fam), coverage contract still routes,
but the learned positional buckets are stale after drift, so the spec
answer diverges from the generic on identical inputs.
- kind 2 (t=8..10): RET drift. Learn on A, pre-drift query agrees,
  setup_worldA2 (same facts, permuted slots: 603 at 0-15, 602 at
  16-31, 601 at 32-47), post-drift query on the same goal disagrees.
  t8: tag 831 rel 601 obj 623
  t9: tag 832 rel 602 obj 625
  t10: tag 833 rel 601 obj 621
- kind 3 (t=11..13): VFY drift, same A to A2 protocol, 2-link chains
  chosen so no bucket index accidentally hits post-drift (verified by
  index arithmetic in the design notes).
  t11: tag 834 (611,602,622) (611,603,620)
  t12: tag 835 (612,603,621) (614,602,625)
  t13: tag 836 (615,603,624) (617,602,628)
- kind 4 (t=14,15): CNT deletion drift. Learn on A, pre-drift agrees,
  setup_worldA3 (world A minus fact slots 0-3: the two 601 facts and
  two 602 facts of i=0; indices shift by 4), post-drift disagrees.
  t14: tag 837 rel 601 subj 611
  t15: tag 838 rel 602 subj 611

CLEAN trials (4, after the 16): fresh state, world A, no drift, no
collision; single queries that agree first-try. The probe must never
fire.
  q0: ret tag 841 (601,623); q1: vfy tag 842 (611,602,622)(611,603,620);
  q2: cnt tag 843 (601,611); q3: ret tag 844 (602,622)

Goal tags: baseline/pre-drift 950+t (clean 970+q); collision goals
960+t (kinds 0,1 only; kinds 2-4 reuse the same goal post-drift to
exercise the plan-hit path). Oracle kinds: ret=oracle_1ret (okind 2),
vfy=oracle_1vfy (3), cnt=oracle_1cnt (new, okind 4, cnt_gen-based).

## 5. Frozen expectations (derivation summary)

- Per collision trial: baseline/pre-drift query agrees (1 Q);
  collision query: att1 disagree + ATTR + RETRY, att2 disagree + ATTR
  + RETRY, att3 disagree (BIND kinds, spec retired to generic, still
  disagreeing) or agree (COV kinds, generic fallback heals). So 4 Q
  lines per trial: 16 baselines/pre-drift agree, 32 collision
  att1/att2 disagree, 8 BIND att3 disagree, 8 COV att3 agree.
- Totals for da_bin: Q lines = 68; agree=1 = 28; agree=0 = 40;
  ATTR = 32; ATTR-MISMATCH = 0; RETRY = 32; HOOK = 0.
- Real probe: 16/16 correct (frozen bar: >= 15/16).
- Null probe (da_nullbin, same battery, pmod=1): always BINDING ->
  8/16 correct (all BIND right, all COV wrong), evsig = 0.
- A fixed guesser scores 8/16; a coin-flip guesser reaches >= 15/16
  with probability 17/65536 (~0.00026). The bar discriminates
  attribution from guessing.

## 6. Kill bars (frozen; ALL must be green for BUILD-PASS)

- K1 (prereg ordering): PREREG.md + NAMECHECK.md committed alone
  before any da_ file exists; git log shows the prereg commit
  strictly before the implementation commit.
- K2 (toolchain guard): Step 0 at startup: PATH=$HOME/safebin,
  `which python3`/`which python` empty, pinned znc
  znc_linux_x86_64_abed8aa1 for all builds. Zero forbidden
  invocations. Zag miscompile workarounds honored (u8 cells, single
  buffer emit, no !(A && B) in while, if-nesting <= 3, no []u8 as *u8).
- K3 (build): da_bin and da_nullbin build clean; exactly one
  `fn main(` per assembled full file; exit 0; stderr empty.
- K4 (probe discipline): da_run1.txt has exactly 32 ATTR lines, 0
  ATTR-MISMATCH lines; every ATTR line carries trial >= 0.
- K5 (attribution accuracy): SCORE-ATTR line reads correct >= 15,
  total = 16 (expected correct = 16).
- K6 (null control fails): da_null run SCORE-ATTR correct <= 9
  (expected exactly 8), total = 16, evsig = 0.
- K7 (clean): 4 CLEAN queries agree=1 on first attempt; 0 ATTR and 0
  RETRY lines after the STAGE CLEAN marker.
- K8 (bounded/self-healing preserved): 68 Q lines; agree=1 count 28;
  agree=0 count 40; 32 RETRY lines; binary exits 0 (no hang; every
  collision query terminates within 3 attempts).
- K9 (hook dormant / non-interference): 0 HOOK lines (no binding
  revision is staged, so the M3 hook must never fire).
- K10 (determinism): sha256 equal across da_run1/2/3.txt and across
  da_null1/2/3.txt; all stderr empty; all exits 0.
- K11 (hygiene): zero em/en-dash bytes in all sources, build script,
  and docs; da_learn.zag and da_main.zag contain zero of the 70+
  scanned world literals (superset of the 17 canonical identifiers);
  da_base.zag and da_module.zag cmp-identical to cb_base.zag and
  cb_module.zag.
- K12 (evidence signature): SCORE-ATTR evsig = 16: every BIND trial
  shows (evb=1,evc=0) and every COV trial shows (evb=0,evc=1). This is
  the attribution-vs-guessing evidence: the probe cites the specific
  evidence bits matching the staged cause.

## 7. Falsification probes

- F1 (spurious fire): probe emits ATTR on a clean query -> caught by
  K7 (0 ATTR after STAGE CLEAN).
- F2 (guessing passes): null probe reaches K5's bar -> capped by K6
  (<= 9) and K12 (evsig = 0 for the null run).
- F3 (attribution flips across retries): second-attempt probe
  disagrees with the first -> ATTR-MISMATCH line, K4 fails on any.
- F4 (probe perturbs state): probe writes contracts/plans -> would
  trip the hook (K9) or change healing counts (K8).
- F5 (nondeterminism): any run-to-run byte drift -> K10.
- F6 (wrong-contract invalidation masked): trigger B still bluntly
  invalidates coverage contracts on BIND trials (it cannot see the
  probe's attribution); this is disclosed, not hidden: the REPORT
  will note the probe reveals trigger B revising the wrong contract
  on BIND trials.

## 8. Build and determinism protocol

- da_build.sh: PATH=$HOME/safebin; cat da_base da_world da_module
  da_learn da_main > da_full.zag; pinned znc -> da_bin. Then
  sed 's/^let PMOD:i32=0;$/let PMOD:i32=1;/' da_main.zag >
  da_main_null.zag; cat ... da_main_null.zag > da_full_null.zag;
  pinned znc -> da_nullbin. Run each binary 3x; sha256 compare.
- S930/S931/S933/S934/S935/S936 are unused by cb_ (verified by grep
  before implementation); they are probe telemetry only.

## 9. File list

da_base.zag, da_world.zag, da_module.zag, da_learn.zag, da_main.zag,
da_build.sh (new); da_full.zag, da_bin, da_run{1,2,3}.txt/.err,
da_main_null.zag, da_full_null.zag, da_nullbin,
da_null{1,2,3}.txt/.err, da_compile.txt, da_null_compile.txt
(generated). REPORT.md (after the verdict).

## 10. Scoring

Main stages each trial t with harness-known cause exp = (t<8 ? 0:1)
(BIND=0, COV=1); the probe never sees exp. After do_query, main reads
S931 (probe cause), S934/S935 (evb/evc); correct++ if S931==exp;
evsig++ if (evb,evc) matches the staged signature. Final line:
`SCORE-ATTR correct=<n> total=16 evsig=<m>`. The null binary scores
identically against the same ledger.
