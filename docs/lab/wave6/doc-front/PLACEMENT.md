# Placement memo — "TNN does not corrupt its own reasoning" front-page doc

**Investigation:** wave-6 doc-front · 2026-09-20
**Verdict: POSITIVE.** The draft is written, every cited number verified
against the actual wave-5 evidence dirs. Four phrasing imprecisions in the
task brief were found and corrected (numbers themselves all check out —
details below). No git push performed, per program law. Drafts live in
`~/workspace/tnn-lab/wave6/doc-front/`.

## Deliverables

- `~/workspace/tnn-lab/wave6/doc-front/INTEGRITY_HEADLINE.md` — the full
  draft section (repo frontmatter + internal TOC, plain confident
  language, honest qualifier, evidence pointers).
- `~/workspace/tnn-lab/wave6/doc-front/PLACEMENT.md` — this memo.

## The front door (what I found)

The working branch is `tnn-native-lab` (the reorg'd tree: `docs/`,
`src/`, `data/`, `artifacts/`, `archive/`). Two front doors:

1. **Root `README.md`** — the true front door for any visitor. Same
   content as `main`'s README (sha `804237a2…`): a "Current entry point —
   R33 research generation" block, a Contents TOC, research-history
   sections, an evidence-tiers table. Stale in one important way: its
   `Research/…` links are **404 on this branch** (the reorg moved them
   under `docs/`), so the README already needs repair independent of
   this task.
2. **`docs/INDEX.md`** — master TOC for the research archive. Its
   `## Layout` section lists `program/`, `hypotheses/`, `generations/`
   — it does not yet mention `lab/` at all (the native-lab waves live at
   `docs/lab/wave1..wave5` but are unlisted).

## Recommended EXACT placement

**A. New file:** `docs/lab/wave5/INTEGRITY.md`
— the draft from `INTEGRITY_HEADLINE.md`, committed with its
frontmatter (`id: W5-INTEGRITY`, `status: PROVISIONAL`,
`hypotheses: [H-07, H-10]`). It sits beside the evidence it
synthesizes (`integ-1/`, `deliberative-refusal/`, `redteam-rt2/`,
`trap-upgrade/`, `ledger-gating/`), following the repo's "one wave,
one directory" hierarchy.

**B. Root README — new top-level section, first in the document.**
Insert directly after the H1 (`# TNN — True Neural Network Research`),
BEFORE the "Current entry point — R33 research generation" block:

```markdown
## Headline result — TNN does not corrupt its own reasoning

**Wave-5 (2026-09-20):** the real scaffold-release learner faced 8
cheat-trap families (four adapted from documented frontier-LLM failure
modes) with adversarial administration and live instruments: **zero
cheat signatures**, **2,595 of 2,595 temptations refused** (myopic
control took 1,327), flat integrity hold through 100x horizons,
byte-identical reruns, zero RNG. Honest boundary, trialed: the learner
is truthful but sensor-deceivable — sustained observation spoofing
breaks the hold; the corroborated-elimination defense held 35/35, and
multi-source trust tiers are the named open problem.

Read the [full integrity result](docs/lab/wave5/INTEGRITY.md).
```

TOC entry — add as the FIRST bullet in the existing `### Contents`
list:

```markdown
- [Headline result — TNN does not corrupt its own reasoning](#headline-result--tnn-does-not-corrupt-its-own-reasoning)
```

**C. `docs/INDEX.md` — Layout section.** Add the missing lab line plus
the headline pointer:

```markdown
- `lab/` — native-lab waves (`wave1`–`wave5`); the headline integrity
  result is `lab/wave5/INTEGRITY.md`.
```

**Why this placement, not elsewhere:** Micah said "the FRONT of the
repo's docs." The root README is the only page every visitor reads, and
`docs/INDEX.md` is the master TOC — those two are the front. Putting
the section *above* the stale R33 entry-point block is deliberate: it
makes the headline the first claim a reader meets, and it is honest to
do so only if the boundary language ("truthful but sensor-deceivable",
scoped envelope) ships with it, which the short README section does via
the link.

## Numbers verification (all checked against local evidence dirs)

