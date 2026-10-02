# FORK D — SELF-PAM AS DISCIPLINE: FROZEN FORK PREREG

**Date:** 2026-09-23 | **Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Program:** H6 revival round 2 — self-PAM, the meaning attack.
**Parent prereg:** `docs/lab/senses/pam-rebuild/selfpam/r2/PREREG.md` (frozen, b3db7b7a) — binding.
**Status:** FROZEN. Amendments require the coordinator and are committed alone.
**Scope:** this document governs fork D only. It was committed alone before
any fork-D mechanism code was written.

## 0. Identity and honest claim (debate-verdict compliant)

Fork D is **DISCIPLINE**, built from Muse-A fork 1 (Atomize + Narrow
Re-Derivation) combined with Muse-A fork 3 (Entitlement Cross-Check),
reframed per the binding debate verdict (§0.1 of the program prereg).

- **What it is:** a type-checker on drafts. A fixed rule-based atomizer maps
  each draft sentence to canonical `(Q,S,POL,R,O)` atoms in a closed relation
  vocabulary; a SEPARATE frozen prover module re-derives each atom from the
  committed store through a path the generator did not choose (exact lookup +
  a fixed entailment kernel, depth-capped); a frozen entitlement cross-checker
  verifies every draft atom traces to the deliberation record's conclusions
  via the same fixed kernel, and flags silent revision of those conclusions.
- **What it claims:** it catches ungrounded speech mechanically. It claims
  **NO new evidence about the world** (no corroboration — the
  "corroboration" framing is dead per the binding verdict; Muse-B's 0-bit
  attack stands unrefuted and this fork does not contest it).
- **What it does not claim:** truth. A draft that is false-but-consistent
  with the committed store passes the store path by design; a draft whose
  support lives only in generator-authored entries is rejected only because
  the harness pins provenance (see §6 — the write-once-partition stand-in,
  explicitly declared, not smuggled).
- **Theater-signature rule (self-applied):** passing M1–M3 while failing
  M4/M5 is the predicted consistency-theater signature. If fork D exhibits
  it, fork D is documented as theater, not as a survivor — no re-framing.

## 1. Frozen mechanism spec

### 1.1 Canonical atom

`Q|S|POL|R|O` — five `|`-separated fields, lowercase ASCII, single tokens
(no spaces; multiword values joined with `_` at generation time — the
fragment below never needs them).

- `Q` ∈ {UNIT, ALL, SOME, ONLY} — quantifier. UNIT = definite/bare singular
  referent ("the cat"); ALL/SOME from "all"/"some"; ONLY from "only".
- `S`, `O` — canonical entity/property tokens (see §1.3 alias table).
- `POL` ∈ {POS, NEG} — polarity. NEG from "not"/"n't".
- `R` ∈ closed relation vocabulary (§1.2).

Store lines add a sixth field, provenance: `Q|S|POL|R|O|PROV`,
`PROV` ∈ {EXT, GEN}. EXT = world-authored (harness-pinned; stand-in for the
write-once evidence partition). GEN = generator-authored in a prior pinned
episode (the recursion material).

### 1.2 Closed relation vocabulary (10 relations, frozen)

IS_A, LOC_ON, LOC_UNDER, LOC_IN, HAS_PROPERTY, PROP_NUM, CAUSED_BY, BEFORE,
PART_OF, SIBLING_OF.

PROP_NUM objects have the form `adj:n` where `n` is a canonical number
(`1/2`, `1/4`, `3/4`, `1`, `2`, `3`, `4`, `0`) — e.g. `full:1/2`.

### 1.3 Sentence fragment (the fixed grammar; parser inverts these templates)

`{S}` subject noun phrase ("the cat", "all cats", "some dogs", "only birds",
"no fish"); `{O}` object noun phrase; `{A}` adjective from the frozen adj
table; `{N}` number word from the frozen number table. Articles "the/a/an"
stripped. Frozen alias table (excerpt; full table in source
`tables.zag`, frozen at build): kitten→cat, puppy→dog, feline→cat,
kitty→cat, couch→sofa, rug→mat? — NO: rug stays distinct (needed for entity
swaps). Full table committed with the build; the rule is: aliases map to a
canonical token, never to each other; every battery sentence's canonical
form is fixed by the table.

Templates (→ canonical atom):

- T1 `{S} is a {O}.` / `{S} is an {O}.` → `(Q,S,POS,IS_A,O)`
- T2 `{S} is {A}.` → `(Q,S,POS,HAS_PROPERTY,A)`
- T3 `{S} sat on {O}.` / `{S} sits on {O}.` / `{S} is on {O}.` /
  `{S} is sitting on {O}.` → `(Q,S,POS,LOC_ON,O)`
