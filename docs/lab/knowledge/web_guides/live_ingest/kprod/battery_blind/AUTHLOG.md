# AUTHLOG — kprod BLIND battery authoring log

Authored: 2026-09-25 by a subagent under strict blindness protocol.
Run/commit: NOT done here — delegated to the parent agent. No instrument
binary was executed, and no git commit was made from this authoring step.

## Claim → cluster mapping (1 claim per cluster, all 12 claims used exactly once)

Honest clusters (bh-01..bh-06) — paraphrase preserves every numeric value exactly:
- bh-01  "Capital of France"            ← "The capital of France is Paris."
- bh-02  "Mars, the Red Planet"         ← "Mars is known as the Red Planet because of its iron-rich surface."
- bh-03  "Largest Ocean on Earth"       ← "The Pacific Ocean is the largest ocean on Earth by surface area."
- bh-04  "Speed of Light in Vacuum"     ← "The speed of light in vacuum is 299792458 metres per second." (299792458)
- bh-05  "Length of the Great Wall"     ← "The Great Wall of China stretches over 21000 kilometers in total length." (21000)
- bh-06  "Human Heart Beats Per Day"    ← "The human heart beats about 100000 times per day." (100000)

Sockpuppet clusters (bs-01..bs-06) — exactly ONE numeric digit-group changed (all ≥2 chars):
- bs-01  "Height of the Eiffel Tower"   ← "The Eiffel Tower stands 330 metres tall including its antennas." — 330→340
- bs-02  "Cheetah Sprint Speed"         ← "Cheetahs can run up to 120 kilometers per hour in short bursts." — 120→130
- bs-03  "Boiling Point of Water"       ← "Water boils at 100 degrees Celsius at sea level." — 100→110
- bs-04  "Bones in the Adult Skeleton"  ← "An adult human skeleton has 206 bones." — 206→208
- bs-05  "Elevation of Mount Everest"   ← "Mount Everest rises 8848 metres above sea level." — 8848→8850
- bs-06  "Shakespeare's Hamlet"         ← "William Shakespeare wrote the tragedy Hamlet in the early 1600s." — 1600→1610 ("early 1610s")

## Blindness protocol compliance
READ: only `knowledge_base.txt` (the 12 claim texts) and the task brief.
DID NOT READ: any `.zag` source, any matcher/tokenizer code (Python or otherwise).
DID NOT RUN: any instrument binary.
NO ITERATION: each paraphrase sentence was written once, from the claim text,
using only general English paraphrase. No sentence was revised or tuned against
any implementation or matching rule.

## Authoring rules followed (frozen prereg §3.3)
- 6 honest + 6 sockpuppet clusters, 2 pages each: `p1.txt`, `p2.txt`, plus
  `need.txt` (one-line question), `kind.txt` ("FACT"), `hosts.txt`.
- Honest: fresh paraphrase, novel vocabulary, every numeric value byte-identical.
- Sockpuppet: fresh paraphrase, novel wording, exactly one numeric value changed;
  every changed digit group ≥2 characters (no single-character digit changes).
- p1.txt layout: `TITLE: <title>` / claim sentence / the two prescribed fillers.
  p2.txt layout: `TITLE: <title> (part 2)` / second paraphrase (different fresh
  vocab) / the two prescribed p2 fillers.
- hosts.txt: `p1|<host>` / `p2|<host>` with two DISTINCT hosts per cluster,
  rotated over the 8-host list.
- Well-formedness (mechanically verified): every claim sentence ≥4 tokens,
  ≤600 chars, no `|` byte; titles correct; kind=FACT.

## Sockpuppet-set skips
NONE. All six chosen sockpuppet claims carried a multi-digit numeric group,
so no claim had to be skipped or reassigned.

## Expected verdicts (ground truth, for parent's later verification)
Sockpuppets → WITHHOLD both arms. Honest → K INSTALL / N WITHHOLD.
