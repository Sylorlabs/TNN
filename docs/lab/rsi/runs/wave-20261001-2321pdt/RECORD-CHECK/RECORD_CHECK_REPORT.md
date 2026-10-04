# RECORD-CHECK report: wave-20261001-2321pdt WAVE_RECORD.md consistency check

Worker: RECORD-CHECK lane (replacement). Toolchain guard Step 0 PASS (python3 absent; see NAMECHECK.md).
Scope: read-only verification of the wave record. No record edits made; fixes are the coordinator's.

## (c) Verdict count: CONFIRMED 44

44 verdict lines enumerated between "## Verdicts" and "## Queued next" (grep count matches manual enumeration).
Lane coverage: 10 of the 11 spawned lanes have verdicts. SENSORY has no verdict yet; the record is honest about this: RT-SENSE states "SENSORY lane still running; needs red-team coverage when it lands." The "(debate pending)" markers and the header note "Debate group: convened after lanes land" are consistent with a still-running lane.

## (a) Contradictions and superseded claims

### A1. CONTLEARN "LEARNOWN-DEMONSTRATED" superseded by CONTLEARN-OWNED "MACHINERY-DEPENDENT", with no annotation (same pattern as the fixed H7R/H6R case)

Earlier line:
"- CONTLEARN (learner-owned push): BUILD-PASS, LEARNOWN-DEMONSTRATED [NEW] (debate pending)."
Later line:
"- CONTLEARN-OWNED (learner-owned integration discrimination): MACHINERY-DEPENDENT [NEW]. ... the integration work sits on the researcher side of the control-plane line. Per-bar: CO-1 FAIL (TREAT 0/6 vs DEMONSTRATED bar); ..."

The later verdict directly tests the earlier verdict's claim and overturns it: TREAT integrates 0/6 fresh 2-hop chains while the unmodified frozen core integrates 6/6, and the verdict states "The red-team QUALIFY stands, strengthened by a clean discrimination." Unlike the H7R/H6R fix (the H7R line carries the parenthetical "(Note: the "3/3 passing" claim in the worker's report is superseded by the H6R BUILD-FAIL verdict recorded below...)"), the CONTLEARN line carries no supersession note. A reader of the CONTLEARN line alone would not learn that LEARNOWN-DEMONSTRATED was falsified by the follow-up discrimination lane.

Mitigating context (recorded, not a fix): RT-INT already carried the qualification "CONTLEARN "LEARNOWN-DEMONSTRATED" label hazard, keep the weak/strong distinction attached when cited," and the CONTLEARN verdict itself disclosed "does NOT claim learner agency (H2-v2/H3 stand)" and "workspace is the single frozen arena (weak H10 sense)." The factual conflict on the DEMONSTRATED claim remains unannotated. RECOMMENDATION: coordinator adds a supersession note to the CONTLEARN line mirroring the H7R fix.

### A2. TNN3-SUBSTRATE "Unblocks H2R/H6R/H7R" vs H6R BUILD-FAIL (observation-level, partial tension)

TNN3-SUBSTRATE line: "Frozen kill bars KB-H2R/H4R/H6R/H7R for the re-attempts. Unblocks H2R/H6R/H7R and H4R's construction half."
H6R line: "BUILD-FAIL ... B1 (trajectory discrimination) PASS; B2 (integration) PASS; B3 ... KILL FIRES ... B4 (retention) SUBSTRATE-INSUFFICIENT ... This is a crisp substrate design gap for the governance record (TNN3-SUBSTRATE adoption pending)."

The package did unblock H6's B1/B2, but the H6R re-attempt still BUILD-FAILs on B3/B4 because of a design gap in the package itself (standing records never protection-pinned, lbid 0 invisible to the selector). The blanket "Unblocks H6R" statement, written before the H6R verdict, is not borne out and carries no qualification note. Weaker than A1 (TNN3-SUBSTRATE is a DESIGN verdict, and RT-GOV pre-disclosed the lbid residual "may need H6R override"), but a coordinator annotation would keep the design recommendation honest.

