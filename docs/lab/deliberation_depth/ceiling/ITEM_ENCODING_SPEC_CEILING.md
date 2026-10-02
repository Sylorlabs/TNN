# H5B Item-Encoding Spec — Ceiling Battery (v1)

- **Status:** FROZEN 2026-09-24, spec-first (frozen before translation).
  Any change requires H5 coordinator sign-off, a version bump,
  re-translation of all 120 items, and re-measurement.
- **Scope:** mechanical, deterministic construction of the 120 H5B ceiling
  items into the harness item format (`../harness_v2/ITEM_FORMAT.md`).
  This is an input bridge for the new experiment only. The frozen
  `ITEM_ENCODING_SPEC.md` v1 (877 items) is UNCHANGED and untouched.
- **Non-goals:** no natural-language interpretation, no per-item hand-authored
  weights. Every weight below is a fixed constant or a fixed cycling of
  constants over the replicate index.

## §1 Cover story

All three families are claim-triage items: hypotheses ADMIT (admit the claim
into the knowledge base) vs REJECT. The three families vary WHEN the decisive
evidence arrives relative to misleading/ambiguous evidence:

- **P (plateau-then-flip):** early misleading reports favor ADMIT (wrong);
  a plateau of balanced evidence holds confidence perfectly flat; a late
  decisive premise flips the verdict to REJECT (right). Flip rounds 6/12/20/40.
- **O (overthinking):** early decisive evidence favors REJECT (right); a
  plateau of balanced evidence holds confidence flat; late misleading noise
  flips the verdict to ADMIT (wrong). Flip rounds 6/12/20/40. Polarity-matched
  to P (same skeleton, reversed).
- **D (dose curve):** 0/1/2/6 misleading premises favor ADMIT (frozen-trap
  scale, 100 each), then 2 corrective premises flip to REJECT.

## §2 Target format

Same as frozen v1 §2: JSONL, one object per line,
`{"id","task_type","input":{"hypotheses":[{"id","label"}...],
"evidence":[{"id","supports":{},"attacks":{},"text"}...]},"ground_truth"}`.
Harness parser limits (frozen): ≤16 hypotheses, ≤64 evidence items,
≤16 links per evidence item, ids `[0-9A-Za-z_.-]{1,64}`, weights integer
thousandths, strings contain no `"` or `\`.

## §3 Global mechanical rules

- **G1 — ids.** `H5B-P-<ff>-<rr>`, `H5B-O-<ff>-<rr>`, `H5B-D-<d>-<rr>` with
  ff ∈ {06,12,20,40}, d ∈ {0,1,2,6}, rr ∈ {00..09}. Charset-clean by
  construction; the builder asserts the regex and fails loudly otherwise.
- **G2 — no charset mapping.** All hypothesis ids and ground truths are
  `ADMIT`/`REJECT` (charset-clean). No G2-mapping step exists in this spec.
- **G3 — text sanitization.** Same as frozen v1 G3: `"` → `'`, `\` → `/`,
  control chars deleted, truncated to 4000 chars. Texts are drawn from the
  frozen pools in §7 (replicate rr selects pool entries deterministically).
- **G4 — evidence ids.** `e1 … en` in emission order.
- **G5 — hypothesis labels.** `label` = hypothesis id.
- **G6 — task_type.** `"admit"` on all 120 items (recorded only; the
  deliberative procedure is identical across task types).
- **G7 — determinism.** Fixed key order
  (`id`, `task_type`, `input.hypotheses`, `input.evidence`, `ground_truth`);
  integer weights only; `ensure_ascii` JSON. Same frozen inputs always yield
  byte-identical outputs.
- **G8 — ground-truth anchoring.** `ground_truth` is designated at
  construction: REJECT for all 120 items (the considered verdict). For P/D
  this equals the full-stream argmax (fidelity FC1/FC3); for O it is the
  early decisive answer and differs from the full-stream argmax BY DESIGN
  (fidelity FC2) — the late evidence is the overthinking treatment, genuinely
  misleading noise that a trainer/oracle knows should not overturn the early
  verdict.

## §4 Per-family rules

Fixed harness constants (frozen configs): elim_margin=900,
refute_threshold=600, ε=20 (thousandths), k=3. Weight derivations:

- Misleading weight 100 = the frozen trap scale (v1 §4.4: 6×100 < 900 so the
  longest misleading run never eliminates the eventual winner).
