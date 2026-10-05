# INDEPENDENCE AUDIT -- CAN A STRANGER CHECK THIS?

Follow-up to `RED_TEAM.md`. The red team's deepest objection was that
every mitigation is authored by the same person who wrote the
experiments. That cannot be fixed from inside. What *can* be fixed is
whether a stranger is **able** to check it.

Question: if you had never read my reports, could you take this repo
and verify the headline negative result?

## METHOD

Deliberately did not read `REPORT.md` first. Cloned the branch cold,
built from source, and hand-derived the bars from raw output and from
the source lines.

## RESULT: YES -- the headline bars are externally checkable

### IA-1: reproduces from a cold clone

```
git clone --branch lane/ownership --single-branch https://github.com/Sylorlabs/TNN.git
cd docs/lab/research-lead/overnight-20260928/borrow/borrow6
znc --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache b6.zag && ./b6
```

Three runs plus the committed `run.txt` all hash to
`7129e4bf89448642b396e7267ae062a48d6f95a9bd2800c2454130253c0aa93e`.
(That was the sha at audit time; IA-7 then removed two always-true
bars, changing it to `cc6903bdf249cd2bfb810f5233eb7013665ee9f1b5e90aa80f5b0a9ccd6a926b`.
The measurement rows are identical -- only the tail changed.)
Self-contained: no `include`, no file reads, no external calls
(`strings` scan for LLM/HTTP/socket symbols: 0 hits;
`tnn_pure_zag_report`: `PURE-ZAG-CLEAN`).

### IA-2: the central structural claim is provable by hand in six numbers

From raw output alone:

```
Q_C=(10,121) answer=11   key=14
Q_A=(20,111) answer=22   key=14    DERIVED SIGNATURE keys differ=0
Q0 eligible = 12 11 12
Q1 eligible = 22 21 22
```

`key = cls0*4 + cls1`, so `key=14` on both queries means both reduce
to the same class pair. **Types cannot separate these queries** --
verified from the `keys differ=0` field, not from my interpretation.

Correct answers are `11` (in `{12,11,12}`) and `22` (in `{22,21,22}`).
The correct structure is length 1 on one query and length 2 on the
other, so **any fixed length preference scores exactly 1 of 2**. That
proves `LEN1_only=1`, `LEN2_only=1`, `TIES=1` without reading a line of
scoring code.

This is the right kind of evidence: the kill is a property of the
world, checkable by inspection.

### IA-3: the headline bars are computed, not asserted

```
B3 best fixed control  -> max over scores[0..2]
B4 best principle      -> max over scores[4..6]
B9 principle_beats_all_fixed -> 1 iff bestPrin > bestFixed
```

Real maxima over the arm scores. Not literals.

### IA-4: per-arm scores are set by comparison against ground truth

```
591:  let okC:i32=0; let okA:i32=0;
614:  if(t==19){ if(get32(pc,0)==ansC){ okC=1; } }
635:  if(t==19){ if(get32(pa,0)==ansA){ okA=1; } }
```

A score flips to 1 only when the emitted result equals the
independent `ansC`/`ansA`. Correct bar structure.

## WHAT THE AUDIT FOUND AGAINST ME

### IA-5: `tnn_bars_lint.sh` reports 3 violations on b6 -- ALL THREE FALSE POSITIVES

```
R3-B VIOLATION ... verdict-named bar 'okC' assigned only a bare literal.
R3-B VIOLATION ... verdict-named bar 'okA' assigned only a bare literal.
R3-B VIOLATION ... verdict-named bar 'pass' assigned only a bare literal.
```

All three are false positives:
* `pass` (line 387) is a loop counter, incremented at 442.
* `okC`/`okA` (591) are accumulators set at 614/635 under a
  comparison against ground truth.

The lint cannot see that an assignment is *conditional on a
comparison*. This is the same false-positive class as fixture M4 in
`RED_TEAM.md`, and it is the **common** case, not the exotic one.

### IA-6: the lint MISSES the two bars that really are hardcoded

`run.txt` ends with:

```
BAR B7_named_modes=0
BAR B8_L3=0
```

These are bare string assertions -- always true, computed from nothing.
`RED_TEAM.md` §A6 calls exactly this shape "structurally incapable of
falsifying its hypothesis." The lint sees them only as a *note*
(pattern C, constant inside a label string), never a violation.

So on this file the lint produced **3 false positives and 2 false
negatives**. Net: worse than useless if read as a gate.

### IA-7: SHARPER INSTRUMENT VERDICT

| | count on b6 |
|---|---|
| real hardcoded bars missed | 2 (`B7`, `B8`) |
| false positives | 3 |
| true positives | 0 |

`B8` had a **fourth** spelling: the literal `0` passed as an argument
(`c=o_i64(ob,c,0)`) rather than inside the label string. Both have now
been removed from the source and from `run.txt`.

**Revised conclusion, superseding `RED_TEAM.md` RT-C:** the lint's
value is not enforcement. It is *naming suspicious identifiers so a
human looks at them*. On a clean file it is pure noise. Anyone treating
`RESULT=CLEAN` as certification, or `RESULT=FAIL` as a defect, is
misusing it. `B7`/`B8` should be deleted from `run.txt` -- they are
static properties checkable by lint, not measurements.

## WHAT THIS DOES NOT ESTABLISH

The audit was performed by the author of the experiments. It
establishes **checkability**, not **independence**. I cannot supply
the missing thing, and the honest position is unchanged from
`RED_TEAM.md`:

> A different person should repeat IA-1 through IA-4 without reading
> `RED_TEAM.md`. If they reach IA-4 and find `okC` set from a literal,
> the result is void.

The single highest-value check remains ~5 minutes of work: build
`b6.zag`, read lines 591/614/635/648-660, and confirm the bars are
derived. Anyone can do it, and until someone who does not already
believe me does it, this lane's central negative is unreplicated.