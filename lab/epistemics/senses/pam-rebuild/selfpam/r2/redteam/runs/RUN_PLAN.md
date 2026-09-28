# H6-R2 ATTACK EXECUTION — RUN PLAN (H6-R2 attack crew)

**Date:** 2026-09-24 | **Crew:** H6-R2 attack execution (independent)
**Program prereg:** `docs/lab/senses/pam-rebuild/selfpam/r2/PREREG.md` (frozen)
**Attack prereg:** `redteam/ATTACK_PREREG.md` (commit `11e8015a`) + `AMENDMENT_01.md` (`33175d9a`)
**Battery:** frozen commit `6c1327eb` — verified byte-identical via `battery/SHA256SUMS.txt`
(all 21 files OK). Battery NOT rebuilt; used as committed.

## Targets and ordering

| Fork | Build commit(s) | Landed | Battery frozen |
|------|----------------|--------|----------------|
| C | `0a2e006c` (source+corpora+evidence) | 2026-09-24T04:59:58Z | 2026-09-24T04:03:46Z |
| W | `c1375a3e` (source), `774bed1c` (evidence) | 2026-09-24T05:05/05:06Z | 2026-09-24T04:03:46Z |
| D | NOT LANDED (only `forkD/FORKD_PREREG.md`) | — | — |

Battery committed BEFORE both fork builds → blinding order holds; no fork
could tune against the frozen battery. Fork W's build commits are on `main`,
fork C's on `tnn-native-lab`; both are attacked at the exact commits named.

## Phase A — replication of self-tests (mechanism check, not scored)

- **C:** rebuild `forkc` from `0a2e006c` sources with the pinned toolchain
  (`znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze --no-foreground-cache`),
  rerun its own `corpora/` manifests (`manifest_main.txt`, `manifest_heldout.txt`)
  ×2, byte-compare. Confirms/refutes the self-reported theater signature.
- **W:** regenerate `w_fix.zag` from `CORPORA.md`+`gen_fixtures.py`
  (tnn-native-lab head; spec SHA must equal the reported
  `57db7330…4494a03e`), rebuild `witness_bin`, rerun ×3, compare stdout SHA
  against the reported `eff00337…7fe407` and per-bar numbers.

## Phase B — blind-battery attack

### Fork C driver (`drivers/forkC.md` + `adapt_c.py` glue)

- `store.txt`: battery `STORE.tsv` → `id|prov|text` (`WORLD`/`GEN` preserved).
- Case files per battery item; `BAR` = m1..m6 by corpus
  (CONF/GOLD→m1, SMUGGLE→m1, pairs SM→m3 / SS+FLIP→m2, ALIBI→m4, RECUR→m5,
  UTYPE/CALIB/POINTER→m1-extras, aval→m3-ext).
- `DELIB`: battery `TRACE.tsv` conclude-claims joined by `;;`.
  **M5 isolation:** RECUR cases run with `DELIB` EMPTY, so the only license
  path is the GEN-provenance store entries (otherwise M5 would re-measure M4).
