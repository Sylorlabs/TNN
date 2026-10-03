# REPORT: RECLAMATION-H3 (learner-issued unpin)

Date: 2026-10-03. Worker: RECLAMATION-H3 worker (non-ledger task;
claim minting paused).
Prereg: committed alone as e24635d62 (strictly before implementation).
Mechanism: unpin_h3.zag, compiled with the pinned znc
(znc 2026.07.0-dev (edition 2026), byte-identical to
src/tools/toolchain/znc_linux_x86_64_abed8aa1); binary sha256
a9759f7c4bd71b944a6e0e2da69264c6f2f192ba4edef4835c8ee9fdf747223c.
Policies 0,1,3,4,5,6,7, teachers, tests, and the anchor protocol are
carried verbatim from the H1 source; new code is additive only
(policy 8 PIN-UNPIN, policy 9 PIN-STALE control, learner routines,
release trace/audit).

## Verdict: FAIL (21/22 kill bars hold)

3/3 runs byte-identical (sha256
284e3083b80d142dbfa1ae4c1c23260a9077f3ae578cc728cb1a8a9daf2c2bcd).
The 29 anchor conditions are bit-for-bit identical to H1B's frozen
runs (`diff` clean against reclamation_h1b/run1.txt). 21 of 22 kill
bars pass. The single miss is K20 STALE-CONTROL, an owned worker
derivation error in the prereg (not a mechanism defect): the prereg
predicted post=7, ret=20 for UNPINSTALE-A20; the mechanism correctly
produces post=6, ret=17, and the corrected derivation below predicts
the measured values exactly.

### The K20 derivation error (owned)

Policy 9 evicts the 16 oldest-stale pool entries: slots 0..15
(touch stamps 1..16), holding hop-1 and hop-2 keys for i=1..8. The
prereg's derivation said loop3 (owner 4) keeps i=5 (post contribution
1). That was wrong: i=5's hop-1/hop-2 keys are 1051/1052, which live
in pool slots 8/9 -- inside the destroyed set. Correct post-test
accounting: loop1 i=9,10 pass (2); loop2 i=9,10 pass (2); loop3
i=1..5 all fail, i=5 included (0); loop4 i=9,10 pass (2). post=6,
ret=(100*6)/35=17, rawA=2+2+10+5=19. Every measured column of
UNPINSTALE-A20 (pre=35, post=6, ret=17, cf=48, ev=16, drop=0,
bacc=20, rawA=19) matches this corrected derivation exactly, and the
policy-9 code implements the frozen rule verbatim. The error is the
worker's arithmetic in the prereg, same class as H1's K13 error.
Per governance the frozen K20 bar stands as missed; the correction
belongs in a fresh preregistration (H3B), not in an amendment.

### Implementation bug found and fixed (transparently reported)

The first build did not clear a slot's released flag when policy 8
reclaimed it, so one release authorized unlimited re-evictions of
the same slot (UNPIN-A20 measured ev=16/drop=0 instead of the frozen
ev=8/drop=8; UNPIN-WRONG hammered a single slot, ret=94 instead of
71). The frozen derivation notes specify consume-once semantics
("the remaining 8 relocations find no released slot -> drop=8"),
so the code was brought into conformance with the frozen spec: the
released flag is cleared when the slot is reclaimed. No frozen
number, bar, or design element was changed. Recompiled, re-ran 3/3
byte-identical; all H3 bars then matched the frozen predictions
except K20 (the derivation error above, which is independent of
this fix -- policy 9 never reads released flags).

## Results (identical across run1/run2/run3)

Anchors (29): bit-for-bit identical to the H1B frozen table
(IMPCON/IMPPIN/IMPLIV/IMPFIFO/IMPPART/IMPLRU rows; IMP rows with
policy 7; IMPADV-M2 ret=71; IMPADV3-M2 ret=14/post=5/rawA=20).

