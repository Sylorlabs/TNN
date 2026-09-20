# Wave-12 Phase-1 — Independent Verification of Reported GOs (workstream 5/8)

**Verifier:** independent subagent (Muse Spark, depth-2), isolated from the build work.
**Date:** 2026-09-20. **Repo:** `sylorlabs/TNN`, branch `tnn-native-lab`.
**Drive:** read-only — no repo state was changed by this verification; no binaries,
caches, or build artifacts were committed anywhere. All rebuilds/reruns were done
in `/tmp` scratch and are not part of the repo.

**Method (uniform across steps):**
1. Rebuilt every committed source (pilot/harness/checker) with the committed
   toolchain and ran it against the committed evidence.
2. Compared each output byte-for-byte (`cmp`) against the committed evidence.
3. Re-ran the committed checker on the committed evidence (and on adversarial
   inputs where available) and compared its output byte-for-byte.
4. Verified prereg freeze commit predates implementation commit via GitHub API
   commit timestamps; verified claimed commits exist and verified full hashes.
5. Grepped all sources for banned RNG/clock/thread imports; confirmed pure Zag
   (no C/Python in implementation, aside from preregistered checkers noted below).
6. Independently recomputed headline bar numbers from the transcripts
   (episode counts, pass rates, gap arithmetic, audit maxima, retention ratios).

**Toolchain used for rebuilds:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
always with `--no-zagd --no-analyze --no-foreground-cache` (no caches written).

Verdict legend: **VERIFIED** = all five checks pass. **DISCREPANCY** = something
differs from the reported claim; graded below as *blocking* (falsifies the GO)
or *non-blocking* (honest deviation, GO can stand with a note).

---

## STEP 1b — complete-state schema, replay protocol, state-evolution law

**Verdict: DISCREPANCY (non-blocking for the evidence; blocking for prereg governance)**

- **Prereg timing:** original prereg freeze commit `7dd3a3866a6c` (19:27:27Z) predates
  the implementation/evidence commit `2e08b77350b6` (19:34:27Z). ✓
- **Amendment timing:** the evidence was produced under **two schema amendments that
  do NOT predate implementation** — both were committed in the SAME commit as the
  implementation/evidence (`2e08b77350b6`), and the amendment document itself says
  `PROPOSED — pending Micah's re-approval`:
  - Amendment A changes the H record/schema from 257 fields / 2304 B to 273 fields / 2432 B.
  - Amendment B adds `K.rctr`, schema v2 (274 fields / 2440 B).
