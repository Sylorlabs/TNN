# PREREG: NT-FRESHCHURN -- Churn without re-teaching: fresh novel subjects each pass

## 1. Question

NT-LIFOBOUND (C445, INCONCLUSIVE) established two findings. Dimension
A: no LIFO liability; once-taught novel subjects do not block revision
(K1..K4 hold at 2x/3x/5x; revision is in-place; survivors stay
eviction-eligible). Dimension B: the NT2 failure signature is
churn-dependent; without re-teach churn, ABL revises successfully
(c_abl=6, forget_abl=0), so the no-reteach regime cannot discriminate
fragility modes (K5 fails; an apparatus finding, not a D1+D2 finding).

NT-LIFOBOUND PREREG Section 8 preregistered the follow-up verbatim:
"restore churn WITHOUT re-teaching by supplying FRESH novel subjects
each pass (each taught once)." This battery runs that probe. Each
phase-2 pass teaches a FRESH set of N_n novel subjects, each subject
taught exactly once in the lifetime. This reinstates the revolving-door
pressure that produced ABL's NT2 signature in NT-PRESSURE, while keeping
the "taught once" property LIFOBOUND tested.

Two competing accounts, frozen before implementation:

- CHURN-DEPENDENCE (predicted): the NT2 signature needs only churn
  (revolving-door evictions knocking out low-net entries), not
  re-teaching. Fresh-novel-per-pass restores K5 discrimination
  (ABL: c=0, forget=6) while MAIN keeps K1..K4. Verdict:
  FRESHCHURN-PASS.
- RE-TEACH-DEPENDENCE (alternative): the NT2 signature needs the
  specific re-teach dynamics (present novel subjects accumulating sup,
  id overlap across passes, or another re-teach-specific factor).
  Fresh churn does NOT restore K5 (ABL revises despite churn).
  Verdict: INCONCLUSIVE, and the churn-dependence account is
  falsified/refined (a substantive negative, not a mere apparatus
  limit).

This is the sharper form of the "genuinely low-value" boundary. The
fresh novel subjects are genuinely low-value: taught once, never
reinforced, never queried, contradicted by nothing. LIFO/D2 must
correctly sacrifice them (youngest-first) while protecting the
reinforced phase-1 entries; ABL's lowest-net rule is tested on whether
it can discriminate under genuine pressure rather than coasting
through an easy regime.

## 2. Subject (frozen: NT-LIFOBOUND's skeleton, two frozen changes)

The subject is NT-LIFOBOUND's subject verbatim: the continuing-learner
skeleton (associative instance memory, sequential lifetime phases,
single main(), no resets, no task labels) with ONLY the D1+D2 memory
rules installed (slot fields subj/rel/obj/dom/valid/sup/ref/ins;
NT-frozen evidence update; D1 checkpoint/restore keyed by (subj,rel);
D2 evict-youngest by max ins; ABL arm = same substrate, NT2 lowest-net
comparator, no checkpoint table). This is the same skeleton, not a
redesign. TWO frozen changes vs NT-LIFOBOUND:

(a) Phase-2 teaching protocol. Pass p in 1..3 teaches, in ascending
order: C (100..105) O2(k); K (106..109) O1(k); N^(p) O1(k), where
N^(p) = 120+(p-1)*N_n .. 119+p*N_n are FRESH novel subject ids.
Every novel subject is taught exactly once in the lifetime; no novel
subject is ever re-taught. U (110..115) never taught in phase 2.

(b) Apparatus: subject-id space enlarged. 3*N_n distinct novel ids are
required; at P5 (N_n=84) the max novel id is 119+252=371. The D1
checkpoint table and the eviction histogram are 272-entry tables
indexed (subj-100), covering subjects 100..371; the arena allocates
8192 bytes (5596 used: 16 header + 640 slots + 4352 checkpoint +
1088 histogram). This is a measurement-table sizing change only. The
learner rules (D1/D2/ABL eviction, evidence update, CAP=20, slot
layout, oracles) are NT-LIFOBOUND's verbatim. The checkpoint table
holds only the learner's own prior evidence; the histogram is
measurement-only. Enlarging them cannot change victim choice: D2
evicts max-ins and ABL evicts min-net regardless of table size.

## 3. Workload (frozen numeric inventory; opaque identifiers)

