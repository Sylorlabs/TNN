# Wave record: 20260927-0821pdt

Staffed lanes: supervised tnn_chat FIT fresh re-run (stale count 11 waves; standing 8-wave rule mandated it) plus the fit_authority SHA256SUMS record-defect repair; fork battery driver per P1/P8/P19/P20 against the frozen 49-entry manifest; prereg design drafts for the four queued blockers (EXP1c, EXP2/K4, B1/P9, COMP-2/P11). Mandatory debate group convened and transcript committed.

## Commits this wave (all local, never pushed)

1. be5bb24c8: lane 1: FIT fresh re-run PASS plus fit_authority/SHA256SUMS repair.
2. db4d57187: lane 2: fork battery 50 named, 48 PASS, 2 UNTESTABLE; fresh frozen 50-entry enumeration manifest.
3. 59b9df4b0: lane 3: four prereg design drafts alone (EXP1c, EXP2-K4, B1-P9, COMP2-P11); drafts only, no implementation, no testing.
4. 09bfaae63: lane 3 documentation-only annotation of prereg headers with design commit id 59b9df4b0. Prereg text frozen at 59b9df4b0.
5. 07d22a39a: debate transcript DEBATE_0821.md (advocate/skeptic/judge), committed with verdict rulings.
6. (this commit): WAVE_RECORD_0821.md plus LOOP_STATE.md debated verdict lines.

## Lane 1: FIT fresh re-run plus SHA256SUMS repair (evidence be5bb24c8)

Rebuilt binaries byte-identical to frozen pins (decline sha 20273a99..., baseline 1ada2fae...). KB1 30/30 specific declines (26 "My knowledge base contains nothing about ...", 4 "No knowledge-base fact ..."), 0 blanket refusals, 3 runs. KB2 17/17 answered, 0 declines, byte-identical baseline parity (6/6 runs). KB5 10/10 answered, 0 declines, same parity. 15/15 run-pairs byte-identical via cmp, all exit 0, all stderr empty. Output hashes byte-identical to all prior wave records. Zero drops vs the 20260925-1421pdt baseline. Entry-point scan over ecbe9b5b7..80c40a7af: no new chat/REPL/interactive entry points; stdin-read backstop grep over 188 new .zag sources: zero hits. D1 never-pruned authority path now holds every chain input read-only (first wave with all four carry-over preconditions passing).

SHA256SUMS repair: created docs/lab/rsi/fit_authority/SHA256SUMS in repo convention, covering nine authority files (2 instrument sources, kb.txt, gaz.txt, 3 fixtures, README.md, AUTHORITY_MANIFEST.md). All shas verified against pins before writing; third-party checkable via sha256sum -c (all nine OK). Draft-time placeholder shas were self-corrected before commit; none remain. Traveling caveat carried verbatim: tnn_chat emits unflagged confabulations on out-of-KB questions.

Zero Python anywhere in lane 1. No em-dashes in any lane doc.

## Lane 2: fork battery driver (evidence db4d57187)

50 named entries, 48 PASS, 2 UNTESTABLE (rh-pull-1-head 5802fec84, rh-pull-2-head 4b76bb59f; pinned toolchain path absent in both trees, non-TNN research-doc trees, unchanged cause nine waves running), 0 FAIL, 0 CONFIRM. Uniform 48/48 grepped evidence: znc pin 48/48, B1 FORKBATTERY-OK 42 byte-identical (5dfe3c16...), B2 bin sha 75b85d3c... 48/48, B3 exit 0 48/48, NEG1 E0002 48/48, NEG2 char-1 diff 48/48, tree probe R32_ZNC_PROBE_OK 48/48. Harness extracted from the 20260923-2321pdt archive (sha f38d9154... matches frozen); rebuilt pure-Zag harness binary byte-identical to prior waves (a2e6284c...).

Manifest drift vs frozen 0521pdt baseline: one new branch (tnn-native-lab-wave-archive-20260927-0521pdt, tested first, PASS); no missing branches; all worktree SHAs unchanged; remote tips unchanged at run start and close. Incident: lane 1 committed be5bb24c8 mid-run; battery pinned run-start HEAD 80c40a7af via read-only git show at pinned commits; results unaffected (judge ruled).

Zero Python anywhere in lane 2. Fresh frozen 50-entry enumeration manifest committed.

## Lane 3: prereg design drafts (evidence 59b9df4b0, annotated 09bfaae63)

Four drafts under docs/lab/rsi/runs/wave-20260927-0821pdt/preregs/, frozen-designed, no implementation, no testing, no adoption. No prereg pre-authorizes Python (grep-verified); no em-dashes (grep-verified).

