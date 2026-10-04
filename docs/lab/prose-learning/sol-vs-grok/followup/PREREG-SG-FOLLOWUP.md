# PREREG-SG-FOLLOWUP — Sol-vs-Grok follow-ups (FROZEN 2026-09-22)

Follow-up package to the Sol-vs-Grok duel (PREREG-SG.md, frozen; duel commit
`e18a2ca135899be69c3e35497fb737124e50b78f`; VERDICT.md: SCENARIO-FIT, no
champion). Implements the three future bars the duel verdict named:
(a) verify-direction hybrid, (b) coref-visible lexical retrieval,
(c) polarity/subject gates. Plus the fresh-sealed-battery generalization check.

## F0. Status

- **FROZEN 2026-09-22.** Builds frozen against `followup/gen/calib` battery
  only (visible, calib-config vocabulary). Amends only by bump + rebuild +
  full rerun, like the duel §8.
- The duel prereg §8 rules apply in full: 5 byte-identical runs, pure Zag,
  zero RNG, proof files, kill bars decide.
- No builder sees the followup SEALED battery (`followup/gen/followup/`),
  its expected values, or its frames before scoring. The followup config
  (`followup/gen/cfg_followup.py`) is visible from this prereg onward (same
  standing as the calib config); the discipline is no build iteration after
  the sealed battery is generated — one shot, scored once.

## F1. Builds (all pure Zag, zero RNG)

All four live in `followup/src/`, share the frozen `sg_parse.zag` parser
unchanged (same file as the duel; the duel's build process already copies
parser + analyzer + compiler from the duel dir — copy once, never edited).

- `sg_verify.zag` — (a) VERIFY-DIRECTION HYBRID: Grok proposes, verifier gates.
- `sg_coref1.zag` — (b1) COREF-LEX: resolved-entity token appended to row lex.
- `sg_coref2.zag` — (b2) COREF-SIM: separate resolved-entity agreement term.
- `sg_gated.zag` — (c) GATED GROK: polarity/subject gates inside the fallback.

Each binary: `argv[1]=teach argv[2]=probe` → verdict lines on stdout,
proof lines to a build-named proof file in CWD
(`proof_verify.txt`, `proof_coref1.txt`, `proof_coref2.txt`, `proof_gated.txt`).
Byte-identical proof SHA256 across 5 runs required (duel §8).

## F2. Mechanism (a): verify-direction hybrid — `sg_verify.zag`

Grok's retrieval runs exactly as in `sg_grok.zag` (exact skeleton path, then
BoW fallback at cosine ≥ 1/4, install-order tie-break). The verifier gates
only the FALLBACK proposal; exact-path proposals pass through unchanged.

Verifier checks on a fallback proposal W for probe (pred P, subject S, both
known — the battery never has unknown probe subjects):

1. **Attestation veto.** Let A = "∄ live pol=0 row with pred == P, subj == S".
   Let H = "∃ row (live or dead) with subj == S, pol != 0, pred ⊇ P".
   If A ∧ H → verdict UNKNOWN (veto=attestation). Rationale: the probed
   (relation, entity) was only ever hedged/negated; no asserted value exists
   to return. (The parser keeps polarity markers inside the relation stem set,
   so a negated teach row's pred is the probe's pred ∪ {marker} — hence ⊇.)
2. **Subject veto.** If W.subj != S → verdict UNKNOWN (veto=subject).
   Rationale: Grok's fallback has no subject gate; returning another entity's
   value is confabulation.
3. **Tie veto.** Re-scan: if any other fallback candidate has score exactly
   equal to W's score (rational equality i2a·prodb == i2b·proda) AND a
   different value → verdict UNKNOWN (veto=tie). Rationale: Grok's 4 typo
   wrong-values came from install-order tie-breaks among equidistant
   candidates; a verifier must not ratify a guess. Ties among candidates
   agreeing on the value do NOT trigger the veto (no guessing involved).
4. Otherwise → W's verdict unchanged.

Proof line: `VERIFY path=<exact|fallback> veto=<none|attestation|subject|tie>
cand=<idx> verdict=<V>`.