| cond           | pol | pre | post | ret | cf | ev | drop | bacc | rawA | rel | av | ai | lc | ar |
|----------------|-----|-----|------|-----|----|----|------|------|------|-----|----|----|----|----|
| UNPIN-B0       | 8   | 35  | 35   | 100 | 28 | 0  | 0    | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-A20      | 8   | 35  | 35   | 100 | 48 | 8  | 8    | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-A32      | 8   | 35  | 35   | 100 | 60 | 8  | 20   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-M2       | 8   | 35  | 35   | 100 | 68 | 8  | 28   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-M3       | 8   | 35  | 35   | 100 | 88 | 8  | 48   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-X2       | 8   | 35  | 35   | 100 | 68 | 8  | 28   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-SILENT   | 8   | 35  | 35   | 100 | 40 | 0  | 8    | 20   | 35   | 0   | 0  | 0  | 12 | 0  |
| PINCTRL-SILENT | 3   | 35  | 35   | 100 | 40 | 0  | 8    | 20   | 35   | 0   | 0  | 0  | 12 | 0  |
| UNPIN-WRONG    | 8   | 35  | 25   | 71  | 48 | 13 | 3    | 20   | 30   | 13  | 8  | 5  | 12 | 5  |
| UNPINSTALE-A20 | 9   | 35  | 6    | 17  | 48 | 16 | 0    | 20   | 19   | 8   | 8  | 0  | 12 | 0  |

Kill bars:
- K1 ANCHOR-CONSENT: PASS. K2 ANCHOR-PIN-MULTI: PASS.
  K3 ANCHOR-CONSENT-MULTI: PASS. K4 ANCHOR-FIFO: PASS.
  K5 ANCHOR-PART: PASS. K6 ANCHOR-LRU: PASS.
  K7 ANCHOR-LIVENESS: PASS.
- K8 IMP-COLD-SAVED: PASS. K9 IMP-MULTI-SAVED: PASS.
  K10 IMP-BEATS-LIVENESS: PASS. K11 IMP-BEATS-CONSENT-CAPACITY:
  PASS. K12 ADV-GAMED: PASS. K13 ADV-DOSE: PASS (corrected
  ret=14/post=5/rawA=20). K14 ADV-FIXED: PASS.
- K15 DETERMINISM: PASS (3/3 byte-identical).
- K16 UNPIN-ALIGNED-CAPACITY: PASS (ret=100 throughout;
  drop = relocations - releases exactly: 16-8=8, 28-8=20).
- K17 UNPIN-MULTI: PASS (ret=100, ev=8, drop=28/48/28).
- K18 AUTHORITY: PASS (UNPIN-SILENT == PINCTRL-SILENT bit-for-bit
  in all 13 numeric columns; ev=0, drop=8 both).
- K19 COLD-PROTECTED: PASS (a_released=0 in all six aligned
  conditions).
- K20 STALE-CONTROL: FAIL (measured ret=17/post=6/rawA=19/ev=16;
  frozen bar demanded ret=20/post=7; owned derivation error, see
  above; the corrected derivation predicts the measured row
  exactly).
- K21 WRONG-RELEASE: PASS (ret=71, post=25, rawA=30, ev=13,
  drop=3, releases=13, audit 8 valid / 5 invalid, a_released=5).
- K22 LEARNER-INTACT: PASS (lcheck=12 in all 10 H3 conditions).

## Answers to the parent questions

(1) Does learner-issued unpin relocate the death decision? Yes,
behaviorally: K18 proves the mechanism cannot reclaim without
learner releases (policy 8 with a silent learner is bit-for-bit
no-reclaim pinning); K16/K17 prove capacity is exactly the
learner's release behavior (drop = relocations - releases, no more,
no less); K21 proves the failure locus is the learner's judgment
(the audit names the 5 invalid releases; retention pays exactly
for those 5).

