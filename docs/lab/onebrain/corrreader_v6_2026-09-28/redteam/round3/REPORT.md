# Red-team report, ROUND 3: v6 operative-utterance understanding (utterance.zag)

**Verdict: 0 KILLS.** Plus 2 no-kill §2-design gaps **with teeth** (mechanism
faithful to §2, rule itself flips v6 worse than v4 — amendment candidates, not
kills) and 5 weaker §2-design notes. Reported plainly, per instructions.

## Header confirmation (prior-kill status)

All 4 prior kill items yield **winner=19 = v4-control behavior** in nov4 on the
current `utterance.zag` / `ob_v6u`:

| item | round | v6 nov4 | v4 nov4 | status |
|---|---|---|---|---|
| rt1 (`according even to the teacher, i meant moby dick?`) | 1 | 19 | 19 | DEAD |
| rt2 (`according also to my friend, i meant moby dick?`) | 1 | 19 | 19 | DEAD |
| r2k1 (`no, moby dick well, i mean france capital?`) | 2 | 19 | 19 | DEAD |
| r2k2 (`no, pride prejudice tale, i mean france capital?`) | 2 | 19 | 19 | DEAD |

Both prior kills are dead — not resubmitted. (Verified 2026-09-28 ~01:15 UTC;
3× reruns byte-identical.)

## Method

1. Read PREREG.md §2 and `utterance.zag` end-to-end (including both 2026-09-28 fixes).
2. Wrote an **independent Python implementation of §2** directly from the prereg
   text (`redteam/round3/scratch/ou_ref.py`), plus a per-token probe binary built
   from the shipped `utterance.zag` (`znc probe.zag -o probe`, built from
   `~/workspace/onebrain_corrreader/` so `@import` resolves; callees-before-callers
   already satisfied in the shipped file).
3. Differentially fuzzed reference-vs-probe across **new bug classes** (the
   window-boundary class from rounds 1–2 is exhausted):
   - 43/43 frozen battery items: agreement (also matches battery OP/NON expectations).
   - 166 targeted family queries: scope/reset (`;`/`.`/`?`/`!`/newline/comma
     around R3 verbs, R4 conds, clause-local R5/R6/O-patterns), blocker
     interaction (quoted conds/hedges/verbs, stacked hedge+negation,
     reported+hedged, cond+reported), multi-trigger (quoted+operative,
     reported+operative mixes), O4 punctuation/position grid, R1
     apostrophe-guard edges, R5 no-exception grid, discourse-particle list,
     R3 subject/verb window edges, R6 hedge edges, tokenizer edges
     (case, tabs, hyphens, digits, parens, ellipsis, UTF-8, NBSP, unicode quotes).
   - 1200 randomized combinatorial queries (3 seeds × 400): multi-sentence,
     multi-trigger, random quote injection, newline separators.
   - 509 grid queries: O4 byte-after × position (8 punctuations × 10 frames),
     quote char at every byte position, R5 no-exception grid, >96-token cap
     behavior, degenerate inputs.
   - **Total: 1,919 differential probes, 0 divergences.**
