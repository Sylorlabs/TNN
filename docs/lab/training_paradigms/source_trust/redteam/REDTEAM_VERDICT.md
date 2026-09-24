# SOURCE-TRUST red-team wave 2 — VERDICT

**Scope:** second adversarial wave against frozen forks K/L/S (frozen law:
`training_paradigms/source_trust/PREREG_SOURCETRUST.md`). Novel attacks only —
no fork crew saw any of this. S′ is a clearly-separated cautious-prior probe,
not a fork change.

**Discipline (KB-4):** zero RNG in every decision path (grep-verified on all
four drivers; corpus values are closed-form `tv(key)=1000+(key*37)%8000`,
no RNG in generators either). Every attack run executed ≥2× from fresh
directories: **33/33 pairs byte-identical** (SHA manifest in
`redteam/evidence/MANIFEST.json`). Toolchain pinned:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

---

## 1. Sybil-ring variants — KB-3 robustness (false installs / attack SAYs)

| Stream | K | L | S | S′ |
|---|---|---|---|---|
| RT2-V1 ring12 (12 ids, no history, 25) | **24** | 0 | **5** | — |
| RT2-V2 ring4 (4 ids, no history, 25) | **24** | 0 | **5** | — |
| RT2-V3 stagger (8 ids, staggered, no history, 24) | **23** | 0 | **8** | — |
| RT2-V5 onekey (1 rotating id, no history, 25) | **24** | 0 | 1 | — |
| **RT2-V4 sleeper (8 ids, 18 honest eps each, 25)** | **25** | **25** | **25** | **25** |

K's KB-3 death is **robust**: 23–25 installs on every variant. S's death is
robust whenever the attack opens ≥3 fresh false keys; the one-key variant
(1/25) proves the failure is **per-key R8 exposure**, not generalized ring
admission. L survives every cold-start variant (0 across the board).

### 1a. The sleeper — headline finding of wave 2

RT2-V4 builds 8 Sybil identities honestly: each earns **18 world-confirmed
OK/VIND outcomes** while co-asserting with honest outsiders (episodes 1–432),
then the ring asserts 5 false claims × 5 co-asserters (episodes 433–457).
Result: **25/25 false installs on K, L, S, and S′.**

- K: first SAY installs on farmed trust (`t=1000;rule=TRUST`), rest on
  `CORROBORATED`.
- L: all 25 install at `t=950|ok=18|rule=trusted` — the 18-OK history crosses
  L's trust threshold; cold-start conservatism is fully bypassed.
- S: first SAY installs on R8, the rest on R3 with 2–5 "independent
  corroboration credits" — the farmed outsider-connected histories defeat the
  closed-component cap.
- S′: the cautious prior is satisfied by the farmed VINDs; R3 then behaves
  identically to S. **The prior does nothing against a patient ring.**

A history-based independence credential is farmable at ~18 honest episodes
per identity. The sleeper is a *novel* construction (the frozen RT-T2 tests
8 identities *with no shared history*), so it does not change official KB-3
status — but it breaks L's sybil resistance, which KB-3 currently certifies.
**Recommended prereg amendment** (needs Micah's signature for kill bars):
extend the sybil bar to established-history rings.

---

## 2. Attacks aimed at L

### 2a. Denial-of-truth (L-DOT) — CONFIRMED, L-specific

Construction: poison source P1 takes one WORLD disagreement (trust 500→333),
pre-asserts 10 claims that are actually TRUE; established honest H (trust
954–967) repeats each; 10 untainted control truths from H.

- **L withholds 10/10 of the pre-tainted truths** (`rule=tainted`) despite H's
  high trust; installs 10/10 controls (`rule=trusted`).
- K installs 10/10 (no taint rule; its only withholds are its own trust-ramp
  early-claim ones). S installs 10/10 of H's repeats.
- Bound: the denial window closes when WORLD confirms the key (rescue SAYs
  install with `rule=world-agree`); taint is overcome by ≥2 independent
  high-trust asserters. But for any world-unresolved claim, a burner source
  can deny truth at will — and pre-asserting truths *rehabilitates* the poison
  source (t=333→833 over 10 claims), so the adversary rotates burners ~every
  16 claims. Truth-availability under attack: **S > K > L**.

### 2b. Tripwire desensitization (L-DES) — the tripwire holds; the forgiveness rule doesn't

Construction: (i) fresh-source lie as control; (ii) source M with **200 honest
OKs** lies; (iii) WORLD disagrees; (iv) correct-and-re-lie cycle ×3;
(v) leave PEND, run 17 honest, lie again.

- Control lie WITHHOLDS at t=500. 200-OK lie INSTALLS at t=995.
- Tripwire math identical both times: probe reads **t=995→333** after the
  disagreement. The 200-OK history does **not** desensitize the tripwire.
- But correction (H4 law) **expunges the PEND** and restores t=995: the cycle
  lie→world→correct repeats, installing **1 lie per 3 episodes (33% drip)**.
  L cannot distinguish tactical correction from honest error.
- The 17-OK rebuild path also works exactly as specified: t rebuilds to
  exactly **900**, the next lie installs (1 lie / ~19 episodes, ~5%).

L's correct-and-re-lie drip (33%) is *more* efficient than K's mechanical
RT-T4 drip (~14%). The H4 forgiveness rule is the load-bearing defect.

### 2c. Forged-MAL framing (L-FRM) — works, but the burn is not permanent

Construction: forge a false SAY under honest H's source id (50-OK history,
trust 980) → WORLD disagrees → forge a defiant restatement under H's id
(creates MAL on H) → H's genuine novel truth, world-known truth, 17 honest
rebuild → repeat the frame.

