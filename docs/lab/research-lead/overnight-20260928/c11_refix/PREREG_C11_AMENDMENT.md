# PREREG Amendment: C11 OPACITY (amended bar for future lanes)

**Lane:** c11_refix | **Worker:** C11-REFIX | **Date:** 2026-10-03 (PDT)
**Type:** prereg-only amendment. No code, no re-scoring, no re-freeze of any
prior lane.
**Status:** DRAFT until committed alone (this file only) before any lane
adopts it; the adoption commit is the freeze.

## 0. Non-retroactivity (frozen)

This amendment does NOT change, re-score, weaken, or re-freeze GEN-REDIM
(C434) or any other prior lane. The standing record is unchanged:

- C434's recorded verdict (PASS, exploratory) stands as recorded.
- OPACITY-ERE's (C450) audit-record correction stands: C434's C11 as frozen
  is **not scorable** -- the bar text ("PASS iff grep returns empty", no
  definitional-list exception) is literally unsatisfiable, and the recorded
  PASS rested on a vacuous BRE grep.
- The amended bar below applies to **future lanes only**. A future lane may
  adopt it only by naming it ("C11-amended") in its own frozen prereg.

## 1. Background

GEN-REDIM (C434) Section 4 froze an opacity discipline with this banned-token
list (15 tokens):

hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|
language|audio|interven|belie|goal|agent

Section 8 froze C11 as:

> C11 OPACITY: PASS iff grep over all built sources (rbase.zag, rgen.zag,
> rd_dmain.zag, rd_gmain.zag, rd_smain.zag), PREREG.md and REPORT.md for the
> Section 4 banned tokens (case-insensitive) returns empty, and every
> exercised identifier is a bare integer.

OPACITY-ERE (C450, 2026-10-03, genuine ERE re-audit) found:

1. The coded audit (`build.sh` Step 4) used bare `grep -in "a|b|..."` (BRE),
   where `|` is a literal pipe character. The pattern could only match a line
   containing the entire literal 15-token string on one line; the definitional
   list is wrapped across two lines, so the audit was **guaranteed empty
   before any exclusion ran**. The recorded C11 PASS was produced by an
   instrument that could never fire.
2. Under genuine ERE (`grep -Ein`), the audited file set yields 3 raw hits:
   - `rgen.zag:12: // no domain handlers, no diamond-specific code.` --
     a REAL hit (token `domain` in a built-source comment), inherited
     verbatim from the digest-pinned frozen reference `ref_rd_gen.zag:12`
     (pinned by sha256 before construction; C10's minimal-diff audit
     requires the comment to carry over). The comment *asserts the absence*
     of domain semantics; it attaches no task semantics to any identifier.
   - `PREREG.md:110-111` -- the prereg's own Section 4 definitional
     token-list lines.
3. The frozen bar text contains **no definitional-list exception**; the
   exception lived only in `build.sh` Step 4's exclusion regex and in
   REPORT.md's audit row. Under the literal frozen text, even the prereg's
   own definitional lines are hits, so the bar is self-defeating as written.
4. No ruling exists on inherited frozen-reference lines vs.
   researcher-authored lines.

## 2. Defects in C434's C11 (enumerated, for the record)

- **D1. Vacuous instrument.** BRE grep with unescaped `|` alternation cannot
  match any single token. Any future opacity audit MUST use ERE
  (`grep -Ein`) and MUST prove it can fire (positive control, Section 5).
- **D2. Missing definitional-list exception in the frozen bar text.** The
  exception existed only in build tooling and the report record, never in
  the bar that governed the verdict.
- **D3. No inherited-line ruling.** A worker that faithfully preserves a
  digest-pinned frozen reference (as C10 requires) inherits its comments.
  Penalizing the lane for a pinned comment makes the bar unsatisfiable for
  any faithful successor; ignoring it silently hides real hits. A ruling is
  required (Section 4).
- **D4. Report-quoting hazard.** Disclosing a hit by quoting it in REPORT.md
  would itself be a hit under the literal bar. The amended bar specifies how
  hits are cited without quoting (Section 4).

## 3. Amended frozen bar text (verbatim; copy into adopting preregs)

