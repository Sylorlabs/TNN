# SEALED EVALUATION: ARENA-REMAP (wave-20261001-2321pdt, ARENA2 lane)

Independent sealed evaluation of the frozen REMAP contestant
(bin/remap, sha256
4a80837a2ad90779c156584ec0be80aabc548ac6c29e5ec91d940ce010ec9a21,
built from the committed implementation source remap_contestant.zag
with the pinned znc; zero source changes after the build)
on the regenerated sealed world (seed 71503461337030).

Scoring: per hidden item, 1000 if the reply string exactly equals the
key, else 0 (arena.zag generic branch; C12 has no special scoring).
Keys computed by the world generator, never by running the contestant.

## Per-bar results

### K1 (C12 transfer): PASS, 6/6 = 1.000

All three sealed runs: C12 6/6. White-box trace (remap_trace.txt,
byte-identical all runs):
  remap_prod out=2,3,0 (x3)
  remap_class reply=yes / no / yes
The 3 remap_prod replies are the learned B template under the
runtime-parsed permutation; the 3 remap_class replies compare the
runtime-parsed candidate triple against the permuted learned A
template. No sealed value is hardcoded anywhere in the mechanism.

### K2 (no regression): PASS

Per-capability scores, v6 refreeze vs REMAP (all three runs identical):

| Cap | n | v6 | REMAP |
|-----|---|------|-------|
| 1 | 6 | 1.000 | 1.000 |
| 2 | 4 | 1.000 | 1.000 |
| 3 | 6 | 1.000 | 1.000 |
| 4 | 4 | 1.000 | 1.000 |
| 5 | 6 | 1.000 | 1.000 |
| 6 | 3 | 1.000 | 1.000 |
| 7 | 3 | 1.000 | 1.000 |
| 8 | 4 | 0.000 | 0.000 |
| 9 | 3 | 0.000 | 0.000 |
| 10 | 2 | 1.000 | 1.000 |
| 11 | 2 | 1.000 | 1.000 |
| 12 | 6 | 0.000 | 1.000 |
| 13 | 6 | 1.000 | 1.000 |
| 14 | 6 | 1.000 | 1.000 |
| 15 | 1 | 0.000 | 0.000 |
| 16 | 6 | 1.000 | 1.000 |
| TOTAL | 68 | 0.794 | 0.882 |

Every non-target capability is byte-identical to the v6 refreeze
record. Zero score regressions on all 15 non-target capabilities.
Total 60/68 = 0.882 on all three runs.

### K3 (determinism): PASS

3/3 full sealed runs produce byte-identical stripped reply streams
(sha256 d429e2e6c8bc9671e2822ca7a706badcb6b0a6a3ae71d1907114981bde3d6c17
all three; ms and rss_kb excluded, the v6 K6 exclusion class) and
byte-identical remap_trace.txt files (sha256
d10332976b5bf2fe8a97808522d1f4beb55da323aaee889a8bafc1787a66ee82
all three).

### K4 (pure Zag): PASS

Zero non-safebin executable invocations in this lane: bash sequenced
the pinned znc builds, the compiled binaries, git read/commit ops,
and file copies only. `which python3` prints nothing at lane start
(NAMECHECK.md Step 0) and lane end (exit 1, verified 2026-10-01).
No PROCESS-FAIL event.

### K5 (sealed validity): PASS

- competitive_arena/ unmodified (git status clean).
- world_gen rebuilt from committed source: sha256
  c4c8340c818e6848c88e34f1989bf382ff097c69a71d6621c6bf28b58dc85211,
  matches the refreeze record. arena rebuilt: sha256
  3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076,
  matches.
- Regenerated turns.jsonl sha256
  0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469,
  matches the sealed world.
- Pre-run answer_key.json sha256
  a05ef916122ea9643fa69e4a4973b94ea1c603da642d9bd07788f61b89a07a51,
  recorded before any contestant run.
- The contestant never opens key/idmap/proof files: grep of the
  mechanism source for answer_key/idmap/proof returns zero hits;
  worlddir is only arg-presence-checked.
- Grep audit of the mechanism source for the sealed remap
  permutation string returns zero hits; the permutation is parsed
  from each question at runtime. No sealed entity, value, template,
  or answer string appears in the source.
