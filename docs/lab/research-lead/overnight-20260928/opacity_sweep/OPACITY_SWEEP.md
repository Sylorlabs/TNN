# OPACITY-SWEEP: genuine-ERE re-audit of GEN-lane opacity bars

Date: 2026-10-03. Worker: opacity-sweep (subagent).
Parent task: follow-up to OPACITY-ERE (C450).
Scope: analysis only. No frozen bar was modified. No commits made by this worker.

## 1. Background: the vacuous BRE pattern

OPACITY-ERE (C450) found that an opacity audit run as

```
grep -in 'hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent' <files>
```

is vacuous: without `-E`, grep uses BRE, where `|` is a literal
character. The pattern then matches only the literal 120-character string
`hypothesis|refine|evaluat|...`, which never occurs, so the audit always
reports zero hits and the bar always "passes". Demonstrated on the frozen
gen_stress materials:

- BRE form (`grep -in`, no `-E`): 0 hits (vacuous pass)
- Genuine ERE form (`grep -Ein`): 10 hit lines

The genuine ERE form used for this sweep (the C402 banned-vocabulary
pattern, documented verbatim in the gen_cycles PREREG):

```
grep -Ein 'hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent'
```

## 2. Lanes swept

The GEN lane family: gen_stress (covered by OPACITY-ERE; re-run here as a
consistency reference), gen_cycles, gen_statefix, gen_subsumes_u,
gen_generality. Branch sources were read read-only via
`git archive`/`git show` (branches lane-genstress-20261003,
lane-genstatefix-20261003, lane-gensubsumesu-20261003); no branch was
checked out and no index was touched.

A wider check of every other lane carrying an opacity audit found the
vacuous pattern in no committed build script: gen_cycles/build.sh,
compose_cycles/build.sh, cycles_generalize/build.sh,
cycles_oscillatory/build.sh, cycles_convergent/build.sh, and
cycles_feedback/build.sh all use genuine `grep -i -E` / `grep -rEi`.
The vacuous form appears only in uncommitted interactive audit invocations
(results recorded in REPORT.md prose), which is why only the GEN lanes
with prose-recorded audits needed the sweep.

## 3. Per-lane results

### 3.1 gen_cycles (bar C7 OPACITY)

- Audit form on record: genuine ERE. build.sh line 9 runs
  `grep -i -E 'hypothesis|...'` over gc_base.zag, gc_uni.zag,
  cyc_nomain.zag, gc_main.zag, gc_redmain.zag, uni_nomain.zag, fail-closed.
- Genuine ERE re-run on the same six files: **0 hits** (exit 1).
- REPORT claims "C7 OPACITY: PASS. Banned-token grep over all built
  sources empty". **Confirmed.** No amendment needed. This lane never used
  the vacuous pattern.

### 3.2 gen_generality (bar K7 OPAQUE-NAMING)

- Bar (PREREG.md): "PASS iff the grep audit finds zero banned-vocabulary
  tokens (Section 3) in gg_new.zag, PREREG.md, and REPORT.md".
