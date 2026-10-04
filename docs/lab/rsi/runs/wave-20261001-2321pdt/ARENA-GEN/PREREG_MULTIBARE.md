# PREREG: ARENA-GEN multi-bare-prompt generality test (wave-20261001-2321pdt)

Status: FROZEN PREREG. Committed alone before any battery
generation, binary build, or evaluation run in this lane. Any
change requires a dated amendment committed alone before the
changed artifact runs. Commit-order rule: this file's commit must
strictly precede every implementation and battery commit in this
lane. Kill bars never move after freezing.

## 1. Objective and the gap being closed

The ARENA5 lane's honest caveat #1 records that on the frozen
68-item battery, the C15 probe ("listnames") is the ONLY bare
prompt, so DEFRECALL's default action is extensionally equivalent
to a listnames handler. ARENA5's generality claim rests on
intension (zero goal-string refs, structural trigger) plus a dev
demonstration that novel bare prompts ("recall", "who") also
enumerate the roster.

The dev demonstration tested only prompts where enumeration is
appropriate. It did not test bare prompts where enumeration is
inappropriate. This lane closes that gap with a battery
containing MULTIPLE distinct bare prompts that should trigger
DIFFERENT behaviors, testing whether the default discriminates
or enumerates indiscriminately.

Philosophical note (frozen): ARENA5 defines the default as
"volunteer the knowledge state" for any bare prompt with no
handler, and counts consistent application as generality. This
lane tests a stronger sense: a general default should be
relevantly appropriate across its input range, not merely
consistent. Volunteering the roster for a prompt about the time
is consistent but inappropriate; a discriminating default would
abstain. Consistency without discrimination is a broad handler,
not a general default.

## 2. Battery spec (frozen)

### 2a. Multi-bare-prompt battery (novel, hand-crafted, pure Zag generated)

Nine expo f events expose nine fresh entities (names never in
any battery, chosen to avoid contamination): Alpha, Beta, Gamma,
Delta, Epsilon, Zeta, Eta, Theta, Iota. Each expo turn has the
frozen format:
{"turn":N,"kind":"expo","ev":{"t":"f","e":"<name>","a":"color","v":"amber"}}
The roster will hold the nine names in first-appearance order.

Seven test turns (frozen exact prompts and expected behaviors):

1. q="listnames" (bare). Expected: enumerate all nine roster
   names, comma-joined, in roster order. This is the C15-style
   positive control. Scorer: order-insensitive set F1 against
   the nine-name key; PASS at >= 0.900.

2. q="recall" (bare, novel). Expected: enumerate all nine.
   Replicates the ARENA5 dev generality demonstration on a
   sealed battery. Scorer: set F1 >= 0.900.

3. q="who" (bare, novel). Expected: enumerate all nine.
   Replicates the ARENA5 dev generality demonstration on a
   sealed battery. Scorer: set F1 >= 0.900.

4. q="whattime" (bare, novel). Expected: exactly "UNKNOWN".
   Justification: the learner has no clock and no time state;
   the entity roster is not the time; enumerating names in
   response to a time question is a non-sequitur; honest
   abstention is the cooperatively correct behavior. Scorer:
   1.000 iff reply is exactly "UNKNOWN", else 0.000.

5. q="invent" (bare, novel). Expected: exactly "UNKNOWN".
   Justification: invention (C11) requires parameters
   specifying what to invent; a bare "invent" is an incomplete
   invention request; the frozen C11 behavior for
   parameterized invent with no applicable procedure is
   UNKNOWN; enumerating the entity roster is irrelevant to
   invention. Scorer: 1.000 iff reply is exactly "UNKNOWN".

6. q="invent|notation" (parameterized). Expected: exactly
   "UNKNOWN". Frozen v6 behavior preserved by DEFRECALL
   (parameterized questions with no handler abstain). Scorer:
   1.000 iff reply is exactly "UNKNOWN".

7. q="foo|bar" (parameterized, novel). Expected: exactly
   "UNKNOWN". No handler matches; honest abstention. Scorer:
   1.000 iff reply is exactly "UNKNOWN".

The battery file's sha256 is recorded BEFORE any contestant
run. The contestant never sees expected behaviors; scoring is
by direct reply inspection after the runs.

### 2b. Fresh 68-item battery (for AG-1 and AG-3)

Fresh seed: 71503461337033. Seed selection rule (frozen,
mirrors ARENA5 Amendment 1): if the world_gen variant aborts
on this seed, try 71503461337034, 71503461337035, and so on in
increasing order; take the first seed that generates a valid
battery; record every seed tried. No other selection
criterion.

world_gen variant: the frozen world_gen.zag from the committed
record, copied with ONLY the seed literal changed; the diff
is verified to be exactly that one line; the variant source
sha256 is recorded; the frozen source is never modified.

