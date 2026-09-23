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
