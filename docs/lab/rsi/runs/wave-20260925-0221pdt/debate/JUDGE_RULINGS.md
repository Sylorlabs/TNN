# JUDGE RULINGS: wave-20260925-0221pdt mandatory debate

Judge: independent leaf agent. Working copy ~/workspace/tnn-rsi, branch
tnn-native-lab. Read: ADVOCATE_BRIEF.md, SKEPTIC_REPORT.md (provenance
probe verified present verbatim), EVIDENCE_V3_0221.md,
REDTEAM_V3_0221.md, JUDGE_BRIEF.md, FORK_RESULTS_0221.md,
TNCHAT_FIT_0221.md, PREREG_CV1_FALLBACK_0221.md,
MEASUREMENT_CV1_FALLBACK_0221.md. Independently re-verified the
load-bearing numbers with git and shell reads only. Zero Python contact
with any wave artifact in this judging. No commits made by the judge;
the coordinator commits. The sealed judge queue, Micah's frontier
files, and the governance ruling items were not touched.

## 1. Verdicts

### (1) D-VID-1 V3: DEAD [NEW] upheld. Skeptic attacks (a) and (b) both rejected.

The coordinator's DEAD verdict stands. The killing evidence is the
frozen T1-GC bar, measured from the committed verify_v3.log in commit
81e33f192: T1GC_baseline_pm=572, T1GC_variant_pm=572, T1GC_BAR=FAIL.
The bar requires variant*1000 >= baseline*1300, i.e. 572000 >= 743600,
false, ratio 1.000 against the frozen >= 1.30. The tie is not an
average-only artifact: all 47 consecutive pairs tie exactly
(pair 0: 398=398, pair 23: 626=626, pair 46: 647=647). G-LIVE passes
(independent red-team re-verification, G1/G2/G3). VKB1 passes (48/48
frames byte-identical across three renders, red-team spot-checked 7 of
7 frames against the manifest). T2 passes (variant min 859 / max 1074 /
mean 976 inside [50, 1500)); T3 passes (variant f0=1607, f47=1543 vs
baseline 1608/1543). VKB3, VKB4 (1.036x), VKB5 pass. VKB6 independent
eye review: no new artifact class, with the plain statement that the
displacement does not read as churning water at normal scale.

Attack (a) (shared verifier defect; DEAD vs UNVERIFIABLE): REJECTED on
independently verified evidence. From the committed verify_v3.log the
same verifier binary on the same run reports T2 per-pair values that
differ between the two sequences: pair 4 A=917 B=916, pair 5 A=917
B=916, pair 12 A=928 B=927, pair 13 A=973 B=972, pair 15 A=951 B=950,
pair 21 A=970 B=969; summaries differ (variant max 1074 vs baseline max
1075, mean 976 vs 977). A verifier that read one sequence twice could
not produce these differences. T3 validates both paths independently
(T3_A_f0=1608, T3_A_f47=1543 against the frozen 1607/1543 within gate;
T3_B_f0=1607, T3_B_f47=1543). The T1-GC validation gate passes
(|572-580|=8 within +-25), so the frozen reference reproduces. The tie
is physically explained by independent measurement (ffmpeg, not the
verifier): foam-channel mean 253.9/255 baseline vs 254.7/255 variant
over a 478x10 sample at f10, only 30 of 4780 sampled pixels differing;
the churn footprint is a ~13 px tall sliver (y 395..408) from
foreshortening at wz about 720. Saturated foam has mask 1 in both
sequences, so displaced resampling flips nothing. The verifier itself
flagged the zero (D1_f10_region_diff_pm=0, D1_DIAGNOSTIC=FAIL) rather
than hiding it.

Ruling on DEAD vs UNVERIFIABLE: DEAD. UNVERIFIABLE requires compromised
evidence. G-LIVE passes, VKB1 holds, both validation gates pass, and
the independent red-team review found no procedure defect. The frozen
verdict mapping (G-LIVE passes and any VKB fails) assigns DEAD. No
sealed pair is prepared.

Attack (b) (2321pdt breach taints the prereg by association): REJECTED.
Git-verifiable timestamps: prereg 0ba679b11 committed ALONE at
2026-09-25 06:47:01 UTC (single-file commit, parent c4f006ea7, exactly
one commit in history touches the prereg path); the breach occurred at
06:55 UTC per BREACH_DISCLOSURE.md with the disclosure committed at
06:55:45 UTC; the 0221pdt implementation commit 81e33f192 came at
2026-09-25 10:21:13 UTC, strictly after. The voided 2321pdt work sits
quarantined in dvid1_geomchurn/void/ for lineage disclosure only and
carries no evidentiary weight; the 0221pdt implementation was built
fresh under the certified prereg (RENDER_SHA
c654ebe4ba3a96361324fdcf362324da30ef857feed4a60202d07d4e00d3827c).
The 2321pdt M4 certification's reasoning stands: taint by association
is not a rule.

