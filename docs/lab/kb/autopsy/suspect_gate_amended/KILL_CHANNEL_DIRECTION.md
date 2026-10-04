# KB4 SUSPECT-gate — FORMAL CLOSURE: the independent-channel direction is KILLED

Issued 2026-09-27 by the fix-or-kill executor (decoration-audit P1 #3,
research-or-kill). The research phase is complete; this is the kill.

## 1. What is killed

The direction **"an independent information channel that improves
TNN's install/withhold decisions"** — i.e., every remaining proposal to
tune the SUSPECT-gate rule, the INFO-REQUEST thresholds, or the channel
calibration to make asking change decisions. No more tuning. The
amended trial's own honest conclusion already said it: "The next repair
is not a better gate rule."

## 2. The evidence (all from `VERDICT_AMENDED.md`, amended run, frozen)

- **Zero-decision ablation, proved twice.** Live (channel consulted) vs
  ablated (INFO-REQUEST always "nothing decisive", every verdict SELF):
  verdict sets identical **184/184 in A and 185/185 in B** (3× SHA-256
  byte-identical reps each). Exactly 20 lines differ, all in the PATH
  tag only (colorconst fixtures re-labeled SELF→CHANNEL). **Zero differ
  in DECISION.** A channel that agrees with the Bayes judgment-only rule
  everywhere is indistinguishable from no channel at all.
- **B1 false-install rate 38/92 = 41.3%** against a ≤10% bar — FAIL.
- **89.1% of fixtures fall through to SELF**; the SELF path
  false-installs at **45.5%**.
- **Follow-up shootout killed the remaining candidates**: C2 = 0.0000
  bits, C3 = 0.0049 bits of information — nothing there.
- The channel's only decisive cases (colorconst match→INSTALL,
  colorconst differ→WITHHOLD) coincide with the Bayes-optimal
  judgment-only action; no class has p_c ≤ 0.1, so the
  match+low-p_c→WITHHOLD override never fires.

## 3. What is NOT killed (genuine findings, preserved as findings)

These stand as experimental results. They are **not** live machinery
and must not be presented as such:

- SUSPECT-with-INFO-REQUEST **structurally eliminates silent poison**:
  B3 bypass installs = 0 (PASS); every ambiguity is auditable on a
  hash-chained ledger.
- **Non-terminal SUSPECT works as designed**: never-resolved fraction 0;
  every SUSPECT line is followed by exactly one verdict line.
- **differ→WITHHOLD does real work**: 45/99 withheld-true (45.5%),
  especially timbredisc (20 true withholds of 30).
- **Attestation, not decision**: the 20 CHANNEL-tagged fixtures
  false-install at 20.0% vs 45.5% for SELF. The channel is a **witness,
  not a decider** — a ledger tag saying an independent model of
  perturbation-truth agrees the class is trustworthy. That is a real,
  measured property of the tagged subset; it just never changed a
  verdict.
- The amended-run package itself (frozen prereg + amendment §8, 12
  byte-identical run outputs, independent verifier PASS on all 12)
  remains valid experimental evidence.

## 4. The "third option" question

An approach-skeptic review was requested from z.ai (GLM-5.3) before
closure, asking whether a real third option exists beyond (a) new
independent research vs (b) kill, and whether the identical-ablation
logic has any flaw. No answer had arrived at closure time; if one
arrives with a concrete flaw or contradictory source, this document
will be amended.

The verdict's own honest conclusion already names the only live
alternative: **"a channel with genuinely more information — one that
can say WITHHOLD on a match (low-p_c class) or INSTALL on evidence the
judgment alone cannot see"** (calibration over primary-correctness /
self-correction signals). That is not a rescue of this gate — it is a
*different experiment* (option (a), new independent research), and it
requires its own frozen prereg. Nothing in this closure blocks it;
nothing in this closure funds it.

## 5. Revival bar

This direction re-opens only on: (i) a genuinely disagreeing source —
a channel demonstrated to change install/withhold decisions against the
judgment-only baseline on a frozen test set; **and** (ii) a new frozen
prereg with preregistered bars, committed before any run. Tuning the
existing gate rule, thresholds, or calibration table does not qualify.