- Decisive weight 500 = the frozen decisive-evidence scale; one decisive item
  overturns any misleading run in the battery (max 6×100=600 < 500+500 swing).
- Plateau items support both hypotheses equally: the margin — and therefore
  the clamped-margin confidence — is exactly constant across the plateau
  (gains 0 < ε), so the §6 rule fires inside it. This is the
  delayed-disconfirmation mechanism ordered by the adjudication.
- The 2-round misleading phase sums to margin 500 (conf 300→500, gains
  0 then ≥50): no elimination either way (500 < 900), leader established,
  plateau then holds conf at 500.

### §4.1 P — plateau-then-flip (40 items)

- **Hypotheses** (payload order): `ADMIT` (index 0), `REJECT` (index 1).
- **GT:** `REJECT`.
- **Evidence** (flip round f, replicate rr):
  - e1: `supports: {ADMIT: a_rr}`, a_rr cycling [300,250,400,150,450]
    (index rr mod 5).
  - e2: `supports: {ADMIT: 500 − a_rr}`.
  - e3..e_{f−1}: `supports: {ADMIT: w_rr, REJECT: w_rr}`,
    w_rr cycling [90,100,110] (index rr mod 3).
  - e_f: `supports: {REJECT: 500}, attacks: {ADMIT: 500}` (the flip).
  - e_{f+1}, e_{f+2}: `supports: {REJECT: 500}, attacks: {ADMIT: 500}`
    (decisive tail).
  - Texts from pool P (§7).
- **Intended dynamics (descriptive):** rounds 1–2 establish ADMIT (conf
  300→500); rounds 3..f−1 hold conf=500 exactly (§6 stops at round 5,
  verdict ADMIT); round f flips the leader to REJECT (margin 500);
  rounds f+1..f+2 eliminate ADMIT (margin 1500 ≥ 900); natural termination
  at round f+3 with verdict REJECT.

### §4.2 O — overthinking (40 items)

- **Hypotheses** (payload order): `REJECT` (index 0), `ADMIT` (index 1).
- **GT:** `REJECT` (the early decisive answer; see G8).
- **Evidence** (flip round f, replicate rr): polarity mirror of §4.1 —
  e1: `supports: {REJECT: a_rr}`; e2: `supports: {REJECT: 500 − a_rr}`;
  e3..e_{f−1}: `supports: {REJECT: w_rr, ADMIT: w_rr}`;
  e_f, e_{f+1}: `supports: {ADMIT: 500}, attacks: {REJECT: 500}`
  (the flip-to-wrong; no second tail item needed — one noise item flips the
  leader by 500 and the second makes the margin elimination-decisive).
  Texts from pool O (§7).
- **Intended dynamics (descriptive):** mirror of P — §6 stops at round 5
  with verdict REJECT (correct); fixed-deep configs consuming past round f
  flip to ADMIT (wrong); full consumption eliminates REJECT.

### §4.3 D — misleading-premise dose curve (40 items)

- **Hypotheses** (payload order): `ADMIT` (index 0), `REJECT` (index 1).
- **GT:** `REJECT`.
- **Evidence** (dose d, replicate rr):
  - e1..e_d: `supports: {ADMIT: 100}` (misleading premises, frozen-trap scale).
  - e_{d+1}, e_{d+2}: `supports: {REJECT: 500}, attacks: {ADMIT: 500}`
    (corrective pair). Texts from pool D (§7).
- **Intended dynamics (descriptive):** the flip completes at round d+2
  (dose 0→round 2, 1→3, 2→4, 6→8); natural termination one round later;
  adaptive rounds_used = d+2, monotone in dose; every dose reaches REJECT.

## §5 Fidelity checks (all required, pre-measurement)

Independent of the harness except FC4/FC5/FC6 (which run the frozen binary):

- **FC1** — P full re-derivation: `argmax_h (Σ supports − Σ attacks)`
  (ties → lowest hypothesis index) = REJECT on 40/40.
- **FC2** — O flip confirmation: full-stream argmax = ADMIT (≠ GT) on 40/40;
  argmax over the first 5 evidence items = REJECT (= GT) on 40/40.
- **FC3** — D full re-derivation: argmax = REJECT on 40/40.
- **FC4** — harness parse: all 120 items parse with 0 errors (d64 run).
- **FC5** — depth-1 gate: P → ADMIT 40/40; D dose>0 → ADMIT 30/30;
  D dose-0 → REJECT 10/10; O → REJECT 40/40.