- Audit form on record: none committed; REPORT.md prose records the
  verdict. The REPORT discloses matches ("The only matches are the
  document byline ... and the Section 3 rule-definition line"), so its
  audit was not purely vacuous BRE (a BRE run would have found nothing at
  all), but the "only matches" claim is incomplete.
- Genuine ERE re-run over the bar's scope: **15 hit lines**
  (gg_new.zag: 1; PREREG.md: 9; REPORT.md: 5). PREREG_AMEND1.md: 0 hits.
  Categorized:
  - Disclosed by REPORT: PREREG.md:67,77,80-83 (Section 3 banned-class
    rule definition, incl. the enumerated examples worker/team/shipment/
    depot/navigation/arithmetic/planning/causal/grammar/language/audio/
    image); REPORT.md:3,54 (document byline "Agent:").
  - NOT disclosed, all benign meta-text: gg_new.zag:3 (self-referential
    compliance comment "No domain vocabulary anywhere in this file");
    PREREG.md:340 ("evidences domain-blindness", verdict mapping);
    PREREG.md:366 ("## 9. Implementation plan", section heading);
    PREREG.md:379 and REPORT.md:148 ("AGENTS.md" toolchain references);
    REPORT.md:12 ("no domain handlers") and REPORT.md:57 ("what
    \"domain\" anything") (compliance assertions).
- **No domain-story token in any world, setup, driver, or result.**
  The bar's intent (domain-blind worlds) holds on the evidence.
- Two discrepancies vs. the frozen bar:
  1. The REPORT's "only matches" enumeration omits 7 benign hit lines
     (plan heading, AGENTS.md x2, domain-blindness mention, two
     compliance assertions, gg_new.zag compliance comment).
  2. The REPORT audited gg_new.zag, PREREG.md, **PREREG_AMEND1.md**
     instead of the bar's scope gg_new.zag, PREREG.md, **REPORT.md**.
     (PREREG_AMEND1.md is genuinely clean; REPORT.md contains the 5
     benign hits above.)

### 3.3 gen_statefix (no opacity bar)

- No OPAQUE-NAMING kill bar. PREREG documents opaque integer identifiers
  and explicitly grandfathers inherited world-builder comments ("may
  contain domain words; they are copied for byte-fidelity and are not
  this experiment's design language").
- Genuine ERE scan of new/built sources (gsf_gen.zag, gsf_main.zag,
  gsf_full_gsu.zag, gsf_full_diamond.zag): hits are (a) the grandfathered
  pair5 comments ("5th domain pair: spatial-layout x task-scheduling",
  "Domain X (spatial layout)", "Domain Y (task scheduling)"), byte-
  identical inherited copies per the K5 FIDELITY bar (gsf_world.zag diff
  empty vs gsu_world.zag); and (b) "no domain handlers"/"no domain
  labels" compliance comments in the new files. No new domain-story
  token in this lane's design language.
- No bar to amend. Grandfathering is explicit and byte-verified.

### 3.4 gen_subsumes_u (no opacity bar)

- Same structure as gen_statefix: no opacity bar; PREREG grandfathers the
  pair5 world-builder comments copied verbatim for world byte-fidelity.
- Genuine ERE scan: identical result. New design files (gsu_gen.zag,
  gsu_main.zag) carry only "no domain handlers"/"no domain labels"
  compliance comments; the pair5 domain-pair comments live in the
  inherited gsu_world.zag. No new domain-story token.
- No bar to amend.

### 3.5 gen_stress (bar K8 OPAQUE-NAMING; OPACITY-ERE reference re-run)

- Genuine ERE re-run over the bar's scope (gs_new.zag, PREREG.md,
  REPORT.md): **10 hit lines**, all benign meta-text: gs_new.zag:3
  (compliance comment); PREREG.md:94,104,108,110 (Section 4 banned-class
  definition); PREREG.md:551 ("Implementation plan" heading);
  PREREG.md:567 and REPORT.md:207 ("AGENTS.md" refs); REPORT.md:3,83
  (bylines, disclosed as the C402-precedent exception).
- REPORT's K8 claim "(Matches are only the document bylines ...)"
  understates the genuine-ERE hit set the same way gen_generality's does.
  Consistent with the OPACITY-ERE (C450) finding.

## 4. Which lanes have real hits?

Under the genuine ERE audit, hit lines exist in gen_stress (10),
gen_generality (15 in bar scope + 1 in NAMECHECK.md, out of scope),
gen_statefix, and gen_subsumes_u (grandfathered pair5 comments +
compliance comments only). gen_cycles has zero hits.

**No lane has a hit that violates the intent of its opacity bar.**
Every hit falls into one of five benign classes:
1. the prereg's own banned-class rule definition (must enumerate examples
   to be checkable);
2. document bylines ("Agent:"/"Worker:", C402-precedent exception);
3. self-referential compliance assertions ("no domain handlers",
   "No domain vocabulary anywhere in this file");
4. structural doc headings ("Implementation plan") and toolchain
   references ("AGENTS.md");
5. explicitly grandfathered byte-identical inherited world-builder
   comments (gen_statefix, gen_subsumes_u).

There is no domain-story token in any built world, setup, driver, or
result file in any swept lane.

## 5. Which bars need amendment? (recommendations; nothing amended)

1. **gen_generality K7** and **gen_stress K8**: as literally written
   ("finds zero banned-vocabulary tokens in <new source>, PREREG.md,
   REPORT.md") these bars are unsatisfiable, because the PREREG must
   define the banned class in prose and the docs carry bylines. The
   REPORT verdicts already carve prose exceptions, but the carve-outs
   are incomplete (gen_generality omits 7 benign lines; gen_stress's
   "only the bylines" omits its Section 4 definition, plan heading,
   AGENTS.md refs, and source compliance comment) and gen_generality's
   REPORT audited PREREG_AMEND1.md in place of the bar-scoped
   REPORT.md. Recommend a future amendment codifying the five
   permitted-exception classes from Section 4 above and fixing the
   audit file list, rather than prose carve-outs. Frozen bars were NOT
   touched by this worker.
2. **gen_cycles C7**: no amendment needed (genuine ERE, zero hits,
   fail-closed build script).
3. **gen_statefix / gen_subsumes_u**: no opacity bar exists; the
   grandfathering of inherited pair5 comments is explicit in the PREREG
   and byte-verified by the fidelity bars. No amendment needed. If a
   future lane reuses the pair5 world without the grandfathering clause,
   its opacity bar must scope inherited comments explicitly.

## 6. Method notes

- Pattern: the C402 banned-vocabulary alternation as documented in the
  gen_cycles PREREG, run as `grep -Ein`.
- Sources read read-only from branch tips via `git archive`/`git show`;
  the shared index and working branches were not modified.
- This completes the opacity audit sweep requested as follow-up to
  OPACITY-ERE (C450).
