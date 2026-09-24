# H6-R2 Final Synthesis — Self-PAM: Corroboration Is Dead, Discipline Survives

**Date:** 2026-09-24 · **Program prereg:** `b3db7b7a` · **Status:** FINAL

## The question

Round 1 died honestly: the C1 "corroborator" checked analytic structure (span sums,
max attestation), not meaning — 9.5% confabulation catch vs a 70% bar, 201/305
confabulations installed as permanent false memory. Round 2 asked: can a meaning-first
redesign revive self-PAM, and does the 0-bit judgment-side ceiling (Muse-B's verdict:
no deterministic function over the same state creates source independence) hold?

## Independent verdicts (all mechanisms pure Zag, zero RNG, byte-identical ×2)

| Fork | Identity | M1 | M2 | M3 | M4 | M5 | M6 | M7 | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| C | consistency enforcer | PASS | PASS | PASS | **FAIL** (0/24) | **FAIL** (0/24) | PASS | PASS | **THEATER** |
| D | discipline | PASS | PASS | PASS | PASS (24/24) | PASS (8/8 + 4/4 held-out) | PASS | absent* | **SURVIVES** |
| W | witness | PASS (22/22) | FAIL (82.6%) | PASS (15/15) | PASS (10/10) | **FAIL** (0/10) | FAIL (30% f-w) | — | **DEAD** |

*D M7 held-out: builder never built the held-out corpus; attack crew ran fresh held-out
cases (10/10 M2, 8/8 M4, 4/4 M5) but a formal M7 corpus is absent.

**Evidence:** fork C build `0a2e006c`; fork D builds `003b3e7c`/`a3dc24f9`/`e6d33de2`/`20025bc7`;
fork W recovered from scratch (byte-identical to reported SHA `eff00337…`), builder never
committed sources — a process defect on record. Re-attack evidence: `a53b75dd` (W),
`f5df1014` + `c83be950` (C/D), all on `tnn-native-lab`.

## What the debate predicted vs what happened

The binding debate verdict (prereg `b3db7b7a`) killed "corroboration" as a framing and
predicted the theater signature: M1–M3 pass, M4/M5 fail — passing surface meaning tests
while accepting self-authored alibis is not survival.

- **Fork C exhibits the predicted signature exactly.** Its mechanism licenses the
  deliberation's say-so (`fs_add_delib`) without store validation, and does not
  discriminate GEN provenance (`lic=STORE:S9xx:GEN` installs). The first attack round's
  "DEAD" verdict on C was invalid (its driver parsed 81/540 cases); the re-attack
  reproduced the builder's numbers exactly and confirmed THEATER.
- **Fork W is a genuine mechanism, not theater** — it passes M4 (10/10 trace-alibi
  rejection), beating the predicted killer — but dies on M2 (scope-pair `attr-attach`
  inference gap), M5 (0/10, exactly the predicted boundary), M6 (30% false-withhold:
  too censorious), and W2 (4/10). Its self-test's "failed most bars" was dominated by
  three scorer bugs found by the re-attack (packed-count unpack errors, a field-clobber
  that paired fixtures by token count, non-interned string comparison) — a standing
  lesson: audit the scorer before trusting a kill.
- **Fork D breaks the predicted signature.** It rejects 24/24 trace alibis and 8/8
  confabulations grounded in *genuinely generator-authored* entries (the re-attack crew
  built a real two-episode authorship chain with pinned deliberation records — not the
  EXT/GEN label stand-in the builder's self-test used), plus 4/4 held-out in a new
  domain. It also rejects 12/12 utterance-type smuggling attempts and is stable under
  paraphrase avalanches.

## Does D crack the wall verdict?

No — it **relocates** it. Muse-B's wall was about self-*corroboration*: no deterministic
function over the same state manufactures source independence. D never attempts
corroboration; it is pure discipline — mechanical provenance enforcement that claims
no new evidence about the world. The wall on semantic self-judgment stands (C and W
confirm it from both sides).

D's residual boundary is exactly where Muse-B said independent information must come
from: D discriminates on the PROV *label*, not on authorship itself. The re-attack's
M5L-001 probe demonstrates provenance laundering — relabel GEN as EXT → INSTALL. Under
honest labeling D survives; the trust root is the label. A write-once evidence
partition the generator cannot author (Muse-B's proposed crack) remains unbuilt and is
the explicit next experiment: D's discipline + a tamper-evident provenance substrate
would move the trust root from labels to physics.

## Process record (for the program's honesty ledger)

1. Sol (`gpt-5.6-sol`) never produced a substantive debate response — repeated
   `choices:null` with zero completion tokens on prompts far below length limits.
   Provider-side failure, documented, not treated as participation. grok-4.6 supplied
   the external voice.
2. First attack round was compromised: committed to wrong branch (`r2-7`), false
   "fork D not found", attacked uncommitted W scratch with a red-team-built witness,
   invalid C verdict (81/540 parse). Fully re-run by two independent re-attack crews
   with a binding driver-validation rule (reproduce the builder's numbers with the
   builder's scorer before independent scoring).
3. Fork W's builder never committed its sources; recovered from scratch and verified
   byte-identical to the reported output SHA before attack. Fork D's committed tree had
   build defects (missing `substrate/`, missing drafts/delib corpora, `build.sh`
   masking znc failure without `pipefail`); recovered locally with SHA-verified
   natives, corpora regenerated byte-identically.

## Bottom line for Micah

- **"Corroboration" as a self-PAM framing is dead.** Confirmed twice independently.
- **Discipline survives.** Fork D is a real, deterministic, pure-Zag mechanism that
  catches mechanically ungrounded speech — including generator-authored alibis and
  recursive self-entries — without claiming any new knowledge about the world.
- **The remaining gap is the trust root of provenance labels.** The next fork to build:
  D's discipline over a write-once evidence partition the generator cannot author.
- **Witness (W) is real machinery with genuine gaps** — testimony itself is faithful
  (W1 95/95, ledger intact), but it fails as a catch mechanism at the M5 recursion and
  over-withholds (M6 30%).
