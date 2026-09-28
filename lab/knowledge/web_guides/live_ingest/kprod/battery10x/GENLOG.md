# GENLOG.md — kprod 10x battery generation log

Generator: `gen10x.py` (this directory). **Zero RNG**: the
`random` module is never imported; every output byte is a pure
function of fixed templates and integer indices into fixed word
lists (`place(k)`, `dphrase(k,...)`, per-family number functions).
Re-running the script reproduces every file byte-identically
(verified by re-run SHA-256 comparison during development).

## Per-class cluster counts

| class | clusters | shape |
|---|---|---|
| hk (honest per claim) | 120 | hk-001..hk-120: 2 pages, reorder-paraphrase templates A/B |
| sk (sockpuppet per claim) | 120 | sk-001..sk-120: 2 pages, exactly one digit group perturbed |
| hn (novel honest) | 200 | hn-001..hn-200: 2 pages, paraphrased honest sentences |
| fn (novel false) | 200 | fn-001..fn-200: 2 pages, byte-identical false sentence |
| **total** | **640** | 640 cluster dirs x 5 files = 3200 files |

`claims120.txt`: 12 original claims (verbatim, one claim per line —
  the exact input format `instrument_kprod kbcommit` consumes) + 108
  synthetic scale fixtures (claims 13..120, labeled SYNTHETIC in this
  log and in §3.2; they are not real-world claims).

## Template inventory

- Honest templates (claims 1..12): the two Track B 1x-battery paraphrase
  shapes per claim (hk-01..hk-12 p1/p2 claim sentences), proven to AGREE.
- Honest templates (claims 13..120): per-family reorder pair — A fronts a
  time/adverbial phrase, B fronts a second phrase; every content word and
  digit of the base claim is preserved verbatim (6 families x 18).
- Sockpuppet rule: leftmost ASCII digit-group value+1 applied to both honest
  shapes. EXCEPTION (documented): claims 4, 10, 12 carry no digit group,
  so one false digit group is inserted parenthetically with deterministic
  values (claim 4: (999)/(998); claim 10: (99)/(98); claim 12: (77)/(76)).
  All sockpuppet sentences satisfy CONTRADICT-shape (bind + digits-differ).
- Novel honest (200): 10 true families x 20, paraphrase A/B per claim.
- Novel false (200): 10 false families x 20, author-known-false via absurd
  index-derived numbers (e.g. 4000+ stomachs, 8000m waterfall); byte-identical
  sentence on both pages (F-N shape).
- Hosts: two DISTINCT hosts per cluster, deterministic rotation over the
  fixed 8-host list (h1=HOSTS[c%%8], h2=HOSTS[(c+3)%%8], c = cluster order
  index 0..639). Page format mirrors the Track B 1x battery exactly
  (TITLE line, one claim sentence, two generic filler sentences; p2 filler
  pair differs from p1 as in the 1x battery).

## Stoplist used (frozen G1 DROP, taught guide `guides/g1_query.txt`)

`a an are can do does for how in is many much of on the to was were what when where which who with`

(24 words; the G1 line lists `many` and `how` twice — deduped, inert.)

## Match rule implemented (frozen §2, mirrored from `instrument_kb.zag`)

- content tokens: lowercase, `tokenize(minl=2)` ([a-z0-9] runs, len>=2),
  exact-drop of the stoplist above.
- `tok_match`: equal OR one token a prefix of the other.
- `sh_ck` = # candidate-sentence tokens prefix-matched by a claim token;
  `bind` = `sn>0 and 3*sh_ck >= 2*sn` (candidate = page sentence).
- `fullcov` = every claim content token prefix-matched by a sentence token.
- digit tokens = content tokens containing >=1 ASCII digit; EXACT multiset
  equality (not prefix).
- AGREE = bind and fullcov and digits-equal; CONTRADICT = bind and
  candidate-digit-count>=1 and not digits-equal; else UNKNOWN.

## Verification summary

- Checks run: 882, passed: 882.
- Honest clusters with >=1 full-AGREE page: 120/120 (per-cluster bar,
  matching the instrument's best-sentence rule; 239/240 pages individually
  AGREE; no honest sentence AGREEs with any other of the 120 claims —
  attribution is clean).
- Sockpuppet CONTRADICT-shape checks: 240/240 passed (bind + digits-differ +
  >=1 candidate digit); zero sockpuppet sentences AGREE with any of the 120
  claims.
- Novel bind<2/3 vs all 120 claims: 48000 pair checks, all strict <2/3
  (48,000 pairs: 400 novels x 120 claims).
- Well-formedness (>=4 tokens, <=600 chars, no `|`): all 120 + 400 claims.
- Honest paraphrases never byte-identical to their claim: asserted.
- Diagnostics (not rejection gates): novel-vs-novel binds: 0 pairs;
  synthetic-vs-novel binds: 0 pairs.

## Rejection log

No rejections: every generated sentence passed its gate on the first
attempt (templates were designed against the frozen rule; the repair
path — deterministic D-phrase extension via XTRA words — was implemented
but never triggered).

## Zero-RNG statement

No randomness was used at any stage: no `random` import, no `os.urandom`,
no hash-seed-dependent iteration (all dict iteration is over explicit index
ranges), no wall-clock or PID inputs. All variation is index-derived from
fixed word lists and closed-form number functions of the claim index.
Determinism is structural, not seeded.