1. PREREG_EXP1c.md: compositional-choice design. Shrunk plan space (399 sketches, at most 3 primitives), 1200-tick horizon, decaying novelty bonus B0(n)=B0/(1+n); reflexes frozen verbatim (EXP1b reflex-smuggling lesson); frozen retune protocol. Kill bars: K1-K6 scaled to 1200 ticks plus new K7 choice-reality (post-enumeration plans chosen on learned credit >= 0.50, else the run is VOID as a test). Cost 144,000 agent-ticks. Waiting on: the six withheld EXP1b red-team corrections committed (or a freezing wave recording why it proceeds without them). No governance ruling gates it.
2. PREREG_EXP2_K4.md: real-failure grounding plus rescuer-lens K4 hardening. 12 real deliberation failure traces curated by a spec-blind curator (never read the one-brain spec), first-12-by-commit-order frozen selection. Kill bars: KH1 one-brain >= 9/12 real traces; KH2 rescuer-lens (b2) exclusion; KH3 attacker-lens (b1) exclusion; KH4 shared-writes-off ablation with joint timing; K2/K3/K5/K6 carried. Frozen anti-guarantee: items NOT constrained to where lenses fail. Cost 180 op-counted runs. Waiting on: a failure-trace corpus that predates the freeze.
3. PREREG_B1_P9.md: P9 bar reformulation re-freeze template for the B1 post-pass-recolor class: KB4a' direction bar (Pearson r >= 0.35 between delta-field magnitude and the frozen bounce field), KB4b' content-conditioned spread (>= 20% with bounce-aligned direction, floor 2.0 per banked ~2/255 knowledge), KB6' percentile-based edge (p99 gradient <= 8), KB0' cheat-proof control (frozen flat-tint control must FAIL KB4a' with r < 0.10, else VOID). Explicitly prospective only: B1 BOUNCE's DISCARD is never re-scored. Waiting on: a new mechanism (k-family stays DISCARDed, jointly unsatisfiable); freezing wave pins the bounce field SHA and runs the pure-Zag probe to confirm thresholds by redraft.
4. PREREG_COMP2_P11.md: rotated-author re-test plus ruling 6 plus stemmer-contingency. Gate zero frozen: no implementation commit until Micah renders ruling 6. Two-leg plan: Leg R (ruling favorable) re-tests with annotated existing lineage; Leg A (ruling adverse) fully re-derives with an independently developed pure-Zag stemmer, retiring the 1121pdt 20/20 rather than re-voting it (P11). Rotated author plus dual-attested implementer (P3/M5), fresh sealed 30-probe set post-freeze, COMP-B1..B6 carried with ADOPT mapping VOID (P10), new COMP-B7 separation and COMP-B8 B5 transcripts. Waiting on: ruling 6; two different workers for author and implementer.

## Prereg commit-order self-check

VACUOUS for adoption: no loop candidate implementation commits this wave (lanes committed evidence, records, designs, and the debate transcript only). Prereg design commit 59b9df4b0 strictly precedes any future implementation commits that may follow these drafts. Standing caveat carried: commit order evidences commit order only, never run order.

## Debate (transcript 07d22a39a, skeptic's provenance probe verbatim)

Judge's rulings: (1) FIT CONFIRMED, tag narrowed from [RE-CERT] to [NEW] (staleness cleared by fresh execution; stale count resets to 0). (2) SHA256SUMS repair CONFIRMED [NEW], with scope stamp (binary/toolchain pins remain prose in README.md; R33 sources and candidate work out of scope). (3) Fork battery CONFIRMED [RE-CERT] (toolchain/extraction-stability scope only). (4) Preregs QUEUED as designed-not-adopted, no verdict; COMP2-P11's ruling-6-gate posture recorded as correct to hold. (5) Commit-order self-check VACUOUS. (6) Governance rulings, sealed pairs, DP-1 UNTOUCHED [VOID]. (7) Interactive TNN holds with narrowed wording: tnn_chat runnable (15 live runs, binaries byte-identical to pins); entry-point scan explicit over merge range ecbe9b5b7..80c40a7af; no runnable interactive TNN beyond the frozen probe instruments.

Provenance answered: FIT is new execution on an inherited frozen chain; SHA256SUMS is a new file with inherited pins; fork battery is new execution of inherited machinery; preregs are new designs with inherited lineage, unfrozen; rulings and pairs inherited and untouched.

## UNTOUCHED this wave

His six governance rulings remain OPEN; all sealed blind pairs (R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14, whirlpool-planform) untouched; DP-1 presentation remains the parent agent's queue decision. This wave neither decided, relitigated, nor re-presented any of them. G1, D-VID-1, ST-1 not touched (standing stand-downs).

## Open questions banked for the parent

Whether the standing pull-head UNTESTABLEs should become a queued coverage item after nine waves; the future record item of getting binary/toolchain pins out of README prose into a checkable file; the loop's own wave-HEAD cadence racing the three-hour wave cadence (lane commits landing mid-battery are inert under pinned-commit extraction, but worth watching).

## Queued next

His six pending governance rulings (untouched); his blind verdicts on the sealed pairs (unchanged, nothing added this wave); DP-1 presentation is a parent-agent queue decision; CV-P adoption still doubly gated (ruling 6 pending); the four prereg drafts now await their freeze-time gates (EXP1c corrections, EXP2 corpus, B1 new mechanism, COMP-2 ruling 6); tnn_chat FIT fresh re-run due again within 8 waves (stale count reset to 0 this wave).
