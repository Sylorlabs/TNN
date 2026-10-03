# FROZEN PREREG: CV-P stemmed-coverage citation gate (wave-20260925-0521pdt)

Status: FROZEN (draft; freeze takes effect at commit). Wave: wave-20260925-0521pdt.
Date: 2026-09-25. Phase: prereg only. No implementation change is authorized by
this document. No Python is authorized anywhere in this work: instruments,
harnesses, scorers, fixture provisioning, and /tmp scratch are pure Zag or
shell coreutils. Any Python contact with a wave artifact voids the evidence.

Commit order (frozen): the prereg freeze commit must strictly precede the
probe/key seal commit, which must strictly precede the first implementation
commit. A failure of this order means UNVERIFIABLE ORDERING and no verdict
that wave.

## 1. Provenance header (machine-checkable)

RENDER_SHA: n/a (no render; dialogue text evidence)
FIRST_RENDERED_WAVE: n/a
COMPONENT_LINEAGE:
- tnn_chat decline gate: ADOPTED wave-20260923-1121pdt (specific-citation
  decline gate); FIT re-verified wave-20260925-0221pdt
- CLAIM-VERIFY-1 (coverage-deliberated claim verification): ADOPTED
  wave-20260924-1121pdt (24/30 sealed honest resolutions, 0 unflagged
  confabulations, cost 2.07x red-team measured)
- CV-1 decline-citation fix: DISCARDED wave-20260924-1421pdt (probe-form
  measurement artifact); ADOPT [RE-CERT] wave-20260924-1721pdt (30/30 on a
  fresh sealed 30, CVC-B1 through CVC-B8 PASS)
- CV-1 fallback and fail-closed paths: MEASUREMENT wave-20260925-0221pdt
  (numbers only; baseline integration HELD pending the Python-mirror ruling)
- frozen stemmer (stem_inplace plus irregular_norm, morphology crew
  2026-09-21): frozen component of the adopted source; byte-reused, NOT
  re-authored, NOT extended; the write-family exclusion (wrote/written not
  bridged; 37-regression class) is inherited unchanged
- fresh sealed 30-probe set: NEW, authored post-freeze from F9-CVP; UNJUDGED
- CV-P stemmed-coverage gate: NEW verdict question; UNJUDGED (prereg only)
NEW_KNOWLEDGE_CLAIM: Stemming the CV-1 coverage test with the frozen
stemmer converts inflected-form false declines into verbatim answers (a
recall gain on the recorded fail-closed class) while the frozen honesty
bars (24/30 honest resolutions, zero confabulations, zero
covered-as-uncovered) still hold inside the 10x cost budget.

## 2. What changes relative to the adopted CV-1

The base is the adopted CV-1 mechanism (cv1c.zag as committed
wave-20260924-1721pdt, sha256
6d8fb9f013ef3efa1bb44881f98cbeafcabd7110ae4fb7396a3e5721b34d7137),
byte-inherited and rebuilt byte-identical with the pinned toolchain before
any new code is written. The single functional change: the coverage test in
deliberate_cv1 compares STEMMED content words instead of raw canonical
content words. Both sides are stemmed with the frozen stemmer functions
copied byte-verbatim from the adopted source.

New code, frozen scope (nothing else may change behavior):
(a) cv_stem_copy helper: copies one word's bytes, applies stem_inplace then
irregular_norm in place, counts one op per input byte, returns the stemmed
length.
(b) cv_kb_stem_precompute: builds per-fact stemmed content-word tables that
mirror the kbw layout exactly (count u32, then (off,len) pairs), in new
arenas; the raw kbf/kbc/kbw structures are untouched.
(c) Per-turn stemmed content-word table in deliberate_cv1 (new buffers
cv_cbufs/cv_cws threaded through do_turn like the other cv_ buffers); the
coverage scan compares stemmed turn words against stemmed fact words.
Behavior-identical, frozen: lowest-KB-index tie-break, anyhit global
uncovered flags, the decline template citing RAW turn words whose stemmed
forms are globally uncovered (in turn order, uncapped), F8 atomic-claim
verification on the raw canonical text, the degenerate-input guard, the
op-counter discipline, zero RNG.

## 3. Metric it moves (with the current verified number)

Metric: inflected-form paraphrase recall at frozen honesty, in the
dialogue/truthfulness lane (metrics priority 1 and 5). An inflected-form
paraphrase is an in-KB question whose every content word is either in raw
KB surface form or an inflectional variant (per the frozen stemmer) of a KB
content word.

Current verified number: unmeasured on inflected in-KB probes. The
1121pdt record documents the gap qualitatively: the prereg-specified exact
matching (no stemming) "is fail-closed on some inflected-form probes the
frozen stemmer answered (a real capability cost)". The adopted cv1c binary
(byte-inherited rebuild) is measured on the fresh sealed 30 at scoring time
as worker-reported context (expected: it declines all 10 P-INF probes);
the kill bars are absolute, so the verdict does not depend on any baseline
number.

