# DDESGEN RESULT: N-Variable Generalization Test

Adversary prereg: c04d5610d (frozen before any implementation).
Target: the 4-variable generality bound found by Red Team 2
(b19e0e594): frozen `synthesize_plan` used `obs = 4 - v_star`,
valid only for 3-variable worlds.
Method: pure Zag, no Python, no em dashes. 3/3 byte-identical runs.

## Verdict: FIXABLE. K1, K2, K3 all PASS.

The 4-variable bound is an artifact of the observation action
encoding formula and hardcoded layout constants, not a deep
representational limit. A single generic encoding rule plus
parameterized state layout fixes all N with no per-variable-count
authoring.

## K1 (generalization attempted and documented): PASS

Prereg c04d5610d committed alone before implementation; this
document plus `ddes_gen.zag` describe exactly what was generalized
and what semantic authority remains researcher-authored (see
"Authority analysis" below). Commit order verified:
prereg strictly precedes implementation.

What was generalized (one-time researcher-authored changes,
each a single generic rule):

1. `synthesize_plan_gen`: `obs = 4 - v_star` replaced by
   `obs = 2 + v_star`. Codes 0=S, 1=W stay reserved;
   observing variable v uses code 2+v. Valid for all v >= 1.
2. `world_step_gen`: 3-variable state layout replaced by a
   parameterized layout for n_vars=N (values st[v*4], time
   st[N*4], timestamps st[N*4+4+v*4]); observation dispatch
   `a >= 2` observes variable (a-2); propagation passes
   `pass < n_vars` (frozen: `pass < 3`).
3. `ddes_world_gen`: `n_vars` is a parameter (frozen: hardcoded 3);
   arrivals buffers 4N, state buffer 8N+4.
4. `emit_plan_gen`: prints O(v) for observation actions.
5. `predict_gen`: arrivals buffer sized 4*n_vars.

Unchanged (already generic): compute_arrivals, compute_frontier,
eff_waits were copied VERBATIM from frozen ddesr.zag. The
derivation core needed no changes at any variable count.

No per-variable-count branches, tables, or cases were introduced.
The generalization is a finite set of generic rules, each valid
for all N.

## K2 (tested on 3/4/5 variables): PASS

3/3 byte-identical runs, md5
38ba97968b396d53a95c3055dd64989a, exit 0, zero stderr.
Every line matches the frozen prereg expectations.

World A (3-var regression): TARGET V*=2 t*=1, PLAN [S,W,O2]
(code 4; the 3-var encoding shifts as designed, so byte-identity
with frozen runs is not expected).
- cfg0 (truth=H0): EXEC real=0, PRED h0=0 h1=1,
  SURVIVE h0, ELIM h1, CONVERGE-OK.
- cfg1 (truth=H1): EXEC real=1, PRED h0=0 h1=1,
  ELIM h0, SURVIVE h1, CONVERGE-OK.

World H (4-var, RT2 sealed): TARGET V*=3 t*=11,
PLAN [S,Wx11,O3] (length 13).
- cfg0: EXEC real=1, PRED h0=1 h1=0,
  SURVIVE h0, ELIM h1, CONVERGE-OK.
- cfg1: EXEC real=0, PRED h0=1 h1=0,
  ELIM h0, SURVIVE h1, CONVERGE-OK.
The RT2 generality break is closed: the plan now ends in a real
observation (code 5 = O3), not W.

World I (5-var, sealed in this prereg; delays 13/14 verified
absent from all frozen DDES source): TARGET V*=3 t*=13,
PLAN [S,Wx13,O3] (length 15).
- cfg0 (truth=H0): EXEC real=1, PRED h0=1 h1=0,
  SURVIVE h0, ELIM h1, CONVERGE-OK.
- cfg1 (truth=H1): EXEC real=0, PRED h0=1 h1=0,
  ELIM h0, SURVIVE h1, CONVERGE-OK.

SUMMARY ok=6/6, plans_built=6 (exactly 1 plan per config;
zero enumeration preserved at all variable counts).

## K3 (purity): PASS

Pure Zag at every stage (source, znc build, execution,
analysis). Zero Python invocations. Zero em-dash or en-dash
bytes in all committed files (byte-checked with grep -P).

## Authority analysis (task question 2)

Q: does the generalization require researcher-authored changes
per variable count, or can the learner derive the encoding?

A: Neither extreme. The fix required a ONE-TIME
researcher-authored change to a generic rule, not per-count
authoring. But the learner does NOT derive the encoding.

Concretely: DDES's synthesis computes the observation action
code via researcher-provided arithmetic (`2 + v_star`). The
action-to-effect mapping (code 5 means "read variable 3's cell")
is a convention shared between the synthesis function and the
world simulator, both researcher-written. The learner never
observes action effects, never tries alternative codes, never
infers the mapping from experience. DDES has no action-effect
model; its "learning" is the derivation of which variable to
target and when, not the discovery of what its actions do.

For the encoding to be learner-derived, the architecture would
need the learner to model action effects from experience (e.g.,
emit probe codes, observe which state cell changes, induce the
code-to-variable map). That is a fundamentally different
architecture, not a parameter change.

So: the bound is FIXABLE at the engineering level, and the fix
makes the researcher's encoding actually generic instead of
pseudo-generic. It does not transfer encoding authority to the
learner. Classification of the DDES lineage is unchanged:
strong L2 (guided one-shot derivation), NOT L3. The K3 finding
from the first adversary (guidance fully researcher-authored)
still stands; this work extends the honest L2 envelope from
3 variables to N variables.

## Net assessment

DDES now derives correct one-shot discriminating plans for
3, 4, and 5 variables with zero enumeration, zero length bound,
and exactly one plan per configuration. The derivation core
(arrival analysis, frontier, synthesis shape) was already
N-generic; only the action encoding and simulator layout were
3-specific, and both are now parameterized by single generic
rules. The remaining researcher-owned semantic authority is
explicit: the action vocabulary, its encoding, the hypothesis
format, and the analysis algorithm. A future architecture that
aims at L3 would need the learner to derive at least the
action-effect mapping from experience.

## Files

- PREREG_DDESGEN.md (c04d5610d)
- ddes_gen.zag (generalized implementation)
- DDESGEN_RESULT.md (this file)
- run1.txt, run2.txt, run3.txt
  (md5 38ba97968b396d53a95c3055dd64989a)