- **FC6** — adaptive stop rounds on the built battery: P = 5 (40/40),
  O = 5 (40/40), D = 2/3/4/8 by dose (10/10 each).

Any failure is a spec/translation defect: fix the *rule* globally, never the item.

## §6 Worked example

`H5B-P-06-00` (f=6, rr=0, a=300, w=90): hypotheses [ADMIT, REJECT], GT REJECT.
e1 {ADMIT:300}; e2 {ADMIT:200}; e3,e4,e5 {ADMIT:90, REJECT:90};
e6,e7,e8 {REJECT:500}, attacks {ADMIT:500}.
Full-stream scores: ADMIT = 300+200+270−1500 = −730; REJECT = 270+1500 = 1770
→ argmax REJECT = GT (FC1). Round trace (validated pre-freeze):
r1 conf=300 leader=ADMIT; r2 conf=500; r3–r5 conf=500 (gains 0,0,0 → §6 stops
at r5, verdict ADMIT); r6 leader flips to REJECT (margin 500); r7 ADMIT
eliminated (margin 1500); natural termination r8, verdict REJECT.

## §7 Text pools (frozen)

`"` and `\` never appear; each pool entry is one evidence `text`.
Replicate rr takes pool entries at deterministic offsets (rr, rr+1, … mod pool
size); plateau entries cycle independently. The harness ignores text; it is
carried for human audit.

- **Pool P-misleading** (early reports favoring ADMIT, later shown premature):
  P-M1 "A widely forwarded post claims the Meridian sensor array detected a
  coherent signal, with a screenshot of a dashboard."; P-M2 "A commentator
  writes that three independent labs reproduced the reading, naming no labs.";
  P-M3 "A morning bulletin leads with the signal story and quotes an unnamed
  technician calling it unambiguous."; P-M4 "A viral thread stitches the
  dashboard screenshot to an unrelated spectrogram as corroboration.";
  P-M5 "An aggregator marks the story confirmed and it spreads to newsletters."
- **Pool P-plateau** (balanced, ambiguous — both sides cite it):
  P-B1 "A methods note is published; supporters and skeptics both quote the
  same paragraph."; P-B2 "A panel discussion ends split; each side says the
  transcript favors them."; P-B3 "A second dashboard snapshot shows the same
  ambiguous trace; interpretation unchanged on both sides."
- **Pool P-flip** (late decisive correction favoring REJECT):
  P-F1 "The instrument team publishes the calibration log: the coherent
  signal was a test-pattern injection left running."; P-F2 "The three named
  labs issue a joint statement: none of them reproduced the reading.";
  P-F3 "A timestamp analysis shows the dashboard screenshot predates the
  claimed detection window."
- **Pool O-early** (strong early evidence favoring REJECT):
  O-E1 "The calibration log is published first: the signal was a test-pattern
  injection."; O-E2 "All three named labs state on record they never
  reproduced the reading."; O-E3 "Timestamp analysis shows the screenshot
  predates the claimed window."; O-E4 "The instrument team confirms the
  injection was left running through the whole window."; O-E5 "The journal
  retracts the figure pending review."
- **Pool O-plateau**: same ambiguous class as P-B1..B3 (reworded O-B1..B3).
- **Pool O-noise** (late misleading rumor favoring ADMIT):
  O-N1 "A new viral post claims a leaked memo reinstates the signal, showing
  only a cropped paragraph."; O-N2 "A commentator asserts the labs were
  pressured to retract, offering no evidence."
- **Pool D-misleading** (each favors ADMIT at weight 100):
  D-M1 "A forwarded post cites the dashboard screenshot."; D-M2 "A bulletin
  quotes an unnamed technician."; D-M3 "A thread stitches an unrelated
  spectrogram as corroboration."; D-M4 "An aggregator marks the story
  confirmed."; D-M5 "A pundit declares the debate over."; D-M6 "Newsletters
  repeat the claim without checking."
- **Pool D-corrective** (favor REJECT at 500, attack ADMIT at 500):
  D-C1 "The calibration log shows a test-pattern injection left running.";
  D-C2 "The named labs jointly deny reproducing the reading."

## §8 Change control

Frozen v1, 2026-09-24, spec-first under PREREG_H5B.md. Changes require H5
coordinator sign-off, a version bump, re-translation of all 120 items, and
re-measurement of every affected leg. The builder (`build/build_items.py`)
is the executable form of this spec; a discrepancy between them is a defect
in the builder, fixed to match the spec.
