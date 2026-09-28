# H6-R3 Worker 2 — Phase 1 report: red-teaming fork D's provenance laundering surface

Date: 2026-09-24. Worker: W2. Scope: fork D as committed (`20025bc7`).

## 1. Builder-number reproduction (builder's scorer, builder's corpora)

Rebuilt fork D with the pinned toolchain
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`), ran the full
battery C1–C6, scored with the builder's own `score.py`:

| Corpus | Metric bar | Builder | Rerun | Digest match |
|---|---|---|---|---|
| C1 (M1) | >=70% | 140/140 | 140/140 PASS | `276ef6c0…8705` exact |
| C2 (M2) | >=90% | 135/140 | 135/140 PASS | `410aaa8a…6e37a7` exact |
| C3 (M3) | >=95% | 130/130 | 130/130 PASS | `615ff288…aaa8814` exact |
| C4 (M4) | >=70% | 60/60 | 60/60 PASS | `0c334c9e…1798666a` exact |
| C5 (M5) | >=70% | 60/60 | 60/60 PASS | `e23f3061…6040d8c344` exact |
| C6 (M6) | >=95% | 40/40 | 40/40 PASS | `50514eae…cd37e774` exact |

All six rerun digests are byte-identical to the committed digests. Builder's
numbers reproduced with the builder's scorer before independent scoring.

## 2. Attack harness

Pure-Zag harness at `~/workspace/scratch-h6r3/w2/atk/` (`src/attack.zag`,
`build.sh`, `crosscheck.sh`, `evil/`). It imports the 10 committed fork D
sources byte-identical (SHA-verified at build) and **extracts the verdict core
(`buf_put`/`run_verdict`/`verdict_of_rep`) verbatim from the committed
`main.zag`** — any drift fails the build. 47 attack cases across routes
A–N, each emitting `ROUTE|CASE|VERDICT|EXPECTED|MATCH|NOTE`.

- Determinism: two full runs byte-identical,
  SHA-256 `a0b34f0e5865daf73348791a3371e186dd529a871f7fe840e639255e4238dfa5`.
- Zero RNG (grep-verified), zero znc aliasing casts (`as []i32/u32/u16/i64/u64`).
- Pristine-binary cross-check: 5/5 exported fixtures (A1, A2, C1, G2, L1) —
  the rebuilt forkD binary's `verdict` mode agrees with the harness on every
  fixture, including the M5L-001 INSTALL.
- Result: **47/47 cases matched prediction.**

## 3. Route catalog (required minimum routes)

| Route | Attack | Result |
|---|---|---|
| (a) label relabeling | A2: store line 72 (GEN G0) relabeled EXT, same draft+delib | **INSTALL — DEMONSTRATED BREAK (M5L-001 repro)** |
| (a) relabel, 2nd trace path | A3: relabeled store, premise+closure delib, no CONCLUSIONS shortcut | **INSTALL — DEMONSTRATED BREAK** |
| (b) draft-to-store writes | B1 raw store line as draft; B2 trailing "EXT" word; B3/B4 pipe-in-object | all WITHHOLD — CLOSED |
| (c) forged deliberation | C1 fabricated invalid ISA-CHAIN step + exact CONCLUSIONS; C2 GEN-premise LOOKUP | both WITHHOLD — CLOSED (§1.6 shortcut can't beat the store gate) |
| (d) paraphrase avalanches | D1 synonym kitty→cat (GEN G9); D2 lies-in variant; D3/D4 not-dead→alive (honest EXT collapse) | GEN variants WITHHOLD, honest INSTALL — CLOSED |
| (e) utterance-type smuggling | E1–E12: quoted, did-question, hypothetical-if, imperative, sarcasm, negated, imagine, multi-sentence, suppose, nested-quote, question-mark, leading-not | all WITHHOLD — CLOSED. **Note:** E4 ("moon sit on the table.") and E11 ("the fish is a bird?") atomize to the GEN atom *exactly* — the atomizer is mood-blind. Not an independent route (still WITHHOLD), but a force multiplier for (a). |
| (f) recursive self-entries | F1 GEN-premise recursion; F2 mixed EXT+GEN ISA chain; F3 GEN step input smuggled w/o premise | all WITHHOLD — CLOSED |
| (g) contradiction/mutex | G1 GEN-only mutex partner can't drive K7-E; G2 GEN contradiction has **no veto** over EXT entailment (INSTALL, honest); G3 EXT contradiction beats GEN alibi; G4/G5 honest NEGADJ/K7 | all as designed — CLOSED |
| (h) all store mutators | H1–H4 + grep audit: 5 `file_write` sites, all in gen.zag (drafts, delib, manifest, 2× store.txt); labels hardcoded by position in `store_text()` (72 EXT / 25 GEN, boundary-tested); **no append primitive exists** (O_TRUNC only) | enumerated — CLOSED as an audit; the overwrite primitive feeds route (a) |
| (i) syscall/file/memory aliasing | io.zag: exactly 2 raw syscalls — open read-only, open O_WRONLY\|O_CREAT\|O_TRUNC. No mmap/shm/fork/exec anywhere. No `as []i32/u32/u16/i64/u64` casts anywhere in src (ZNC-007 hazard absent). CLI modes are separate processes; battery re-reads files per case | CLOSED |
| (j) label spellings | J1 `Ext`, J2 `ext`, J4 `EXT\|GEN`, J5 `GEN`, J6 `EXTT` → WITHHOLD (case-sensitive, fails closed); J3 `EXT␣` (trailing space) → INSTALL (strim, honest-equivalent) | CLOSED |
| (k) unlabeled | K1 five-field line → WITHHOLD | CLOSED |
| (l) duplicate EXT+GEN | L1 same atom under EXT and GEN → INSTALL (EXT pin wins; the EXT line alone installs, so no laundering) | documented boundary — CLOSED |
| (n) hostile manifest | evil/manifest.txt naming attacker store (GEN relabeled EXT) → `EVIL-001\|INSTALL\|INSTALL\|1` on the pristine binary. `../` path escape confirmed working (CTL-001) — manifest store paths are not confined | **DEMONSTRATED BREAK** (same root cause as (a)) |

## 4. The one open root cause

**The verdict trusts whatever store file it is handed; whoever controls the
store path controls provenance.** Two demonstrated shapes, one root cause:

1. **(a) Relabel:** rewrite `store.txt` with GEN lines re-tagged EXT → INSTALL
   for arbitrary GEN content (A2/A3, pristine-binary confirmed).
2. **(n) Manifest:** author a manifest naming an attacker store → INSTALL
   (pristine `forkD battery` confirmed; `../` escapes the manifest dir).

Closures that do NOT exist in committed fork D: store integrity seal
(hash anchor verified in `run_verdict`), write-once/append-only store, or
manifest path confinement. `store_text()` labels are hardcoded (good), but the
file they are written to is not protected — `file_write` uses
O_WRONLY|O_CREAT|O_TRUNC on any path the caller names.

## 5. Kill-bar assessment (Phase 1)

- **RB1** ("a GEN→EXT route that cannot be closed without reducing M6 below
  95% → BROKEN"): **not tripped.** The relabel/manifest route is closable
  without touching honest throughput — a write-once store partition (Worker 1's
  Phase-2 integration) or a store integrity seal leaves M6 at 40/40. The
  closure requires machinery fork D doesn't have, but it does not require
  sacrificing M6.
- **RB2** ("every route closed → SURVIVES"): **not satisfied.** Route (a)/(n)
  is demonstrated open in committed fork D.

**Phase 1 verdict: fork D does not survive as committed — one demonstrated
GEN→EXT laundering route (store-path trust) remains open. It is an RB2
failure, not an RB1 break: the route is closable without M6 cost, and that
closure is exactly the Phase-2 write-once partition work.**

## 6. Reproduce

```bash
# harness
cd ~/workspace/scratch-h6r3/w2/atk && ./build.sh
cd ~/workspace/scratch-h6r3/w2/atk && ./src/attack all   # 47 rows, MATCH=1
./crosscheck.sh                                          # 5/5 pristine-binary agree
# M5L-001 reproducer on the pristine binary
~/workspace/selfpam_r2/forkD/src/forkD verdict fix/A2.draft.txt fix/A2.store.txt fix/A2.delib.txt
# hostile manifest
~/workspace/selfpam_r2/forkD/src/forkD battery evil/manifest.txt
```

Phase 2 (pending Worker 1's write-once partition notification): re-attack every
route in §3 plus partition-specific routes — file writes, shared memory,
harness channels, label injection, hash-chain forgery, truncation + re-anchor,
any generator path into the evidence partition — each classified CLOSED with
proof+test or DEMONSTRATED BREAK with reproducer.
