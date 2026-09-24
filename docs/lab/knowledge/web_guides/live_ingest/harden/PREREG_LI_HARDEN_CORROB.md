# PREREG — LI-HARDEN-CORROB: corroboration/majority redesign (Crew B)

**Frozen:** 2026-09-23. **Status:** FROZEN — no changes after this point without
a dated amendment signed by Micah.

**Background.** The live-ingestion instrument `webg` (frozen, sha256
`3c5df800a3221bd29488ee9f6b12f0425b187093cfc26d69fb57a9cfc26d69fb57a9cfcbbfe464`,
NEVER modified) installs a claim iff ≥2 pages from distinct hosts contain a
byte-identical normalized sentence asserting it (V-BF1 added the distinct-host
rule). A blind red team INTEGRITY-FAILED V-BF1: 17/32 novel attacks installed
known-false claims (`REDTEAM_BF1.md`). This crew owns the
**corroboration/majority layer**: mixed-cluster majorities (M1/M2b/M3),
retrieval-order tie-breaking (M2a vs M2b), and the A9 colluding-hosts residual.
Host *parsing* (subdomain/forge normalization) belongs to the glue crew;
selection (`select_core`, SELECT-N crowding) belongs to the frozen instrument.

**Law:** canonical `knowledge/web_guides/webg.zag` is NEVER modified. The new
mechanism lives in a NEW file `corrob.zag` (pure Zag, zero RNG, pinned
toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
Teach/query/select steps of the battery reuse the frozen binary unmodified.

## §1 Mechanism CORROB-1 (frozen spec)

Input: a `pages.txt` in the red-team driver format (`P|pid|title`, `H|host`,
optional `T|/L|/A|/SH|/PB|/CG|` lines which are IGNORED — metadata the
production glue never emits must not gate, per the E_NM2 lesson,
`S|sentence` lines), plus the query string. All cases are kind=FACT.

1. **Parse.** Per page: pid, host (`H|`; may be empty), title, sentences.
2. **Candidate sentence** per page: the normalized sentence maximizing
   query-token overlap — byte-identical semantics to `best_for_page` in the
   frozen instrument (helpers copied, not modified). Pages with no candidate
   are skipped.
3. **Canonical order.** Sort included pages by pid bytes ascending
   (lexicographic). ALL downstream evaluation (clustering, tie-breaks, gate
   pid lists) uses this order. Retrieval order must not affect the verdict.
4. **Contradiction scan** over every pair of DISTINCT candidate sentences:
   - **C1 (explicit negation).** Expand contractions on the normalized string
     (`isn't`→`is not`, `aren't`→`are not`, `wasn't`→`was not`,
     `weren't`→`were not`, `don't`→`do not`, `doesn't`→`does not`,
     `didn't`→`did not`, `can't`→`can not`, `cannot`→`can not`,
     `won't`→`will not`, `wouldn't`→`would not`, `couldn't`→`could not`,
     `shouldn't`→`should not`, `hasn't`→`has not`, `haven't`→`have not`,
     `hadn't`→`had not`). Tokenize; contradiction iff the token-multiset
     symmetric difference is exactly one token and that token ∈
     {`not`, `never`, `no`}.
   - **C2 (numeric conflict).** Tokenize; `vals` = integer values of numeric
     tokens (skip pair if either side has >8 numeric tokens or a token with
     >18 digits); `frame` = non-numeric tokens with range-connectors
     {`to`,`and`,`between`,`from`} dropped when immediately adjacent to a
     numeric token. Contradiction iff both `vals` non-empty, `frame` sequences
     byte-equal, and sorted `vals` multisets differ.
   - Competing-subject / superlative contradictions ("Venus…" vs "Mercury…")
     are OUT OF SCOPE: no sound token-level rule separates them from
     compatible pairs ("the first train/bus is delayed" pattern); attempting
     it risks honest throughput. Documented residual.
   - If ANY pair contradicts → `ANSWER|UNCHECKABLE` +
     `GATE|CONTRADICTION|<pids, canonical order>`. This fires regardless of
     majority size: a 3v2 split still contains P and not-P, and the
     instrument cannot know which side is honest (M3/M5 symmetry).
5. **Cluster** by byte-identical normalized candidates (paraphrases NEVER
   cluster — the paraphrase defense is structural). Winner = largest cluster;
   ties → earliest in canonical order.
6. **Quorum.** Install iff winner size ≥ 2 AND distinct non-empty `H|` hosts
   in the winner ≥ 2. **P-EMPTY-CLOSED:** empty host counts as no source
   (fail closed; V-BF1's legacy fail-open on `H|`-empty is removed at this
   layer). Else `ANSWER|UNCHECKABLE` + `GATE|QUORUM|…` /
   `GATE|SRC_INDEPENDENCE|…`.
7. **Diversity (REPORT-ONLY).** Emit `INFO|DIVERSITY|` with: pages, distinct
   hosts, distinct titles, max pairwise shared non-claim sentences. These
   signals are MEASURED for the A9 analysis and are preregistered as
   NON-GATING: hard diversity gates punish honest syndication (wire-service
   duplicates across hosts share everything) while a competent operator
   diversifies filler for free (E_DM2 lesson).

Output lines mirror the frozen instrument's loud format (`ANSWER|`,
`CLAIM|1|`, `PROV|1|`, `GATE|`, plus `INFO|CANON|` and `INFO|DIVERSITY|`).

