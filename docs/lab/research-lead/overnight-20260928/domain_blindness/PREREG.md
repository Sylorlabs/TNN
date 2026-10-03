# PREREG: DOMAIN-BLINDNESS -- Does the Unified Composition Operation U Depend on Human-Meaningful Identifiers?

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Step 0) strictly precedes all implementation.

## 1. Question

Micah's DOMAIN-BLINDNESS TEST: for every general composition mechanism,
(1) train under arbitrary opaque identifiers, (2) rename every
domain/relation/entity identifier after freeze, (3) preserve only
learned behavior/structure, (4) composition result must remain
equivalent. "If performance depends on human domain identity, that is
architectural failure."

The unified behavior-contract composition operation U (COMPOSE-COLLAPSE,
verdict SUBSUMPTION; exercised adversarially in COMPOSE-PAIR6-ADV,
verdict INFORMATIVE-FAIL) is the mechanism under test. GEN: no GEN
implementation exists in any compose lane (searched compose_collapse,
compose_ops, lane-compose-pair6; nothing named GEN implements a
composition operation), so this battery tests U only. If a GEN
implementation appears later, it gets its own preregistered battery.

Concrete form of the test here: take the exact P6 build
(base + U logic + P6 driver), apply a FROZEN mechanical renaming that
replaces every human-meaningful identifier with opaque tokens, rebuild,
run, apply the frozen inverse mapping to the output, and require
byte-identical composition decisions. Any divergence is architectural
failure, and the first differing output byte locates the leak.

## 2. Sources under test (frozen digests, verified in NAMECHECK Step 1)

- `ref_uc_base.zag` -- fact store, probe_kind, behaviors
  (WALK/COUNT/MAYBE/IDENT), MAP table, contract observation, teaching.
  sha256 `736f12e7452fb0a95c2dbfc8115028a4e1afba9529cb6cd727acb65367799218`
  (canonical collapse digest; matches PAIR5-committed and P6-committed refs).
- `ref_uc_uni.zag` -- THE UNIFIED OPERATION U: kind-set admission,
  ordered trial execution with end-to-end verification, failure-triggered
  widening, success recording.
  sha256 `ec36df4a01cb1a2b93043184e6e2c84b07658fe7b0c317f9a489ffd6b7b4562e`
  (canonical collapse digest).
- `p6_new.zag` -- P6 world setups, oracle scaffolding, driver main.
  sha256 `32d84056de2878f8db000ff87b2fb4b96cbf187d6cf42c357081bfb69a123870`.
  This file carries EVERY exercised domain/relation/entity identifier.

