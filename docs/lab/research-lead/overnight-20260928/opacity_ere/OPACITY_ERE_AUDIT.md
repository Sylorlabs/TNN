# OPACITY-ERE Audit: genuine-ERE re-run of GEN-REDIM C11 and GEN-NM10 N6

**Worker:** OPACITY-ERE | **Date:** 2026-10-03 (PDT) | **Analysis only; no code changed.**

## 1. Background

GEN-POOLFLOOD (C446 PASS) found **O2: the prior opacity audits were vacuous as coded.**
Both lanes' `build.sh` use bare `grep -in "a|b|...|z"` (BRE), where `|` is a literal
pipe character. The pattern can only match a line containing the entire literal
string `hypothesis|refine|...|agent` on one line. The definitional token lists in
both PREREGs are wrapped across two lines, so the audits were guaranteed to return
empty even before the exclusion filter ran. Confirmed by re-execution:

| Lane | Coded (BRE) hits | Genuine (ERE, `grep -Ein`) raw hits |
|---|---|---|
| GEN-REDIM (C11 scope) | **0** | **3** |
| GEN-NM10 (coded scope) | **0** | **2** |
| GEN-NM10 (prereg scope, +REPORT.md) | **0** | **2** |

`grep -Ein "hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent"` on the exact file sets the builds audit.

## 2. GEN-REDIM C11

C11 scope: `rbase.zag, rgen.zag, rd_dmain.zag, rd_gmain.zag, rd_smain.zag, PREREG.md, REPORT.md`.

Genuine-ERE raw hits (3):
1. **`rgen.zag:12: // no domain handlers, no diamond-specific code.`** - REAL HIT.
   The word "domain" (token `domain`) in a comment of a built source.
2. `PREREG.md:110` - the definitional token-list line (first half).
3. `PREREG.md:111` - the definitional token-list line (second half).

Hit (1) is **inherited verbatim from the frozen reference**:
`ref_rd_gen.zag:12` contains the identical comment. `build.sh` Step 1 pins that
file by sha256 digest (`d6f1f9d8f4747293bb7a8e99474660347dc24693f62f3d25caaf1d83c19c9d9a`)
and Step 2 asserts `cmp ref_rd_gen.zag ../gen_stress/ref_gs_gen.zag` (GEN-STRESS
frozen source). C10's minimal-diff audit explicitly allows comment lines in the
added/removed sets, so the comment carries over by construction. The same comment
also propagates into the derived `rgen_nomain.zag` / `gen_nomain.zag` (line 12),
which are outside C11's listed scope but worth noting.

**Assessment:** the hit is a comment *asserting the absence* of domain semantics
("no domain handlers"), not an identifier carrying task semantics. Every exercised
identifier in the built sources remains a bare integer / m0..m7 opaque handle, so
the scientific conclusion of the opacity discipline is unaffected. But C11 as
**frozen cannot literally pass**: the kill-bar text reads "PASS iff grep ...
returns empty" with **no definitional-list exception** (the exception exists only
in `build.sh` Step 4's exclusion regex and in REPORT.md's record of the audit).
Under the literal bar, even PREREG.md's own Section 4 definitional lines are hits,
and the frozen reference file pins a comment containing a banned token. The bar
is self-defeating as written; it needs the exception clause (as N6 has) plus a
ruling on inherited comments, then re-freeze.

**Corrected record:** GEN-REDIM's recorded "C11 OPACITY | PASS" rested on a
vacuous BRE grep. Under genuine ERE the opacity *discipline* holds (one
inherited absence-asserting comment; no semantic identifiers), but the C11
*bar+verdict as frozen* is defective and cannot be scored PASS as written.

## 3. GEN-NM10 N6

N6 scope per frozen PREREG Sec 7: "grep over the new drivers, PREREG.md and
REPORT.md ... returns empty outside the definitional token list."

Genuine-ERE raw hits (2):
1. `PREREG.md:65: REPORT): hypothesis|refine|evaluat|domain|plan|causal|navigat|`
2. `PREREG.md:66: arithmet|grammar|language|audio|interven|belie|goal|agent.`

Both are the definitional token list itself (Section 3). Zero hits in
`nm_b1main.zag`, `nm_b2main.zag`, and `REPORT.md`. **N6 holds as written.**

Two record corrections, however:

(a) **Scope mismatch:** the coded audit (`build.sh` Step 2) checks only
`nm_b1main.zag nm_b2main.zag PREREG.md`; the frozen bar also names REPORT.md,
and REPORT.md's own audit row records "(drivers + PREREG)" - matching the coded
under-scope, not the frozen bar. Re-auditing REPORT.md with ERE returns zero
hits, so this discrepancy is benign in outcome, but the record should note the
three versions (frozen bar > coded audit = REPORT record).

(b) **The coded exclusion regex never fired either:** `build.sh` Step 2 excludes
matches of `^[^:]*:[0-9]*:[a-z|.]*$` (bare lowercase pipe-separated lines).
GEN-NM10's definitional list is *inline in prose* (`REPORT): hypothesis|...`),
so line 65 would NOT have been excluded by that regex - a genuine-ERE drop-in
of the as-coded audit would have failed N6 on the lane's own definitional
lines. The correct criterion is the frozen text's "outside the definitional
token list", under which N6 passes. This is further evidence the audit was
never exercised as intended.

## 4. Corrected verdicts

| Lane | Recorded verdict | Genuine-ERE finding |
|---|---|---|
| GEN-REDIM C11 | PASS | **Not scorable as frozen.** One real hit (`rgen.zag:12`, "domain" in comment), inherited verbatim from the digest-pinned frozen reference; comment asserts absence of domain semantics. Opacity discipline substantively holds, but the bar text ("returns empty", no exception) is unsatisfiable and the PASS was produced by a vacuous grep. |
| GEN-NM10 N6 | PASS | **Holds.** No banned tokens outside the Section 3 definitional list in drivers, PREREG, or REPORT. |

Neither finding changes the lanes' scientific results (byte-identical batteries,
chain layouts); this is an audit-record correction, not a science invalidation.

## 5. Follow-ups recommended (for parent / research lead)

1. **Amend + re-freeze C11** (or record a governance erratum): add the
   definitional-list exception explicitly, and rule on inherited frozen-reference
   comments vs. researcher-authored lines. Do not score the current C11 text PASS.
2. **Amend + re-freeze N6's coded audit** to include REPORT.md (or amend the bar
   text to match the coded scope); either way make the three artifacts agree.
3. **Repo-wide sweep:** any other lane using `grep -in "a|b|..."` for opacity or
   similar audits inherits the BRE vacuity; flag them all for genuine-ERE
   re-audit (gen_stress, gen_cycles, gen_statefix, gen_subsumes_u, gen_generality
   are the obvious candidates, not checked in this task).

## 6. Method notes

- Pure shell grep; no code changes; no commits made by this worker.
- Genuine-ERE command (exact):
  `grep -Ein "hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent" <files>`
- GEN-POOLFLOOD's REPORT.md (C446) was not found in the workspace tree
  (searched `~/workspace/tnn-rsi/docs/lab/...`, git log, memory). O2's details
  were taken from the task handoff and verified independently against the lane
  files; the "two real hits during drafting" could not be reconciled to a file
  here - the only real hit in the two audited lanes is `gen_redim/rgen.zag:12`.
  The second drafting hit was likely in a GEN-POOLFLOOD draft file or was the
  NM10 definitional-lines-vs-exclusion-regex mismatch documented in 3(b).
