# PREREG_E1.md -- Discriminating experiment E1: licensed-structure inspector for H1c

Wave: wave-20261001-2321pdt, lane BATTERY-E1.
Status: FROZEN DESIGN. This file is committed alone before any E1
world file, spec file, or tool source is created. Kill bars never
move after freezing.

## 0. Freeze record and provenance

E1 is the top-prioritized discriminating experiment from
BATTERY-CLUSTER/CLUSTER_ANALYSIS.md. It tests hypothesis H1c for
Cluster 1 (DERIVATION SUBORDINATION): "No standing derived structure
(locus: persistent learner state). No persistent representation of
composed procedures or laws exists at all; every multi-hop answer is
recomputed per query (BFS) or absent."

E1 discriminates, across all of Cluster 1 in one run, between:
- "derived structure absent" (H1c confirmed), and
- "derived structure present but subordinated" (H1c killed as
  stated; H1a, read-path precedence inversion, wins per the cluster
  analysis).

Frozen binary (no source edits permitted; the inspector is an
external probe):
- `tnn2.zag` SHA-256:
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
- `freeze_shim2_bin` SHA-256:
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
  (path: docs/lab/research-lead/overnight-20260928/
  core_freeze_tnn2_shim/freeze_shim2_bin)
- Pinned znc SHA-256:
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (path: src/tools/toolchain/znc_linux_x86_64_abed8aa1)

World id block: 71000-71999. Fresh and disjoint from v3
(50000-59999) and the PF battery (60000-69999). Material
differences from PF-A1/PF-C1/PF-C2 and v3-M1 are stated per world
in section 3. No world is a trivial FW1-FW9 variant.

## 1. Global constraints

PURE ZAG ONLY for all research logic. Shell only: invoke znc, run
binaries, git ops, move/copy files, sha256sum manifests. Each world
runs 3 times from fresh state via `freeze_shim2_bin <world>
<state.bin>`; transcripts and state.bin saved per run. No em-dashes
in any doc; check with check_no_dash.sh before commit. Commits
local only under
docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E1/; never push;
never git reset --hard; never rebase. This prereg is committed
alone first; world generation, tool building, and runs follow in
separate commits (commit-order self-check). The BATTERY and
BATTERY-CLUSTER lane directories are read-only for this lane.

## 2. Inspector design (frozen)

### 2.1 What counts as a licensed derived structure

A LICENSED DERIVED STRUCTURE is a persistent answer-bearing
structure in the frozen learner state satisfying all of:

1. PERSISTENCE: it is an active tag-20 node in state.bin after the
   full world stream, identical across all 3 runs (detection
   machinery is the v3_inspect_state lineage, unchanged).
2. DERIVED ANSWER: its answer value is the world-defined derived
   value for a derived key (compose relation, derived-fact
   relation, or revised-law relation), per the per-world bars in
   section 2.3.
3. LICENSED EVIDENCE: its evidence set includes at least one
   triple from EACH of the derivation's component roles (the
   per-world role sets in section 2.3), where a triple is licensed
   evidence iff it appears in the world's OBSERVE stream and its
   object value is reachable as a literal in the structure's graph
   walk (tag-101 to tag-902 literal reachability, the v3
   machinery). The subject==ms restriction of v3_inspect_state is
   REMOVED: composition's second hop has a different subject than
   the structure key, so the v3 restriction cannot license
   composition evidence by construction.
4. NOT A FLAT PROMOTION: for the composition worlds (W1, W2, W4),
   no evidence triple has (s, r) equal to the structure's own
   (subj, rel) key with the derived answer as object (the derived
   answer was never directly taught on the derived key). For the
   law world (W3), where the revised answer IS directly observed,
   the bar instead requires both-phase evidence (original-phase
   AND contradiction-phase triples for the same instance), the
   D11v3 lineage pattern; a flat last-write promotion carries only
   the contradiction-phase triple.

### 2.2 Oracle-blind detection

