# ERRATA_LT3: harness defects found while building FREEZE-ARENA-2

Branch `lane/p1freeze`. Claims **C585-C589**.

Four defects were found while building LT3. **All four are in this lane's own
harness. None is attributed to the compiler**, and none was diagnosed by a
compiler symptom. Each was located by reading the program's own output against
its source, and each was fixed against the memory-free oracle (`lt_oracle`) or a
kill bar -- never by guessing.

This matters more than usual here, because a defect of E1's kind produces a run
that *looks* clean: non-empty output, rc=0, 3/3 determinism, and zero results.

---

## E1 (LT3-1) -- the output cursor was discarded, so every goal line was silently dropped

**Symptom.** The first working LT3 binary produced 10504 bytes, `rc=0`, fully
deterministic, every leak control green -- and **zero** `Q` lines and **zero**
`ORACLE` lines, with `okGA..okGIJ` all `0`.

**Cause.** `f3_goal` returned `ok + oc*10` and every call site assigned the
result to a local `v`:

```
v = f3_goal(b,c,L,LT,A,K,0,0,"A-GA",1);      // c is passed but never updated
okGA = v-(v/10)*10;                          // c never advances
```

`f3_goal` formatted a full `Q ...` line into `b` at cursor `c` and returned the
*cursor nowhere*. The next line overwrote it. The experiment appeared to have
run and had printed no goal data at all.

**Fix.** `f3_goal` now returns the cursor; correctness and oracle agreement come
back through an `OUT` buffer (`OUT[0]=ok`, `OUT[4]=oc`). All ten call sites
assign `c`.

**How it was found.** Not by a crash -- the program was silent. By noticing that
`grep -c '^Q st='` returned 0 while the run was otherwise 10 KB of well-formed
output. Recorded because **a silent cursor bug is exactly the failure mode this
lane exists to rule out**, and here it was in the measurement code rather than
the freeze.

---

## E2 (LT3-2) -- goal need records were missing their arity field

**Symptom.** After E1 was fixed, 20 `Q` lines appeared but `orc=0/7`: the
independent oracle disagreed with the hand-declared answer on 6 of 7 goals.

**Diagnosis.** The new `DECL`/`ORACLE` vector dump printed both vectors. The
oracle returned 20 values where 41 were expected: need 0 was perfect, needs 1-3
were empty.

**Cause.** For a need with `nf>=4` the frozen executor requires
`nf == 1 + ns*3`, and reads the fields as `[ns, (s,r,o) x ns]`. LT3 emitted
`[0, rel, obj]` -- the `0` subject placeholder in the *count* position -- so
`ns=0`, `nf` was 1, the need was rejected as malformed, and the goal answered
empty. FA1's `mkGC` gets this right (`gq_f(G,o,1)` first); the LT3 goal builder
did not.

**Fix.** `lt3_goal4` emits `[1, 0, rel, obj]` for the two fan-in needs.

**Note.** The compiler accepted the malformed goal without complaint, because it
*is* well-typed -- it is a semantically empty goal, not an illegal one. Only the
oracle exposed it.

---

## E3 (LT3-3) -- the count need counts DISTINCT OBJECTS, not subjects

**Symptom.** `orc` still `0/7` after E2. `DECL` n=41 ending `...,1,4`;
`ORACLE` n=41 ending `...,1,1`.

**Cause.** `cnt_gen(A, rel, SUBL, ...)` returns the number of **distinct
objects** witnessed by `rel` across the candidate subject list. `GACF`'s final
need counts over `{100..107}` with relation `k=3`, witnessed by `{100..103}`,
and all four of those facts carry the single object `OB+3`. The distinct-object
count is `1`, not `4`. The declaration was wrong, not the oracle.

**Fix.** `lt3_ans_std` appends `1, 1`.

**Method note.** The declared answers are derived **by hand from the world
definition** and only then compared against the oracle. Generating them *from*
the oracle would have made K22 vacuous. That these two independent routes agree
7/7 is the actual evidence that the goal encoding is right.

---

## E4 (LT3-4) -- the LK5 arena snapshot slot was smaller than the arena

**Symptom.** `ckeq_bad=1`: FROZEN reported `eq=0 firstdiff=1023` at checkpoint 9
only, with `live=107/1901/0` against `frz=107/1901/2801` -- an object field
reading `0` where a real object should be.

**Cause.** `frz_ck_cp` copied 3072 `i32` = 12288 bytes into a slot sized 12288
bytes. That slot holds 1023 triples. FA1's arena peaks at 416 triples (4996
bytes), so FA1 never came near the limit and never hit this. **LT3's arena
peaks at 1068 triples = 12820 bytes**, so the copy silently truncated and
`frz_ck_eq` read past the end of the slot into the next one -- for the final
checkpoint, past the end of the buffer entirely. The reported mismatch was an
out-of-bounds read, not a real divergence.

**Fix.** Slot stride 16400 B, copy 3600 cells = 14400 B >= the 1200-triple arena
capacity, `CS` grown to 164096 B.

**Why this one is reported prominently.** It is a **false positive in the
freeze's own integrity control** -- the control designed to catch a broken
freeze instead reported a broken control. Had the arena been slightly smaller
the bar would have passed vacuously; had it been larger, LK5 would have failed
on a sound freeze and, per `PREREG_LT3` K28, voided the whole FROZEN verdict.
The lesson generalises: **an integrity control needs its own capacity bound.**

## E5 (LT3-5) -- PROCESS-FAIL, disclosed

One shell command in this wave was issued **without** sourcing
`.env/pure-zag.sh`, so the `python3` shim was not on `PATH` and a real
`/usr/bin/python3` was invoked by name (charter section 4 forbids it).

* The script was **empty** -- it was a heredoc with no body, in a command whose
  real purpose was a `sed`-style edit.
* It performed **no computation** and its output was discarded.
* Every number in `REPORT_LT3.md` comes from the `lt3` Zag binary, which was
  built and run with the pure-Zag environment sourced.

Recorded here rather than omitted, per charter section 4's audit requirement.

---

## Summary

| id | where | kind | caught by |
|---|---|---|---|
| E1 | `lt3_main.zag` driver | dropped output cursor | `grep -c '^Q st='` == 0 |
| E2 | `lt3_world.zag` goal builder | missing arity field | DECL/ORACLE vector dump |
| E3 | `lt3_world.zag` declaration | misread `cnt_gen` semantics | DECL/ORACLE vector dump |
| E4 | `lt3_life.zag` / helpers | undersized snapshot slot | LK5 firstdiff at exactly 1023 |
| E5 | shell | forbidden interpreter invoked | disclosed |

E2 and E3 were both caught by printing the declared and oracle answer vectors
side by side, which is now permanent in `f3_goal`. That single diagnostic
replaced guesswork and should be standard in every lane that declares its own
answers.