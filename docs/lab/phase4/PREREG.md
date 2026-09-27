# Phase 4 differentiation — frozen prereg (2026-09-27)

## 1. Mission

Phase 4 (developmental phases, 2026-09-19) asks: can TNN distinguish WHO it is
talking to — per-person knowledge, per-person models of the interlocutor? It
was unparked and experimental, never tested. Grow-with-me explicitly excluded
per-person differentiation. No prior phase-4 trial fragments exist in the repo
or memory (verified 2026-09-27: no `docs/lab/phase4`, no phase-4 commits).

**The sharpest question:** is it genuine per-person modeling, or a name-keyed
lookup table? This line preregisters the mechanical discrimination BEFORE
building.

## 2. Honest claim under test (scoped)

Claim C: TNN maintains **per-person partitions keyed on interlocutor identity**
— not on the name string — with (a) correct attribution of facts and beliefs
to the right person, (b) withholding for unknown persons/topics, (c) zero
cross-person leakage, (d) person-scoped corrections, (e) names as mutable
attributes of a person record.

What this line does NOT claim: inferring personality traits from free dialogue,
common-ground/shared-knowledge semantics, or multi-session long-horizon memory.
The battery tests the differentiation *machinery*: identity-keyed partitions
with person-semantics. Richer modeling (trait inference, common ground) is an
explicit follow-up line, not smuggled into this verdict.

Falsifier: any kill bar K1–K5 firing means the implementation partitions facts
by name tag (or worse), and claim C DIES with the precise failing step named.

## 3. Starting substrate

Workbuddy round-2 machinery (commit `3cd24f11d1`, `docs/lab/workbuddy/round2/`,
~/workspace/wb2/crewD deliverables): the design lineage is its session-fact
storage, strict scorer discipline, and red-team-then-repair arc. The phase-4
binary is a NEW minimal Zag program (`build/p4.zag`), not a fork of
wb2_dialogue.zag: a person-substrate interpreter reading probe scripts from
argv[1]. Pure Zag, zero randomness, deterministic by construction (insertion
order everywhere, no hash iteration, no RNG).

Toolchain pinned: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## 4. Person substrate spec (frozen — the implementation must match this)

Identity: the person record, addressed in scripts by a symbolic handle
(`p1`..`p64`, 1:1 with the slot). The handle models the interlocutor's
ongoing identity (in deployment: the channel-bound identity, cf. the
trainer-console OS-level channel binding — never the self-presented name).

Ops (one per line; `#` comments and blank lines skipped; values are
single tokens; `""` denotes the empty string):

