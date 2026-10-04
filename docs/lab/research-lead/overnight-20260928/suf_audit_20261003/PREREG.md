# PREREG — SUF L3 CLAIM AUDIT (frozen before audit conclusions)

Worker: REDTEAM-SUF. Branch: `redteam/suf-audit`.
Dir: `docs/lab/research-lead/overnight-20260928/suf_audit_20261003/`
Date frozen: 2026-10-03. Ledger head at freeze: `504641745`.

This file is committed ALONE, before `SUF_AUDIT.md` and `L3_CANDIDATE.md` exist.

## 0. Mandate

The canonical ledger records **"L3 achieved anywhere: zero."** I do not take that
verdict on faith, and I do not take the lanes' self-bounding admissions on faith
either. Self-criticism can be accurate, understated, or (the failure mode that
matters) *generous to itself in the direction that makes the negative result
look robust*. My job is to re-derive every L3-adjacent verdict **from source**.

## 1. Scope (frozen lane list)

Audit every lane under `docs/lab/research-lead/overnight-20260928/` whose
directory name or ledger entry asserts invention / L3 / open-form:

`l3_inr_sealed` `l3_inr_impl` `l3_inr_k10` `l3_rx` `l3_rx_k10`
`l3_suf_intermediate` `l3_suf_redteam` `l3_suf_adversary` `l3_suf_scaling`
`l3_next` `l3_interm_repr_reuse` `l3_ctx_pair_hypothesis`
`l3_ctxpair2_hypothesis` `grammar_program_gpi3` `grammar_program_gpi2`

Plus: any lane whose ledger entry claims invention and whose directory does not
carry an `l3_` prefix. Explicit search for `l3_niv2` and `calr` (both may be
absent; absence is itself a finding to record).

## 2. The question I must answer for every claim (charter §7)

> **"If I inspect the source BEFORE the experiment, can I enumerate every
> structural form the learner could possibly produce?"**

`YES` is disqualifying. The audit unit is the **emittable-form set** `F`, defined
as the set of structural forms the learner can put into the world, not the set
of behaviours it can produce. I must produce, for each lane:

1. `F` enumerated from source, with `file:line` and the **literal** lists/arrays
   that define it.
2. The **construction path**: which function builds a structural form, from what
   inputs, under what condition.
3. Whether `F` is finite-and-written-by-the-researcher, or genuinely
   history-determined.
4. Verdict + one-line source citation.

## 3. Method (frozen, pre-committed)

**M1 — Source-first, ledger-last.** For each claim I read the `.zag` source and
reconstruct `F`. Ledger text, lane README prose, and RESULTS/VERDICT files are
read *only after* `F` is reconstructed, and are treated as claims to be checked,
never as evidence. If ledger prose and source disagree, **source governs** and
the discrepancy is itself reported.

**M2 — Enumeration test.** `F` is "enumerable from source" iff there exists a
finite, human-readable, researcher-authored specification (a list of operator
ids, a `switch`/dispatch table, a template array, a grammar production list, a
mutation enum) from which every emitted form can be derived by inspection,
without running the learner. If I can write down that list, the claim is capped.

**M3 — Causal-history test.** For each candidate structural choice point I ask:
is the chosen form a function of (a) a researcher-written finite menu indexed by
a runtime counter/score, or (b) the learner's accumulated history in a way that
selects a form *not itself present in the menu*? Only (b) can survive. A score
that merely *ranks* menu items is (a). A history that *grows* the menu is (b) —
I will state what growth would be required.

**M4 — Adversarial both directions.** Explicitly required: for each lane,
(i) find whether the self-admission **understates** the bound (lane is more
bounded than it admits → harsher verdict), and (ii) find whether the incumbent
red team was **too generous** (lane may be less bounded than admitted → escalate).
Both outcomes are reportable wins. A lane whose verdict survives in both
directions is marked `ROBUST`.

**M5 — Artifact check.** Every claim must cite a runnable artifact (`.zag` +
a commit sha + a determinism/verification record if one exists). Claims whose
artifact cannot be located are INVALID regardless of prose. Claims resting only
on a ledger sentence are INVALID.

**M6 — Consistency check.** Ledger claim IDs must be minted and non-contested.
`C377`–`C466` are CONTESTED and may not be minted. Any lane resting on a
contested ID is reported as `ID_CONTESTED` in addition to its scientific class.

**M7 — Purity.** Any computation I run is Zag-only, via
`tools/zbuild.sh X.zag --rep 3`, after sourcing `.env/pure-zag.sh`. I expect
to need little computation; this audit is a reading task. If I do run Zag I
record it. I use no other interpreter.

## 4. Kill criteria (frozen — a claim meeting ANY of these is capped)