Oracles identical to NT-LIFOBOUND (opaque numeric subject ids; no
semantic labels anywhere):

- O1(k) = 200 + ((k*37 + 11) mod 64), all k. (Oracle, phase 1.)
- O2(k) = 200 + (((O1(k)-200)+32) mod 64) for contradicted subjects,
  guaranteed different from O1(k). (Oracle, phase 2.)
- Phase 1 ("early experience"): 16 subjects 100..115, obj O1(k).
  Train to criterion: repeat passes; after each pass probe all 16.
  Criterion = 16/16 correct for 2 consecutive passes. Max 50 passes
  (fail-safe; hitting it = arm FAIL at that pressure point).
- Phase 2 ("world change + fresh novelty each pass"): 3 passes over,
  in ascending order: C (100..105) taught O2(k), K (106..109) taught
  O1(k), N^(p) = 120+(p-1)*N_n..119+p*N_n taught O1(k). U (110..115)
  never taught in phase 2.
- Retention probe: query all 100..115 plus the full fresh-novel range
  120..119+3*N_n. Score C (100..105) vs O2, K (106..109) vs O1, U
  (110..115) vs O1, N presence over 120..119+3*N_n. FORGET =
  subjects among C+K+U answering neither their phase-1-correct nor
  (for C) their phase-2-correct obj (absent -> -1 counts as
  forgotten).

Pressure points (frozen; CAP=20 fixed; same three points as
NT-LIFOBOUND for direct comparability):

- P2: N_n = 24. N^(1) = 120..143, N^(2) = 144..167,
  N^(3) = 168..191. Total distinct subjects 16+72=88, ratio 4.4x
  distinct (2.0x per-pass pressure, matching LIFOBOUND's per-pass
  insertion load).
- P3: N_n = 44. N^(1) = 120..163, N^(2) = 164..207,
  N^(3) = 208..251.
- P5: N_n = 84. N^(1) = 120..203, N^(2) = 204..287,
  N^(3) = 288..371.

Arms per pressure point (each on a FRESH learner): MAIN (D1+D2),
ABL (rules removed). One binary runs all six arms sequentially and
emits all lines; 3 runs must be byte-identical. Output tag NTFRESH.

## 4. Frozen predictions (hand-derived by tracing the NT-LIFOBOUND
##    rules under the fresh-novel protocol; general N_n, then per-point)

Phase 1 is identical to NT-LIFOBOUND at all points (no pressure):
TTC1 = 2, probe1 = 16/16, nevict = 0. Slots hold 100..115 with
(O1, sup=2, ref=0); MAIN ins stamps 1..16; ABL nets 2.

MAIN (D1+D2), phase 2. Pass 1: C hit+mismatch -> ref=1 (in place,
ins 1..6); K hit+match -> sup=3; N^(1): 120..123 fill the 4 free
slots (ins 17..20); 124..119+N_n revolving-door evictions on the
youngest slot: N_n-4 evictions, victims 123 (ins 20) then
124..118+N_n (each once), all D1 checkpointed. End of pass 1:
present = 100..115 (ins 1..16), 120,121,122 (ins 17,18,19),
119+N_n (ins 16+N_n). Pass 2: C ref 1->2 (in place); K sup 3->4;
N^(2) all fresh/absent -> N_n insertions, each evicting the current
youngest: victims 119+N_n (ins 16+N_n) then 120+N_n..118+2N_n
(each once), N_n evictions, all checkpointed. End of pass 2:
present = 100..115, 120,121,122, 119+2N_n (ins 16+2N_n). Pass 3:
C ref 2->3 > sup 2 -> revise in place to (O2,1,0), ins untouched;
K sup 4->5; N^(3) fresh -> N_n insertions, victims 119+2N_n then
120+2N_n..118+3N_n, N_n evictions. Total MAIN nevict = 3*N_n-4
(the pigeonhole minimum: 3*N_n insertions into 4 free slots).
phev_main = 0 (the youngest door never touches ins 1..16).
Retention: C = O2 (6/6), K = O1 (4/4), U = O1 (6/6),
N presence = {120,121,122,119+2N_n,119+3N_n} = 5, FORGET = 0.
EVHIST_main: bins 123..118+3N_n = 1 each (contiguous: pass 1 covers
123..118+N_n, pass 2 covers 119+N_n..118+2N_n, pass 3 covers
119+2N_n..118+3N_n).

