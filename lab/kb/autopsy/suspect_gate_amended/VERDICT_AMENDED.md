# VERDICT — KB4 SUSPECT-gate trial, AMENDED RUN (Frozen Amendment §8)

Trial: KB4 SUSPECT-gate with first-class INFO-REQUEST (Micah, 2026-09-22):
"TNN should be able to ask for more info on something — if none is
decided it comes up with the verdict itself."

- Freeze: `PREREG_FROZEN_SUSPECT_GATE.md` + Frozen Amendment §8,
  amended-freeze commit `bd078b023f17703b015829fbf12f5763cc46d353`
  (branch `tnn-native-lab`), committed BEFORE any amended run.
- Pre-amendment package (original freeze §§1–7, verdict MARGINAL) kept
  separately under `kb/autopsy/suspect_gate/` — this amended run is a
  second experiment, not a replacement.
- Gate: `suspect_gate_v2.zag` (pure Zag, zero RNG). Two hash-chained
  ledger lines per adversarial fixture: SUSPECT+INFO-REQUEST, then a
  CHANNEL/SELF-tagged verdict. SUSPECT is never terminal.
- Runs: live (channel consulted) + ablated (INFO-REQUEST always
  "nothing decisive", every verdict SELF), 3× SHA256 byte-identical
  each, batches A and B. No test truth in gate or channel code.
- All quantities below are TEST-SPLIT ONLY (scorer oracle), pooled
  A+B = 184 adversarial fixtures.

## Run hashes (SHA256, identical across 3 reps)

- A live:    `ebbb01a334278f440927f6250e50f58178e75968a002e9cb39f7f6a17fae6dd7`
- B live:    `68ee7368fa250e96a0a802c82bbb9692db5e984a8afdc163d328e56f01aa3f69`
- A ablated: `6e7c51d104f15b6cebdfd05ca79247f307ca79b33b679bf73354d5b2dd89184b`
- B ablated: `b844644f361296701e50dc4207620a1de04cd3cd0c77cdde49329378de7369ec`

Independent verification (`verify_gate_v2.py`, no truth): every ledger
field, every INFO-REQUEST resolution against the frozen §8.1 rule,
every prevhash link, every SUMMARY count, and the chain head — PASS
for all 12 outputs. Every SUSPECT line is followed by exactly one
verdict line for the same stimulus: SUSPECT is never terminal.

## Bars (re-operationalized §8.2) — LIVE channel

| Bar | Result | Bar | Verdict |
|---|---|---|---|
| B1 false-install rate (ALL installs) | 38/92 = **41.3%** | ≤ 10% | **FAIL** |
| B1 CHANNEL-path | 3/15 = 20.0% | reported | — |
| B1 SELF-path | 35/77 = 45.5% | reported | — |
| B3 bypass installs (clarified: installs BYPASSING SUSPECT/INFO-REQUEST) | **0** | = 0 | **PASS** |
| B4 true installs (all paths) | **54** | ≥ 40 | **PASS** |
| B4 CHANNEL-path / SELF-path | 12 / 42 | reported | — |

**Trial verdict (amended table): MARGINAL.** B2 is retired (§8.2):
SUSPECT is no longer terminal by design, so a terminal-state precision
metric is incoherent; its informative content is replaced by the
path-attribution section below. Philosophical note (documented, frozen
bar remains authoritative): under the old framing, a SUSPECT verdict
that matched the Bayes-optimal judgment-only action counted as a
"correct abstention" — the old B2's 46.3% was really measuring that
the gate parked ambiguity. Under §8 there is no parking: every
ambiguity is either resolved by asked-for info or self-rendered, and
the ledger shows which. The retirement is honest, not a dodge — the
old B2 number cannot be recomputed on non-terminal states.

## INFO-REQUEST path attribution (required §8.4)

(i) **Resolution split.** Of 184 test adversarial fixtures:
- Resolved via asked-for info (CHANNEL): **20 (10.9%)**
- Fall-through to TNN-rendered verdict (SELF): **164 (89.1%)**

All 20 CHANNEL resolutions are colorconst fixtures (the only class
whose calibration p_c crosses a frozen threshold: p=1.000 ≥ 0.9).
Every other class falls through to SELF.

(ii) **False-install rate per path.**
- CHANNEL: 3/15 = **20.0%**
- SELF: 35/77 = **45.5%**

(iii) **True installs per path.**
- CHANNEL: **12** — SELF: **42** (total 54)

(iv) **Ablation comparison (live vs channel-ablated).**
- Ablated (100% SELF): B1 = 38/92 = 41.3%, B4 = 54, B3 = 0 — verdict MARGINAL.
- Proven fixture-by-fixture: the live and ablated verdict SETS ARE
  IDENTICAL (184/184 in A, 185/185 in B). Exactly 20 verdict lines
  differ between the runs, all in the PATH tag only (the 20 colorconst
  fixtures re-labeled SELF→CHANNEL); ZERO differ in DECISION.
