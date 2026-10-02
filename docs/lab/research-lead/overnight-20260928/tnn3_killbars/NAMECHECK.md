# NAMECHECK: TNN-3 Kill-Bar Drafter

Date: 2026-10-01. Session: e0d4f332-8192-41d4-aa15-f95f81c4333b.
Assignment: draft TNN-3 kill bars that would have caught TNN-2's narrow
implementations of runtime construction, inquiry, and revision. BAR
DESIGN ONLY. No TNN-3 implementation. No source edits to any TNN
build. Status of this draft: DRAFT-NOT-FROZEN, for Micah's review.

## Step 0: Toolchain guard (mandatory)

Executed before any work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing; only
`guard-check-done` printed. No forbidden executable is reachable in
this worker's PATH. This worker performs analysis and drafting only:
it reads committed reports, writes two markdown documents, and commits
them. No computational research operation was performed in any
interpreter. No TNN-3 code was written. Step 0 recorded here.

## Scope check

- Owned path only:
  `docs/lab/research-lead/overnight-20260928/tnn3_killbars/`
- Inputs read, never modified:
  - TNN-2 prereg `7c1e30522`
    (`tnn2_prereg/TNN2_PREREG.md`, kill bars K-T2-1 through K-T2-8)
  - Construction red team `340e94e3e`
    (`tnn2_redteam_construction/CONSTRUCTION_REDTEAM.md`,
    CONSTRUCTION-ATTACK-SUCCESS)
  - Inquiry red team `4e329c772`
    (`tnn2_redteam_inquiry/INQUIRY_REDTEAM.md`,
    INQUIRY-ATTACK-SUCCESS)
  - Revision red team `687ba0219`
    (`tnn2_redteam_revision/REVISION_REDTEAM.md`,
    REVISION-ATTACK-SUCCESS)
  - Revision generalization analysis `edbb0e9b5`
    (`tnn2_revision_generalization/REVISION_GENERALIZATION.md`,
    REVISION-GENERALIZATION-ANALYSIS-COMPLETE)
  - Red team synthesis `42b4dfa91`
    (`tnn2_synthesis/REDTEAM_SYNTHESIS.md`,
    enumerated-schema / filled-slot pattern)
  - Compression analysis `b2a6ae82c`
    (`tnn2_compression/COMPRESSION_ANALYSIS.md`)
- TNN-2 source (`tnn2.zag` at `f4de7ff46`): not touched, not rebuilt.
- The running CORE-FREEZE-TNN2 evaluation: not disturbed.
- Paper (`TNN_RESEARCH_PAPER_20260929.md`): untouched.
- No per-mechanism patches proposed. No implementation guidance
  beyond what is needed to keep the bars implementation-neutral.

## Provenance of inputs

| Report | Commit | Finding used |
|---|---|---|
| TNN-2 prereg | `7c1e30522` | K-T2-3, K-T2-4, K-T2-5, K-T2-6 wording (the loopholes) |
| Construction red team | `340e94e3e` | 3 linear templates, 2 reachable in production; depth-4/96-path/12-value bounds; sum branch test-gated; 5-hop unrepresentable; no DEC; no reuse |
| Inquiry red team | `4e329c772` | L3 hardcoded constants 30/-999; L6 absent; ambiguous to arbitrary; misleading to lock-in |
| Revision red team | `687ba0219` | single-schema literal-patch; learner chose operands, researcher chose topology; t2_trial never invoked by revision |
| Revision generalization | `edbb0e9b5` | K-T2-6 loophole attribution (Cause 1: the bar admitted it); 5 repair topologies; info needs A-E; "two structurally different sealed repairs with derived content" recommendation |
| Red team synthesis | `42b4dfa91` | enumerated-schema / filled-slot pattern; "fixed templates with variable content" is L2 |
| Compression analysis | `b2a6ae82c` | inquiry guide content constant; revision repair fully researcher-authored |

All commits verified present in `tnn-native-lab` history on
2026-10-01.

## Deliverables

1. `TNN3_KILLBARS_DRAFT.md` (this directory): the drafted bars with
   rationale, what each would have caught in TNN-2, and deterministic
   verification procedures.
2. This NAMECHECK.md.

## Constraints honored

- Draft only. Every bar is marked DRAFT-NOT-FROZEN. Nothing here is a
  frozen threshold and nothing here governs any build until Micah
  reviews it and a TNN-3 preregistration freezes it (or amends it)
  before any TNN-3 implementation begins.
- No em dashes in loop documentation.
- Pure safebin PATH for the whole session.

## Verdict

TNN3-KILLBARS-DRAFT-COMPLETE (drafting only; no implementation, no
source edits, pure safebin PATH).