### A3. BATTERY-E4 verdict cites the wrong prereg commit (record error, needs coordinator fix)

BATTERY-E4 line: "All process bars PASS (prereg b63f80289 strictly first; ...); ... Commits: b63f80289 (prereg) -> 5a2c7c91c (prereg restore after incident) -> ... Incident: H5R2-SKEPTIC2 worker commit f461e812d accidentally deleted BATTERY-E4/PREREG_E4.md and NAMECHECK.md (411 deletions); restored byte-identical before any implementation commit; E4-K1 holds."

Verified in git: b63f80289 is ARENA5's prereg commit ("ARENA5: freeze DEFRECALL prereg (autonomous goal completion by generic default recall) + NAMECHECK Step 0"), not BATTERY-E4's. The BATTERY-E4 lane's real commits (all resolve): 5a2c7c91c (prereg restore, content SHA b3fd77c2), f26ddb294 (worlds), 67680ebb1 (tools), 61df738fe (runs + verdict). ARENA5's real chain (all resolve): b63f80289 (prereg) -> f3320caf8 (Amendment 1) -> 2320c3454 (implementation) -> 6582398e9 (sealed eval).

So the BATTERY-E4 line's "prereg b63f80289 strictly first" and the E4-K1 commit-order claim cite a commit belonging to a different lane. The true original E4 prereg commit id is unrecoverable from the record (it was deleted by f461e812d; only the byte-identical restore in 5a2c7c91c exists). DO NOT FIX as a worker; the coordinator should correct the E4 commit chain and decide what E4-K1 rests on. (The ARENA5 line's use of b63f80289 is correct.)

### A4. H7R trailing line "Dispatched ARENA5 as the replacement build" has no supporting linkage (possible copy error, unverifiable)

H7R line ends: "No L3 authorship claim made. (Note: ...superseded...) Dispatched ARENA5 as the replacement build." The ARENA5 verdict describes DEFRECALL following ARENA4's roster work; nothing in the record links ARENA5 to H7R's substrate re-attempt or explains what it replaces. Flagged for the coordinator to check; no contradiction provable from the record alone.

## (b) Verdicts missing required elements

- H6R BUILD-FAIL: the only verdict line with NO commit ids anywhere in it (no "Commits:" segment, no prereg/implementation references). Label, frozen bars (KB-H6R), and numbers (50/80 vs 50/80, margin 0 vs bar >= 15; P3 3/3) are present.
- Fork battery: no single verdict label word (PASS/FAIL); it is a battery summary with full counts (59 refs: 2 FRESH PASS + 55 RE-CERT PASS + 2 UNTESTABLE + 0 FAIL; archive 47/47 + 1 new = 48/48), frozen pins, and commit 668ae8d8f. Acceptable as a report but noted.
- All other 42 verdict lines carry a label, the frozen bars or decision rule, numbers, and commit ids. All cited commit ids resolve in git (108 unique ids checked; the 4 non-resolving tokens, 19dcf2e4, 36f5047d, 6f2b155b, aee1b6f2, are binary SHA-256 prefixes, not commit references). Spot-checked ancestor claims hold (00b31af53 < ec52cf1ca; dc7df4aba < 9db334bd4). Every referenced lane dir exists under the wave dir.

Record-maintenance gaps (not verdict defects): "## Commits this wave" still reads "(to be filled as lanes land)"; "## Queued next" still reads "(to be filled)."

## Red-team qualifications: ALL RECORDED