ABL (no D1, lowest-net comparator, no ins stamps), phase 2. Pass 1:
identical to NT-LIFOBOUND: C ref=1 (net 1); K sup=3 (net 3);
120..123 fill slots 16..19 (net 1); 124..119+N_n revolving door on
slot 0 (lowest net 1, lowest slot index): N_n-4 evictions, victims
100 then 124..118+N_n. End of pass 1: slot 0 = 119+N_n (net 1);
100 absent; 101..105 (net 1); 106..109 (net 3); 110..115 (net 2);
120..123 (net 1). Pass 2: C 100 absent -> insert, evicts slot 0
(119+N_n; net 1, lowest slot index among net-1 candidates):
1 eviction; C 101..105 hit+mismatch -> ref=2 (net 0); K sup=4
(net 4); N^(2) all fresh/absent -> N_n insertions: the first five
evict the net-0 subjects (101..105, slots 1..5), the rest churn on
slot 0 (lowest index among net-1): victims 101,102,103,104,105,
100, 125+N_n..118+2N_n; N_n evictions. End of pass 2: slot 0 =
119+2N_n (net 1); ALL of C absent; 120..123 (net 1, slots 16..19);
120+N_n..124+N_n (net 1, slots 1..5). Pass 3: C all absent ->
insert, churning slot 0 (lowest index among net-1): victims
119+2N_n, 100, 101, 102, 103, 104; survivor 105 in slot 0 (net 1);
6 evictions; K sup=5 (net 5); N^(3) fresh -> N_n insertions,
victims 105 then 120+2N_n..118+3N_n (slot-0 churn), N_n evictions.
End of pass 3: slot 0 = 119+3N_n; ALL of C absent. Total ABL
nevict = (N_n-4) + (1+N_n) + (6+N_n) = 3*N_n+3. Retention:
C = 0/6 (all absent -> predict -1); K = 4/4; U = 6/6;
FORGET_abl = 6 (all of C answers neither O1 nor O2);
N presence = {120,121,122,123,120+N_n..124+N_n,119+3N_n} = 10;
phev_abl = 13 (100 in pass 1; 100..105 in pass 2; 100..105 in
pass 3; informational, not a kill bar). EVHIST_abl: bin 100 = 3,
bins 101..104 = 2, bin 105 = 2, bins 119+N_n = 1, 119+2N_n = 1,
bins 124..118+N_n = 1 each, bins 125+N_n..118+2N_n = 1 each, bins
120+2N_n..118+3N_n = 1 each. (Check: 3+8+2+2+(N_n-5)+(N_n-6)+
(N_n-1) = 3N_n+3.)

Frozen numeric predictions per pressure point:

P2 (N_n=24):
- MAIN: ttc=2, probe1=16, nevict=68, RET c=6 k=4 u=6 npres=5
  forget=0 phev=0. EVHIST: 123..190=1 each; 100..115=0.
- ABL: ttc=2, probe1=16, nevict=75, RET c=0 k=4 u=6 npres=10
  forget=6. EVHIST: 100=3, 101=2, 102=2, 103=2, 104=2, 105=2,
  143=1, 167=1, 124..142=1 each, 149..166=1 each, 168..190=1 each.

P3 (N_n=44):
- MAIN: ttc=2, probe1=16, nevict=128, RET c=6 k=4 u=6 npres=5
  forget=0 phev=0. EVHIST: 123..250=1 each; 100..115=0.
- ABL: ttc=2, probe1=16, nevict=135, RET c=0 k=4 u=6 npres=10
  forget=6. EVHIST: 100=3, 101..104=2 each, 105=2, 163=1, 207=1,
  124..162=1 each, 169..206=1 each, 208..250=1 each.

P5 (N_n=84):
- MAIN: ttc=2, probe1=16, nevict=248, RET c=6 k=4 u=6 npres=5
  forget=0 phev=0. EVHIST: 123..370=1 each; 100..115=0.
- ABL: ttc=2, probe1=16, nevict=255, RET c=0 k=4 u=6 npres=10
  forget=6. EVHIST: 100=3, 101..104=2 each, 105=2, 203=1, 287=1,
  124..202=1 each, 209..286=1 each, 288..370=1 each.

