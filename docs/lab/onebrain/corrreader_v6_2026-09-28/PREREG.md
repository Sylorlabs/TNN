# PREREG — operative-utterance understanding (v6)

**Frozen:** 2026-09-27 (PDT). **Status:** preregistered before any mechanism code is written.
**Parent line:** one-brain correction-protection. The v5 skip rule is sound; the v5 correction
*reader* was killed by red team (naive token triggers `no`/`actually`/`meant`/`correction` with no
handling of quotation, mood, hedging, or negation — 4 kills). This prereg governs the replacement:
native operative-utterance understanding, built in pure Zag (zero RNG), living inside
deliberation — the correction reading (rd==0) consults it.

## 0. Reframe amendment (Micah, 2026-09-27)

This is **not a classifier** and TNN is not a classifier. What is built here is a **native
deliberative mechanism**: TNN's own machinery for determining the operative status of an
utterance — operative correction vs quoted speech vs reported speech vs hypothetical vs
negated vs hedged — as part of its understanding/epistemics, living inside its deliberation,
not a bolted-on module. Terminology updated accordingly ("operative-utterance understanding",
"understanding pass", "operative status"); the frozen rules (§2) are unchanged. Architecturally
the mechanism is a **single understanding pass** (`ou_annotate`): TNN reads the utterance once
and records each token's operative status as deliberation state; downstream machinery (reading
evidence, topic selection, reintegration) consults that understanding rather than re-deciding
it at each call site. This is a broad repair to how TNN reads utterances, not a narrow token
gate: the correction reading no longer fires on bare tokens at all — it fires on TNN's
understanding that a correction was operatively performed.

## 1. Definitions

An **operative correction** is an utterance by the speaker, in the current turn, that *performs* a
self-correction act: it revokes or refines a prior description X and substitutes Y
("no, I meant prejudice"). The speaker is the utterer; the act is performed — not quoted,
supposed, denied, or hedged.

**Non-operative classes:**
- **QUOTED:** correction phrasing inside quotation marks (any nesting depth), i.e. not the
  speaker's own voice at that point.
- **REPORTED:** correction phrasing attributed to a third party via a speech verb
  ("my friend said…", "she told me…", "according to…").
- **HYPOTHETICAL:** correction phrasing inside a conditional/suppositional clause
  ("if…", "suppose…", "what if…", "unless…", "whether…").
- **NEGATED:** the correction verb itself negated ("never", "not", "didn't", "did not",
  "had not", "hadn't" + mean/meant).
- **HEDGED:** the correction phrasing under a hedge ("maybe", "perhaps", "might have",
  "possibly", "could", "I think", "I guess", "seems").

**Preregistered rulings (frozen):**
- R-A: Hedged = non-operative. A withheld commitment is not a performed act. The skip rule's
  false-positive cost is a verdict flip; resolve ambiguity conservatively. (The prior red team
  graded the hedge kill "moderate" — genuinely arguable; this prereg settles it.)
- R-B: First-person self-report ("i said no, i meant X") = operative. REPORTED requires
  third-party attribution; the speaker's own voice stays operative.
- R-C: Trigger set is FROZEN at {`no`, `actually`, `meant`, `correction`}. Present-tense `mean`
  remains a documented gap (carried over from attack 6 / n1) — out of scope for this line.
- R-D: The 4-token post-trigger topic window is UNCHANGED (attack-6 topic-dilution documented
  limitation, was HOLD) — out of scope for this line.

## 2. Classification rules (frozen)

Input: the lowercased query bytes `qbuf[0..qlen]`, and a trigger-token occurrence at byte
offset `off`, length `len`. Output: 1 = operative correction occurrence, 0 = not.

- **R0.** Token not in {`no`,`actually`,`meant`,`correction`} → 0.
- **R1. QUOTE.** Scan bytes `[0, off)`: toggle in-double-quote on `"` (byte 34); toggle
  in-single-quote on `'` (byte 39) only when NOT between two alphanumeric bytes (apostrophe
  guard: "don't" must not toggle). If inside either at `off` → 0.
- **R2. CLAUSE.** Clause = maximal span around `off` bounded by `;` `?` `!` `.` newline or
  buffer ends. R5, R6, and the R7 positive patterns are clause-local. R3 and R4 use the
  wider *sentence* scope defined in their rules (commas do not end mood scope).