Baseline behavior (reproduced 2026-10-03 in /tmp, 3/3 byte-identical):
whole-output sha256
`be713f822779afdd7cf1c3f2e87670dc4b5e903fa73a8bc0ede0a105f3a219d7`
(byte-identical to the P6 lane's frozen K4 digest).

## 3. Scope decision (frozen)

The exercised identifier surface is EXACTLY the numeric identifiers,
setup-function names, and query labels in `p6_new.zag`. Rationale:

- The U logic file (`ref_uc_uni.zag`) is asserted to contain no
  identifiers at all (only mask bits 0/1, the -2 miss sentinel, MAP
  indices, counters). Kill bar B5 tests this mechanically: the frozen
  renaming script run against `ref_uc_uni.zag` must yield a
  byte-identical file.
- The base setup functions `setup_p1`, `setup_p2a`, `setup_p2b`,
  `setup_p3`, `setup_p5extra` in `ref_uc_base.zag` are DEAD CODE in the
  P6 build: their only caller was `ref_uc_uni.zag`'s `main`, which is
  stripped during assembly (`sed '/^fn main/,$d'`). They are never
  executed and cannot affect any composition decision. They are left
  byte-identical (renaming dead code cannot change behavior; leaving it
  frozen keeps the base reference intact).
- Behavior classes (0=WALK, 1=COUNT, 2=MAYBE, 3=IDENT) are the
  mechanism's own fixed vocabulary (protected-core-adjacent), not
  domain identifiers. They are NOT renamed.
- The -2 miss sentinel, kind bit positions, MAP indices, counters,
  buffer sizes, and small count/answer values (1, 2, 3 as VALUES, not
  identifiers) are NOT renamed.

## 4. Variant A: identifier renaming (frozen permutation)

Opaque token namespaces: entities -> 5000+idx, relations -> 9000+idx.
All positive, disjoint from the -2 sentinel and from small count values.

Entity table (sorted source order; mechanical, no semantic content):
21->5001, 22->5002, 61->5003, 62->5004, 63->5005, 71->5006, 81->5007,
82->5008, 83->5009, 84->5010, 101->5011, 102->5012, 103->5013,
111->5014, 112->5015, 201->5016, 202->5017, 203->5018, 211->5019.

Relation table: 81->9001, 82->9002, 91->9003, 92->9004, 93->9005,
99->9006.

Note 81 and 82 are BOTH entity ids (stops) and relation ids (walk/count
relations, distractor facts). The renaming is therefore
POSITION-AWARE: fact subjects/objects and teach/exec/uni_solve subject
fields take the entity table; fact relation fields and map_new rel
fields take the relation table.

Setup-function names: setup_p6->setup_w1, setup_p6_noX->setup_w2,
setup_p6_noY->setup_w3, setup_p6pipe->setup_w4.
Query labels: "P6-ABL-X"->"QB", "P6-ABL-Y"->"QC", "P6-PIPE"->"QD",
"P6"->"QA". ("ABL-X"/"ABL-Y" literally name domain structures, so they
are renamed. "UNI", "ORACLE", "CENSUS", "INTER=", "WIDEN=1", "ARM=" are
fixed scaffolding and stay.)

Validity argument (frozen; why the renamed world is a faithful
isomorphism): both tables are injective; every image is positive, so no
collision with the -2 miss sentinel; facts are renamed consistently
per-field, so subject-hood is preserved exactly (pkind depends only on
subject-hood); walk chains and count multiplicities are preserved;
teach expected values that are entities (21, 83, 63) are renamed
consistently with their subjects, while teach expected values that are
counts (1, 2, 3) are untouched and remain non-subjects (all renamed
subjects are >= 5001, so no count value can become a subject); the
distractor fact (83,81,84)->(5009,9001,5010) preserves 5009's
subject-hood; the dead MAP's relation 99->9006 still has no facts.

### 4.1 Frozen mechanical renaming procedure (transcribed verbatim into rename_a.sh)

Input: the frozen `p6_new.zag`. Output: `db_new.zag`. All steps are
fixed sed/grep invocations; no human judgment, no hand edits.

1. Strip every line starting with `//` (all human vocabulary in
   comments), prepend a fixed 3-line neutral header naming the file,
   the frozen permutation, and the no-hand-edits rule.
2. Function names (word-boundary; `_` is a word char, so `setup_p6`
   cannot match inside `setup_p6_noX`):
   `s/\bsetup_p6_noX\b/setup_w2/g; s/\bsetup_p6_noY\b/setup_w3/g;`
   `s/\bsetup_p6pipe\b/setup_w4/g; s/\bsetup_p6\b/setup_w1/g`
3. String labels, longest first:
   `s/P6-ABL-X/QB/g; s/P6-ABL-Y/QC/g; s/P6-PIPE/QD/g; s/P6/QA/g`
4. Positional tagging of identifier fields (GNU sed -E):
   - `s/fact_add\(A,([0-9]+),([0-9]+),([0-9]+)\)/fact_add(A,E\1,R\2,E\3)/g`
   - `s/map_new\(A,([0-9]+),([0-9]+),([0-9]+),([0-9]+)\)/map_new(A,\1,\2,R\3,R\4)/g`
   - `s/teach\(A,([0-9]+),([0-9]+),([0-9]+)\)/teach(A,\1,E\2,E\3)/g`
   - `s/exec_map\(A,([0-9]+),([0-9]+)\)/exec_map(A,\1,E\2)/g`
   - `s/uni_solve\((A|C),B,c,([0-9]+),/uni_solve(\1,B,c,E\2,/g`
   (The `fn` definition lines do not match these call shapes.)
5. Entity table, 3-digit tokens before 2-digit tokens (no prefix
   collisions within a length group):
   `s/E101/5011/g; s/E102/5012/g; s/E103/5013/g; s/E111/5014/g;`
   `s/E112/5015/g; s/E201/5016/g; s/E202/5017/g; s/E203/5018/g;`
   `s/E211/5019/g`
   `s/E21/5001/g; s/E22/5002/g; s/E61/5003/g; s/E62/5004/g;`
   `s/E63/5005/g; s/E71/5006/g; s/E81/5007/g; s/E82/5008/g;`
   `s/E83/5009/g; s/E84/5010/g`
6. Relation table:
   `s/R81/9001/g; s/R82/9002/g; s/R91/9003/g; s/R92/9004/g;`
   `s/R93/9005/g; s/R99/9006/g`
7. Strip tags that matched no table entry (these are count values,
   expected to be exactly E1/E2/E3; R0 from map_new rel2=0):
   `s/E\([0-9][0-9]*\)/\1/g; s/R\([0-9][0-9]*\)/\1/g`
8. Audits (fail closed, non-zero exit on any failure):
   a. `grep -w -E '21|22|61|62|63|71|81|82|83|84|91|92|93|99|101|102|103|111|112|201|202|203|211'`
      on the output must return NOTHING (no original identifier token
      survives as a whole word).
   b. `grep -E 'P6|setup_p6|inbound|outbound|ABL-'` must return NOTHING
      (no human label survives).
   c. `grep -o -E '[ER][0-9]+'` must return NOTHING (no tagging
      residue).
   d. `grep -n '//'` must show ONLY the 3 header lines (no vocabulary
      in comments).

### 4.2 Frozen inverse output mapping (Variant A)

Applied to the renamed binary's stdout before comparison. Fixed sed:
- `s/5001/21/g; s/5002/22/g; s/5003/61/g; s/5004/62/g; s/5005/63/g;`
  `s/5006/71/g; s/5007/81/g; s/5008/82/g; s/5009/83/g; s/5010/84/g;`
  `s/5011/101/g; s/5012/102/g; s/5013/103/g; s/5014/111/g;`
  `s/5015/112/g; s/5016/201/g; s/5017/202/g; s/5018/203/g;`
  `s/5019/211/g`
- `s/QB/P6-ABL-X/g; s/QC/P6-ABL-Y/g; s/QD/P6-PIPE/g; s/QA/P6/g`
(All tokens are fixed-width; no prefix collisions; replaced values
introduce no new matchable tokens.)

## 5. Variant B: kind-label polarity swap (second adversarial dimension)

The kind labels 1 (NODE/subject) and 2 (NUM/non-subject) are researcher
ontology in `pkind`. Variant B applies, ON TOP of Variant A, a global
polarity swap {1<->2} of kind labels: a mechanical automorphism that a
label-blind mechanism must be invariant to.

Frozen edits:
- On a copy of `ref_uc_base.zag` -> `db_base_kswap.zag`: within the
  `fn pkind` body only, swap the two returns via placeholder:
  `sed '/^fn pkind/,/^}/ { s/return 1;/return K/; s/return 2;/return 1;/; s/return K/return 2;/; }'`
- On `db_new.zag` -> `db_new_kswap.zag`: swap kin/kout in the four
  uni_solve calls: `s/5003,1,2,/5003,2,1,/g` (this token is unique to
  those calls).
- Audits: `diff ref_uc_base.zag db_base_kswap.zag` must show EXACTLY
  the two pkind return lines changed; `diff db_new.zag
  db_new_kswap.zag` must show EXACTLY the four uni_solve lines changed.

Frozen inverse output mapping (Variant B): the Variant A inverse,
followed by mask polarity swap-back via placeholders:
- `s/inmask=2/inmask=T/; s/inmask=1/inmask=2/; s/inmask=T/inmask=1/`
- `s/outmask=2/outmask=T/; s/outmask=1/outmask=2/; s/outmask=T/outmask=1/`

## 6. Assembly, build, run (frozen)

- `sed '/^fn main/,$d' ref_uc_uni.zag > uni_nomain.zag`
- `cat ref_uc_base.zag uni_nomain.zag db_new.zag > a_full.zag`
- `cat db_base_kswap.zag uni_nomain.zag db_new_kswap.zag > b_full.zag`
- Region audits: each concatenated region must cmp byte-identical to
  its source (head/tail -c by recorded byte sizes).
- Compile with pinned safebin znc; run each binary 3x; sha256 each run.
- Apply the frozen inverse mapping; `cmp` against the frozen baseline
  output digest
  `be713f822779afdd7cf1c3f2e87670dc4b5e903fa73a8bc0ede0a105f3a219d7`.

## 7. Frozen predictions

- P1: `rename_a.sh` applied to `ref_uc_uni.zag` yields a byte-identical
  file (B5: the U logic contains no identifiers to rename).
- P2: 3/3 runs of each variant binary are pairwise byte-identical
  (determinism, B2).
- P3: inverse-mapped Variant A stdout is byte-identical to the frozen
  baseline output (B3).
- P4: inverse-mapped Variant B stdout is byte-identical to the frozen
  baseline output (B4).

## 8. Frozen kill bars

- B1 MECHANICAL RENAMING: PASS iff the implementation transcribes the
  Section 4.1 procedure verbatim, all four step-8 audits pass, and the
  script file's first commit postdates the prereg commit (commit-order
  self-check).