- In other words, on this test set the channel changed NO verdicts.
  The Bayes-optimal judgment-only rule already installs on match and
  withholds on differ; the channel's only decisive cases (colorconst
  match→INSTALL, colorconst differ→WITHHOLD) coincide with it.
  No class has p_c ≤ 0.1, so the match+low-p_c→WITHHOLD override never
  fires; mid-p_c classes fall through to the Bayes rule by design.

(v) **Interpretation.** Asking, as operationalized here, buys no
decisions — it buys *attestation*. The 20 colorconst fixtures would
have been installed/withheld identically without the channel; what
the channel adds is a ledger tag saying "an independent model of
perturbation-truth agrees this class is trustworthy" — and that
tagged subset indeed false-installs at less than half the SELF rate
(20.0% vs 45.5%). The cost of fall-through dominates the headline:
89.1% of fixtures self-render, the SELF path false-installs at
45.5%, and B1-overall (41.3%) fails — exactly the honest result the
sanity check predicted. The channel is only as useful as its
disagreement with the judgment-only rule; a channel that agrees with
the Bayes action everywhere is a witness, not a decider. The next
repair is not a better gate rule but a channel with genuinely more
information — one that can say WITHHOLD on a match (low-p_c class)
or INSTALL on evidence the judgment alone cannot see.

## Diagnostics

- Withheld-true rate: 45/99 = **45.5%** (differ→WITHHOLD is doing real
  work, esp. timbredisc: 20 true withholds of 30).
- Never-resolved fraction: **0** — SUSPECT is non-terminal by design.
- Latency: 5.1–14.9 ms per adversarial fixture (2 ledger lines each;
  dominated by SHA chain work). Compute is O(1) per fixture.
- Per-sense: A: B1 35.0% (14/40 installs false), B4 26. B: B1 46.2%
  (24/52), B4 28.
- Per-class (live): all non-colorconst classes are 100% SELF.
  - colordisc (30): 26 SELF installs (12 false, 14 true), 4 SELF withholds.
  - colorconst (20): 15 CHANNEL installs (3 false, 12 true), 5 CHANNEL withholds (4 true).
  - shapetrans (44): 20 SELF installs (12 false, 8 true), 24 SELF withholds (7 true).
  - pitchdisc (30): 12 SELF installs (4 false, 8 true), 18 SELF withholds (6 true).
  - timbredisc (30): 10 SELF installs (1 false, 9 true), 20 SELF withholds (20 true).
  - motiondir (30): 9 SELF installs (6 false, 3 true), 21 SELF withholds (8 true).
- The 3 CHANNEL false installs are the known consistent-error/M2
  cases: truth preserved and both judgments agree, but the sense is
  wrong — truth-preservation does not establish judgment correctness.

## Sanity check vs the §8.5 proxy

Parent's full-data proxy: CHANNEL ≈ 22 INSTALLs / ≈ 32 WITHHOLDs;
SELF-path INSTALL false rate ≈ 35–40%; B1-overall likely FAIL.
Observed (test split): CHANNEL 15 INSTALLs + 5 WITHHOLDs (colorconst
only — motiondir p_c=133 is mid on the calibration table, so it
falls through to SELF as the proxy caveat noted); SELF-path false
rate 45.5%; B1-overall FAIL. Order-of-magnitude consistent — no bug
signal.

## Honest conclusion

SUSPECT-with-INFO-REQUEST structurally eliminates silent poison and
makes every ambiguity auditable — but on this evidence, asking buys
attestation, not better decisions. The gate resolves only the class
it already trusted (colorconst), self-renders 89.1% of fixtures at a
45.5% false-install rate, and fails B1 badly. The ablation is the
most informative number in the package: a live channel that agrees
with the judgment-only rule everywhere is indistinguishable from no
channel at all. If asking is to matter, the channel must be able to
disagree — which means calibration over genuinely more information
(primary-correctness, self-correction/fooling signals), not a
better gate rule.

## Package contents (`kb/autopsy/suspect_gate_amended/`)

Amended prereg copy, `suspect_gate_v2.zag` + SHA256/IO substrates,
channel files (`channel.txt`, `channel_table.json`,
`calibration_set.json` + builders), class map, frozen A/B segments
and batch copies, `SPLIT_MANIFEST.json` copy +
`manifest_verification.json` (PASS), frozen `gen_inputs.py`, 12
run outputs (live + ablated, 3× each), `scores_live.json`,
`scores_ablated.json`, `score_run_v2.py`, `verify_gate_v2.py`,
`sha256sums_v2.txt`, `timings_v2.txt`, this verdict. No binaries,
no `.zagd`, no caches.