- **R3. REPORTED.** If a speech verb in {say, said, says, saying, tell, told, tells, telling,
  write, wrote, writes, writing, claim, claimed, claims, claiming, state, stated, states,
  think, thought, thinks, thinking, believe, believes, mention, mentioned, mentions,
  report, reported, reports, ask, asked, asks, asking} occurs
  before the trigger in its *sentence* AND a third-person subject in {he, she, they, him,
  her, them, his, their, friend, friends, mother, father, brother, sister, man, woman,
  guy, person, people, teacher, doctor, boss, neighbor, john, mary, dad, mom, buddy,
  colleague, wife, husband, son, daughter} occurs within the 3 tokens before that verb
  → 0. Sentence = span split on `?` `.` `!` `;` only (commas do not end mood scope —
  reported content spans clause boundaries: "she told me no, i meant moby dick" — the
  "i meant" clause is still her speech). Special case: "according" before the trigger
  with "to" within the next 2 tokens → 0. First-person "i said" is exempt (ruling R-B).
  A sentence break resets the scope: "she told me the answer. no, i meant the other one?"
  keeps the second sentence operative.
- **R4. HYPOTHETICAL.** If any of {if, suppose, supposing, whether, unless, assuming,
  provided} occurs before the trigger in its sentence (same sentence scope as R3) → 0.
  ("no wait, unless the capital moved, i meant paris?" — the unless-clause conditions
  the correction even across the comma.)
- **R5. NEGATED.** For verb triggers (`meant`; `mean` is not a trigger): if a negation token
  in {never, not, nobody, none, hardly, scarcely, barely, didn, don, doesn, isn, aren,
  wasn, weren, haven, hasn, hadn, won, wouldn, couldn, shouldn, mustn, needn, daren}
  occurs within the 3 tokens before the verb, or token `t` occurs within 3 tokens before
  with the previous token in {can, don, didn, doesn, isn, aren, wasn, weren, haven, hasn,
  hadn, won, wouldn, couldn, shouldn, mustn, needn, daren, ain} → 0.
  Exceptions: a clause-initial `no` is a discourse marker, never a negator (protects the
  canonical "no, i meant X"); and a `no` immediately followed by `i`/`we` is the discourse
  "no, i …" construction, never a negator (protects first-person "i said no, i meant X",
  ruling R-B).
- **R6. HEDGED.** If any of {maybe, perhaps, might, possibly, could, probably, presumably,
  apparently, seems, seem} occurs within the 4 tokens before the trigger, or (`i` within
  4 tokens before AND the token after that `i` is in {think, guess, believe, suppose}) → 0.
- **R7. POSITIVE PATTERNS** (must match one, else 0):
  - **O1:** trigger `no`, where every token before it in the clause is a discourse particle
    in {well, oh, uh, um, ah, okay, ok, right, so} (clause-initial modulo particles),
    AND within the next 4 tokens after `no` there is `i`/`we` followed by `mean`/`meant`,
    or the token `correction`. ("no, i meant X"; "well no, i meant X")
  - **O2:** trigger `actually`, with `i`/`we` + `mean`/`meant` within 3 tokens on either side.
  - **O3:** trigger `meant`, with `i`/`we` within the 3 tokens before it.
  - **O4:** trigger `correction` is the first token of the clause, or (the previous token
    is in {a, the, my, this, that} AND the byte immediately after the token
    (`qbuf[off+len]`) is `:` or `,`, or the token is the last token of the clause)
    — i.e. label use ("correction: X", "a correction: X"), not attributive use
    ("the correction policy").

First 0 wins (R0→R6); R7 decides 1 vs 0.

## 3. Frozen classification battery (43 items)

Format: id | query | expected | class. The 4 red-team kills are included verbatim (K1–K4).

OPERATIVE (12):
- G01 | really, moby dick and austen's novel are the ones; no, i meant prejudice? | OP | genuine (q06 idiom)
- G02 | really, herman melville and the whaling tale are the ones; no, i meant dick? | OP | genuine (q07 idiom)
- G03 | really, the capital of france and the paris museum are the ones; no, i meant louvre? | OP | genuine (q08 idiom)
- G04 | i meant the louvre | OP | bare i-meant (q39)
- G05 | no, i meant moby dick; really, pride and prejudice is better? pride and prejudice is finer? | OP | genuine (E01)
- G06 | correction: the louvre | OP | label (O4)
- G07 | a correction: the louvre | OP | label w/ article (O4)
- G08 | i actually meant the louvre | OP | actually (O2)
- G09 | actually, i meant the louvre | OP | actually fronted (O2)
- G10 | france capital is paris; no wait, i meant lyon? | OP | mid-stream self-correction
- G11 | no, i meant moby dick; no, i meant pride and prejudice; really, pride and prejudice is better? | OP | double correction (a4)
- G12 | i said no, i meant moby dick | OP | first-person self-report (ruling R-B)
- G13 | well no, i meant the louvre? | OP | discourse particle before no (O1)