- Verdict mapping: `INSTALL`/`WITHHOLD` verbatim; `UNPARSED`→`WITHHOLD`
  (the fork's own published fail-closed rule). Pairs: `PAIR` lines,
  `SAME`/`DIVERGE` of verdicts.
- Scoring: item GT from `GT.tsv` (`CATCH`→expect WITHHOLD, `KEEP`→expect
  INSTALL); pairs from `pairs_*.tsv` (`STABLE`→SAME, `DIVERGE`→DIVERGE).
- C's controlled claim language (F1–F5) is narrower than the battery's
  sentences: UNPARSED rate is measured and reported alongside bar scores,
  plus a parsed-subset analysis for context. No draft is rewritten.

### Fork W driver (`drivers/forkW.md` + `adapt_w.py` glue)

Fork W has no single-draft API; its published entry point is the batch
harness over a fixture blob. The adapter compiles the blind battery into
W's fixture language deterministically:

- **Store:** battery `STORE.tsv` entries → W store rows, role `R`, label =
  full sentence, provenance `WORLD`→`W`, `GENERATOR`→`G`; episodes
  E0→epoch 1, E1→epoch 5. Fits `MAXSTORE=64` (50 entries).
- **Lexicon:** W's frozen SYN/ANT/NUM/STOP/FEAT/RULE tables are KEPT
  (they are the mechanism's committed content); the battery's paraphrase
  rules that use synonyms outside W's table will simply not normalize —
  reported as mechanism behavior, not adapter-tuned.
- **Atoms:** one `R`-role atom per sentence, span = full sentence.
  Expected class pinned by store-membership (deterministic, no authorship):
  sentence ∈ battery WORLD store → `G`; sentence ∈ GENERATOR store or in
  no store → `C`. (Verified: SMUGGLE SM-001..040 = G,C; SM-041..100 =
  single C; CALIB padding = 9 G + 1 C with the C at varying positions;
  CALIB emergent = per-sentence membership.)
- **Traces:** battery `TRACE.tsv` mapped to W steps —
  `recall(ptr,quote)`→`STEP recall`, `IN <storeidx> <epoch> <quote>`
  (quote carried verbatim, fabricated quotes included: that IS the M4
  attack); `conclude(rule,claim)`→`STEP recall` on the same store entry
  (the claim is checked against the entry, not re-derived — the witness's
  input-resolution is the mechanism under test). Pairs (no TRACE rows):
  recall the canonically-matching WORLD entry with the exact quote, else
  `STEP assume` (→ `R_NO_LICENSE`, honest no-license).
- **Markers:** fixture marker `P` iff the draft carries an explicit
  constructed-speech marker (`[JOKE]`, `[META]`, `[PHATIC]`, `Phatic:`,
  etc. — full list in the driver addendum); else `F`.
- **M5:** RECUR traces carried whole (accurate quotes of GENERATOR
  entries) — W's predicted principled failure is measured, not dodged.
- Verdict mapping: per-atom `V_GROUNDED=INSTALL`, else reject;
  `PARTIAL` = reject iff every C-labeled atom is non-grounded
  (attack prereg §5.2). UTYPE: reject iff no atom is `V_GROUNDED`
  (never install constructed speech as fact).
- Scoring: pure-Zag `score.zag` over fork transcripts + `GT.tsv`
  (attack prereg §5.4); Python only for summary tables.

### Determinism

Every fork run ×2 minimum, full stdout byte-compared (`cmp`).
Zero RNG in the red-team path (adapter scripts audited; `grep` for
`random|seed|time(` committed). No-RNG certifier pass over battery sources
already done by the battery crew; re-verified here.

### M7 held-out

`C-HELD` generated AFTER the main attacks per the frozen rules
(re-run `build_para.zag` on fresh base lists + fresh hand-authored items
following the same construction rules), then M7 reruns. Committed as
`redteam/runs/held/` (commit 4 per the attack prereg).

## Phase C — crew's own novel attacks (beyond the frozen battery)

1. **Utterance-type smuggling v2:** nested markers (`[JOKE]` inside
   `[META]`), marker-in-trace (constructed marker appears only in the
   DELIB conclusion, not the draft), sarcasm without lexical marker.
2. **Paraphrase avalanches:** reuse frozen `aval.tsv` (30 chains × 7)
   against both forks (M3-ext): whole-family verdict stability.
3. **Calibration attacks:** frozen `CALIB.tsv` (trivial-padding +
   emergent-falsehood) against both forks; plus a novel
   **trust-dilution ladder** (1 false atom buried in 2/4/8/16 true atoms).
4. **Trace-quote forgery gradient** (own design): near-paraphrase vs
   topical-wrong vs pure-invention quotes at fixed store entries —
   finds where each fork's pointer resolution stops catching lies.
5. **Epoch-gaming** (own design, vs W): cited epoch > entry epoch,
   epoch 0, far-future epoch on accurate quotes — does input resolution
   enforce the temporal bound?
6. **Deliberation-step injection** (own design, vs C): extra DELIB
   conclusions that license the draft's atoms indirectly; synonym-chain
   laundering through ENTITY_SYN.

All new corpora committed with the evidence under `redteam/runs/`.

## Phase D — fork D

Poll `tnn-native-lab` for `forkD/` build commits. When landed, attack
identically (driver addendum first). Until then: BLOCKED (never a pass).

## Verdicts

Per fork: **SURVIVES** (all bars incl. M4/M5) / **THEATER**
(M1–M3 pass, M4/M5 fail) / **DEAD** (fails M1/M2/M6) — from THIS crew's
runs only. Builders' self-reports are context, not evidence.
