# Arm D — deliberative chunking chooser: design document

**Trial:** native-authorship trial 1 (prereg `docs/lab/native_authorship/PREREG.md`,
frozen commit `50fb8ff86e5a1966eecdc03c829e3b972b055c1b`)
**Author:** implementer subagent, 2026-09-27
**Status:** K5 + K6 verified on the frozen 57-question production battery

## What this is

Arm D replaces the frozen `(kind, shape) -> candidate` lookup with a runtime
**eliminative deliberation** over the same 9 fixed candidates, the same
classifier, and the same executor. The choice is made from **input-derived
evidence** — facts about *this* question and *this* text — by stated
elimination criteria, with a machine-readable trace of every step.

## File layout (this directory)

| File | Role |
|---|---|
| `chooser.zag` | The deliberative chooser + `d_intake` entry. Imports `dlib.zag`. |
| `dlib.zag` | Fixed machinery: `classify`, `text_shape`, the 9 candidates, `cand_answer`, all helpers. = `intake.zag` (at prereg commit) with lines 1775–2062 deleted (the frozen lookup + the production entry) and lookup-name mentions scrubbed from comments. Regenerable: `git show 50fb8ff86e5a1966eecdc03c829e3b972b055c1b:docs/lab/mg_chunking_promote/intake.zag \| sed '1775,2062d'`, then the two comment substitutions. |
| `R33_NATIVE_IO_V1.zag` | Syscall/allocator layer, byte-identical to `docs/lab/mg_chunking_promote/R33_NATIVE_IO_V1.zag` (SHA-256 `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`). |
| `battery_d.zag` | 57-question regression harness. Battery questions byte-verbatim from `battery1.zag`; calls `d_intake`; emits the same `# LIVE SUMMARY` line format. |
| `build.sh` | Build + K5/K6 verification (mirrors production `build.sh`). |
| `evidence/RUN_D1.out`, `evidence/RUN_D2.out` | Two full runs (byte-identical). |
| `evidence/SHA256SUMS` | Run SHAs. |

Build: `cd docs/lab/native_authorship/chooser && ./build.sh` (toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, pinned SHA
`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`).

## The deliberation

Inputs: `(qid, question bytes, text bytes)` only. The expected answer is
forwarded to the executor for scoring exactly as production does; the chooser
never reads it.

### Evidence features (all computed from q/t; zero RNG)