### Predicted outcome (frozen, directional)

FRESHCHURN-PASS at P2, P3, P5: K1=1, K2=1, K3=1, K4=1, K5=1 at
every point; OVERALL=FRESHCHURN-PASS-ALL. The churn-dependence
account predicts the NT2 signature returns in ABL (c_abl=0,
forget_abl=6, nevict_abl=3N_n+3, u_abl=6) because the fresh-novel
revolving door evicts the contradicted subjects (net 0 in pass 2,
slot-0 churn in pass 3) before ref can exceed sup, exactly as the
re-teach door did in NT-PRESSURE; meanwhile MAIN keeps K1..K4
because revision is in-place and the youngest door confines all
3N_n-4 evictions to the genuinely low-value fresh subjects.

### What would falsify the prediction (honest triggers)

- c_main < 6 or forget_main > 0 -> FAIL-RETENTION at p: fresh churn
  broke revision; the "genuinely low-value" boundary has a dark
  side under genuine pressure (INFORMATIVE-FAIL naming LIFO as a
  liability here).
- phev_main > 0 or nevict_main != 3*N_n-4 -> FAIL-K2 at p:
  tenure-protection failed or the trace is wrong; mechanism unknown.
- K1..K4 hold but K5 fails (ABL revises: c_abl = 6, or
  forget_abl = 0, or the signature otherwise absent) ->
  INCONCLUSIVE at p, AND the churn-dependence account is
  FALSIFIED: churn alone does not restore the NT2 signature; the
  signature needs re-teach specifically (or another unmodeled
  factor). This is the key discriminating outcome of the battery:
  a K5 failure here is a substantive negative about the mechanism,
  not a mere apparatus limit.

## 5. Assembly, build, run (frozen)

- Single source file `nt_freshchurn_full.zag`: the NT-LIFOBOUND
  source (`nt_lifobound_full.zag`, C445) with ONLY the frozen
  Section 2 changes (teach_p2 takes a pass index and teaches the
  fresh range N^(p) = 120+(p-1)*N_n..119+p*N_n; 272-entry
  checkpoint/evhist tables indexed (subj-100) covering 100..371;
  arena 8192 bytes; npres over the full fresh range 120..119+3N_n)
  and the Section 6 kill-bar literals. D1/D2/ABL rules, evidence
  update, slot layout, CAP=20, oracles, phase 1, retention probe,
  FORGET definition are NT-LIFOBOUND's verbatim. Output tag
  `NTFRESH`.
- Canonical helpers copied verbatim (z_alloc, get32, set32, o_app,
  o_i64, o_nl, o_flush).
- Build: `znc nt_freshchurn_full.zag -o nt_freshchurn_bin` under
  safebin-only PATH.
- Run `nt_freshchurn_bin` 3 times; outputs `nt_freshchurn_run1.txt`,
  `nt_freshchurn_run2.txt`, `nt_freshchurn_run3.txt`. Require
  byte-identical (cmp) and record sha256.
- Output lines (all numeric): per pressure point and arm: TTC1,
  probe1, nevict, retention (c/k/u/npres/forget), nonzero
  eviction-histogram bins, MAIN phase-1-eviction count (bins
  100..115, for K2), and per-point K1..K5 verdict bits plus a
  per-point verdict line.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic output
  only via the single-buffer cursor helpers + one `_zag_raw_syscall`
  write (never `_zag_print`); no `!(A && B)` in while conditions
  (De Morgan); if-nesting at most 3 deep with hoisted call results;
  no `[]u8 as *u8` casts (thread `_zag_malloc as *u8`).

## 6. Frozen kill bars (per pressure point p; N_n(p) = 24/44/84)

- K1_p (learning intact under capacity; else VOID at p): ttc_main
  in 1..50 AND probe1_main = 16 AND ttc_abl in 1..50 AND
  probe1_abl = 16. Else VOID at p.
- K2_p (eviction minimal, no churn, victims confined to N):
  nevict_main == (3*N_n - 4) AND phev_main == 0 (zero evictions of
  phase-1 subjects 100..115 in MAIN, from the histogram).
- K3_p (uncontested retention survives): k_main = 4 AND u_main = 6.
- K4_p (revision survives under fresh churn): c_main = 6 AND
  forget_main = 0.
