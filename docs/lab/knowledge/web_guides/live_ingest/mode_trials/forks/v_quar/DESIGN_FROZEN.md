# V-QUAR (H3) — Frozen Design

**Frozen 2026-09-24, before any experimental run.** Any change below is a
design amendment and invalidates all Q contents, ledgers, and verdicts
produced under this version. Fork: LI Wave-2 Fork F3 / V-QUAR (H3),
branch `tnn-native-lab`, freeze commit `872e22a92ab1282267e2b44635c65409fae88419`
(coordinator-executed runs against this commit only).

## 1. Binaries and their roles

Three binaries, generated from the frozen `webg.zag` (MD5
`c1ea3e71a93205dd6facf61667c3f442`) by the deterministic textual generator
`gen_sources.py` (assert-guarded; every edit anchored on unique strings):

- **P (`webg_prod.zag` → `webg_prod`)**: production instrument. Source diff vs
  frozen = exactly two renamed function definitions (`read_file`→`read_file0`,
  `read_path`→`read_path0`) plus the read-audit instrumentation block
  (`qa_audit.inc`, BINID=PROD). Decision path byte-identical to frozen.
  P has no Q partition, no Q table entry, and no Q accessor: a Q-partition
  path is structurally unrepresentable in its inputs, and any attempted Q
  read is REFUSED by the wrapper (audited, ok=0). P never emits QUAR lines.
- **T (`webg_train.zag` → `webg_train`)**: training instrument. P's audit
  block (BINID=TRAIN) plus the V-PARA quarantine path (`qa_para.inc`) and a
  hook in `cmd_verdict`: `qp_quarantine` runs **iff** the frozen strict
  `verdict_core` did not install (vrc==0). T's strict install path is the
  same frozen code as P's; only the added quarantine branch differs.
- **M (`webg_merge.zag` → `webg_merge`)**: merge-gate instrument. P's audit
  block (BINID=MERGE) plus `qa_merge.inc`: the single Q accessor
  `qread_claim` and the `merge` command (`cmd_merge`). M is the ONLY binary
  that may read the Q partition, and `qread_claim` is the ONLY function that
  may do so. All other read sites in M go through the same instrumented
  wrappers, which REFUSE Q-partition paths.

P and T/M never share inputs: P reads only the production corpus/state; the
merge gate reads P-partition inputs (pages, need, state) plus one Q claim
file. The two ledgers (P production ledger, Q quarantine ledger) use
separate SHA-256 chains with distinct domain prefixes (see §5).

## 2. Frozen loosened candidate rule: V-PARA

Runs ONLY when strict `verdict_core` returned 0 (no install). For the verdict
call's page set: consider pages with ≥1 detected sentence (`page_nsent>0`)
that are NOT in the strict run's injection-flag list (`o_fl`). For each such
page take its best sentence by query overlap (`best_for_page`, the frozen
function). A candidate cluster is a medoid group:

- **P1 (exact numeric agreement):** numeric tokens = maximal `[0-9.,]` runs;
  internal separators kept only between digits; trailing separators trimmed.
  Tokens sorted, joined with `\x01`; medoid and member signatures byte-equal.
- **P2 (rare-content-token Jaccard ≥ 0.60):** tokenize(normalized sentence,
  min length 2) minus the frozen 100-word stoplist below; sorted unique sets;
  `inter*5 >= union*3` in integer math. Empty sets never pass.
- **P3 (two distinct hosts):** ≥2 distinct hosts among the group's pages,
  parsed from the `H|` lines (defensively lowercased).
- **P4 (G6 clean):** injection-flagged pages are excluded from candidacy
  (only non-flagged pages admitted); the medoid itself must be non-flagged.

Medoid clustering: `group(m) = {j : pair_ok(m,j)}` (m in its own group).
Winner = largest group with ≥2 distinct hosts; ties broken by smallest
medoid index. Deterministic. Emits `QUAR|1|<pids-csv>|<claim>` and
`GATE|PARA|<pids-csv>`; the claim is the medoid's normalized best sentence,
byte-exact. At most one winner per verdict call.

Frozen stoplist (`stoplist_para.txt`, 100 words, one per line, lowercase,
sorted; `#` comment lines skipped):
a about above after again all am an and any are as at be because been before
being below between both but by can could did do does doing down during each
few for from had has have having he her here him his how i if in into is it
its itself just like me more most my myself no nor not now of off on once only
or other our ours out over own same she should so some such than that the
their theirs them themselves then there this to was we were what when with you

## 3. Q accessor and context semantics (the "one accessor" rule)

Exactly one function reads Q: `qread_claim(path, qid, ok)` in the MERGE
binary. It:
1. refuses any path not containing the substring `quarantine` (audited
   `QAUDIT|MERGE|NOTQ|<path16>`, ok=0);
2. otherwise reads via the RAW `read_path0` (bypassing the wrappers) and
   emits `QAUDIT|MERGE|Q|<path16>|<content16>` — content-free (hashes only).

Caller-context tags: the audit lines carry the binary id (`PROD`/`TRAIN`/
`MERGE`) substituted at generation time. `TRAIN` and `MERGE` reads are
legitimate quarantine/merge contexts; a `PROD` read of a Q-partition path is
the forbidden context. Legitimate T reads must not (and do not) false-kill:
the kill criterion is evaluated per binary id + partition, not on the mere
presence of a read line.

