# RED-TEAM REVIEW: ARENA4 ROSTER BUILD-PASS (wave-20261001-2321pdt, RT-ARENA4)

Reviewer role: independent second opinion on the ARENA4 lane's ROSTER
BUILD-PASS verdict (C15 0.947). Method: every claim re-derived from
committed sources via git show on the recorded commits (prereg+audit
19d9edc87, implementation 171c45101, sealed eval f8d7b9b2e) plus one
independent rebuild of the frozen scorer with the pinned znc.
Pure Zag throughout; safebin PATH only. See NAMECHECK.md Step 0.

## Verdict: EVIDENCE-HOLDS

The BUILD-PASS stands. All 8 frozen kill bars were attacked along the
8 assigned axes; every bar's evidence reproduces from the committed
record. Two non-blocking observations are recorded at the end; neither
moves a bar.

## Axis 1: Weakened bars (prereg K1-K8 vs SEALED_EVAL.md)

No bar moved. Checked each bar textually against the frozen prereg
(PREREG_ARENA_GOAL.md at commit 19d9edc87, byte-identical to the
working tree: sha256
dcc2c254a5c9f67f6f825c42d9e032d4d43d1af34c689e7eee81e4098351842e):

- K1: prereg demands C15 >= 0.900 on the sealed 68-item battery, all 3
  runs. Eval reports 0.947 on all 3 runs. Bar text unchanged.
- K2: prereg demands per-cap scores byte-identical to the v6 refreeze
  (caps 1-7,10,11,13,14,16 at 1.000; caps 8,9,12 at 0.000), total
  54.947/68 = 0.808. Eval table matches exactly; I re-verified the
  v6 column against REFREEZE_RECORD.md (wave-20261001-1721pdt) line by
  line. Arithmetic: 54 + 0.947 = 54.947; 54.947/68 = 0.8079 -> 0.808.
- K3: prereg demands 3/3 byte-identical stripped reply streams and
  roster_trace.txt files. Eval reports both hashes; I re-stripped
  ms/rss_kb from the committed replies.jsonl files and reproduced
  sha256 5e1ff7223683c6f0e5998836e8aadfdc441cfc3476918963233f6e77e981efbd
  on all 3 runs, and 743113d0f340f03957ccd673269dcdc9b2fbe7b0d995c251635e81dd3e58a6bd
  for all 3 traces. Both match the eval's claimed hashes exactly.
- K4: pure Zag, which python3 empty at start and end. Eval claims PASS
  with lane-start NAMECHECK and lane-end verification. No counter
  evidence in the committed record.
- K5: tool hashes, world hash, pre-run key hash, no sealed-file reads,
  grep audit. Eval reports world_gen c4c8340c..., arena 3899577b...,
  turns.jsonl 0fc3edb0..., answer_key.json a05ef916... I reproduced all
  four from the committed sealed world; a05ef916... also appears in
  ARENA2/SEALED_EVAL.md as that lane's independent pre-run record.
- K6: ROSTER_OFF ablation -> listnames UNKNOWN, C15 0.000, others
  unchanged. The committed ablation source differs from the
  implementation by exactly the 3 roster_touch call sites commented
  out (diff verified); the committed runabla results.json shows
  cap 15 at 0.000, total 0.794, every other cap unchanged; the
  ablation trace ends "listnames n=0 reply=UNKNOWN" and item 63
  replies "UNKNOWN".
- K7: 164 added / 0 removed lines, 0 modes/bridges/routers/gates,
  one learner-state structure. I diffed the refreeze v6 source
  (sha256 c6dbc20cf447dce7ab506576b42557a0542065e170bee6516558ecfb435d1e89,
  matches the refreeze record) against the committed
  roster_contestant.zag: exactly 0 removed lines, 164 added lines,
  0 mode/bridge/router/gate keyword hits in added lines.
- K8: L3 disclaimer recorded verbatim in both docs; no L3 claim made.

BUILD-PASS rule (K1-K4 must PASS; K5-K8 must also PASS) applied as
frozen. Nothing was redefined after results.

## Axis 2: Commit-order self-check

Strict ordering holds, verified from commit timestamps and contents:

- 19d9edc87 (2026-10-02 06:54:56 UTC): prereg freeze + C15 audit.
  Contains exactly 3 files: C15_AUDIT.md, NAMECHECK.md,
  PREREG_ARENA_GOAL.md. Zero implementation source. Pure prereg.
- 171c45101 (2026-10-02 06:57:39 UTC): ROSTER implementation.
  Contains roster_contestant.zag + run_sealed.sh only.
- f8d7b9b2e (2026-10-02 07:00:52 UTC): sealed evaluation + judge
  brief, ablation source, binaries, run data.

Prereg strictly precedes implementation strictly precedes sealed runs.
The prereg text was never amended: byte-identical from freeze commit
to working tree (later commits f461e812d deleted and a5d7a6ef7
restored the file byte-identical; content unchanged).

## Axis 3: The C15 audit (ordering-fragile claim)

Independently verified from the frozen scorer source. Extracted
competitive_arena/arena.zag from the refreeze commit c4e5a650e
(source sha256 76033aae69e2e473f7c4963f2e0121245fbd937626f070930c49ae142af570b4).
The cap-15 scoring block:

    if(cap==15){
      let ea:[]u8=z_alloc(12*16); let ra:[]u8=z_alloc(12*16);
      let ne:i32=split_csv(an,44,ea,12);
      let nr:i32=split_csv(rp,44,ra,12);
      let inter:i32=set_inter(ea,ne,ra,nr);
      if(ne+nr>0){sc=2000*inter/(ne+nr);}
    }

split_csv splits on commas; set_inter counts pairwise string-equality
matches between the two name lists. Order plays no role anywhere.
The scorer is genuinely an order-insensitive set F1, not exact match.
The ARENA2 "ordering-fragile" rejection is factually refuted, exactly
as the audit claims. (The audit's quoted snippet omits the z_alloc
lines; semantics identical.)

Strongest check: I rebuilt this frozen source with the pinned znc.
The produced binary is byte-identical (cmp clean, 82739 bytes,
sha256 3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076)
to the lane's committed sealed/bin/arena and to the refreeze record's
hash. The sealed eval scored with the genuine frozen scorer.

Score math confirmed: 9 reply names, 10 key names, intersection 9 ->
2000*9/19 = 947 (integer division). C15 = 0.947.

## Axis 4: "9 of 10 entities observable"

Verified from the committed sealed world (f8d7b9b2e):

- "Segunu" occurs 0 times in the lane's exposure.jsonl. The lane's
  exposure.jsonl is byte-identical (diff clean) to the refreeze run1
  world exposure.jsonl, so this is a battery property, not a regen
  artifact.
- Exactly 9 distinct entity names appear in exposure turns (fact "e"
  keys plus relation "a"/"b" endpoint keys): Dagumo, Datamo, Kavipe,
  Sehiru, Tetaru, Zofiru, Zosumo, Zovina, Zovinu. Relation endpoints
  introduce no additional names.
- First-appearance order (Kavipe Sehiru Zovina Datamo Zovinu Tetaru
  Zosumo Dagumo Zofiru) matches the roster reply order in the trace.
- Answer key index 63 = "Kavipe,Sehiru,Zovina,Datamo,Zovinu,Tetaru,
  Zosumo,Dagumo,Zofiru,Segunu" (10 names, internal index order);
  Segunu appears exactly once in the key file, in that answer string.

The honest experience-based ceiling of 0.947 and the kill bar at 0.900
(below it, not demanding the briefing-only 10th name) are both sound.

## Axis 5: Roster population (experience only)

Verified from roster_contestant.zag at commit 171c45101:

- roster_touch is defined once and called at exactly 3 sites: line 899
  inside learn_fact (entity buffer eb from the fact turn) and lines
  937-938 inside learn_rel (both endpoint buffers ab, bb from the
  relation turn). No other call sites exist.
- read_file call sites: /proc/self/status (rss), the lane's own
  roster_trace.txt (trace append), the lane's own state.bin, and the
  turn file. No briefing/key/idmap/proof reads. worlddir is only
  arg-presence-checked.