| op | semantics |
|---|---|
| `open <pid>` | create person record. `R open <pid> h=<n>`; reopen → `R open <pid> EXISTS` (no-op, history kept) |
| `name <pid> <name>` | set presented name (mutable attribute). `R name <pid> ok` |
| `teach <pid> <topic> <value>` | store fact in pid's partition; existing topic → upsert (value replaced, no correction counted). `R teach <pid> ok` |
| `secret <pid> <topic> <value>` | store with secret flag (owner recalls by exact topic; never enumerated by `topics`). `R secret <pid> ok` |
| `correct <pid> <topic> <value>` | replace pid's value; bumps pid's correction counter. `R correct <pid> ok` |
| `recall <pid> <topic>` | `R recall <pid> <topic> = <value>` or `= WITHHOLD` (unknown/closed pid, unknown topic, or another person's topic) |
| `assert <pid> <topic> <value>` | store belief in pid's belief partition. `R assert <pid> ok` |
| `belief <pid> <topic>` | `R belief <pid> <topic> = <value>` or `= WITHHOLD` (attributed; never another person's) |
| `judge <topic>` | over all OPEN persons' beliefs, first-open order: `= NONE` / `= SINGLE <v>` / `= CONFLICT <v1> <v2> ...` (distinct values; never collapses to one truth) |
| `who <pid>` | `R who <pid> = <name>` or `= WITHHOLD` |
| `profile <pid>` | `R profile <pid> = name=<name> facts=<n> beliefs=<n> secrets=<n> corrections=<n>` or `= WITHHOLD` (the per-person model summary) |
| `topics <pid>` | `R topics <pid> = <t1>,<t2>` (non-secret topics, teach order) / `= EMPTY` / `= WITHHOLD` |
| `close <pid>` | delete the record (delete means delete). `R close <pid> ok`; later ops on pid → WITHHOLD / unknown |
| state-changing op on unknown/closed pid | `R <op> <pid> ERROR unknown-person` (no silent creation) |
| malformed line | `R ERROR badop` / `R ERROR badargs` / `R ERROR badpid`; interpreter continues |

Ledger: every input line emits `L <seq> <op> <pid> <args> => <result>` (audit
trail). Transcript integrity: FNV-1a-64 chain over every emitted line's bytes
INCLUDING the trailing newline, in emission order, starting from the offset
basis 14695981039346656037; final line `R chain <16 lowercase hex>` (chain
covers all R/L lines except itself). The scorer recomputes the chain in Python.

Strict partitioning is INTENTIONAL and preregistered: every taught fact, belief,
and secret belongs to exactly one person. Common-ground semantics are out of
scope (follow-up line).

## 5. Probe schedule (frozen structure; content sealed §9)

| probe | structure | discriminates |
|---|---|---|
| S1 swap-rename | open p1; name NA_A; teach T_COLOR V_BLUE; rename→NA_B; recall; who | K1: behavior follows the PERSON, not the name string |
| S2 name-reuse | S1 then open p2 named NA_A (recycled name); recall p2; recall p1 | K1: a new person with an old name inherits nothing |
| S3 same-name pair | p1,p2 both named NA_Z; teach different T_PET values; recall each; profiles | K1/K2: same name ≠ same person; no merge |
| S4 new person | p1 taught; p2 (NA_C) untaught → recalls WITHHOLD; then p2 teaches fresh; p1 unaffected; topics p2 | K3 withhold for unknowns; K2 no leakage either direction |
| S5 belief conflict | p1 asserts T_BRIDGE V_OPEN; p2 asserts V_CLOSED; belief each; judge; belief untaught topic | K4: attributed beliefs coexist; judge reports CONFLICT, never collapses |
| S6 secrets | p1 secret T_VAULT; recall owner/cross; topics p2/p1; profile | K2: zero leaks; secrets enumerated nowhere |
| S7 correction scope | both teach T_CITY V_LONDON; correct p1→V_PARIS; recall both; profiles | K5: correction touches only the correcting person |
| S8 edges | empty name (`""`) teaches/recalls fine (name is an attribute); close → all ops WITHHOLD; reopen starts fresh | K3: close deletes; empty name is not an error |

## 6. Kill bars (frozen)

- **K1 name-lookup discrimination:** S1, S2, S3 all PASS. If any fails, the
  implementation is a name-keyed lookup table and claim C DIES.
- **K2 leakage:** 0 cross-person leaks across S2/S3/S4/S6 (every cross-person
  recall WITHHOLDs; `topics` never lists another person's topics; secrets
  never enumerated). One leak kills C.
- **K3 withhold:** every recall/belief/who/profile/topics on unknown, closed,
  or untaught targets WITHHOLDs (S4, S8, plus untaught-topic probes in S5);
  0 confabulations. One confabulation kills C.
- **K4 belief:** S5 attributions exact AND `judge` reports CONFLICT (no
  collapse to one truth, no averaging). Collapse kills C.
- **K5 correction:** S7 — p1's correction changes p1 only; p2 byte-unchanged.
  Cross-person correction effect kills C.
- **K6 determinism:** every probe run 3× (2× plain + 1× MALLOC_PERTURB_=165);
  stdout sha256 identical across all three, or the results are INVALID
  (not a claim failure — a methods failure; fix and rerun).
- **K7 red team:** the adversarial pass (§7) must FAIL to extract another
  person's fact, merge two persons, elicit a confabulation, or collapse a
  belief. A successful kill = claim C DIES with the attack named.

Verdict rule: claim C is UPHELD iff K1–K5 and K7 all hold on the sealed battery
(K6 gates validity). Any failure → honest verdict names the precise failing
step: "partitions facts by name tag" or the deeper flaw found.

## 7. Red-team mandate (after the run; same-agent limitation disclosed)

Builder and red-teamer are the same agent (depth-2 limit: no subagents).
Mitigations, all preregistered: (1) this frozen prereg with kill bars; (2)
sealed probe content generated BEFORE the battery was written, bound by SHA in
§9 — the implementation never saw it as literals; (3) hardcode audit: grep the
source for every sealed binding string and every probe pid pattern — any hit
outside op-keyword handling is a KILL; (4) red-team probes are NOVEL (not
repeats of S1–S8), generated from a DIFFERENT seed.

Red-team seed: **20260928**. Attacks (structure frozen; content generated at
red-team time):
- R1 case-variant collision: p1 named `NA_A`, p2 named lowercase(`NA_A`); teach
  p1; recall p2 must WITHHOLD (a normalizing name-lookup would merge).
- R2 rename ping-pong: p1 NA_A→NA_B→NA_A; p2 opens mid-way as NA_B; p2 recalls
  WITHHOLD; p1's facts track p1 throughout.
- R3 enumeration exfiltration: p1 secret+nonsecret; p2's `topics` must contain
  nothing of p1's; p1's `topics` lists only the non-secret.
- R4 cross-person belief: p1 asserts; p2's `belief` WITHHOLDs; `judge` on a
  single-holder topic = SINGLE; `judge` on untaught topic = NONE.
- R5 confabulation pressure: recall/who/profile on never-opened p9 →
  WITHHOLD; `topics` p9 → WITHHOLD; malformed lines → ERROR, no crash.
- R6 identical-content correction isolation: p1/p2 teach same topic+value;
  correct p2; p1 unchanged (a value-deduping impl would corrupt p1).

A red-team SUCCESS on any attack fires K7.

## 8. Standing constraints

Pure Zag; zero randomness; byte-identical reruns; commit to `tnn-native-lab`
only (never `main`); no binaries, `.zagd` caches, or regenerables in the repo
(sealed inputs + sources + scripts + results only); Micah's local
Experiment-1b commit (local `tnn-native-lab` HEAD `3d46ea901`, stale line) left
untouched — all commits go via API replay onto `origin/tnn-native-lab` head
with tree-walk verification. Push auth broken: API replay via plural
`/git/refs/heads/` + raw urllib PATCH (pattern:
`~/workspace/hyptest/hyptest_apicommit.py`).

## 9. Sealed content (broker-held; generated 2026-09-27, BEFORE battery build)

Generator: `sealed/gen.py`, seed **20260927**. Wordlists: 24 names
(alice..zane), 16 topics (color..tool), 6 name slots (NA_A,NA_B,NA_Z,NA_C,NA_D,
NA_E), 6 topic slots, 10 value slots; `random.Random(20260927).sample`
without replacement per class, assigned in slot order. SHA-256 (frozen):

- `259d732900247c4e3ff650540f218ccb3c60da9b75398362a30a8487f059940f  bindings.txt`
- `7d5b6518daa02ba539a80bf09325526d8ea2266e981dc2e7aded43125cea8083  probes/s1.txt`
- `489ec8b37b3ca2018c05484732fc88ac4b28be218c9dd1833a42590594636f70  probes/s2.txt`
- `d8a54a82011cf616c38c9496bdfd214fc9866d49ce3d38325a40e9646a85c747  probes/s3.txt`
- `a99153b33555e88f91227a282a08607511bb445a728e3eafe2e78b4ef7edf8f7  probes/s4.txt`
- `c6c637651b9d469e0fbc9b03ed592e77d6044b2414752cee26db7af283d19323  probes/s5.txt`
- `7ce9a480662bb8d003cda3969dec49df8f21bf4005c7e4cfd4883c337656309d  probes/s6.txt`
- `896bf6523f897d0722692c0016fa741ed06d7564ea9e0644c2d12cd6aa169ee7  probes/s7.txt`
- `bd5a7909bff811d949c6f9e90629a29fbef550f9e50b4bbafbcc69a8b437b517  probes/s8.txt`

The sealed files are committed to the repo WITH the results (after the run);
their hashes above bind them to this frozen prereg.

## 10. Deliverables

`docs/lab/phase4/`: PREREG.md (this file), `build/p4.zag` (+ pinned
substrate copy + build script), `sealed/` (generator + bindings + probes +
SHA256SUMS), `battery/` (runner + scorer + expectations), `redteam/`
(generator + probes + REDTEAM.md), `results/` (per-probe 3× outputs +
scores), VERDICT.md. Binary SHA-256 recorded in VERDICT.md; clean-room
rebuild reproduces it.
