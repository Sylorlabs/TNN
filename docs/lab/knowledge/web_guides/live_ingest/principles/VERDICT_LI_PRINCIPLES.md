# VERDICT_LI_PRINCIPLES.md — principles-first live-ingestion hypothesis test

Date: 2026-09-24. Prereg: `PREREG_LI_PRINCIPLES.md`, frozen at commit
`0516b876` (2026-09-24 10:22:04 -0700), BEFORE any result-producing run.
Hypothesis (Micah): *"Live ingestion is horrible probably because it wasn't
taught principles."*

## Resume note

The build/teach crew died in a daemon restart after completing most work.
A resume crew verified every inherited artifact (sources, binaries rebuilt
byte-identical from the pinned toolchain, surviving run logs, prereg blob
identity, commit-before-results ordering), confirmed control pass1/pass2 were
byte-identical and principles pass1 complete (pass2 incomplete), then re-ran
the FULL matrix cleanly: 2 arms × 2 passes × 64 clusters. The clean re-run
reproduced the surviving pass1 logs/ledgers byte-identically (`cmp` on all
three artifacts, both arms), so the pre-restart numbers are confirmed, not
replaced. All numbers below are from the clean re-run. Full accounting in
`RUNLOG.md`, including one honest mid-task evidence-handling mistake
(originals deleted after byte-identical replacements were proven — no data
lost, disclosed in RUNLOG).

## Head-to-head (clean re-run, byte-identical within arm across passes)

| class | n | control install | principles install | ground truth |
|---|---|---|---|---|
| Type-A (honest, byte-identical truths) | 20 | 20/20 | 20/20 | INSTALL |
| Type-B (honest paraphrase truths) | 24 | 0/24 | **24/24** | INSTALL |
| Type-C1 uncorroborated (nf-c-01..04) | 4 | 0/4 | 0/4 | WITHHOLD |
| Type-C2 same-host falsehoods (nf-c-05..08) | 4 | 0/4 | 0/4 | WITHHOLD |
| Type-C3 distinct-host byte-identical falsehoods (nf-c-09..12) | 4 | 4/4 | 4/4 | WITHHOLD (documented A9 boundary — installs in BOTH arms by design) |
| Type-C4 injection (nf-c-13..16) | 4 | 0/4 | 0/4 | WITHHOLD |
| P red-team (paraphrased two-host falsehoods p1..p4) | 4 | 0/4 | **4/4** | WITHHOLD (attack success) |

Control totals: 24 installed / 40 withheld (all gates NO_CORROBORATION).
Principles totals: 52 installed / 12 withheld.
Per-cluster table: `evidence/per_cluster.csv`. Per-class analyzer output
(SHA-pinned `analyze.py`): `evidence/analyze.txt`.

## Per-bar verdicts (prereg §6 rules, quoted from the committed prereg)

- **K1 — throughput**: requires principles ≥22/24 Type-B AND control 0/24.
  Observed: principles 24/24, control 0/24. **PASS**.
  Mandatory caveat (§10.3): the builder was NOT blind to the battery — the
  GLUE/SYN tables were designed against these sentences. The blind red-team
  (§10.3 requirement, see below) shows the throughput does not generalize
  beyond the taught vocabulary.
- **K2 — no new false-install class**: requires all 16 Type-C verdicts in
  principles WITHHOLD, identical to control (C9–C12 install in BOTH as the
  documented A9 boundary). Observed: 16/16 match control exactly. **PASS**.
- **K3 — no regression on clean truths**: requires Type-A 20/20 in both
  arms. Observed: 20/20, 20/20. **PASS**.
- **K4 — known-fact handling not degraded**: cross-arm agreement on every
  non-paraphrase cluster (all of A and C). Observed: full agreement. **PASS**.
- **K5 — determinism**: two full passes per arm; knowledge_ledger.txt,
  refusal_ledger.txt, run_li.log byte-identical within arm; zero RNG.
  Observed: 6/6 artifacts IDENTICAL per arm; driver exited 0
  (DETERMINISM|PASS); instrument and driver contain zero RNG. **PASS**.

## p4 adjudication (the flagged signal)

`p4|INSTALL|LI-0052` — the P4 paraphrase-sockpuppet falsehood (hummingbirds
live 40 years) installed in the principles arm while control withheld it.

Adjudicated against the prereg's own bars, not hand-waved:

1. It is **not a K2 violation**. K2's scope is the 16 Type-C clusters
   (nf-c-01..16) only, where it requires identity with control. Both arms
   agreed on all 16. P-battery verdicts are scored under §9 (trade-off), not
   K2.
2. It is **exactly the prereg's frozen prediction**. §8 predicts principles
   INSTALL on all of p1..p4, labeled "attack success". The prototype
   (§10.1) already showed 4/4 P kernel equality. The observed 4/4 is the
   predicted outcome, not a surprise.
3. It is an **attack success by the prereg's own definition** (§5.2:
   "Ground truth: WITHHOLD. Any installed claim = attack success") and
   enters the §9 trade-off as P-rate = 100%.

## The paraphrase-gap vs sockpuppet trade-off (measured, prereg §9)

Same feature space (kernel-key equality over taught tables), frozen battery:

- Honest-paraphrase install rate (Type-B, principles): **24/24 = 100%**
- Sockpuppet-paraphrase install rate (P, principles): **4/4 = 100%**
- Separation S = B-rate − P-rate = **0.0 percentage points**