The inspector reads only state.bin and the world's OBSERVE stream.
It never reads QUERY lines, so the oracle expected values carried
on QUERY lines are invisible to it by construction. The checker
(e1_struct_check) reads the inspector report plus the transcript's
ANSWER lines; it applies the frozen per-world bars from this
prereg. World parameters (id ranges, derived values, probe
indices) live only in the checker as frozen bar data, the same
lineage as v3_struct_check's C5v3/D11v3.

### 2.3 Per-world licensed-derived bars (frozen)

W1 (composition vs retrieval, PF-A1 family). DERIVED=1 iff there
exists a STRUCTURE with rel=71609, subj in {71101, 71102},
answer=71902, whose evidence contains at least one triple
(s in {71101, 71102}, r=71601, o=71901) [P role] AND at least one
triple (s=71901, r=71602, o=71902) [Q role], and contains no triple
(s=subj, r=71609, o=71902) [never taught on the derived key].

W2 (derived-fact contradiction, PF-C1 family). DERIVED=1 iff there
exists a STRUCTURE with subj=71201, rel=71709, answer=71203, whose
evidence contains (71201, 71701, 71202) [chain-A role] AND
(71202, 71702, 71203) [chain-B role], and contains no triple
(71201, 71709, 71203) [never taught on the derived key].

W3 (cross-relation revision transfer, PF-C2 family). DERIVED=1 iff
there exists a STRUCTURE with subj in {71301, 71302}, rel=71801,
answer=subj+20, whose evidence contains (subj, 71801, subj+10)
[original-phase] AND (subj, 71801, subj+20) [contradiction-phase].

W4 (clean composition, v3-M1 family). DERIVED=1 iff there exists a
STRUCTURE with rel=71519, subj in {71501, 71502}, answer = 71595
for subj 71501 or 71596 for subj 71502, whose evidence contains at
least one triple (s in {71501, 71502}, r=71511) [P role] AND at
least one triple (r=71512, o=answer) [Q role], and contains no
triple (s=subj, r=71519, o=answer) [never taught on the derived
key].

### 2.4 Behavioral bypass and first-class criteria (frozen)

Transcript ANSWER lines are indexed in order (ANSWER[0] is the
first). Bypass means the behavior operators produce answers that
a first-class derived structure would not produce, while the
derived structure persists in state.

- W1: BYPASS=1 iff DERIVED=1 and ANSWER[0]=71999 and
  ANSWER[1]=71999 (the taught flat wrong fact shadows the
  composed answer). FIRSTCLASS=1 iff DERIVED=1 and
  ANSWER[0]=71902 and ANSWER[1]=71902.
- W2: bar probe is ANSWER[2]. BYPASS=1 iff DERIVED=1 and
  ANSWER[2]=71213 (the contradiction is honored by direct-fact
  shadowing while the derived structure keeps answer 71203).
  FIRSTCLASS=1 iff there exists a STRUCTURE subj=71201
  rel=71709 answer=71213 whose evidence contains
  (71201, 71701, 71202), (71202, 71702, 71203), and
  (71201, 71709, 71213) (the derived layer itself absorbed the
  exception).
- W3: transfer probe is ANSWER[3]. BYPASS=1 iff DERIVED=1 and
  ANSWER[3]=71411 (original law; no transfer). FIRSTCLASS=1 iff
  DERIVED=1 and ANSWER[3]=71421 (the shift transferred).
- W4: BYPASS=1 iff DERIVED=1 and ANSWER[0]=-2 and ANSWER[1]=-2
  (miss despite a standing derived structure). FIRSTCLASS=1 iff
  DERIVED=1 and ANSWER[0]=71595 and ANSWER[1]=71596.

### 2.5 Validity (frozen)

A world is E1-VALID iff its validity probes return the taught
values (the world taught what it claims):
- W1: ANSWER[2]=71901 and ANSWER[3]=71902.
- W2: ANSWER[0]=71203 and ANSWER[1]=71203 (promotion);
  ANSWER[3]=71202 and ANSWER[4]=71203 (taught links).
- W3: ANSWER[0]=71311 and ANSWER[1]=71411 (promotion);
  ANSWER[4]=71313 and ANSWER[5]=71413 (uncontradicted instances).