- B2 DETERMINISM: PASS iff 3/3 runs per variant are pairwise
  byte-identical (cmp); digests recorded.
- B3 BLINDNESS-A: PASS iff inverse-mapped Variant A stdout cmps EMPTY
  against the frozen baseline output.
- B4 BLINDNESS-B: PASS iff inverse-mapped Variant B stdout cmps EMPTY
  against the frozen baseline output.
- B5 U-LOGIC IDENTIFIER-FREE: PASS iff the frozen renaming procedure
  applied to `ref_uc_uni.zag` changes zero bytes, AND a numeric-token
  inventory of `ref_uc_uni.zag` shows no relation/entity-scale
  constants (only mask bits 0/1, the -2 sentinel, MAP indices,
  counters).
- B6 NO NEW SEMANTICS: PASS iff (a) `diff ref_uc_base.zag
  db_base_kswap.zag` shows exactly the two pkind lines;
  (b) `diff db_new.zag db_new_kswap.zag` shows exactly the four
  uni_solve lines; (c) grep for comparisons against any renamed
  identifier value in all built sources returns empty
  (no `== 5001`-style branches anywhere).

## 9. Verdict mapping (frozen)

- B1-B6 all PASS: verdict PASS (blind). U's composition decisions are
  invariant to human domain/relation/entity identifiers AND to
  kind-label polarity. The composition operation does not read labels.
- B3 FAILS: verdict FAIL (label-dependent, ARCHITECTURAL FAILURE).
  Report the first differing output byte/line as the leak location and
  trace which code path consumed the identifier.
- B4 FAILS while B3 passes: verdict FAIL (kind-label dependent).
  The mechanism's behavior depends on the researcher's NODE/NUM
  polarity assignment.
- B5 FAILS: verdict FAIL. The U logic file itself contains
  identifiers; quote the lines.
- B1 FAILS: verdict VOID. The renaming was not purely mechanical;
  re-freeze with a corrected script, do not hand-tune.
- B2 FAILS: verdict UNDECIDED. Name the decisive rerun.

## 10. Honest boundaries (pre-declared)

- Behavior classes (WALK/COUNT/MAYBE/IDENT) are mechanism vocabulary,
  not renamed; a mechanism that depended on class NUMBER semantics
  would not be caught here (that is a separate protected-core
  vocabulary question).
- The -2 sentinel and the admission/trial/widening control flow are
  untouched by construction.
- This battery tests the P6 composition workload (diamond decline +
  ablations + pipeline control); it does not test other workloads.
- The ORACLE scaffolding is driver code, renamed with the driver.
- GEN does not exist; only U is tested.