- The GO verdict is claimed on evidence run against the **amended** schema, while the
  amendments were still awaiting Micah's re-approval. Under the program's standing
  rule (rule changes need Micah's re-approval), the prereg strictly governs the
  *original* schema only.
- **Evidence reproducibility (genuine):** all evidence hashes verify (`sha256sum -c`
  clean); rebuilt binaries match the committed hashes byte-exactly; every transcript
  re-ran byte-identical: 1000/1000 replay, 600/600 permutation, planted `K.rctr`
  detection 5/5 batches, negative control 0 divergence, v2 closure 0 alarms and
  1000/1000 replay. Pure Zag; banned-token grep clean.
- **Bottom line:** the science is real and every number reproduces. But the GO was
  declared on an amended schema whose amendments are still marked pending Micah's
  approval — **do not treat 1b as a closed GO until Micah re-approves the amended
  schema (or the evidence is re-run on the frozen original).**

## STEP 1c — sealed verdict record, coincident firewalls, ledger canonicalization

**Verdict: VERIFIED**

- **Prereg timing:** prereg `57773c3ada35` (19:36:42Z) predates implementation
  `0a979452b63b` (19:52:36Z); no amendments. ✓
- Rebuilt both committed binaries (`fwmain.zag`, `fwgate.zag`); binary hashes exact:
  `73b51ac99f54e21c75aceecee9ab5ebb880bbb18760b7e252d900654161990d5` and
  `bd649a9eb956c1df55a4cc2f87f1011bd72da31aabd11c5db6021fb1b1592809`.
- Re-ran all modes (verdictinv, tamper, meminv, refuseinv, ledginv, wiring, replay)
  plus gate-clean and all 20 planted probes: **every output byte-identical, exit 0**.
  Gate clean 0 violations; 20/20 planted probes caught.
- Confirmed the cross-chain comparison checks both chains independently and compares
  headers/payloads, masking only the two documented `variant_id` bytes (the coherent
  interpretation documented in the report, not a hole).
- Pure Zag; no C; no live banned RNG/clock/thread imports.

## STEP 1d — phrasing variation, adaptivity/arbitrariness harnesses, null control

**Verdict: DISCREPANCY (blocking for prereg governance; evidence itself is genuine)**

- **The committed prereg is literally truncated.** Git blob
  `474c24d045f89250b32a53c395b5a2b852c31e92` (11,862 bytes) ends mid-sentence:
  `hash-of-state arm, code = FNV-1a(projection bytes) % 8 mapped to`
  followed by a literal `...[truncated 4149 chars]`.
  The omitted remainder (detector controls, null baseline, downstream bars, build
  plan) **cannot be proven frozen before implementation** — those rules were not in
  the committed prereg.
- **Evidence reproducibility (genuine):** inventory hash exact; all five programs
  rebuilt; all 12 evidence modes re-ran byte-identical (trial differs only by a
  runner-appended `trial_exit=0` line): 100/100 trials, 20 distinct/class,
  adaptivity 1600/1600, novel 600/600, detector behaviors, null-vs-ArmC PASS.
  Machinery line budget 259+149=408 ≤ 500. Pure Zag.
- The report itself notes Step 1c+1d integration remains pending.
- **Bottom line:** nothing about the evidence looks fabricated — it all reproduces
  from committed sources — but a GO cannot rest on a prereg whose tail is missing.
  **The prereg must be re-frozen complete and the evidence re-run after it (or
  Micah must explicitly waive the truncation) before 1d counts as a closed GO.**

## STEP 5a — repaired code pilot (`16a7815597e8b38a6d26ce63c2296c5570497dce`)

**Verdict: VERIFIED** (with two non-blocking notes)

- **Commit exists:** full hash `16a7815597e8b38a6d26ce63c2296c5570497dce`
  confirmed on `tnn-native-lab` (2026-09-20T20:19:22Z). ✓
- **Prereg timing:** prereg `57d1a388dda2` (19:32:51Z, single commit, no later edit)
  predates the repair/GO commit. The PC3 path (K3 fires on C4) was explicitly
  preregistered: §6 allows K1–K3 to be attempted twice, each attempt a **dated
  amendment**; §11 step 4 sequences "dated PREREG amendment committed → scaffold
  fixed → full genuine re-run". The amendment was filed in the same commit as the
  repaired evidence; its text asserts it froze *before* any repaired evidence was
  generated. Commit-level ordering is coarse but the prereg's amendment requirement
  was honored in substance, and the repair path itself was frozen pre-build. ✓
- **Evidence vs verdict:** rebuilt pilot from committed sources reproduces
  `corrected_run1.log` **byte-identically** (3,950 episodes; `corrected_run2.log`
  cmp-identical) and `planted_pc3.log` byte-identically. Rebuilt checker reproduces
  `checker_corrected.txt` exactly (audit median 64 / max 384, 12/12 poisons killed,
  retention 10/10/stage, PASS). Per-stage transcript counts recomputed from the EP
  lines match the prereg table exactly (C1 70/10/20 … C12 210/30/60; fault 10,
  comp 10, adversarial 30 per stage; total 3,950 = 3,350+120+120+360). Corrected
  run: heldout 100% all stages, fault 10/10, comp 10/10, traps 8/8, k3 0/10,
  k4 5/5, c7var 7/7; planted run: C4 k3 = 2/10 fired (predicted ≥2), all other
  stages 0/10. B2 (disconnect retention ≥85%) independently recomputed: 1.00 all
  stages. The checker is a genuine independent implementation (imports only
  substrate + zutil, recomputes every bar from the transcript).
- **Pure Zag:** no C/Python; banned-token grep clean.
- **Notes (non-blocking):** (1) the transcript format is space-separated whereas the
  prereg's §8 examples show comma-separated — a protocol deviation; the checker
  parses the actual format, and the verdict is unaffected. (2) a stale comment in
  `pilot.zag` lists wrong per-stage counts, but the actual `pilot_nscaf/nwatch/nheld`
  functions match the prereg table and the transcript exactly.

## STEP 5b — English curriculum 1x pilot

**Verdict: VERIFIED** (with one non-blocking note)

- **Prereg timing:** prereg `038abe1efc21` (19:33:51Z, single freeze commit) predates
  implementation/results `62d9828263f7` (20:02:14Z) and evidence `6b2bc9cee680`
  (20:03:04Z). ✓
- **Evidence:** reassembled `run_a`/`run_b` from the 4 committed chunks each;
  both are **byte-identical**, sha256 `f17671e7a454b19cade4a4489b959e3a2fc37d009c7d1930e7b4eaf8db270124`
  — exactly the hash claimed in `ev/README.md`. ✓
- **Checker:** rebuilt `check.zag` from committed sources; its output on `run_a`
  reproduces `check_a.txt` **byte-identically**: `CHECK,GO`, **44/44 bars PASS**,
  zero FAIL, every `AUDITMAX ≤ 4096` (E5 max 2,688 B = 66% of the 4,096 cap).
  Episode counts confirmed: E1 800 + E2 600 + E3 400 + E4 500 + E5 800 + E6 300 +
  EV 480 = **3,880**. Stage table matches the report (E1 640 binds/40 corrections/
  80 gavagai/40 poison/40-40 pre/0 absorptions; …; E6 120/120 pre, 60/60 practice;
  C4 6/6 learner-initiated disconnects; KFAIL,0,0).
- **Checker discrimination (honest verifier):** the rebuilt checker returns
  `CHECK,DEAD,12` on the invalid `smoke_old` run — it caught the two harness bugs
  it was supposed to catch, and passes the repaired run. Not a rubber stamp.
- **Pilot re-run:** the rebuilt pilot was re-run end-to-end from committed sources;
  its 3,880-episode transcript is **byte-identical** to committed `run_a` (7m14s run).
  The transcript on the branch is therefore exactly what the committed sources
  produce — no hand editing.
- **Pure Zag:** banned-token grep clean across pilot, checker, and vendored
  substrate; `st_memory_core.zag` verified byte-identical (sha256) to the Step-2
  version on the branch. No C/Python in the implementation.
- **Note (non-blocking):** four build-note/bug-fix amendments
  (`PREREG_AMENDMENTS.md` A1–A4: ISO field format, read-only op slot, slot-value
  collision fix, E5 token-buffer fix) were committed in the same commit as the
  results, flagged for Micah's retroactive review. They change no bar, schedule,
  test, metric, or kill condition — the first full run is honestly kept as
  `smoke_old` with the checker's DEAD verdict as the diagnostic trail. Also:
  C6 (no-curriculum baseline) and E6-K3 (human-reader clarity) are explicitly
  DEFERRED in the report, so the GO covers the instrumented battery only. Minor
  prereg typo: E1 poison episodes labeled "(80 eps)" in §3 but the frozen kind
  arithmetic (k1 38..39 of ep%40) unambiguously gives 40 — implementation matches
  the arithmetic.

## STEP 5c — messy-reality 1x pilot ("MRC survives")

**Verdict: VERIFIED** (with one non-blocking note)

- **Prereg timing:** prereg `9bf4e8a41b82` (19:33:15Z) predates harness commit
  `a7a943343bf3` (19:46:06Z); no amendments. ✓
- **Re-runs:** rebuilt `mrc.zag` from committed sources; **all three arms re-run
  byte-identically** to the committed transcripts (CUR/CTL/INJ, 4,560 episodes each:
  4,500 pilot + 60 negative-control), and a second CUR run is byte-identical to the
  first. ✓
- **Separate evaluator:** re-ran the committed `check_mrc.awk` on each transcript;
  outputs reproduce `check_{cur,ctl,inj}.out` **byte-identically**, all ending
  `CHECK_OK` with zero `CHECK_FAIL` lines. The awk re-implements the §2.3 schedule
  from the episode index, recomputes `whash`, grades demands per cell, and enforces
  the B7 integrity invariants (no vote-resolution, no fabricated completion, no
  strengthen-from-noise, no false collusion accusation, no silent pinned touch) —
  any violation fails loudly. **The awk evaluator is explicitly preregistered**
  (prereg §2.5: "The checker (`check_mrc.sh` + `check_mrc.awk`)…"), so its being
  awk rather than Zag is compliance, not a deviation. The harness itself is pure
  Zag; static RNG grep clean.
- **Headline numbers recomputed from committed checker outputs:** CUR_REV
  1156/1156 = 100%, CTL_REV 138/1156 = 11.94% → gap **88.06** pts; CUR_HOLD
  3083/3083 = 100%, CTL_HOLD 609/3083 = 19.75% → gap **80.25** pts. Both far exceed
  the 15-point kill bar. B2: CUR 0/2442 premature (0% ≤ 5%), INJ 264/2706 = 9.75%
  (>5%, detector live). B3: 0/450 clean corruption all arms. B4: audit max 1728 B
  (CUR/INJ), 1024 B (CTL) — all ≤ 4096. Negative control 0/60 resisted on all arms
  (the reported, accepted hole). In-Zag `CL_CHECK` all pass; `bytes == entries×64`
  holds.
- **Note (non-blocking):** the per-arm awk checker emits
  `B1b_gap,DIE,gap_rev=-nan,gap_hold=-nan` — it cannot see the other arm when run
  per transcript (as `run_mrc.sh` runs it), so the headline gap is a manual
  cross-read of `check_cur.out` (arm 0 OVERALL) and `check_ctl.out` (arm 1
  OVERALL). The underlying numbers are genuine, committed, and reproduced; the gap
  arithmetic is trivial and confirmed above. A combined-transcript checker mode
  would close this cosmetic hole.

---

## Summary table

| Step | Reported | Verdict | Blocker? |
|---|---|---|---|
| 1b | GO (amended schema) | **DISCREPANCY** | Governance: amendments pending Micah's re-approval; evidence itself reproduces |
| 1c | GO | **VERIFIED** | — |
| 1d | GO | **DISCREPANCY** | Committed prereg is truncated mid-sentence; omitted rules can't be proven frozen |
| 5a | GO (`16a78155…`) | **VERIFIED** | Notes only (transcript format deviation; stale comment) |
| 5b | GO (44/44, 3,880 eps) | **VERIFIED** | Notes only (4 build-note amendments retro-review; C6/E6-K3 deferred) |
| 5c | "MRC survives" | **VERIFIED** | Note only (B1b gap is a manual cross-read of two checker outputs) |

**What is genuinely solid:** the mechanical evidence. Every transcript, every checker
output, and every binary hash in steps 1c, 5a, 5b, 5c (and the mechanical layer of
1b/1d) reproduced byte-identically from committed sources on an independent rebuild.
The checkers discriminate (5b's checker kills the buggy run; 5c's awk enforces the
integrity invariants). No RNG, no C/Python in any implementation path, vendored
substrates byte-identical.

**What is not closed:** two governance items, both blocking a "closed GO" label —
(1) step 1b's amendments are still marked pending Micah's re-approval, and the GO
was declared on the amended schema; (2) step 1d's committed prereg is truncated and
must be re-frozen complete. Neither looks like fabrication; both are paperwork
failures that the program's own standing rules (frozen prereg before build; rule
changes need Micah's re-approval) say cannot be waived without Micah's word.

No work remains open: every check listed in the method section completed for all
six steps.