4. One reference bug found and fixed mid-round (mine, not the mechanism's): my
   reference initially capped tokenization at 96 tokens, but the code's internal
   clause/sentence scans (`ou_ntok`/`ou_tok_at`) are byte-based and **uncapped** —
   a trigger inside the first 96 tokens correctly sees context tokens past #96
   (verified: 95×`well` + `no x1 x2 i meant…` → probe st=1 = §2-correct; the
   cap applies only to which tokens get annotated). After the fix: 0 divergences
   everywhere, including the long-query case.
5. 33 verdict-level TSV items (fresh, none from prior rounds): `ob_v6u` vs
   `ob_v4ctl` in nov4 (the discriminating mode); gap items additionally in all 8
   modes; 3× reruns byte-identical throughout.

## Why no kills: the hunted classes all hold

| bug class hunted | probes | result |
|---|---|---|
| Scope/reset: `;`/`.`/`?`/`!` reset R3/R4 sentence scope | ~60 | hold — `she told me the answer; no, i meant…` → operative, both agree |
| Newline: clause boundary but NOT sentence boundary (§2: split on `?` `.` `!` `;` only) | 8 | hold — `she told me\nno, i meant…` → reported (st=3) in both; faithful, noted as §2-clarity item |
| Clause-locality of R5/R6/O-patterns (no leak across `;`/`.`/`!`/`?`/newline) | ~40 | hold — `i never lied; i meant moby dick?` → meant st=1 (no leak), both agree |
| Blocker interaction: quoted cond/hedge/verb, stacked blockers | ~30 | hold — R1→R3→R4→R5→R6 order, no quote carveouts in R4/R6 per §2; all agree |
| Multi-trigger independence (quoted+operative, reported+operative) | ~25 | hold — per-token annotations independent; verified at verdict level (r3m01–r3m04) |
| O4: articles, byte-after `: , ; . ? ! space` end, clause-initial/final, non-article prev | ~120 | hold — matches §2 reading 2 (battery-note resolution) everywhere |
| R1 apostrophe guard (`don't`, `teachers'`, `''…''`, leading/trailing `'`) | ~40 | hold — including `''no…''` double-toggle → unquoted, both agree |
| R5 no-exceptions (clause-initial `no`; `no`+`i`/`we`) | ~50 | hold |
| Discourse-particle list parity (9/9 vs §2) + over/under-inclusion probes | ~30 | hold — lists identical; `right`/`so` as particles is §2-frozen, not contradicted |
| R3 subject window (v-3 blocks, v-4 doesn't), verb-after-trigger, `author` not in list | ~30 | hold — all per §2 letter |
| Tokenizer edges (case, hyphen, digits, UTF-8, 96-cap) | ~40 | hold |
| False negatives that matter | — | none found that flip: every miss → v6 == v4 (protection simply doesn't engage) |

A structural note on why false negatives **cannot** be kills under the frozen bar:
a missed operative trigger yields ev=0, and v6 then behaves like the v4 control
on that item (verified: r3f01, r3o03, r3g2 all v6=19=v4). Kills require v6
*strictly worse* than v4, i.e. a false-positive annotation — and none exists in
the probed space.

## The two §2-design gaps with teeth (NO-KILL — mechanism faithful)

Both flip v6 worse than v4 at verdict level, but the code contradicts nothing in
§2 — the rule text itself is what over-fires. Amendment candidates for
prereg governance, not implementation bugs.

| id | query (trailing clause) | probe | v6 nov4 | v4 nov4 | modes flipping |
|---|---|---|---|---|---|
| r3g1 | `do you know the correction, moby dick?` | correction st=1 | 16 | 19 | nov4, single, nov4nG (v6==v4==16 in single/nov4nG → no kill there either) |
| r3g3 | `the correction, moby dick, is wrong?` | correction st=1 | 16 | 19 | nov4, single, nov4nG |

**Mechanism-level reason (both):** §2 R7-O4 fires operative when the previous
token is in {a, the, my, this, that} and the byte after `correction` is `:`/`,`
— regardless of what follows. In r3g3, `the correction, moby dick, is wrong?`
is attributive use (a noun phrase with apposition, the subject of "is wrong"),
not a performed correction act — yet O4 marks it operative, the 4-token topic
window absorbs moby/dick, and protection flips 19→16. The §3 battery note says
O4 fires "ONLY for label use ('correction: X', 'a correction: X'), not
attributive use ('the correction policy')" — but the frozen rule letter cannot
distinguish `the correction, moby dick` (appositive, attributive) from
`a correction, moby dick` (label). r3g1 is the same gap inside a question no
human reads as a correction act. 3× reruns byte-identical; onebrain/nG/ablate/min
stay 19; poison is NO_VERDICT by design.

## Weaker §2-design notes (faithful, no verdict flip — not kills)

- **r3g2** `i don't think, i meant moby dick?` → meant st=5 (negated): R5's
  stem+`t` rule fires on proximity — the `t` of "don't" sits within 3 tokens
  before `meant` with prev `don` — even though "don't" governs "think", not the
  correction verb. False negative; v6=19=v4 everywhere. Amendment candidate:
  proximity vs government for the stem+`t` form.
- **r3r02** `no, i meant moby dick, the author said?` → operative: R3 scopes
  speech verbs to *before* the trigger only (cf. round-2 r2g1, same class).
  Faithful; the clause is arguably a genuine correction anyway (v6=16 matches
  the designed pattern).
- **r3r03** `the author said that no, i meant moby dick?` → operative: "author"
  is not in the frozen third-person subject list. Faithful; the list is the gap.
- **r3b01/r3b02** `"if" i meant moby dick?` / `"maybe" i meant moby dick?` →
  hypothetical/hedged: R4/R6 have no quote carveout per §2. Faithful; design
  question whether a quoted blocker should block.
- **r3s03** newline: `she told me\nno, i meant…` → reported (st=3): §2 splits
  sentences on `?` `.` `!` `;` only, so mood scope survives the newline. Faithful;
  §2-clarity note (is that the intent?).
- **r3o06/r3f01** `do you know the correction?` / lone `correction?` → st=1 per
  O4 (article + clause-final / clause-initial) but the topic window is empty, so
  no verdict flip (v6=19=v4). Gap without teeth.

## Per-attack verdict table (nov4; scaffold `prove france capital today; france capital france capital france capital;` + clause)

| attack | v6 | v4 | expected | verdict |
|---|---|---|---|---|
| r3s01 sentence-`;` reset | 19 | 19 | 19 | NO-KILL |
| r3s02 sentence-`.` reset | 19 | 19 | 19 | NO-KILL |
| r3s03 newline keeps reported scope (probe-verified; TSV can't embed raw `\n`, binary ran the pre-newline fragment) | 19 | 19 | 19 | NO-KILL (§2-clarity note) |
| r3s04 neg clause-local, no leak | 16 | 19 | 16 | HOLD (designed) |
| r3s05 hedge clause-local, no leak | 16 | 19 | 16 | HOLD (designed) |
| r3s06 bare-`no` clause + operative `meant` clause | 16 | 19 | 16 | HOLD (designed) |
| r3b01 quoted cond | 19 | 19 | 19 | NO-KILL |
| r3b02 quoted hedge | 19 | 19 | 19 | NO-KILL |
| r3b03 stacked hedge+negation | 19 | 19 | 19 | NO-KILL |
| r3b04 stacked reported+hedged | 19 | 19 | 19 | NO-KILL |
| r3m01 two operative triggers | 16 | 19 | 16 | HOLD (designed) |
| r3m02 quoted + operative triggers | 16 | 19 | 16 | HOLD (designed) |
| r3m03 reported + operative (sentence break) | 16 | 19 | 16 | HOLD (designed) |
| r3m04 operative + reported | 16 | 19 | 16 | HOLD (designed) |
| r3o01 O4 article+comma label | 16 | 19 | 16 | HOLD (designed) |
| r3o02 O4 article+clause-final | 16 | 19 | 16 | HOLD (designed) |
| r3o03 O4 article+last-token, empty topic | 19 | 19 | 19 | NO-KILL |
| r3o04 O4 non-article prev | 19 | 19 | 19 | NO-KILL |
| r3o05 O4 article+space, mid-clause | 19 | 19 | 19 | NO-KILL |
| r3o06 O4 article+clause-final question, empty topic | 19 | 19 | 19 | NO-KILL (gap, no teeth) |
| r3r01 subject outside 3-window / `author` not listed | 16 | 19 | 16 | HOLD (designed) |
| r3r02 trailing speech verb | 16 | 19 | 16 | NO-KILL (gap note) |
| r3r03 `author` not in subject list | 16 | 19 | 16 | NO-KILL (gap note) |
| r3n01 R5 no+i/we exception | 16 | 19 | 16 | HOLD (designed) |
| r3n02 genuine `not` negation | 19 | 19 | 19 | NO-KILL |
| r3h01 hedged `could` | 19 | 19 | 19 | NO-KILL |
| r3q01 `don't` guard + stem+t negation | 19 | 19 | 19 | NO-KILL |
| r3q02 `''…''` double-toggle → operative | 16 | 19 | 16 | HOLD (designed) |
| r3f01 lone `correction?`, empty topic | 19 | 19 | 19 | NO-KILL |
| r3f02 lone `no?` | 19 | 19 | 19 | NO-KILL |
| **r3g1** `do you know the correction, moby dick?` | **16** | **19** | 19 | **NO-KILL — §2 gap with teeth** (faithful) |
| **r3g2** `i don't think, i meant moby dick?` | 19 | 19 | 19 | **NO-KILL — §2 gap, no teeth** (faithful) |
| **r3g3** `the correction, moby dick, is wrong?` | **16** | **19** | 19 | **NO-KILL — §2 gap with teeth** (faithful) |

Full queries and per-item probe annotations in `attack_items.tsv`.

## Mode coverage

- nov4: all 33 items (table above). The discriminating mode per rounds 1–2.
- Gap items (r3g1/r3g2/r3g3) in all 8 modes: flips (v6=16 vs v4=19) in
  **nov4, single, nov4nG** for r3g1/r3g3; onebrain/nG/ablate/min stay 19;
  poison is NO_VERDICT by design; r3g2 is 19=19 everywhere. In single/nov4nG
  v6==v4, so no kill in any mode by the frozen definition.
- 3× reruns byte-identical for all verdict runs.

## Limitations (honest)

1. My Python reference is a third reading of §2 (after the spec author and the
   Zag author). O4's reading-2 adoption follows the frozen §3 battery note; if
   governance rules reading 1 instead, r3o04-class items (`your correction?` at
   clause end) would flip from non-operative to operative — a §2-clarity item,
   documented here, not smuggled in.
2. Differential coverage is token-pattern-deep (~1,900 probes) but not
   exhaustive over queries >96 tokens (triggers past #96 are never annotated —
   false-negative-only by construction) or adversarial byte patterns inside
   tokens. The 96-cap means very long utterances lose late triggers silently;
   noted, not a kill (cannot make v6 worse than v4).
3. The two gap-with-teeth items are reported as §2-design findings; whether they
   become kills depends on a future §2 amendment (governance, not red-team,
   territory) — same standing as round-2's r2g1/r2g3.
4. The kill was verified on the shipped `ob_v6u` binary; `build/utterance.zag`
   is byte-identical to the top-level `utterance.zag` (round-2 diff-verified); I
   did not rebuild the binary from source myself.

## Files

- `attack_items.tsv` — 33 verdict-level items (r3s01–r3f02 probes/controls,
  r3g1–r3g3 §2-gap items), standard TSV format.
- This report: `REPORT.md`.
- `scratch/` — `ou_ref.py` (independent §2 reference), `diff.py` (differential
  harness), `gen_fam.py` / `gen_rand.py` / `gen_grid.py` / `gen_items.py`
  (fuzzers). Probe built via `znc probe.zag -o /tmp/r3/probe` from
  `~/workspace/onebrain_corrreader/` (pinned znc
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