- W4: ANSWER[2]=71591 and ANSWER[3]=71595.

## 3. Worlds (fresh sealed worlds; streams pinned verbatim)

World files are generated byte-exact from these streams after this
prereg freezes (e1_worldgen.zag); E1_MANIFEST.sha256 is committed
before any run. QUERY lines carry the oracle expected value for
the scorer lineage convention; the inspector never reads them.

### E1-W1: construction vs retrieval (PF-A1 family)

Material difference from PF-A1: fresh id block, two composed
subjects sharing one mid node (shared-step composition), and the
flat wrong fact is taught on BOTH subjects.

```
OBSERVE 71101 71601 71901
OBSERVE 71102 71601 71901
OBSERVE 71901 71602 71902
OBSERVE 71101 71609 71999
OBSERVE 71102 71609 71999
QUERY 71101 71609 71902
QUERY 71102 71609 71902
QUERY 71101 71601 71901
QUERY 71901 71602 71902
```

### E1-W2: derived-fact contradiction (PF-C1 family)

Material difference from PF-C1: fresh id block, single promotion
pair (not doubled), contradiction value shares the subject id
family (71213) so a flat promotion is distinguishable from chain
evidence by relation, not by id novelty.

```
OBSERVE 71201 71701 71202
OBSERVE 71202 71702 71203
QUERY 71201 71709 71203
QUERY 71201 71709 71203
OBSERVE 71201 71709 71213
OBSERVE 71951 71960 71971
OBSERVE 71952 71960 71972
OBSERVE 71953 71960 71973
OBSERVE 71954 71960 71974
QUERY 71201 71709 71213
QUERY 71201 71701 71202
QUERY 71202 71702 71203
```

### E1-W3: cross-relation revision transfer (PF-C2 family)

Material difference from PF-C2: fresh id block, the systematic
contradiction covers two of three instances (not two of two
probed), leaving an unseen instance on the SAME relation as a
within-relation generalization probe in addition to the
cross-relation transfer probe. Validity probes cover the
uncontradicted instances on both relations.

```
OBSERVE 71301 71801 71311
OBSERVE 71302 71801 71312
OBSERVE 71303 71801 71313
OBSERVE 71401 71802 71411
OBSERVE 71402 71802 71412
OBSERVE 71403 71802 71413
QUERY 71301 71809 71311
QUERY 71401 71819 71411
OBSERVE 71301 71801 71321
OBSERVE 71302 71801 71322
OBSERVE 71961 71960 71981
OBSERVE 71962 71960 71982
QUERY 71301 71809 71321
QUERY 71401 71819 71421
QUERY 71303 71801 71313
QUERY 71403 71802 71413
```

### E1-W4: clean composition (v3-M1 family)

Material difference from v3-M1: fresh id block, no decoy/noise
structure, no taught fact on the compose relation at all. This is
the positive-attempt world: if derived structures ever form, they
form here, where nothing competes with them.

```
OBSERVE 71501 71511 71591
OBSERVE 71502 71511 71592
OBSERVE 71591 71512 71595
OBSERVE 71592 71512 71596
QUERY 71501 71519 71595
QUERY 71502 71519 71596
QUERY 71501 71511 71591
QUERY 71591 71512 71595
```

## 4. Frozen decision rule

Let D be the set of worlds w in {W1, W2, W3, W4} such that w is
E1-VALID on all 3 runs and DERIVED(w)=1 on all 3 runs.

Process preconditions (any failure yields E1-INCONCLUSIVE, an
instrument failure, not an H1c verdict): all 4 worlds x 3 runs
byte-identical transcripts (E1-K2); equal state.bin SHA-256 per
world across runs (E1-K2); E1-VALID on every run; DERIVED
consistent across the 3 runs of each world; E1-K1, E1-K3, E1-K4,
E1-K6 all PASS; calibration controls PASS.

- E1-ABSENT iff D is empty. Supports H1c: no standing derived
  structure exists for any Cluster 1 signature; multi-hop answers
  are recomputed per query or absent.
