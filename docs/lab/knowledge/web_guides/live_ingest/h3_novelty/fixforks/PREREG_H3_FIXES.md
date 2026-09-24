# PREREG — H3 spec-break fix forks (WORKSTREAM C)

**Frozen:** 2026-09-23. No changes after this point without a dated amendment.
This prereg is committed BEFORE any fix-fork Zag line is written, any
adversarial fixture is authored, or any fix run executes. Ordering is
load-bearing: the fixture designs (§3) and fix approaches (§4) are frozen
before the first build; runs may not begin until the prereg commit lands.

## §1 Question and scope

H3 CONFIRMED: a pure-Zag detector distinguishes nothing-new vs
novel-installable vs novel-but-blocked vs genuine-failure-to-install (14/14
corpus verdicts correct, byte-identical reruns). Red-team RT2 then broke the
frozen spec on five corpora — five distinct equivalences byte-identity cannot
see (`VERDICT_RT2.md`): F1 translation-equivalents, F2 double-negation
restatements, F3 fact-splitting, F4b cross-corpus nonce-substitution
smuggling, F5 normalization-gap (zero-width characters).

This workstream builds, tests, and red-teams one pure-Zag fix fork per break.
Each fork is a spec **amendment candidate**: it extends the frozen H3 §2
matching rules in exactly one dimension. None amends frozen law by itself —
Micah's signature is required for any amendment to become law. Until then the
forks are experimental instruments, and any break a fork does not close
stays OPEN as a known boundary.

Non-goals (recorded, not evaded): the debate's O2 (paraphrase-flood
budgeted-attention), O3 (failure-cell fault injection), O7 (post-G4
deterministic consistency check) are separate preregistered experiments, not
fixes for these five breaks. The synthesis §5 amendment candidates
(K-construction freeze, `known=` convention, audit-schema O6) are
documentation freezes, not mechanism fixes. None is built here.

## §2 Common fork architecture (all five forks)

- **Base:** the frozen `novel.zag` mechanism (LESION=0), copied whole into
  each fork file. Forks are independent; no shared fix code.