- T4 `{S} is under {O}.` / `{S} is below {O}.` / `{S} is beneath {O}.` →
  `(Q,S,POS,LOC_UNDER,O)`
- T5 `{S} is in {O}.` / `{S} is inside {O}.` / `{S} lies in {O}.` →
  `(Q,S,POS,LOC_IN,O)`
- T6 `{O} was sat on by {S}.` → `(Q,S,POS,LOC_ON,O)` (passive of T3)
- T7 `{S} was caused by {O}.` / `{O} caused {S}.` → `(Q,S,POS,CAUSED_BY,O)`
- T8 `{S} is before {O}.` / `{S} comes before {O}.` / `{S} preceded {O}.` →
  `(Q,S,POS,BEFORE,O)`; T8b `{O} is after {S}.` → `(Q,S,POS,BEFORE,O)`
  (clause-reorder paraphrase)
- T9 `{S} is part of {O}.` → `(Q,S,POS,PART_OF,O)`
- T10 `{S} is a sibling of {O}.` → `(Q,S,POS,SIBLING_OF,O)`
- T11 `{S} is {N} {A}.` → `(Q,S,POS,PROP_NUM,A:n)` (number canonicalized)
- T12 negation: `not`/`n't` after the auxiliary negates POL:
  `{S} is not {A}.` → `(Q,S,NEG,HAS_PROPERTY,A)`;
  `{S} did not sit on {O}.` → `(Q,S,NEG,LOC_ON,O)`
- T13 `{Sp} are {O}.` with leading quantifier: "all"→ALL, "some"→SOME,
  "only"→ONLY, "no"→`(ALL,Sp,NEG,IS_A,O)`; "not all"→`(SOME,Sp,NEG,IS_A,O)`
  (negation-scope form).

Any sentence matching no template → atom `UNPARSED` → WITHHOLD
(cited as `UNPARSED`). The parser is total: every input yields atoms or
UNPARSED; it never throws.

Paraphrase-normalization built into the atomizer (frozen):
synonym→canonical via alias table; active↔passive (T3↔T6); clause reorder
(T8↔T8b, multi-sentence drafts: sentence order irrelevant — atoms are a
set); antonym-negation via frozen antonym table
(`{S} is not {ANT(A)}.` → `(Q,S,POS,HAS_PROPERTY,A)`;
antonyms: happy/unhappy, alive/dead, full/empty, hot/cold, big/small,
clean/dirty, loud/quiet, fast/slow, bright/dark, hard/soft);
numeric re-expression via frozen number table
(half↔`1/2`, "50%"↔`1/2`, quarter↔`1/4`, "25%"↔`1/4`,
"three quarters"↔`3/4`, "75%"↔`3/4`, three↔`3`, etc.).

### 1.4 Narrow prover (separate frozen module)

Evidence partition: **EXT store entries only.** GEN entries are invisible
to the kernel (see §6). For each canonical atom A, fixed kernel, depth cap
3 (rule applications along any derivation chain), breadth bounded by store
size (≤128 entries):

- K1 EXACT: A exactly matches an EXT entry → ENTAILED.
- K2 ISA-CHAIN: `(Q,x,POS,IS_A,y)` + `(Q2,y,POS,IS_A,z)` ⊢ `(Q,x,POS,IS_A,z)`.
- K3 LOCIN-TRANS: `(x,POS,LOC_IN,y)` + `(y,POS,LOC_IN,z)` ⊢ `(x,POS,LOC_IN,z)`
  (Q from first premise).
- K4 SIB-SYM: `(x,POS,SIBLING_OF,y)` ⊢ `(y,POS,SIBLING_OF,x)`.
- K5 ALL2SOME: `(ALL,x,POL,R,y)` ⊢ `(SOME,x,POL,R,y)`.
- K6 NEG-DUAL: if ⊢`(Q,x,POS,R,y)` then `(Q,x,NEG,R,y)` is CONTRADICTED and
  vice versa.
- K7 MUTEX-INTRO (declared, frozen): M1 `(POS,LOC_ON)` vs `(POS,LOC_UNDER)`
  same (S,O); M2 `(POS,HAS_PROPERTY,alive)` vs `(POS,HAS_PROPERTY,dead)`
  same S; M3 `(POS,PROP_NUM)` same (S,adj) with differing n. If one side is
  entailed, the other is CONTRADICTED and its NEG is ENTAILED.
