# Interactive TNN status: wave-20261002-0221pdt, INTERACTIVE lane

## Verdict

A runnable interactive TNN exists on branch tnn-native-lab and holds a live
multi-turn probe chat. Verdict: WORKS.

## The working entry point

- Source: `docs/lab/rsi/fit_authority/tnn_chat.zag` (frozen authority instrument,
  sha256 `c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c`,
  matches AUTHORITY_MANIFEST.md)
- What it is: frozen v1 retrieval core plus dialogue state manager from
  `docs/lab/dialogue/dialogue.zag` (verbatim above line 1784), with the batch
  driver replaced by an interactive stdin line loop using unbuffered raw
  syscalls. Multi-turn state (salience, topic, user context, history,
  pending-question buffer, per-turn answer exclusion, NOVEL composition path)
  persists across turns.
- Imports vendored in build dir: `R33_NATIVE_SHA256_V2.zag`
  (`9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf`)
  which itself imports `R33_NATIVE_IO_V1.zag` in Linux form
  (`e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`).
  The Darwin-form copies in the R33 generation tree do not build on this Linux
  znc; Linux form required.
- Knowledge inputs (run directory): `kb.txt` (38 facts,
  `3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1`),
  `gaz.txt` (27 entities,
  `b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a`),
  both byte identical to the frozen authority copies.

## Exact build and launch

Build (pure Zag, pinned znc verified sha256 `498abcb5ab346f8c...` before use):

```
znc tnn_chat.zag --no-zagd --no-analyze --no-foreground-cache -o tnn_chat
```

Launch (from a directory containing kb.txt and gaz.txt; chat is line-based
over stdin, so a piped script is equivalent to a human typing):

```
./tnn_chat < probes.txt
```

Binary: ELF x86-64, 270204 bytes,
sha256 `1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c`.
This hash is byte identical to the binary hash recorded in the original
2026-09-23 smoke report: same frozen source plus same pinned toolchain
reproduces the same binary nine days later.

## Evidence

1. Build: `znc` exit 0, zero errors, build log in `build/build.log`.
2. Three-prompt scripted probe (`build/probes3.txt`, sha
   `9461b78fc58750af4e2684bc84336ca91248072d47d1c0f7971e00d9b60c5941`):
   output `build/run3.out` (sha `10a01041ba9f453ccfa6fe3d92a28c7e102045700ca7675832325a1f949c3b98`)
   shows ready banner, 38 facts loaded, correct retrieval, NOVEL composition,
   and clean quit.
3. Determinism: second identical run byte identical (`cmp` clean).
4. Five-exchange red-teamed probe chat: see PROBE_CHAT.md, byte captured in
   `build/probe5.out` (sha `d61610ca1d4d814a1af4d72b2673908a40e1c6b04cc5172695a7f363f22538b9`),
   inputs `build/probe5.txt`.
5. Multi-turn state confirmed: pronoun resolution across turns ("when was he
   born?" after "who wrote the martian?" resolves to Andy Weir) and `/new`
   resets conversation state.

## Candidate evidence table

| Candidate | Location | Status | Evidence |
|---|---|---|---|
| tnn_chat.zag interactive driver | `docs/lab/rsi/fit_authority/tnn_chat.zag` | WORKS | built with pinned znc, 270204-byte ELF, ran 3- and 5-turn scripted chats, deterministic, byte captured |
| tnn_chat_decline.zag | `docs/lab/rsi/fit_authority/tnn_chat_decline.zag` | plausible but not exercised | decline probe instrument from same authority; not needed for this verdict |
| dialogue.zag | `docs/lab/dialogue/dialogue.zag` | superseded | batch driver only; tnn_chat.zag is its code with an interactive main() |
| R33 continuing-life entry point | `docs/generations/R33/runs/R33_CONTINUING_LIFE_V1/CURRENT_ENTRY_POINT.md` | not runnable as interactive chat | archive infrastructure, no stdin chat loop found in tree |
| any REPL in src/zag | `src/zag/` | missing | directory is empty except INDEX.md; no implementation source there |
| stdin-reading Zag program elsewhere | whole tree grep | none found | no other .zag file implements a stdin line loop |

## Known limits of this instrument (not defects in the survey)

- Closed book: 38 facts, no learning across turns (no new fact acquisition).
- The baseline instrument hallucinates on out-of-KB prompts instead of
  declining (see PROBE_CHAT.md turn 4); the decline variant is the
  knowledge-boundary instrument, not this one.
- Zero RNG, fully deterministic: repeated identical sessions are byte identical.

## Reproduction

All inputs, scripts, logs, and outputs are in `build/` in this lane dir.
Rebuild with the two commands above and compare binary sha256 against the one
recorded here.
