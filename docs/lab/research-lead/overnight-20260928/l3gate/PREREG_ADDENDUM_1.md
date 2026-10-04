# PREREG ADDENDUM-1 (C611) — integrity disclosure, fixture provenance, selection correction

Lane `lane/l3gate`. Worker L3-GATE (continuation of the session that froze
`PREREG.md` at `090b6fc16`, 2026-10-03 22:54:53 -0700).

**This addendum changes NO threshold in `PREREG.md` §1.** It is committed alone,
before any gate program is built or run in this session. Its three jobs:
disclose two defects in the prereg's own packaging, certify fixture
provenance, and correct one factual error in §2's *named instance*.

---

## A1. DEFECT 1 — the prereg commit was not alone (disclosed, assessed)

`PREREG.md` line 4 claims "**Committed ALONE, before any gate program exists.**"
That is **false as a statement about the commit**. `git show --stat 090b6fc16`
shows **9 paths / 4211 insertions** in that one commit: `PREREG.md` plus eight
`.zag` files.

**Assessment, with evidence.** All eight are read-only *inputs* (fixtures), not
gate programs and not results. Each was checked byte-for-byte against its
canonical upstream source:

| Fixture in `l3gate/src/` | Canonical path | Resolves at | sha256 (16) |
|---|---|---|---|
| `c603_mf_floor.zag` | `l3macro_unknowndepth/mf_floor.zag` | `lane/l3macro` | `df85b3ffb62fb33f` |
| `suf1_learner2.zag` | `l3_suf_intermediate/src/learner2.zag` | `lane/recovery` | `e49a4269d6099ca3` |
| `c397_gpi3_driver.zag` | `grammar_program_gpi3/gpi3_driver.zag` | `redteam/suf-audit` | `99001aa7d4c535e9` |
| `c397_gpi3_learner.zag` | `grammar_program_gpi3/gpi3_learner.zag` | `redteam/suf-audit` | `e76ed761ef00840f` |
| `rx2.zag` | `l3_rx/src/rx2.zag` | `arch/cogops-unify` | `98f908499daaddfc` |
| `rx4.zag` | `l3_rx/src/rx4.zag` | `arch/cogops-unify` | `8ab5b17d34cb4380` |
| `c281_gl2m_h1.zag` | `xdomain_grammar_l2m/gl2m_h1.zag` | **`4e7eb30b1` only** | `3c83d6806672f577` |
| `c281_glm_learner.zag` | `xdomain_grammar_l2m/glm_learner.zag` | **`4e7eb30b1` only** | `ca1110f65bc13b6b` |

All eight: **IDENTICAL**.

**Two of the eight (the CALR / `xdomain_grammar_l2m` lineage, i.e. the C281
family) are absent from every tip and resolve ONLY at `4e7eb30b1`.** This is
exactly the failure mode `lane/recovery` warned about: *a lane may LOOK absent
when it is merely invisible.* Checked, as instructed, before concluding
anything about a missing lane. Consequence: the C281-lineage fixtures are
**provenance-certified at a non-tip commit**, and any conclusion resting on them
is a conclusion about the state of that tree at `4e7eb30b1`.

**Why the thresholds still stand.** A fixture is an input. Committing inputs
beside a prereg cannot reveal a gate result, because no gate program existed.
Verified: the earliest mtime of any gate artifact is 23:04, ten minutes after the
22:54:53 commit. **No threshold was chosen after seeing a gate result.**

## A2. DEFECT 2 — a transcription bug found in the G2 program BEFORE any run

`gate/g2_dn.zag` (uncommitted at prereg time) transcribed the frozen core's
quiescence loop with the change flag **overwritten** instead of accumulated:

```
let ch:i32=1;  ... if(r[q]!=pv[q]){ch=1;} else {ch=0;}   // LAST slot wins
```

versus the claim's own `mf_floor.zag`:

```
let ch:i32=0;  ... if(r[q]!=pv[q]){ch=1;}              // ANY slot wins
```

With `q=0..3` and R0 the only live register, the transcription reports
quiescence one pass early whenever R3 is unchanged. **Disclosed here, before
running, and fixed before the first G2 run.** This is a transcription defect,
not a threshold change, so it does not void the prereg. Any G2 number produced
before this fix would have been void; none was produced.

## A3. CORRECTION to §2's named instance — `C401` does not exist as an L3 claim

`PREREG.md` §2 names "**C401** (L3-NIV2-WAVE9, 2026-10-03)" as the newest
adjudication. **`C401` is not locatable as any L3 claim.** The only occurrence of
the string `C401` in the entire ledger apparatus is
`STAGED_LEDGER_ENTRIES.md:277`, a reconciliation note that `C401-C410` working-tree
entries were never appended. The real L3-NIV2 series is **C294, C312, C324, C334,
C348, C350, C358, C364, C367, C391** (all 2026-10-02). The prereg appears to have
skipped from `C294` to `C401` by numeric order and mistaken a numeric neighbour
for a claim.

**The SELECTION RULE of §2 is unchanged and is re-applied honestly**, by commit
timestamp descending, over L3-class claims **and** adjudications, restricted to
those with recoverable primary source:

| Rank | Claim | Lane | Commit timestamp |
|---|---|---|---|
| 1 | **C603** MACRO-FLOOR (L2, not L3) | `lane/l3macro` | 2026-10-03 21:25:01 -0700 |
| 2 | **C600/C602** frozen-core loop audit; CALR family -> L1 | `lane/l3macro` | 2026-10-03 21:04:26 -0700 |
| 3 | **SUF-AUDIT** adjudication: C281->L1, C397->L2, C335->L1 | `redteam/suf-audit` | 2026-10-03 19:14:04 -0700 |
| 4 | C453 L3-RX-BUILD CONDITIONAL-PASS 15/16 | staged (watchdog) | 2026-10-03 10:08:08 UTC |
| 5 | C459 L3-INR-SEALED, L3-KILLED | staged (watchdog) | 2026-10-03 08:04:25 UTC |
| 6 | C397 GPI-3 (L2) | `redteam/suf-audit` | 2026-10-02 |

Ranks 1-3 are **adjudications that already demoted their subject**. Because the
mission's headline claim is the C281 lineage and because ranks 4-5 are the newest
claims that still *assert* L3 novelty, the results table carries **all six**, with
ranks 1-3 flagged. `C401` is recorded as **NOT-VERIFIABLE** under G0 (artifact
provenance failure: no such claim), excluded from G4's numerator and denominator,
and named in the coverage table — never converted into a verdict.

## A4. One further prereg/implementation divergence, disclosed

`PREREG.md` §G1 step 2 says the prover is **EMITTED** from the extracted literals
plus a fixed kernel. The implementation available at prereg time is
**hand-authored** per claim, with the two preregistered in-gate assertions
(`ASSERT-NOLEARNER`, `ASSERT-KEYONLY`) enforced over the emitted bytes. The
assertions are the enforceable part; the emission is not fully automatic.
**This weakens G1 and is stated as a limitation, not glossed.** `PROVER_LOC` is
therefore a floor on cheapness, not a measurement of it: a hand-written prover can
be made short by leaving work out. G1's own `ASSERT-KEYONLY` is the guard against
that failure and is reported per claim.