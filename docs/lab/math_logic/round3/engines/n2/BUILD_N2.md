# BUILD_N2.md — N2 native build record (MATH R3)

## Source
- `n2.zag` (pure Zag, zero RNG; single source file, no imports beyond the
  deliberation-depth harness util `dlb_util.zag` resolved via include path)

## Toolchain (pinned)
- `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Build command (from `math_logic/round3/engines/n2/`)
```
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 n2.zag \
  --no-zagd --no-analyze --no-foreground-cache -o n2_bin
```
- Result: `znc: wrote native binary n2_bin (194884 bytes main, 0 external tools)`
- Binary SHA-256: `97ef61681baf750bc67bffc2c482f7d44475551bbf323788f755ce0d2c814a6f`
- `n2_bin` is a build artifact and is NOT committed (sources-only commit).

## Knowledge store (pinned default)
- Path (relative to engine CWD): `../../batteries/knowledge/KNOWLEDGE_STORE_NL.md`
- Absolute: `~/workspace/tnn-lab/math_logic/round3/batteries/knowledge/KNOWLEDGE_STORE_NL.md`
- The brief's anticipated path `round3/batteries/KNOWLEDGE_STORE_NL.md` does not
  exist on disk; the landed R3 NL store is under `batteries/knowledge/`.
- Repo commit: `db913da907d0` (tnn-native-lab, reported by coordinator 2026-09-25)
- SHA-256: `910ea9da0989e113587a3856583ba1ec1ea8b4f59258ab3374f1b17b9220084a`
- Format: `[Kddd] (kind)` header lines followed by body lines; the parser reads
  the kind from the header (`(definition)` sets the definition bit) and cites
  body-only spans (the `[Kddd] (kind)` header is citation metadata, cited via
  the item id, not part of the cited text).

## Invocation
```
./n2_bin <problem.txt> <output.txt> [store_path]
```
- Two-arg form uses the pinned default store above.
- Exit 0 on success, 3 on any sealed path (input, output, or store), 4 on I/O
  or determinism failure.

## Smoke results P01–P03 (R2 raw-NL problems, default store)
| Problem | Verdict | Derivations | Flags | Output SHA-256 |
|---|---|---|---|---|
| P01 | WITHHELD | 0 | NONE | 85dc6b7a367bd9f48a2723d8c1bf25835f2d2800498ece0b037fd5cdbe7238ce |
| P02 | WITHHELD | 0 | NONE | 45c4153af112334fe3f7b7faebadd47de74b457e987bb6bb3924a28cccb3bd73 |
| P03 | WITHHELD | 0 | NONE | 6a8450e081c9ea2071339d01e50a548a5a4b840a8d0239cdff4dc1ad56be09f5 |

All three honestly WITHHELD: these R2 problems state a goal with no
marker-based ("because"/"since"/"therefore") reasoning chain in the problem
text and no definitional containment path that survives the polarity and
contradiction checks. The engine withholds rather than inventing support.

## Determinism
- Internal: every run performs a 3× in-process byte-identical self-check over
  the full output buffer before writing; any mismatch exits 4. All runs above
  exited 0.
- External: each of P01–P03 and each synthetic test below was run 3× as
  separate processes; all outputs byte-identical (`cmp` clean) across runs and
  against the recorded outputs.

## Synthetic mechanism tests (non-sealed, hand-written)
| Test | Mechanism exercised | Verdict | Result |
|---|---|---|---|
| since | `Since Y, X` marker + GIVEN bottom-out | DERIVED | X←Y←problem premise, 2 links |
| because | `X because Y` marker + GIVEN bottom-out | DERIVED | X←Y←problem premise, 4 trace links |
| therefore | `Y. Therefore X.` marker + previous-sentence Y | DERIVED | X←prev sentence←premise, 2 links |
| def | P_DEF definitional containment via K104 (Congruence) | DERIVED | goal←[K104], 1 link |
| contra | contradictory problem premises + K103 polarity-flip refutation | REFUTED | negated candidate←[K103], CONTRADICTION_FOUND |
| weak | 4+ competing supports → weak links → kill at 2 | WITHHELD | C0 status=weak_kill |

All six give the intended verdict; all are 3× byte-identical externally.

## Sealed guard
- Input path containing `sealed` → exit 3 (`n2: sealed guard tripped on path`).
- Output path containing `sealed` → exit 3.
- Tested with path strings only; no sealed content was opened or read.

## Mechanism simplifications and limitations
1. **Overlap is word-level (≥4 non-stop words), not byte-level.** The brief says
   "≥4 non-stop bytes"; the implementation counts distinct non-stop WORDS.
   Mechanism reason: byte-overlap without word boundaries matches substrings
   across word edges ("even" inside "seven"); word-granular hashing is the
   minimal unit that keeps overlap semantically grounded. Conservative
   direction: word-level is stricter than raw byte overlap.
2. **Polarity is fixed-marker parity over the whole span.** Markers: not, no,
   never, neither, none, without, n't, cannot, false, impossible, fails,
   denies, refutes, contradicts. Mechanism reason: bounded byte-only
   processing has no clause scope, so polarity cannot be localized around the
   overlap region; span-level parity is the conservative choice (may miss
   genuine contradictions inside long spans, never invents them).
3. **Stop list is closed-class function words; numerals are content.**
   "one"/"two" were removed from the inherited stop list: in mathematical
   text number-words are content-bearing ("two even integers"), and the
   list's own contract is "closed-class function words only".
4. **Definition expansion replaces the first matching raw head occurrence**
   in deterministic head order (16 heads parsed: K101–K109; K110's
   parenthetical head "(finite, equally likely outcomes)" is not recognized —
   the walker stops at the comma, a known under-derivation).
5. **The `therefore` Y is the immediately previous problem sentence.**
   Problem premises are sentence-granular items, so the marker's own item is
   too narrow to hold Y; the lookback uses the previous problem sentence's
   existing span. No text is generated.
6. **Refutation reuses the cited conclusion span** plus a polarity/refutation
   flag rather than generating negated text, respecting the "existing spans,
   no output templates" rule.
7. **Contradiction scan skips store-vs-store pairs.** The store is the authored
   consistent background theory; pitting definitions against each other only
   measures shared vocabulary (e.g. K102/K103 share "prime number integer 1"
   with a local "not"), never genuine inconsistency. Only
   conclusion-vs-cited and problem-premise-vs-cited pairs are enforced.
8. **P_DEF requires ≥2 key terms in the current span.** A single shared word
   (e.g. a variable fragment from " and "-splitting) licenses vacuous
   definitional links; the bound keeps definitional support non-degenerate.
9. **Conjunct splitting on "," / ";" / " and " is purely syntactic.** It can
   fragment mathematical expressions ("the sum of 2a and 2b ..."), producing
   fragment links in the trace. Verdicts are unaffected (all fragments must
   still bottom out), but traces may show sub-claim links.
10. **Custom H5-style weakest-candidate elimination** rather than formal H5
    hypothesis structures, to stay on the native side of the anti-bridge line:
    no typed semantic variables, no formula grammar, no unification.

## Bugs found and fixed during this build
- Visited-set cycle check compared the current span against all visited
  entries including itself → every candidate died at depth 0. Now checks
  ancestors only (`vn-1`).
- Term-array slice used the u64 entry index as a byte offset
  (`ka[toa..]` instead of `ka[toa*8..]`) → P_DEF/P_GIVEN/shared silently read
  misaligned hashes for every item after the first. Latent: never fired
  before because no support path had ever succeeded past item 0.
- `(definition)` kind detection ran on the trimmed header line, but the
  trimmer strips boundary parens → the `)` was eaten and zero definitions
  were detected. Now checked on the untrimmed line.
- Default store path had one `..` too many (`../../../` → `../../`).

## Commit
- Sources-only: `n2.zag`, `BUILD_N2.md` under `math_logic/round3/engines/n2/`.
- Excluded: `n2_bin`, `.zag-cache/`, `.zagd.semantic-ready`.
