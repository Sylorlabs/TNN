# ARENA_SYNTHESIS.md

# ARENA5 Synthesis for the Debate Group (wave-20261001-2321pdt)

Three lanes, three verdicts, one mechanism. This synthesis states
exactly what each verdict established, how they relate, and the
precise bounded claim that remains.

## 1. What each verdict established

### 1a. ARENA5: BUILD-PASS

Mechanism: DEFRECALL (defrecall_contestant.zag, commit 2320c3454),
an extension of the v6 baseline adding a persistent entity roster
(12x16 slot table at W offset 14000, populated by roster_touch
from learn_fact/learn_rel) plus a generic default action at the
existing fallback position.

Key numbers:

- K1: C15 = 0.947 on the fresh sealed 68-item battery (seed
  71503461337032), bar 0.900, on all three runs. The 0.947 is the
  honest experience-based ceiling: entity index 9 (Momado) never
  appears in expo turn events on any seed (structural, verified
  from the frozen world_gen source). Set F1 with the 10-name key:
  2000*9/(10+9) = 947.
- K2: 54.947/68 = 0.808 total; all 15 non-target capabilities
  byte-identical to the v6 fresh baseline. Zero regressions.
- K3: 3/3 byte-identical stripped reply streams and roster
  traces.
- K4: pure Zag; `which python3` prints nothing at lane start
  and end.
- K5: sealed validity holds (arena rebuilt to the refreeze hash,
  world_gen variant is a 1-line seed diff, pre-run hashes
  recorded, grep audit zero hits for all 10 sealed names).
- K6: ablation (three roster_touch call sites disabled): C15 =
  0.000, others unchanged. The roster is causally necessary; the
  default action alone hallucinates nothing.
- K7: diff vs v6 is 174 lines added, 0 removed, 0 changed.
  Zero new modes, bridges, routers, task-specific gates, or
  hardcoded semantic cases. Zero "listnames" hits in the
  mechanism source: zero dedicated goal handlers.
- K8: explicit L3 disclaimer recorded (fails C0-A, C0-B, C0-C,
  C0-D; L2 goal infrastructure, not representational invention).

Scope as frozen in the prereg: DEFRECALL is a CANDIDATE only.
No L3 claim, no TNN-2 substrate claim, no TNN-beats-LLM claim.
The canonical 0.573 is not moved.

The autonomy claim demonstrated: goal completion with no
dedicated handler, via the generic default action, whose trace
line reads "defrecall", not "listnames".

### 1b. RT-ARENA5: QUALIFY

Verdict: the BUILD-PASS stands. All 8 frozen kill bars hold as
frozen; the reviewer independently reproduced the load-bearing
evidence (byte-identical binary hash, 3/3 stripped streams and
traces, surgical ablations, commit-order self-check:
b63f80289 < f3320caf8 < 2320c3454 < 6582398e9).

The qualification (named, bounded): on the sealed battery the
generic default action is EXTENSIONALLY EQUIVALENT to a
listnames handler. Exactly one of the 68 test items is a bare
prompt (the C15 "listnames" probe). So the battery cannot
discriminate a truly general default action from a renamed
listnames handler. The generality evidence is therefore
intensional (zero goal-string branches in the source,
content-blind trigger) plus the lane's dev-probe demonstration
(prereg 7.4: novel bare prompts "recall" and "who" enumerate;
parameterized prompts abstain; empty roster abstains), both of
which the reviewer independently reproduced, including novel
probes of the reviewer's own ("summarize", "x", "what are
you" all enumerate; known head "fact" with empty params stays
UNKNOWN).

The qualification does not overturn any bar. It bounds what
the battery can discriminate, and it names the evidence the
generality claim rests on.

### 1c. ARENA-GEN: NARROW (verified VERIFIED by ARENA-GEN-VERIFY)

The follow-up lane built a multi-bare-prompt battery (7 test
items, fresh entities Alpha through Iota): items 0-2 must
enumerate (listnames, recall, who); items 3-6 must abstain
(whattime, bare invent, invent|notation, foo|bar). Frozen
decision rule in PREREG_MULTIBARE.md.

Results:

- AG-1 (C15 >= 0.900 on fresh 68-item seed 71503461337033):
  PASS (0.947, reproducing ARENA5 exactly).
- AG-2 (7/7 behaviors): FAIL, 5/7. "listnames", "recall",
  "who" enumerate correctly (1.000 each); "whattime" and bare
  "invent" enumerate the roster where exactly "UNKNOWN" was
  required; the two parameterized prompts abstain correctly.
- AG-3 (zero regressions): PASS. AG-4 (3/3 byte-identical):
  PASS. AG-5 (pure Zag): PASS.

Verdict per the frozen rule: NARROW.

What this establishes: the default action fires for EVERY bare
prompt whose head matches no specific handler (dispatch miss +
bare prompt + non-empty roster), regardless of whether
enumeration is semantically appropriate. The white-box trace
shows five defrecall firings for five bare prompts, including
"whattime" (the learner has no clock; the roster is not the
time) and bare "invent" (an incomplete invention request; the
roster is irrelevant to invention). The mechanism does not
discriminate; it applies a structural rule blindly. The
ARENA5 dev demonstration was one-sided: it tested only prompts
where enumeration is appropriate and counted the behavior as
generality.

