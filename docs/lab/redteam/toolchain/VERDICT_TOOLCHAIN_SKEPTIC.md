# TOOLCHAIN/ARTIFACT SKEPTIC — Verdict (2026-09-21)

**Role:** red-team skeptic, implementation layer. Brief: attack compiler artifacts,
oracle independence, RSI circularity, silent corruption, and the no-RNG scans.
Micah's order: do not pull punches.

**Method:** source audit of headline artifacts + live probes on the pinned toolchain
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, `znc 2026.07.0-dev`).
Every probe below was actually executed; outputs are quoted verbatim. Probe sources
kept in `/tmp/redteam_probe/` (ephemeral); key evidence digests recorded here.

**Ranking rule (parent guidance):** attacks we already found and documented ourselves
rank WEAKER than attacks pointing at untested gaps. "Proven live" outranks
"could be" — but "proven mechanism, untested blast radius" is stated as such.

---

## Probes executed

| # | Probe | Result |
|---|---|---|
| P1 | Clean-room rebuild of `rsi.zag` (caches cleared), 5 base runs vs committed `runs/base_r*.log` | **byte-identical** (md5 `46550728db9f37a5e7e50c213bab1006`); determinism regenerates from source, no cache/replay artifact |
| P2 | Same source built 3× from clean state | **3/3 identical binary hashes** (`cf7122367c86e6486d0ae445db6878d9`); pinned toolchain is build-deterministic |
| P3 | ZNC-2026-09-21-007 reproducer: 5 consecutive `nio_alloc(512) as []i32` (exact replica of `rngscan_v2.zag:613-617`) | **BUG LIVE**: `vln[0]` reads `1065` (=`voff[65]`) instead of `2000`; `vst[0]`→`2065`, `valn[0]`→`3065`, `vie[0]`→`4065`. Reads of the 2nd+ table are deterministically corrupted |
| P4 | `MALLOC_PERTURB_=165/90` on rebuilt RSI binary | outputs identical — **but probe vacuous** (see P5) |
| P5 | Raw `_zag_malloc` read-without-write ± perturb | fresh pages read `0` regardless → allocator zeroes fresh pages (mmap or explicit); perturb cannot reach it |
| P6 | free→malloc(same size)→read-without-write | **recycled chunk is dirty**: `b[0]=0, b[31]=171, b[63]=171` (0xAB fill survives). Free lists are NOT scrubbed |

---

## Ranked attacks

### A1 — SERIOUS — The no-RNG certifier is built on a live miscompile (PROVEN live, blast radius UNTESTED)

**Finding.** ZNC-2026-09-21-007 (`as []i32` consecutive same-size casts alias on read)
is live on the pinned toolchain — proven by P3 just now, replicating the exact
pattern from the checked-in source. The pattern is present in the certification
tooling itself:

- `wave12/step1a-v2/checker/rngscan_v2.zag`: 23 casts, incl. 5 consecutive 512-byte
  casts (lines 613–617) and 7 consecutive 256-byte casts (824–830)
- `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag`: 30 casts
- `wave12/step1a-v2/thin-certifier/certifier/thincert.zag`: 9 casts, incl. 3
  consecutive 512-byte casts (763–765) and 2 consecutive 256-byte casts (652–653)

