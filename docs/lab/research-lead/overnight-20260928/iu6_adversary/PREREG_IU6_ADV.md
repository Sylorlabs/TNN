# PREREG: H-INTENT-UNIFIED6 Red Team (FROZEN)

## Target

H-INTENT-UNIFIED6 SURVIVES (7/7). R8: all-pairs both-truncated guard.
For each unordered pair (a,b) with em=0 on both and both records
truncated (npairs>16), kind-dispatched answers computed over qlen bytes;
any disagreement emits `INTENT TRUNCATED-CONFLICT-POSSIBLE: truncated
candidates disagree beyond top two; WITHHOLD AMBIGUOUS` and returns
kind=-2. Precedence: verbatim guard first, top-two guards second,
all-pairs third, gap tie last.

Frozen claim under test: "The both-truncated guard now covers genuine
contradictions among ALL truncated candidates with em=0, regardless of
rank. The X-IU5-1 hazard class (silent resolution via ranking) is
closed at the mechanism level."

## Frozen attacks

### X-IU6-1: Fourth-anchor both-truncated dissenter

Four truncated (true npairs=17, em=0) candidates on query `xab`:
- P_dissent: proc (reverse), 17 pairs, `xab>bax` 17th (unrecorded).
  Answer `bax`.
- P_agree: proc (emit-input[0]x3), 17 x-prefixed pairs, `xab>xxx`
  17th (unrecorded). Answer `xxx`.
- B1: bridge (x-rule), 17 pairs (3-char), `xab>xxx` 17th. Answer `xxx`.
  Score 30000.
- B2: bridge (x-rule), 17 pairs (16x4-char + `xab>xxx`), `xab>xxx`
  17th. Answer `xxx`. Score 20000.

Learn order (fresh W): P_dissent, P_agree, B1, B2.
Query: `xab` (qlen=3).

The dissenter (P_dissent, `bax`) is not in the top two (B1=30000,
B2=20000 outrank it). The top-two both-truncated guard compares B1 vs
B2: answers `xxx` vs `xxx` agree, falls through. R8 must catch a
disagreeing pair (e.g., B1 vs P_dissent).

PASS (attack FAILS, mechanism holds) iff: kind=-2 AND the diagnostic
contains `truncated candidates disagree beyond top two`.

SUCCEEDS (attack succeeds) iff: kind>=0 (decisive, silent resolution
of the genuine P_dissent/B1 contradiction), or kind=-2 without the
R8 diagnostic.

Genuineness: P_dissent's training contained `xab>bax` as pair 17;
B1's contained `xab>xxx` as pair 17; both unrecorded (em=0, npairs=17).
Direct application confirms `bax` vs `xxx`.

### X-IU6-2: Verbatim third-anchor (disclosed boundary probe)

Three candidates on query `xab`:
- V1: bridge (x-rule), 3 pairs (3-char) INCLUDING `xab>xxx` RECORDED.
  Verbatim (npairs=3 <= 16), em=1. Answer `xxx`. Score 70000
  (em=1, cf=1, lm=1).
- V2: bridge (x-rule), 6 pairs (5x4-char + `xab>xxx` RECORDED).
  Verbatim (npairs=6 <= 16), em=1. Answer `xxx`. Score 60000
  (em=1, cf=1, lm=0, tlen=-1 mixed).
- T3: proc (reverse), 17 pairs, `xab>bax` 17th (unrecorded).
  Truncated, em=0. Answer `bax`. Score 10000.

Learn order (fresh W): T3, V1, V2.
Query: `xab` (qlen=3).

Ranking: V1 (70000) > V2 (60000) > T3 (10000). gap=10000 > 0.

Guards:
- Verbatim guard: top=V1, second=V2, both em=1, answers `xxx` vs
  `xxx` agree -> no fire.
- Top-two truncated guard: em_top=1, em_second=1 -> no branch fires
  (verbatim-vs-truncated and both-truncated branches need em=0 on
  at least one side).
- R8: V1 (em=1) and V2 (em=1) are skipped; no em=0/em=0 pair exists
  (T3 is the only em=0 candidate) -> no fire.
- gap=10000 != 0 -> decisive.

Expected: kind=1 (bridge), answer `xxx`. The genuine T3/V1
contradiction (`xab>bax` in T3's unrecorded tail vs `xab>xxx` in V1's
recorded data) is silently resolved.