| ID | Criterion | Cap |
|---|---|---|
| **K1 MENU** | Emitted forms are a selection from a literal, finite, researcher-written list of forms (operator ids, dispatch table, template array, enum). | ≤ L2+ |
| **K2 ENUMERABLE** | `F` is decidable by static reading; no form exists that the source cannot already name. (charter §7 answer = YES) | ≤ L2+ |
| **K3 BRUTE** | Candidates are enumerated exhaustively by the program and the winner is argmax over the enumerated set. If the enumeration *is* the contribution, argmax is the whole result. | ≤ L2; if enumeration >10^6 and is the contribution, ≤ L1 |
| **K4 TEMPLATE** | Novelty is in slot *arguments* (weights, bindings, thresholds); the *structure* is a fixed template. | ≤ L2 |
| **K5 ORACLE LEAK** | Acceptance signal derives from a researcher-held answer / reference solution rather than from held-out observable consequence. | ≤ L1 |
| **K6 SCORE-RANK** | The "discovery" is a ranking over pre-existing candidates by a researcher-authored score; learning = tuning the score. | ≤ L2 |
| **K7 ARTIFACT** | No runnable artifact, or artifact contradicts the prose. | INVALID |
| **K8 CONTESTED-ID** | Rests on a contested claim ID. | INVALID (pending) |
| **K9 NO-FREE-STRUCTURE** | Every structural degree of freedom is fixed by researcher code; history only sets *parameters*. | ≤ L2 |

## 5. Escalation criteria (frozen — the pre-registered bar for calling something L3)

A claim is **L3** only if ALL of the following hold, each with source evidence:

- **E1 NO MENU.** There is no researcher-written finite list of forms to select
  from. Not "small menu", not "enum". Absent.
- **E2 NOT ENUMERABLE.** The charter §7 answer is **NO**: reading the source
  does not let a reader write down the set of forms the learner can produce.
- **E3 HISTORY-CAUSAL.** At least one structural choice is determined by the
  learner's accumulated history, and that choice is not derivable from any
  researcher-written enumeration. Demonstrated by a concrete trace: same source,
  different history ⇒ different structural form; and a proof that the form was
  not in the menu because the menu does not contain it.
- **E4 NOT BRUTE-FORCE.** The form is not the argmax of an in-program
  enumeration. (Argmax over an open-ended, incrementally-grown space is
  allowed; argmax over a closed pre-written space is not.)
- **E5 CONSEQUENCE-SELECTED.** The form survives because it works on held-out
  data, selected by observable consequence, not by researcher assertion or a
  reference answer.
- **E6 REPRODUCIBLE.** Deterministic under `--rep 3`, and the artifact is
  committed at a citable sha.

Failure of any one of E1–E6 ⇒ not L3. All six ⇒ **L3**.

## 6. Classification lattice (frozen)

- **L3** — all of E1–E6.
- **L2+** — genuinely above template-filling: the structure varies with the
  problem in a way the source does not literally enumerate, but the vocabulary of
  variation is researcher-bounded. Partial escape only.
- **L2** — structure fixed; parameters/selection learned. Includes MENU,
  TEMPLATE, SCORE-RANK.
- **L1** — no structural choice at all; only scalar/threshold fitting, or the
  contribution is the enumeration itself.
- **INVALID** — unsupported, contradicted by artifact, or contested-ID.

## 7. Constructive half (pre-committed)

I will attempt to specify one new candidate (`L3_CANDIDATE.md`) that could pass
E1–E6, and state **exactly, and falsifiably, what would have to be true** for it
to pass — including the pre-registered *falsifiers* that would kill it. A
proposal that cannot state its own kill condition is not a proposal.

## 8. Self-imposed limits (to prevent me from softening my own audit)

- I will not improve, repair, or extend any audited mechanism. Read + classify.
- I will not run a mechanism to "see if it works better than advertised" — that
  is the owning lane's job. I run Zag only to check a *factual* source claim.
- If I cannot find source evidence for a claim, the verdict is INVALID, not
  "probably fine".
- Every verdict line must carry a `file:line` or a ledger line number. A verdict
  with no citation is not a verdict.

## 9. New claim IDs

`C5xx` block and higher only. `C377`–`C466` MUST NOT be minted.

## 10. Kill criteria for MY OWN audit (falsifiable)

My audit is itself falsified if:
- **S1** I classify any lane L3 without citing all six of E1–E6 with source.
- **S2** I rely on any lane's self-assessment as evidence for its own verdict.
- **S3** I soften a classification because the incumbent red team already made it.
- **S4** I fail to report at least one case where a lane is MORE bounded than it
  admits (K-understatement), or at least one case where the incumbent red team
  was too generous (escalation). If neither exists after the audit, I must say
  so explicitly and justify it.
- **S5** I cannot state a falsifier for my own constructive proposal.