Bars (measured on the SEALED followup battery, relative to the two frozen
duel binaries re-run on that same battery):
- **HYBRID CHAMPION** (verdict changes): SG-PARA(verify) ≥ SG-PARA(grok) − 0.01
  AND SG-WRONG(verify) ≤ 0.05.
- If SG-WRONG ≤ 0.05 but PARA misses the −0.01 bar → "safe but narrower"
  (scenario-fit stands; verifier costs paraphrase).
- If SG-WRONG > 0.05 → FAIL (verification insufficient).

## F3. Mechanism (b): coref-visible lexical retrieval

Duel facts: neither Sol nor Grok does coreference (SG-COMP Sol 0.0000,
Grok 0.1667 — the 4 Grok got right were install-order tie wins on the
correct entity, not coref). The `multi` slice is answerable only via
coreference-mediated retrieval: teach line
`The {ra} of "{e}" is {v1}. It has a {mra} of {v2}.`
probed as `What is the {mra} of "{e}"?`
The probe names the entity; the teach row for the {mra} relation has no
lexical trace of the entity (its sentence used "It").

Two arms test the two designs the duel verdict named:

**(b1) `sg_coref1.zag` — entity token in row lex.**
At teach time, when coreference actually fired for a sentence (parser
`sctx[48] == 1`), append the resolved entity's stem uids (`entstem[0..ent_n)`)
to the row's lexical set before install (re-sort/dedup; lex set grows by ≤
ent_n uids). Nothing else changes: same exact path, same BoW fallback,
same tie-break. Probe lex is unchanged (it names the entity).

**(b2) `sg_coref2.zag` — separate entity-similarity term.**
Lex sets unchanged. In `bow_best`, rank candidates by the augmented key
`(4·i2 + prod·subj_bonus, prod)` where subj_bonus = 1 iff
row.subj == probe.subj (both known) else 0 — i.e. a +1/4 cosine-unit bonus
for resolved-entity agreement. The ≥ 1/4 hit threshold applies to the
UNBONUSED score (lexical evidence alone must clear the bar; the bonus only
re-ranks). Install-order tie-break retained.