NON-OPERATIVE (32):
- K1 | prove france capital today; france capital france capital france capital; my friend said no, i meant moby dick? | NON | REPORTED (red-team kill, verbatim)
- K2 | prove france capital today; france capital france capital france capital; if i said no, i meant moby dick, would you correct me? | NON | HYPOTHETICAL (red-team kill, verbatim)
- K3 | prove france capital today; france capital france capital france capital; maybe i meant moby dick? | NON | HEDGED (red-team kill, verbatim)
- K4 | prove france capital today; france capital france capital france capital; i never meant moby dick? | NON | NEGATED (red-team kill, verbatim)
- Q1 | prove france capital today; "no, i meant moby dick"? | NON | QUOTED (literal double quotes)
- Q2 | prove france capital today; 'no, i meant moby dick'? | NON | QUOTED (literal single quotes)
- Q3 | he said 'no, i meant moby dick' yesterday? | NON | QUOTED nested + REPORTED
- Q4 | "my friend said no, i meant moby dick"? | NON | QUOTED whole clause
- R1 | she told me no, i meant moby dick? | NON | REPORTED (told)
- R2 | according to my friend, i meant moby dick? | NON | REPORTED (according to)
- R3 | they claim i meant moby dick? | NON | REPORTED (claim, third-person)
- H1 | suppose i said no, i meant moby dick? | NON | HYPOTHETICAL (suppose)
- H2 | what if i meant moby dick? | NON | HYPOTHETICAL (what if)
- H3 | unless i meant moby dick, the answer stands? | NON | HYPOTHETICAL (unless)
- H4 | no wait, unless the capital moved, i meant paris? | NON | HYPOTHETICAL ("no wait, unless…" — red-team priority phrasing)
- N1 | i had not meant moby dick? | NON | NEGATED (had not)
- N2 | i hadn't meant moby dick? | NON | NEGATED (contraction split hadn+t)
- N3 | there is no way i meant moby dick? | NON | NEGATED (mid-clause no)
- E1 | perhaps i meant moby dick? | NON | HEDGED (perhaps)
- E2 | i think i meant moby dick? | NON | HEDGED (i think)
- E3 | it seems i meant moby dick? | NON | HEDGED (seems)
- E4 | i could have meant moby dick? | NON | HEDGED (could)
- B1 | really, france capital france capital; no, moby dick? | NON | bare no, no O-pattern (n3)
- B2 | really, france capital france capital; correction: moby dick? | OP | label (n2 — reader fires, duel kills downstream; the understanding says OP)
- B3 | no moby dick here? | NON | mid-clause no, no O-pattern
- B4 | i never said no? | NON | negated, no correction verb (no trigger fires: "no" mid-clause)
- B5 | do you know the correction policy? | NON | "correction" attributive ("the correction" + following byte is a space, not `:`/`,`/end) → NON (O4 narrowed)
- B6 | the correction was wrong? | NON | "correction" mid-clause, not label use → NON (O4 narrowed)
- B7 | i meant well? | OP | "i"+"meant" → OP by O3 (no revoked content, but the *form* is an operative self-correction report; the duel/topic machinery decides what it corrects — the understanding only judges the act)
- B8 | we meant the louvre? | OP | we-subject (O3)

Note on B5/B6: O4 is narrowed — `correction` with a preceding article fires ONLY for label
use: the byte after the token is `:`/`,`, or it is the last token of the clause; or it is
clause-initial. Attributive use ("the correction policy") stays NON.

## 4. Bars

- **B-und (understanding):** 100% agreement on the 43 frozen items above. Rationale for exact:
  a single false positive can flip a verdict through the skip; a false negative falls back to
  unprotected behavior (status quo). The bar is exact because the cost is asymmetric.
- **B-e2e (skip re-verification):** v7 nov4 = 38/44, v8 nov4 = 16/20, all other 7 modes
  byte-identical to v5 verification; 3× byte-identical reruns; the 4 kill items (K1–K4
  scaffold) now produce bid 19 = v4-control behavior.
- **B-rt (independent red team):** fresh adversarial items (priorities: "no wait, unless…"
  constructions, nested quotations, self-corrections mid-stream). KILL = the mechanism's operative-status output
  contradicts §2 on a fresh item AND protected-with-understanding does strictly worse than the
  v4 control on that item. Zero kills required.
- **Governance:** adoption does NOT re-enact from this line. On all bars passing, report to
  the parent; the parent routes the adoption decision.

## 5. Build rules

Pure Zag, zero RNG, deterministic given state. Build from the v5 source
(`onebrain_v5_corrprotect.zag`, SHA-256 `234e9d1e…beeca` per VERIFICATION.md) with the
correction reading (rd==0) consulting the operative-utterance understanding (single
`ou_annotate` pass; the evidence scan and topic window read the annotations);
everything else byte-identical in behavior. Commit evidence to `tnn-native-lab`
(never `main`); no binaries, caches, or `.zagd` in the commit.
