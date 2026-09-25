# N4 ANALOG-NATIVE — build record

Date: 2026-09-25. Engine dir: `math_logic/round3/engines/n4/`.
Brief: `math_logic/round3/briefs/BRIEF_N4.md`. Frozen spec: `math_logic/round3/IDEAS_ADDENDUM_R3.md`.

## What it is

N4 is analogical case-based reasoning over raw text, pure Zag, zero RNG.
RETRIEVE ranks the frozen case library by deterministic 4-gram byte
multiset cosine^2 (exact i64 arithmetic, tie-break by case id), tries the
top 3. ALIGN finds longest common 4-gram chains (deterministic greedy)
between current and case problem bytes. ADAPT substitutes problem-ID bytes
and alignment-map spans into each case-trace step in order. VERIFY matches
each adapted step against NL knowledge-store items through four frozen
surface idiom recognizers (MP / CONTRA / LEMMA / BICON) used ONLY as
verifiers, never generators. Unverified steps are dropped along with all
dependents (CITES[STEP k]); if the surviving chain reaches the goal
skeleton the engine derives, else it withholds. Withholding is the default.

## Pins

- Toolchain (pinned): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Knowledge store (pinned per brief): the R3 NL store landed 2026-09-25.
  - Path: `math_logic/round3/batteries/knowledge/KNOWLEDGE_STORE_NL.md`
  - Commit: `db913da907d0` on `tnn-native-lab`
  - File SHA-256: `910ea9da0989e113587a3856583ba1ec1ea8b4f59258ab3374f1b17b9220084a`
  - Embedded as `store_data.zag` (`N4_STORE_BYTES`); also accepted via argv[3].
  - Parser accepts the R3 `[Kddd]` header format (claim text on following
    lines) and the legacy `Kddd <text>` line format.
- Sealed batteries: never read. Binary exits 3 if any input path contains
  "sealed" (verified: no file opened, no output written).

## Case library (frozen renderer)

- Renderer `render.zag` reads ONLY public `traces/TRACE_P01..P22.txt` and
  public `problems/P01..P22.txt`. Guarded against sealed paths.
- Output: `cases/C01..C22.txt` + `cases_data.zag` (embedded Zag consts).
- Renderer is deterministic: re-run reproduces all files byte-identically.

## Spec simplifications (documented, mechanism-level reasons)

1. **22 cases, not 40.** Only 22 qualifying public traces exist
   (`TRACE_P01`–`TRACE_P22`). Duplicating traces or inventing cases would
   fabricate evidence, so the library holds 22 distinct cases. Recorded
   here instead of silently.
2. **Every public trace is deliberative and ends WITHHELD** (`ANSWER:
   WITHHELD`, `deliberative_verdict`); none contains `S_MP`, `S_PBC`, or
   `S_UI` schema derivations. The case library therefore cannot honestly
   supply verified derivation steps, and the engine withholds on P01–P03.
   This is the correct behavior, not a failure: the verifier dropped all
   240 candidate steps (3 cases x 80 steps) on every problem.
3. **Span substitution is byte-preserving by construction.** ALIGN finds
   byte-identical common spans, so substituting case-span bytes with
   current-span bytes replaces bytes with identical bytes. The only
   effective adaptation on this library is problem-ID substitution
   (P01->P0X). This vacuity is inherent to byte-identity alignment, not a
   deviation; analogical transfer through this alignment cannot move
   content, which is part of why the engine withholds.
4. **Idiom licenses under the R3 NL store:** MP@[] (the frozen "=>"
   surface does not appear in the R3 NL K005 wording), CONTRA@[K005],
   LEMMA@[K001,K202], BICON@[]. The recognizers are frozen; licenses are
   whatever the store's actual bytes contain.
5. **Bug found and fixed by positive test:** the CONTRA verifier had two
   off-by-one literal offsets (`p0+13` for 12-char "if assuming ",
   `p1+34` for 33-char " leads to a contradiction, infer "), which made it
   reject a valid contradiction step. All four matchers now pass positive
   and negative unit tests (scratch `zz_test`, removed after).

## Build (exact commands, cwd = engines/n4)

```
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 \
  render.zag --no-zagd --no-analyze --no-foreground-cache -o render_bin
./render_bin                      # writes cases/ + cases_data.zag
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 \
  n4.zag --no-zagd --no-analyze --no-foreground-cache -o n4_bin
```

Binary SHA-256: `002d3222a683d3d178510ecabd89a86f7d748b55d6f8c7b36b806385af421a1f`

## Smoke results (2026-09-25)

| Problem | Verdict | 3x external reruns | 3x in-process reruns |
|---------|---------|--------------------|----------------------|
| P01 (sqrt(2) irrational) | WITHHELD | byte-identical | byte-identical (exit-5 gate armed) |
| P02 (primes 4k+3) | WITHHELD | byte-identical | byte-identical |
| P03 | WITHHELD | byte-identical | byte-identical |

Audit excerpts (P01): `knowledge-store: embedded items=25
idiom-licenses: MP@[] CONTRA@[K005] LEMMA@[K001,K202] BICON@[]`,
`goal-skeleton: the square root of 2 is irrational.`, `TOP3: C21 C17 C16`,
each case `survived 0/80 goal not reached -> CASE FAILS`,
`ANSWER: WITHHELD`.

Sealed-guard: `./n4_bin <sealed problem> <out>` -> exit 3, "sealed guard
tripped on problem path", no output written. Same for sealed store path.

## Commit

Sources committed via `~/workspace/commit_racefree.py` to branch
`tnn-native-lab` (binaries, `.zagd`, and `.zag-cache/` excluded).
Commit: `74787890596eb843e00c77e8e05d63bb6bde3dc0`
