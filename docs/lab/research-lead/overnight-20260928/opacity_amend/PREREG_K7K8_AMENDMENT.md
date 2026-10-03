# PREREG Amendment: gen_generality K7 and gen_stress K8 OPAQUE-NAMING (amended bars for future lanes)

**Lanes:** gen_generality (K7), gen_stress (K8) | **Worker:** OPACITY-AMEND-RETRY | **Date:** 2026-10-03 (PDT)
**Type:** prereg-only amendment. No code, no re-scoring, no re-freeze of any prior lane.
**Status:** DRAFT until committed alone (this file only) before any lane adopts it; the adoption commit is the freeze.

## 0. Non-retroactivity (frozen)

This amendment does NOT change, re-score, weaken, or re-freeze gen_generality (K7) or gen_stress (K8) or any other prior lane. The standing record is unchanged:

- The recorded verdicts of the gen_generality and gen_stress lanes stand as recorded.
- OPACITY-SWEEP's (C462) audit-record correction stands: under a genuine ERE audit, the REPORT prose carve-outs in both lanes understate the true hit sets (K7: REPORT claims the matches are "only" the byline and Section 3 rule-definition lines, but genuine ERE finds 15 hit lines in the bar's scope; K8: REPORT claims the matches are "only the document bylines", but genuine ERE finds 10 hit lines). All hits fall into benign meta-text classes; no hit violates the intent of either bar. The frozen bar texts, as literally written ("finds zero banned-vocabulary tokens"), are unsatisfiable as stated, because a prereg must define the banned class in prose and the documents carry bylines.
- The amended bars below apply to **future lanes only**. A future lane may adopt one of them only by naming it ("K7-amended" or "K8-amended") in its own frozen prereg.

## 1. Background

OPACITY-ERE (C450) demonstrated that a banned-vocabulary audit run as bare `grep -in "a|b|..."` (BRE) is vacuous: without `-E`, `|` is a literal pipe, so the pattern matches only a line containing the entire 15-token literal string, which never occurs, and the audit always reports zero hits.

OPACITY-SWEEP (C462, 2026-10-03) ran the genuine ERE form of the C402 banned-vocabulary pattern

```
grep -Ein 'hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent'
```

over the gen_generality and gen_stress materials and found:

- **gen_generality (bar K7 OPAQUE-NAMING):** genuine ERE over the bar's scope (gg_new.zag, PREREG.md, REPORT.md) yields **15 hit lines** (gg_new.zag: 1; PREREG.md: 9; REPORT.md: 5). The REPORT's "only matches" enumeration omits 7 benign hit lines. Additionally, the REPORT audited gg_new.zag, PREREG.md, **PREREG_AMEND1.md** instead of the bar-scoped gg_new.zag, PREREG.md, **REPORT.md** (PREREG_AMEND1.md is genuinely clean; REPORT.md contains 5 benign hits).
- **gen_stress (bar K8 OPAQUE-NAMING):** genuine ERE over the bar's scope (gs_new.zag, PREREG.md, REPORT.md) yields **10 hit lines**, all benign meta-text (gs_new.zag:3 compliance comment; PREREG.md:94,104,108,110 Section 4 banned-class definition; PREREG.md:551 "Implementation plan" heading; PREREG.md:567 and REPORT.md:207 "AGENTS.md" refs; REPORT.md:3,83 bylines disclosed under the C402 precedent).
- **No domain-story token in any world, setup, driver, or result.** The intent of both bars (domain-blind worlds) holds on the evidence. Every hit falls into one of the five benign classes in Section 4 below.

The REPORT verdicts already carve prose exceptions, but the carve-outs are incomplete and the bar texts contain no exceptions at all. This amendment codifies the exceptions in the bar text and fixes the audited file list, following the C11-REFIX (C456) pattern.

## 2. Defects in the frozen K7 and K8 (enumerated, for the record)

- **D1. Unsatisfiable bar text.** "PASS iff the grep audit finds zero banned-vocabulary tokens in <new source>, PREREG.md, and REPORT.md" cannot be satisfied literally: the prereg must enumerate the banned class in prose (its definitional lines are hits) and the documents carry bylines (hits under the C402 precedent exception). Exceptions lived only in REPORT prose, never in the bar that governed the verdict.
- **D2. No audit-instrument specification.** The frozen bars do not specify ERE (`grep -Ein`). A bare BRE grep with `|` alternation is vacuous and cannot match any single token. Any future opacity audit MUST use ERE and MUST prove it can fire (positive control, Section 5).
- **D3. Incomplete prose carve-outs.** K7's "only matches" enumeration omits 7 benign hit lines (the "Implementation plan" section heading, two AGENTS.md toolchain references, the "evidences domain-blindness" verdict-mapping mention, two compliance assertions, the gg_new.zag compliance comment). K8's "only the document bylines" omits its Section 4 definitional lines, the "Implementation plan" heading, AGENTS.md references, and the gs_new.zag compliance comment.
- **D4. Wrong audit file list for K7.** The REPORT audited PREREG_AMEND1.md in place of the bar-scoped REPORT.md. An amended bar must fix the audited file set to the prereg-enumerated list.
- **D5. Report-quoting hazard.** Disclosing a hit by quoting it in REPORT.md would itself be a hit under the literal bar. The amended bars specify how hits are cited without quoting (Section 4).

