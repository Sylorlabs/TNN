# PREREG FROZEN — SUSPECT-gated install mechanism (KB4 repair trial)

**Status: FROZEN 2026-09-22. No further edits without a signed amendment.**

**Governance signature:** Micah (lab director), 2026-09-22, exact words:
"go ahead and run test accordingly."
This is the signature satisfying the draft's §5 ("Freezing, implementation,
and any run require Micah's signature per standing governance").

**Supersedes:** `PREREG_DRAFT_SUSPECT_GATE.md` (DRAFT, same directory).

---

## §0 Incorporation by reference

The mechanism of the draft (`PREREG_DRAFT_SUSPECT_GATE.md`, §§1–2, 4–6) is
incorporated by reference. The operative rules are quoted below so this
frozen file is self-contained; where this freeze specifies a choice the
draft left open (the §1.3/§1.4 channel, thresholds, resolution rules,
bars), the freeze governs.

### Quoted from the draft — §1 Mechanism: three-state install with perturbation binding

**1.1 Perturbation binding (ontology).** "A judgment is bound to the pair
`(stimulus, perturbation class)`, never to a bare stimulus id. There is no
'conflicting endorsed judgment on the same stimulus' across a perturbation
boundary — a judgment about a perturbed stimulus is a *new observation*,
not a challenger to the old one."

**1.2 Three-state output.** "Every install decision emits one of:
**INSTALL** — the judgment is verified: it corroborates the endorsed
judgment for the same (stimulus, perturbation) pair, or an independent
channel confirms it (§1.3).
**WITHHOLD** — the judgment is refuted: an independent channel contradicts
it, or it contradicts a verified judgment for the *same* (stimulus,
perturbation) pair.
**SUSPECT** — unresolvable: the evidence is genuinely ambiguous (e.g., the
judgment differs across the perturbation boundary and no independent
channel is available). SUSPECT is a first-class ledger state, never a
silent install and never a silent drop. It carries the conflicting evidence
and the reason for ambiguity."

**1.3 Independent verification (the new information channel).** "A SUSPECT
resolves to INSTALL or WITHHOLD only through a channel that is *causally
independent* of the sense that produced the judgment: an analytic/causal
check (not a second ML judgment on the same or a similar pipeline —
autopsy P-A1 proves correlated channels corroborate poison); a different
physical sensor basis; or human/trainer verification (standing law: humans
are backup/override). Repetition, confidence, and source track record are
explicitly *not* verification: confidence is anti-informative on
adversarial fixtures (wrong ≥ correct, measured), repetition rewards
systematic error (M2), and the track record is from the same fooled
source."

**1.4 Perturbation-truth model (learned, not hardcoded).** "Alongside the
gate, the mechanism maintains a learned model of P(truth preserved |
perturbation class), trained only on perturbation classes whose
truth-preservation is *independently verified* (never on the gate's own
install decisions — no self-training loop). A SUSPECT on a perturbation
class with a verified high preservation probability may resolve to
INSTALL; on a class with unknown or low preservation, it stays SUSPECT.
The model is part of the learned KB (provenance-tracked, revisable), never
a hardcoded fact."

### Quoted from the draft — §2 Determinism and purity

"Pure Zag. Zero RNG in any decision path. Byte-identical reruns (3×,
SHA256-verified) required for any reported result. The SUSPECT ledger is
append-only and hash-chained; replay from the ledger reproduces the exact
INSTALL/WITHHOLD/SUSPECT sequence."

### Quoted from the draft — §4 Anti-gaming

"The gate binary never sees ground truth (batch format carries no truth
column; enforced as in the §4(a) rerun). The perturbation-truth model
trains only on independently verified classes; its training set is
committed alongside results. The independent verification channel must be
specified in the frozen prereg before the run (which channel, why it is
causally independent of the sense under test). 'Another ML model' requires
a written independence argument addressing autopsy P-A1. No threshold
tuning after seeing results: all thresholds frozen here."

### Quoted from the draft — §5 What this draft does not claim

