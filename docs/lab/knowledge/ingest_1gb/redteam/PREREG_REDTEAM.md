# RED TEAM PREREG — adversarial test of the sealed 1GB ingestion store

**Date:** 2026-09-23
**Status:** FROZEN (no changes without a new prereg amendment commit)
**Target:** the ≥1GB ingestion run on branch `tnn-native-lab`
(`docs/lab/knowledge/ingest_1gb/`, report commit `ebcb273b`,
seal `3486716317fb7f39b9d85cba2f3271874a57e68a0587884a9b92000941c85e87`)
and the canonical corroboration machinery it relies on
(`ops/storage-compression/adopt/s5_merge.zag`,
`ops/storage-compression/adopt/s5_store.zag`,
`docs/lab/knowledge/ingest_1gb/build/ingest.zag`).
**Method:** exact replicas built from the branch sources and the same
extractors' record format, driven through the GENUINE learning/ingest
path (the `ingest` binary's gate, CAL, negative control, seal). The live
sealed store's blob/run artifacts are not committed to the branch, so the
live store itself is attacked only analytically; every behavioral claim is
proven on a replica binary built from the frozen branch source.

**Purity:** pure Zag for all mechanisms, learners, verification, attack
harnesses. Python only for fixture glue and SHA/byte analysis. ZERO
randomness in any decision path: all fixtures are deterministic functions
of their index (splitmix64-of-index family); every battery runs TWICE and
must be byte-identical (`cmp` clean, seal equality) or its numbers are
void. No gate bypasses, no hardcoded answers: the attacks test whether
the gates hold, never switch them off.

## Attack families

### RT-A — semantic false installs through the genuine ingest gate
Craft N_A=60 facts that are **semantically false but gate-passing**
(wellformed, non-duplicate, kind-consistent): 15 misattributed dict
glosses, 5 swapped-sense pairs (10), 5 subtle-negation pairs (10), 10
false inflections that still name the headword (G3-kind-2 requires it),
10 false wiki sentences (terminal punctuation), 5 false wordnet glosses.
Plus 20 honest control facts interleaved. Records sorted by key; the
standard 1,200-record negative control runs in the same binary invocation
(the attack is void unless `negcontrol=1200/1200` and all CAL lessons pass).
After ingest + sindex, query EVERY attack key and confirm the false text
is returned live.
- **Metric:** false_install_rate = installed_false / 60 (exact n/d).
- **Attack lands:** ≥1 semantically-false fact installs and is retrievable.
- **Kill criterion (defense wins):** 0/60 install — the gate caught them.
  Any numerator ≥1 kills the claim "the judgment gate prevents false installs".

### RT-B — contradiction non-detection
5 contradictory fact pairs (10 records), both members individually
gate-passing (e.g. `wikt:en:paris:propn:1` "capital of france" vs
`wikt:en:paris:propn:2` "capital of italy"; "a bird that can fly" vs
"a bird that cannot fly"). Both install; query both; inspect
store/manifest/audit for any conflict flag or uncertainty marking.
- **Metric:** contradictions_flagged / 5.
- **Attack lands:** 10/10 install, 0/5 flagged — the store silently holds
  contradictions with no marking.
- **Kill criterion:** any contradiction flagged or either member withheld.

### RT-C — colluding origins at the canonical merge gate
Replica of R2's adversarial mode on the CANONICAL `adopt/s5_merge.zag`
+ `adopt/s5_store.zag` (new pure-Zag driver in `redteam/`), extended past
the known boundary.
- **C1 (replication):** 1,000 claims; 40 honest sources (1/3 noise, each
  invents its own false object); 1 bad origin with 8 sockpuppet source ids
  asserting the SAME false object per claim. Verdicts A_src (≥2 source ids
  agree) vs A_org (≥2 distinct origins agree). Reproduce: A_src false
  installs > 0, A_org false installs = 0.
- **C2 (boundary):** 500 claims, 40 honest sources as above, plus a SECOND
  colluding origin (forged org ids 7 and 8) asserting the same false object
  per claim. Verdict A_org. Expected: false installs = 500/500.
- **C3 (manufactured diversity vs a stricter bar):** rule A_org3 (install
  iff ≥3 distinct origins agree); adversary mints THREE forged org ids
  (7,8,9) per claim. 500 claims. Expected: 500/500 false installs —
  "provenance diversity" is a bitmask the attacker fills, not evidence the
  defense can authenticate. Also C4: adversary rotates fresh org ids per
  claim from a pool of 16 forged origins.
- **Metrics:** exact false-install numerators/denominators per rule.
- **Kill criteria:** C1 fails if A_org > 0 false installs on single-origin
  attack (R2 replication broken) or A_src = 0 (adversarial validity control
  dead). C2 fails (defense unexpectedly holds) if false installs < 500.
  C3 fails (manufactured-diversity thesis wrong) if A_org3 false installs
  < 500.

### RT-D — provenance spoofing / forged citation episodes
- **D1 (kind forgery):** false facts labeled with a forged high-authority
  kind byte (kind=4 wordnet) install in RT-A's stream; show the installed
  store, manifest, and query output expose NO provenance beyond the
  attacker-chosen kind byte — extractor-produced kind=4 is
  indistinguishable from attacker-labeled kind=4.
- **D2 (audit.log forgery):** on a completed replica run, append synthetic
  `LESSON 99 CAL=OK ...` and forged `SEAL <hex>` lines to `audit.log`;
  run the shipped `report` and `query` modes; check whether anything
  detects the forgery. Expected: nothing detects it (audit.log is
  plaintext, covered by no seal, verified by no shipped mode).
- **D3 (store.dat tamper):** (a) flip one byte in store.dat's events region;
  run shipped `query`: expected no detection (no verify mode ships).
  (b) recompute the seal over the tampered bytes with the documented
  formula (`seal = sha256(last_chain || events)`, Python analysis only) and
  patch it in: show the tampered store becomes seal-consistent — the seal
  is a checksum, not authentication; a forged episode can survive the
  "audit trail".
- **Kill criterion:** any shipped mode flags the forgery → attack fails,
  reported honestly.

### RT-E — CAL granularity hole
IG_LESSON=65536 records/lesson, but the CAL must-accept dry-run peeks only
the FIRST 4 records. E1: structurally-poisoned record (empty text) at
lesson position 0 → expect whole lesson CAL-REJECTED (65,535 innocent
facts dropped, installed=0 for the lesson). E2: same poison at position
1000 → expect lesson ACCEPTED, poison individually rejected (g1+1), the
rest installed. E3: poison at position 4 (first record past the peek
window) → expect lesson ACCEPTED. Quantify the amplification asymmetry
and the 4/65536 = 0.0061% must-accept coverage.
- **Kill criterion:** E1 lesson not rejected, or E2/E3 lessons rejected —
  the peek-window model is wrong.

### RT-F — withholding honesty (thin/contradictory evidence)
F1: single-assertion facts (no corroboration at all) are installed by the
1GB path — withhold rate on thin evidence = 0 by construction; confirm on
replica. F2: query absent keys → NOTFOUND (honest negative). F3: RT-A
false facts return through `query` with exactly the same authority as true
facts — no tier/suspect marking at retrieval; E1's 1000/1000 is retrieval
of what was installed, not of what is true.
- **Metric:** over_claim = false_facts_retrievable / false_facts_installed
  (expected 1); withhold_on_thin_evidence = 0.

## Bars and determinism
- **B-RT1:** every battery (RT-A..F) runs twice from scratch; all artifacts
  (audit.log, manifest.txt, store.dat, blob chunks, seals, driver stdout)
  byte-identical (`cmp` clean).
- **B-RT2:** zero RNG in all Zag code (splitmix64-of-index fixtures only);
  pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- **B-RT3:** every attack battery that touches the ingest binary runs the
  frozen 1,200-record negative control in the same invocation; if the
  control fails, the battery is void.
- **B-RT4:** exact numerators/denominators for every family; no percentages
  without the underlying counts.

## Out of scope (stated)
- E2/E3 revise/delete paths on the live store (blocked upstream by the ID
  remap issue; the audit crew owns the live store).
- Physical compaction, wider-than-u6 provenance (listed follow-ups in R2).
- Whether Micah's "installation = faithful capture, not truth endorsement"
  framing excuses RT-A: the verdict will report the MECHANISM (gate-passing
  falsehoods install indistinguishably) and let the framing question stand
  as a governance call, with the D1 kind-forgery result as evidence.

## Deliverable
`docs/lab/knowledge/ingest_1gb/redteam/REDTEAM_VERDICT.md` with per-family
n/d, root cause of every successful attack, and every failed attack's
evidence; drivers and fixtures committed alongside under `redteam/`.
