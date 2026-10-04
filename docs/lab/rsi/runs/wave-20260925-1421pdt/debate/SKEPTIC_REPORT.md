# Red-team skeptic report: wave-20260925-1421pdt debate group

Skeptic role. Two standing process confirmations, no new candidates.
Nothing was added to or removed from Micah's sealed judge queue; the
six governance rulings and nine sealed pairs are untouched. Red lines
observed by both workers: pure Zag only, zero Python anywhere, commits
stay local, no push, no frozen bar weakened.

Evidence read in full:
- docs/lab/rsi/runs/wave-20260925-1421pdt/forks/FORK_RESULTS_1421.md
- docs/lab/rsi/runs/wave-20260925-1421pdt/chat_fit/FIT_1421.md

Independent repo verification performed read-only (git merge-base,
git log, git show, git ls-tree, git rev-parse equivalent reads; no
writes, no checkouts). Results cited inline.

---

## Item 1: Fork battery 31/31 PASS, draft verdict CONFIRM [RE-CERT]

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer: everything the battery exercised is inherited. The znc binary
tested on all 31 forks is the pinned sha
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
unchanged from prior waves. The shell battery fixtures are the same
frozen fixtures. The pure-Zag harness was extracted read only from the
2321pdt archive branch (sha f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6
d73e5e6f4b31aac3f719738) and rebuilt byte-identical to last wave's
harness (sha a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f
9f4ef66). What is nominally new: the run-start origin tip 93f0fd54c
(origin moved 84ed45077 -> 93f0fd54c since last wave), the local HEAD
9526cdb5c5 (moved 0ca683756 -> 9526cdb5c5), and the newly archived
wave-1121pdt branch at 60a05799. But the battery did not test any of
that new content: it tested the pinned znc binary as extracted from
those commits, plus the frozen shell battery. The new code in the
three merges (Micah's own PAM/MATH frontier work) was exercised by
nothing in this battery. The two previously untested origin tips,
695997f5 and 236e5a17815f, were covered only transitively: confirmed
ancestors of 93f0fd54c via merge-base --is-ancestor (independently
re-verified this wave, both YES), not directly tested.

### Attack (a): duplicate padding, 31 entries vs 24 unique commits

The file states "Entries total: 31" and "Unique commits tested: 24" in
the same section, and names every duplicate explicitly. Enumerating
the 7 redundant entries:

1. origin-tnn-native-lab-runstart-tip duplicates
   origin-tnn-native-lab at
   93f0fd54c82cf2af6b1a699b6e56f003707fdc2f.
2. wave3-probe duplicates forktest-tnn-native-lab at
   bd30978748fa83bbea6e423a7074cf32b7304291.
3. wave3-senses duplicates forktest-tnn-native-lab at
   bd30978748fa83bbea6e423a7074cf32b7304291.
4. wave3-trades duplicates forktest-tnn-native-lab at
   bd30978748fa83bbea6e423a7074cf32b7304291.
5. forktest-wave-debate-session-1-backup duplicates
   local-wave-debate-session-1-backup at
   3947dca1a77c00818575dbc7476556c8278b8b7b.
6. origin-reorg-phase-0-1 (via FETCH_HEAD) duplicates
   forktest-reorg_phase-0-1 at
   9914322267e1358e5542a23c72ec51d1a9ae43df.
7. origin-wg-freeze (via FETCH_HEAD) duplicates forktest-wg-freeze at
   f875b34179f570ba1ad555262cd401ddc4a52848.

31 - 7 = 24, which matches the file's own arithmetic. The verdict on
honesty: "31/31 PASS" is literally true (31 enumerated forks were
tested, 31 passed) and the file discloses the 24-unique-commit count
in the same breath, so this is not deception. But it is honest only in
full context. The duplicate entries buy execution-path coverage
(seven extra extraction/chmod copies, each znc copy sha-verified) and
zero new code coverage: testing commit X in worktree A and worktree B
is the same commit tested twice. Any downstream summary quoting
"31/31 PASS" without the duplicate caveat inflates apparent coverage.
Steel-man of the defense: re-running the battery per fork also
re-verifies the per-fork extraction pipeline (chmod +x of tree-mode
artifacts, sha match per scratch dir), which is exactly what a
divergence detector is for; the duplicates are cheap and intentional.

### Attack (b): the run-start-tip duplicate entry and "Live: 3"

Live is listed as 3: local-tnn-native-lab, origin-tnn-native-lab, and
origin-tnn-native-lab-runstart-tip. The third is the file's own
"explicit duplicate" of the second, so unique live commits = 2, not 3.
The entry exists to pin the run-start tip at 93f0fd54c alongside the
closing ls-remote re-check (identical sha). But the closing re-check
section already proves the tip did not move ("The tip did NOT move
during this run", both reads 93f0fd54c82cf2af6b1a699b6e56f003707fdc2f).
So the duplicate entry is fully redundant with origin-tnn-native-lab
plus the closing re-check. Its existence is disclosed, not deceptive,
but "Live: 3" is a count of live entries, not live commits, and the
file never says that sentence. Recommendation carried in this report:
report live entries and unique live commits as two numbers.

### Attack (c): divergence detector, not capability evaluator

This attack lands. A 31/31 PASS certifies: the pinned znc binary
extracts intact (sha match on every fork), the shell battery vectors
(B1, B2 rerun, B2 recompile-identical, B3 check --strict --no-zagd,
NEG1, NEG2, PROBE) behave identically everywhere, and the harness
builds deterministically. It certifies nothing about the code that
actually changed this wave: the local branch moved 0ca683756 ->
9526cdb5c and the origin tip moved 84ed45077 -> 93f0fd54c, and neither
the PAM/MATH frontier code in those merges nor any candidate logic
was compiled or executed by this battery. A defect introduced in
Micah's frontier code between those SHAs would sail through 31/31
PASS. The draft verdict is labeled CONFIRM [RE-CERT] as a "standing
process confirmation", which is correctly scoped if read as toolchain
stability, but it is oversold the moment any reader treats fork PASS
as evidence about the merged frontier code. The file does not make
that claim itself; the risk is downstream. The verdict should carry a
one-line scope stamp: certifies toolchain and extraction stability
only, not the contents of the moved commits.

### Attack (d): ancestor check vs direct testing of 695997f5 and 236e5a17815f

The file's claim is that because both tips are ancestors of the tested
tip 93f0fd54c, testing the merged tip "covers them". I re-verified the
ancestry claims: both return YES. The logical gap: merge-base
--is-ancestor proves provenance containment (every commit in the
tip's history is contained in 93f0fd54c's history), not behavioral
coverage of the tip as it existed at that moment. If a defect lived at
695997f5 in a file that the merge 93f0fd54c then removed or
overwrote, testing the merged tip would not reveal it, and this wave
never ran the battery against the znc binary as extracted from
695997f5 itself. So the sentence "they are explicitly NOT untested
this wave" is the weakest sentence in the file: they were not
directly tested; they are transitively covered for artifacts the
battery actually exercises. The concession: for what this battery
exercises (the pinned znc binary at the current tip), testing the
merged tip is sufficient, because the battery tests one pinned binary
sha and the current tip's copy is the one that matters going forward.
The gap is theoretical at this wave's scope, but the claim should be
reworded to "transitively covered for current-tip purposes; not
directly tested at their own tips."

### Attack (e): internal consistency of the results file

Checked and it holds together. Table rows: 1 local + 12 archive
branches + 1 wave-debate-session-1-backup + 2 origin entries + 5
FETCH_HEAD remote heads + 7 forktest worktrees + 3 wave3 worktrees =
31. Live 3 + Fixture 28 = 31. Fixture: 12 archives + 1 wave-debate +
5 remote heads + 7 forktest + 3 wave3 = 28. 31 - 7 duplicates = 24
unique commits, matching the stated count. The new archive branch
(wave-1121pdt at 60a0579973fa64c80ec2501afc1f5d3080b9b8ba) is treated
as fixture "since its SHA has not moved since it was created",
consistent with the stated live/fixture rule. The znc mode record
distinguishes the 100644 archive branches (20260924 0221pdt and 0521pdt,
no wave- prefix) from the 100755 ones (wave-0221pdt, wave-0521pdt and
the rest); the naming is confusing but the split is internally
consistent. "No commits, merges, resets, rebases, or pushes were made
by this worker" matches the red lines. Minor observation: exact
vectors were "spot-checked verbatim on local-tnn-native-lab" with the
pattern "grepped across all 31 full.logs", so per-fork verbatim
verification rests on OVERALL=PASS in 31/31 RESULT.txt files and
harness_exit=0 VERDICT=PASS on 31/31, which are machine-checked per
fork; acceptable, and disclosed. Concession: the file's counts,
SHAs, and live/fixture split are internally consistent; no
contradiction found.

### Cost

About 23% of this wave's battery spend (7 of 31 executions) re-ran the
battery on commits already tested in the same wave. That is cheap
shell work and buys per-fork extraction verification, so the cost
attack is weak on dollars but worth a line in the runbook: if the
battery ever gets expensive, the duplicate entries are the first thing
to drop, since they add no code coverage.

### Item 1 verdict as skeptic

CONFIRM, but only within a stamped scope: toolchain and extraction
stability, 31 executions / 24 unique commits, 2 unique live commits.
The draft is not deceptive as written, but "31/31" and "Live: 3" must
not travel without the duplicate disclosure, and the verdict must not
be read as certifying the merged frontier code, which this battery
never touches.

---

## Item 2: tnn_chat FIT FRESH PASS on 9526cdb5c5d5de732c87583f29d09418894cf8b8

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer: all artifacts under judgment are inherited and frozen. The 38
facts (kb.txt sha 3ef27296c147a101eea0f093940cdbe1bb8be9fe58c211181196
46aec6889be1), gaz.txt, baseline tnn_chat.zag (frozen sha c0776ad6...),
decline tnn_chat_decline.zag (frozen sha a87011fe...), the two R33
support sources, the pinned znc, the three probe fixtures, the
expected classes, and the expected output hashes: every one of these
is byte-identical to the prior certified record. Nothing in the chain
is new: precondition (3) showed zero diff lines across all three
merge ranges, and the fresh re-run reproduced the frozen binary shas
(1ada2fae baseline, 20273a99 decline) and all three prior output
hashes byte-identically. The only "new" element is the certification
event itself: a fresh re-run executed on the new HEAD 9526cdb5c5,
correctly tagged [RE-CERT], not a candidate verdict. Instrument
provenance this wave: the two .zag sources were scavenged from the
2321pdt archive branch (docs/lab/rsi/runs/wave-20260923-0834pdt/
paths; I verified the frozen sha c0776ad6... is present there),
fixtures from the 0221pdt archive branch, kb/gaz/R33/znc from HEAD,
all sha-verified before use. That is inherited provenance reassembled
by hand, not fresh lineage.

### Attack (a): the brief misstated the last FIT wave

The brief said the last FIT re-cert was wave-20260925-0821pdt on
b4507fb22. The repo record, independently verified: commit f2b8126ba
exists with message "wave-20260925-0221pdt: tnn_chat FIT re-cert fresh
re-run, FIT on b4507fb22"; git log --all --grep=FIT shows no 0821pdt
entry; the 0821pdt archive branch contains no chat_fit or tnnchat FIT
files (only pre-existing fitchat0521 scratch and unrelated
generations files). The brief was wrong, and the FIT worker caught it
in the file's own "Record correction" section. Did the error infect
the baseline choice or the precondition analysis? Trace: the brief's
numbers (30/30 declines, 0 blanket refusals, 17/17, 10/10, 9/9) match
the 0221pdt record TNCHAT_FIT_0221.md exactly, so the brief carried the
right numbers with the wrong wave label. The worker then checked
three candidate archive branches, including the true last-certified
0221pdt one, so the correction widened the check rather than
narrowing it. The worker also corrected the merge count: three merges
(b043e9ea1, 0ca683756, 9526cdb5c), not two; I verified all three
exist between b4507fb22 and 9526cdb5c. Concession: the attack fails on
the evidence. The briefing error did not infect the verdict, and the
worker self-corrected with verifiable citations. Residual process
note: the coordinator's brief was written from memory, not from the
repo record; briefs should cite commit SHAs for "last certified"
claims.

### Attack (b): structural fragility of the FIT re-certification process

Precondition (2) failed because the baseline instrument source
tnn_chat.zag is absent from all three checked archive branches: the
09-23 run directories holding it were pruned. I spot-verified the
pattern (present at frozen sha in the 2321pdt archive branch, absent
at that path in the 0221pdt archive branch), consistent with the
worker's full .zag content-scan claim. The standing note to freeze FIT
instrument sources into a never-pruned authority path was never acted
on; docs/lab/bytegen/authority_law/dialogue/ holds only the R33
support sources, and the hazard was already noted at 0221pdt/0821pdt.
Did this wave's fresh re-run repair the process or repeat the
workaround? It repeated the workaround: sources scavenged from older
run dirs, sha-verified, rebuilt, re-run. The certification for this
wave is epistemically valid (frozen shas matched byte-exact, 2/2
binary reproducibility, 9/9 rerun determinism), but the process is
structurally fragile in a bounded, self-detecting way: the standing
rule (precondition 2) caught the failure and forced the re-run rather
than silently passing. That is the governance working as designed.
The attack lands halfway: the re-run repairs this wave's
certification, not the process. Until the authority-path freeze
happens, every future carry-over check will fail precondition (2)
and force a scavenger-hunt re-run. The file already carries this as
an "Open hazard for the coordinator" with a concrete recommendation;
the skeptic's addition is that this is now a three-wave-old open
hazard, and "recommended follow-up" is becoming "deferred
maintenance".

### Attack (c): does re-running frozen probes on an unchanged chain measure anything new?

Steel-man: precondition (3) showed the enumerated chain byte-unchanged
across all three merges (zero diff lines per range), the toolchain is
pinned by sha, and determinism was already established (9/9
run-pairs). If the chain is unchanged and the toolchain is unchanged,
then re-running the identical frozen probe set is nearly entailed by
prior evidence: the only live variable is the build and execution
environment at the new HEAD. The marginal information gain is (i)
binary reproducibility on the new HEAD (2/2 PASS, byte-identical to
frozen 1ada2fae and 20273a99), (ii) confirmation that the
sha-verified scavenged sources still rebuild and run clean on this
host, and (iii) 9/9 rerun determinism plus output hashes
byte-identical to prior records. That is real but small: a
stability re-verification, not a discovery. The PASS is not vacuous
(it did check something: toolchain/host determinism on the new HEAD),
but its evidential yield beyond precondition (3) + (4) + sha
verification is thin, and its real function is procedural: the
standing rule forces a fresh re-run whenever precondition (2) fails.
Concession: the file labels the result [RE-CERT] and states "this is
not a candidate verdict", which is the honest tag. No overclaim
detected here, only a measured verdict that the numbers are a
re-confirmation of an unchanged artifact.

### Attack (d): scope honesty of the FIT verdict

The file communicates scope without overclaim, and it does so
explicitly in three places: the header ("Path taken: FRESH RE-RUN.
this is not a candidate verdict and it is not merge review of the
merged-in work; it certifies the 38-fact closed-book probe chain
only"), the "Literal scope" section (working HEAD is post-merge; the
merge folded Micah's PAM/MATH work, which is CLOSED and not
re-litigated; nothing in his merged-in frontier files was touched),
and the "Caveats (plain language)" section (closed-book probe
instrument, not an open-domain conversational model; the decline
binary is a supervised red-team probe instrument, not a general
interactive TNN; no live learning, no open-domain conversation). One
sentence to watch: "The merges since b4507fb22 introduced no
observable FIT deviation" could be misread as certifying the merged
work, but the surrounding scope statements immediately foreclose that
reading. Concession: the attack fails. The scope communication is
exemplary and should be the template for future FIT reports.

### Cost

The fresh re-run cost is modest: 2 rebuilds and 15 probe runs, all
shell-driven. But it was forced by a preventable precondition failure
(the unfixed authority-path freeze), so its real cost is not compute
but process: a third consecutive wave of scavenger-hunt re-runs while
the standing note sits unactioned. The coordinator should either
action the freeze or explicitly downgrade the standing note; leaving
it open while repeatedly working around it is how process debt
normalizes.

### Item 2 verdict as skeptic

FRESH FIT PASS on 9526cdb5c5 stands. The briefing error was caught
and did not infect the verdict; the scope is communicated without
overclaim; the re-run is a valid but thin re-confirmation of an
unchanged chain, honestly tagged [RE-CERT]. The process remains
structurally fragile on precondition (2), the failure was
self-detected by design, and the three-wave-old open hazard (freeze
the FIT instrument sources into a never-pruned authority path) is the
real finding of this item.

---

## Cross-cutting notes for the judge

1. Counting discipline: both verdicts pad headline counts with
   disclosed duplicates (fork battery: 31 executions / 24 unique
   commits / 2 unique live commits). Disclosed padding is honest; only
   ensure the short form never travels without the caveat.

2. Neither confirmation touches Micah's new frontier code. The fork
   battery never executes it; the FIT report explicitly closes it
   out of scope. The wave is clean on its own terms, but it is a
   quiet wave by design: two process re-certs, zero candidates, zero
   frontier coverage.

3. Zero Python contact is claimed in both files with explicit
   statements (shell coreutils only, no python3 invocation, no
   Python scratch files including /tmp). Nothing in the evidence
   contradicts these claims.

4. No commits were made by either worker; the coordinator commits.
   Nothing pushed. No frozen bar was weakened. No em-dash in this
   report, per the loop documentation style rule.

5. Recommended follow-ups for the coordinator: (i) action or
   explicitly retire the FIT authority-path freeze note; (ii) require
   briefs to cite commit SHAs for "last certified" claims; (iii)
   stamp fork-battery verdicts with the toolchain-stability-only
   scope line; (iv) reword "previously untested tips ... explicitly
   NOT untested" to "transitively covered for current-tip purposes".
