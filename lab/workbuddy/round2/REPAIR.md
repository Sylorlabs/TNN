# Crew D Repair Report — Workbuddy Round 2

**Source:** `build/wb2_dialogue.zag`
**Source SHA-256:** `0bec5459b2959ec056c6c8771de7de009d7fd9406d7029d98fa97faa1a9d531b`
**Base:** Crew B source (`902723167908e3fa8903737503b6c4fc318326efcb664d03632e1779db5088b8`)
**Date:** 2026-09-27

## What Crew C found (the four defects)

| # | Defect | Example |
|---|--------|---------|
| 1 | Teaching the same subject + verb with a *different* complement overwrote the old fact instead of coexisting with it | `quinn was promoted.` then `quinn was praised.` → only one survived |
| 2 | A correction only retracted facts with the same subject **and** verb, so changing the verb left the stale fact live | `quinn was promoted.` → `no, quinn resigned.` → both facts still answered |
| 3 | Corrections only worked right after a teaching, not right after a question | `what is the gate code?` → `no, the gate code is 2222.` → mangled |
| 4 | Some `what is` answers ended with two periods | `what is the vault code?` → `the vault code is 7760..` |

## How the repair works

### 1. Complement-aware fact identity (fixes defect 1)

Facts are now identified by **(subject, verb, complement-signature)**, not just (subject, verb).
A new helper (`wb2_compl`) extracts the complement — the part of the fact after the verb —
and re-teaching the exact same triple is idempotent, while a different complement creates
a sibling fact. A signature lookup (`wb2_sig_find`) finds the exact match.

| Input | Result |
|-------|--------|
| `quinn was promoted.` then `quinn was praised.` | 2 facts coexist; both `was quinn …?` questions answer `yes.` |
| `quinn was promoted.` then `quinn was promoted.` | still 1 fact (idempotent) |

### 2. Subject-wide correction tombstones (fixes defect 2)

A correction now retracts **every live session fact for that subject, regardless of verb**,
then installs the corrected fact. Retraction is by *tombstone*: the dead row's fact-id is
set to `-1` instead of being deleted or overwritten in place. (An earlier attempt used
`fid=0` for dead rows; that aliased them onto KB row 0 — "Herman Melville wrote the novel
Moby Dick." — so `-1` was chosen.)

All fact scanners were audited: every row scan that looks for a live fact now requires
`fid >= 100000` (the live-session range), which excludes tombstones (`-1`) and KB facts
(`0–47`). One gap found during the audit was closed: `general_fact` (the legacy
entity-question lookup) did not skip tombstoned rows, and `emit_fact` looks rows up by
fact-id, so a dead row could theoretically have been served again. It now skips `fid<0`.

New session fact-ids are allocated as **max existing session fid + 1**, so they can never
collide with a tombstone or a reused id.

| Input | Result |
|-------|--------|
| `quinn was promoted.` → `no, quinn resigned.` | `was quinn promoted?` → `I don't know.`; `was quinn resigned?` → affirmed; count is 1 |

### 3. Corrections after questions (fixes defect 3)

A new hook sits in the after-question correction dispatch. When the correction-marked
remainder is a declarative sentence (has a verb, is teach-shaped), it is routed through
the same corrected install path as a correction after a teaching — retract-by-subject,
then install. Two deliberate carve-outs:

- **Bare-entity remainders** (`no, i meant the eiffel tower.`) keep the legacy re-ask
  path. The check is precise: the remainder must *be* a KB entity name (optionally with
  a leading "the"/"a"/"an"), not merely *mention* one — so `no, tnn retired.` (declarative,
  mentions an entity) correctly installs instead of being mangled.
- **Actually:** `actually,` and `actually ` are now recognized as correction markers
  alongside `no,`, `i meant`, etc.

| Input | Result |
|-------|--------|
| `what is the gate code?` → `no, the gate code is 2222.` | installs; next `what is` serves `2222.` |
| `who wrote the martian?` → `no, the lighthouse keeper resigned.` | installs as a taught fact; count is 1 (previously this fell into a legacy path that answered an unrelated Darwin fact) |

### 4. Exactly one period on `what is` answers (fixes defect 4)

The `what is` lookup now normalizes its echo: any trailing periods on the stored fact are
stripped, then exactly one is added. This covers facts stored with punctuation,
correction-installed facts, and single-token subjects (`what is quinn?`).

| Input | Result |
|-------|--------|
| `the vault code is 7760.` → `what is the vault code?` | `the vault code is 7760.` (one period) |

## Aux-less sentences (found during validation, fixed)

Crew B's subject/verb splitter only understood sentences with known auxiliary verbs
("was", "is", …). Bare declaratives like `quinn resigned.` got an empty subject, which
meant stale aux-less facts survived subject-wide correction. A second splitter
(`wb2_split2`) falls back to treating the final token as the verb, and every
identity-critical function (signature lookup, retraction, upsert, `what is` lookup)
now uses it. Verb-group-gated yes/no functions deliberately keep the old splitter —
an aux-less fact has no verb group, so those paths correctly decline to judge it and
the honest echo/withhold behavior remains.

## What was preserved

- T1, T2, T4, T5, T6 behaviors: unchanged (battery 24/24 PASS).
- Operator order in the turn pipeline: unchanged; all new logic sits inside existing
  branches or in helpers called from them.
- Determinism: every probe and battery session run twice, byte-identical; S1 matches
  the frozen SHA under `MALLOC_PERTURB_=165` and `=90`.

## Bounded-loop history (honest disclosure)

The original plan was one bounded repair loop. In practice, validation runs after the
first loop exposed four more in-scope defects, which were fixed and re-validated:

1. After-question aux-less corrections (`no, the lighthouse keeper resigned.`) were
   mangled into unrelated KB answers — fixed by routing declaratives through the
   install path.
2. Aux-less stale facts survived subject-wide correction (empty subjects from the
   lexicon-only splitter) — fixed by `wb2_split2`.
3. Aux-less facts bypassed `what is` period normalization — fixed.
4. Single-token `what is` subjects bypassed normalization — fixed.

Each fix was followed by a full re-run of the battery, probes, S1, and regressions;
all pass. Two further audit findings were also closed in the same pass:

5. The declarative/entity carve-out was too aggressive: `no, tnn retired.` (mentions a
   KB entity) was left to the legacy path, which served "Herman Melville wrote the
   novel Moby Dick." — fixed with the precise bare-entity check.
6. `general_fact` could return a tombstoned row to `emit_fact` — fixed with the
   `fid<0` skip.

An audit of the F4 challenge/provenance paths (`are you sure?`, `how do you know?`)
confirmed they cannot serve a tombstoned fact: every path that tombstones also clears
the previous-answer fact-id, so a dead id is never stashed.

**No further source edits will be made.** Any new failure found from here on is
reported as-is.

## Files delivered

| File | Contents |
|------|----------|
| `build/wb2_dialogue.zag` | repaired source (only deliverable that matters) |
| `REPAIR.md` | this report |
| `RESULTS2.md` | scores, tables, verdict |
| `SHA256SUMS.md` | hash manifest for source, probes, outputs, evidence |
| `battery_run/` | 20 strict battery sessions (fresh outputs) |
| `crewc_run/` | 32 Crew C probes × 2 runs each |
| `probes/d_p1..d_p8` (+ `.r1`/`.r2`) | Crew D's own fresh probes |

Excluded from the commit-ready set: `wb2_dialogue_bin`, `.zag-cache/`, `.zagd`,
and all regenerable artifacts.
