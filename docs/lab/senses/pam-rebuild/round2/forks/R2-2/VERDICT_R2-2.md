# VERDICT R2-2 — Two-sided adversarially-distinctive signature

**Status:** **DEAD — falsified on B5 and the novel-collision kill bar.**
**Deciding bar:** B5 (false-install rate 4.0% targeted vs 1% kill threshold; 14.4% overall vs 2% threshold). The novel-family kill bar also fails independently (425 novel false installs).
**Hypothesis (verbatim from DEBATE_A §16 HC-2):**

> **HC-2 — Two-sided adversarially-distinctive signature (P4+P8).**
> *Rule:* INSTALL only if the percept's relational signature is nearer to enrolled true exemplars than to a frozen bank of known-false collision patterns, by a preregistered margin, on attack-aware features. Nearer to (or within margin of) a known-false pattern → WITHHOLD. The false bank grows with every caught attack across rounds.
> *Sketched kill bar:* false-install ≤1% under signature-targeted attacks (attacks designed to collide); retrieval accuracy ≥90%; every enrolled false pattern must withhold its own class (no self-collision installs). Dies if a novel collision class installs, or if answering the false-bank regress ("always one attack behind") fails measurably.

**Contract (frozen):** INSTALL iff `dist(percept, nearest true) + 0.15 < dist(percept, nearest false)`, implemented as integer milli-units: `dt + 150 < df`.

## Bar table

| Bar | Requirement | Result | Verdict |
|-----|-------------|--------|---------|
| B1 viability | mean primary accuracy on frozen 370 ≥ 60% | 365/370 = 98.6% | ✅ PASS |
| B2 vs Approach A | delta reported | R2-2 98.6% vs A 74.1% (+24.6pp) | — reported |
| B3 efficiency | ops/bytes vs A; signature vs 36B datum | 162k vs 1,085k ops; 32B vs 36B | — reported |
| B4 contract proof (HARD) | ≥10% changed AND fewer false installs | 49.7% changed; 836 < 2022 | ✅ PASS |
| B5 KB4 (HARD) | ≤1% targeted; ≤2% overall | 4.0% targeted; 14.4% overall | ❌ FAIL (KILL) |
| B6 determinism (HARD) | 3 byte-identical runs, chains verified | 1 run; 11,285/11,285 chains verify; 3-run not completed (dead at B5) | ⚠️ INCOMPLETE |
| B7 beauty | mechanism elegance; artifacts pending Micah | Two-sided reference works; no artifacts produced | — pending |
| Retrieval ≥90% | installed-correct / installed | 249/249 = 100% | ✅ PASS |
| Self-collision | 7/7 bank entries withhold | 0 installs | ✅ PASS |
| Novel families | zero false installs (kill bar) | 425 false installs | ❌ FAIL (KILL) |

## Why it died

The two-sided contract works as designed — it withholds when a percept is near the false bank — but the false bank cannot cover the attack space. Two independent failures:

1. **B5 targeted (4.0% vs 1%):** R2A-SHP-1 (occlusion-bar) defeats the contract at 17.8% false-install (71/400). The occlusion attack moves the shape signature far from BOTH the true exemplars and the bank's occlusion entries, landing in a region where `dt + 150 < df` still holds because the bank's 2 occlusion patterns don't cover the attack's variation.

2. **Novel-family regress (425 installs):** PTC-2 (400), CCN-2 (340), MOT-2 (350) — attack classes NOT in the bank — install false memories at high rates. The hypothesis's "bank grows with every caught attack" does not answer the "always one attack behind" regress measurably: novel attacks install before they can be caught.

The mechanism is load-bearing (B4 passes: contract changes 49.7% of decisions, cuts false installs from 2022 to 836), but load-bearing is not sufficient. The bank is always incomplete, and the margin cannot distinguish "far from bank because safe" from "far from bank because novel attack."

## Build notes

- znc compiler hangs/crashes on SHA256 + single 3700-write builder; workaround: chunked builders (40 records/chunk). Not a prereg change.
- Stride bug fixed: `(i*10+w*4)` → `(i*40+w*4)` in EX_get/FB_get.
- Bank: 7 PREREG-faithful entries (G3 ×1.15 boost, 2 occlusion, 2 reversed, H1 metamer, H1 flicker).
- Fixture counts: 5,100 normal + 5,815 adversarial (granular tables govern); 1,850 targeted; 1,090 novel. See evidence/GEN_LEDGER.md.
- Fixture generation byte-identical across 2 independent runs (MANIFEST.sha256 matches).