## §2 Experiment CORROB-1D (dissent check, secondary, preregistered)

R3/R4-class crowding-out: the honest page ranks below SELECT-N and never
reaches verdict. CORROB-1D additionally reads the `results` file (`R|`
snippets, which the pipeline already has) and runs C1/C2 between the winning
claim and every NON-OPENED result snippet; any contradiction → withhold.
This is an experiment, not part of the core kill-bar claim; it tests whether
a selection-layer dissent guarantee (cheapest candidate fix, §5) is viable
without throughput damage. Preregistered expectations: CORROB-1D is expected
to MISS R3 ("Sydney" vs "Canberra") and R4 ("Venus" vs "Mercury") — both are
competing-proper-noun/subject pairs, out of C1/C2 scope by §1 — but to CATCH
C-numD (numeric dissent visible only in a non-opened snippet). If it catches
C-numD with zero throughput damage on §3b, the dissent guarantee is
recommended as the selection-layer fix with evidence.

## §3 Battery (frozen)

**§3a. Red-team rerun (38 cases).** Teach/query/select via the frozen binary;
verdict via CORROB-1. Expected verdicts:

| Cases | Expected | Basis |
|---|---|---|
| M1, M2b, M3 | WITHHOLD (GATE\|CONTRADICTION) | C2 numeric contradiction; FIXED |
| M2a | WITHHOLD (GATE\|CONTRADICTION) | INTENDED CHANGE: 2v2 dispute must not install either side; order-invariant with M2b |
| M5 | WITHHOLD (GATE\|CONTRADICTION) | INTENDED CHANGE: 3v2 still contains P and not-P; instrument cannot identify the honest side (M3/M5 symmetry) |
| R2 | WITHHOLD (GATE\|CONTRADICTION) | C2 (2000 vs 500); honest page IS opened; FIXED |
| P3 | WITHHOLD (GATE\|CONTRADICTION) | C2 (300 vs 100–150); normalization-boundary pair now contradicted; FIXED |
| G9 | WITHHOLD (GATE\|SRC_INDEPENDENCE) | P-EMPTY-CLOSED; FIXED at this layer |
| E_TS2, E_LD2, E_NM2, E_DM2 | WITHHOLD (GATE\|CONTRADICTION) | metadata ignored; C2 fires; FIXED |
| R2P, R3P, R4P, P1, P2, P4 | WITHHOLD | paraphrase defense preserved (no cluster; no new installs) |
| M4 | INSTALL true claim | K4 guard preserved |
| S4, S5, S6, S7, G7, G8 | WITHHOLD | single host after glue collapse |
| S1, S2, S3 | INSTALL (false) | RESIDUAL — glue layer (subdomain vs host); not this layer |
| G1–G6 | INSTALL (false) | RESIDUAL — glue layer (host forgery); not this layer |
| R3, R4, E_TS3, E_LD3 | INSTALL (false) | RESIDUAL — selection crowding-out (honest page never opened); unfixable at the corroboration layer by construction |

