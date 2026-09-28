# DEEP-DIVE METHOD — behavioral diagnostics by default (PAMs v2, Team 7)

**Standing law (Micah, 2026-09-23):** TNN is a deep diver by default for
behavior. Behavioral issues get white-box deep dives — instrumented internals,
knowledge-vs-machinery evidence — never surface patches.

This document makes that law operational: a mandatory protocol, the probe
machinery that automates it, and the rules that make it the DEFAULT path.

## 1. The mandatory protocol

No behavioral failure is closed, patched, or re-scoped without all five
steps. Each step produces a frozen artifact; the next step may not begin
until the previous artifact exists and is digest-pinned.

**(a) Reproduce + freeze the failure.** Recompute the headline metric from
the frozen evidence inside the diagnostic instrument (not by hand, not by
re-reading the verdict). Assert exact equality with the reported numbers.
SHA256-freeze the raw input bytes; record the digest. If the metric does not
reproduce exactly, stop — the failure record is corrupt, not the system.

**(b) Instrument white-box internals.** Capture the decision-time state the
system actually consumed: ledger/audit traces, gate dispositions with reasons,
confidence paths, deliberation records. Rule: the instrument reads what the
mechanism read — post-deliberation inputs, not pre-deliberation fields
(R2-4 lesson: `prog` vs `final_prog` differ on the trials that matter; the
hand analysis used the wrong one, the harness caught it).

