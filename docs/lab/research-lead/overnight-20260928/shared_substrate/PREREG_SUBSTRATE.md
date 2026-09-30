# PREREG: Shared Substrate for Fact + Causal Learning (I2)

Frozen before any implementation exists. Any amendment is committed
transparently and re-frozen before implementation. No bar may be
altered after seeing results.

Worker: I2 (Integration Architecture Worker).
Date: 2026-09-30.

## Context

Integration Step B is BLOCKED (commit recorded in
integration_step_b/BLOCKED_REPORT.md). A "simple port" of the
validated causal machinery into unified_learn.zag would be a
redesign, not an integration. Per the research prompt section 22:
when integration reveals incompatible assumptions, that is
architectural evidence, and the correct move is to design a new
shared substrate.

Steps D and E succeeded (merged curricula run sequentially; FDCR
concepts form on the continuing workspace), so the goal is a
substrate that can host fact learning AND causal learning on one
continuing workspace, resolving the Step B incompatibility at the
architecture level rather than by porting.

## K1: Incompatibility analysis (frozen here)

### unified_learn.zag (1892 lines, W = 65536 bytes, fixed layout)

1. Causal store: 16 flat rules, 28 bytes each, at CBASE=1104.
   Rule = [used, cond_var, cond_val, action, effect_var, effect_val,
   status]. Exactly 2 variables (s0, s1) assumed everywhere.
2. Interface: per-episode online `clearn(W, base, s0, s1, act, ns0,
   ns1)` and `cpredict(W, base, s0, s1, act, out[2])`. No episodes
   are stored. No ambiguity representation. Conflicts are only
   flagged (status=2), never resolved.
3. The same W also hosts procedure learning (16 slots), bridge
   rules (4), intent store, string area. Fact learning happens on
   strings (lexicon/concepts in the DEVINT layers).

### causal_learn.zag (1057 lines, W = 8940 bytes, fixed layout)

1. Exactly 3 variables assumed everywhere. All indexing is
   `i*3+v`; masks are 3-bit; workspace offsets hardcode the
   3-variable stride.
2. First-class episodes: state[3], action, next_state[3], status,
   sequence number. Up to 256 episodes (nep counter).
3. Entities: per-action hypotheses with condition mask over the 3
   variables, per-variable condition values, per-variable effect
   kind (UNRES/UNCH/SET/ADD) plus effect parameter, ambiguity flag,
   parent pointer, supporting episode list (up to 64).
4. Contests: competing entities for one action are resolved by
   probe evidence (find_contest, new_contest, contest_feed).
5. Interface: batch file processing
   (`causal_learn <obs.txt> <probe.txt>`), not per-episode calls.
6. The 14/14 validation applies to the batch interface on
   3-variable problems only.

### Why the port fails (five incompatibilities)

1. Variable arity: 2 (compile-time, unified) vs 3 (compile-time,
   causal). Changing either side breaks its own validated tests.
2. Rule representation: flat stateless match-and-fire rules vs
   structured episodic entities with masks, effects, ambiguity,
   parents, support lists.
3. Learning protocol: online per-episode updates vs batch
   accumulate-then-split/contest/merge.
4. Ambiguity handling: flag-and-forget vs explicit candidates plus
   probe-driven contests.
5. Workspace layout: two fixed, incompatible region maps; no free
   8940-byte region in unified's 65536-byte W that avoids the
   procedure/bridge/intent stores.

### Architectural evidence (the diagnosis, not a verdict)

The incompatibility is not an accident of coding style. It is
evidence that both systems hardcode the same design decision at
compile time: the number of state variables and the flatness of
the hypothesis representation. A shared substrate must make both
decisions runtime data:

- variable count is a workspace header field, not a constant;
- a causal hypothesis is an episode-supported structured entity,
  not a fixed 7-field tuple;
- episodes are stored records, so batch and online protocols can
  share one learner (online = batch of one followed by an
  incremental contest pass).

## K2: Shared substrate design (frozen here)

### Name

`substrate.zag`: one continuing workspace W holding a fact store
AND an episodic causal store, with nvar as a runtime header
field.

### Workspace layout (prototype scale)

W = 32768 bytes. Header (64 bytes at 0):

- 0: magic 0x53554253 ("SUBS")
- 4: nvar (runtime variable count, 1..8)
- 8: ep_stride (bytes per episode record, computed from nvar)
- 12: ent_stride (bytes per causal entry, computed from nvar)
- 16: ep_base (offset of episode records)
- 20: ent_base (offset of causal entries)
- 24: fact_base (offset of fact triples)
- 28: str_base (offset of string area)
- 32: str_cursor (bump allocator position)
- 36: ep_count
- 40: ent_count
- 44: fact_count
- 48: seq (global sequence counter)
- 52: max_ep (64), 56: max_ent (64), 60: max_fact (256)

