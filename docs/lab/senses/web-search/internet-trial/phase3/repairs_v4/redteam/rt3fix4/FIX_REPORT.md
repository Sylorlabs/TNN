# HELL-HOLE V4 — Fix Round 4 Report (2026-09-24)

## Repaired source identity
- Workdir: `/home/hatch/workspace/scratch-hellhole/redteam/rt3fix4/`
- Source: `g_intent6_v4fix4.zag`
- Baseline source SHA256 (fix3): `4157f1224b9a88310b902196caa880d0889c2a44c8b070c346274ac8fb398b4c`
- Repaired source SHA256: `1a1b787071fc99a8db8740ca56fbc7a3b9c154486a0f9dacb8ebf6b7bea8d890`
- Binary: `run4_fix1` (pinned toolchain `znc_linux_x86_64_abed8aa1`)
- Pure Zag, zero RNG, no commit. All outputs byte-identical across 3 runs.

## RT3d before / after
| metric | baseline (fix3) | repaired (fix4) |
|---|---|---|
| deadpan installs | 52 | **3** |
| joke misses | 20 (17 mechanism + 3 ceiling) | **3** (all ceiling) |

49 of 52 deadpan installs were genuine rule overfires, fixed. The 3 joke
misses are the documented comprehension ceiling (unchanged).

## Per-item classification of remaining RT3d installs
1. **D16** `I never repeat my mistakes; I thought I made one once, but I was wrong.` → N_NEG.
   **Adversarial boundary.** The attacker derived this from the repair
   specification and mislabeled a famous joke NONJOKE. The classifier's
   carried-path valence read is defensible; not chased by design.
2. **D24** `To save money, substitute shampoo with dish soap.` → P_DA4S.
   **Shape boundary.** A text-initial purpose infinitive is lexically
   indistinguishable from the joke's purpose clause. Documented, not chased.
3. **D35** `He smoked two packs a day and lived to ninety; imagine that.` → R_IRONY.
   **Comprehension ceiling.** Requires multi-premise pragmatic reasoning
   (smoking→death expectation vs lived-to-ninety). Documented ceiling.

## Per-item classification of remaining RT3d joke misses
- **J38** ladder/high-school, **J39** password123, **J40** time-flies/fruit-flies.
  All three are the documented comprehension ceiling (garden-path syntax,
  meta-humor, lexical double-meaning requiring world knowledge). Unchanged
  from baseline; no mechanism fix available in a lexical classifier.

## Repairs made (round 4)
- **N_NEG**: added direct-object-aware `j_valence_clash` (positive verb on a
  negative noun with no negation pivot); expanded antonym/aux/prefix
  machinery; blocked purpose-infinitive "to <verb>" between verb and noun;
  added sincere status-report vetoes; removed generic laughed/joke triggers.
- **N_PUN family**: wired the five previously-dead detectors
  (`j_pun_grow/over/jump/line/comeout` → N_PUN_GROW/OVER/JUMP/LINE/OUT) with
  real semantic-class primers; execution-verified (J03–J07, E06/E09/E12/E14,
  C13). N_PUN: retired `running/catch`; weather-veto on `stop/stopped`;
  imperative-frame veto on `iron/wrinkles`.
- **N_VALENCE** (new, contra 56): standalone valence clash
  (`I adore my migraines`) — fires exactly once across all corpora (J15).
- **N_BAR**: tense needs past/present/future anchor (any position); long-face
  needs horse/photon; limp forms added.
- **N_QA**: single punch words must be answer-final; added "guess why"/"know why".
- **N_COMPLY**: absurd entity must occur in an `as X` role frame; added `advised`.
- **N_DEFLATE**: local-man/local-woman news-parody subjects only.
- **N_TAG**: contextual gates for tomorrow/not-so-sure/not-get-it/no-idea;
  whisper path only `too crowded`.
- **N_PAYOFF**: explicit simile frames only (`is/was like`, `like a/the`).
- **R_SATIRE**: cheese-festival overfire fixed — `j_satire_absurd` no longer
  fires on bare absurd entities (explicit satire markers only).
- **R_TROPE**: `literally`/`a million`/`to death` need an absurd entity.
- **P_DA/P_DB**: emergency-response veto wrapping rules 1–36; negated-act,
  prescribed-ingestion, mock-benefit, microwave-collocation, drop-target,
  rescue/craft-context, breathing-modifier, concurrent-wearing,
  substitution-target, myth-attribution gates; `j_purpose_to` now sees
  text-initial infinitives.
- **j_grave_ctx**: grave/institutional context veto for the over/jump idiom
  puns; hyphenated nominalization (`jumping-to-conclusions problem`) exempt.
- **NEG deny/question guards**: determiner-led referential NPs exempt from
  prefix echoes; `uncertainty` added to F_ABSTRACT; `cardboard box` absurd.
- Scorer fixed: skips non-label header rows; oracle read from last column.

## Regression batteries (all with repaired binary)
| battery | result | 3× SHA256 |
|---|---|---|
| RT3d (95) | 3 installs (classified above), 3 ceiling misses | `ee34de4b…792264` |
| RT3c (76) | 0 installs, 20 ceiling misses (unchanged) | `eebc17bf…79de0f4` |
| RT3b (73) | 0 / 0 (2 mid-fix regressions fixed) | `e71e7c8a…c969110` |
| RT3 (75) | 0 / 0 (1 mid-fix regression fixed) | `456c531b…6cbb4033` |
| Frozen30 (30) | 30/30, byte-identical to fix3 final | `e7107e22…6f6e919` |
| Round-3 guards (14) | 14/14 UNCERTAIN | `a1382288…bd2963a8b` |
| neg_r4 (30, NEW original sincere negatives) | 30/30 UNCERTAIN, 0 installs | `e8df84ef…0cb7fda9` |

Full SHAs:
- rt3d: `ee34de4bab5a6380ca48a6bf54815e0df4c550fdb3c961ae6312051671792264`
- rt3c: `eebc17bf865aaa972fca6ba19a5dc24849c07c685e28b351d834d0de579de0f4`
- rt3b: `e71e7c8a3ae9367a74152595406aa58f4eacbabc9169ffa3ff5759440c969110`
- rt3: `456c531b8bc99311d9fe85c7d3dbbf7a647428ff1c800b076ba1f6cbb4033bce`
- frozen30: `e7107e22e3825799efcfa6eb32dd222b5c5c8a1e8dd116aaf84468d616f6e919`
- negr3: `a138228856e550abb6e01f726da8f3d57a68a3bc56b1b35eb8a745bd2963a8b3`
- negr4: `e8df84efeb5e035d0c36c52300a37a5b219ca7d08291af34852b0cb7fda94087`

## Frozen status
Frozen30 output is byte-identical to the fix3 canonical output
(SHA `e7107e22…6f6e919` matches the recorded fix3 SHA). No frozen regression.

## Notes
- Two mid-fix regressions (RT3b D16/D17 via new pun detectors; RT3 C05 via
  tense-anchor position; RT3 E06 via grave-ctx overbreadth) were caught by the
  batteries and repaired with principled gates before final runs.
- `neg_r4.tsv` is 30 original natural-sincere sentences (not from any attack),
  added as a permanent negative corpus.
- Not committed, per instructions.