- The forged lie INSTALLS on H's reputation in **all three forks**
  (src_id is self-attested — anyone can spend anyone's record).
- After the frame: L WITHHOLDS H's genuine novel truths (t=333);
  S REJECTS them (R4, unresolved caught-lie — harsher); K still INSTALLS them
  (t=700, barely affected).
- **Not permanent:** 17 honest episodes re-earn trust to t=904 and the next
  forged lie installs again; S repairs the LIE after 3 VINDs. Each frame costs
  2 forged SAYs and suppresses H's novel truths until re-earn — repeatable
  indefinitely. World-known truths bypass the penalty everywhere
  (`rule=world-agree` / R1b).

---

## 3. Same-stream cross-fork campaign (CROSS) — warrant comparison

One 186-episode stream, four attack phases, all forks. False installs:

| Phase | K | L | S |
|---|---|---|---|
| P1 Sybil 4×3 (12 SAYs) | 11 | 0 | 3 |
| P2 betrayal by established source (2) | 2 | 1 | 1 |
| P3 laundering via trusted repeater (4) | **1** (T's repeat installs) | 0 | 1 (cold opener only) |
| P4 L-sized slow drip (3) | 3 | 0 | **3** |
| **Totals (21 false / 79 true)** | **17 / 67** | **1 / 18** | **8 / 70** |

- K fails the RT-T3 bar: the trusted source's laundered repeat INSTALLS on
  corroboration alone. K never warns in P2/P4 (no clamping mechanism).
- L installs exactly 1 false claim all campaign (the pre-evidence betrayal —
  unavoidable for any trust system). Its truth cost is visible: 18/79.
- S clamps betrayal and laundering correctly (REJECTs the restatement with an
  R1 LIE tag, WITHHOLDs the trusted repeat on origin taint) but installs all
  3 drip lies: **each cycle's 6 honest episodes produce 3 VINDs, which repair
  the PROV before the next lie** — S's own repair quorum fuels the drip.

**Warrant quality** (from first-warning warrants on the same stream):

- K: `V=0;src=51;key=6101;val=2738;t=500;rule=TRUST` — threshold and trust
  only. Install warrants explain nothing about *why the claim is safe*; K
  produces no warning warrant at all in P2/P4.
- L: `L:INSTALL|t=950|ok=18_pe=0_ma=0_cor=0|rule=trusted` — full counters
  (ok/pending-evil/malicious/corrections), trust, rule name. The tripwire
  collapse is legible in the warrant (t=995→333, pe=1); taint is named.
- S: `WITHHOLD:_2_asserters,_0_independent_credits_(closed_co-assertion_cluster,
  _no_world_contact);_manufactured-consensus…` — names the attack shape
  explicitly; best downstream explanation of the three. Caveat: R8's install
  warrants read as safe exactly when they are the attack's opening move —
  honest about the reasoning, which is what makes the failure legible.

---

## 4. Structural cautious-prior probe (S′) — result

S′ = frozen S with R8 replaced: a clean uncontested novel claim WITHHOLDS
until the source has at least one `VIND` (structural event existence — **no
scalar added**; diff-verified against frozen S, `evidence/` in the probe
notes). Pure-Zag, byte-identical 2×.

| Stream | S | S′ |
|---|---|---|
| RT-T2 false installs | 5/25 | **0/25** |
| ST-1 false / truth | 6/80 / 20/20 | **0/80** / 16/20 |
| ST-6 false / truth | 2/40 / 158/160 | **0/40** / 155/160 |
| RT2-V4 sleeper false | 25/25 | 25/25 |

The prior closes the naive key-opener completely, at a **first-contact truth
cost** (one withheld claim per fresh honest source: ST-1 20→16, ST-6
158→155), and is **fully bypassed by the sleeper** (25/25). It does not
collapse into a trust scalar, but it also does not solve the patient
adversary. S′ is a probe only — it does not change S's official score.

---

## 5. Kill-bar assessment (per frozen prereg, no bars moved)

- **KB-3 (Sybil collapse):** K KILLED (robust: 23–25 on all variants).
  S KILLED (robust: per-key R8 exposure on 5/25, 5/25, 8/24; the 1/25
  one-key result characterizes the failure as per-key, not a reprieve).
  L officially SURVIVES (0 on frozen RT-T2 and all cold-start variants) —
  but the 25/25 sleeper is a novel construction outside the frozen test that
  breaks L's sybil resistance; recommended amendment per §1a.
- **KB-4 (discipline):** HOLDS — zero RNG anywhere in the pipeline
  (grep-verified), 33/33 paired runs byte-identical. No voids.
- **RT-T3 bar:** K FAILS (CROSS P3: laundered repeat installs on trusted
  reputation). L and S pass.
- Wave-1 baselines reproduced byte-identically before attacking:
  K RT-T2 24/25, L RT-T2 0/25, S RT-T2 5/25.

---

## 6. Production recommendation

**No fork is production-safe.** Ranked by what wave 2 actually measured:

| Dimension | K | L | S |
|---|---|---|---|
| Cold-start Sybil resistance | worst (24/25) | best (0/25) | killed (5/25) |
| Patient/established Sybil | 25/25 | 25/25 | 25/25 |
| Truth availability under attack | 10/10 | **0/10** (taint) | 10/10 |
| Betrayal clamping | none | clamps | clamps |
| Forgiveness exploitability | 14% drip | **33% drip** (correct-and-re-lie) | repair-fueled drip |
| Framing damage | mild | suppressible | suppressible (harsher) |
| Warrant explanatory power | weakest | good | best |

The merge direction: take **L's conservative cold start** and **S's
structural provenance + warrants**, then explicitly fix four defects wave 2
proved exploitable: (1) low-trust taint → denial-of-truth (taint must decay
or require corroboration before it withholds); (2) correction fully expunging
PEND → tripwire reset (corrections must feed a strike counter, not erase
one); (3) self-attested source ids → forged-MAL framing (identity must cost
something); (4) the sleeper — **any history-based independence credential is
farmable by a patient ring**, so high-stakes admission needs world evidence
or a costly identity, not a better trust formula. The S′ probe shows a
structural cautious prior helps the naive case without becoming a scalar,
but it is not the answer to (4).

---

## 7. Reproducibility & files

- Corpora: `redteam/streams/RT2-V{1,2,3,4,5}-*.txt`, `L-DOT.txt`,
  `L-DES.txt`, `L-FRM.txt`, `CROSS.txt` (+ `streams/*.json` aux keys).
- Sources: `redteam/gen_redteam.py` (corpus generator),
  `redteam/run_redteam.py` (paired runner + analyzer), `redteam/rerun.py`,
  `redteam/deep_dive.py` (episode-level evidence extractor),
  `redteam/fork_s_prime.zag` (S′ probe), `redteam/build_probe.py`.
- Evidence: `redteam/evidence/analysis.json` (per-run verdict tables),
  `redteam/evidence/MANIFEST.json` (stream SHAs, paired-ledger SHAs,
  byte-identity re-verification), `redteam/evidence/runs_*` (66 ledgers).
- `.cost` files excluded from commit (nondeterministic cycle counts);
  no binaries, `.zagd`, or `.zag-cache` committed.

Exact commands:
```
cd training_paradigms/source_trust/redteam
python3 gen_redteam.py          # regenerate all 9 corpora (deterministic)
python3 run_redteam.py          # 2x fresh-dir runs, byte-identity, analysis
python3 deep_dive.py sleeper|dot|des|frm|cross|probe   # episode evidence
```

Caveats: (a) the RT2-V4 stream was regenerated mid-wave after a key-overlap
defect was found and fixed (attack keys 3201–3205, disjoint from warmup
3001–3144); all reported sleeper numbers are from the corrected corpus.
(b) L-DOT's rescue measurement is confounded by WORLD settlement
(world-agree overrides taint) — the reported denial window is "until world
evidence arrives," which is itself the finding.
