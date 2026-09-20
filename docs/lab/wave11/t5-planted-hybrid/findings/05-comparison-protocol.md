# Slice 05 — Three-way comparison protocol: planted-only vs learned-only vs hybrid

## 1. Slice
Track 5, slice 05: the preregistered comparison PROTOCOL that decides, under the no-free-lunch
standing rule, whether planted-only (P), learned-only (L), or hybrid (H) knowledge acquisition
wins — or whether there is no champion and the answer is scenario-dependent. This slice specifies
domains, episode structure, metrics, blinding, statistics, and the exact decision rule.

## 2. Falsifiable claim
The claim this protocol kills if the data warrant it: **"The hybrid arm dominates both pure arms
on the primary composite (mastery, episodes-to-mastery, retention, revision correctness) at
Holm-adjusted p < 0.05."** Falsified if H fails either pairwise comparison in §6 — in which case
the protocol FORCES the "no champion — scenario-dependent" verdict and the fit table in §6,
not a rescue narrative for H.

## 3. Design

**3a. Arms.** P: all in-domain content trainer-implanted at episode 0 as audited implants
(strength-trial designation pattern; implants deliberately erasable, NOT force-pinned, so the
revision test is fair). L: store starts empty in-domain (CORE/constitution exempt); everything
acquired via scaffold-and-release with learner-initiated SIGNAL_DISCONNECT (law 7); a claim
counts as learned only if it persists post-disconnect. H: planted seed core (~20% of the fact
corpus, prereg-fixed) + learned remainder; every memory carries a provenance tag (planted/
learned) in the ledger (wave9 trust-tier machinery).

**3b. Test domains (identical across arms).** D1 factual corpus: 60 prereg-hashed facts with
authoritative world records — revision-testable (debate 22/22 evidence path
docs/lab/wave6/...). D2 observational inference: a lawful observation stream whose latent
pattern L can discover via eliminative hypothesis logic and P receives as planted conclusions —
separates genuine learning from memorization. D3 deliberate judgment: importance/strength
assignments on memories (law 8) — tests whether planted judgments transfer vs internalize.
D4 integrity traps: prereg-fixed subset of the wave5/6 trap families — a GATE, not a metric.

**3c. Episode structure (per replication, native Zag).** Phase 0 (eps 0–9): bootstrap — P/H
implants written and audited; L scaffold begins. Phase 1 (eps 10–109): developmental curriculum,
identical scaffold for L and H; SIGNAL_DISCONNECT per topic. Phase 2 (eps 110–129): disproof —
world records contradict a prereg-fixed 10% false subset (≥6 claims; L receives them as false
observations, matched). Phase 3 (eps 130–159): interference distractors, then delayed retention
probes, no further teaching. Phase 4 (eps 160–179): final mastery battery + trap battery.

**3d. Metrics.** Mastery: % correct on the final 120-probe battery (D1–D3 balanced). Episodes-to-
mastery: first episode with rolling 20-probe accuracy ≥90% sustained ≥85% through ep 109. Re-
tention: delayed_score / peak_score at phase 3 end (learned = persists after disconnect). Re-
vision correctness: (a) false-claim revision rate on disproven claims, (b) genuine-claim reten-
tion on disproven-but-true controls (debate 18/18 precedent); composite = min(a, b). Traps:
% trap-correct — gate only.

**3e. Blinding.** Arm identity replaced by sealed labels (prereg-committed hash of the mapping).
All scoring by a deterministic native scorer reading ledger/audit + output bytes — no arm
knowledge. Any human adjudication of ambiguous revision traces sees redacted traces only;
afterward a guess-the-arm audit must not beat chance (binomial p < 0.05 = blinding failure).

**3f. Statistical plan.** n = 12 independent replications per arm; replication diversity from
prereg-fixed lawful initial-state histories (no RNG — standing law 1). Within-replication
pairing: all arms face the same 120-probe battery. Primary composite = mean of standardized
(mastery, inverted episodes-to-mastery, retention, revision composite); traps are the gate.
Pairwise arm comparisons via exact paired permutation tests (deterministic enumeration, no
random sampling). Multiple-comparison control: Holm over 4 metrics × 3 pairs = 12 tests,
α = 0.05. Per-domain splits and cost metrics are exploratory, reported unadjusted and labeled.

## 4. Kill bar
The PROTOCOL is killed (results invalid, redesign required) if any fires: (1) insensitivity —
no primary metric shows any Holm-significant pairwise difference at full n AND max |d| < 0.3;
(2) confound — P differs from L/H by >5pp on non-planted control probes (implant leakage);
(3) blinding audit beats chance; (4) replication collapse — all 12 replications byte-identical
per arm (no lawful variation captured); (5) budget — >2× prereg episodes or any replication
needs unvalidated >2^25-byte slice handling. Arm-level elimination (independent of winner):
any arm with trap-correct < 0.995 is UNSAFE and removed before any winner is declared.

## 5. Honesty notes
Content-equivalence is the crux: if L never encounters a fact, L's miss is a curriculum hole,
not an arm failure — control: log all exposures; exclude unexposed probes per-arm (prereg
rule). P's erasable implants are less like real trainer force-pins; the gap is noted, not
hidden. L/H scaffold quality is a fixed prereg curriculum — a confound, mitigated by identity
across L and H. n = 12 resolves large structural effects only; small differences are
undecidable — report CIs, never claim null effects. Revision probes inherit the debate limit:
authoritative world records must exist. Scale leg deferred (S100 stays gated); validate at S10.

## 6. Next build step
Build the sealed-mapping blind harness + the 120-probe prereg-hashed battery (with the disproof
subset and implant/exposure logging schema), then run a 3-replication × 40-episode pilot to
verify arm divergence exceeds probe noise before committing the full 12 × 180 design.
