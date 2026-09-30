# FREEZE: C1 simple baseline implementations

Date: 2026-09-30 UTC
Status: FROZEN (committed alone; prereg 26937cb55 strictly precedes).

## Sources and binaries

| File | SHA-256 |
|------|---------|
| mem.zag | 5d3070e0f515ec2e4213fdb2562310e4e3fad0d3c94837415ec64a168725f224 |
| freq.zag | f0f3d287dba731a31d74717b661e4858d200a1642185af5109a4d4bcc977edb6 |
| rand.zag | 8ce39a1c7270ba027daf69664aaee75fa4920452b20c082ab8c373707e0c6367 |
| mem_bin | aad8d533e52fd969723742ba09aad6c6110c4a571d84c6d2b26a2e732f78216a |
| freq_bin | 59a0e7ae7ec44aa3010693d9245e49a05817150dfc94a2b27df73a9f39458e44 |
| rand_bin | 0d562d69fe516e4f5f6df95108f61f86dd939a18898b2ab09e69866f57152fd7 |

Compiled with the pinned znc (src/tools/toolchain/znc_linux_x86_64_abed8aa1).
Compiler warnings A0101 (findsub) and A0107 (w_write) are the same
patterns as the frozen contestant.zag; behavior verified by smoke
test, not by warning count.

## Smoke tests (pre-freeze, on w0 turns)

- mem: obs fact of|pzf|xi stored; query A1 attr of/pzf answered "xi".
- mem: query B1 (chain) answered ""; act turn answered {"done":true}.
- freq: query A1 answered "xi" (sole observed value).
- rand: query A1 answered "xi" (sole vocab entry, deterministic).

## Interface contract (matches run_race.sh)

- argv: <turn.json> <statedir>. One JSON reply line on stdout.
- obs fact: update state.txt. query attr: "answer" from the
  baseline's rule. query other: "answer":"". act: {"done":true}
  (no tool use). brief/save/load/end/toolresult: {"ack":true}.

## What is frozen

The three .zag sources, the three compiled binaries, and this file.
The results phase runs these exact binaries against the frozen
worlds (e0a30377f) via the frozen driver (b8d38d9c8 run_race.sh).
No source changes after this commit.