- **Direction:** every fix ADDS ways to establish NON-NOVELTY (match K). No
  fix removes a frozen match, and no fix can cause an install or suppress a
  genuine candidate: equivalence stages run inside the K-matching path only
  (the debate's S3 firewall). A sentence the equivalence stage does not
  match proceeds exactly as the frozen instrument would classify it.
- **Audit:** each fix emits an `EQUIV=<kind>` flag on the `AUD|` line of
  every sentence it newly matches (`TRANSLATION`, `NEGATION`, `COMPOSED`,
  `NONCE_TEMPLATE`; F5 needs no flag — the amended norm is the match path).
  The `REPORT|` line format is frozen and unchanged.
- **Determinism:** zero RNG in every decision path (K-RNG); two full passes
  byte-identical (K-DET).
- **Inputs:** forks F1–F4 take the frozen three args
  (`<kfile> <corpusfile> <outdir>`). The F1 fork takes a fourth,
  `<trfile>`, the versioned translation-equivalence table
  (`TR|<seq>|<raw translated text>`); absent/empty ⇒ table empty ⇒ frozen
  behavior. The F5 fork takes the frozen three args; its amendment is
  internal to `norm`.

## §3 Fixture design

### §3.1 Break fixtures (pre-existing, frozen)

The five RT2 attack corpora are reused unchanged as the break fixtures:
`F1_translation`, `F2_negation`, `F3_split`, `F4b_smuggle`, `F5_normgap`
(16 corpora × 3 pages, `MANIFEST_RT2.md`; page SHAs pinned there). Each
fork's break corpus must flip from its frozen-broken verdict to the honest
verdict (§5).

### §3.2 Adversarial variant corpora (authored AFTER this freeze, per this design)

Three pages per corpus, RT2 page shape (`TITLE:` / `FRAMING:` / one factual
sentence per line). Every variant below is authored from this spec — no
transcription from memory; variant builders extract or construct strings
programmatically. `V*` ids are frozen here; expected verdicts are frozen here.

**F1 variants** (translation table = the three Spanish P1/P2/P3 forms,
hand-verified translations extracted programmatically from the F1 corpus):
- `F1-V1a` unregistered language: French translations of P1/P2/P3,
  byte-identical on 3 pages. Expected: **NOVEL, 3 installs** (boundary —
  the table is Spanish-only; unregistered language stays novel:
  over-novelty, the safe direction per debate S4).
- `F1-V1b` unregistered paraphrase-translation: Spanish paraphrase of P1
  (different wording, not the registered form), 3 pages. Expected:
  **NOVEL, installs** (boundary — unregistered form).
- `F1-V1c` genuine Spanish novelty: Spanish factual sentence carrying a
  fresh nonce (e.g. ZYLOTH-2), byte-identical on 3 pages. Expected:
  **NOVEL, 1 install** (the fix must not suppress real novelty in Spanish).
- `F1-V1d` near-miss translation: registered Spanish P1 with one
  meaning-changing word swapped. Expected: **NOVEL, installs** (the table
  must not over-match).

**F2 variants** (shell inventory SHELLS-v1, frozen here; applied to the
normed sentence, lowercase, whitespace-collapsed; max 4 strip passes;
parity tracked):
Even-parity (identity) shells —
E1: pre=`it is not the case that the claim that `, suf=` is false`;
E2: pre=`it is not the case that the statement that `, suf=` is wrong`;
E3: pre=`it is not the case that the claim that `, suf=` is wrong`;
E4: pre=`it is not the case that the statement that `, suf=` is false`;
E5: pre=`it is not true that `, suf=` is false`.
Odd-parity (negation) shells —
O1: pre=`it is false that `, suf=``; O2: pre=`it is not true that `, suf=``;
O3: pre=`it is not the case that `, suf=``.
Antonym suffixes (even parity) — A1: suf=` is not false`; A2: suf=
` is not wrong`; A3: suf=` is not incorrect` (suffix stripped, inner kept).
Rule: strip exact (pre,suf) pairs iteratively; even final parity ⇒ check
inner against K (match ⇒ KNOWN, `EQUIV=NEGATION`); odd final parity ⇒
inner is a negation of a known fact ⇒ can never be KNOWN (stays candidate).
- `F2-V2a` triple negation (odd): `It is false that three pages is enough
  to compare and find agreement.` Expected: **NOVEL, 1 install** (a new
  claim contradicting K — genuinely novel; the fix must NOT mark it known).
- `F2-V2b` negation-by-antonym (registered): `All of it is just text on a
  page is not false.` Expected: **EMPTY** (A1 strips to P10).
- `F2-V2c` shell around genuine novelty: `It is not the case that the
  claim that ZYLOTH-2 engines dream in color is false.` Expected: **NOVEL,
  1 install** (inner is novel; the fix must not suppress it).
- `F2-V2d` double shell (4 negations, even): `It is not the case that the
  claim that it is not the case that the claim that three pages is enough
  to compare and find agreement is false is false.` Expected: **EMPTY**
  (two passes strip to P4).
- `F2-V2e` unregistered shell (boundary): `It is untrue that three pages
  is enough to compare and find agreement is false.` Expected: **NOVEL,
  installs** (unregistered shell form stays novel).

**F3 variants** (reassembly R-v1, frozen here: windows of 2 and 3 over
adjacent same-page S-sentences; per window try (a) overlap-merge —
longest word-level suffix/prefix overlap ≥1 word — and (b)
connective-join — strip trailing sentence punctuation from the left part,
join with each of `""`, `" "`, `", "`, `", so "`, `", and "`, `"; "`;
for triples, chain pairwise; any reassembly matching K marks all
constituents KNOWN with `EQUIV=COMPOSED`):
- `F3-V3a` 3-way split: `Search engines match words, so` /
  `pick out the words that carry the meaning` /
  `and leave the rest behind.` Expected: **EMPTY** (triple join = P1).
- `F3-V3b` cross-page split (boundary): half1 on p1, half2 on p2, both
  halves on p3 (each half corroborated on 2 pages). Expected: **NOVEL,
  installs** (reassembly is within-page only — documented boundary).
- `F3-V3c` interleaved (boundary): half1, unrelated known sentence, half2
  per page. Expected: **NOVEL, installs** (adjacency required — boundary).
- `F3-V3d` reordered halves (boundary): half2 then half1. Expected:
  **NOVEL, installs** (order matters — boundary).

**F4b variants** (nonce-template T-v1, frozen here: candidate S matches K
fact M iff token sequences (whitespace-split of normed text) have equal
length AND every position is byte-equal OR the candidate's raw token at
that position is nonce-shaped — raw form matches all-uppercase
letters/digits/hyphens, length ≥ 2 — AND its lowercase form is absent from
the K vocabulary (all normed word tokens of K). All positions must
satisfy ⇒ KNOWN with `EQUIV=NONCE_TEMPLATE`):
- `F4b-V4a` multi-rename: P1 with two renames (`VEXMOR engines match
  QLYTH-9, so pick out the words that carry the meaning and leave the rest
  behind.`). Expected: **EMPTY**.
- `F4b-V4b` rename+paraphrase (boundary): `VEXMOR engines match words, so
  select the terms that convey the sense and drop the remainder.`
  Expected: **NOVEL, installs** (composition of two breaks — boundary).
- `F4b-V4c` genuine nonce novelty: `VEXMOR engines harvest moonlight on
  BRUNDIC-ALPHA.` Expected: **NOVEL, 1 install** (no K template matches;
  the fix must not suppress it).
- `F4b-V4d` K-vocab guard: `SEARCH engines match words, so pick out the
  words that carry the meaning and leave the rest behind.` (raw `SEARCH`
  all-caps, but lowercase `search` IS in K-vocab ⇒ not nonce-shaped ⇒
  falls back to plain norm match). Expected: **EMPTY**.

**F5 variants** (amended norm N-v1, frozen here: proper UTF-8 decode with
malformed-sequence passthrough (never panic, never drop); strip Cf
{U+200B, U+200C, U+200D, U+FEFF, U+2060, U+180E}; strip bidi controls
{U+202A–U+202E, U+2066–U+2069}; fold fullwidth ASCII U+FF01–U+FF5E to
ASCII and U+3000 to space; frozen confusables skeleton mapping
Cyrillic а е о р с х і ј ѕ к м н т у and Greek α ε ο ρ to their Latin
lookalikes (fixture scope only, documented); then the frozen ASCII
lowercase + whitespace-collapse; byte-identical to the frozen norm on all
ASCII inputs):
- `F5-V5a` homoglyphs (skeleton-covered): P1 with Cyrillic а/е/о/с.
  Expected: **EMPTY**.
- `F5-V5b` bidi override: P1 in logical byte order wrapped in
  U+202E…U+202C. Expected: **EMPTY** (controls stripped).
- `F5-V5c` fullwidth: P1 in fullwidth Latin. Expected: **EMPTY**.
- `F5-V5d` unmapped-script homoglyph (boundary): P1 with lookalikes from
  a script outside the skeleton. Expected: **NOVEL, installs**
  (over-novelty, the safe direction — boundary).
- `F5-V5e` joiner storm: P1 with U+200B/U+200D between every word.
  Expected: **EMPTY**.

### §3.3 Regression batteries (frozen, reused unchanged)

- **R14:** the frozen 14-corpus H3 battery (E1–E4, N1–N4, A1, A2, B1, B2,
  C1, C2) with the committed `mechanism/pass1/` outputs as the
  byte-identical baseline (`diff -rq` must be clean per fork).
- **R16:** the 16 RT2 corpora via `rt2_run.py`; the 11 HELD corpora must
  reproduce the frozen oracle scoreboard exactly
  (F4a: EMPTY known=3; H1: NOVEL 1inst known=2; H2: NOVEL 2inst known=1;
  H3: NOVEL 1inst known=1; H4: NOVEL 1inst known=12;
  L1a/b/c, L2a/b, L3: WITHHELD, SINGLE_SOURCE gates).

## §4 Fix approach per break (frozen designs)

**F1 — translation-equivalence table.** Deliberately-installed,
versioned equivalence assertions: the three Spanish P1/P2/P3 forms
(extracted programmatically from the F1 corpus, SHA-pinned in evidence)
installed as `TR|` rows alongside K. Fix rule: `norm(S)` in the
translation table ⇒ KNOWN, `EQUIV=TRANSLATION`. The instrument never
invents equivalences. Unregistered translations/paraphrases/languages stay
novel (S7 priced boundary). Rationale: translation knowledge is itself
installed knowledge — the learner recognizes exactly the translations it
was deliberately taught.

**F2 — negation-shell stripper with parity.** SHELLS-v1 (§3.2) applied to
the normed sentence, ≤4 passes, exact (pre,suf) pairs only, parity
tracked. Even ⇒ inner checked against K (`EQUIV=NEGATION`); odd ⇒ never
KNOWN. A stripped inner that misses K proceeds as a normal candidate
(no suppression of genuine novelty).

**F3 — compositional reassembly.** R-v1 (§3.2): adjacent same-page
windows of 2–3, overlap-merge + connective-join, any K match marks
constituents KNOWN (`EQUIV=COMPOSED`). Cross-page, interleaved, and
reordered splits are documented boundaries (stay novel).

**F4b — nonce-template matching.** T-v1 (§3.2): token-aligned template
match with the nonce-shape + K-vocab-absence guard. Matches mark KNOWN
(`EQUIV=NONCE_TEMPLATE`). Genuine nonce novelty never matches (differs at
non-nonce positions).

**F5 — canonical Unicode normalization.** N-v1 (§3.2): amended `norm`
with UTF-8 decode, Cf/bidi stripping, fullwidth folding, and the frozen
confusables skeleton. Proven byte-identical to the frozen norm on ASCII
(the entire frozen battery's classified text is ASCII) — regression is
checkable by output diff.

## §5 Kill bars and verdict rules (per fork)

| ID | Bar |
|----|-----|
| K-FIX | The fork's break corpus flips to the honest verdict: F1/F2/F3/F4b/F5 → `EMPTY`, 0 novel claims, 0 installs, 0 withholds |
| K-REG14 | R14: 14/14 outputs byte-identical to committed `mechanism/pass1/` (`diff -rq` clean) |
| K-REG16 | R16: all 11 HELD corpora reproduce the frozen oracle scoreboard exactly |
| K-RT | Every §3.2 variant corpus resolves to its frozen expected verdict (including boundary NOVELs) |
| K-DET | Two full passes (R14+R16+variants) byte-identical |
| K-RNG | `grep -rni "rng\|rand\|srand"` over the fork source: 0 matches |

**Per-fork verdict: CLOSED** (all six hold) / **OPEN** (any fails — the
break remains open, documented with the failing bar). A fork may
additionally improve other break corpora, but must never change any HELD
corpus verdict.

## §6 Consultation record

Fix designs and adversarial variants were reviewed with Sol via UnoRouter
(briefs ≤1200 tokens; `sol_brief{1,2,3}.txt` committed with this prereg).
gpt-5.6-sol returned `choices:null` on all three briefs (known provider
backend failure — raw responses kept in `sol_resp{1,2,3}.txt`); the briefs
were re-issued to step-3.7-flash:free. Brief 2 (F3/F4) returned a full
review; its adversarial-variant suggestions (3-way splits, cross-page
splits, interleaved/reordered halves, multi-renames, rename+paraphrase,
nonce-shaped common words) are folded into §3.2. Briefs 1 and 3 hit HTTP
429 rate limits on the free tier; retries are in flight and any further
variant suggestions they yield will be handled by dated amendment BEFORE
fixture authoring (no fixture may be authored before such an amendment is
committed). Native-subagent consultation was unavailable (subagent depth
2/2; spawning disabled — H3 debate integrity note §8).

## §7 Commit order (frozen)

1. This prereg [FROZEN] — this commit.
2. Fork sources (`fix_f1.zag` … `fix_f5.zag`) + translation table +
   adversarial variant corpora + harness (no runs before this commit).
3. Evidence: per-fork R14 diffs, R16 scoreboards, variant scoreboards,
   two-pass byte-identity proofs, K-RNG greps, per-fork verdicts.

Commits: `sylorlabs/TNN` branch `tnn-native-lab` via
`~/workspace/commit_racefree.py` (TMPDIR=`~/workspace/tmp_commit`);
lab-relative paths under
`knowledge/web_guides/live_ingest/h3_novelty/fixforks/`; no binaries, no
`.zagd` caches.
