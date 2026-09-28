# GUIDED LEARNING (gl) SLOWNESS — FINAL SYNTHESIS

**For Micah — plain language. Your question, your words: "why does
guided learning run so much slower, is it worth it, or is there free
lunch?"**

Terminology: "guided learning (gl)" is your final pick for the
paradigm formerly called scaffold-and-release. Used throughout.

**Preregistered before any work:** `forks/g7_slowness/PREREG.md`
(commit `e01d8205`). Three crews, 10 forks, every one pure Zag, zero
randomness, every run reproduced byte-for-byte, every fork prereg
frozen before its implementation was built.

## The headline

**Free lunch is real.** The new variant (FL2: provisional install +
eliminative revocation) learns at deliberate teaching's speed and cost
**and** survives a lying teacher — the thing that used to be guided
learning's expensive exclusive. The old scaffold (38 episodes, 392
audit entries) is now strictly dominated and should be retired in
favor of FL2 (15 episodes, ~270 entries). Details below; nothing here
is defended, it was all tested against teaching head-to-head.

## Why it was slower — the measured breakdown

The old guided-learning arm (B) vs deliberate teaching (A) on the
collision task: **24 episodes slower** (release at E38 vs install at
E14) and **125 more audit entries** (392 vs 267 — the trial report's
"193" for A was a prose error; the recount from fresh builds is 267).

Where the 24 episodes went:

| chunk | episodes | verdict |
|---|---|---|
| E15–28: waiting for the world to contradict the REKEY shortcut | 14 | **INHERENT** — given the evidence schedule |
| E30–37: the 8-episode "verification streak" before disconnect | 8 | **REMOVABLE** — dropping it changes nothing |
| E11–14: probing vs teaching's calibration | 0 | wash — both arms spend it |

Where the 125 extra audit entries went:

| chunk | entries | verdict |
|---|---|---|
| one SCAFFOLD heartbeat entry per episode, 128 total | 128 | **REMOVABLE** — pure overhead |
| everything else (eliminate/commit/disconnect entries, fewer calibrations, etc.) | −3 | nets out |

The "2× audit cost" was essentially **one thing**: a heartbeat entry
logged every episode whether anything happened or not. Removing it
(P2) gives 267 entries — exactly tying teaching — with byte-identical
behavior and an exact ledger replay. Removing the streak too (P3):
release at E30, 267 entries, same behavior as the old scaffold.

**The wait is real but it isn't fixed.** Moving the world's
contradicting evidence earlier (D1b: audit at E15–24 instead of
E29–48) made the 14-episode blind wait vanish — B committed at E15.
The wait is set by the *evidence schedule*, not the machinery. You
can't eliminate a shortcut before the world contradicts it; that's the
entire price of "never trust a statement."

## Is it worth it — priced per property

- **Disconnect-verification** (learned = still there after the teacher
  channel dies): costs **exactly 1 audit entry** (FL1: 268 vs 267).
  It was never the expensive part.
- **Lie-resistance** (survives a teacher that teaches the wrong rule):
  costs **~2 more entries** (FL2: 269 honest / 271 lying vs 267) plus
  the evidence-schedule wait above. On the old scaffold this property
  cost 24 episodes and 125 entries; on FL2 it costs almost nothing.
- **The heartbeat**: 128 entries, buys nothing. Not worth it. Gone.

## The free lunch: FL2

How it works, in one paragraph: the learner installs the taught rule
**provisionally** at E14 (same gate as teaching), disconnects from the
teacher at E15, then keeps checking the installed rule against its
**own observation of the world** every episode — simulating the
alternatives on scratch copies, never trusting the teacher's word
again. If the world contradicts the installed rule, the learner
**revokes it itself** and commits whatever survived. No scaffold
channel, no heartbeat, no waiting on a schedule someone designed.

The numbers (all vs an in-binary teaching baseline, 267 entries):

| | honest teacher | lying teacher |
|---|---|---|
| acquire / release | E14 / E15 | E14 / E15 |
| audit entries | 269 (+0.7%) | 271 (+1.5%) |
| lie installed? | n/a | yes — provisionally, then **revoked at E29**, true behavior committed |
| persistence | 24/24 | 24/24, zero lie-actions after revoke |

Proven three ways: built twice by two independent crews (78/78 checks,
byte-identical evidence), the early-evidence rematch (same profile),
and a **fresh task** with a different shortcut and a different audit
(quarantine-and-hold vs a BYPASS cheat: 99/99 checks, 269/271 entries,
lie revoked at E29). Not a one-task artifact.

The predicted failure also held: FL4 ("commit as soon as simulation
says the candidate understands the rule") committed the lie at E11 —
because "understands" meant "understands what the teacher *said*," the
same hole teaching has. **The wait isn't a commit-logic bug; it's the
price of catching liars.** FL2 doesn't remove the wait — it makes
everything around the wait free.

One honest wart: on the lying stream FL2 **acts the lie for 14
episodes** (E15–28) before the world's evidence arrives to kill it —
same exposure the old scaffold had while probing, but now under a
provisional install. The evidence schedule sets that window (on the
early-evidence stream it shrinks to ~1 episode). Revocation is real,
not instant.

## What this means

1. **Retire the old scaffold arm** (E38/392). FL2 dominates it on
   every axis: faster, cheaper, and equally lie-resistant.
2. **Default to FL2** (pending your word): teaching's speed and cost
   with guided learning's lie-resistance. The G3 boundary ("teaching
   for trusted teachers, scaffold for untrusted ones") collapses —
   FL2 covers both.
3. **Kill the per-episode heartbeat** everywhere: it's pure cost, no
   load-bearing function (replay stays exact without it).
4. The remaining open cost is the **evidence schedule itself** — how
   fast the world contradicts a bad rule. That's the next thing to
   attack, and it's an environment question, not a learner question.

## Honest caveats

- One lie design per task (REKEY-as-correct; BYPASS-as-correct), one
  behavior family (deliberate memory ops), candidate policies given
  not generated, experimenter-designed worlds throughout.
- FL2's revocation window equals the world's silence: 14 episodes on
  D1's schedule. Against a lie the world *never* contradicts, FL2
  keeps the lie — same as the old scaffold, honestly priced now.
- Wall-clock was VM-noisy and tiny (0.055s vs 0.133s medians);
  episodes and audit entries are the real cost currencies.

## Commits (tnn-native-lab)

- G7 prereg (frozen): `e01d8205cc1c78dad22ed8dc536a4a35dd624b24`
- Profiler (P0 baseline + P1/P2/P3): `dfdb7556`, `bbe223d3`,
  `9fbce30e`, `81dcdaa0`, `0948b9c7`, `eac04bd1`, `8b82006b`
- Free lunch (preregs + FL1/FL2/FL4 + synthesis): `5bd04048`,
  `77c41dbf`, `5a73f9b4`, `1bd3c1d0`, `2e73ba12`
- Rematch (R1/R2/R3 + synthesis): `32881275`, `8783f5af`,
  `98d52433`