ARENA-GEN-VERIFY recount verified all four checkable claims:
the per-prompt results hold, AG-2 is 5/7 exactly, the
DEFRECALL binary hash matches ARENA5's sealed build on all
three legs, and the battery and run hashes match the committed
evidence. (Limitation recorded honestly: the AG-1/AG-3 turn
files were not committed in that lane, so those two bars could
not be recounted; the NARROW's load-bearing claims all hold.)

## 2. How the three verdicts relate

- RT-ARENA5 qualifies the ARENA5 generality claim: on the
  sealed battery, extensionally, the default action equals a
  listnames handler, because the battery contains exactly one
  bare-prompt item. Intensionally (source audit), it is not a
  handler. The battery cannot tell; the source can.
- ARENA-GEN narrows the claim further: extensionally, across a
  diverse bare-prompt battery, the mechanism is a
  "bare-prompt handler", not a general default action. The
  generality is real in scope (it applies to all bare prompts,
  not one goal string) but shallow in content (it cannot
  distinguish appropriate from inappropriate enumeration).
- ARENA-GEN does NOT refute ARENA5's intensional claim: zero
  branches keyed on any goal or question string still holds
  (zero "listnames" hits, zero fresh-entity hits in source).
  ARENA5's BUILD-PASS stands on its own frozen bars.

The progression is: PASS on the bars as preregistered (ARENA5)
-> the bars cannot discriminate generality (RT-ARENA5) ->
the generality, tested directly, is indiscriminate
(ARENA-GEN).

## 3. The precise boundary of the DEFRECALL claim now

What DEFRECALL IS:

- A structural trigger: dispatch miss (prompt head not in the
  six existing handler heads) AND bare prompt (no parameters)
  AND non-empty roster. No question string or goal string is
  referenced anywhere in the trigger.
- Not a listnames handler: zero goal-string branches, proven by
  source grep and by firing on content-free bare prompts ("x")
  that no synonym list could cover without researcher-authored
  strings.
- 0.947 on the sealed battery, causally tied to the
  experience-built roster (K6 ablation: C15 = 0.000 with the
  roster off; supplementary run: C15 = 0.000 with the default
  action off, so the default action is the goal-completion
  path and no hidden handler carries the goal).
- Honest about absence: empty roster yields UNKNOWN with no
  trace line and no hallucination.
- Zero regressions across the other 15 capabilities; L2 goal
  infrastructure with an explicit no-L3 disclaimer; CANDIDATE
  status only; canonical 0.573 unmoved.

What DEFRECALL IS NOT:

- Not a general default action in the cognitive sense. It
  cannot discriminate which bare prompts warrant enumeration
  and which warrant abstention.
- It answers "whattime" with a list of names. It answers a
  bare "invent" with a list of names. A discriminating
  default would abstain on both.
- The "handler-free goal completion" is real but narrow: the
  mechanism volunteers persistent knowledge for any bare
  prompt, appropriate or not. Content-blindness is a
  structural fact, not a feature.

## 4. What would be needed to lift the NARROW

A discriminating trigger, not just "bare prompt". The needed
demonstration:

1. A mechanism that enumerates on "listnames", "recall",
   "who" (and novel appropriate bare prompts) while abstaining
   to UNKNOWN on "whattime", bare "invent", and other novel
   inappropriate bare prompts, with the negative cases
   supplied by an independent adversary (not the builder).
2. The discrimination must be general machinery or
   learner-created, not a researcher-authored whitelist or
   blacklist of prompt strings. Any prompt-keyed branch,
   enumerated synonym list, or researcher-supplied "invention
   vs recall" classifier reintroduces exactly the handler the
   lane removed and fails the one-system architecture
   accounting.
3. The discrimination must preserve K2 (zero regressions), K6
   (causal), and K7 (architecture) quality bars.

Open question for the research program: what general
learner-owned signal could mark a bare prompt as
"answerable from the roster"? A prompt-roster relevance
check, a learned abstention policy, or an emergent
question-type structure are hypotheses; none is demonstrated.

## 5. The debate question

Does the NARROW undermine the BUILD-PASS, or does the
BUILD-PASS stand within its bounded scope?

For "BUILD-PASS stands": the frozen bars were all met, no bar
moved, all evidence was independently reproduced, and the
intensional claim (zero goal handlers) is intact. NARROW tests
a discriminating-generality claim that ARENA5 never
preregistered as a kill bar; its prereg K7 bars only demanded
no goal handlers, and that bar is clean. Judging BUILD-PASS by
a bar the lane never froze would itself be a governance
violation.

For "NARROW undermines the advertised result": if
"handler-free goal completion via a general default action"
extensionally equals "handler-free but indiscriminate roster
enumeration on any bare prompt", the autonomy claim carries
less meaning than the language suggested. The dev-probe
demonstration was one-sided by design (only prompts where
enumeration is appropriate), and the generality evidence on
the sealed battery was, as RT-ARENA5 showed, indiscriminable
from a handler. A PASS that depends on never testing negative
cases is a PASS within a scope the battery, not the
mechanism, defined.

The honest position this synthesis takes: BUILD-PASS is valid
on its frozen bars and should not be retroactively re-graded.
But the mechanism's claim on the words "general default
action" is, after ARENA-GEN, untenable without the
discrimination result in section 4. The bounded claim in
section 3 is what the evidence supports: a content-blind
structural trigger that volunteers persistent knowledge. The
debate is whether that bounded claim is the thing worth
promoting, or the sign that the default-action direction
needs a discriminating trigger before it becomes cognitive
infrastructure.

No L3 claim anywhere in this synthesis. No canonical score
moved. Pure synthesis: no experiments were run, no mechanism
source was modified, no Python was invoked.