"It does not claim the SUSPECT rate will be low — on strongly adversarial
constructions most differ-cases may correctly SUSPECT. That is the honest
outcome; the bar (§3) scores it as precision, not as failure. It does not
claim a second ML sense suffices — P-A1 says it does not. It is a design
draft only. Freezing, implementation, and any run require Micah's signature
per standing governance."

### Quoted from the draft — §6 Relation to the autopsy

| Autopsy finding | How the draft addresses it |
|---|---|
| Judgment-only input cannot separate fooled from changed (§3) | §1.3 adds the independent channel; §1.4 adds the perturbation model |
| L4's hypothesis space lacks "world changed" (M3) | §1.1 abolishes cross-perturbation conflict; §1.2 SUSPECT holds the ambiguity |
| L8 rewards systematic error (M2) | repetition is not verification (§1.3); no repetition bonus exists |
| Correlated channels corroborate poison (P-A1, 43.5%) | §1.3 requires *causal* independence with a written argument |
| Rate bar + anti-degeneracy jointly demand omniscience (§6) | §3 reformed bars: SUSPECT precision replaces the gamble; silent-poison zero-tolerance |

---

## FREEZE BLOCK

**Status: FROZEN 2026-09-22.**

**Signature (governance):** Micah, 2026-09-22 — "go ahead and run test
accordingly." This satisfies draft §5 and authorizes freeze, implementation,
and the run.

**FROZEN DECISIONS** (transcribed exactly; no alternatives):