Sustained minor correction, with one rejection of the skeptic's
correction: the skeptic's path correction is ADOPTED (EVIDENCE_V3_0221.md
and REDTEAM_V3_0221.md cite
docs/lab/rsi/runs/wave-20260924-2321pdt/dvid1_geomchurn_v3/PREREG_DVID1_V3_2321.md,
but the committed path is
docs/lab/rsi/runs/wave-20260924-2321pdt/dvid1_geomchurn/PREREG_DVID1_V3_2321.md;
the _v3 suffix belongs to the 0221pdt run dir). The skeptic's line-count
correction is REJECTED: I re-checked with git show plus wc -l, and the
committed file is 328 lines at freeze and at HEAD, so the evidence's
"(328 lines)" citation is correct. The coordinator corrects the path
only; no evidence change.

### (2) Fork battery: 27/27 PASS [RE-CERT] confirmed. Count correction ADOPTED.

The 27-row table stands: every enumerated fork ran the full shell
battery plus the rebuilt pure-Zag harness (byte-identical rebuild
a2e6284c...), all 27 PASS, zero CANNOT-CONFIRM, znc sha matched the
pinned 498abcb5... on every fork, NEG1/NEG2 discriminated everywhere.
Evidence commit 5c90fecc8.

The count correction is adopted on the report's own evidence: the
report states that origin-tnn-native-lab-runstart-tip "tests the same
commit as origin/tnn-native-lab this wave," and both rows list
4050b1097941d341c2d02e5efca25fc1877906e5. The genuinely distinct live
forks are 4: local-tnn-native-lab (b4507fb22), origin/tnn-native-lab
(4050b1097), local-archive-1721pdt (088a1914, new this wave),
local-archive-wave-2321pdt (e33b5ddb, new this wave). The record is
corrected to "27 enumerated entries, 4 distinct live forks (plus 1
duplicate entry: runstart-tip at the same commit as origin/tnn-native-lab),
22 fixture forks." Coverage remains adequate: enumeration was fresh
this wave (git branch -a, git worktree list), every fork whose SHA moved
since last wave is in the live set, and the closing origin-tip re-check
held (4050b1097 at run start and at close; independently confirmed).
This correction changes the count sentence only, not the 27/27 PASS.

### (3) tnn_chat FIT: CONFIRM [RE-CERT] on b4507fb22. Precondition-2 failure handling upheld.

The standing rule worked as designed. Carry-over precondition (2) hard
failed: the baseline instrument source tnn_chat.zag (frozen sha
c0776ad6...) is absent from the designated archive branch
tnn-native-lab-wave-archive-wave-20260924-2321pdt (the 09-23 run dirs
were pruned from that snapshot). Per the rule a failure forces a fresh
re-run, not a waiver, and the fresh re-run was performed. Numbers on
HEAD b4507fb22: binary reproducibility 2/2 PASS (decline rebuild
byte-identical to 20273a99, baseline to 1ada2fae); KB1 30/30 specific
declines with 0 blanket refusals on each of 3 runs; KB2 17/17 answered,
0 declines, byte-identical baseline parity, 3 runs; KB5 10/10 answered,
0 declines, byte-identical baseline parity, 3 runs; rerun determinism
9/9 run-pairs byte-identical; all three output hashes (a2ca4dd7,
e05fb4ec, 4f1603aa) byte-identical to the prior wave's records; all 15
runs exited 0 with empty stderr. Evidence commit f2b8126ba.

I independently verified the two load-bearing chain-integrity claims.
First, the merge disjointness: git diff e33b5ddb..b4507fb22 touched
exactly 115 files, all under docs/lab/ambig_1080p, docs/lab/math_logic,
or docs/lab/onebrain, zero paths outside those three, so the merge
introduced no FIT-relevant change. Second, the skeptic independently
re-hashed the baseline instrument from the 0923-2321pdt archive path and
got c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c,
matching the frozen record. The re-run chain is provably the frozen
chain. The literal scope sentences confine the claim to the 38-fact
closed-book probe chain.

Sustained non-verdict finding: archive pruning degraded the carry-over
precondition's usability this wave. Recommend the coordinator freeze
the frozen instrument sources into a never-pruned authority path (see
section 3).

### (4) CV-1 fallback/fail-closed: ACCEPT as MEASUREMENT [NEW], numbers only, no adoption claim.