This is the DISCLOSED out-of-scope boundary ("The
verbatim-meets-truncated branches remain top-two-only; a third-anchor
verbatim-vs-truncated conflict is out of scope", IU6_RESULT.md).
SUCCEEDS here means the boundary is CONFIRMED (real and exploitable),
not that the verdict changes. Per the H-CAUSAL-UNIFIED4 precedent,
confirming a disclosed boundary does not change the verdict UNLESS it
falsifies the headline claim. The IU6 headline claims coverage for
"truncated candidates with em=0"; this attack uses a verbatim (em=1)
anchor and does not falsify it.

PASS (attack FAILS) iff: kind=-2 (mechanism withholds despite the
disclosed boundary).

SUCCEEDS (boundary CONFIRMED) iff: kind>=0 with answer `xxx` and no
TRUNCATED-CONFLICT diagnostic. Verdict: BOUNDARY CONFIRMED, no
downgrade (disclosed out-of-scope).

### X-IU6-3: Guard shadowing / precedence

Verify that the top-two guards and R8 do not shadow each other
incorrectly. Two sub-tests:

X-IU6-3a: On the K-IU6-1 fixture (X-IU5-1 third-anchor), where ONLY R8
can fire (top-two agree), the diagnostic must read EXACTLY
`INTENT TRUNCATED-CONFLICT-POSSIBLE: truncated candidates disagree
beyond top two; WITHHOLD AMBIGUOUS`.

X-IU6-3b: On the K-IU6-2a fixture (K-IU5-1a top-two both-truncated),
where the top-two guard fires, the diagnostic must read EXACTLY
`INTENT TRUNCATED-CONFLICT-POSSIBLE: both records truncated with
different answers; WITHHOLD AMBIGUOUS` (the UNCHANGED top-two text).
R8 must not shadow it with the "beyond top two" text.

PASS (no shadowing bug) iff: both diagnostics are exact.

SUCCEEDS (shadowing bug) iff: X-IU6-3a yields the top-two diagnostic
text, or X-IU6-3b yields the "beyond top two" text, or either yields
kind>=0.

### X-IU6-4: Regression (no silent changes)

Rebuild from committed sources (`git show HEAD:...`):
- `iu6_verify.zag` output md5 must equal `a4dad5090897bf0a82c5fddad3e45b57`
  (frozen IU6 hash), 3/3 byte-identical.
- `unified_learn.zag` main(): 20/20, md5 `904de9f83a2873c7a8862b71804a9065`
  (frozen IU4 hash).
- `intent_learn.zag` main(): 10/10, md5 `98315faec8faea24e75533892c0b240d`
  (frozen IU4 hash).

PASS (no regression) iff: all md5s match, 3/3 deterministic.

SUCCEEDS (regression) iff: any md5 differs or non-determinism.

## Verdict rule

- X-IU6-1 SUCCEEDS -> DOWNGRADED (falsifies "ALL truncated candidates
  with em=0, regardless of rank"). If the mechanism is fundamentally
  broken (e.g., R8 never fires), KILLED.
- X-IU6-2 SUCCEEDS -> BOUNDARY CONFIRMED, no verdict change (disclosed
  out-of-scope; does not falsify the both-truncated headline claim).
- X-IU6-3 SUCCEEDS -> DOWNGRADED (precedence bug).
- X-IU6-4 SUCCEEDS -> KILLED (frozen bars broken).
- All FAIL -> H-INTENT-UNIFIED6 SURVIVES this red team.

## Frozen methodology

1. This prereg committed alone before any attack code, build, or run.
   Commit order verified by `git merge-base --is-ancestor`.
2. Harness: `iu6_adversary/iu6_adv.zag` = mechanism region of the
   COMMITTED `unified_learn.zag` (lines 1-1471, everything before
   `fn main`), cmp-verified byte-identical against `git show HEAD:...`;
   only `main()` replaced with attack drivers. No mechanism edits.
3. Raw evidence: `IU6_ADV_RAW.txt` (md5 recorded, 3/3 byte-identical),
   exit 0.
4. Pure Zag throughout: prereg, harness, builds, runs, greps, md5,
   cmp. No Python at any stage.
5. Toolchain: znc 2026.07.0-dev (edition 2026), pinned.
6. Only adversary-owned paths staged: `iu6_adversary/`. No broad git
   add. No em dashes in loop documentation.
7. Binaries built in /tmp/iu6adv only, never committed.
