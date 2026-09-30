# Substrate Synergy Phase 2: Result

## Verdict: SYNERGY2-TESTED

Both remaining synergy directions show a positive cross-mechanism
effect. All frozen kill bars hold.

## Frozen bars (from PREREG_SUBSTRATE_SYN2.md)

- K1: 2 synergy directions with measurable predictions P3, P4.
  Specified in prereg 4472d4a0b, committed alone before
  implementation.
- K2: P3 and P4 both hold (directional). N_proc=1 < N_blind=10.
  E_causal=20 < E_flat=420 at 20/20 accuracy both conditions.
- K3: pure Zag, zero Python, zero em-dash bytes, 3/3
  byte-identical (md5 f4c7c68e5067ee82484e0df578cd10a7),
  exit 0, zero stderr.

## Direction 3: procedure to experiment (P3)

World W3: 8 actions, frozen effect table
e = [2,5,0,7,1,6,3,4]. Passive phase records 8 procedure facts
(a_i, "eff", e_i) identically for both conditions. Hidden outcome
rule: O iff e(x)+e(y)=10. Valid pairs: (1,1),(3,6),(6,3),
(5,7),(7,5).

- COND-PROC (planner reads the procedure store, tests only
  sum-10 pairs in row-major order): N_proc = 1.
- COND-BLIND (planner ignores the procedure store, tests all 64
  pairs in row-major order): N_blind = 10.
- P3 holds: 1 < 10. The procedure store prunes 59 of 64
  candidates before any action.

## Direction 4: causal model to memory (P4)

World W4: 40 episodes (ep_i, cause c_i, effect e_i), learned once
and stored identically for both conditions as 80 flat episode
facts plus 40 causal index facts (e_i, "caused_by", c_i).
20 probes: e_0, e_2, ..., e_38.

- COND-CAUSAL (one index query per probe): E_causal = 20
  examinations, accuracy 20/20.
- COND-FLAT (linear scan of episode effect facts, then one cause
  query): E_flat = 420 examinations, accuracy 20/20.
- P4 holds: 20 < 420 at equal accuracy. The causal links act as
  a direct effect-to-cause index; without them retrieval is a
  linear scan.

## Capacity

Fact counts: P=8, B=8, C=120, F=120. No workspace near the
256-fact cap.

## Determinism

- 3/3 runs byte-identical.
- md5: f4c7c68e5067ee82484e0df578cd10a7.
- Exit 0, zero stderr bytes, zero non-ASCII bytes.
- Pure Zag: znc compiled and ran syn2.zag with no Python at any
  stage. The substrate core (fact store, init) is copied
  verbatim from substrate_syn.zag.

## Honest scope

The effect table, outcome rule, episode pairing, search order,
and retrieval routines are researcher-authored. Procedure facts
and causal index facts are learned from observation (one
observation each), but the learning is trivial recording. The
claim is comparative: the planner does better consulting the
procedure store than ignoring it, and the retriever does better
using the causal index than scanning flat episodes. This is not
a claim that the learner invented procedures, causal links,
planning, or retrieval. Combined with phase 1, all four required
synergy directions (concept to procedure, contradiction to
revision, procedure to experiment, causal model to memory) now
show positive cross-mechanism effects on the shared substrate.

## Commits

- Prereg: 4472d4a0b (alone, before implementation)
- Implementation + result: (this commit)

## Files

- PREREG_SUBSTRATE_SYN2.md
- syn2.zag
- SYN2_RESULT.md
- SYN2_RAW_1/2/3.txt, SYN2_ERR_1/2/3.txt (empty)