- RT-SENSE on DEVANG3: QUALIFY (not dissent, not clean holds); BUILD-PASS stands; K_SEAL non-discrimination vs fixed-width-3 control recorded.
- RT-HPIREV2: Part 1 QUALIFY (Q1 certification defect, Q2 rank-diagnosability load-bearing); Part 2 bound PARTIALLY survives (ADV-S4 break, ADV-M1 silent success confirmed).
- RT-ARENA5: QUALIFY (BUILD-PASS stands); extensional-equivalence-on-this-battery qualification recorded.
- RT-GOV: HOLDS on all three axes, one QUALIFY (Amendments 1-2 amendment-discipline flag); five escalation decisions listed.
- RT-C174: EVIDENCE-HOLDS with carried qualifications (bar (c) = shared-code fallback; bar (d) = K-H3-world compat).
- RT-INT: EVIDENCE-HOLDS with carried qualifications (CONSEQ independent-adversary clause never met; CONTLEARN label hazard).
- RT-EXEC: EVIDENCE-HOLDS on F1 and TNN3H5R, with explicit UPHOLD BUILD-FAIL recommendation.

## (d) Other issues

- The H7R/H6R contradiction named in the task brief is present and already fixed (the H7R parenthetical note supersedes the worker's "3/3 passing" claim; substrate halves recorded as H2R PASS, H7R PASS, H6R FAIL). H2R itself is a prior-wave verdict, correctly not counted among the 44.
- 15-vs-16 capability count: the ARENA verdict flags it ("the "15 capabilities" count does not reproduce from sealed records (16 capabilities, 68 items; flagged, not asserted)") and ARENA4 repeats the flag. Internally recorded; sealed records govern. Not hidden.
- F2V3 header says "F2 v4 depth-9 candidate" while the lane was spawned as "F2v3"; the verdict body is internally consistent ("the fix from the v3 BUILD-FAIL"). Minor naming drift only.
- S-prime seed accounting is consistent across F1-REPAIR and F1-REPAIR2: 9/9 (5100) + 11/11 (6100) + 7/7 (7300) = 27/27 degenerate-path seeds.
- H5R2 claim chain is explicitly annotated at each step: BASELINE-MATCHES -> DECOY-DISCRIMINATES ("BASELINE-MATCHES is RESOLVED, not contradicted") -> SKEPTIC-SURVIVES ("necessity STILL UNPROVEN against this skeptic, reported honestly"). No hidden contradiction.
- BATTERY-E3's "reframes every construction observation" mandate is answered for ROSTER by ARENA-BLIND (ORACLE-FREE); no record claim asserts the mandate was executed for other mechanisms. No contradiction.
- Fork battery arithmetic checks: 2 + 55 + 2 + 0 = 59 refs; 47/47 + 1 new = 48/48 archive.
- No verdict references a nonexistent lane: all lane dirs (ARENA, ARENA2-5, ARENA-BLIND, BATTERY, BATTERY-CLUSTER, BATTERY-E1/E2/E3/E4/E5/E6/E8, C174, C9BAT, CONSEQ, CONTLEARN, CONTLEARN-OWNED, DEVANG3, F1, F1-BUFFER, F1-FOLLOWUP, F1-REPAIR, F1-REPAIR2, F2V3, FORK, H5R2-BASELINE, H5R2-DECOY, H5R2-REPRO, H5R2-SKEPTIC2, H6R, H7R, HPIREV2, RT-ARENA5, RT-C174, RT-EXEC, RT-GOV, RT-HPIREV2, RT-INT, RT-SENSE, SENSORY, TNN3-SUBSTRATE, TNN3H5R) exist.

## Summary for the coordinator

Two items need coordinator action (worker must not edit the record):
1. A1: annotate the CONTLEARN line to record that LEARNOWN-DEMONSTRATED was superseded by CONTLEARN-OWNED's MACHINERY-DEPENDENT (mirror the H7R/H6R fix note).
2. A3: correct the BATTERY-E4 commit chain (b63f80289 belongs to ARENA5; E4's true chain starts at the restored prereg 5a2c7c91c) and rule on what E4-K1 rests on.
Optional: annotate A2 (TNN3-SUBSTRATE "Unblocks H6R" vs H6R BUILD-FAIL), check A4 (H7R "Dispatched ARENA5" linkage), add H6R commit ids, fill "## Commits this wave" and "## Queued next".
