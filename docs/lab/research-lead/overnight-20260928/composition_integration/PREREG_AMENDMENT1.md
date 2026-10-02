# PREREG AMENDMENT 1: H-COMPINTEG-1 redesign

Status: FROZEN 2026-10-02. Committed before the redesigned
implementation is run. The original PREREG.md stands; this amendment
corrects two design flaws discovered during implementation testing
(probe run, not a verdict run). No kill bar is weakened: K1-K8 keep
their meaning, with corrected hand-derivations below.

## Flaw 1 (fatal): EXTEND-ONE is single-link; I1/I3 hand-derivation wrong

The frozen PREREG derived I1's answer (108) as "lv_dfs terminates at
108 via a (longest first)" where a=[1,1,1,2]. But EXTEND-ONE extends by
exactly ONE link: from frontier 104 via (104,2,105) the adapted MAP
ends at 105, not 108. Reaching 108 required composing a with MAP_Y
([2,2,2], 105->108), which the battery never trains. The probe
confirmed: explore observed 105, prediction settled at 105, and the
arm failed its preregistered assertions. The original I1/I3
derivations were factually incorrect, not merely unlucky.

## Flaw 2 (integration hazard): prediction FACTs pollute adaptation

C280's prediction machinery stores predictions as FACTs in the shared
fact store. C278's adapt_specialize scans that store for alternative
relations. The probe showed the interaction is real: the explore
FACT (101,70,105) was picked up by adapt_specialize as a world
alternative, creating a 1-link self-referential [70] MAP (101->105
via the learner's own FACT). In I3-Q2 this [70] MAP stayed intact
after the world change and natively re-verified the stale prediction:
a degenerate self-fulfilling loop. This is reported as a genuine
integration finding (section 4), and the redesign eliminates it by
construction (below), so the battery tests the intended integration.

## Redesign (frozen)

Train X with the QUERY relation: ev_teach(11,70,12),(12,70,13),
(13,70,14), then ev_query_adapt(W,11,70,14,0). MAP_X has relseq
[70,70,70] and field 4 = 70.

Consequence 1: adapt_specialize only considers facts with
r_alt != R[j]. Since every R[j] = 70 and every prediction/training
FACT for these arms carries r = 70, the learner's own FACTs are
invisible to the operator by construction. World-offered
alternatives (r = 2) remain visible. No frozen code is touched; the
visibility follows from the relation algebra.

Consequence 2: single-link Z-worlds suffice. I1/I3 Z facts:
(101,70,102),(102,70,103),(103,70,104),(104,2,108). EXTEND-ONE
produces [70,70,70,2] ending at 108 in one segment. No Y segment is
needed; the composition under test is exactly extend+verify+wire.

Consequence 3: lv_predict's MAP-execute fallback is harmless.
MAP_X (field 4 = 70) is found by the fallback, but t2_exec guards on
chain literals, so executing from a foreign subject returns
-999999 and the fallback skips it. I4 therefore withholds with
nobasis exactly as preregistered.

## Corrected hand-derivations

- I1: explore x4 (op=1, retire=1): cycle 1 creates trial
  [70,70,70,2], executes to 108, teaches FACT(101,70,108) score 0
  (MAP fallback finds nothing executable from 101); cycles 2-4
  predict 108 and confirm, score reaches 3. Q1: lv_setup predicts
  108 rel 3; native fails (MAP_X ends at 104); bracket creates
  a=[70,70,70,2] (extend) and t=[70,70] (truncate scaffolding);
  specialize creates nothing (all r=70 facts skipped); lv_dfs
  terminates at 108 via a (longest first); verify 108==108;
  promote MAP_Z with LINK14 to a. Expect: ans=108; a type-16->MAP_X,
  relseq [70,70,70,2], kind 1; MAP_Z LINK14->a; exactly 2 live
  adapted MAPs; explore FACT score 3.

- I2: explore x4 (op=2, retire=1) builds FACT(11,72,13) score 3
  via trial [70,70]. Q: predicts 13 rel 3; native fails (MAP_X ends
  at 14); bracket: extend nothing (frontier 14 dead end), truncate
  creates t=[70,70], specialize creates sp=[72,70] (from the explore
  FACT, terminal 14, inert); lv_dfs: t tried before sp (lower id),
  terminates at 13. Expect: ans=13; t type-16->MAP_X, relseq
  [70,70], kind 2; MAP_Z LINK14->t.

- I6: teach (12,2,99) after training. Explore x4 (op=3, retire=1):
  specialize sees only (12,2,99) at j=1 (the (11,70,14) training
  FACT has r=70=R[0], skipped), creates exactly one trial [70,2]
  per cycle, executes to 99, builds FACT(11,74,99) score 3. Q:
  predicts 99 rel 3; native fails; bracket creates t=[70,70],
  xs=[70,2] (via (12,2,99)), sp=[74] (from explore FACT, len 1,
  terminal 99, inert); lv_dfs order MAP_X, t, xs, sp: xs
  terminates at 99. Expect: ans=99; xs type-16->MAP_X, relseq
  [70,2], kind 3; MAP_Z LINK14->xs.

- I4: unchanged: ans=-3, zero type-16 edges, 1 live MAP.

- I3: setup as I1 through explore; q1=compose_integ -> 108,
  MAP_Z LINK14->a. World change: teach (104,2,140), kill
  (104,2,108) (teach-then-kill). q2: lv_setup predicts 108 rel 3;
  native fails (a unreadable via cc path; MAP_X ends 104; t2
  intact ends 103; MAP_Z stale); adapt_revise2: a STALE, kind 1
  (recorded by integ_tag_extend), rev_extend_src builds
  a2=[70,70,70,2] via (104,2,140) with type-16 a2->a, retires a;
  lv_dfs: a2 ends at 140 != 108. Expect: q1=108; q2=-2; a retired;
  a2 live, relseq [70,70,70,2], type-16 a2->a; no LINK14 targets
  a2; FACT(101,70,108) score still 3. The preregistered breakdown
  stands: structure is revised and wired, but the stale learner
  prediction blocks acceptance.

- I5: unchanged bounded diagnostic (<=10 cycles, q3=140,
  MAP_Z2 LINK14->a2). The [70]-loop hazard is gone by
  construction, so recovery exercises the C181 supersession/score
  dynamics only.

## Kill bars

K1-K8 unchanged in meaning; I1/I2/I6/I3 assertions use the
corrected derivations above. K7 (no `expected` token in
integ_patch.zag; zero em/en dashes) and K8 (frozen sha256) stand.