The item stands as measurement-only evidence. Numbers: M1 24/24 honest
resolutions (A 8/8 truthful fallback, B1 4/4 degenerate guard including
the bare "?", B2 8/8 specific declines, D 4/4 verbatim answers); M2 0
unflagged confabulations; M3 0 false coverage claims (60 distinct quoted
words machine-checked against the frozen kb.txt); M4 per-class
breakdowns as pre-registered; M5 atomic-verification text fired 0/24;
M6 2/2 full sealed runs byte-identical (transcript 3223d24e7... both
runs). Commit order 5abab17a2 (prereg-only, 10:17:08 UTC) <
28865dc75 (seal-only, 10:17:09 UTC) < 575c96d28 (scoring, 10:17:17
UTC) holds; no implementation commit exists this wave (byte-inherited
1721pdt cv1c.zag 6d8fb9f0..., rebuilt binary byte-identical to the
adopted 710d8bc5...). Seal integrity independently verified: PROBES.md
sha 56fbc9b821f24be9ce6b144d57692e9f57a125073639fe0267f5c2e8b0d86b9b
and KEY.md sha 77716c0fa1acecd725b40f9d821ca884ff618be224ed1b52e77c90aa2447416c
re-hashed identically at the seal commit and at scoring time. Zero
sealed probe bytes in the candidate source by static grep. Zero Python
contact stated.

No adoption claim exists in the document. It states: "It makes no
adoption claim, no readiness certification, and no verdict of any kind,"
and closes with "Measurement only. No adoption claim. Baseline
integration remains held pending Micah's Python-mirror ruling." The
baseline-integration hold is respected. This measurement is behavior-path
evidence only and does not pre-judge Micah's ruling (6).