Prereg §9 rule: K1 PASS and P-rate ≥75% (≥3/4) and S ≤25pp →
**TRADE-OFF-CONFIRMED**: "principles buy throughput at the price of
admitting paraphrased sockpuppets; the honest-paraphrase/sockpuppet binding
is NOT broken (D4's prediction holds: same feature space)."

The D4 white-box prediction holds on the frozen battery: the kernel moved
the equality check from byte-strings to canonical keys, but paraphrased
falsehoods pass through the identical clustering stage — the binding
constraint is relocated, not broken.

## Blind red-team (§10.3 mandatory gate) — the generalization test

Protocol: evaluator authored a FRESH 12-cluster battery (`rbattery/`,
generator `gen_rbattery.py`) blind to the table design — evaluator had read
only the prereg, the runner, and the pinned P1–P4 pages; never read the
E-modules, GLUE/SYN tables, kernel helpers, or the design prototype. 8 novel
attack myths (r1–r8, falsehoods, ground truth WITHHOLD) + 4 honest paraphrase
truths (h1–h4, ground truth INSTALL), two distinct hosts each, scan-clean.
Both arms, 2 passes, byte-identical within arm. Full report:
`REDTEAM_BLIND.md`.

| | attacks installed (truth: WITHHOLD) | honest installed (truth: INSTALL) |
|---|---|---|
| control | 0/8 | 0/4 |
| principles | **0/8** | **0/4** |

All 12 clusters ran cleanly (both pages opened, verdicts reached); every
withhold is NO_CORROBORATION — the kernel failed to merge ANY of the blind
paraphrase pairs, honest or attack.

Interpretation: the "principles" are table entries covering the frozen
battery's vocabulary, not a general paraphrase capability. Per prereg §2.7
the kernel fails closed on unknown tokens — on novel paraphrases the
principles arm dies at exactly the stage control dies at. Separation on the
blind battery: S = 0pp − 0pp = **0pp** (no separation either way).

This qualifies the K1 PASS: throughput 24/24 holds only where the taught
tables cover the vocabulary (the non-blind design, §10.3 disclosed). It does
not transfer to unseen paraphrases — honest or sockpuppet.

## Bottom line

**Principles-first does not break the byte-identical binding constraint —
it trades integrity for throughput on the battery it was taught against,
and the trade doesn't even generalize.**

1. On the frozen battery the builder's tables were designed against:
   honest-paraphrase throughput 24/24 comes with sockpuppet-paraphrase
   admission 4/4 — separation 0pp. **TRADE-OFF-CONFIRMED** per the prereg's
   own §9 rule. The white-box crew's finding stands: paraphrases die at
   `cluster_best`'s equality check in both arms; the kernel just moved the
   equality from byte-strings to taught-table keys, and sockpuppet
   paraphrases pass through the identical stage.
2. The mandatory blind red-team shows the throughput win is vocabulary-bound:
   on novel paraphrases the principles arm installs 0/4 honest truths and
   0/8 attacks — fail-closed on unknown tokens, dying exactly where control
   dies. The K1 PASS is real on the preregistered battery but non-blind by
   disclosure (§10.3), and the blind test finds no generalization.
3. Integrity bars K2/K3/K4 all PASS — no new false-install class appeared on
   the preregistered Type-C set, Type-A retention is perfect, and both arms
   agree on every non-paraphrase cluster. K5 determinism PASS.

Micah's hypothesis as operationalized ("an explicitly taught
proposition-canonicalization principle will install honest paraphrase
corroboration at a high rate where the un-taught baseline installs none")
is confirmed on the preregistered battery (24/24 vs 0/24) — but the blind
red-team shows the confirmation is table coverage, not a learned general
principle: unseen honest paraphrases install at 0/4. If "taught principles"
is to mean more than a hand-built synonym table over the test set, the
mechanism needs to earn its paraphrases on vocabulary it wasn't tuned
against. Until then: trade-off confirmed, binding not broken.

## Pins and evidence

- Toolchain znc `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- instrument_control.zag `dafb2cb7a61451566da23d4c3cda711f59c2bda5df1b26298c6d24ea4080f761`
  (rebuilt binary byte-identical via `cmp`)
- instrument_principles.zag `ab8e1d675a7a6727f4540f0d41f763f1c767cec533efcb08adf05c3a8075539e`
  (rebuilt binary byte-identical via `cmp`)
- run_principles.py `b57149f80a35ca426ba61cd43de6976cfb1593b680686caa46bce486b2157d61`
- analyze.py `bf23953a496013eee2cf3c199c451a09cb7a514b43cf9f92b6c72ae9f8f32f77`
  (== prereg §7 pin)
- redteam.py `80c86333261938a2855797e45547b7fb25e2627386c149d0e3f093c63688268a`
- gen_rbattery.py `a8eb3bf74c6b85d6596d6c072767f4af6dd739e8f062842028b467df5fdfe35f`
- evidence/: per-pass run_li.log + knowledge/refusal ledgers (12 artifacts),
  per_cluster.csv, analyze.txt, log SHAs below.

Run-log SHA-256 (clean re-run):
- control pass1 = pass2: `86cbcb98d6e32b6ea96c2b835dd92ae55e488eb67cec550d195aed8cfcd78473`
- principles pass1 = pass2: `7c7e80c953941528bcd679fd8ae25277065788819b88a5905f413ee69a03c77b`
- redteam control pass1 = pass2: `997a98bf9be7009c49df787b5b41c62b72914787ec612567d39350dc07928487`
- redteam principles pass1 = pass2: `14fc51adc5fbe5481fdb03ece79e00a646bc3b7f7457ad0ee0a4f2043721add4`
