# Judge rulings: wave-20260925-1421pdt debate group

Independent judge. Evidence read in full before ruling:
- forks/FORK_RESULTS_1421.md
- chat_fit/FIT_1421.md
- debate/ADVOCATE_BRIEF.md
- debate/SKEPTIC_REPORT.md

Standing context: this wave ran two process confirmations, no new
candidates. Nothing was added to or removed from Micah's sealed judge
queue; his six governance rulings and nine sealed pairs are untouched.
Owner red lines held across the wave: pure Zag only, zero Python
anywhere, commits stay local, no push, no frozen bar weakened. I do
not commit; the coordinator commits.

Provenance-probe check: the skeptic's verbatim probe ("What is the
provenance of the artifacts under judgment, and what exactly is new
versus inherited?") appears verbatim before Item 1 (line 21) and
before Item 2 (line 184) of SKEPTIC_REPORT.md. Certification is intact
for both items; neither ruling is void.

---

## Item 1: Fork battery, draft verdict CONFIRM [RE-CERT] 31/31 PASS

RULING: CONFIRM, with MODIFY to the verdict line.

The cited evidence decides it. The results file states "Entries total:
31" and "Unique commits tested: 24" in the same section and names all
7 redundant entries explicitly; 31 minus 7 equals 24, matching its own
arithmetic. The skeptic independently verified this and found no
internal contradiction: 1 local plus 12 archive branches plus 1
wave-debate-session-1-backup plus 2 origin entries plus 5 FETCH_HEAD
remote heads plus 7 forktest worktrees plus 3 wave3 worktrees equals
31; live 3 plus fixture 28 equals 31. "31/31 PASS" is literally true:
31 enumerated forks were tested and 31 passed (OVERALL=PASS on 31/31
RESULT.txt files, harness exit 0 VERDICT=PASS on 31/31), the pinned
znc sha 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
matched on every fork, NEG1 and NEG2 discriminated as required on all
31. Zero Python contact is attested and uncontradicted. The origin tip
did not move during the run: run-start tip
93f0fd54c82cf2af6b1a699b6e56f003707fdc2f and the closing read-only
ls-remote tip are verbatim identical, so CANNOT-CONFIRM count zero is
earned.

The skeptic's four attacks land in substance but not in a way that
overturns the draft. On (a): the 24 unique-commit count is disclosed
in the same breath as 31/31, so the file is not deceptive, but the
short form must never travel without the duplicate caveat. On (b):
"Live: 3" counts live entries; unique live commits are 2
(local-tnn-native-lab and origin-tnn-native-lab, with the
runstart-tip entry an explicit duplicate of the latter), and the file
never says that sentence. On (c): the battery certifies toolchain and
extraction stability only. It never executed the merged frontier code
(local moved 0ca683756 to 9526cdb5c, origin moved 84ed45077 to
93f0fd54c), so a defect in Micah's frontier code would sail through
31/31 PASS. The file makes no such claim itself; the risk is
downstream, and the verdict must carry the scope stamp. On (d): the
ancestry checks on 695997f5 and 236e5a17815f re-verified YES, but
ancestry proves provenance containment, not direct behavioral testing,
so the sentence "they are explicitly NOT untested this wave" is
overstated and must be reworded. None of these invalidate a PASS; they
narrow what the PASS means. That is exactly what MODIFY is for.

Modifications ordered:

1. The verdict line as recorded must read, verbatim:
   "CONFIRM [RE-CERT]: 31/31 entries PASS, 24 unique commits
   (live entries 3, unique live commits 2); certifies toolchain and
   extraction stability only, not the contents of the moved commits."
2. The sentence "they are explicitly NOT untested this wave" in the
   results file is ordered reworded to: "the previously untested tips
   695997f5 and 236e5a17815f are transitively covered for
   current-tip purposes via confirmed ancestry of 93f0fd54c; they
   were not directly tested at their own tips."
3. Precedent P1 (load-bearing): fork-battery verdict lines must
   always carry entry count, unique-commit count, unique live-commit
   count, and the toolchain-stability-only scope stamp. A short form
   like "31/31 PASS" must never travel without the duplicate caveat.

Rationale for CONFIRM rather than OVERTURN: every number the draft
verdict rests on is corroborated by the skeptic's independent
verification; the attacks disclose context the draft should carry,
not errors that void the result. Overturn requires cited evidence
that the result is false; there is none.

---

## Item 2: tnn_chat FIT, draft verdict FRESH FIT PASS on 9526cdb5c

RULING: CONFIRM. The draft verdict stands unmodified.

The cited evidence decides it. The coordinator's brief misstated the
last FIT wave (said 0821pdt; the true last certified FIT is
wave-20260925-0221pdt, commit f2b8126ba, on b4507fb22; no 0821pdt FIT
evidence exists in the repo record). The skeptic independently
verified this error, and it did NOT infect the verdict: the brief's
numbers match the 0221pdt record TNCHAT_FIT_0221.md exactly, the
worker self-corrected in the file's own "Record correction" section,
checked three archive branches including the true 0221pdt one, and
corrected the merge count to three (b043e9ea1, 0ca683756, 9526cdb5c),
all three chain diffs returning zero lines. Precondition (2) of the
standing carry-over rule failed honestly: the baseline tnn_chat.zag
(frozen sha c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c)
is absent from all three checked archive branches after the 09-23
run-directory pruning, and the skeptic spot-verified the pattern. The
rule therefore required a fresh re-run, which was performed.

