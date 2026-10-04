# NAMECHECK: TNN-3 Prerequisites Analyst

Date: 2026-10-01 UTC. Session: ce474bae-ae38-46d3-afc3-145b2453a122.
Assignment: define what must be true before TNN-3 can be preregistered.
This is a prerequisites checklist, NOT a TNN-3 design. Analysis only.

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

Result: `which python3 python` returned nothing before
`guard-check-done`. No forbidden executable is reachable in this
worker's PATH. Safebin contains only allowed tools (coreutils, git,
znc plumbing). This worker performed analysis only: it read
committed reports and working drafts, wrote two markdown documents,
and committed them. No computational research operation was performed
in any forbidden interpreter. Zero forbidden invocations. Step 0
recorded here.

## Scope check

- Owned path only:
  `docs/lab/research-lead/overnight-20260928/tnn3_prereq/`
- All input reports (red teams, compression, audit, synthesis,
  revision generalization, frontier backlog, alternative-explanation
  attack, freeze eval draft): read, never modified.
- TNN-2 source and binary: not touched (frozen; evaluation in
  progress is not disturbed).
- Sealed FW assets: not accessed (never inspected; only the
  evaluator's own draft report was read).
- Paper (`TNN_RESEARCH_PAPER_20260929.md`): untouched.
- NO TNN-3 design is proposed in this task. Design content that
  appears in the referenced synthesis report is cited as an input,
  not adopted or extended here.

## Provenance of inputs (commits verified in tnn-native-lab history)

| Input | Commit | Status |
|---|---|---|
| Construction red team (ATTACK-SUCCESS) | `340e94e3e` | committed |
| Inquiry red team (ATTACK-SUCCESS) | `4e329c772` | committed |
| Revision red team (ATTACK-SUCCESS) | `687ba0219` | committed |
| Compression analysis | `b2a6ae82c` | committed |
| Governance audit (GOVERNANCE-AUDIT-PASS) | `622363372` | committed |
| Red team synthesis | `42b4dfa91` | committed |
| Revision generalization analysis | `edbb0e9b5` | committed |
| Alternative-explanation attack | `ccee9e5e6` | committed |
| Frontier backlog (17 questions) | `65effc909` | committed |
| Ledger C143-C149 (freeze eval follow-up required) | `503a3bedc` | committed |
| Freeze eval draft (uncommitted) | - | on disk, `core_freeze_tnn2_eval/` untracked |
| Transfer analysis (uncommitted) | - | on disk, `tnn2_transfer/` untracked |

## Deliverables

1. `TNN3_PREREQUISITES.md` (this directory): checklist with per-item
   status, what is missing, what the freeze and adversary results
   will add, answers to the six assigned questions, and the minimal
   completed set that justifies starting TNN-3 preregistration.
2. This NAMECHECK.md.

## Verdict

TNN3-PREREQUISITES-MAPPED (analysis only; no design, no source edits,
pure safebin PATH, paper untouched).
