# SUBSTRATE RESULT: Shared Fact + Causal Substrate Prototype

Worker: I2 (Integration Architecture Worker).
Date: 2026-09-30.

## Verdict: SUBSTRATE-PROTOTYPED

All 3 kill bars pass.

## Commits (local, tnn-native-lab, owned path only)

- Prereg: `926598043` (committed alone before any implementation).
- Amend1: `c0c91f30a` (corrected stride formulas, added ep_processed
  field and specialization rule; re-frozen before implementation).
- Implementation + result: this commit.
- Commit order verified: prereg and amendment strictly precede
  implementation (git merge-base --is-ancestor).

## Kill bar verdicts

- K1 (incompatibility analysis): PASS. The prereg documents five
  incompatibilities between unified_learn.zag (2 variables, flat
  28-byte rules, online per-episode interface, flag-and-forget
  conflicts, fixed 65536-byte layout) and causal_learn.zag
  (3 variables, episodic entities with masks/effects/ambiguity/
  parents/support, batch interface, probe-driven contests, fixed
  8940-byte layout).
- K2 (design): PASS. The substrate makes variable count a runtime
  header field and makes causal hypotheses episode-supported
  structured entities. No variable-count constant appears in the
  machinery; all strides and offsets derive from nvar. Fact
  triples coexist with episodes and entries on one workspace.
- K3 (prototype): PASS. substrate.zag compiles with znc (warnings
  only, pre-existing style), runs fact episodes AND causal
  episodes on one W, passes all 10 frozen checks, is 3/3
  byte-identical (md5 7fc47e227ecdcae3e46049716dcfae11, exit 0,
  zero stderr), uses pure Zag at every stage, and contains zero
  em-dash bytes (byte-checked).

## What the prototype demonstrates

One workspace (32768 bytes, nvar=3 as runtime data) runs:

1. Fact learning: (cup,color,red), (cup,material,wood),
   (bowl,color,blue) learned; query returns red; teaching
   (cup,color,green) records conflict counter = 1 and the query
   returns green (latest wins).
2. Causal learning over 5 episodes with actions SETX and WAIT:
   general entries are created with empty condition masks; a
   conflicting episode marks the entry ambiguous and specializes
   it into two children split on the discriminating variable
   (first X, then Y); the probe episode resolves in favor of the
   correct child. Final state: 6 entries, 4 active, 2 ambiguous.
   Queries: (1,1,0) WAIT -> (1,1,1); (1,0,0) WAIT -> (1,1,0);
   (0,0,0) WAIT -> (0,0,0); (0,0,0) SETX -> (1,0,0). All correct.

## Architectural evidence (the Step B resolution)

The Step B block was not a porting failure but a design signal:
both systems hardcoded variable arity and hypothesis flatness at
compile time. The shared substrate removes all five
incompatibilities at the architecture level:

1. Variable arity is workspace data (header field), not source.
2. Hypotheses are structured entities with condition masks,
   per-variable effect kinds, ambiguity status, parents, and
   supporting episode lists, not fixed tuples.
3. Episodes are stored records, so the online protocol
   (sub_causal_update) and any future batch protocol share one
   learner.
4. Ambiguity is represented explicitly and resolved by
   specialization plus probe evidence, not flagged and dropped.
5. One region map is computed from nvar; fact, episode, entry,
   and string regions coexist without overlap.

## Honest limitations (not hidden)

- Effect vocabulary is UNCH/SET only (no ADD, no SET-with-delay);
  the validated causal_learn.zag has FX_ADD and richer machinery.
- Child2 support filtering carries only consistent support; a
  production version needs the full contest machinery for
  multi-support splits.
- Fact conflict policy is latest-wins with a counter; no belief
  revision semantics yet.
- The prototype does not rewrite unified_learn.zag. It proves the
  minimal common representation exists and runs. Adopting it as
  the unified learner's causal core is a defined follow-up, and
  per the architecture-review rule it would require re-validation
  of the unified test suite, not a silent swap.

## Files

- PREREG_SUBSTRATE.md (prereg + Amend1)
- substrate.zag (implementation)
- SUBSTRATE_RESULT.md (this file)
- SUBSTRATE_RAW.txt (run output, md5 7fc47e227ecdcae3e46049716dcfae11)

## Purity

Pure Zag at every stage (source, znc build, execution). No Python
invoked. Zero em-dash bytes in all committed files. Commits local
on tnn-native-lab; nothing pushed.