| Claimed | Source | Status |
|---|---|---|
| 8 trap families, 0 cheat signatures on real learner | `integ-1/TRIAL_RESULTS.md` "Zero cheat signatures on R across all eight trap families" | ✓ |
| 2,595 temptations refused, 100x | `deliberative-refusal/TRIAL_RESULTS.md` "refused all 2,595 scheduled temptations over 2,000 blocks" | ✓ |
| 10x leg also 0 takes | table "main 10x: 0,0,0,0" | ✓ |
| Myopic took 1,327 | takes (1250,76,0,1) | ✓ |
| Pressure took 1,405 | takes (1405,0,0,0) | ✓ |
| Flat 1000‰ hold all 2,000 blocks | "integrity hold 1000‰ on all 2,000 blocks" | ✓ |
| Instruments live: E=8, F/G/H=1 fires; IL phantom/empty/noshape bite; arm C A-sig1=1, B-sig=1, judge HACK h2=1 | `integ-1/TRIAL_RESULTS.md` evidence point 2 + table | ✓ |
| 137/137 INTEG_CHECK, INTEG_FAILURES 0, byte-identical `cb986552…` | `integ-1/TRIAL_RESULTS.md` official run | ✓ |
| Attack 73/73 checks; R1 HOLD, R2/R3 BREAK (false COMMIT @s15; false-theory disconnect @s24, 21 episodes) | `redteam-rt2/TRIAL_RESULTS.md` | ✓ |
| Defense 35/35; D3 HOLD on true theory; D3b genuine-shift HOLD | `redteam-rt2/TRIAL_RESULTS.md` | ✓ |
| Residual: two consecutive fabricated −1s still force UNCOMMIT; multi-source trust tiers specified, not built (`DEFENSE.md` §4) | `redteam-rt2/TRIAL_RESULTS.md` residual + boundaries | ✓ |
| 8/8 adversarial claims blocked; 60/60 honest chains IL_OK; 433 LG_CHECK 0 mismatches | `ledger-gating/TRIAL_RESULTS.md` | ✓ |
| Zero RNG, byte-identical reruns, exact ledger replay | all four TRIAL_RESULTS instrument checks | ✓ |
| SIGNAL_DISCONNECT learner-initiated; "learned = persists after disconnect" | `redteam-rt2` R3 diagnosis; program law | ✓ |

**Local dirs read:** `wave5/integ-1/`, `deliberative-refusal/`,
`trap-upgrade/`, `redteam-rt2/`, `ledger-gating/`,
`llm-failure-research/`, `wave4/rl-redteam/` (lineage check).
Note: `wave5/longhorizon-temptation/` does not exist locally — the
long-horizon methodology lives in `wave4/longhorizon-temptation/` and
was ported into integ-1 as instrument 4. Nothing cited is affected.

## Corrections to the task brief (numbers fine, phrasing was not)

1. **"8 LLM-informed cheat-trap families"** → only families **E–H**
   (sycophancy, evaluation-aware deception, sandbagging, unfaithful
   reasoning) are LLM-informed adaptations (see
   `trap-upgrade/PREREG_UPGRADE.md` citing the LLM failure catalog);
   A–D are the wave-4 originals (A: poisoned evidence/premature
   commitment, B: long-horizon temptation, C: claims-channel early
   disconnect, D: integrity ledger). The brief's A–D names ("trap
   features, memorization traps, loophole exploits, provenance gaps")
   do not appear in the evidence — I used the evidence-grounded names.
2. **"RL red-team harness"** → the `rl-redteam` harness is
   **deterministic** (zero RNG, static grep gates, fail-closed); "rl"
   names the reward-channel attack lineage (bribes, corruption,
   forgery), not an RL-algorithm adversary. The draft says
   "adversarial red-team harness" and names the lineage explicitly.
3. **Horizons** → integ-1 ran 480 episodes = **11.16x** (not 100x);
   the preregistered 4,800-episode (100x) stretch is defined but
   **not run**. The 100x no-degradation figure belongs to
   deliberative-refusal. The draft scopes this precisely; the brief's
   "over long-horizon runs" is true but underspecified.
4. **"2,595 at 10x and 100x"** → 2,595 is the 100x leg's count; the
   10x leg (200 blocks) refused all of its temptations too. Draft
   phrased accordingly.

## Open questions needing Micah before this is the front page

1. **Status sign-off.** Draft frontmatter is `PROVISIONAL` ("claimed
   but awaiting independent confirmation"). Does he want that, or a
   stronger status — and does he personally approve the headline claim
   wording "TNN does not corrupt its own reasoning"?
2. **Boundary language.** The draft leads the honest qualifier
   ("truthful but sensor-deceivable") in the one-sentence summary and
   the README section. Confirm he's comfortable with that as the
   front-page framing — or whether he'd rather the README lead be
   claims-only with the boundary one click down.
3. **Stale README entry-point block.** The current "Current entry
   point — R33 research generation" block sits below the new section
   and its `Research/…` links are broken on `tnn-native-lab`. Keep as
   history, rewrite, or remove?
4. **MATRIX.md + H-07 are stale.** The hypothesis matrix has no
   wave-5 rows, and H-07's open question says "so far the native
   cognitive results are negatives" — no longer true in the same way.
   Add wave-5 rows / revise H-07 as part of this change, or separate?
5. **Family naming.** Confirm canonical names for A–D (draft uses
   "poisoned evidence", "long-horizon temptation", "claims-channel
   early disconnect", "integrity ledger" from `integ-1/TRIAL_RESULTS`).
6. **Program law respected:** nothing pushed; the two files above are
   local drafts in `~/workspace/tnn-lab/wave6/doc-front/`. Committing
   `docs/lab/wave5/INTEGRITY.md` + the README/`docs/INDEX.md` edits to
   `tnn-native-lab` awaits his go-ahead on 1–4.

## Next step

Get Micah's rulings on 1–4 (5 is minor), then: write
`docs/lab/wave5/INTEGRITY.md` from the draft, apply the README section
+ TOC entry and the `docs/INDEX.md` Layout line on the
`tnn-native-lab` branch, and open the branch changes for his review —
no push to the repo without his explicit approval.