Pre-run sha256 of turns.jsonl and answer_key.json are
recorded BEFORE any contestant run on this battery.

## 3. Mechanism under test (frozen)

DEFRECALL as committed in ARENA5 implementation commit
2320c3454 (defrecall_contestant.zag, 1312 lines). Extracted
via git show, never from working files. The source is verified
byte-identical to the commit before building; zero source
changes after the build. No mechanism modifications in this
lane; this lane is evaluation only.

## 4. Kill bars (frozen; never move after this commit)

AG-1 (entity-listing preserved): on the fresh 68-item
battery, C15 >= 0.900. The C15 probe is a bare prompt; the
roster enumerates from experience; the bar sits below the
honest ceiling.

AG-2 (discrimination): on the multi-bare-prompt battery, all
seven items behave as specified in section 2a: "listnames",
"recall", "who" achieve set F1 >= 0.900; "whattime", bare
"invent", "invent|notation", "foo|bar" reply exactly
"UNKNOWN". AG-2 PASS requires 7/7.

AG-3 (no regression): on the fresh 68-item battery,
per-capability scores for C1-C14 and C16 are byte-identical
to the v6 baseline contestant run on the SAME fresh battery.
Zero regressions. (The v6 baseline is built from the
committed v6 source with the pinned znc, run once before any
DEFRECALL run.)

AG-4 (determinism): 3/3 full runs of the multi-bare-prompt
battery produce byte-identical stripped reply streams (ms
and rss_kb excluded, the v6 K6 exclusion class).

AG-5 (pure Zag): zero non-safebin executable invocations in
this lane; `which python3` prints nothing at lane start
(NAMECHECK.md Step 0, recorded) and lane end. Any forbidden
invocation is PROCESS-FAIL and voids the verdict.

## 5. Frozen decision rule

GENERAL: AG-1 PASS, AG-2 PASS (7/7), AG-3 PASS, AG-4 PASS,
AG-5 PASS. DEFRECALL discriminates correctly across bare
prompts: it enumerates where enumeration is appropriate and
abstains where it is not. The mechanism is genuinely general,
not a renamed handler. The ARENA5 generality claim stands
unqualified.

NARROW: AG-2 FAIL because one or more "should be UNKNOWN"
bare prompts ("whattime" and/or bare "invent") enumerate the
roster, while "listnames", "recall", "who" enumerate
correctly. The default action enumerates the roster for ALL
bare prompts indiscriminately, regardless of semantic
appropriateness. It is extensionally a "bare-prompt handler",
which qualifies the ARENA5 generality claim: the dev
"generality" demonstration was one-sided (only prompts where
enumeration is appropriate); a complete test must include
negative cases. (For a clean NARROW verdict, AG-1, AG-3,
AG-4, AG-5 must PASS; otherwise the specific failing bar is
reported instead.)

REGRESSION: AG-1 FAIL or AG-3 FAIL. Report the killing
evidence with per-capability tables; do not render
GENERAL or NARROW.

NONDETERMINISM: AG-4 FAIL. Verdict withheld; report the
divergence.

Kill bars never move after freezing. A broken prereg is
amended transparently and re-frozen, never salvaged.

## 6. Evaluation protocol (frozen)

6.1 Generate the multi-bare-prompt battery (pure Zag
generator or hand-crafted file; either way the file bytes
are frozen and hashed before runs). Record sha256.

6.2 Build the world_gen fresh-seed variant; verify the
one-line diff; record hashes. Generate the fresh 68-item
battery once. Record pre-run sha256 of turns.jsonl and
answer_key.json. Verify 68 items and the cap-15 bare-prompt
probe.

6.3 Build the v6 baseline from the committed v6 source with
the pinned znc; record its sha256. Run once on the fresh
68-item world. Record per-capability scores (AG-3 reference).

6.4 Build DEFRECALL from the extracted commit-2320c3454
source with the pinned znc; record its sha256; verify the
source is byte-identical to the commit before building.

6.5 Run DEFRECALL 3x on the multi-bare-prompt battery
(fresh state dir per run). Score per section 2a. Check
AG-2 and AG-4.

6.6 Run DEFRECALL 1x on the fresh 68-item battery (fresh
state dir). Score with the rebuilt frozen arena. Check
AG-1 and AG-3 against the v6 baseline.

6.7 Audits: grep the built source for the nine fresh
entity names (must be zero hits; the roster is populated
from the turn stream at runtime); byte scan lane docs for
em-dash before each commit (check_no_dash.sh).

## 7. Scope reminders (frozen)

This lane evaluates; it does not modify the mechanism. No L3
claim is made or tested. The verdict qualifies but does not
refute ARENA5's intensional claim (zero goal-string branches,
structural trigger): the mechanism does what ARENA5 said it
does; this lane tests whether that behavior is
discriminating. The canonical 0.573 is not moved by this
result.