- E1-SUBORDINATED iff D is nonempty AND every w in D has
  BYPASS(w)=1 AND no w has FIRSTCLASS(w)=1. Kills H1c as stated
  (standing derived structures exist); supports "present but
  subordinated"; H1a (read-path precedence inversion) wins per the
  cluster analysis.
- E1-FIRSTCLASS iff D is nonempty AND at least one w in D has
  FIRSTCLASS(w)=1. Kills H1c outright; derived structures drive
  behavior.
- E1-AMBIGUOUS iff D is nonempty and some w in D has
  BYPASS(w)=0 and FIRSTCLASS(w)=0. Report only; no H1c verdict.

## 5. Process bars E1-K1 through E1-K6

- E1-K1 (prereg ordering). PASS iff this file's commit strictly
  precedes the first commit containing any E1 world file, spec
  file, or tool source, and this file's SHA-256 is unchanged after
  the battery.
- E1-K2 (determinism). PASS iff all 4 world transcripts are
  byte-identical across 3 fresh-state runs AND the per-world
  state.bin SHA-256 is equal across the 3 runs.
- E1-K3 (frozen binary). PASS iff freeze_shim2_bin and tnn2.zag
  match the section 0 hashes before and after the battery, and
  zero modifications under the frozen cognition paths.
- E1-K4 (seal integrity). PASS iff E1_MANIFEST.sha256 verifies
  (all files OK) and grep of 71000-71999 over tnn2.zag and
  freeze_shim2_bin returns zero matches.
- E1-K6 (no-leak). PASS iff e1_audit_noleak reports zero leaks.

## 6. Calibration

- Competent control: a synthetic inspector report containing a
  W1-conformant LICENSED DERIVED structure plus a synthetic
  transcript with derived answers; the checker must print
  DERIVED=1 and FIRSTCLASS=1 for check E1W1.
- Degenerate control: a synthetic report with only flat and
  per-instance structures; the checker must print DERIVED=0 for
  all four checks.
- Inspector machinery cross-check: run e1_inspect_state on the
  committed v3 m1/m3 state bins with their world files; the
  STRUCTURE lines must match the committed v3_inspect reports
  exactly (detection machinery unchanged); EVIDENCE lines may be a
  superset (the widened licensing of section 2.1 is the only
  delta), documented in the run report.

## 7. K-C0A audit (zero new semantic cases in the inspector)

Frozen audit procedure, executed after the inspector is built and
before runs:

1. e1_inspect_state.zag contains zero integer literals in
   71000-71999 and zero string literals naming a world, role, or
   relation; verified by grep. The inspector is fully generic over
   any state.bin plus any worldfile.
2. Predicate-vocabulary diff against the lineage baseline
   v3_inspect_state.zag: the only semantic delta is the removal of
   the subject==ms evidence restriction (section 2.1); the
   structure-detection predicates and the literal-walk machinery
   are unchanged.
3. The inspector collects OBSERVE lines only; QUERY lines are
   never read (oracle-blind by construction).
4. World parameters (id ranges, derived values, probe indices)
   appear only in e1_struct_check.zag as the frozen per-world bars
   of section 2.3 (scorer data, the v3_struct_check lineage), never
   in the inspector.
5. The audit prints K-C0A PASS/FAIL. K-C0A FAIL voids the
   inspector; rebuilding requires a new prereg section, never a
   silent fix.

## 8. Predicted outcome (recorded before execution)

E1-ABSENT. Basis: v3 M1 inspector found only unlicensed structures
(EVIDENCE count=0); v3 M3 found per-instance structures with
per-instance evidence and D11v3 FAIL; PF-A1 showed retrieval
shadowing with no construction trace; PF-C2 showed no transfer.
No evidence to date suggests a standing derived layer.

## 9. Criterion 0 status (binding)

This experiment probes frozen researcher-authored mechanisms with
a white-box inspector. C0-A through C0-D are NOT MET. No score
here may be described as L3, L3-adjacent, or progress toward L3.
Report as mechanism-targeted evidence for H1c only.