Bars (sealed battery, vs frozen Grok re-run on the same battery):
- Coref capability: SG-COMP ≥ 20/24 for a variant to count as "coref-visible"
  (the duel verdict's named threshold).
- No regression: SG-WRONG ≤ SG-WRONG(grok) AND SG-PARA ≥ SG-PARA(grok) − 0.03.
- (b) is DIAGNOSTIC-ONLY per the duel prereg — it cannot change the
  scenario-fit verdict; it reports whether the "neither does coref" cell is
  repaired.

## F4. Mechanism (c): polarity/subject gates — `sg_gated.zag`

Grok's fallback with the gates INSIDE the candidate loop:

1. **Attestation gate (preempt).** Same A ∧ H rule as (a) step 1, applied
   before fallback: if the probed (relation, entity) was never asserted and
   only hedged/negated → UNKNOWN.
2. **Subject gate.** Fallback candidates with subj != probe.subj are excluded
   from the pool (not merely vetoed after). If no candidate remains →
   UNKNOWN.
3. BoW ≥ 1/4 threshold, best-score wins, lowest-install-index tie-break
   RETAINED (tests whether the gates alone fix the typo ties — the tied wrong
   candidates were largely cross-entity).

Exact path unchanged. Proof: `GATED path=<exact|fallback> gate=<none|
attestation|subject> cand=<idx> verdict=<V>`.

Bars (sealed battery, vs frozen binaries re-run on it):
- **Champion eligibility**: SG-PARA(gated) ≥ SG-PARA(grok) − 0.03
  AND SG-WRONG(gated) ≤ 0.05 AND SG-SAFE(gated) ≥ 0.90.
- **CHAMPION = gated Grok** (scenario-fit verdict CHANGES): eligible AND
  SG-PARA(gated) − SG-PARA(sol) ≥ 0.03 (the duel's meaningful margin).
- If WRONG ≤ 0.05 but PARA < grok − 0.03 → "safe but narrow" (report).
- If WRONG > 0.05 → gates insufficient (FAIL).

## F5. Sealed followup battery — `followup/gen/cfg_followup.py`

Fresh battery, same generator (`gen/battery.py` + `gen/expected.py` +
`gen/score_sg.py` unchanged), NEW vocabulary disjoint from calib AND scored
(see §F5.1 word lists; builders do not inspect the generated battery).
Structure identical: 384 teach lines, 432 probes, same slices and ids.
Generated AFTER build freeze (commit C). Validated with `check_sg.py`
(0 failures required) before scoring.

**F5.1 — frozen word lists (celestial theme).**
- relations (12 pairs): ("star magnitude","stellar brightness"),
  ("moon phase","lunar cycle"), ("comet tail","comet train"),
  ("orbit period","revolution time"), ("planet mass","planetary weight"),
  ("nebula span","cloud expanse"), ("eclipse hour","occultation time"),
  ("tide height","tidal rise"), ("aurora glow","polar light"),
  ("crater depth","basin depth"), ("solar flare","sun eruption"),
  ("galaxy tally","star count")
- ent_main: Zephyria Quillon Vespera Lumina Noctua Aurelia Stellia Astrala
- ent_neg: Duskwatch Grimhold Murkfell Shadewick Nightfall Darkmere Sableport Ebonwick
- ent_hedge: Quibble Waverly Hazemere Mistmere Dithera Vacilla Fluctua Wobblia
- ent_contr: Feudwick Clashmere Rivalwick Joustmere Contenda Oppugna Adversa Contraria
- ent_distr: Wispmere Phantomwick Specterwick Apparia Ghostmere Shademere Ectowick Polterwick
- distr_rels: ["satellite name","telescope lens","rocket fuel"]
- multi_rels: [("quasar flare","quasar outburst"),("pulsar beat","pulsar rhythm"),
  ("meteor streak","meteor trail"),("ring system","annular band")]
- value_params: (13, 47, 31, 420, 1810, 190); year_rel: 4; contr_delta: 19;
  multi_v0: 800; multi_dv: 13

## F6. Run protocol

1. Build all four + rebuild frozen `sg_sol`/`sg_grok` from the duel's frozen
   sources; calibrate each against `followup/gen/calib` (expected: Sol
   SG-PARA≈0.50, Grok SG-PARA≈0.98, both ≥ their duel metrics).
2. Freeze builds (commit B). Generate sealed battery (commit C), validate
   with check_sg.py (0 failures).
3. 5 runs each of all six binaries on the sealed battery; SHA256 of stdout
   and of proof files; all five byte-identical required.
4. Score with `gen/score_sg.py` (frozen) → SG-PARA/SAFE/PREC/COMP/WRONG per
   build; compare to bars.
5. Verdict (commit D): `followup/VERDICT-SG-FOLLOWUP.md` — per-build table,
   per-bar PASS/FAIL, and the answer to the package question: does any
   result change the original SCENARIO-FIT, no-champion verdict?

## F7. Kill bars (apply to all four builds)

- KB-F-DET: any of the 5 runs differs (stdout or proof SHA256) → FAIL.
- KB-F-PROOF: proof line count != 432 probe verdict lines → FAIL.
- KB-F-TOOL: any toolchain/compiler warning treated as error → FAIL
  (the duel's analyzer warning is a known benign indexing note; only NEW
  warnings fail).
- KB-F-CACHE: no `.zagd`/binaries committed, ever.

## F8. What success/failure means for the package

The package question is whether any follow-up changes the duel's
SCENARIO-FIT, no-champion verdict:
- (a) or (c) meeting its champion bar → verdict CHANGES (name the champion).
- All failing → verdict STANDS, with the measured numbers explaining why
  (e.g. verifier buys safety at a paraphrase cost; gates fix X of Y
  wrong-values).
- (b) reports the coref cell regardless; it cannot change the verdict.

**FROZEN 2026-09-22.**