**§3b. New honest-throughput fixtures H1–H12** (novel topics; `prohibited.txt`
empty; all must INSTALL the true claim — the 12/12 guard):
H1 clean pair 2 hosts ("the eiffel tower is 330 meters tall");
H2 clean triple 3 hosts; H3 same numbers, different filler/titles;
H4 paraphrase agreement ("330 meters tall" / "stands 330 meters high");
H5 range-format agreement ("100 to 150" / "100-150" — C2 must NOT fire);
H6 agreeing negations ("emperor penguins cannot fly" / "…cannot fly and hunt
in groups"); H7 "never" agreement; H8 4-host byte-identical;
H9 date agreement ("in 1969" ×2); H10 extra numeric context in one page;
H11 superlative agreement ("mercury is the closest planet to the sun" ×2 —
R4-scope exclusion must NOT fire); H12 "no"-determiner agreement.

**§3c. New contradiction fixtures** (all must WITHHOLD with
GATE|CONTRADICTION): C-neg1 ("the vault is open"×2 vs "is not open"×1);
C-neg2 contraction ("isn't"); C-neg3 ("never"); C-num1 (2000 vs 500);
C-num2 range-vs-single (100-to-150 vs 300); C-num3 2v2 tie in BOTH page
orders (order-invariance); C-num4 ("between 100 and 150" vs 300);
C-num5 word-number paraphrase ("three hundred meters" vs "100 to 150 years"
— C2 must not fire, withhold via no-cluster); C-numD numeric dissent
visible only in a non-opened result snippet (for CORROB-1D).

**§3d. Permutation determinism.** M1, M2a, M2b, R2, H1, C-num3: rewrite
pages.txt with reversed and rotated P|-block orders → verdict bytes must be
identical (after the binary's own output; no rep tags to normalize — the
binary emits none).

## §4 Kill bars

- **K1** mixed-cluster: M1/M2b/M3 withhold — must hold (were false installs).
- **K2** order-invariance: M2a verdict == M2b verdict; §3d permutations
  byte-identical.
- **K3** contradiction-visible A9: R2, P3 withhold.
- **K4** paraphrase defense: R2P/R3P/R4P/P1/P2/P4 withhold; zero new installs.
- **K5** throughput: H1–H12 install 12/12.
- **K6** determinism: every case 2 runs → byte-identical.
- **K7** honesty: residual table (§3a) reproduced exactly; the full-battery
  kill bar (0 false installs over all 38) is NOT claimed — 11 expected
  residuals are named above with their owning layer.

Pass = K1–K6 hold. K7 is a reporting bar.

## §5 A9 verdict criteria (preregistered)

A9 (pure unanimity: ≥2 distinct hosts, byte-identical claim, no visible
contradiction) is a **WALL** for the corroboration layer iff:
(a) no INFO|DIVERSITY metric separates the R2/R3/R4 rings from the H1–H12
honest fixtures at any threshold without also flagging an honest fixture,
and (b) contradiction detection cannot fire on pure-unanimity sets by
construction (nothing to contradict). If both hold, the report names the
cheapest fixing signal the loop cannot manufacture today: a
**selection-layer dissent guarantee** — when any result snippet
C1/C2-contradicts the winning claim, open at least one dissenting page
(uses data the pipeline already emits; no new metadata); second-cheapest:
install-time KB-contradiction check against already-committed beliefs.

## §6 Standards & commits

Zero RNG in decision paths. Pure Zag for the mechanism; Python for
drivers/analysis only. Canonical `webg.zag` SHA verified before and after.
Commits to `sylorlabs/TNN`, branch `tnn-native-lab`, via
`~/workspace/commit_racefree.py` (TMPDIR=`~/workspace/tmp_commit`),
lab-relative paths → `docs/lab/knowledge/web_guides/live_ingest/harden/`:
(1) this prereg [FROZEN, before any building]; (2) `corrob.zag` + fixtures +
battery evidence + verdict report. No binaries, no `.zagd` caches.
