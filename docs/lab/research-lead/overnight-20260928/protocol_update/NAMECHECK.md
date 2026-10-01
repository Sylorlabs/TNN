# NAMECHECK: Protocol Updater (corruption detector integration)

## Step 0: Toolchain guard

- Safebin activated at startup: `$HOME/safebin` populated with
  symlinks to system tools (git, sh, bash, ls, cp, mv, rm, mkdir,
  cat, grep, sed, awk, wc, cmp, sha256sum, git-receive-pack,
  git-upload-pack); `export PATH="$HOME/safebin"` applied.
- `which python3 python` returns nothing (verified in this PATH).
- Zero forbidden executables invoked in this task.
- No Zag compilation needed for this task (draft update only);
  no binaries built, no sealed worlds opened.

## Scope

- DRAFT UPDATE ONLY. `LIFETIME_PROTOCOL_V2.md` is DRAFT-NOT-FROZEN
  and remains so. No freeze language added or removed. The frozen
  v1 draft (`LIFETIME_PROTOCOL_DRAFT.md`) is untouched.
- No implementation, no variant, no evaluator work.
- The research paper is untouched. Nothing pushed.

## Input provenance

- Protocol v2 draft:
  `docs/lab/research-lead/overnight-20260928/lifetime_protocol/LIFETIME_PROTOCOL_V2.md`
  (read before edit; head commit at task start `8307a9a9e`).
- Corruption detector spec:
  `docs/lab/research-lead/overnight-20260928/corruption_detector/CORRUPTION_DETECTOR.md`
  (commit `ff2d1e1ef`).
- Grounding analyses referenced by the detector: eviction
  corruption `986c52fdc`, zombie census `2b81d0692`. Read only
  through the detector spec; no source re-inspection performed.

## What was added and why

Step 4a of the protocol required the driver to run a corruption
detector at each world boundary, and Section 6.1 defined the
CORRUPTION event type, but no detection algorithm existed. The
detector spec (ff2d1e1ef) supplied one. Six edits integrate it:

1. Section 0 changelog, new item 10: records the source, the
   item-2 vs item-10 distinction (event type defined vs
   algorithm specified), and the affected sections.
2. Section 5 step 4a: cross-reference corrected from "Section 6"
   to "Section 6.2".
3. Section 6.1 CORRUPTION bullet: pointer to the algorithm
   section added.
4. New Section 6.2 "Corruption detector (driver-side)": the
   integrated algorithm. Two passes (per-MAP root validity with
   valid-root set {101,102,103,104}; shared/hijacked root walks
   with 80-step bound), canonical snapshot format with SHA-256
   and (id, promo_index) identity, BOOTSTRAP/Z_RANGE/FOSSIL/
   VALID/ZOMBIE/Z_SHARED/Z_HIJACKED taxonomy, onset-only
   transition rule, world-granular attribution caveat, EVICT vs
   CORRUPTION distinction, shared-root landmine rule, three
   recommended extensions (guard field-12, literal-operand
   field 8, policy-anchor liveness), driver cost, non-claims,
   and the retention-sweep mapping to Section 7.7 end-states.
5. Section 7.7 ZOMBIE bullet: Z_SHARED and Z_HIJACKED map to
   ZOMBIE at the retention sweep.
6. Section 18 CORRUPTION EVENTS bullet: pointer to Section 6.2.

## Verification

- Zero em dashes and zero en dashes byte-verified in the edited
  file (grep for U+2014 and U+2013, no hits).
- Title line still reads `# LIFETIME EVALUATION PROTOCOL (V2,
  DRAFT-NOT-FROZEN)`. No freeze language touched.
- No other sections modified: `git diff --stat` shows only
  `LIFETIME_PROTOCOL_V2.md` and this directory's NAMECHECK.md.

## Standing metrics (this task)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: the integration edits
  (researcher-owned measurement-infrastructure documentation;
  the legitimate role).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- COGNITION LINES: 0. MODES: 0. BRIDGES: 0. HANDLERS: 0.
- SEMANTIC CASES: 0. SUF DECISIONS: 0.
- Nothing frozen, nothing pushed, no sealed worlds opened.