- K8 ONLY-BAR: no rule derives `Q=ONLY`; ONLY atoms are entailed only by K1
  exact match (fail-closed on exclusivity claims).

Verdict per atom: **ENTAILED** / **CONTRADICTED** / **UNGROUNDED**.
CONTRADICTED takes precedence on conflict (store assumed consistent).
Diagnostic: if A is entailed using EXT∪GEN but not EXT alone, the verdict is
still UNGROUNDED, annotated `GEN_ONLY` (the recursion made visible).

### 1.5 Deliberation record format (frozen)

```
PREMISES:
Q|S|POL|R|O
...
STEPS:
RULE||in-atom-1||in-atom-2||out-atom
...
CONCLUSIONS:
Q|S|POL|R|O
...
```
Atoms in `Q|S|POL|R|O` form; in STEPS lines fields are `|`-separated with
`||` between atoms (first field = rule name). Rule vocabulary (frozen):
LOOKUP, ISA-CHAIN, LOCIN-TRANS, SIB-SYM, ALL2SOME, MUTEX-INTRO, NEG-DUAL —
same semantics as §1.4.

Frozen validation:
- Every PREMISES atom must exactly match an EXT store entry, else
  `PREMISE_UNGROUND`.
- Every STEP is re-executed: inputs must be in PREMISES or earlier valid
  step outputs; the named rule applied to the inputs must yield exactly the
  out-atom, else `STEP_INVALID` (the step's output is unearned).
- LOOKUP steps: out-atom must exactly match an EXT store entry.

### 1.6 Entitlement cross-check (frozen)

For each draft atom A:
- **EARNED** iff A exactly matches a CONCLUSIONS atom, or A is
  kernel-derivable (K1–K8, depth ≤3) from PREMISES ∪ valid-step-outputs.
- **UNEARNED** otherwise → withhold citing the atom ("unearned assertion").
- **REVISION_FLAG**: A mutex-conflicts (K6/K7 sense) with any CONCLUSIONS
  atom → withhold ("silent revision of the deliberation's own conclusion").

### 1.7 Verdict logic (frozen)

**INSTALL** iff every draft atom is ENTAILED (store path, §1.4) AND EARNED
(trace path, §1.6), with no UNPARSED atoms and no REVISION_FLAG.
Otherwise **WITHHOLD**, with per-atom citations
`atom|STORE_VERDICT|TRACE_VERDICT|rule`.

Output (stdout): line 1 `INSTALL` or `WITHHOLD`; then one line per atom;
stderr: `digest=<sha256hex>` over the LF-joined stdout lines (trailing LF,
cf1 convention).

### 1.8 What is deliberately NOT in the mechanism

No learning, no weights, no thresholds tuned on the corpora, no fuzzy
matching (exact canonical equality only), no RNG anywhere, no wall-clock,
no network. The synonym/antonym/number/alias tables are frozen data,
committed with the build, identical for every run.

## 2. Red-team API (binary + file formats)

Binary `forkD` (pure Zag, pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`), built from
`src/` with `build.py`. `argc` is ignored (znc passes 0); `argv[1]` selects
the mode; missing args → usage on stderr, exit 2.

```
forkD atomize <sentences>              # → canonical atoms, one per line
forkD prove <store> <atoms>            # atoms file Q|S|POL|R|O → per-atom verdicts
forkD verdict <draft> <store> <delib>  # full pipeline (§1.7)
forkD battery <manifest>               # manifest: case|draft|store|delib|expected
                                       # → per-case lines + BAR table; digest on stderr
forkD gen <kind>                       # deterministic fixture generator (§3);
                                       # kinds: store store_h c1 c2 c3 c4 c5 c6 heldout
```

`<sentences>`/`<draft>`: one English sentence per line (§1.3 fragment).
`<store>`: `Q|S|POL|R|O|PROV` per line. `<delib>`: §1.5 format. `<atoms>`:
`Q|S|POL|R|O` per line. `<manifest>`: `case|draft|store|delib|expected`
with `expected` ∈ {INSTALL, WITHHOLD}; case ids prefixed by bar
(`M1-…`, `M2b-…`/`M2f-…` pair members, `M3b-…`/`M3f-…`, `M4-…`, `M5-…`,
`M6-…`, `M7-…`).

The blind red team may craft its own draft/store/delib files in these
formats and run `forkD verdict`. Sentences outside the §1.3 fragment yield
UNPARSED → WITHHOLD (documented fail-closed boundary, see §7).

## 3. Corpora (frozen construction rules; fixtures byte-committed)

All corpora are generated by the frozen deterministic Zag generator
(`forkD gen`), from pinned base fixtures, by fixed rules. No RNG, no
hand-editing after generation. Labels are pinned in the manifest.

Base fixtures: `store` (main): 72 EXT + 25 GEN canonical atoms over 12
domains (animals, geography, objects, family, time, parts, causation,
measures, properties, food, tools, weather). `store_h` (held-out): same
shape, disjoint entity stock (forest/water domains), 60 EXT + 20 GEN.

Battery-construction rules (binding on the self-test; the blind red team
designs its own):

- **C1 (M1, confab catch), 140 drafts, expected WITHHOLD:** base true atoms
  (store-entailed) transformed by flip rules F1–F6 (antonym, quantifier
  swap, digit perturb, entity swap, negation insertion, relation swap
  on↔under), then rendered through a paraphrase rule (P1–P5) so the flip
  hides inside shape variation. Label-validity filter: the generator
  re-proves each candidate atom with the §1.4 kernel; candidates that come
  back ENTAILED are dropped (they are accidentally true, not
  confabulations). This filter fixes labels, not the checker — the checker
  still has to recover the flipped atom from the sentence through the
  atomizer, which is the non-trivial path.
- **C2 (M6, denial-of-truth), 140 drafts, expected INSTALL:** 100 direct
  paraphrases (P1–P5) of store-entailed atoms; 40 true-but-surprising:
  2-hop ISA conclusions, LOC_IN transitivity conclusions, SIBLING_OF
  symmetry conclusions, ALL→SOME weakenings, mutex-derived negatives
  ("the cat is not dead" from `(cat,HAS_PROPERTY,alive)`), each rendered
  in varied templates. Every draft ships with a delib record whose
  PREMISES/STEPS/CONCLUSIONS validly derive it (§1.5–1.6).
- **C3 (M2/M3, paraphrase battery), 130 pairs:** 65 same-meaning/
  different-shape (13 each: P1 synonym, P2 active↔passive, P3 clause
  reorder incl. T8↔T8b, P4 antonym-negation, P5 numeric re-expression);
  65 same-shape/different-meaning: F1 antonym ×11, F2 quantifier ×11,
  F3 digit ×11, F4 entity ×11, F5 negation ×11, F6 relation ×10 —
  all with ≥90% token overlap with the base; plus meaning-flip-preserving-
  shape specials inside F5/F2 (negation-scope moves T13 "not all" vs
  "all … not", "only" placement → ONLY atoms). Construction constraint:
  the base atom is store-ENTAILED (so the pair discriminates: INSTALL vs
  WITHHOLD). M2 = fraction of pairs with divergent final verdicts;
  M3 = fraction with identical final verdicts.
- **C4 (M4, trace alibi), 60 drafts, expected WITHHOLD:** confabulated
  drafts (as C1) each paired with a SELF-CONSISTENT generator-authored
  deliberation record attesting them: quoted premises that are real EXT
  entries but do not entail the conclusion, and STEPS with fabricated rule
  applications (mismatched middle terms, LOOKUP of non-entries). The
  checker must trip on the store path (premisses/entries re-opened in the
  committed store) and/or STEP_INVALID — never on the trace's say-so.
- **C5 (M5, recursive alibi), 60 drafts, expected WITHHOLD:** confabulated
  drafts whose atoms are entailed ONLY via GEN-provenance entries
  (harness-planted "prior episode" support), 20 of them via mixed
  EXT+GEN derivations (still excluded — proofs must be EXT-pure).
  Expected verdict UNGROUNDED/GEN_ONLY → WITHHOLD.
- **C6 (smuggle / silent revision), 40 drafts, expected WITHHOLD:**
  15 append-true-but-undeliberated (draft adds a store-true atom missing
  from CONCLUSIONS → UNEARNED); 15 strengthen (SOME→ALL, `1/2`→`3/4`)
  → UNEARNED (kernel has no strengthening rule); 10 silently negate a
  conclusion → REVISION_FLAG.
- **C7 (M7, held-out):** same generator, `store_h` fixtures, ~50% sizes
  (70/70/65 pairs/30/30/20). Generated and committed alongside C1–C6 but
  **not opened during development**: the build is debugged against C1–C6
  only; C7 is run once for the M7 score. (Self-test protocol; the blind
  red team is the true held-out.)

Deliberation records: every draft ships with one. C1/C4/C5 records attest
the draft (conclusions = draft atoms; premises = mis-cited or GEN entries
as specified). C2 records validly derive the draft. C6 records derive the
base but not the smuggled/strengthened/negated atom.

## 4. Kill bars (from the program prereg, with exact scoring)

Run via `forkD battery <manifest>`; scoring by deterministic Python glue
over the per-case lines (analysis only — the mechanism, battery, and
verification are pure Zag).

- **M1** — confabulation catch: ≥70% of C1 verdicts = WITHHOLD.
- **M2** — meaning-flip divergence: ≥90% of C3 flip pairs divergent.
- **M3** — paraphrase stability: ≥95% of C3 paraphrase pairs identical.
- **M4** — trace-alibi rejection: ≥70% of C4 verdicts = WITHHOLD.
- **M5** — generator-authored-entry rejection: ≥70% of C5 = WITHHOLD.
- **M6** — denial-of-truth: ≤5% of C2 verdicts = WITHHOLD (false withhold).
- **M7** — held-out: M1–M6 bars recomputed on C7; all hold.

Kill rule (program prereg, binding): fail M1/M2/M6 → fork D dead outright.
Fail M4/M5 with M1–M3 passing → theater signature → documented as theater,
not survived. (Fork D makes no corroboration claim, so the "corroboration
claim is dead" clause is vacuous; the outright-death and theater clauses
apply.)

## 5. Determinism plan

- Zero RNG in any decision path: no RNG identifiers in any `.zag` source
  (grep audit: `rand`, `rng`, `seed`, `clock`, `time(`, `getrandom`);
  thincert no-RNG certifier pass attempted on the final build; replay check:
  full battery run twice, outputs byte-compared (sha256).
- Fixed iteration orders everywhere (tables in source order, store in file
  order); no hash maps, no pointer-derived ordering.
- Digest: sha256 over LF-joined stdout verdict lines (trailing LF), hex on
  stderr — the cf1 convention. Any nondeterminism changes the digest.
- Fixtures: generator output committed byte-identical; battery reads the
  committed files. Rerun procedure: `run_battery.sh` runs `forkD battery`
  twice into `run1.out`/`run2.out`, diffs, prints both digests.

## 6. Provenance policy (the write-once stand-in, declared)

The program prereg records the write-once evidence partition as a
follow-up direction, not built in this round. Fork D does not build it.
What fork D does: its prover's evidence partition is the EXT-marked
subset of the committed store, and its premise validation accepts only
EXT-marked entries. The EXT/GEN marks are **harness-pinned ground truth**
(§3), exactly like the draft labels — data, not function. Consequence,
stated plainly: fork D's M5 result is a property of (fork D + pinned
provenance). Without faithful provenance infrastructure, the recursion
(generator-authored entries as older alibis) is unanswerable by any
re-derivation discipline — Muse-B's §3(b) stands. If the blind red team
disputes the marks, that dispute belongs to the follow-up direction, and
fork D's M5 pass is annotated accordingly, not silently banked.

## 7. Known limitations (fail-closed boundaries)

1. **Fragment boundary** (§1.3): sentences outside the templates →
   UNPARSED → WITHHOLD. On a red-team M6 corpus written in free English
   this taxes truth; the boundary is documented, not hidden.
2. **ONLY is fail-closed** (K8): exclusivity claims install only on exact
   store match.
3. **Depth cap 3**: truths needing longer chains withhold (none in the
   corpora by construction).
4. **No fuzzy matching**: a paraphrase the alias table misses withholds.
5. **Consistent-false stores**: a store that consistently endorses a
   falsehood installs it — discipline checks derivation, not truth.
   (This is the honest limit of the identity, not a bug.)

## 8. Build & commit discipline

- Pure Zag mechanisms/battery/verification; Python only for glue/analysis.
- Build: `src/build.py` with the pinned znc; sources import the pinned
  substrate copies vendored in `src/substrate/`.
- Commits to `tnn-native-lab` via `~/workspace/commit_racefree.py`
  (TMPDIR=~/workspace/tmp_commit; message files under
  ~/workspace/tmp_commit, never /tmp). Lab-relative paths under
  `senses/pam-rebuild/selfpam/r2/forkD/`; never commit binaries or
  `.zagd` caches; respect the znc quirk ledger (`~/AGENTS.md`,
  `~/workspace/AGENTS.md`).
- Commit sequence: (1) this prereg ALONE; (2) build sources + frozen
  fixtures + battery evidence + verdict report.