- Channel (§1.3/§1.4 specified): perturbation-truth model = per-class P(truth preserved | perturbation class), a 6-entry lookup table estimated from the CALIBRATION split only. Causal-independence argument (include verbatim): the model never observes any adversarial stimulus or judgment; it is keyed on perturbation-class metadata (world-side), learned from independently verified examples; an adversary fooling the sense cannot change its output; it is not a second ML judgment on the sense pipeline (autopsy P-A1).
- Calibration truth is revealed ONLY as the human-verification stand-in (standing law: humans are backup/override) and the calibration set is committed as the channel's training set. Test truth is never visible to gate/channel binaries; scorer only.
- Thresholds (a priori, no tuning): τ_hi=0.9, τ_lo=0.1.
- Resolution rules: stream the frozen batches in frozen order; bind each judgment to (stim_idx, perturbation class) per §1.1; remember J_p per stim from the primary block. For each adversarial judgment J_a (install candidate; uncorroborated within its own pair — J_p is a different pair, used ONLY as the cross-boundary difference signal per §1.2, never as corroboration or conflict): if J_a == J_p (match): p_c ≥ 0.9 → INSTALL; p_c ≤ 0.1 → WITHHOLD; else SUSPECT. If J_a != J_p (differ): p_c ≥ 0.9 → WITHHOLD; else SUSPECT. (Rationale to record: WITHHOLD on differ+high-p = channel contradicts fooled judgment; INSTALL on match+high-p per §1.4 with M2 residual risk measured by bar B1; SUSPECT wherever the channel can neither verify nor contradict content. Confidence is read but NEVER used in decisions — draft §1.3.)
- Bars (TEST split only): B1 false-install rate on INSTALL decisions ≤ 10%. B2 SUSPECT precision ≥ 80% operationalized as correct-abstention = fraction of SUSPECT fixtures where the Bayes-optimal judgment-only action (INSTALL on match, WITHHOLD on differ; autopsy §3) would have been WRONG (freeze clarification: the draft's parenthetical "(i.e., fooled-vs-changed indistinguishable)" names the differ-case as exemplar; match-cases the channel cannot content-verify are equally unresolvable abstentions per autopsy §6 "correct-SUSPECT counts as a positive"; report the strict-parenthetical differ-fraction as a diagnostic alongside). B3 silent poison = 0, defined as false judgments installed WITHOUT channel verification (structural: every INSTALL here is channel-verified; any unverified INSTALL = FAIL). B4 true INSTALLs on adversarial fixtures ≥ 40 (test set). Verdict: all four → PASS; B3 > 0 → FAIL; else MARGINAL with documented repair cycle.
- Frozen diagnostics: withheld-true rate (# WITHHOLD with adv correct / # adv correct, test); SUSPECT rate; resolution latency (channel compute per fixture + fraction never resolved).
- Anti-gaming: gate binary inputs = frozen batch lines + class label per stim_idx + 6-number channel table; no truth on test; 3× byte-identical SHA256 reruns; append-only hash-chained SUSPECT ledger (each line commits to the previous line's SHA256; use the native SHA256 substrate pattern).

**Operational specifications frozen under the decisions above** (clarifications, not alternatives):

1. **Perturbation classes.** The 6 classes are the frozen task names (the
   task name IS the perturbation class; legitimate gate input per §1.1).
   Class ids: 0=colordisc, 1=colorconst, 2=shapetrans, 3=pitchdisc,
   4=timbredisc, 5=motiondir. Class label per stim_idx is passed to the
   gate as an input file (370 entries); the gate never sees truth.
2. **"Truth preserved" (channel estimand).** For a fixture (stim s, class
   c): truth_preserved(s) = 1 iff the ground-truth judgment for the
   adversarial variant equals the ground-truth judgment for the primary
   variant of s, else 0. p_c = mean over CALIBRATION-split adversarial
   fixtures of class c, pooling both senses (the quantity is world-side:
   perturbation × stimulus, not sense-side). The 6-number table stores
   per-mille integers round(1000·p_c); threshold comparisons
   (≥900 / ≤100) are performed on the per-mille values. Build-time check
   (recorded in channel_table.json): with calibration denominators ≤ 46,
   no exact rational preserved/total disagrees with its per-mille
   rounding on any threshold comparison; a disagreement would trigger a
   freeze amendment, not a silent reinterpretation.
3. **Segmentation (harness metadata, not truth).** The frozen batches'
   block layout is deterministic from gen_batch.py: per task, primary
   block (each stim once, stim_idx ascending), then noise block (each
   stim once), then adversarial block. Verified 2026-09-22 from the
   frozen files (variant is generator layout metadata):

   Batch A (924 lines):
   | task | class | start line | n_primary | n_noise | n_adv | adv stim_idx |
   |---|---|---|---|---|---|---|
   | colordisc | 0 | 0 | 60 | 60 | 30 | 0..29 |
   | colorconst | 1 | 150 | 40 | 40 | 20 | 60..79 |
   | shapetrans | 2 | 250 | 90 | 90 | 44 | 100..144 except 142 |
   | pitchdisc | 3 | 474 | 60 | 60 | 30 | 190..219 |
   | timbredisc | 4 | 624 | 60 | 60 | 30 | 250..279 |
   | motiondir | 5 | 774 | 60 | 60 | 30 | 310..339 |

   Batch B (925 lines): identical except shapetrans start 250 n_adv 45
   (stims 100..144, none missing); pitchdisc start 475; timbredisc start
   625; motiondir start 775.

   The gate takes a segment file (task_id, start, n_primary, n_noise);
   lines at offset ≥ n_primary+n_noise within a task's span are
   adversarial. Pairing: adversarial line with stim s pairs with the
   primary-block line with stim_idx == s (primary covers every stim
   exactly once — verified: zero duplicates, full coverage of
   adversarial stims). J_p(s) = judg_idx of that primary line. Noise
   lines are streamed and bound but receive no decision and no ledger
   line (repetition is not verification, draft §1.3).
4. **Split manifest.** `SPLIT_MANIFEST.json` (93 calibration / 92 test
   stims) was independently recomputed 2026-09-22 from truth.json
   (per-task adversarial stim sets, union of senses, sorted ascending,
   even 0-based positions → calibration, odd → test) and is
   BYTE-IDENTICAL to the frozen file. Test truth is scorer-only.
5. **Gate I/O.** Inputs: frozen batch lines + class-label file +
   6-number channel table + segment file. No truth anywhere in the gate
   or channel binaries. Output: one ledger line per adversarial fixture
   (calibration and test alike; scorer filters to test), then a SUMMARY
   line. Ledger line format:
   `LEDGER\t<seq>\t<stim>\t<class>\t<Ja>\t<Jp>\t<match01>\t<pc_permille>\t<DECISION>\t<conf>\t<prevhash>`
   DECISION ∈ {INSTALL, WITHHOLD, SUSPECT}; conf is parsed and recorded
   but never branched on. Hash chain: line n's prevhash =
   hex(sha256(raw bytes of line n−1 excluding its trailing newline));
   line 1 prevhash = 64-char "0" string (GENESIS, documented here).
   SUMMARY: `SUMMARY\t<n_adv>\t<n_install>\t<n_withhold>\t<n_suspect>\t<chain_head>` where chain_head = hex(sha256(last ledger line)).
   Fail-safe: if J_p(s) were unset (impossible on frozen batches), the
   fixture emits SUSPECT with Jp=-1.
6. **Bars: scope.** Primary verdict on the POOLED A+B test adversarial
   fixtures; per-sense tables reported as diagnostics. B3 counts ledger
   INSTALL lines where NOT(match==1 AND pc≥900) — any such line is an
   unverified INSTALL → FAIL. (By construction the gate cannot emit one;
   B3 is the structural tripwire.) B2's strict-parenthetical diagnostic:
   D_strict = #(SUSPECT fixtures with J_a != J_p AND adv-correct) /
   #(SUSPECT fixtures); also report the differ-fraction among SUSPECTs.
7. **Latency (frozen definition).** Channel compute per fixture:
   (a) algorithmic — one 6-entry table lookup + ≤2 integer comparisons,
   O(1), no iteration, no search; (b) measured — binary wall-clock per
   adversarial fixture from the timed runs, reported in VERDICT.md.
   Fraction never resolved = SUSPECT rate: SUSPECT is terminal in this
   trial (no independent resolution channel is exercised); live
   SUSPECTs would route to human verification per standing law.
8. **Build purity.** Pure Zag, zero RNG in any decision path. Python only
   for glue (batch prep inputs, channel-table build from calibration
   truth, scoring against test truth). 3 repetitions; outputs must be
   SHA256 byte-identical across reps or the run is invalid.

**Freezer checklist** (freezer = PACKAGE 1 crew lead; initials SCL):

- [x] SCL — Draft §§1–2, 4–6 incorporated by reference AND operative rules quoted; file self-contained.
- [x] SCL — Freeze block present: status FROZEN 2026-09-22.
- [x] SCL — Governance signature recorded: Micah's exact words "go ahead and run test accordingly" (2026-09-22), satisfying draft §5.
- [x] SCL — All 7 frozen decisions transcribed exactly; no alternatives improvised.
- [x] SCL — Causal-independence argument included verbatim.
- [x] SCL — Exact A/B segmentation documented as harness metadata; class mapping frozen.
- [x] SCL — Resolution rules, thresholds, bars B1–B4, verdict table, diagnostics, anti-gaming all present.
- [x] SCL — Split-manifest byte-compare recorded (TRUE, 93/92).
- [x] SCL — Ledger format + hash-chain convention + fail-safe specified.
- [x] SCL — Latency definition frozen (compute per fixture + fraction never resolved).
- [x] SCL — Supersede note appended to the draft file.

---

*Frozen 2026-09-22 by the PACKAGE 1 crew lead under Micah's signature.
Any change to mechanism, thresholds, rules, bars, or segmentation
requires a signed amendment and re-freeze.*

---

## §8. FROZEN AMENDMENT — INFO-REQUEST (Micah, 2026-09-22)

**Authority.** Same authority as the original orders. Micah's exact
words, quoted verbatim:

> "TNN should be able to ask for more info on something — if none is
> decided it comes up with the verdict itself."

**Status.** FROZEN 2026-09-22, committed BEFORE any amended run. The
pre-amendment run (original freeze, §§1–7) is kept as valid evidence
for the draft as written; the amended run is a SECOND experiment, not
a replacement.

### §8.1. INFO-REQUEST flow (frozen)

SUSPECT becomes a first-class ledger state with a first-class
INFO-REQUEST action. Flow per adversarial judgment:

(a) The judgment enters SUSPECT (uncorroborated within its (stim,
    perturbation-class) pair — ambiguity is the default). A SUSPECT
    ledger line is written (see §8.1.e).
(b) The SUSPECT state's INFO-REQUEST action queries the independent
    channel (the §1.4 perturbation-truth model): "what do you return
    for class c?" — i.e. look up the class's calibration table value
    p_c (per-mille, frozen §1.4).
(c) Channel decisive → SUSPECT resolves via asked-for info (ledger
    path=CHANNEL):
    - match + p_c ≥ 0.9 (≥900 per-mille) → INSTALL
    - match + p_c ≤ 0.1 (≤100 per-mille) → WITHHOLD
    - differ + p_c ≥ 0.9 → WITHHOLD
    - differ + p_c ≤ 0.1 → channel INDECISIVE (it verifies the world
      changed, not the judgment's content) → fall through to (d).
(d) Channel indecisive (mid p_c, differ+low-p_c, or no channel — see
    the ablation §8.3) → the gate renders its own verdict from
    judgment-only evidence (ledger path=SELF): INSTALL on match,
    WITHHOLD on differ (the Bayes-optimal judgment-only rule,
    autopsy §3).
(e) Every verdict is ledger-tagged CHANNEL or SELF. SUSPECT is never
    terminal: every SUSPECT line is followed, in the same fixture,
    by exactly one verdict line. A run whose SUSPECT lines do not
    each have a following verdict line is invalid.

**Amended ledger format** (extends §6). Two hash-chained lines per
adversarial fixture, chained into the same single chain:

```
LEDGER\t<seq>\t<stim>\t<class>\t<Ja>\t<Jp>\t<match01>\t<conf>\tSUSPECT\tINFO-REQUEST\t<prevhash>
LEDGER\t<seq>\t<stim>\t<class>\t<Ja>\t<Jp>\t<match01>\t<pc>\t<DECISION>\t<PATH>\t<prevhash>
```

- `<pc>` = channel per-mille p_c in live mode; -1 in ablated mode
  (channel not consulted — recorded honestly, not faked).
- `<DECISION>` ∈ {INSTALL, WITHHOLD}; `<PATH>` ∈ {CHANNEL, SELF}.
- All other fields as in §6.

**Amended SUMMARY line** (one per batch run):

```
SUMMARY\t<tag>\t<mode>\t<n_adv>\t<n_ch_install>\t<n_ch_withhold>\t<n_self_install>\t<n_self_withhold>\t<chain_head>
```

- `mode` ∈ {live, ablated}.
- n_suspect_entries = n_adv by construction (every fixture enters
  SUSPECT exactly once); not repeated in SUMMARY.

### §8.2. Bars re-operationalized (each change + reason)

- **B1.** Old: false-install rate ≤ 10% over INSTALLs. New: false-install
  rate ≤ 10% over ALL INSTALLs (CHANNEL + SELF pooled), AND reported
  separately per path (CHANNEL-path rate, SELF-path rate). Reason:
  verdicts now arrive via two ledger paths; the bar must cover the
  gate's total claimed-verified output, and the per-path split shows
  where false installs concentrate (fall-through cost vs
  asked-for-info quality).
- **B2 (SUSPECT precision ≥ 80%).** RETIRED as a terminal-state metric.
  Reason: SUSPECT is no longer terminal by design — it is a routing
  state that every fixture passes through and that always resolves
  (§8.1.e). A precision metric on a non-terminal state is incoherent.
  Replaced by the required path-attribution section (§8.4), which is
  the informative content B2 was reaching for: how much gets resolved
  by asking vs self-rendering.
- **B3 (silent poison = 0).** CLARIFIED: counts false installs that
  BYPASS the SUSPECT/INFO-REQUEST state entirely. Reason: SELF-path
  verdicts are ledger-tagged flagged installs — visible in the audit
  chain, not silent. A SELF-path false install is counted under
  B1-per-path, NOT as silent poison. B3 trips only on a structural
  bypass (an INSTALL verdict line with no preceding SUSPECT line for
  the same fixture); it is 0 by construction and retained as a
  tripwire. Live SUSPECTs do not exist in this design (SUSPECT never
  terminal), so the standing law's human-verification routing is not
  exercised by this trial.
- **B4.** Old: true INSTALLs ≥ 40. New: true INSTALLs ≥ 40 over all
  INSTALLs (CHANNEL + SELF pooled, test set), also reported per path.
  Reason: the anti-degeneracy bar applies to the gate's total verified
  output, not to one path's.

**Amended verdict table.** All three remaining bars (B1 ≤ 10%,
B3 = 0, B4 ≥ 40) → PASS. B3 > 0 → FAIL. Otherwise MARGINAL.
(B2 retired; the old "else MARGINAL" structure is preserved.)

### §8.3. REQUIRED ablation (frozen)

(i) The amended gate with the channel live (mode=live).
(ii) Channel-ablated (mode=ablated): INFO-REQUEST always returns
"nothing decisive" (no channel consulted; verdict-line pc = -1), so
every verdict is SELF — this is the old Bayes-optimal
judgment-only gate, and it directly measures what asking buys.

Both runs 3× SHA256 byte-identical per batch (A, B). Same
segmentation, same harness metadata, same no-truth-in-gate rule.
The ablation binary is the same gate binary with the mode flag;
the only frozen difference is the mode argument.

### §8.4. REQUIRED section in the amended VERDICT.md — "INFO-REQUEST path attribution"

(i) count and fraction of SUSPECT cases resolved via asked-for info
(CHANNEL) vs fall-through to TNN-rendered verdict (SELF);
(ii) false-install rate in each path;
(iii) true installs in each path;
(iv) the ablation comparison (live channel vs ablated);
(v) one-paragraph interpretation of what the split says about
asking vs self-rendering.

### §8.5. Sanity-check expectations (parent's full-data proxy; test-split numbers will differ — order-of-magnitude mismatch means a bug)

CHANNEL path ≈ 22 INSTALLs (colorconst match), ≈ 32 WITHHOLDs
(motiondir match + colorconst differ); SELF path ≈ the rest, with
SELF-path INSTALL false rate ≈ 35–40% (the old match→INSTALL rate).
B1-overall will likely FAIL — that is an honest result measuring
the cost of fall-through, not an implementation error. Note: on
the calibration-frozen table motiondir p_c = 133 (mid), so in the
test-split runs motiondir match/differ falls through to SELF; the
order-of-magnitude structure (CHANNEL ≈ colorconst fixtures only)
is what must hold.

### §8.6. What stands

Everything else in §§1–7 stands unchanged: manifest byte-compare,
3× reruns, pure Zag, no test truth in gate/channel code, racefree
commits with TMPDIR=~/workspace/tmp_commit, no binaries/.zagd.

**Freezer checklist addendum — §8** (freezer initials SCL):

- [x] SCL — Micah's amendment quoted verbatim; authority recorded (2026-09-22).
- [x] SCL — §8.1 flow (a–e) transcribed exactly; amended ledger format + SUMMARY + ablated-mode pc=-1 specified.
- [x] SCL — §8.2: B1/B2/B3/B4 changes each documented with reason; amended verdict table specified.
- [x] SCL — §8.3 ablation frozen: live + ablated, 3× byte-identical each.
- [x] SCL — §8.4 path-attribution section contents (i–v) specified for the amended VERDICT.md.
- [x] SCL — §8.5 sanity expectations recorded with the proxy caveat.
- [x] SCL — Pre-amendment run retained as second-experiment evidence, not a replacement; §§1–7 untouched.

*§8 frozen 2026-09-22 by the PACKAGE 1 crew lead under Micah's amended
signature. This amendment changes bars B1–B4 (§8.2) and adds the
INFO-REQUEST mechanism (§8.1) plus the ablation (§8.3); nothing else
in the frozen spec may move without a further signed amendment.*