The re-run numbers are complete and all cited: binary reproducibility
2/2 PASS on HEAD 9526cdb5c, both rebuilds byte-identical to the frozen
records (decline 20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7,
baseline 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c);
KB1 30/30 specific declines with 0 blanket refusals across 3 runs;
KB2 17/17 answered, 0 declines, byte-identical baseline parity across
3 runs; KB5 10/10 answered, 0 declines, byte-identical baseline parity
across 3 runs; rerun determinism 9/9 run-pairs byte-identical; all
three output hashes byte-identical to prior wave records (a2ca4dd7...,
e05fb4ec..., 4f1603aa...). Zero Python contact is attested and
uncontradicted. The scope is communicated without overclaim in the
header, the literal-scope section, and the plain-language caveats;
the PASS is honestly tagged [RE-CERT] and states it is not a candidate
verdict and not merge review. Nothing in the evidence contradicts the
PASS.

The skeptic's structural-fragility attack lands halfway and is
accepted as a finding, not as grounds to overturn. The re-run is a
valid but thin re-confirmation of an unchanged chain: its marginal
information gain is toolchain and host determinism on the new HEAD
plus binary reproducibility, which is real but small. That thinness
does not void the result; the standing rule forces the re-run
whenever precondition (2) fails, and the rule worked as designed
(failure self-detected, not silently passed). The real finding of
this item is process: the standing note to freeze FIT instrument
sources into a never-pruned authority path is now three waves
unactioned, and the re-run repeated the scavenger-hunt workaround
without repairing the fragility.

Ordered actions:

1. Record the brief-error correction in the wave record: the last
   certified tnn_chat FIT before this wave was wave-20260925-0221pdt
   (commit f2b8126ba, FIT on b4507fb22), not 0821pdt. This wave's
   carry-over baseline was correctly taken from 0221pdt.
2. Re-issue the authority-path freeze as a standing directive (this
   replaces the repeated recommendation): the coordinator will freeze
   tnn_chat.zag (frozen sha c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c)
   and tnn_chat_decline.zag (frozen sha
   a87011fe10dbc5bac5b0d6e36391033974acfcc46b852618989e3e800cbc3e4b)
   into a never-pruned authority path (docs/lab/bytegen/authority_law/dialogue/
   or a sibling never-pruned path), or explicitly retire/downgrade the
   standing note with a stated reason, no later than the next wave.
   Leaving it open while repeatedly working around it normalizes
   process debt.
3. Precedent P2 (load-bearing): coordinator briefs must cite commit
   SHAs for "last certified" claims. Briefs written from memory are
   how this error happened; the record is the source of truth.

Rationale for CONFIRM rather than OVERTURN: the briefing error was
caught by the worker and independently shown not to infect the
baseline choice or the precondition analysis; the scope statements
foreclose any overclaim; the re-run's evidence is a valid
re-confirmation, honestly labeled. Overturn requires cited evidence
that the result is false; there is none.

---

## Precedents and standing notes adopted (kept few and load-bearing)

P1. Fork-battery verdict lines always carry: entries tested, unique
commits tested, unique live commits, and the scope stamp "toolchain
and extraction stability only, not the contents of the moved commits".
Short forms never travel without the duplicate caveat.

P2. Coordinator briefs must cite commit SHAs for "last certified"
claims.

P3. Ancestor-transit claims must be worded as "transitively covered
for current-tip purposes; not directly tested at their own tips".

D1. Standing directive (re-issued, escalated): freeze the two frozen
FIT instrument sources into a never-pruned authority path, or
explicitly retire the note with a stated reason, no later than the
next wave.

Carried context: CV-P and COMP-2 adoption remain barred pending
Micah's governance ruling 6; the D1 intelligence lane is closed by
honest survey; G1 sunshafts and the D-VID-1 lane stand down.

---

## Final verdict slate for LOOP_STATE.md

1. Fork battery: CONFIRM [RE-CERT]: 31/31 entries PASS, 24 unique
   commits (live entries 3, unique live commits 2); certifies
   toolchain and extraction stability only, not the contents of the
   moved commits. (Verdict line modified per order; results file
   sentence reworded per order 2 above.)
2. tnn_chat FIT: FRESH FIT PASS on 9526cdb5c5d5de732c87583f29d09418894cf8b8
   [RE-CERT]. Brief-error correction recorded (last certified FIT was
   wave-20260925-0221pdt, commit f2b8126ba, not 0821pdt). Standing
   directive D1 re-issued on the authority-path freeze.

Nothing added to or removed from Micah's sealed judge queue. Six
governance rulings and nine sealed pairs untouched. No candidate
verdicts. No em-dashes were used in this file, per the loop
documentation style rule.
