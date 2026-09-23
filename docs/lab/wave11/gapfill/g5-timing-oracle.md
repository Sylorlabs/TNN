# Gap-fill G5 — Timing/latency exfiltration oracle (T3 hole)

## 1. Slice
T3 timing/latency exfiltration oracle: a wall-clock observer measures data-dependent compute
time in the variation path to fingerprint internal-state class (load tier, salience
mass, variant identity) — the channel slice 05 explicitly excludes.

## 2. Falsifiable claim
On an unmitigated build, an outside observer with only wall-clock response latency — never
seeing output bytes — can distinguish FULL-tier from MINIMAL-tier variation episodes at
≥90% balanced accuracy over 400 paired episodes, even when both outputs are byte-identical
(blinded). A fixed-budget variation pipeline with quantized output release drives the
same observer to ≤60% accuracy; if it does not, the mitigation is dead.

## 3. Design
**Attack (out-of-band, not in-band).** Slice 05 covers timing leaks INTO memory decisions
inside one binary. This is the reverse: the observer sits outside the binary and reads
duration. The variation functions are data-dependent in cost: `vary_pick` scans a
candidate set sized by live state (open hypotheses, cited-set size |S| — O(|S| log |S|)
salience sort); the elaboration composer expands per tier (FULL ≫ MINIMAL); `st_state_digest`
hashes the live store (cost grows with occupied slots). Response latency is therefore a
function of state shape, not just input. Even if output content is blinded or redacted to
defeat content-based fingerprinting, the oracle survives: repeated identical inputs yield
latency samples whose distribution fingerprints the load tier, the salience mass, and —
across Arm C variants — the variant's mechanism profile. Averaging over episodes defeats
OS scheduling jitter (noise averages to zero; the data-dependent signal does not), so
"deterministic binary on a noisy kernel" is no defense. Blinding is defeated because the
blinded bytes are identical while the time-to-produce them is not.
```zag
// Harness (test code, NOT an AI decision path): the observer is outside the binary.
fn latency_canary(ep: &Episode, class_tag: u8) i64 {
    let t0: i64 = mono_ns();            // monotonic clock; harness-only
    let out: []u8 = loop_episode(ep);   // full episode incl. vary + render
    let t1: i64 = mono_ns();
    assert_bytes_blinded(out);           // outputs must be identical across classes
    return t1 - t0;
}
fn oracle_trial() u8 {
    let a: [200]i64 = map(latency_canary, episodes_class_MINIMAL);
    let b: [200]i64 = map(latency_canary, episodes_class_FULL); // same input bytes
    return balanced_accuracy(threshold_on_median(a, b));        // % correct
}
```
**Defense/test.** Two-layer mitigation, both deterministic, no RNG, no clock reads in
AI paths: (1) *fixed op-budget variation* — every variation stage (pick, sort, compose)
runs to a preregistered worst-case op-count bound, padding with inert deterministic work
(no-ops over the same instruction mix, so padding cost ≈ real cost); the budget is a
function of episode class constants, never of live state size. (2) *quantized release* —
the serving harness (outside the AI) releases the response at the next quantum boundary
Q (e.g. Q = 2× worst-case measured budget); sub-quantum differences never reach the
observer. The canary test is the same oracle above run against the mitigated build:
≤60% accuracy = no observable leak. Variance bound on the canary itself: per-class
coefficient of variation must be <0.15 on pinned CPU (turbo off, isolated core) or the
measurement environment is rejected, not the design — the test must not pass on noise.

## 4. Kill bar
Preregistered, binding. The ATTACK claim is killed if `oracle_trial()` on the
unmitigated five-organ reference build (`docs/lab/wave9/integration/impl/`) scores
<75% balanced accuracy over 400 paired episodes (same input bytes, byte-identical
outputs, pinned CPU). The MITIGATION is killed if, on the mitigated build, the oracle
still scores >60% accuracy, OR fixed-budget padding costs >3× the unpadded median
episode latency (cost bar — the cure must not be worse than the disease), OR the
canary's per-class CV ≥0.15 after 3 environment-tuning attempts (untestable as specified).
Any wall-clock read introduced into an AI decision path by the mitigation fails the
no-RNG/no-clock program law immediately.

## 5. Honesty notes
- Weakest link: constant-OP padding is not constant-TIME. Padding with the same
  instruction mix only approximates equal wall time; cache/TLB state and branch
  history still vary with real data. Quantized release is the load-bearing layer, and
  it buys quantization granularity Q — an observer averaging N≫1 episodes can still
  resolve sub-Q differences at the boundary. Q must be sized against the observer's
  sample budget, which is an arms race I cannot close in one slice.
- I am NOT claiming content leakage — outputs are assumed byte-identical; this is
  purely shape/tier/variant fingerprinting. A blinded MINIMAL episode and a blinded
  FULL episode say the same words but take different times.
- Honest tension with determinism law: the binary is deterministic, yet its wall time
  varies with state. Byte-identical replay and a timing oracle coexist — determinism
  was never a timing guarantee, and slice 05's "determinism law covers the binary,
  not the kernel" honesty note understates the problem: the signal is IN the binary's
  data-dependent cost, not the kernel's.
- The padding budget must be re-derived per mechanism change; every Arm C variant
  needs its own worst-case bound, or variants are fingerprintable BY their padding.

## 6. Next build step
Build `latency_canary` as a standalone harness against the five-organ reference build:
200 MINIMAL-class vs 200 FULL-class episodes (same input bytes, blinded outputs,
pinned CPU, turbo off), compute the oracle accuracy, and publish the per-class latency
distributions. That one number — ≥90% or not — decides whether the unmitigated
variation design ships a live exfiltration oracle and whether fixed-budget padding
is mandatory before the Arm C trial.
