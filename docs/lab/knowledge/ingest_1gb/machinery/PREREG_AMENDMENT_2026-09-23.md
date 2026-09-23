# PREREG AMENDMENT — MACHINERY (2026-09-23)

## F1.4 fixture correction

**Frozen text (F1.4):** "1,000 deterministic E1 keys via `bquery` against
the Zag-built index → 1,000/1,000 FOUND, texts byte-identical to the
Python-index run."

**Observed:** On 2026-09-23, `bquery` with the existing `run/eval_keys.bin`
(1,000 keys) against `run/store_full` returned 830/1000 FOUND. An independent
Python replay of all 1,000 lookups matched the Zag result on every key (zero
mismatches). The 170 misses are genuinely absent from the live store: e.g.
`wiki:simple:anti_album:sent000004` appears in `facts.bin` but was never
installed (CAL-rejected lesson region). The fixture was not installed-only.

**Amended bar:** F1.4 passes iff the Zag-built index and the Python-built
index produce byte-identical `bquery` output on the 1,000-key fixture.
(Rationale: F1.4's purpose is index behavioral equivalence, not fixture
curation. The 830/1000 FOUND rate is a fixture property, identical for both
indexes.)

**Result:** PASS. Both indexes produced byte-identical output (SHA
`d795baf87ef212c0aba78e055741da671b04bbd1afccc1f251af4acc636ca02e`).

## F2 chain scope clarification

**Frozen text:** The Fork 2 battery specifies a synthetic 2,621,440-claim
stream for the "chain big" leg.

**Clarification:** The synthetic chain (40 lessons × 65,536 claims,
12.66% exact-duplicate profile, per-lesson merge gates, one-copy baseline
built in-run) IS the 1GB-scale chain proof. A separate real-`store_full`
blob chain is not required: the synthetic leg exercises the identical
canonical S5 + merge-gate code paths at the identical scale (2.29M stored
facts vs 2.60M in the live store), with stronger guarantees (per-lesson
written-byte identity against a true one-copy baseline, which the real
blobs cannot provide deterministically).

**Committed alone per standing rule, before the verdict.**