**(c) Run the probe split.**
- **KNOWLEDGE probes** (on the frozen record): could the system state the
  relevant knowledge? K1 — knowledge presence at the program layer
  (byte-substring-probe style: the knowledge signal must be found IN the
  record bytes, e.g. `progF==PASS` alongside `judgment==truth`). K2 —
  knowledge delivery: did the knowledge reach the decision point (the
  gate's actual input)? K3 — partition every failure into mechanism
  buckets with zero residue. K4 — adjudication gap: was the knowledge
  present in the white-box input but unread by any rule?
- **MACHINERY probes** (synthetic, knowledge held fixed): does the mechanism
  execute correctly when the knowledge is fixed? M1 — control: clean
  synthetic inputs must produce the designed output at 100%. M2 — the
  suspect rule, triggered deliberately on synthetics, must fire exactly as
  documented. M3 — replay: re-implement the documented rule over the frozen
  record; any disposition mismatch is a machinery deviation until proven
  otherwise. All synthetic inputs are closed-form in the trial index; zero
  RNG anywhere.

**(d) Knowledge-vs-machinery verdict with evidence.** Apply the frozen
taxonomy (§3). The verdict names a repair class, never just a label. Every
number carries an evidence pointer (input digest, ledger digest, report
digest). Bucket-level repair mapping is mandatory — a bare label
("KNOWLEDGE") without the bucket table is not a verdict.

**(e) Never ship a surface patch without (a)–(d).** A surface patch is any
change that improves the headline metric without passing through the
verdict's repair class. The instrument BLOCKS it mechanically: the verdict
emits `surface_patch=BLOCKED` with the counterexample that disqualifies the
naive fix (R2-4: cf2 — install-more without adjudication installs false
permanents).

## 2. Verdict taxonomy (frozen)

- **MACHINERY-BUG** — the mechanism does not execute its own design
  (replay mismatches, synthetic control failures). Repair: CODE-REPAIR.
- **KNOWLEDGE** — the white-box state contained, or could have contained,
  the information needed, but the system lacked the rule or the program
  knowledge to act on it. Repair: RULE-ADDITION (deliberate audited
  revision) or PROGRAM-TEACHING. Note the load-bearing subtlety the R2-4
  case proved: a *missing rule* is a knowledge gap, not a machinery
  ceiling — the gate had every input needed to write the correct rule; the
  rule was absent.
- **MACHINERY-BY-DESIGN** — the mechanism executes the design exactly and
  the design fully accounts for the failure. Repair: none at this layer.
- **SPEC-TENSION** (orthogonal flag) — the best achievable outcome under
  any mechanism change is arithmetically below the bar (gate-side ceiling
  < bar, proven from the frozen record). Repair: SPEC-CHANGE. Never a code
  patch, never a bar moved by hand — amendments go to Micah.
- **INCONCLUSIVE** — the deliverable is the gap list, honestly.

## 3. The instrument: diagnose.zag

The protocol's steps (a)–(d) are automated by the pure-Zag diagnostic
harness (`diagnose.zag`, frozen by `PREREG_DIAG.md` 2026-09-23):
`diagnose <case_record> <expect> <report_out>`. Case-agnostic; case
specificity comes from the input files, never from harness edits. It keeps
its own append-only 16-word audit ledger
(op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60),
SHA256-chained. Zero RNG; byte-identical reruns (3-run digest check is a
kill bar). Python glue (`gen_case_record.py`) derives inputs from frozen
evidence — glue is never the instrument.

Worked self-application: `DIAG_VERDICT_R24_RK3.md` + `DIAG_REPORT_R24_RK3.txt`
(R2-4/RK-3: verdict KNOWLEDGE + SPEC-TENSION, 0/11,840 replay mismatches,
surface patch BLOCKED).

## 4. The DEFAULT diagnostic path

This section specifies how deep-diving becomes what happens *without being
asked* — the default, not the exception.

**What triggers it.** Any of these opens a deep-dive case automatically:
1. A frozen bar fails (any fork, any round) — the verdict may not be written
   until the harness has run on the failure.
2. A metric moves unexpectedly between runs (determinism break, regression).
3. A human (Micah, a crew lead, the coordinator) reports "it behaves wrong"
   — the report becomes a case record, not a patch ticket.
4. A red-team or audit flags a cheat signature, bar-gaming, or
   claimed-without-evidence number.

**What it overrides.**
- *The "just fix it" reflex.* No code change lands on a behavioral failure
  without a verdict whose repair class names that change. "Obvious" fixes
  are the most suspect: obviousness is usually a surface patch wearing
  confidence.
- *Hand analysis as evidence.* Spreadsheets, eyeballed counts, and
  "I read the file" are triage, not diagnosis. Numbers that decide a
  verdict must be recomputed inside the instrument (the 2366/2372 lesson).
- *Verdict-first reasoning.* The failure does not get a story until the
  probes run. The R2-4 verdict's story ("the gate working as designed")
  was 62% of the truth; the instrument found the other 38% (knowledge
  delivery gap, suppression bucket, deliberation downgrades).
- *Silence windows don't apply to instrumentation.* A deep dive may run
  during a hold; only its conclusions wait for the window to lift.

**What "surface patch" attempts it blocks.** The harness verdict carries a
machine-readable `surface_patch=` field. BLOCKED is emitted when the
failure's bucket table contains a KNOWLEDGE bucket whose naive repair has
a disqualifying counterexample on the frozen evidence. Blocked attempts
include: threshold tuning to move the headline metric, installing more /
withholding less without the missing adjudication rule, rewording the bar,
and any change whose justification is "it makes the number go up" rather
than the verdict's repair class. Unblocking requires either a new probe
battery that dissolves the counterexample or Micah's explicit amendment.

**Where it lives in TNN's machinery.** The diagnostic harness plugs into the
existing audit-ledger conventions (16-word entries, §3): every deep-dive
case appends its own DIAG_* opcodes (101–108) to a case ledger, so
diagnostics are themselves audited, replayable state — TNN's deliberation
layer can invoke `diagnose` on any failure record as a native diagnostic
step, with the verdict's repair class routing to the revision machinery
(rule-addition), the teaching path (program-teaching), or governance
(spec-change). The instrument is deliberation's white-box eyes, not a
separate tool.

## 5. Red-team rule

Every deep-dive conclusion gets an adversarial review before the case
closes. The reviewer is not the builder; the review is recorded in the
verdict doc with dispositions (sustained / answered / partially sustained
with action). The harness ships RT1–RT4 prompts in every report; the human
reviewer must add at least one original attack. A verdict without a
red-team section is not finished.

## 6. Anti-patterns (what a deep dive is not)

- A longer verdict document with the same hand-counted numbers.
- A fix with a post-hoc "diagnosis" section.
- Blaming the bar before the ceiling is proven arithmetically.
- "The mechanism is correct" without a replay (M3) — correctness is
  demonstrated, not asserted.
- Closing on INCONCLUSIVE without the gap list — the gaps are the
  deliverable then.