Episode record (ep_stride bytes):
seq(4), state[nvar bytes], action(1 byte), next_state[nvar bytes].
Remaining bytes zeroed. Stride = 8 + 2*nvar, rounded up to 4.

Causal entry (ent_stride bytes):
used(4), action(4), mask(4), cond_vals[nvar*4],
fx_kind[nvar] (0=UNRES,1=UNCH,2=SET),
fx_param[nvar*4], status(4) (0=active,1=ambiguous,2=superseded),
parent(4), support_count(4), support[8*4].
Stride = 32 + 8*nvar, rounded up to 4.

Fact triple (12 bytes): e_off(4), a_off(4), v_off(4). Strings live
in the string area (bump allocator). A later triple with the same
(e,a) and a different v records a conflict (fact_conflict
counter) and the query returns the latest.

### Generic functions (all nvar-parametric, no variable-count
constants in code)

- `sub_init(W, nvar)`: validate 1<=nvar<=8, compute strides,
  lay out regions, zero counters.
- `sub_fact_learn(W, e, a, v)`: intern strings, append triple,
  bump conflict counter on (e,a) value change.
- `sub_fact_query(W, e, a, out)`: latest matching triple, or 0.
- `sub_episode(W, state, act, next)`: append one episode record.
- `sub_causal_update(W)`: incremental learning over new episodes:
  for each unprocessed episode, find matching active entries
  (action equal, masked condition matches); if none, create an
  entry with mask=all variables set to the episode state and
  per-variable effects (UNCH if next==state, else SET to
  next value); if a matching entry predicts a different effect
  for some variable, mark it ambiguous, create a child entry
  that specializes the condition (adds the discriminating
  variable value from the episode), and let the next probe
  episode resolve: children whose predictions match survive,
  the parent is superseded.
- `sub_causal_query(W, state, act, out_next)`: most specific
  matching active entry predicts; if two active entries match
  and disagree, return 2 (ambiguous); if none match, return 0.

### Prototype demonstration (frozen scenario)

One main() on one W with nvar=3, running BOTH:

1. Fact episodes: learn (cup,color,red), (cup,material,wood),
   (bowl,color,blue). Query (cup,color) -> red.
   Then teach (cup,color,green): conflict recorded, query ->
   green (latest wins), conflict counter = 1.
2. Causal episodes on a 3-variable world with actions SETX and
   WAIT. World law: SETX sets X=1. WAIT: if X=1 and Y=0 then
   Y=1; else if X=1 and Y=1 and Z=0 then Z=1; else nothing.
   Episodes (state X,Y,Z):
   e1: (0,0,0) SETX -> (1,0,0)
   e2: (1,0,0) WAIT -> (1,1,0)
   e3: (0,0,0) WAIT -> (0,0,0)
   e4: (1,1,0) WAIT -> (1,1,1)
   e5 (probe): (1,0,0) WAIT -> (1,1,0)
   Expected: after e2 the WAIT entry predicts Y:=1 under cond
   X=1. e3 creates a second WAIT entry (cond X=0, all unchanged).
   e4 conflicts with the e2 entry on Z, which becomes ambiguous
   and specializes into X=1&Y=0 (Y:=1) and X=1&Y=1 (Z:=1).
   e5 resolves in favor of the X=1&Y=0 child. Final query
   (1,1,0) WAIT -> Z:=1. This demonstrates stored episodes,
   structured entities, ambiguity, specialization, and
   probe resolution on the shared substrate.
3. Determinism: 3/3 byte-identical runs required.

### What the prototype does NOT claim

It does not claim the full split/merge/contest machinery is
ported, and it does not claim unified_learn.zag is rewritten.
It demonstrates the minimal common representation that removes
all five incompatibilities: nvar-parametric episodes and
structured entities coexist with fact triples on one workspace.

## Kill bars

- K1 (analysis): this prereg documents the five
  incompatibilities. Kill: analysis missing or misstates either
  file.
- K2 (design): this prereg specifies the substrate layout and
  functions. Kill: any fixed variable-count constant in the
  design, or no fact store coexisting with the causal store.
- K3 (prototype): the committed prototype compiles with znc,
  runs fact episodes AND causal episodes on one W, passes the
  frozen scenario expectations, is 3/3 byte-identical, uses pure
  Zag (no Python at any stage), and contains zero em-dash bytes.
  Kill: any failure.

## Commit order

This prereg is committed alone. The implementation commit must be
a strict descendant, verified with git merge-base --is-ancestor
before the result is reported.