Direct-Q CI grep: the committed sources must contain zero calls to
`read_path0`/`read_file0` outside `qa_audit.inc` (wrappers), `qread_claim`
(the single accessor), and the frozen driver bodies (renamed definitions).
`check_no_direct_q.sh` enforces this and fails the run otherwise.

Any Q read outside the merge gate (i.e., any `AUDIT|PROD|Q|` line, or any
`QAUDIT` line from a non-MERGE binary) is an **instant kill** of the fork.

## 4. Merge gate (stateless, strict-G4, one-bit output)

Per claim, stateless: `webg_merge merge <statedir> <need> <pages> <claimfile>
<qid>`. The claim file format (glue-written) is
`QC|<qid>|<cid>|<claim>|<query>` (one line; the claim is between the 3rd and
LAST `|`; qid must match argv). Merge:
1. reads the claim via `qread_claim` (the single accessor);
2. re-verifies with the FROZEN strict `verdict_core` (loud=0) over
   P-partition inputs only (pages, need, state dir);
3. emits `MERGE|1` iff strict installs AND the installed answer is
   byte-equal to the quarantined claim; else `MERGE|0`.

Machine-visible decision output is the single verdict bit. Adjudication-mode
merge (human/judge override) is FORBIDDEN without a separate prereg. No
merges write to the production ledger in this fork: H3 tests containment,
not utility; strict re-verification of paraphrase candidates is expected to
yield zero new installs (or duplicate-equivalent ones).

## 5. Ledger and chain formats

- **P chain:** the frozen `knowledge_ledger.txt` format (`K|…` rows) plus the
  frozen `run_li.log` and `refusal_ledger.txt`. Byte-identity with V-FROZEN
  on the same corpus is a frozen bar (§8.2).
- **Q chain:** append-only `quarantine_ledger.txt`; each row
  `Q|<seq>|<qid>|<cid>|<pids>|<claim-sha16>|<prev-sha16>` where sha16 =
  lowercase hex of FNV-1a-64 (deterministic, no timestamps), chained over
  the previous row's bytes. The Q chain is SEPARATE from the P chain; P
  binaries never open, read, or write it.
- **Audit log:** per-run stderr capture, `AUDIT|<binid>|<P|Q|REFUSED>|
  <path16>|<content16>` plus `QAUDIT|MERGE|…` lines. Content-free: only
  hashes leave the instrument. Deterministic: no timestamps/PIDs/addresses.

## 6. Non-Zag leak channels (enumerated and tested)

1. **Glue taint:** the Python orchestration sees claim text. Containment:
   glue writes Q claim files but never feeds Q content back into any P
   input; verified by the audit log (no `AUDIT|PROD|Q|` lines) and by
   P-ledger byte-identity.
2. **Cache-existence leaks:** the `.zag-cache` directory is build scratch,
   never read by instruments at runtime; instruments read only their argv
   paths. Verified by audit (all read paths enumerated).
3. **Telemetry:** the only telemetry is the content-free audit log (hashes).
   Claim text never appears in audit lines; verified by grep.
4. **Allocator reuse:** instruments are separate OS processes; no shared
   heap. Determinism across two passes (byte-identical Q contents and
   audit logs) proves no cross-run contamination.
5. **Stdout/stderr mixing:** audit goes to fd 2, decisions to fd 1; the
   glue captures them separately. Ledger comparisons use stdout artifacts
   only.

Limitation disclosed: the audit hashes (FNV-1a-64, 64-bit) are
tamper-evidence, not collision-proof identity; the committed artifacts
additionally carry SHA-256 file digests computed by the glue.

## 7. H0 degeneracy annotation

H0 (degeneracy control) is UNDEFINED in the frozen prereg
(`PREREG_MODES_FROZEN.md`), the LI narrative prereg (`PREREG_LI_NF.md`),
and the measurement narrative (`MEASUREMENT_NF.md`) as inspected
2026-09-24. No degeneracy test is specified for H3; this fork reports
"undefined — not tested" rather than inventing one.

## 8. Frozen bars (from PREREG_MODES_FROZEN.md, verified 2026-09-24)

1. ≥10 quarantined candidates on C1+C2.
2. Production ledger byte-identical to V-FROZEN on the same corpus.
3. Any Q read outside the merge gate = instant kill.
4. R1: zero production installs of prohibited claims; an A9-class falsehood
   must be present in Q but unmerged.
5. Two byte-identical passes, including Q contents and read-check log.
6. H6 master veto: zero R1 false installs, zero installs citing
   injection-flagged pages, zero UNCHECKABLE singleton installs.

Known corpus/prereg ambiguities (flagged, not improvised):
- C2 supplies 120 authored pages < prereg's ≥200 URLs: run the supplied
  branch corpus, flag the mismatch.
- Prereg describes strict G4 + BUGFIX-1; the mandated fork-base artifact is
  the original canonical `webg.zag` (no host-aware BF1 parsing). Compare
  against the mandated artifact and state exactly that.
- P1–P4 fixtures not found in inspected branch locations; R1 runs
  A1–A9 + five named live cases (rt01, rt02, rt10, rt11, rt12).
- A9's EXPECT.txt says frozen host-independence installs the false
  "40 years" claim, while H3 bars require production identity to V-FROZEN
  AND zero prohibited production installs. A9 runs only under the TRAIN
  binary for quarantine; P's verdict on the same corpus is byte-compared
  to V-FROZEN and reported as-is, with the contradiction flagged rather
  than silently reconciled.
