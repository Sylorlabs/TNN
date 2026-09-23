# SPEC-SOL: Sol architecture build contract (FROZEN 2026-09-22)

Implements the **Sol** contender from PREREG-SG §2: factorized quorum semantic
index with proof-carrying retrieval. Pure Zag. Zero randomness. Byte-identical
reruns.

## 1. Reuse (read-only)

- `@import("sg_parse.zag")` — the frozen front end (tokenizer, stemmer,
  entity tagger, relation tagger, attitude scanner, coreference threading).
  Do NOT modify it. No other parsing code.
- You may add any new Zag code (index, quorum, proofs, I/O).

## 2. Frame extraction (per sentence, deterministic)

For each teach line in file order:
- Reset `peid = 4294967295` at line start; thread across sentences within the
  line (after each teach sentence, `peid = eid` if `eid != 4294967295`).
- Split sentences on bytes `.` `?` `!` (46/63/33), exactly like the reference.
- Call `prep_sentence(..., is_probe=0, mode=2, ppn=0, ppn_n=0)` per sentence.
- Frame fields from `sctx`/`relbuf`/`cpos`/`tsuid`:
  - `subj` = `g64(sctx,64)`; skip sentence if `== 4294967295`.
  - `pred` = sorted deduped set of `g32(relbuf,k*4)`, `k < g32(sctx,44)`.
  - `pol` = `g32(sctx,72)` (0 asserted / 1 hedged / 2 negated).
  - `vok` = `g32(sctx,80)`, `val` = `g64(sctx,88)`; skip sentence if `vok=0`.
  - `lex` = sorted deduped set of `g32(tsuid, cpos[k]*4)`, `k < g32(sctx,4)`.
- Probes: same, with `is_probe=1`; `peid` threads across probe lines
  (no coref trigger occurs in probes; harmless).

## 3. Install (index build)

- Rows stored in install order (index 0,1,2,…). Keep per row:
  `pred` (≤8 uids), `subj`, `pol`, `val`, `lex` (≤16 uids), `dead` (0/1).
- Contradiction rule: when installing a row with `pol=0`, if a **live** row
  exists with equal `pred`-set, equal `subj`, `pol=0`, and different `val`,
  mark **both** rows dead. (Identical duplicates are not contradictions.)
- Rows with `pol≠0` are stored but never yield VALUE.

## 4. Retrieval (per probe)

1. If `subj == 4294967295` → `UNKNOWN` (proof: `no_entity`).
2. Candidates = **all** rows (live or dead) with `pred`-set **equality**
   (sorted-set equality) to the probe's `pred`.
3. Quorum per candidate: `pol` equality **and** at least 2 of:
   - subject-equal (`subj` equality),
   - object-equal — **vacuously true** when the probe posits no object
     (`vok=0`, i.e. every probe in this battery),
   - lexical overlap: rational cosine ≥ 1/2, i.e.
     `2·inter² ≥ |A|·|B|` with `inter = |probe.lex ∩ cand.lex|`,
     `A = probe.lex`, `B = cand.lex` (pure integer arithmetic).
   (With the vacuous object factor, this reduces to
   `pred-eq ∧ pol-eq ∧ (subject-eq ∨ lexical≥1/2)` for this battery.)
4. If any quorum-passing candidate is dead → `CONTRADICTION`.
5. Else if any quorum-passing live candidate → `VALUE:<val>` of the
   lowest install index among them.
6. Else → `UNKNOWN`.

## 5. Output

- argv: `sg_sol teach.txt probe.txt`.
- stdout: one line per probe, `id\tVALUE:<val>` | `id\tUNKNOWN` |
  `id\tCONTRADICTION`, probe-file order, **nothing else** on stdout.
  `<val>` = decimal integer (`prn`).
- `proof_sol.txt` in CWD, one `id\t<trace>` per probe, deterministic:
  `SOL cand=<pred-eq count> quorum=<passing count> subj=<0/1> obj=<0/1>
  lex=<0/1> dead=<0/1> verdict=<V>`
  (`subj/obj/lex` = factors of the chosen candidate, or `0/0/0` when none;
  `dead=1` when the verdict came from a dead candidate.)
- Tie-breaks: lowest install index. No RNG, no clock, no pointer-derived
  output. Fixed-size global tables (≤2048 rows is plenty).

## 6. znc lessons to respect (from workspace AGENTS.md)

- Zero every arena/counter header explicitly before use.
- Never name a function `zalloc`; never `nio_free` a `_zag_arg` pointer;
  `argc` is always 0 — read `_zag_arg(n)` unconditionally.
- No `==` on slices; no `};`; flatten else-nesting past 4 levels.
- Avoid consecutive same-size `as []i32` casts (miscompile); prefer `[]u8`
  arenas with explicit little-endian u32 accessors for tables.

## 7. Acceptance before freeze

- Builds clean with the pinned toolchain
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
- 5 runs on `gen/calib/` byte-identical: SHA256(stdout) and
  SHA256(`proof_sol.txt`) equal across runs.
- Sanity: every `canon` calib probe should return its taught value
  (the builder may check this; the scored answers stay sealed).