- Disclosure: while verifying the turn protocol from the committed
  sealed world, the worker saw the sealed C12 question strings
  (contestant-visible content). They are parsed at runtime, never
  hardcoded; the grep audit is the evidence.

### K6 (negative controls): PASS, both halves causal

- K6a ablation REMAP_PROD_OFF (remap_prod handler disabled,
  one-line source delta; binary sha256
  670c1a90a77b612307b1a8c93f96456a26db2e11573b4a9e1e416feb57eb68f4):
  the 3 remap_prod items reply UNKNOWN (0/3), the 3 remap_class
  items still pass. C12 = 3/6 = 0.500, total 57/68 = 0.838.
- K6b ablation REMAP_CLASS_OFF (remap_class handler disabled,
  one-line source delta; binary sha256
  efeba3df64c6ec855f36e79d9d2890a410047ed21fe802e9dbf7903e3e32db2a):
  the 3 remap_class items reply UNKNOWN (0/3), the 3 remap_prod
  items still pass. C12 = 3/6 = 0.500, total 57/68 = 0.838.
Each handler is necessary for its half; neither half is carried by
the other or by the base.

### K7 (architecture): PASS

Diff of the v6 base source against remap_contestant.zag: 94 lines
added, 0 lines changed. Additions: parse_qsegs4 (4-int question-part
parser), trace1 (decision-log appender), the two handler blocks, and
comments. Keyword scan of all added lines for mode/bridge/router/
gate: zero hits. Zero new modes, zero bridges, zero routers, zero
task-specific admission gates, zero hardcoded semantic cases. The two
new handlers are question-type handlers in the existing test-turn
dispatch, the established v6 pattern. Learner-state structures
created: none new (existing Zem template slots reused; the trace log
is a decision record, not cognitive state). Capability-source delta:
the transfer answers are computed from learner state (exposure
templates) plus the runtime-parsed permutation; source contributes
only the generic composition operation.

### K8 (no L3 claim): PASS (disclaimer recorded)

This mechanism does not meet Criterion 0: the "apply the
question-given permutation to the learned template output" semantics
is researcher-authored handler logic (fails C0-A runtime-defined
semantics); the recoding form is fixed, not incrementally constructed
from experience (fails C0-B); no unforeseen representational forms are
produced (fails C0-C); no new representation is invented, only an
existing template reused under a recoding (fails C0-D). Plainly:
REMAP is L2 transfer infrastructure (composition of learned structure
with a given recoding), not L3 representational invention. No L3
claim is made.

## Verdict: BUILD-PASS

K1 PASS (6/6), K2 PASS (60/68, zero regressions), K3 PASS (3/3
byte-identical), K4 PASS (pure Zag), K5 PASS (sealed validity),
K6 PASS (both ablation halves causal), K7 PASS (94 added, 0 new
modes/bridges/routers/handlers-as-gates/semantic cases), K8 PASS
(L3 disclaimed).

Scope reminders (unchanged): REMAP is a CANDIDATE only. No L3 claim,
no TNN-2 substrate claim, no TNN-beats-LLM claim. The canonical 0.573
is not moved by this result.

## Negative finding carried from the pick analysis (not built)

C9 (causal) as implemented is unpassable by any genuine causal
mechanism: the 12 causal observations satisfy x==y==z in every case
(chain permutation observationally unidentifiable by design), the
battery contains zero intervention turns, and the discrim items always
list the true chain first with key = chain[0], so the only 3/3
mechanism is question-format parsing (zero experience, zero causal
structure), rejected as gaming. The honest causal answer (UNKNOWN)
scores 0. Recommendation: the world generator should randomize
candidate order and add real intervention turns before any future
causal lane is attempted. This finding is recorded in NAMECHECK.md
and the prereg section 2.

## Toolchain

safebin PATH for the whole lane; `which python3` prints nothing at
start and end; zero Python or other interpreter invocations; shell
only sequenced pinned znc, built binaries, git read/commit ops, and
file copies. No PROCESS-FAIL event. Zero em-dash bytes in lane docs
(byte scan via check_no_dash.sh before each commit).