- Brief turns are no-ops in the contestant ("No specific action
  needed"); the sealed brief turn is the empty {"turn":0,"kind":"brief"}.
  Briefing content cannot enter the roster.
- Grep audit reproduced: zero hits for all 10 sealed entity names
  (Kavipe, Sehiru, Zovina, Datamo, Zovinu, Tetaru, Zosumo, Dagumo,
  Zofiru, Segunu) in the mechanism source.
- The listnames handler (line 1259) dispatches on the head string
  only, then reads learner state via roster_count/roster_emit. Empty
  roster replies UNKNOWN.

## Axis 6: Determinism and ablation

Verified from committed run evidence (f8d7b9b2e), all reproduced
above under Axis 1 (K3) and the K6 paragraph:

- 3/3 stripped reply streams byte-identical; 3/3 roster traces
  byte-identical; hashes match the eval's claims exactly.
- All 3 runs: C15 = 0.947, total 0.808, per-cap table identical.
- Ablation: surgical delta confirmed (only the 3 call sites commented
  out); C15 = 0.000, total 0.794, all other caps unchanged, item 63
  replies UNKNOWN. The roster is causally necessary for the gain.

## Axis 7: The 15-vs-16 discrepancy

Verified. The sealed battery.json (refreeze run1 world) contains 68
items across 16 distinct capabilities numbered 1..16 (cap 15 n=1,
cap 16 n=6). The lane's use of "16 capabilities, 68 items" reproduces
from the sealed records; the "15 capabilities" phrasing in earlier
parent task texts does not. The lane flagged the discrepancy rather
than asserting either count, which is the honest handling.

## Axis 8: Knowledge vs architecture (generality)

Assessment, from the verified source:

- The roster POPULATION is general: every entity observed in any
  fact or relation exposure is recorded, independent of any question.
  The structure accumulates learner experience; the 9-name roster on
  the sealed item is genuinely experience-derived.
- The listnames HANDLER is wire-protocol-specific: it fires on the
  literal "listnames" head. A differently worded goal question would
  score 0. This matches the v6 base's established pattern (fact/hop2/
  conflict/zem handlers all dispatch on question heads), so it is not
  a new architectural smell, but the mechanism's transfer to a fresh
  battery with different goal phrasing is untested.
- Honest bounds, all disclosed or visible: 12-slot cap with no
  eviction (a 13th distinct entity would be silently dropped);
  exact-string dedupe (no aliasing); enumeration in first-appearance
  order (irrelevant to this scorer, untested elsewhere).
- Architecture accounting holds: 164 added lines, 0 removed, 0 new
  modes/bridges/routers/gates/semantic cases, one learner-state
  structure at the documented offset. The lane explicitly disclaims L3
  and scopes every claim to the sealed battery; the canonical 0.573
  is not moved.

None of this threatens the BUILD-PASS: every frozen bar is met on the
evidence, and the lane's own caveats cover the generality bounds. The
right follow-up is a fresh-battery transfer test (different goal
phrasing, more entities than slots), not a verdict change.

## Observations (non-blocking)

1. Documentation imprecision: C15_AUDIT.md and SEALED_EVAL.md attribute
   sha256 3899577b... to "competitive_arena/arena.zag". That hash is
   the compiled scorer BINARY (as the refreeze record states); the
   source file's sha256 is
   76033aae69e2e473f7c4963f2e0121245fbd937626f070930c49ae142af570b4.
   Cosmetic only: the binary the lane used rebuilds byte-identical
   from the frozen source, as shown above.
2. Reviewer toolchain disclosure: while composing one compound shell
   command during this review I typed a stray `python3 -c` fragment;
   the shell could not resolve python3 (command not found, nothing
   executed, no output produced). No Python ran at any point in this
   review. Recorded per the guard's disclosure norm.

## Toolchain

safebin PATH for the whole review. `which python3` and `which python`
print nothing (exit 1) at review start. All verification used safebin
shell tools (git, grep, sed, awk, wc, sha256sum, diff, cmp) and one
pinned-znc rebuild of the frozen scorer source. Zero interpreter
invocations beyond the disclosed non-resolving fragment above.