| # | Feature | Meaning |
|---|---|---|
| 0 | kind | `classify(q)`, 0–17 — used as *evidence*, never as a lookup key |
| 1 | shape | `text_shape(t)` — single/multi |
| 2 | nwords | word count of this text (space-split, no table) |
| 3 | nbytes | text length in bytes |
| 4 | nlines | newline count + 1 |
| 5 | lenclass | SHORT <120B / MED <1500B / LONG ≥1500B |
| 6 | ans_unit | what the question asks for: LETTER / WORD / NUMBER / YESNO / TEXT / UNKNOWN (parsed from question vocabulary by priority: backwards → TEXT, contain → YESNO, how many → NUMBER, letter/'s in → LETTER, word → WORD) |
| 7 | count_unit | for NUMBER: count over WORDS / LETTERS / UNKNOWN |
| 8 | addr_depth | 0 = no addressing (whole-text), 1 = one address (first/last/Nth/contain), 2 = nested two-level ("Nth sub-unit of the Mth word of T" — a bare "first/last word of T" addresses the word itself and is depth 1) |
| 9 | edge | question names text edge: FIRST / LAST / NONE |
| 10 | last_anchor | question addresses the last word (`wn == -1`) |
| 11 | needle_hit | for YESNO: is the needle a whole word *in this text* (word-boundary scan, table-free) |
| 12 | relative | "after "/"before " present (relative-addressing vocabulary) |
| 13 | anchor_third | addressed unit's third of the text (start/mid/end), −1 if N/A |

### Elimination stages (fixed order; each fired sub-criterion emits a D-ELIM line)

- **D0** — degenerate guard (in `d_intake`, before deliberation): empty text or
  empty question → `# D-REFUSE`, no candidate runs, packed stats zero.
- **S1 unit filter** — the candidate's native addressable unit must express the
  answer unit. LETTER answers eliminate WORD (word-table addressing; its
  letter paths are out-of-unit fallback work). WORD answers eliminate the
  fixed-byte spans (span boundaries cannot align to word boundaries).
  Spaceless texts eliminate WORD unless the question is about word structure
  (degenerate single-entry table; byte scan dominates).
- **S2 span domination** — SPAN5's 5-byte grid is strictly coarser than SPAN3's
  3-byte grid (span counts cited from this text); no byte-exact answer needs
  the coarser grid.
- **S3 edge filter** — no edge named: END_DIRECT degenerates to its CHAR path,
  dominated by CHAR. Edge named: fixed spans cannot address an edge directly.
- **S4 addressing-depth filter** — depth 2: WORD?CHARSCAN (a contains-then-scan
  mechanism) and BOTH_ENDS (no two-level addressing) are dominated by the
  word→char zoom. Depth 0: end-anchoring buys nothing; REV_WORD is WORD with
  overhead.
- **S5 contains specialization** (YESNO only) — needle is a whole word in this
  text: full-text scans unnecessary, word-try mechanisms suffice. Otherwise:
  word-table lookup cannot hit; sub-word scan required.
- **S6 final selection** — ordered preference rules over survivors (first match):

| Rule | Condition | Winner | Rationale |
|---|---|---|---|
| F1 | named edge + LETTER answer | 9 END_DIRECT | direct O(1) edge read |
| F2 | addr_depth = 2 | 3 WORD>CHAR | word-scale locate, character-scale resolve |
| F31 | YESNO + whole-word needle hit | 4/3/2 | cheap word-boundary try, no scan |
| F32 | YESNO + sub-word needle + LONG text | 6/4/3 | dual-direction scan, nearer end bounds work on a hit |
| F33 | YESNO + sub-word needle | 4/3/6 | word-boundary try, char-span scan on miss |
| F4 | last_anchor | 5 REV_WORD | address from the right |
| F51 | NUMBER + word count | 2/1 | word-boundary mechanism |
| F52 | NUMBER (other) | 1/2 | byte-scan mechanism |
| F6 | WORD answer | 2/1 | word-table addressing |
| F7 | TEXT (backwards) | 1 CHAR | reversal is a byte-order operation |
| F10 | LETTER + single address | 1/3/4 | byte-scan resolves the position directly |
| F81/F82 | kind = 0 (unknown) | 2 if shape=multi else 1 | most general mechanism for this text's structure |
| F9 | — | 1 CHAR | universal byte-scan fallback |
| F0 | survivor set empty (never fires; insurance) | 1 CHAR | — |

Preference lists (e.g. `4/3/2`) take the first *surviving* candidate, so an
eliminated preferred candidate never blocks the rule. F1 deliberately requires
a LETTER edge: on word edges ("first/last word of T") END_DIRECT would only run
its degenerate CHAR path, so the trace never claims a direct read it didn't do.

### Trace format (machine-readable, instrumentation only)

- `# D-FEAT qid=…` — all 14 features.
- `# D-EV qid=… cand=N NAME ev="…"` — ≥1 input-specific evidence item per
  candidate (this text's byte/word/span counts, this question's addressing
  facts), for all 9 candidates on every input.
- `# D-ELIM qid=… stage=… elim="…" reason="…"` — elimination order + reasons.
- `# D-CHOICE qid=… winner=N NAME rule=F… why="…"` — final choice + rule.
- `# D-REFUSE qid=… reason="…"` — degenerate inputs.

The trace emitters only read choice state; all elimination decisions mutate the
`alive` bitmask via `d_kill2`, which performs no output. Blanking the emitters
cannot change any choice (P-trace neuter-safe by construction).

## Anti-lookup argument (for the K4 audit)

1. The frozen lookup is not present in the build: `dlib.zag` deletes it, and no
   source in this directory references it (verified by grep).
2. `kind` is one of 14 features; elimination criteria are stated in terms of
   answer-unit, addressing-depth, edge vocabulary, needle-hit-on-this-text,
   text length class, and text shape — never "if kind = K pick C".
3. Same-kind inputs diverge by non-kind features by design: e.g. two CONTAINS
   questions with the same kind pick different candidates when one needle is a
   whole word of its text and the other is a sub-word needle in a LONG text
   (F31 vs F32); unknown-vocabulary questions (kind 0) pick WORD vs CHAR by
   text shape (F81 vs F82).
4. The chooser's deliberation was validated against the 57Q battery only; the
   fresh trap battery and oracles were never accessed (signed statement in the
   delivery report).

## Verification (K5/K6)

- K5: 57/57 correct, 57/57 native, 0 fallbacks on the frozen battery.
- K6: two runs byte-identical; rebuild-from-source reproduces the run;
  zero RNG on the choice path (grep-clean).
- Degenerate probes (scratch, not committed): empty text → clean refusal, empty
  question → clean refusal, kind-0 novel vocabulary → no crash, 2000-byte text
  → no crash, all deterministic across reruns.

See `K5K6.md` for SHAs.
