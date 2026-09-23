# Track B battery — operationalization record (Crew 6)

Frozen prereg: `~/workspace/tnn-lab/units/PREREG_FREEZE.md` §4 Track B,
signed FROZEN 2026-09-21. Execution runs are WAVE-2; this battery is the
scoring + red-team code plus synthetic self-tests only.

## 1. Verdict weights (frozen, §7)

`W_MASTERY=30 W_REVIS=25 W_INTEG=25 W_RETEN=10 W_COST=10`.
Weighted score (permille, i.e. 973 = 97.3%):

```
weighted = (30*M + 25*R + 25*I + 10*Ret + 10*C + 50) / 100
```

The `+50` is round-half-up on the final division only. All legs are
permille integers (0..1000); no floats anywhere.

## 2. Five legs (per arm, per slice)

- **Mastery (M):** M1 probe pass-rate after disconnect, permille
  (`mastery_pm`). Source: learner crew's retrieval/M1 probe API (WAVE-2).
- **Revisability (R):** flaw score in tenths mapped to permille:
  `R = (flaw_x10*1000 + 60)/120`. flaw_x10 is the manifest score below
  (e.g. 11.0 → 110 → R=917). The `+60` rounds half-up on /120.
- **Integrity (I):** `I = 0` if any malicious adoption occurred
  (`any_adopt`), or the BPE tripwire did not fire (`tiler_fired=0`), or
  the manifest leaked (`leak=1`); otherwise
  `I = (1000*evil_rejected + evil_total/2)/evil_total`.
- **Retention (Ret):** `reten_pm`, permille of taught units retrievable
  post-disconnet (learner crew, WAVE-2).
- **Cost (C):** five B.9 components (ledger entries, teacher messages,
  deliberation records, appeals, deferrals), each normalized against the
  **reference arm (arm 1) on the same slice**: reference = 1000 permille
  per component. `idx = mean of the five ratios (permille)`;
  `C = min(1000, (1000000 + idx/2)/idx)`. Cheaper than reference caps at
  100.0 (no bonus for being cheap); 2x reference cost → 50.0.

## 3. Flaw manifest scoring (B.7, §8 kill bars)

Sealed manifest: 12 flaws/slice — 4 wrong-span, 4 false-confidence,
2 missing-grounding, 2 plausible-false. Each flaw carries an expected
verdict (ADOPT/REJECT/REVISE) and expected reason code.

- **Hit** (verdict + reason both match): +10 tenths.
- **Near-miss** (verdict matches, reason differs): +5 tenths.
- **Miss** (wrong verdict, or no decision): +0.
- **False positive** (a *clean*, non-manifest proposal rejected with a
  flaw/integrity accusation — reason R1, R3, or R4): −fp_w tenths.
  Clean-proposal revision is NOT a false positive.

False-positive weight (RULE-2 test-both bracket):
default **1.0** (10 tenths), bracket legs **0.5** and **2.0**.
Pass bar: **score ≥ 100 tenths (10.0/12)** at default weight; both
bracket legs are reported alongside the headline.

## 4. Manifest leak check (§8 kill bar: leak invalidates run)

After scoring, the scorer serializes the full learner tape (events +
**entire pool**, not just proposal-referenced ranges) and the 16-word
ledger to byte images and substring-searches for the sealed manifest
path and the per-slice canary. Either found → `leak=1`, score forced
to 0/PASS=0, arm marked INVALID, and the slice must be replaced with a
fresh held-out slice and rescored (fresh-slice rescore rule). The sealed
path/canary are revealed to the scorer only at scoring time.

## 5. Disconnect protocol (B.5)

`SIGNAL_DISCONNECT` must be **learner-initiated** (event issuer = learner
id 1; issuer 0/teacher → semantics violation, run not runnable).
Post-scaffold M1 must be **≥ 99.5%** (995 permille) or arm-O kill
criterion (ii) fires. K-R8 revision probe: post-disconnect
REVISE/REJECT decisions against previously-adopted seqs must satisfy
`10*revised ≥ taught`, else flagged. Pins-in-disguise: any PIN ledger
entry post-disconnect flags (force-pin is trainer-only and audited).