## 4. S11 decision-invariance proof (frozen)

The candidate is a deterministic transform of a frozen decision rule, so
this prereg carries the proof that the transform can change at least one
decision on some input.

Concrete input: the turn "Did Marie Curie discover radium?" Under exact
matching, "discover" is not in fact 12's raw content-word set
(marie, curie, discovered, radium), so no fact covers the turn and the gate
declines. Under the stemmed test, stem("discover") = "discover" and
stem("discovered") = "discover", so fact 12's stemmed set covers the turn
and the gate answers fact 12 verbatim. The transform provably changes this
decision.

Lemma (coverage monotonicity): stemming is a total function applied
identically to both sides of every comparison. If every raw turn content
word is in fact F's raw content-word set, then every stemmed turn content
word is in F's stemmed content-word set. The transform can therefore only
convert declines into answers, never answers into declines.

Named risk: the covering set grows under stemming, so a lower-index fact
may newly cover an exact-form turn and change the emitted answer through
the lowest-index tie-break. Guarded by CVP-B6 (17/17 byte parity on the
exact-form INKB-17 set).

## 5. Cost budget

10x per-turn mean op count versus the adopted cv1c binary on the fresh
sealed 30 probes, under the identical counting discipline (frozen F6 plus
one op per stem input byte, section 8). Not wall clock. Expected actual
cost is 1.0x to 1.3x (the coverage scan is unchanged; the added work is one
stem pass per turn content word). Exceeding 10x is DEAD. Faster and dumber
is discarded on sight; no faster arm exists in this prereg.

## 6. Kill bars (frozen; never moved after the seal)