The thin certifier is the CURRENT no-RNG gate ("hardened replay check plus thin
per-build certifier — PASSED", MEMORY.md 2026-09-21). The tool that certifies
Micah's no-randomness law reads its own tables through a known-corrupting cast.

**Why byte-identical reruns can't save it.** P3's corruption is fully deterministic
(same wrong values every run). A 5/5 byte-identical certification can be 5/5
identically wrong. This is the sharpest form of the "perfect scores as artifacts"
worry: determinism and correctness are orthogonal, and the lab's primary
determinism instrument (rerun hashing) is blind to this bug class by construction.

**Honest judgment:** the miscompile IS real (not "could be"). Whether it corrupts
any actual certification verdict is UNTESTED — it depends on whether indices 0–2
of the 2nd+ tables hold live data on the scanner's real inputs. The AGENTS.md
workaround (`[]u8` arenas + explicit `t_put32`/`t_get32`) was documented but the
checked-in certifier sources were never migrated.

**Concrete test:** rebuild `thincert.zag`/`rngscan_v3.zag` with the documented
workaround, run both old and new certifiers over the full corpus of certified
builds, diff every verdict. Any divergence = the gate was compromised. Estimated:
one crew, pure Zag, no new science. **This is the single highest-value audit in
this report.**

### A2 — SERIOUS — RSI "exact reproduction" is entailed by construction (PROVEN from source)

**Finding.** The 3/3 "+10000 predicted → +10000 actual" is not a measurement that
could have come out otherwise. From `rsi.zag`:

- T-PRIN-PRIORITY's prediction is a **hardcoded constant**: `m_s32(reff,nc*4,10000)`
  (line ~270). It is not computed from the self-model at all.
- T-DENSE / T-DOMAIN3 predict `10000 − m_baseline` — i.e., the tautological
  assumption that the fix closes 100% of the measured gap.
- Costs (100/150/300) are hardcoded constants; the entire ranking
  (eff×100/cost) is driven by authored numbers. The verdict's own follow-up #3
  admits costs were never verified against implementation.
- The "variant runs" are the same battery functions with the failure flag flipped:
  `run_prin(ops, prin=1)` literally executes `if(prin==1){installed_truth=1;}`.
  The variant does not test the fix against the world; it re-runs the author's
  if-statement with the other branch taken.
- The "convergence" claim (variant runs emit only the 2 remaining RECs) is the
  same tautology one level up: the weakness flags are computed from metrics
  computed by the flagged code.

**What IS real:** the closed loop executes — diagnosis from measured metrics,
template selection, ranking, the refusal branch, audit records. The pipeline is
genuine machinery in pure Zag. **What is NOT demonstrated:** calibration. A
prediction of `10000` that is hardcoded, verified by re-running the code that
defines the scale, carries zero bits of evidence about self-model accuracy.

**Oracle gap (brief §2):** `verify_rsi.py` adjudicates KB2 as
`sign(actual)==sign(pred) and |actual| ≥ 0.5·|pred|` — far looser than the
verdict's "reproduced EXACTLY" headline, which was eyeballed from logs, not
mechanically checked. The oracle verifies logs against the prereg spec; it
cannot see that the spec's prediction step is vacuous. This is the precise
limit of oracle independence: oracles catch implementation-vs-spec drift (they
did — see the info-source escaped-hash catch), never spec-vs-world drift.

**The distinguishing test** (answers Sol #5's demand and brief §3):
1. **Held-out weakness:** implant a weakness measurable only by a NEW battery the
   recommender never saw; require a quantitative prediction *before* the variant
   runs, computed without observing the fix mechanism.
2. **Genuine quantitative risk:** predict a non-extreme value — e.g. the effect
   of a *partial* fix (2 phrasings instead of 3) — where the outcome is not
   entailed by a binary flag.
3. **Independent implementation:** the variant is implemented by a coder working
   from the REC text alone, forbidden from flipping the battery's own flag.
4. **Publish failures:** preregister N interventions; report all outcomes. The
   current record (3/3, zero failed interventions ever reported) has total
   selection effect.

**Honest judgment:** the exactness IS an artifact of design (proven, not
hypothetical). The verdict's own "honest calibration, not a miracle" framing
understates it: a hardcoded constant verified against its own definition is
neither calibration nor miracle — it is a unit test of an if-statement wearing
a lab coat. Grade for the *loop* stands (B+); grade for the *calibration claim*
should be retracted until the held-out test above passes.

### A3 — SERIOUS — Recycled heaps are dirty: byte-identical ≠ robustly deterministic (mechanism PROVEN, exposure UNTESTED)

**Finding.** P5/P6: fresh `_zag_malloc` pages read zero (so `MALLOC_PERTURB_`-style
adversarial testing is vacuous against this allocator), but **freed chunks are
recycled without scrubbing** — P6 read back `171` (0xAB) from a same-size
reallocation. Any `free → malloc → read-before-write` path yields
history-dependent values that are perfectly deterministic *for a fixed allocation
history* — i.e., invisible to 5/5 byte-identical rerun checks, and fragile under
any change in prior heap history.

**Why it matters for "no RNG".** The no-randomness law is certified by (a) static
scans for RNG calls and (b) replay determinism. Neither detects uninitialized
reads of recycled heap: the values are deterministic per run, and no RNG
*function* is ever called. A learner with arena reuse across episodes (the
normal case for long-horizon runs) that misses one initialization reads
deterministic garbage — the run is byte-identical, the result is
history-contingent. AGENTS.md already records one bite (L2's slot table, "worked
on allocator luck until the M8 perturbations").

**Honest judgment:** mechanism PROVEN by probe; `rsi.zag` itself is clean
(`m_alloc` explicitly zeroes). Whether any headline long-horizon binary has a
live free→realloc→read path is UNTESTED — no init-hygiene audit exists lab-wide.

**Concrete test:** static audit — every `_zag_malloc`/`nio_alloc` site must be
dominated by a zeroing loop or a full write before any read (grep-able,
mechanical). Plus a *poisoning allocator* mode for the test harness: pre-fill
freed chunks with a canary and fail any run whose outputs shift. One crew-day.

### A4 — SERIOUS — Silent thresholds the batteries never probe (class PROVEN by the 2^16 incident; current exposure UNTESTED)

**Finding.** The 2^16 parse-bound defect (AGENTS.md, HTD-1 composition battery)
is the exemplar: a codegen defect latent because *no validation manifest ever
contained an item > 65,535 bytes*. Deterministic, silent (ITEMS_PARSE_BAD looks
like a data error, not a compiler bug), caught only by a handoff that happened
to cross the threshold. The class is: **round-number thresholds where behavior
changes discontinuously and the test corpus never goes near them.** Live
instances in current sources:

| Threshold | Location | Silent behavior |
|---|---|---|
| 65,536 (2^16) | item parse bound checks | reject/parse divergence (demonstrated) |
| 33,554,432 (2^25) | any slice index | panic on *any* index incl. 0 — audit ledgers scale with episodes×units |
| 128 keys | `rsi.zag ln_teach` (`if(nu<128)`) | facts 129+ **silently dropped**, no error; metric degrades deterministically |
| 64 records | `rsi.zag au_append` into `m_alloc(64*64)` | **no bounds check** — `n*64` write past the buffer if records exceed 64; silent heap corruption, deterministic |
| 4,194,304 (2^22) | manifest bound checks (`ln>4194304`) | same latent class as 2^16 |

The 128-key and 64-record cases are the most insidious: they fail *silently and
deterministically*, and — crucially — **comparative bars (variant − baseline)
are blind to shared degeneracy**: if both legs use the same store, both drop
fact 129 equally, the delta is preserved, the bar passes on a degenerate
foundation. The three "caught and repaired" incidents (Q1N degenerate leg,
escaped-hash tamper trips, same-domain corroboration) were all caught because a
bar *failed*. The dangerous class is degenerate legs that *pass*.

**Honest judgment:** the class IS real (2^16 happened). Current exposure of the
other thresholds is UNTESTED.

**Concrete test — fuzz-at-the-edges battery** (pure Zag, deterministic, no RNG):
for every binary with a size-dependent path, run the boundary quartet
`{T−1, T, T+1, 2T}` where T ∈ {65535/65536, 128/129 keys, 64/65 audit records,
2^25−1/2^25 slice bytes, 4194304±1 manifest bytes} and assert (a) no silent
behavior change, or (b) a loud, preregistered failure mode. Anything that
silently degrades = a finding. This battery should be a standing gate, not a
one-off.

### A5 — MINOR — Sol #4 (frozen pipeline / cache / harness error): TESTED, cleared for the probed binary

**Engagement with Sol:** partially disagree on RSI, agree as lab hygiene.

- **Cache/replay:** P1 rebuilt `rsi.zag` from clean source with no `.zagd`
  available ("zagd unavailable; foreground compilation continues") — logs are
  byte-identical to the committed runs. The result regenerates from source; it
  is not a replayed artifact. P2 shows the pinned toolchain is build-deterministic
  (3/3 identical binary hashes), scoping the old "build-specific codegen defect":
  that defect predates/differs-from the pinned toolchain and does not reproduce
  in it.
- **"Evaluator reading expected outputs":** for RSI the stronger version of this
  concern is A2 — there is no independent evaluator at all; the variant *is* the
  mechanism with a flag. Sol's "hidden state/cache dependence" reading of the
  v2 0.96→0.26 collapse is one hypothesis; an equally consistent one is that v2
  genuinely exercised a different code path. The collapse deserves its own
  bisect, not a presumption of caching.
- **Residual:** clean-room rebuilds are not routine practice; the "don't commit
  .zagd" rule exists because staleness bit before. And "failure paths converted
  to default pass" is untested lab-wide — recommend a fail-open/fail-closed audit
  of battery error paths (does any `else` branch silently record a pass?).

**Honest judgment:** for the RSI binary, Sol #4 is answered by probe. As a
standing lab-wide hygiene gap, minor.

### A6 — MINOR–SERIOUS — Oracle independence has a hard ceiling (scoped, not broken)

**Finding.** The oracles are log-parsers adjudicating bars against the prereg.
They are genuinely independent of the Zag *implementation* (separate language,
parse-don't-trust discipline) and they have caught real bugs — the info-source
escaped-literal hash (5 false tamper trips) was caught by oracle digest
comparison, and the Q1N degenerate leg was caught because a bar failed. What
they cannot do, structurally:

1. Catch spec-level circularity (A2) — the oracle checks the prediction *format*,
   not whether the prediction was entailed.
2. Verify provenance the logs don't contain — `verify_rsi.py` never checks the
   variant binaries were built from the same source with only the flag changed.
3. Adjudicate headlines looser than their bars — KB2's bar (≥50%) vs the
   "EXACTLY" headline.

**Honest judgment:** oracles are effective implementation-vs-spec checkers and
should stay; they are not experiment-validity checkers and should stop being
described as if they were. The fix is adversarial *spec* review (red-team the
prereg before the run), which is what this report is.

### A7 — MINOR — RSI "constitution screen" is a compile-time constant, not deliberation

**Finding.** Trap refusal is `if((9&CMASK)!=0){emit_refused(5,1);}` with
`CMASK=31` — unconditionally true, by authorial constant. The non-trap templates
sit behind `if((0&CMASK)!=0)` — unconditionally false. The "deliberative
recommender" deliberates over weaknesses (real, from measured metrics) and
ranks by eff/cost (real arithmetic on authored constants), but the constitution
screen is a hand-written if/else, not a check against a constitution data
structure. The negative control (`rsi_nogate.zag`, gate zeroed → traps emitted
as RECs) proves the branch executes, not that any deliberative safety property
holds — the gate *is* the author's constant.

**Honest judgment:** already partially disclosed (fixed catalog). The refusal
behavior is real code behavior in pure Zag; the framing ("refused with
constitution reason codes") overstates the mechanism. Minor — but the pattern
"hardcoded constant presented as deliberative outcome" is the same pattern as
A2, and it recurs.

---

## What this report does NOT claim

- No proof that any headline *AI capability* result (mastery scores, flaw
  batteries, championship faithfulness) is wrong. The proven artifacts above are
  in the RSI loop's calibration claim (A2), the certifier's integrity (A1), and
  latent robustness (A3, A4) — not in learner mastery numbers, which I did not
  re-derive.
- The pinned toolchain builds deterministically (P2) and fresh rebuilds
  reproduce results (P1): the lab's determinism *practice* is sound for the
  binaries probed. The holes are in what determinism *proves* (nothing, about
  correctness) and in untested code paths.

## Recommended crew dispatches (ranked by value)

1. **Certifier rebuild + verdict diff** (A1): migrate thincert/rngscan-v3 off
   `as []i32` to the documented `[]u8`+accessor workaround; diff all historical
   certifications. Blocks the no-RNG law's credibility until done.
2. **RSI held-out prediction trial** (A2): preregister the 4-part distinguishing
   test; retract "calibration" language until it passes.
3. **Init-hygiene static audit + poisoning-allocator mode** (A3): lab-wide,
   mechanical.
4. **Standing edge-battery gate** (A4): boundary quartets for every
   size-dependent path; fail loud on silent degradation.
5. **Fail-open/fail-closed error-path audit** (A5 residual): one pass over
   battery `else` branches.

## Deferred

- Re-bisection of the prose-v2 0.96→0.26 collapse (Sol #4's cache hypothesis):
  needs the v2 harness and corpora; flagged for a dedicated crew.
- Direct >65,535-byte probe of the current HTD-1 comp binary: the parse path is
  entangled with the full battery (state snapshots, corp cache); the edge
  battery (rec. 4) subsumes it.
- Blast-radius audit of `as []i32` in non-certifier headline binaries: grep
  shows the pattern concentrated in step1a-v2 checkers/certifiers; a full-tree
  consecutive-cast scan is mechanical follow-up.
- Re-running the aliasing probe under `--no-analyze` vs default flags: the
  miscompile reproduced under the lab's standard build flags; flag-sensitivity
  is second-order.

## Evidence inventory

- Probe sources: `/tmp/redteam_probe/` (`alias_probe3.zag` + substrate,
  `uninit_probe.zag`, `recycle_probe.zag`, `rsi_fresh` build+logs) — ephemeral;
  rerunnable from the recipes in "Probes executed".
- `rsi.zag` line refs: prediction constants ~266–280 (`m_s32(reff,…,10000)`,
  `10000-m1`, `10000-m3`, costs 300/100/150); trap screen ~322–330
  (`(9&CMASK)`, `(18&CMASK)`, `(4&CMASK)`); variant flags in `run_para`/`run_prin`/
  `run_spoof`; `ln_teach` 128-cap; `au_append` unbounded write.
- Certifier line refs: `rngscan_v2.zag:613-617, 823-836`; `rngscan_v3.zag`
  (30 casts); `thincert.zag:652-653, 763-765` (9 casts).
- Digests: fresh RSI build logs `46550728db9f37a5e7e50c213bab1006` (= committed);
  3 clean builds `cf7122367c86e6486d0ae445db6878d9` ×3.

*Skeptic: toolchain/artifact leg, TNN red team, 2026-09-21. No punches pulled;
no results fabricated — every "PROVEN" above names its probe.*
