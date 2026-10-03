# PREREG_C15BOUND.md: bounded C15 abstention measurement (candidate d)

Wave: wave-20261002-1121pdt | Lane: ARENA | Date: 2026-10-02
Status: FROZEN. No extended battery exists at freeze time. This file is
committed alone before bare_battery.zag is written.

## Purpose

Continue the C15 abstention work by quantifying DEFRECALL's abstention
boundary on an extended bare-prompt battery. No mechanism change: the
frozen lane rule stands (genuine prompt-intent discrimination is a new
11-step frontier proposal, not a patch). This freezes the BOUNDED claim
so the C15 number can be reported honestly.

## Bounded claim (frozen)

DEFRECALL abstains (replies exactly UNKNOWN) exactly on:
 (i) parameterized prompts (e.g. `invent|notation`), and
 (ii) bare prompts with an empty roster.
On any bare prompt with a non-empty roster it enumerates the roster,
whether or not the prompt is a roster request. The C15 score is
therefore conditional on prompt intent, not a general abstention
capability.

## Method

- bare_battery.zag (pure Zag, safebin): generates a battery with
  1 brief turn, 9 expo fact events (entities Alpha..Iota, same as the
  frozen multibare battery), then bare test turns, then done.
  Bare prompts (frozen list, 12):
    roster requests (4): `listnames`, `names`, `whoarethey`, `roster`
    non-roster bare (8): `whattime`, `invent`, `recall`, `who`,
      `summarize`, `countthem`, `help`, `define`
  Expected answers: roster CSV for the 4 roster requests; UNKNOWN for
  the 8 non-roster prompts. Battery hash recorded before runs.
- Contestant: defrecall_contestant.zag source via `git show` from
  commit 2320c3454 (the ABSTENTION_TEST lineage), built with pinned
  znc; binary sha256 must match 3d629deda888c18d19ff95ce9819829f2c268cf8e459330b7c573c3892cd57d7
  (the sealed binary). Zero source changes.
- 3 runs, fresh state each; stripped reply streams hashed.

## Frozen bars

- B1 (determinism): 3/3 stripped reply streams byte-identical.
- B2 (instrument): battery sha256 recorded pre-run; turn count fixed.
- B3 (purity): pure Zag, safebin, no contestant changes.
- B4 (honest report): abstain rate on the 8 non-roster bare prompts and
  roster accuracy on the 4 roster requests, reported separately. The
  bounded claim is CONFIRMED if abstain rate = 0/8 and roster accuracy
  = 4/4; any deviation is reported as found.

Prediction (not a bar): abstain rate 0/8, roster accuracy 4/4,
confirming the structural (bare vs parameterized) boundary measured in
ABSTENTION_TEST.