M5 coverage-gap ruling: ADOPTED. The prereg pre-registered path 2 as
unreachable by probe on the frozen KB ("pre-registered reachability
note"), so M5 measured only silence. A reachability argument is an
argument, not evidence: a fail-closed path that cannot fire on the
frozen KB cannot be probe-verified on that KB. Ruling: M5 is barred
from being cited as verification of the fail-closed path in any future
verdict until a fault-injection probe (for example, deliberately
corrupted fact text) observes the firing. Recorded as a standing note.

Self-attestation weakness: ADOPTED as a standing process note, not a
verdict defect. The report discloses self-attestation honestly
("self-attested (single worker session)"), so there is no deception.
Ruling: future sealed measurements require structural
author/implementer separation (different workers for author and
implementer); self-attestation is no longer accepted. This is a
coordinator staffing rule and does not touch any of Micah's rulings.

## 2. Skeptic disclosure ruling: disclosure RECORDED, report STANDS, not tainted.

The skeptic disclosed one read-only python3 one-liner used to
character-check its own draft for dashes: it read and wrote no wave
evidence, and the zero-dash result was re-confirmed with pure shell.
The operative condition of the prospective 0521pdt M4 R1 rule is
"Any Python contact with a new wave artifact voids its wave evidence."
Contact here was with the skeptic's own draft only, and the one-liner's
output was not used as wave evidence (the dash-free status stands on
the pure-shell re-confirmation). The 1121pdt M5 precedent (accidental
python3 -c, no artifact touched, disclosure recorded, memo stood) and
the 1421pdt judge's (e) ("the operative condition is contact with an
artifact; there was none") apply directly. Ruling: the disclosure is
recorded, the skeptic report stands, the report is not tainted.

Required record correction (nit, not a verdict change): the committed
report's sentence "No Python was used at any step of this review" is
inaccurate as written, because the one-liner was Python use by the
reviewer. The coordinator corrects that sentence in the wave record to
"No Python touched any wave evidence or review artifact; this draft's
dash check was re-confirmed with pure shell." This follows the S7/stdout
precedent pattern (disclosed, not voided) without narrowing anything:
no red line is altered and the S7 strike question remains Micah's
ruling.

## 3. Sustained non-verdict findings for LOOP_STATE.md

a. Prereg design lesson (metric-region vs sliver mismatch): ADOPT as a
standing note. The frozen T1-GC region is a ~204 px radius screen circle
while the lever's true footprint is a ~13 px tall foreshortened sliver
(x 419..1016, y 395..408), so the 1.30x bar was unreachable by
geometry, not just by lever weakness. The bar was frozen and is not
weakened; future preregs must match the metric region to the lever's
actual screen footprint, or operate the metric in world space.

b. Prereg path citation correction: ADOPT the path correction
(dvid1_geomchurn, not dvid1_geomchurn_v3) as a required record edit in
EVIDENCE_V3_0221.md and REDTEAM_V3_0221.md. REJECT the skeptic's
line-count correction: the committed file is 328 lines (verified via
git show at freeze and at HEAD), so the evidence's "(328 lines)" is
correct and stays.

c. Fork live-count honesty: ADOPT. Future fork reports state "N distinct
live forks" plus duplicate entries disclosed explicitly, instead of a
bare count that includes duplicates.

d. Never-pruned authority path for FIT instruments: ADOPT as a
coordinator recommendation. Archive pruning removed the 09-23 run dirs
from the designated archive branch and broke carry-over precondition
(2) this wave. The frozen instrument sources (baseline tnn_chat.zag
c0776ad6..., decline tnn_chat_decline.zag a87011fe...,
R33_NATIVE_IO_V1.zag e6379ddb..., R33_NATIVE_SHA256_V2.zag 9824f6db...,
kb.txt 3ef27296..., gaz.txt b75fd113..., the three fixtures) should be
frozen into a never-pruned authority path so future preconditions are
testable without archive archaeology.

e. M5 citation bar: ADOPT as a standing note (see section 1, item 4).

f. Structural author/implementer separation: ADOPT as a standing
staffing rule (see section 1, item 4).

## 4. Governance items: none touched or narrowed.

Confirmed. A grep over this wave's committed docs shows zero mentions
of S7, MD-SSD, S11, S11-AUD, or C12. The CV-1 measurement explicitly
holds baseline integration pending Micah's Python-mirror ruling and
makes no adoption or readiness claim. The M5 bar and the
author/implementer separation rule govern future wave process only; they
do not decide, pre-empt, or narrow any of his six pending rulings
(S7 strike, MD-SSD-1, S11 pull, S11-AUD pull, C12 queue,
Python-mirror-developed logic). The python-mirror question remains his
to decide, and until he rules no newly Python-mirror-developed logic
may be adopted.

## 5. Prereg commit-order self-check: PASS.

D-VID-1 V3: 0ba679b11 (prereg freeze) at 2026-09-25 06:47:01 UTC
strictly precedes 81e33f192 (implementation plus evidence) at
2026-09-25 10:21:13 UTC. The prereg commit is single-file and alone;
the breach disclosure (06:55:45 UTC) postdates the prereg, consistent
with the 2321pdt M4 certification. PASS.

CV-1 fallback: 5abab17a2 (prereg-only, 10:17:08 UTC) <
28865dc75 (seal-only, 10:17:09 UTC) < 575c96d28 (scoring,
10:17:17 UTC). Prereg commit is 1 file; seal commit is 3 files; no
implementation commit exists this wave. PASS.

No UNVERIFIABLE ORDERING items this wave.

## 6. Final verdict table and queued-next list

| item | ruling | tag |
|---|---|---|
| D-VID-1 V3 geometry-churn lever | DEAD stands; killing bar T1-GC 572 pm vs 572 pm, ratio 1.000 < 1.30; skeptic attacks (a) and (b) rejected on cited evidence | [NEW] |
| Fork battery | 27/27 PASS; count corrected to 4 distinct live forks plus 1 duplicate entry, 22 fixtures | [RE-CERT] |
| tnn_chat FIT | FIT confirmed on b4507fb22; fresh re-run mandatory and chain independently verified | [RE-CERT] |
| CV-1 fallback/fail-closed | accepted as measurement-only evidence (24/24 honest, 0 confabulations, 0 false coverage claims, M5 0/24, 2/2 deterministic); no adoption claim; baseline integration held | [NEW] |
| Skeptic python one-liner disclosure | recorded; report stands, not tainted; report sentence corrected in the record | process |
| M5 citation bar | M5 barred from future verdict citations until fault-injection evidence | standing note |
| Author/implementer separation | structural separation required for future sealed measurements | standing note |

Queued-next list:

1. Whirlpool surface-planform: READY-FOR-JUDGE, QUEUED-UNJUDGED (from
the frozen component lineage in JUDGE_BRIEF.md). It was not judged
this wave.
2. Micah's six governance rulings, all still pending and untouched by
this debate: (1) strike S7 vs the narrowed artifact-touch Python test;
(2) MD-SSD-1 keep-with-UNVERIFIABLE vs re-freeze and re-run;
(3) S11 image pull; (4) S11-AUD pull; (5) C12 queue vs pulled as a
confounded stack; (6) whether Python-mirror-developed logic may ever be
adopted going forward.
3. The CV-1 fallback measurement stands as [NEW] measurement evidence
for the baseline-integration question, to be weighed whenever Micah
makes ruling (6); it authorizes nothing by itself.
4. Record corrections for the coordinator when committing: prereg path
citation in EVIDENCE_V3_0221.md and REDTEAM_V3_0221.md (dvid1_geomchurn,
not dvid1_geomchurn_v3); fork "4 distinct live forks (plus 1 duplicate
entry)" sentence in FORK_RESULTS_0221.md; the skeptic report's Python
sentence correction (section 2).
5. Standing notes for LOOP_STATE.md: the prereg metric-region lesson
(3a), the M5 bar (3e), structural author/implementer separation (3f),
and the never-pruned FIT instrument authority path (3d).
