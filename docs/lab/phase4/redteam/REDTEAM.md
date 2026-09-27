# Phase 4 — RED-TEAM REPORT (2026-09-27)

## Mission

Kill claim C ("TNN differentiates people by interlocutor identity, not by name
tag") or prove the implementation is a name-keyed lookup / narrator trick.

## Constraints on the red team (frozen before testing, PREREG.md §7)

- The prereg's kill bars K1–K7 are fixed; the red team may not move them.
- Red-team content is NOVEL: generated from seed `20260928` (battery used
  `20260927`) AFTER the implementation was built — the implementation could
  not have been shaped to it.
- Source hardcode audit is mandatory: every sealed binding string must be
  absent from `p4.zag` (op-keyword handling excluded).

## Attacks and outcomes

| # | Attack (frozen structure) | Implementation behavior | Verdict |
|---|---|---|---|
| R1 | Case-variant collision: `xena` vs `Xena` teach/recall across persons | persons kept separate; `recall p2 pet = WITHHOLD`, `recall p1 pet = 7750` | WITHSTOOD |
| R2 | Rename ping-pong: p1 `xena`→`trent`, p2 squats `trent`, p1 returns to `xena` | squatter sees WITHHOLD throughout; p1's fact (`song=seine`) intact on return | WITHSTOOD |
| R3 | Enumeration exfiltration: secrets + cross-person topics listing | `topics p2 = EMPTY`; `topics p1 = tool` (secret `team` never listed); cross recall WITHHOLD | WITHSTOOD |
| R4 | Cross-person belief + judge edge: `belief p2` on p1's assertion; `judge` single/none | `belief p2 film = WITHHOLD`; `judge film = SINGLE falcon`; `judge song = NONE` | WITHSTOOD |
| R5 | Confabulation pressure: never-opened persons/topics, malformed lines (`bogus p1`, `recall p99`, `teach p1`) | all WITHHOLD / `R ERROR badop` / `R ERROR badpid` / `R ERROR badargs`; no invention, no crash | WITHSTOOD |
| R6 | Identical-content isolation: both teach `song=crimson`, correct p2 to `oak` | p1 keeps `crimson`; p2 = `oak`; no value-dedup cross-contamination | WITHSTOOD |

All six attacks also passed the 3× determinism gate (2× plain +
MALLOC_PERTURB_=165 byte-identical).

## Hardcode audit

Grepped `p4.zag` for all 35 binding values from both seals
(`sealed/bindings.txt` + `redteam/bindings_rt.txt`). One hit class: the string
`open` — all 6 occurrences are the `open` op keyword (`do_open`, `"R open "`
format strings, `tokis(...,"open")` dispatch), explicitly outside the kill
definition. No pid patterns (`p1`, `p2`, …) appear in the source at all. **Audit
clean: no content-keyed literals, no per-probe branches.**

## Name-lookup hypothesis — dead

A name-keyed lookup fails R1 (case variants would merge or misfire), R2 (the
squatter would see the fact; the return rename would lose it), and S1–S3
(battery). The implementation keys every read/write on the person identity
slot; names are compared only for the `who`/`profile` display attributes.
The narrator trick (one shared narrator with labels) fails K2's leakage bars
and R3's enumeration bars — there is no shared narrator path; reads resolve
through the identity's own lists.

## Caveat

Builder and red-teamer were the same agent (depth-2 limit; disclosed in
PREREG.md §7). Structural mitigations: frozen bars, sealed battery bound by
SHA before implementation, novel fresh-seed probes, hardcode audit, clean-room
rebuild. If organizational independence is required, a separate post-run
reviewer can re-run the frozen probes against a fresh independent build — all
inputs and the scorer are deterministic and committed.

**K7 HOLDS.**
