# KB4 channel investigation — 2nd-opinion brief

You are an INDEPENDENT INVESTIGATOR, not an implementer. Your job is analysis.
Work in `~/workspace/tnn-lab/kb/autopsy/channels2/`. Zero RNG in any executable
part. Read the evidence below (authoritative; do not re-litigate the numbers).

## Background (measured, frozen evidence)

The system (TNN, a deterministic AI; all reasoning/verifying in Zag, a native
compiled language; Python glue only) faces adversarial judgments about sensory
percept-like stimuli (classes: colordisc, colorconst, shapetrans, pitchdisc,
timbredisc, motiondir). An adversary can fool the primary judgment; the
SUSPECT gate was built to ask for more information (INFO-REQUEST) before
rendering a verdict (INSTALL = trust the judgment / WITHHOLD = don't install).

**SUSPECT-gate trial (amended):** B1 false-install 41.3% vs ≤10% bar (FAIL);
B3 silent poison 0 (PASS); B4 true installs 54 ≥ 40 (PASS). Verdict MARGINAL.
Only 20/184 fixtures resolved via the channel (all colorconst, the one class
whose calibration p crosses threshold); 164/184 fell through to TNN's own
verdict at 45.5% false-install. Ablation: channel-ablated verdicts are
IDENTICAL fixture-by-fixture to live — asking bought attestation, not better
decisions.

**Channel shootout (TEST n=184, prior entropy ≈0.9958 bits):**
- (a) causal perturbation model: 0.0695 bits, res-acc 0.656, false-install 0.280
- (b) cross-time (noise proxy): 0.0110 bits, 0.560, 0.398
- (c) multi-source agreement: 0.0797 bits, 0.668, 0.339
- (d1) confidence (neg control): 0.0003 bits, 0.484 — anti-informative
- (d2) confidence delta (neg control): 0.0123 bits, 0.549
- (a)+(c): 0.1483 bits, 0.811, **0.151 false-install — champion on bits, NOT deployable**
- (a)+(b): 0.0637 bits, 0.653, 0.347

Both original crews independently concluded: the judgment stream plus
perturbation-class metadata caps out around 0.15 bits of the ~1 bit needed;
the repair is "a channel the adversary cannot correlate: human verification
on a calibration set, a different physical sensor basis, or an analytic check
on the stimulus itself."

Standing rules: zero randomness in AI decision paths; determinism (byte-identical
reruns) required; all executable reasoning in Zag; every claim needs frozen
evidence; Micah's law — TNN must NEVER be a yes-man (no sycophancy).

## Your three required deliverables

(a) **Steelman the failure.** In information-theoretic terms, WHY is every
tested channel information-poor? What information is actually missing — not
just "more bits needed." Steelman the adversary: what property of the
adversarial construction makes the judgment stream so exhaustible?

(b) **Propose 2-3 concrete candidate GENUINELY INDEPENDENT channels** — ones
the adversary cannot correlate. For each: sketch how it would be built and
tested in pure Zag on this corpus (93 calibration / 92 test adversarial
fixtures; stimuli are percept-like with class/variant metadata but NO raw
stimulus signal in the current corpus — say honestly if a candidate needs new
data, and what that data is). Keep it concrete: what table/file would be
frozen, what the Zag instrument reads, what verdict it emits.

(c) **For each candidate, name what would FALSIFY it** — the measurement or
outcome that kills it, stated crisply enough to preregister.

Write your full verbatim to `~/workspace/tnn-lab/kb/autopsy/channels2/<your-name>_verbatim.md`
(e.g. `native_verbatim.md`). Then report back a concise summary.