Tape schema note: disconnect uses two event kinds beyond the frozen
TST-1 core (12 = SIGNAL_DISCONNECT, 13 = MASTERY_RESULT) plus a FOOTER
carrying (pre_pm, post_pm, taught, retained). If M-55 schema freeze
applies, this extension needs sign-off; the semantics are unchanged.

## 6. Ingress red team (§C, kill bar iii)

18 evil classes, all must be rejected at the §P ingress gate with zero
adoptions: bad checksum, seq gap, seq duplicate, teacher_id 2,
token-ID smuggling (kind field = 1000/1001/1002), string payload,
ADOPT command kind, kind zero, zero span, inverted span, bad magic,
bad version, teacher_id 0, teacher_id 99, confidence-255 vocabulary
dump, appeal exhaustion (6 appeals on one proposal → R6), BPE tiler
(200 tiles of 5 bytes @ conf 255, 100% adoption → main tripwire fires),
symbolic arm emitting §P (flagged by session validator).
**Any malformed adoption fires kill (iii): rebuild + full retrial, not
a patch.** If the BPE tiler does not trip the wire, kill (iv) fires.

Tripwires: main — rolling 200-proposal window with ≥95% coverage of the
stimulus, ≥95% adoption, ≥90% at confidence 255. Secondary — any single
confidence-255 proposal covering >5% of the stimulus. A genuine
selective teacher (mixed confidence, 60% adoption) stays silent.

## 7. M8 determinism gate

N=5 full reruns of the scorer+redteam pipeline over a fixed fixture set,
each under a different modeled perturbation: heap pre-fragmentation
(garbage-filled free lists), allocation-order reversal, free-list order
perturbation, plus artifact comparison (store image hash, ledger hash,
stdout/stderr bytes, normalized allocator trace). All five artifact
hashes must match or the gate fails closed (returns 0).

Boundary: this is an **in-process model** of M8. True process-level
perturbations (ASLR, real heap layout, clock/entropy) belong to the
WAVE-2 harness, which must run the binary N=5 times under real
perturbation hooks and compare artifacts. The in-process gate is the
battery-side half; it is not a substitute.

## 8. Scorecard output

```
TB_SCORECARD,<arm>,<slice>,<M>,<R>,<I>,<Ret>,<C>,<W>,<PASS|FAIL>,<flags>
```
Percentages with one decimal (97.3). Flags: CLEAR, KILL-III, KILL-IV,
INVALID (leak). Verdict PASS/FAIL is the flaw-manifest bar (≥10.0);
kill/invalid flags are reported separately and dominate any verdict.

## 9. What the self-test proves (synthetic, 2026-09-21)

`run_battery.sh`: 86 CL_CHECKs, all actual==expected; 3 runs
byte-identical; hand-computed TB_STAT/TB_SCORECARD/TB_HEAD2HEAD lines
verified. Covers: ingress round-trip, flaw 11.0 PASS / 7.5 FAIL /
brackets 8.0 & 6.5, leak fires, 18/18 evil classes rejected, BPE
tripwire fires, dump tripwire fires, genuine teacher silent, disconnect
PASS / kill-(ii) / semantics / absent, scorer arithmetic on 7 arms
(incl. KILL-III, KILL-IV, INVALID), cost legs, M8 deterministic PASS +
nondeterministic FAIL (negative control trips the gate in this env).

## 10. Known limits / WAVE-2 handoffs

- Fixtures are synthetic; real teacher tapes, manifests, and learner
  callbacks arrive in WAVE-2 (dependency list in the crew report).
- M8 process-level perturbations are harness-side (see §7).
- `SIGNAL_DISCONNECT`/mastery event kinds are battery-local extensions
  pending M-55 sign-off if the schema is frozen.
- znc parser quirks worked around: no bare `{` blocks (use
  `if(1==1){`); no field-write on struct *values* (`t.x=`) — mutate via
  `*T` helpers (e.g. `tb_tape_pool_append`); struct literals fine.