## 3. Amended frozen bar texts (verbatim; copy into adopting preregs)

### K7-amended (gen_generality OPAQUE-NAMING)

> **K7 OPAQUE-NAMING (amended):** PASS iff ALL of (a)-(e) hold.
>
> (a) **Genuine-ERE audit.** `grep -Ein "<TOKEN_ALTERNATION>"` (case-insensitive, extended regex) over the prereg-enumerated audited file set (gg_new.zag, PREREG.md, REPORT.md) returns no hits except as allowed by (b). Bare `grep -in` with `|` alternation (BRE) is forbidden; it is vacuous.
>
> (b) **Permitted-exception classes.** Hits are excepted ONLY when they fall in one of the five classes of Section 4: (1) the prereg's own banned-class rule-definition lines, (2) document bylines ("Agent:"/"Worker:", C402 precedent), (3) self-referential compliance assertions ("no domain handlers", "No domain vocabulary anywhere in this file", and equivalent statements asserting the discipline), (4) structural document headings ("Implementation plan" and equivalents) and toolchain references ("AGENTS.md" and equivalents). Class (5) (grandfathered inherited comments) applies only where the prereg explicitly grandfathers a named inherited file. A hit that is a permitted exception MUST be disclosed in REPORT.md with file:line, token index, and class, but does not affect the verdict. Any hit outside these classes fails K7.
>
> (c) **Researcher-authored lines are strictly liable.** Any line this lane authored or modified that carries a domain-story token (a banned token used with task semantics, e.g. a world identifier named by domain) fails K7. There is no "it was just a comment" exception for lane-authored text.
>
> (d) **Report hygiene.** REPORT.md must not quote banned tokens verbatim. Hits are cited as file:line plus token index in the frozen token list plus exception class.
>
> (e) **Positive control.** The build script must prove the instrument can fire: run the exact audit pipeline (including any definitional-line exclusion) against a synthetic prose line containing a banned token and require a reported hit. If the positive control fails, the audit instrument is broken and the lane is VOID (re-freeze required; a broken instrument cannot establish the bar).

### K8-amended (gen_stress OPAQUE-NAMING)

> **K8 OPAQUE-NAMING (amended):** PASS iff ALL of (a)-(e) hold.
>
> (a) **Genuine-ERE audit.** `grep -Ein "<TOKEN_ALTERNATION>"` (case-insensitive, extended regex) over the prereg-enumerated audited file set (gs_new.zag, PREREG.md, REPORT.md) returns no hits except as allowed by (b). Bare `grep -in` with `|` alternation (BRE) is forbidden; it is vacuous.
>
> (b)-(e) **Identical to K7-amended (b)-(e).** The same five permitted-exception classes, the same strict-liability rule for researcher-authored lines, the same report-hygiene rule, and the same positive control apply. The audited file set is (gs_new.zag, PREREG.md, REPORT.md).

**Token list (frozen; 15 tokens, order fixed for index citation):**

hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|
language|audio|interven|belie|goal|agent

Token indices: 1=hypothesis, 2=refine, 3=evaluat, 4=domain, 5=plan, 6=causal, 7=navigat, 8=arithmet, 9=grammar, 10=language, 11=audio, 12=interven, 13=belie, 14=goal, 15=agent.

**Kill mapping (frozen):** K7-amended / K8-amended FAIL -> BUILD-FAIL (the lane broke naming discipline). Positive-control failure -> VOID (instrument broken; re-freeze; never salvage by re-running the same broken audit).

## 4. The five permitted-exception classes (codified from OPACITY-SWEEP C462 Section 4)

