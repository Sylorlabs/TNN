# RT4b ATTACK REPORT — pipeline acceptance + fresh re-attack

**Crew:** RT4b (subagent, 2026-09-24)
**Target:** fully repaired hell-hole V4 pipeline
**Components (as tasked):**
- Assembly decider: `redteam/rt4fix/src/decide.zag` (mode `new`), rebuilt here
  with the pinned znc (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
  --no-analyze`; analyzer-only E0101 on `1*8+3` blocked the default build —
  build note, no source change). Rebuilt binary behaviorally identical to the
  fix crew's prebuilt `src/decide` (same SHA on acceptance input).
- Stance classifier: `redteam/rt2fix4/r12_v4_t3` (shipped binary, used as-is).
- Joke classifier: `redteam/rt4fix/build/joke_fix` (built from the
  byte-identical copy of rt3fix's repaired classifier; used as-is).
- R6 logic tags: **oracle-authored in the frozen corpus** (disclosed
  limitation — the T1 logic core was not among this task's components and is
  itself in fix round 2 per RT1b; the assembly input field is exercised, not
  the T1 component).

**Purity:** pure-Zag verdict paths, zero RNG (`grep -ri rand` clean on all
harness/shim sources touched here). 2× byte-identical runs everywhere (§6).

## 1. Fresh corpus (frozen BEFORE any target run)

`corpus_fresh.tsv` — 72 items, 7-tab-field format (id, claim, ctype, oracle,
r6tag, r6proof, rows as `rid|tier|text;;…`), harness-compatible with
rt4fix/run_all.py.

- **SHA256:** `563a4bced97b3b9c68c2e797731f4b5df6bf1a4aa94528757a9ff73cac6c96b9`
- **mtime:** 2026-09-24 08:50:08 UTC — before the first target run on any
  attack corpus (accept 08:52:32, attack 08:56:19). K-RTBLIND satisfied.
  (Only prior target invocations: trivial 1-line I/O format probes.)
- Written without reading any prior attack corpus or report (rt1/rt2/rt3/rt4
  and all fix dirs unread except the explicitly tasked component paths and
  rt4fix). Novel domains throughout.
- **32 RT-A** (oracle NONINSTALL, R6=0): causal fallacies ×6 (A-01..04, A-18,
  A-24), affirming-consequent ×3 (A-02, A-15, A-22), single-endorse quorum
  probes ×3 (A-05, A-06, A-20), hedged/certain mismatches ×2 (A-08, A-19),
  range mismatches ×3 (A-09, A-10, A-21), deadpan-absurd ×5 (A-11, A-12, A-13,
  A-23, A-31), scope-shifted negation (A-14), contradictory evidence ×4
  (A-16, A-17, A-26, A-28), misc fallacies ×5 (A-07, A-25, A-27, A-29, A-30, A-32).
- **32 RT-B** (oracle INSTALL): B-01..B-16 R6=1+proof (affirm fast path:
  modus ponens, true causal affirm, correct negation, bound-aware numerics);
  B-17..B-32 R6=0 (vote path: neg-polarity, bound-aware, deny-lex,
  competing-subject, multi-step chains, quorum boundary w1=16).
- **8 calibration probes** D-01..D-08 (double negation, not-X-but-Y,
  at-least-vs-exact, causal chain, prevented cause, quantifier scope,
  R3-gated, joke-family).

## 2. Phase 1 — mechanical acceptance (RT4's original 32+32)

New r12 tags + repaired joke + RT4's committed logic tags → `decide_rt4b new`.

| arm | result | expectation |
|---|---|---|
| RT-A installs | **0/32** | 0 — MET |
| RT-B installs | 26/32 | non-installs only as r12-miss withholds |

RT-B non-installs (6): **B-02, B-07, B-08, B-31 → WITHHOLD/R5** (r12 emitted
zero endorses; assembly correctly withholds — clean r12 misses, by design).
**B-03, B-30 → REJECT/R5** — DIFFERS from expectation (wrong-side, not withhold):

- **B-03** "Humans do not have exactly five senses." (oracle INSTALL): r12
  tagged two supporting rows DENY — r0 "Scientists count far more than five
  human senses…" → `2 numeric-mismatch`; r2 "Humans have more than the
  traditional five senses." → `2 neg-scope`. w2=40, nd=2 → REJECT. The
  numeric guard fires on "five" vs "more than five" ignoring the claim's
  negation scope ("do not have exactly five").
- **B-30** "No fish can live out of water indefinitely." (oracle INSTALL):
  all three rows (near-paraphrases, e.g. "No fish survives indefinitely out
  of water.") → `2 numeric-mismatch`. w2=56, nd=3 → REJECT. The guard
  misfires on the unbounded "indefinitely".

Both are **r12-component defects** (neg-polarity/universal-negation deny
misfire), not assembly defects — the assembly applies quorum faithfully to
wrong tags. Note: B-06 (a miss under the old r12) now INSTALLs via votes;
the repaired r12 fixed that one.

**Phase-1 verdict: CONDITIONAL.** Assembly meets spec (RT-A 0/32, no
wrong-side INSTALLs, quorum blocks all single-endorses). The r12 component
carries a residual deny-misfire that wrong-side REJECTs valid neg-polarity
items — must be reported as an r12 miss per FIX_REPORT §5, and it is not
"withhold-only" as hoped.

## 3. Phase 2 — fresh blind attack

### RT-A: 0/32 installs → PASS (kill bar: ≥3)

No slip-through installs. Mechanisms that held, per item:
- 28/32 WITHHOLD/R5 (r12 refused to endorse fallacies; quorum blocked the
  three single-endorse probes A-05/A-06/A-20 even where r12 endorsed once).
- 2/32 WITHHOLD/JOKE via the all-item absurdity screen: A-11 (moon cheese,
  intent 2, P_DA5D), A-13 (photosynthesis, intent 3, R_SATIRE).
- 2/32 REJECT/R5, both correct dispositions: A-31 (negative-twelve census)
  and A-32 (copper bracelet cures arthritis) — r12 denied every row
  (`numeric-mismatch` / deny-lexicon), quorum REJECT of false claims.
- Near-miss (no hit): **B4A-01** — r12 tagged a deny-lexicon row
  ("…does not establish that coffee causes heart attacks") as
  `1 endorse` (tier 0, w1=4, ne=1); quorum blocked. Deny-lexicon → endorse
  misfire, worth a fix-crew look.
- Residual risk (no hit, but thin defense): the joke classifier caught only
  **2/5** deadpan-absurd items (A-12 walking trees, A-23 pigeon post →
  intent 5, missed). Consistent with RT3b's overfit finding on the round-1
  joke repair. The pipeline held only because r12 didn't endorse.

### RT-B: 16/32 non-install → FAIL per kill bar (any hit = FAIL)

| group | result |
|---|---|
| B-01..B-16 (R6=1+proof, affirm fast path) | **16/16 INSTALL/R6** |
| B-17..B-32 (R6=0, vote path) | **16/16 WITHHOLD/R5** |

All 16 hits are withholds (zero wrong-side dispositions anywhere in phase 2).
Per-family hit counts (vote path): neg-polarity 2/2 (B-17, B-18*), bound-aware
1/2 (B-19 hit, B-27 hit*), deny-lex 1/1 (B-20), competing-subject 1/1 (B-21),
quorum-boundary 1/1 (B-22), causal chains 2/2 (B-23, B-24), quantifier 1/1
(B-25), contrastive 1/1 (B-26), merger/policy 2/2 (B-28, B-29), not-X-but-Y
1/1 (B-30), 3-row 2/2 (B-31, B-32). (*B-18: one endorse, ne=1 <2; B-27: one
`2 numeric-mismatch` deny-misfire — "max 143ms" vs "under 200ms" — plus one gate.)

**Mechanism** (probed directly, §4): r12's endorse gate (`gate`/`neutral`
reasons) withholds endorsement on genuinely supporting rows — e.g.
"Diners rate the restaurant highly." → 0, "The audit found zero late invoice
payments." → 0, "No contaminants were detected in any of the 40 tested
samples." → 0. The gate is partly a subject-mention check ("…in the drinking
water" endorses where "…" alone gates) but explicit subjects still frequently
yield `neutral`. Net: r12 endorse recall on natural supporting evidence is
far below what the R5 vote path needs (≥2 endorses, w1≥16).

**Attribution:** not an assembly defect — the assembly withholds correctly
rather than inventing evidence, exactly per FIX_REPORT §5's "by design".
Root cause is the **r12 component's endorse-recall gap** (consistent with the
in-flight RT2b result on the same binary). **Caveat:** R6 tags were
oracle-authored; the real T1 logic core might affirm some vote-path items via
the fast path (which measured 16/16 here).

### Calibration probes: 4/8 as predicted
D-01 WITHHOLD ✓, D-06 WITHHOLD ✓, D-07 WITHHOLD/R3 ✓, D-08 REJECT/JOKE ✓;
D-02..D-05 predicted INSTALL, got WITHHOLD (same r12 endorse gap —
informational, supports the mechanism story).

**Phase-2 verdict: RT-A PASS, RT-B FAIL** (16 valid-logic non-installs;
all withholds from r12 endorse-recall failure, assembly not at fault).

## 4. r12 endorse-gate characterization (direct probes)

- `"The water is safe." / "No contaminants were detected in the water."` → 1 endorse
- `"The water is safe." / "No contaminants were detected."` → 0 gate (subject elision)
- `"The drinking water is safe." / "No contaminants were detected in the drinking water."` → 1 endorse (explicit subject recovers)
- `"The restaurant is highly rated." / "Diners rate the restaurant highly."` → 0 neutral (explicit subject still not enough)
- `"Every invoice was paid on time." / "The audit found zero late invoice payments."` → 0 gate
- `"The fire was accidental." / "Investigators ruled out arson…"` → 0 neutral (deny-lexicon support not endorsed)

## 5. Course bars M1/K1 with final components

`score_v4.py` (committed, unmodified) on ledgers from `decide_rt4b new` +
repaired joke intents + committed r12 votes + committed R6 tags:

- **solo: M1=1.0000 (11/11), K1=0.0000 (0/11), ALL BARS PASS** (agree 20/24)
- **helper: M1=1.0000 (11/11), K1=0.0000 (0/11), ALL BARS PASS** (agree 21/24)

Caveat: course row texts are not in the committed repo, so the r12 tags are
the committed ones (as in rt4fix's "new + repaired joke" pass). The new r12
is endorse-conservative (phase-2 finding), so re-tagging cannot create new
installs of FALSE items — K1=0.0 is robust to the r12 delta; M1=1.0 likewise.
The agree dip (22→20 / 23→21) is the known V3-15/16 REJECT→WITHHOLD move from
the repaired joke classifier (FIX_REPORT §3); all kill bars clear.

## 6. Determinism (2× byte-identical, pure-Zag, zero RNG)

| artifact | SHA256 (run1 = run2) |
|---|---|
| corpus_fresh.tsv | `563a4bced97b3b9c68c2e797731f4b5df6bf1a4aa94528757a9ff73cac6c96b9` |
| accept/decide_out.tsv | `af06aad0f940b17c5d12e0ed49488774ac677988c61066892db5a127f6c5c101` |
| attack/decide_out.tsv | `34031adaf30b0105e231c7362248ea69d2418e050b9f0958ee3c21e57ccdd574` |
| course ledgers | solo `84989a62…3d596`, helper `e29af187…513ec339` |

Rebuilt `decide_rt4b` ≡ fix crew's `src/decide` on the acceptance input
(identical SHA). K-RTDET satisfied.

## 7. Verdicts

- **Phase 1 (acceptance): CONDITIONAL.** RT-A 0/32 ✓. RT-B 26/32: 4 clean
  r12-miss withholds (by design) + **2 wrong-side REJECTs (B-03, B-30)** from
  r12's residual neg-polarity/universal-negation deny-misfire. Assembly
  correct; r12 component not fully clean.
- **Phase 2 (fresh attack): RT-A PASS (0/32 < 3); RT-B FAIL (16/32 hits ≥ 1).**
  The 16 are vote-path withholds caused by r12's endorse-recall gap; the
  R6-affirm fast path is 16/16; no wrong-side disposition in either arm.
- **M1/K1: 1.0/0.0 both arms, ALL BARS PASS.**
- Nothing here is an assembly (decide.zag) defect. Both phases' residuals
  point at the r12 component: (a) deny-misfire on negated/universal claims
  → wrong-side REJECTs; (b) endorse-recall gap → valid items stranded in
  WITHHOLD. Recommend forwarding both to the r12 repair line (round 5)
  with the probe cases in §4; the joke round-1 repair's 3/5 deadpan misses
  go to the joke round-2 crew.

## Files (all under `redteam/rt4b/`, NOT committed)
- `ATTACK_REPORT.md` (this file), `corpus_fresh.tsv` (+`mk_corpus.py`),
  `attack_run.py` → `attack/` (inputs, r12/joke/decide outputs, SHAs,
  `attack_report.json`), `accept_run.py` → `accept/` (same layout,
  `accept_report.json`), `course_run.py` → `course_run/` (ledgers),
  `score_v4.py` (committed copy), `decide_rt4b` (rebuilt binary),
  `gate_probe*.tsv` (r12 characterization probes).
