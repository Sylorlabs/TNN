# PREREG_AMENDMENT1.md: QT-AS and QV-AS hand-derivation corrections

Status: PRE-VERDICT amendment. Pure arithmetic/hand-trace
correction only. No algorithmic counting change. No
learner/operator code change. Two driver-side fixes
(stat-offset reads and F-COUNT literals) are mechanical
corrections to experiment-side bookkeeping, not to the
frozen learner machinery or the frozen counting rules.

## Error 1: QT-AS 368 -> 324 (hallucinated world fact)

PREREG.md section 5 derived QTRUNC op-2 (SUBSTITUTE) as
88 = 44 (candidate collection) + 44 (candidate fid 20
(100,2,50) SHAPE-FAIL). That fact does not exist. In the
frozen world (section 1), fid 20 is (120,6,121), the
first fact of the INVERT region; there is no (100,2,50)
fact. (The (100,2,50) VAL fact belonged to an earlier
INVERT design that was replaced by the reversed-relseq
design before the prereg was written; the derivation was
not updated.)

For QTRUNC (100,42,32), op-2 candidate collection finds
zero candidates: the only live fact with sub==100 and
rel != 18 does not exist (fid 7 has rel==18 == d_entry
and is excluded). So op-2 = 44 ticks (collection only),
and QT-AS = 2 (agg) + 6 (partner) + 234 (op-1) + 44
(op-2) + 38 (op-3) = 324.

## Error 2: QV-AS 1142 -> 1193 (foldwalk discovery order)

PREREG.md section 5 derived QINV op-1 rsrc=0 b=2 as 134
= 21 (partner-head) + 113 (AGG-tail: entry 22 +
foldwalk(122,3) = 91). The foldwalk derivation assumed
the discovered relations were (s1,s2)=(5,6). They are
not. ex_foldwalk discovers (s1,s2) from the first two
facts in order: f1=fid22 (122,6,123) gives s1=6,
f2=fid23 (123,5,124) gives s2=5. So the walk is:
g1=find(124,6)->fid24 (25 ticks), g2=find(125,5)->fid25
(26 ticks), then g1=find(126,6) fails (44 ticks, fid 26
has rel 18). Foldwalk = 23+24+25+26+44 = 142, not 91.
mr_agg_seg = 22+142 = 164, b=2 = 21+164 = 185 (not
134). Corrected op-1 = 185+185+185+44 = 599 (rsrc=0:
b1=185, b2=185; rsrc=2: b1=185, b2=44).
QV-AS = 2+7+599+208+181+196 = 1193.

The per-op cumulative A_SEARCH trace from an
instrumented scratch build (in /tmp, not committed)
confirms: QINV op-1 ends at 608 (=2+7+599), op-2 at 816
(+208), op-3 at 997 (+181), op-4 at 1193 (+196); QTRUNC
op-2 ends at 286 (=242+44).

## Driver-side mechanical fixes (experiment side only)

- Stat-offset reads in driver.zag were off by one slot
  for four fields (hand-written against the shifted
  layout): PIPE_HIT 1372->1368, BINDING 1360->1356,
  BIND_DECIDED 1364->1360, BIND_TRIES 1368->1364. The
  learner's layout and all learner stat accesses were
  already correct (mechanical sed shift verified).
- F-COUNT literals updated to the corrected values:
  QT-AS 324, QV-AS 1193.

## What does NOT change

- Frozen counting rules (section 3): untouched.
- Frozen learner machinery (section 2): untouched
  (mr_invert, mr_abstract, mr_concretize, mr_adapt,
  ex_query, and all helpers are byte-identical to the
  pre-amendment implementation).
- All other hand-derived counts (QC-AS=333, QS-AS=335,
  QE-AS=1242, QN-AS=1102, all AE=2, all ablation-arm
  informational counts): untouched; the instrumented
  trace confirms each per-op delta.
- Kill bars K1-K8, falsifiers, K7 audit: untouched
  (F-COUNT now checks the corrected values).