- K5_p (discriminative validity; the NT2 signature RETURNS):
  (c_abl = 0 AND forget_abl = 6) AND (u_abl = 6 AND
  nevict_abl = 3*N_n + 3). The signature's qualitative core
  (contradicted subjects lost, not revised) is NT-PRESSURE's
  unchanged; the nevict literal is the fresh-regime traced value
  (3N_n+3), frozen in Section 4.

## 7. Verdict mapping (frozen; liability-prioritized)

Per pressure point (K5 checked LAST so a genuine liability is
never masked by a K5 outcome):

- K1 fails -> VOID at p.
- K2 fails -> FAIL-K2 at p (tenure/churn liability: victims
  escaped the N set, or churn differed from the traced minimum).
- K3 or K4 fails -> FAIL-RETENTION at p (revision liability: fresh
  churn blocked revision or caused forgetting -> the dark side of
  the genuinely-low-value boundary is REAL).
- K1..K4 hold, K5 fails -> INCONCLUSIVE at p (the churn-dependence
  account is FALSIFIED here: churn alone does not restore the NT2
  signature; the signature needs re-teach specifically).
- K1..K5 all hold -> FRESHCHURN-PASS at p (no liability AND the
  apparatus discriminates under fresh churn; the NT2 signature is
  churn-dependent, not re-teach-dependent).

Overall: FRESHCHURN-PASS at P2, P3, P5 -> overall
FRESHCHURN-PASS-ALL (predicted). Any FAIL-K2 or FAIL-RETENTION at
any point -> that point is an INFORMATIVE-FAIL; report the failed
bars with the histogram-derived mechanism. K5 failing while
K1..K4 hold -> overall INCONCLUSIVE with the churn-dependence
falsification stated plainly.

## 8. Honest boundaries (pre-declared)

- Same skeleton as NT-LIFOBOUND, not a redesign; the port boundary
  from NT-PORT PREREG Section 1.1 stands (contlearn2 schema
  machinery and H-CONTLIFE-1 hash-table memory remain unported).
- Subjects are memorized (subj,rel)->obj associations; no L2/L3
  claim. The experiment measures retention/revision/eviction
  dynamics only.
- The apparatus change (272-entry tables, 8192-byte arena) is
  documented in Section 2(b); it cannot affect victim choice.
- Per-pass insertion load matches NT-LIFOBOUND (N_n novel
  insertions per pass); the distinct-subject count is higher
  (16+3N_n), which is the point of the fresh-novel design.
- Three capacity points (2x/3x/5x per-pass pressure); single
  contradiction magnitude; graded contradiction out of scope.
- The eviction histogram is measurement-only; the checkpoint table
  holds only the learner's own prior evidence.

## 9. Amendment record (transparent; committed before implementation)

Amendment 1 (2026-10-03, post-freeze implementation bugfix; the frozen
spec is UNCHANGED): the first implementation wrote the eviction
histogram at byte offset 4508, which overlaps the D1 checkpoint table
(656 + 272*16 = 5008). The correct histogram base per the frozen
Section 2(b) layout is 5008 (arena used 6096 bytes, still within the
frozen 8192 allocation). Symptom caught before any verdict was drawn:
P5 MAIN showed impossible histogram bins (e.g. 102=220, an obj value
written by ck_set into the histogram) and phev=918, while P2/P3 (max
novel id 251/191, below the overlap threshold) were unaffected. The
fix changes only the histogram base offset (4508 -> 5008) in
nt_freshchurn_full.zag; no rule, protocol, prediction, or kill-bar
change. The binary was rebuilt and all three runs re-executed after
the fix; only the post-fix runs count toward the verdict.

Amendment 2 (2026-10-03, prediction typo correction; informational
only, no kill bar affected): the PREREG Section 4 MAIN retention
summary and per-point lines predicted npres=5 for MAIN, but the
Section 4 trace itself is unambiguous: pass 3's youngest door evicts
119+2N_n (listed in the pass-3 victims), so the end-of-pass-3 novel
presence is {120,121,122,119+3N_n} = 4, not 5. The binary outputs
npres=4 at all three points, matching the trace. The "5" was an
arithmetic slip in the summary line. npres is measurement-only (not
in K1..K5); the verdict is unaffected. Corrected MAIN npres
prediction: 4 at P2/P3/P5.
