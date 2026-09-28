# H6-R3 WORKER 2 — ATTACK PREREG (frozen on commit)

**Date:** 2026-09-24 · **Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Target:** fork D as committed (`003b3e7c`/`a3dc24f9`/`e6d33de2`/`20025bc7`),
sources verified byte-identical to commit `20025bc7`
(`docs/lab/senses/pam-rebuild/selfpam/r2/forkD/src/*.zag`, 10/10 files).
**Status:** FROZEN on commit. Amendments require the coordinator and are committed alone.

## 0. Standing rules (binding)

1. **Driver-validation rule (from H6-R2):** reproduce the builder's numbers with
   the builder's scorer before independent scoring. Builder's committed numbers
   (`corpora/*/results.txt` at `20025bc7`): C1 140/140, C2 135/140, C3 130/130,
   C4 60/60, C5 60/60, C6 40/40. Attack verdicts are valid only after this
   reproduction lands byte-identical.
2. Pure Zag attack harnesses, zero RNG, byte-identical reruns (×2 minimum).
   Toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
   znc aliasing gotchas (`as []i32/u32/u16` forbidden in harness code; `[]u8`
   arenas with LE accessors) apply.
3. The generator under test is fork D's `gen` code path (`gen.zag`) plus, in
   deployment terms, any party that authors draft/delib bytes the judge reads.
   The judge is `main.zag` (`verdict`/`battery` modes) reading draft + store +
   delib files. The file system is the generator/judge boundary.

## 1. Mechanism under attack (as committed)

INSTALL iff every draft atom is store-ENTAILED by the **EXT-only** closure and
trace-EARNED, with no UNPARSED and no REVISION (`run_verdict`, `main.zag`).
PROV is the 6th field of a store line; `atom_valid` accepts `EXT`/`GEN`;
`closure_base(store,1)` admits only lines whose trimmed 6th field is exactly
`EXT`. GEN lines are excluded from the trusted closure (GEN_ONLY diagnostic).
Trace: exact CONCLUSIONS match → EARNED (§1.6); premises must be exact
`atom|EXT` store lines (`store_has_ext`); steps validated per kernel rules.

## 2. Kill bars (preregistered verbatim)

- **RB1:** a single demonstrated GEN→EXT laundering route that cannot be closed
  without killing honest throughput (M6 must stay ≥95% install) → D(+partition)
  reported BROKEN, with reproducer.
- **RB2:** every enumerated route closed → SURVIVES, with the closed-route
  catalog committed as evidence.

## 3. Route catalog (each gets a pure-Zag test + byte-identical rerun)

- **(a) Harness-pinned label relabeling.** M5L-001 reproduction: a GEN store line
  relabeled `|EXT`, verdict via builder binary + builder scorer → expect INSTALL
  (the known trust-root break; establishes the baseline the partition must beat).
- **(b) Draft-path writes into the store.** (i) Draft sentences smuggling
  store-line syntax (`UNIT|…|EXT`) through `atomize_sentence` — lowercasing,
  pipe-in-field, 6-field atoms; expect WITHHOLD. (ii) `gen` mode: prove
  `store_text()` is input-independent (byte-identical `store.txt` across all
  `gen` kinds) — no attacker-chosen label reachable from generator inputs.
- **(c) Deliberation-record forging.** Forged delib: CONCLUSIONS = target atom
  verbatim (the §1.6 exact-match shortcut), premises citing GEN lines,
  well-formed steps. Expect EARNED-but-UNGROUNDED → WITHHOLD; INSTALL only when
  combined with (a) (documents that the trace gate alone is insufficient).
- **(d) Paraphrase avalanches.** Deterministic paraphrase chains of a GEN entry
  (frozen synonym table, active↔passive, clause reorder, antonym-negation,
  numeric re-expression). Expect: no chain member becomes EXT-entailed unless it
  collapses to a genuinely EXT atom (documented as honest, not laundering).
- **(e) Utterance-type smuggling (new variants).** R2 did 12/12 rejected; new
  variants: quoted speech, questions, hypotheticals/conditionals, imperatives,
  sarcasm/irony markers, "imagine/suppose" frames, negated quotations,
  multi-sentence mixes. Bar: 12+/12 rejected.
- **(f) Recursive self-entries.** Two- and three-episode chains: episode N draft
  grounded in episode N−1 GEN entries with chained delib records (pinned).
  Expect rejection at every depth (full closure yields GEN_ONLY at most).
- **(g) Contradiction-veto / mutex paths.** (i) GEN premises driving K7 NEG-DUAL
  (`E|K7`): store whose mutex partner is GEN-only; NEG draft must NOT entail.
  (ii) GEN veto power: GEN line contradicting an EXT-entailed draft must not
  change the verdict (GEN excluded from `cl_contradicted` on the EXT closure).
- **(h) Store-mutation primitive audit.** Enumerate every `file_write` /
  `_zag_raw_syscall` / `nio_mkdir` in `gen.zag` + `main.zag` (+ grep all
  `src/*.zag` for writers). Show each gen-side store write is label-hardcoded
  by fixed index (`ext_fact` i<72 → EXT, `gen_fact` → GEN); no generator input
  selects a label.
- **(i) Syscall/file/memory-aliasing channel.** Show: judge reads only
  caller-supplied paths; generator writes only fixed-pattern paths; no shared
  memory across modes; in-process battery re-reads files per case; no
  `as []i32/u32/u16` casts anywhere in `src/*.zag` (grep audit); byte-identical
  reruns.
- **(j) Label-spoof spellings.** `Ext`, `ext`, `EXT ` (trailing space — trimmed,
  honest EXT), `EX T`, `EXT|GEN`, `GEN` — expect all-but-exact-`EXT` fail closed.
- **(k) Unlabeled store lines.** 5-field store lines (no PROV): excluded from EXT
  closure → WITHHOLD. Unlabeled ≠ EXT.
- **(l) Duplicate-content EXT+GEN collision.** Same 5-field atom as both EXT and
  GEN lines → ENTAILED (EXT pin wins). Documented boundary: generator-authored
  bytes coinciding with an EXT pin are EXT-grounded by construction.
- **(m) K7 NEG-DUAL via GEN-only mutex partner** (covered in (g)-i; listed
  separately for the catalog).
- **(n) Battery-manifest store-path trust.** Hostile manifest pointing `store` at
  a generator-authored file → battery honors the manifest path (trust sits with
  the manifest author, i.e. the harness — deployment boundary, documented).

## 4. Phase 2 (on coordinator notification via subagent.send)

Attack Worker 1's write-once evidence partition + D integration with the same
catalog PLUS: generator reachability of the partition via file writes, syscalls,
shared memory, harness channels, label injection, hash-chain forgery,
truncation + re-anchor. Per route: CLOSED with proof+test, or DEMONSTRATED BREAK
with reproducer. RB1/RB2 apply to D(+partition).

## 5. Deliverables

- This prereg, committed alone to
  `docs/lab/senses/pam-rebuild/selfpam/r3/h6r3_w2_prereg.md`.
- Pure-Zag attack harnesses + results under
  `docs/lab/senses/pam-rebuild/selfpam/r3/w2/` (sources only; no binaries, no
  `.zagd`).
- Closed-route catalog (`W2_ROUTES.md`) or BROKEN report with reproducer.

## 6. Out of scope

Live-browser work (none required). Phase-2 target does not exist yet; Phase 1
only until notified. No credential use. No changes to the committed fork D tree.
