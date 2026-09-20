# DEBATER M2 - Opening position: replay-divergence as primary gate, static scanning as secondary

## (1) Thesis

The v2 blind red-team round is evidence: the plants that mattered - computed syscall immediates, the runtime-built /dev/urandom path, the _zag_clock_monotonic_ms timer intrinsic - were caught only by replay divergence. Both static scans missed the mechanisms entirely. Two builds, two K2 kills, zero times the static layer carried the catching. The honest restructure: promote hardened multi-run replay to the primary no-RNG gate, keep v2 static as a secondary tripwire (no K2 bar, no rebuild), add per-trial-build blind red-teaming as process. This unblocks Arm C on evidence, not on hope.

## (2) Three strongest arguments

**1. Follow the empirical record.** Static analysis fights an asymmetric battle - the hider needs one unseen trick; the scanner must enumerate them all. Plant (1) hid behind a shape-matching init check that zeroed allocator pages made plausible; (2) was a hand-rolled EntrySet invisible to token-based scanning; (3) rode the literal pin_table carve-out. Each miss is a category failure - a fix patches one hole while the hider picks another. Replay is symmetric: any runtime nondeterminism, however hidden, must manifest as output divergence across runs, or it cannot affect the trial's results. The watch items are the ledger: replay caught the real ones; static caught the easy ones.

**2. Replay's weakness is cheaply fixable; the static weakness is not.** The one replay hole on record (zeroed pages hiding uninitialized reads) is a harness problem: the v3 amendment's replay-hardening section (N runs, heap pre-dirtying, varied allocation patterns) fixes it. Adopt that section alone: a certified gate in days. The static failures each demanded a redesign - fail-closed init, structural hash-iteration detection, narrowed carve-outs, register-taint, an intrinsic ban: ~1280 lines, no guarantee it survives its own K2. Harden what already works; don't rebuild what twice didn't.

**3. It preserves defense-in-depth and unblocks Arm C fastest.** The no-RNG law governs the AI's decision paths; this debate is only about the certification tool. The static scanner still runs, reports, and tripwires the easy misses - it just no longer holds a kill bar it may never pass. Per-trial-build red-teaming stays as process, so the gate keeps getting adversarially tested. The Arm C trial is parked right now behind a passing auditor version; hardened replay is the fastest route to unparking it - the harness exists, the hardening is days.

## (3) Honest concession - the strongest argument against

Replay is behavioral evidence, not mechanical proof: a plant could stay deterministic in the lab yet be nondeterministic in deployment - environment-dependent nondeterminism the lab never triggers. The answer: a hidden RNG that never reaches measured behavior cannot confound the trial; the deployment gap is real, so replay must cover deployment-like conditions - adversarial environments, varied OS state, timing surfaces - named in the preregistered N-run matrix, or the gate is theater. Conceded: replay-first is not mechanical proof. But neither is an unbuilt v3 - the record shows two dead versions, zero passing ones, while replay produced the only catches that mattered. Proven behavioral catching beats promised mechanical catching.

## (4) What it unblocks, and its cost

Unblocks: Arm C - the parked state-variation experiment - once the hardened replay matrix passes preregistered bars. A harness change (days), not a scanner rebuild (weeks plus a third blind round).

Cost: the replay-hardening section as a standalone deliverable, plus a prereg amendment narrowing the gate (needs Micah's re-approval). What it does not cost: the ~1280-line v3, a third K2 round, or another month ending up back here with the same evidence.