> **C11 OPACITY (amended):** PASS iff ALL of (a)-(e) hold.
>
> (a) **Genuine-ERE audit.** `grep -Ein "<TOKEN_ALTERNATION>"`
> (case-insensitive, extended regex) over the prereg-enumerated audited file
> set (built sources, the prereg, and the report) returns no hits except as
> allowed by (b) and (c). Bare `grep -in` with `|` alternation (BRE) is
> forbidden; it is vacuous.
>
> (b) **Definitional-list exception.** Hits are excepted ONLY on the
> definitional token-list lines designated in the prereg's naming section:
> lines whose content is nothing but banned tokens joined by `|`. The prereg
> must present the list on such dedicated lines and must not mention banned
> tokens anywhere else in prose. A bare-token line appearing in a BUILT
> SOURCE is never excepted (built sources must not contain the list at all).
>
> (c) **Inherited-line ruling.** Lines present VERBATIM in a digest-pinned
> frozen reference file (digest pinned before this lane's freeze) are not
> this lane's authored lines. A banned-token hit in such a line does not
> fail C11, but MUST be disclosed in REPORT.md with provenance (file, line,
> pinning digest) and a classification: ABSENCE-ASSERTING (the line asserts
> the absence of the banned concept, e.g. "// no domain handlers, no
> diamond-specific code.") or SEMANTICS-CARRYING. Absence-asserting hits are
> recorded and do not affect the verdict. Semantics-carrying hits in
> inherited lines are escalated to the research lead for a ruling on the
> frozen reference; the lane records PASS-WITH-DISCLOSURE and the reference
> is flagged for its own erratum. Hits are cited by file:line and token
> INDEX in the token list (e.g. "token #4"), never quoted verbatim in the
> report (quoting would itself be a hit under (a)). Any line the lane
> ADDED or MODIFIED relative to the pinned reference is researcher-authored:
> a hit there fails C11 with no exception.
>
> (d) **Identifier discipline.** Every exercised identifier in the built
> sources is a bare integer or an opaque handle of the prereg's declared
> opaque scheme (e.g. structures m0..m7, bare-integer relations/entities);
> no identifier carries human task semantics. REPORT records the identifier
> census observed in the built sources.
>
> (e) **Positive control.** The build script must prove the instrument can
> fire: run the exact audit pipeline (including the definitional exclusion)
> against a synthetic prose line containing a banned token and require a
> reported hit. If the positive control fails, the audit instrument is
> broken and the lane is VOID (re-freeze required; a broken instrument
> cannot establish the bar).

**Token list (frozen; 15 tokens, order fixed for index citation):**

hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|
language|audio|interven|belie|goal|agent

Token indices: 1=hypothesis, 2=refine, 3=evaluat, 4=domain, 5=plan,
6=causal, 7=navigat, 8=arithmet, 9=grammar, 10=language, 11=audio,
12=interven, 13=belie, 14=goal, 15=agent.

**Kill mapping (frozen):** C11-amended FAIL -> BUILD-FAIL (the lane broke
naming discipline). Positive-control failure -> VOID (instrument broken;
re-freeze; never salvage by re-running the same broken audit).

## 4. Rulings (binding on adopting lanes)

**R1. Definitional exception is part of the bar, not the tooling.** An
exception that lives only in `build.sh` or in REPORT.md does not exist for
verdict purposes. The bar text in Section 3 is the complete criterion.

**R2. Inherited comments.** A banned-token hit in a line inherited verbatim
from a digest-pinned frozen reference is a property OF THE REFERENCE, not of
this lane's naming discipline, and cannot fail this lane's C11 -- because
the lane cannot remove or edit the line without violating minimal-diff, so
penalizing it would make the bar unsatisfiable for every faithful successor
(exactly C434's situation). Mandatory disclosure (provenance +
absence-asserting vs semantics-carrying classification) keeps the discipline
honest instead of silent. Absence-asserting comments (the C434 case: token #4
in `// no domain handlers, no diamond-specific code.`, pinned in
`ref_rd_gen.zag:12`) are the expected benign form; they assert the very
absence the discipline requires.

**R3. Researcher-authored lines are strictly liable.** Any added or modified
line containing a banned token fails C11. There is no "it was just a
comment" exception for lane-authored text: if the lane wrote it, the lane
owns it.

**R4. Report hygiene.** REPORT.md must not quote banned tokens verbatim.
Hits are cited as file:line + token index + classification. The prereg's
definitional lines are the only permitted verbatim occurrence of the tokens
in lane documents.

**R5. Scope is enumerated, not implied.** The adopting prereg must list the
exact audited files. Derived or auxiliary built sources (e.g.
`rgen_nomain.zag`-style assemblies) must be either listed in the audited set
or explicitly excluded with justification; exclusion without justification
is a prereg defect.

## 5. Genuine audit form (frozen spec for the build script)

The build script MUST implement all of the following, fail-closed
(`set -e` or equivalent):

```sh
# 1. ERE audit over the prereg-enumerated file set (case-insensitive).
TOKENS="hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent"
HITS=$(grep -Ein "$TOKENS" <built sources...> PREREG.md REPORT.md 2>/dev/null \
  | grep -v "^PREREG.md:[0-9]*:[a-z|]*$" || true)
# The exclusion above is anchored to the prereg AND to bare-token-line
# content. It must NOT be a bare content pattern applied to all files:
# a definitional-looking line in a built source is a hit, not an exception.

# 2. Positive control: the instrument must fire on a genuine prose hit,
# through the same pipeline including the exclusion.
CTL=$(printf 'x.zag:1:// domain handler stub\n' \
  | grep -v "^PREREG.md:[0-9]*:[a-z|]*$" | grep -Ein "$TOKENS" || true)
[ -n "$CTL" ] || { echo "C11 VOID: positive control failed; audit instrument broken"; exit 1; }

# 3. Verdict.
if [ -n "$HITS" ]; then
  echo "C11 FAIL: banned-token hits:"; echo "$HITS"; exit 1
fi
echo "C11 PASS (amended): no banned-token hits outside the definitional list."
```

Notes:
- `<built sources...>` is replaced by the prereg's enumerated list (R5).
- If the lane has digest-pinned frozen references, Step 3's failure output
  is triaged per ruling R2/R3: verbatim-inherited hits go to REPORT.md
  disclosure (PASS-WITH-DISCLOSURE for absence-asserting), researcher-authored
  hits are BUILD-FAIL. The triage compares hit lines against the pinned
  reference files (exact line match); anything not verbatim-inherited is
  researcher-authored.
- The positive control pins the two historical failure modes shut: BRE
  vacuity (D1 -- an unescaped-`|` grep fails the control) and
  over-broad exclusion (the old bare-content regex is replaced by the
  prereg-anchored form, and the control proves prose hits survive it).

## 6. What this amendment changes vs. C434's C11

| Aspect | C434 (frozen) | C11-amended |
|---|---|---|
| Regex flavor | unspecified (coded as BRE, vacuous) | ERE mandatory (`grep -Ein`); BRE forbidden |
| Definitional exception | only in build.sh/REPORT.md | in the frozen bar text (R1) |
| Inherited reference lines | unruled | excepted with mandatory disclosure + classification (R2) |
| Researcher-authored hits | fail (implied) | fail, strictly liable incl. comments (R3) |
| Report quoting of hits | unruled (quoting = new hit) | file:line + token index, never verbatim (R4) |
| Audited file set | listed | must be enumerated; derived sources listed or explicitly excluded (R5) |
| Positive control | none | mandatory; failure -> VOID |
| Identifier clause | "every exercised identifier is a bare integer" | kept; REPORT records the census |

## 7. Adoption instructions

A future lane adopts this amendment by writing in its prereg: "C11:
C11-amended (c11_refix/PREREG_C11_AMENDMENT.md, frozen <commit>), audited
files: <list>." The lane's build script implements Section 5 verbatim with
its file list substituted. The amendment's own freeze is the commit that
carries this file alone before any adoption.

## 8. Record status

- Analysis-only task (C11-REFIX); no code written or changed.
- Sources read: `opacity_ere/OPACITY_ERE_AUDIT.md` (C450),
  `gen_redim/PREREG.md` (C434) Sections 4 and 8,
  `gen_redim/build.sh` Step 4, `gen_redim/REPORT.md` C11 row,
  `gen_redim/ref_rd_gen.zag:12` and `gen_redim/rgen.zag:12`.
- Open for the research lead: whether any currently-frozen reference file
  carrying a banned token in an inherited comment (known case:
  `ref_rd_gen.zag:12`, token #4, absence-asserting) should receive its own
  reference erratum, or whether R2 disclosure at each adopting lane is
  sufficient. This amendment does not decide that; it only requires the
  disclosure.
