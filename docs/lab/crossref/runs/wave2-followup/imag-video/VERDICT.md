# T2-IMAG video battery — weirdness-removal VERDICT

Crew: IMAG video-battery crew (Wave-2 crossref follow-up). Date: 2026-09-24
(PDT), ~08:32–08:55. Task: remove the two caveats on the T2-IMAG REPRODUCED
verdict — (a) independently verify the a39aadf→4d1a40ecaa additive-diff claim
and justify the pin amendment, (b) RUN the committed-but-unrun Q2 evidence,
(c) re-verify the FULL video battery at the amended pin.

## Declaration: CLEAN

The video battery is **CLEAN**. The pin amendment (a39aadf + 4d1a40ecaa) is
justified by an independent diff and by behavioral proof: the FULL battery —
Q1, Q2, Q3, text-only control, and Q1V — reproduces byte-identically at
4d1a40ecaa, and Q2 re-derives 12/12 / 12/12 / 24/24 from committed sources
at both pins. No remaining weirdness.

## 1. Independent diff verification (a39aadf → 4d1a40ecaa)

Both pins API-verified independently via GitHub commits endpoint:
- `a39aadf6e563ca470c37a4770afbe350c023c98b` — "Imagination-design trial:
  mechanism, evidence, verdicts (2026-09-22)", 2026-09-22T05:07:31Z.
- `4d1a40ecaaecaf53cd13cf492737f605d17f35a2` — "imagination: Q1V video
  battery PASS 12/12 both modes; taste probe verdict; pitch amendment
  applied; gallery sources", 2026-09-22T05:26:06Z (~19 min later).

Full diff on `docs/lab/imagination/` (21 files, 1271 insertions, 11 deletions):

| File(s) | Change | Classification |
|---|---|---|
| `src/imagine.zag` | **207 insertions, 1 deletion** (numstat-verified) | Q1V-ONLY, additive. The 1 deletion is a comment line documenting `w0 domain … 4=VIDEO`. All insertions: (i) 5 comment lines documenting the VIDEO domain layout; (ii) 15 brand-new functions (`ig_qv_dir`, `ig_qv_trajectory`, `ig_qv_spdrank`, `ig_qv_speed`, `ig_qv_speedchange`, `ig_qv_zone`, `ig_qv_reentry`, `ig_qv_midpoint`, `ig_qv_edit_mv`, `ig_q1v_emit`, `ig_q1v_sc1..sc4`, `ig_q1v_run`) — zero definitions of any of these names exist in the a39aadf source (grep: 0 `q1v`/`qv_` occurrences there); (iii) one new `if (a1=="q1v")` dispatch branch in `main()`, inserted between two existing branches that each `return 0` before reaching it — mutually exclusive string-equality conditions, so no existing dispatch path is reachable-by-accident. New functions only CALL pre-existing helpers (`ig_place`, `ig_ewput`, `ig_clear`, …); they redefine nothing and add no globals. |
| `PREREG.md` | 1 line changed | Doc-only: the pitch-bin CORRECTION note ("Wording only; behavior correct, no rescore"). |
| `PROPOSED-amendment-pitch-…md → PREREG-amendment-2026-09-22-pitch.md` | rename R079, 8 lines | Doc-only: status NOT APPLIED → APPLIED + approval note. |
| `PROPOSED-amendment-video-…md → PREREG-amendment-2026-09-22-video.md` | rename R088, 5 lines | Doc-only: status NOT APPLIED → APPLIED + application note. |
| `RUN-LOG.md` | 31 lines | Doc-only: the Q1V run entry replacing the "drafted, NOT applied" line. |
| `SHA256SUMS` | **14 insertions, 0 deletions** | Evidence-only: hashes for imagine.zag, the two amendment docs, verify_q1v.py, Q1V-RESULTS.md, and the 10 Q1V logs. No existing hash (Q1/Q2/Q3/control) was removed or altered. |
| NEW files | `Q1V-RESULTS.md` (84), `TASTE-PROBE.md` (117), `verify_q1v.py` (244), `logs/q1vm_rep1..5.txt`, `logs/q1vh_rep1..5.txt`, `gallery_src/RENDER-NOTES.md` (106), `gallery_src/render_gallery.py` (343) | All additions; none is battery code except `verify_q1v.py` (independent Python checker) and the Q1V logs. `render_gallery.py` is a Python PNG renderer for the viewable gallery — not part of the Zag battery. |

Substrate check: `docs/lab/wave1/toolchain/R33_NATIVE_IO_V1.zag` is
byte-identical between the two pins (empty `git diff --stat`); one copy
served both builds (blob `a6b440d2…`, sha256
`e6379ddb…f61d8`).

**Result:** the prior crew's claim is CONFIRMED and sharpened — the diff is
purely additive on every load-bearing path. The only behavior-affecting
bytes added are the Q1V functions and their dispatch branch, which are
unreachable from Q1/Q2/Q3/control invocations.

## 2. Q2 — committed-but-unrun evidence, now RUN

Q2 (design generation) exists at `a39aadf` (logs + `verify_q2_gen.py` +
`verify_q2_gen3.py` + `Q2-VERIFY.md`) but was never rerun by any crew.
Re-derived from committed sources in two clean builds:

| Pin | Build | q2m SHA | q2h SHA | GEN-1 | GEN-2 | GEN-3 |
|---|---|---|---|---|---|---|
| `a39aadf` (evidence pin) | 205365 bytes main — EXACTLY the trial RUN-LOG's "205365 bytes after the 2026-09-22 Q3 rebuild" | `7a0b3cf7…` 3/3 identical = committed | `b4105a25…` 3/3 identical = committed | **12/12** | **12/12** | **24/24** |
| `4d1a40ecaa` (amended pin) | 226401 bytes main | `7a0b3cf7…` 3/3 = committed | `b4105a25…` 3/3 = committed | **12/12** | **12/12** | **24/24** |

GEN-1/GEN-2 via committed `verify_q2_gen.py` (unmodified, argv-driven).
GEN-3 via committed `verify_q2_gen3.py` with only its two hardcoded lab
paths repointed to this crew's rerun logs (patch proven path-only by diff;
the verifier's `sys.path`-injected `verify_imag` is byte-identical to the
committed one — sha256 `9b694e45…` both copies). All 24 probes:
ported == hand-traced, zero investigations needed. The committed numbers
(12/12, 12/12, 24/24) are NOT taken on faith — they re-derive exactly.

## 3. FULL battery re-verification at the amended pin (4d1a40ecaa)

Stronger than the prior crew's (they ran only Q1V at 4d1a40ecaa): the
ENTIRE battery was run at 4d1a40ecaa — byte-identity vs committed
SHA256SUMS plus all committed scorers:

| Leg | Reps | This rerun SHA256 | Committed SHA256SUMS | Scorer result |
|---|---|---|---|---|
| q1 machine | 3/3 identical | `df2d1b1c…` | match | `verify_imag.py`: **36/36** |
| q1 human | 3/3 identical | `d5eede6f…` | match | `verify_imag.py`: **36/36** |
| q2 machine | 3/3 identical | `7a0b3cf7…` | match | GEN-1 **12/12**, GEN-2 **12/12** |
| q2 human | 3/3 identical | `b4105a25…` | match | GEN-3 **24/24** |
| q3 machine | 3/3 identical | `f7f82ae0…` | match | **6/8** (misses Cracker Barrel + Starbucks; STRONG 4/5, MODERATE 2/3) |
| q3 human | 3/3 identical | `cfbaecf8…` | match | **4/8** (misses Cracker Barrel + all 3 MODERATE; STRONG 4/5, MODERATE 0/3) |
| q1v machine | 5/5 identical | `55b26e05…` | match | `verify_q1v.py`: **12/12** (PASS vs IMAG-V ≥9/12) |
| q1v human | 5/5 identical | `5bb44282…` | match | `verify_q1v.py`: **12/12** (PASS vs IMAG-V ≥9/12) |
| text-only control | stdout byte-identical to committed `logs/textonly.txt` (`71d3738f…`) | match | patched-path `verify_q1_textonly.py` (diff-proven logic-identical): **2/36** both modes (hits: scene 5 q1, scene 7 q1, answer=4) — guard <12/36 holds |

Q3 agreement: machine 6/8 vs human 4/8 → **MARGINAL**, |6−4|=2 →
**NO-DIFFERENTIATION** — the frozen figures exactly.

**Behavioral proof of the additive claim:** Q1/Q2/Q3/control reproduce
byte-identically at 4d1a40ecaa with SHAs unchanged from a39aadf —
the Q1V addition altered no pre-existing code path in fact, not just in
diff.

Q4 blind ratings remain excluded per the frozen prereg (rater pending).
No RNG anywhere; deterministic pure-Zag rebuilds; pinned znc
`znc 2026.07.0-dev (edition 2026)`, flags `--no-zagd --no-analyze
--no-foreground-cache` (matching the trial RUN-LOG).

## 4. Pin amendment — justified

Frozen pin should read: **T2-IMAG evidence = `a39aadf` (Q1/Q2/Q3/control)
+ `4d1a40ecaa` (Q1V video battery)**. Justification: (i) the diff is proven
additive (207 insertions all Q1V, 1 comment-line deletion, zero Q1/Q2/Q3
code-path changes, SHA256SUMS grew by insertion only); (ii) the full battery
reproduces byte-identically at 4d1a40ecaa, so the amended pin is
behaviorally equivalent to the split-pin reading for every frozen claim;
(iii) Q2's committed-but-unrun evidence now stands on re-derived runs at
both pins. Nothing in the amendment changes any frozen figure, bar, or
decision rule — it only attributes the video battery to the commit that
actually built and ran it.

## Integrity notes

- Prior crew state (`~/workspace/scratch-crossref/T2/IMAG/`) was READ
  (VERDICT.md, RUNLOG.md, CREW_NOTES.md) but not reused for builds — this
  crew re-fetched both pins fresh into `video/clean/` (sparse,
  `--filter=blob:none`, `git fsck` clean at both pins). No vanishing-tree
  incident this run.
- No `/tmp` used; TMPDIR=`~/workspace/tmp_commit` throughout.
- Nothing committed (per tasking, the coordinator does the single
  publication commit). No `.zagd`/`.zag-cache`/binaries left in any
  checkout; build artifacts live only under `video/build*/`.
- Work dir: `~/workspace/scratch-crossref/T2/IMAG/video/` — this
  VERDICT.md, RUNLOG.md, `clean/` (sparse checkout, resting at `a39aadf`,
  `git status` clean), `build/` (4d1a40ecaa mirror + runs), `build_old/`
  (a39aadf mirror + Q2 runs), `scratch/` (path-repointed verifier copies
  with diff-proven patches).