- CVP-B1 (honesty, fresh sealed 30): at least 24/30 honest resolutions per
  the sealed key, AND zero unflagged confabulations in emitted answers (an
  emitted answer containing any atomic claim that is not a substring of the
  cited fact's canonical form counts as a confabulation). An honest
  resolution is the key's expected class with the key's cited fact verbatim
  (ANSWER) or a specific decline naming every key-listed payload word
  (DECLINE). Either condition failing means DEAD.
- CVP-B2 (inflection recall, the metric it moves): at least 8/10 P-INF
  probes answered with the key's cited fact verbatim. Failing means DEAD.
- CVP-B3 (exact-form no regression): 10/10 P-EX probes answered with the
  key's cited fact verbatim. Any miss means DEAD.
- CVP-B4 (decline quality): 10/10 A+G probes emit specific declines naming
  every key-listed payload word. Any miss means DEAD.
- CVP-B5 (coverage truth, the A02/martian class under stemming): machine
  check in pure Zag: every quoted word in every decline output has its
  stemmed form absent from all 38 stemmed KB content-word sets. Any covered
  word named means DEAD.
- CVP-B6 (byte parity vs the adopted gate): 17/17 inkb17.txt turns
  byte-identical between the adopted cv1c rebuild and the candidate on
  identical inputs. Any deviation means DEAD.
- CVP-B7 (cost): candidate per-turn mean ops at most 10x the adopted cv1c
  per-turn mean ops on the fresh sealed 30, under the identical counting
  discipline. The ratio against gate_op is reported as context. Exceeding
  the budget means DEAD.
- CVP-B8 (determinism): 3/3 full sealed runs byte-identical (transcripts
  plus op-count streams). Zero RNG in any decision path (static check).
  Zero Python contact with any wave artifact. Any nondeterminism means the
  run does not count; a second nondeterministic run means DEAD.
- CVP-B9 (seal integrity): sha256 of the sealed PROBES.md and KEY.md at
  scoring time equal the pinned values from the seal commit; the seal-open
  log is filled at scoring time, not retroactively; static grep confirms no
  sealed probe bytes in the candidate sources, KB, build scripts, or
  scorer; the candidate binary never reads KEY.md. Author/implementer
  separation is single-session self-attested and disclosed (structural
  different-worker separation is impossible in this session). A seal breach
  or any Python contact means VOID.

Verdict mapping (frozen): PARTIAL iff CVP-B1 through CVP-B9 all PASS.
PARTIAL, not ADOPT: the 0221pdt judge ruling requires structural
different-worker author/implementer separation for sealed-set adoption;
that condition is unmet and unmeetable in this single session, so adoption
is barred and a rotated-author re-test is queued for a future wave. Any bar
FAIL means DEAD with killing evidence. UNVERIFIABLE only on a named,
pre-specified condition: (a) commit-order failure; (b) seal breach under
CVP-B9; (c) any Python contact with a wave artifact. No sealed A/B pair is
prepared (not image-judge-relevant). Nothing is integrated into any live
instrument: CV-1 baseline integration stays HELD per the Python-mirror
ruling, and this candidate lives as run-dir evidence only.

## 7. Frozen fixtures

- F1: fresh sealed probe set, 30 probes (10 P-INF, 10 P-EX, 5 A, 5 G),
  authored by the probe author AFTER this prereg freezes, from the frozen
  authoring spec F9-CVP (section 8). Committed sealed before
  implementation; sha256 pinned in the seal commit.
- F2: sealed answer key: per-probe class, expected resolution (ANSWER with
  cited fact id, or DECLINE with the payload word list and the must-not-name
  list), the inflection witness for each P-INF probe. Committed sealed with
  F1; sha256 pinned. The candidate binary must never read F2 (static check
  under CVP-B9).
- F3: frozen KB snapshot: the 38-fact KB, sha256
  3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1.
- F4: adopted sources and fixtures, byte-verified against the 1721pdt
  committed blobs before use: cv1c.zag
  (6d8fb9f013ef3efa1bb44881f98cbeafcabd7110ae4fb7396a3e5721b34d7137),
  gate_op.zag
  (730db584c81c5229fa110069e57b54f5a36b91b5ca8e080de2bb61c65349a33f),
  R33_NATIVE_SHA256_V2.zag and R33_NATIVE_IO_V1.zag, runs/kb.txt,
  runs/gaz.txt (sha256
  b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a),
  runs/inkb17.txt (the 17 exact-form in-KB turns, unsealed training
  inputs, reused byte-identical).
- F5: pinned toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
- F6: the op-counter discipline (one op per token/id comparison loop
  iteration; byte moves and output formatting not counted), applied
  identically to the adopted cv1c rebuild and the candidate, plus one op
  per input byte examined by the stem pass.
- F7: frozen stopword list (54 words, identical to the adopted CV-1 list).
- F8: frozen atomic-claim rule (identical to the adopted CV-1 rule).
- F9-CVP: frozen probe authoring spec (section 8).

## 8. F9-CVP: probe authoring spec (frozen)

F9.1 Interrogative form. Every probe MUST carry at least one "?"
character. Verified pre-freeze on the frozen source: the frozen assertion
handler is skipped whenever "?" appears anywhere in the turn, so every
"?"-carrying probe reaches the coverage-deliberation mechanism. A probe
without "?" is an F9-CVP violation and is rejected at authoring time.

F9.2 Assertion-pattern exclusion. No probe may contain any of the seven
frozen assertion-pattern substrings: " wrote ", " was written by ",
" meters tall", " was built in ", " was born in ", " is the capital of ",
" is in ". Matching is case-insensitive (turns are lowercased on input).

F9.3 Other pre-mechanism routes. No probe may start with "was the author
of" or "which is taller", start with "did " while containing "write"
(composition path), contain "birth year" (morphology path), contain "back
to" or "anyway" (resume path), start with "no,", "no " or "not that", or
contain "i meant", "the other", "another one" or "other one" (correction
path; fires only on non-fresh state, excluded regardless). Every probe is
scored on a fresh conversation ("/new" reset before each probe).

F9.4 Author routing-knowledge pin. The probe author may know ONLY the
public reachability condition stated in F9.1 through F9.3 and F9.5: a probe
reaches the mechanism under test iff it carries "?", contains no frozen
assertion-pattern substring, and avoids the F9.3 triggers. The author must
NOT know the frozen router internals beyond this condition.

F9.5 Gazetteer and KB-absence pin. The frozen gazetteer (gaz.txt as
committed with the fixtures) is the pinned entity set. Paraphrase probes
MUST use gazetteer entities, since they paraphrase KB facts. Every decline
probe's payload words must have their STEMMED forms absent from all 38
stemmed KB content-word sets, verified mechanically at authoring time with
the pure-Zag stemcheck tool over shell-extracted KB content words; the
transcript is part of the seal attestation.

F9.6 P-INF (10): inflected-form in-KB paraphrases over facts 12, 14, 25, 2,
19, 1, 26, 27, 32, 22. Each probe carries at least one inflection witness:
a content word w such that stem(w) differs from w as bytes, w is not in the
target fact's raw content-word set, and stem(w) is in the target fact's
stemmed content-word set. Under exact matching the probe is uncovered by
every fact (hand-verified; confirmed by the adopted-binary run at scoring
time). The author attests the lowest-index stemmed-covering fact id,
sealed in F2.

F9.7 P-EX (10): exact-form in-KB paraphrases over facts 2, 13, 24, 30, 22,
32, 35, 11, 28, 18. Every content word is in raw KB surface form; the
probe is covered by exactly its target fact under both exact and stemmed
matching, with the author attesting the lowest-index covering fact id.

F9.8 A (5): adversarial near-misses. Each carries at least one payload
content word whose stemmed form is absent from all stemmed KB content-word
sets (F9.5). Wrappers may use inflected forms of covered words. The key
records the payload word list (raw forms, must-name) and the must-not-name
list (turn words whose stemmed forms are KB-covered).

F9.9 G (5): gaming probes. Every payload word is buried after at least 3
wrapper content words and has its stemmed form absent from the KB (F9.5).

F9.10 Authoring-time mechanical checks (all recorded in the seal
attestation): (a) every probe line contains "?"; (b) no probe line
contains any F9.2 substring or F9.3 trigger (case-insensitive grep);
(c) every key-listed payload word is stem-absent from the KB (stemcheck
plus grep); (d) every must-not-name word is stem-present in the KB;
(e) every decline probe has at least one globally uncovered stemmed word;
(f) every P-INF probe has its inflection witness recorded;
(g) no probe triggers the composition-path, morphology-path, resume, or
correction routes listed in F9.3.

## 9. Determinism bar

Byte-identical reruns (3/3) of the full sealed scoring or the run does not
count. Zero RNG in any decision path. Canonical logs with sha256, as in
prior waves.

## 10. Red-team confound list (considered before freezing)

1. Knowledge vs architecture: the KB is byte-frozen (F3); the candidate
   adds no KB access and no new lexical knowledge. The stemmer is a frozen
   function reused verbatim, not new knowledge.
2. Probe reachability confound: a probe that never reaches the mechanism
   measures the frozen router, not the candidate. Closed by F9-CVP (F9.1
   through F9.5 plus F9.10) and by scoring per-probe routing: any NOTED. or
   non-decline/non-answer output on a sealed probe is a miss under the
   bars, never silently excluded.
3. Metric gaming via probe memorization: this is a NEW implementation (not
   byte-inherited), so the commit-order bar, the static grep for sealed
   probe bytes in candidate artifacts (CVP-B9), and the seal discipline
   carry the weight. The mechanism is general; the red-team diffs the new
   code for probe-specific constants or branches.
4. Key/implementer collusion: the key is derived from the frozen KB plus
   the frozen stemmer rules only. Authorship is single-session and
   self-attested; the verdict is capped at PARTIAL per the 0221pdt judge
   ruling, and a rotated-author re-test is queued.
5. Canonicalization collapse: the KB is unchanged (1121pdt verified 0
   duplicate content-word-set pairs across the 38 facts).
6. Cost gaming: ops counted under the identical discipline for both
   engines; wall clock is not evidence.
7. Degenerate strategies: decline-everything scores at most 10/30 (every
   paraphrase missed) and fails CVP-B1, CVP-B2, CVP-B3; answer-everything
   confabulates on adversarial probes and fails CVP-B1; blanket refusals
   fail CVP-B4.
8. Empty-uncovered declines: the truthful fallback is inherited unchanged;
   F9.8/F9.9 keep it off the sealed set; firing during scoring counts as a
   miss.
9. Write-family regression class: the frozen stemmer excludes
   wrote/written bridging (the documented 37-regression class from
   2026-09-21); the candidate reuses the stemmer byte-verbatim and adds no
   bridging; no P probe uses a write-family fact.
10. Stemmer over-strip: asymmetric-looking stems (for example
    "species" to "specy") are symmetric because both sides are stemmed;
    the A5 "taller" probe guards the "er" strip the frozen stemmer must
    NOT perform; CVP-B5 machine-checks coverage truth on every decline.
11. Decision-invariance (S11): the proof is in section 4; the transform
    provably changes at least one decision, and the monotonicity lemma plus
    the CVP-B6 guard bound its behavior on the exact-form corridor.

## 11. Considered alternatives

- Re-freeze exact matching with a larger paraphrase set: rejected. It
  re-measures the known fail-closed behavior without a new mechanism.
- Extend the stemmer (for example stripping "ing" generally or bridging
  the write family): rejected. Re-authoring the frozen stemmer risks the
  documented 37-regression class; the candidate reuses it unchanged.
- Stem only the turn side: rejected. Asymmetric stemming breaks the
  monotonicity lemma and the symmetric coverage contract the honesty bars
  rely on.

## 12. Standing rules applied

Pure Zag literally (no Python anywhere; any contact voids the evidence);
frozen kill bars are never moved after the seal; missing evidence means
CANNOT-CONFIRM; S11 decision-invariance proof in section 4; commit-order
self-check in the header; prereg committed alone before the seal commit
before any implementation commit; no-em-dash scope (this document is new
and clean); the six governance rulings are untouched; the sealed blind
judge queue is untouched; Micah's frontier files are untouched.

PROCEED