1. **The prereg's own banned-class rule definition.** The bar's definitional lines must enumerate examples to be checkable; they are therefore hits under their own rule. Exception covers ONLY dedicated definitional lines (bare banned tokens joined by `|`). The prereg must present the list on such dedicated lines and must not mention banned tokens elsewhere in prose. A bare-token line appearing in a BUILT SOURCE is never excepted; built sources must not contain the list at all.
2. **Document bylines.** Lines of the form "Agent:" / "Worker:" and equivalent attribution bylines. C402-precedent exception.
3. **Self-referential compliance assertions.** Lines that assert the discipline itself, e.g. "no domain handlers", "no domain labels", "No domain vocabulary anywhere in this file", or equivalent statements that deny (not supply) task semantics. These assert the absence the bar requires; they attach no task semantics to any identifier.
4. **Structural document headings and toolchain references.** Section headings such as "Implementation plan" and references to the shared toolchain file "AGENTS.md" (and equivalents). Meta-text about document structure, not design language.
5. **Explicitly grandfathered byte-identical inherited comments.** Lines carried over verbatim from a named inherited file for byte-fidelity, where the prereg explicitly grandfathers them (the gen_statefix/gen_subsumes_u pair5 world-builder comments are the documented precedent: copied for world byte-fidelity, byte-verified identical, and not the experiment's design language). Class 5 applies to a future lane ONLY if that lane's prereg names the inherited file and states the grandfathering; otherwise a hit in such a line is researcher-authored and fails the bar.

## 5. Genuine audit form (frozen spec for the build script)

The build script MUST implement all of the following, fail-closed (`set -e` or equivalent):

```sh
# 1. ERE audit over the prereg-enumerated file set (case-insensitive).
# K7: <new source> = gg_new.zag. K8: <new source> = gs_new.zag.
TOKENS="hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent"
HITS=$(grep -Ein "$TOKENS" <new source> PREREG.md REPORT.md 2>/dev/null \
  | grep -v "^PREREG.md:[0-9]*:[a-z|]*$" || true)
# The exclusion above is anchored to the prereg AND to bare-token-line
# content. It must NOT be a bare content pattern applied to all files:
# a definitional-looking line in a built source is a hit, not an exception.

# 2. Positive control: the instrument must fire on a genuine prose hit,
# through the same pipeline including the exclusion.
CTL=$(printf 'x.zag:1:// domain handler stub\n' \
  | grep -v "^PREREG.md:[0-9]*:[a-z|]*$" | grep -Ein "$TOKENS" || true)
[ -n "$CTL" ] || { echo "K7/K8 VOID: positive control failed; audit instrument broken"; exit 1; }

# 3. Verdict.
if [ -n "$HITS" ]; then
  echo "K7/K8 FAIL: banned-token hits:"; echo "$HITS"; exit 1
fi
echo "K7/K8 PASS (amended): no banned-token hits outside the permitted exceptions."
```

Notes:
- Step 3's failure output is triaged against Section 4: hits in permitted-exception classes go to REPORT.md disclosure (file:line, token index, class) and do not fail the bar; researcher-authored domain-story hits are BUILD-FAIL.
- The positive control pins the two historical failure modes shut: BRE vacuity (an unescaped-`|` grep fails the control) and over-broad exclusion (the control proves prose hits survive the prereg-anchored exclusion).

## 6. What this amendment changes vs. the frozen K7 and K8

| Aspect | Frozen K7/K8 | K7-amended / K8-amended |
|---|---|---|
| Regex flavor | unspecified | ERE mandatory (`grep -Ein`); BRE forbidden |
| Permitted exceptions | only in REPORT prose (incomplete) | codified five classes in the frozen bar text (Section 4) |
| K7 audited file set | bar said gg_new.zag, PREREG.md, REPORT.md; REPORT audited PREREG_AMEND1.md instead | fixed to the bar's enumerated list: gg_new.zag (K7) / gs_new.zag (K8), PREREG.md, REPORT.md |
| Researcher-authored hits | fail (implied) | fail, strictly liable incl. comments |
| Report quoting of hits | unruled (quoting = new hit) | file:line + token index + class, never verbatim |
| Positive control | none | mandatory; failure -> VOID |
| Inherited comments | unruled for these lanes | class 5, only with explicit prereg grandfathering |

## 7. Adoption instructions

A future lane adopts one of these bars by writing in its prereg: "K7: K7-amended (opacity_amend/PREREG_K7K8_AMENDMENT.md, frozen <commit>), audited files: <list>." or "K8: K8-amended (opacity_amend/PREREG_K7K8_AMENDMENT.md, frozen <commit>), audited files: <list>." The lane's build script implements Section 5 verbatim with its file list substituted. The amendment's own freeze is the commit that carries this file alone before any adoption.

## 8. Record status

- Analysis-only task (OPACITY-AMEND-RETRY); no code written or changed.
- Sources read: `opacity_sweep/OPACITY_SWEEP.md` (C462) and `c11_refix/PREREG_C11_AMENDMENT.md` (C456), used as pattern template.
- Delivered to the opacity_amend directory of the tnn-rsi-gpi3 worktree; not committed (coordinator commits).
- Open for the research lead: (1) whether gen_generality's recorded PASS should carry a standing audit-record correction noting that the REPORT audited PREREG_AMEND1.md in place of the bar-scoped REPORT.md (the bar's verdict intent still holds: the 5 REPORT.md hits are all benign class 2-4 meta-text); (2) whether future lanes reusing the pair5 world without explicit grandfathering language should default class 5 off. This amendment defaults it off.