(2) Is the learner's judgment just another policy in disguise? The
K19/K20 pair discriminates: the same "staleness" intuition as a
learner judgment (belief + revision history, K19: releases zero A
entries, ret=100) vs as a mechanism rule (primary comparison,
K20: destroys 16 cold entries, ret=17). The two authorities produce
opposite retention under otherwise identical protocol. A disguised
policy could mimic either row; it cannot produce both from
different authorities unless the authorities differ. The honest
residual: the simulated learner's rule is simple (belief
reconciliation over a revision log); the structural claim
demonstrated is decision-authority relocation, not a new kind of
intelligence. Only the REVISED reason is exercised; there is no
sealed post-freeze adversary.

(3) Does H3 beat H1B? On authority, not on the aligned adversary:
H1B's policy 7 restores more capacity under the aligned adversary
(IMP-M2: ev=28/drop=0 vs UNPIN-M2: ev=8/drop=28) because importance
reclaims churn history the learner never held. H3's advantage is
structural: retention of learner-held knowledge is 100 by
construction (the mechanism cannot violate it), and the miss case
is graded and auditable (K21) rather than a silent boundary.
H1B's miss case (adversarial importance inflation, ret 71->14)
remains the sharper capacity story; H3's miss case (learner never
releases -> the measured pinning leak; learner releases wrongly ->
audit-named retention price) is the honest failure mode of the
authority relocation.

## Honest caveats (from the prereg, unchanged)

- The learner is simulated; its "judgment" is belief
  reconciliation over its own revision history. The claim is
  decision-authority relocation, tested behaviorally.
- Only the REVISED reason is exercised; INCORPORATED/SUPERSEDED
  are the same unpin path, not run here.
- No sealed post-freeze adversary-designed world; adversaries are
  the frozen H1B mechanism stressors.
- The WRONG condition's corrupted log is harness-injected to model
  learner fallibility; the honest measurement is the audit's
  detection and the exact retention price.
- Owner-scoped reads retained; the label-free routing caveat
  carries over.
- No repair proposed or canonized: measured prices are evidence.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which
python` return nothing under that PATH (verified 2026-10-03 at
startup and before compile); no forbidden executable invoked at any
point (shell used only for mkdir, cp, znc invocation, binary
execution, sha256sum, cmp, diff, git ops, file reads/writes). No
PROCESS-FAIL condition triggered. Pinned znc verified
byte-identical to src/tools/toolchain/znc_linux_x86_64_abed8aa1
before the prereg commit. Git writes via /usr/bin/git directly
(safebin git symlink EPERM lesson); explicit pathspecs; no git
reset; local only, never pushed. The znc defect workarounds from
AGENTS.md were followed in all new Zag code (u8 cells, hoisted
flags, max 3-deep ifs, no negated conjunctions in while
conditions); the build succeeded first try with no defect
symptoms.

## Commits

- e24635d62: frozen prereg (PREREG.md + NAMECHECK.md), alone,
  strictly before implementation.
- This commit: unpin_h3.zag (implementation), unpin_h3_bin
  (sha256 a9759f7c4bd71b944a6e0e2da69264c6f2f192ba4edef4835c8ee9fdf747223c),
  run1/2/3.txt, run1/2/3.err, REPORT.md. Local only, never pushed.

## Follow-ups for the parent

- H3B candidate: fresh preregistration correcting K20 to the
  verified values (UNPINSTALE-A20: ret=17, post=6, rawA=19, ev=16,
  drop=0, cf=48), then a fresh run of the unchanged mechanism. All
  other 21 bars already pass on this binary; the H3B delta is the
  K20 derivation only.
- The H3 mechanism (policy 8 + learner routines + trace/audit) is
  a candidate substrate piece for the continuing-learner memory
  question: death as a learner cognitive judgment with a
  white-box trace, where capacity drop measures release behavior.
- Open: INCORPORATED/SUPERSEDED reasons, sealed post-freeze
  adversary worlds, and the successful-episode importance source
  from the H1 follow-ups remain unrun.
