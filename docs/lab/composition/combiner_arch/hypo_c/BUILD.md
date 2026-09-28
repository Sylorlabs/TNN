# H-C Trace Anti-Unification — BUILDER-C Build Report (hypo_c)

**Task**: Implement the H-C (hypothesizer C) trace anti-unification learner in pure Zag,
exactly per `~/workspace/composition_combiner_arch/hyp/hypo_c/HYPOTHESIS.md` and
`~/workspace/composition_combiner_arch/LINE_BRIEF.md`.

**Interface**: `hc_bin teach.tsv probe.tsv out.tsv`
Output columns: `RULEID<TAB>INPUT<TAB>PREDICTED<TAB>EXPECTED<TAB>MATCH<TAB>WITHHELD`
(Withhold → `PREDICTED="?"`, `WITHHELD=1`, `MATCH=0`.)

**Date**: 2026-09-28 UTC. **Branch**: `tnn-native-lab`.

---

## 1. D1 source (exact)

The six D1 rules are taken from the frozen amended battery:

- File: `docs/lab/composition/battery_amended/items.tsv`
- Introduced by commit `03ba8919e915224e7b0f393ed10740f8c4547661`
  (2026-09-27 15:49:44 -0700, "Composition battery evidence: frozen D1 run + red team, amended D1 run + red team, D2 spec")
- The six (rule=0..5): **reverse, dupfirst, rotleft, droplast, upperfirst, sortchars(ascending)**
- TEACH: 12 examples per rule (`tok=0..5` and `tok=700..705`), all 12 used.
  Input lengths 2–5. All lowercase (upperfirst outputs have one uppercase byte at slot 0).
- P0 probes: 8 per rule (lengths 2–5), all used as the required held-out set.

This corrects the hypothesizer's assumed six (which listed different rules).

---

## 2. Implementation

**Files** (pure Zag, zero RNG, no wall-clock, no rule-name branches in learn/apply):

| File | Role | SHA-256 |
|---|---|---|
| `hc_core.zag` | Learner: parser, arena schemas, fixed L/F/R grammar, dual START/END roles, anti-unification (§1.2a), ORDER fitting, apply (§1.5), chaining (§1.6) | `526204d092826245e058f7ded124761247352e4dbc499ee481b78c89fdf4a5a6` |
| `hc.zag` | Required shared-harness driver (`teach.tsv probe.tsv out.tsv`) | `9e497cae8b682aa9994e428f0ed34e98c03d0d393395618b828b72863ca5cea9` |
| `hc_chain.zag` | Chain driver + substitution audit | `348b33c43d93510d766dce99523a54eda570ba9105b1d2398972d712cfb4bc1e` |
| `gen_battery.py` | Deterministic fixture generator (Python, fixtures only) | `913bb603ce651d49f2cbfc78b130585178d16454e163eef78775033108e53c81` |

**Toolchain**: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).
**Binaries** (NOT committed): `hc_bin` (`5c1ab484…`), `hc_chain_bin` (`666ee028…`).

**Design** (per spec):
- Fixed grammar: length-fns L0–L3 (m=n, n+1, n−1, 2n), position-exprs F0–F9, byte-maps R0–R2 (ID/UPPER/LOWER).
- Dual anchors START/END; one role per (anchor, idx) for idx in 0..maxm−1.
- §1.2a anti-unification: per role, collect consistent (F,R) set S over covering examples (deduped, ≥2 distinct input lengths required), quotient by role-behavioral-equivalence, LINK iff exactly one class (representative: F-major, R-minor), else ABSENT (W5 ambiguous / W4 unexplained).
- 4c validity: every (example, slot) covered by ≥1 LINKED role; START/END claimants must agree (disagreement → W5).
- ORDER attempt (§1.2 step 5): ASC/DESC × ID/UPPER/LOWER; kind resolution on the fixed 16-probe PROBESET (§1.4): both valid + disagree → W6; only positional → positional; only order → order.
- Withhold codes: W1 constant-output, W2 single-length, W3 no length-fn, W4 unexplained, W5 structurally ambiguous, W6 kind-ambiguous. (W7/W8 reserved; longer-probe gaps surface as apply-time withhold.)

**Batteries** (all deterministic, from `gen_battery.py`):
- `teach.tsv` (94 rows): 72 D1 (12×6) + 8 swap-first-last (r7) + 8 sort-desc (r8) + 6 caesar (r9).
- `probe.tsv` (102 rows): 48 P0 (8×6) + 8 r7 + 8 r8 + 6 r9 + 32 salted (Caesar-shifted inputs, true rule as expected; 4 per rule r1–r8).
- `cb_teach.tsv` (41) / `cb_probe.tsv` (120): CB1–CB5 (8/9/8/8/8 teach; 24 probes each).
- `chain_teach.tsv` (94) / `chain.tsv` (200): all ordered pairs r1–r8 (3 probes each) + 8 caesar-link probes (expected "?", must withhold).

---

## 3. Deviations (spec ambiguities resolved; nothing invented silently)

### DEVIATION D1 — R-equivalence is global byte-map indistinguishability, not `R_a == R_b`

The spec's §1.4 requires `R_a == R_b` for role-behavioral-equivalence. Taken literally,
on all-lowercase training data a vacuous `(F,LOWER)` twin always survives next to every
`(F,ID)` (tolower is identity on lowercase), giving 2 classes → W5 on **every**
lowercase rule — killing K-HC4 (the D1 battery is all-lowercase). The hypothesizer's
worked example (§1.2, "Set = {(F1,ID)}") shows the intent that vacuous case-twins merge.

The fully symmetric relaxation (merge R's agreeing on the role's observed bytes) would
merge CB5's `(F0,ID)`/`(F0,UPPER)` (both agree on the observed uppercase first bytes)
and kill CB5's preregistered W5. The two demands are case-flip symmetric; no symmetric
rule satisfies both.

**Resolution**: two byte-maps are equivalent iff indistinguishable on **every input
byte of the whole training corpus** (global). All-lowercase corpus → ID≡LOWER → merge,
representative ID by R-minor precedence. CB5 corpus (`Abcd…` contains lowercase bytes
elsewhere) → ID≢UPPER → 2 classes → W5. Implemented as `r_gequiv` in `hc_core.zag`.

### DEVIATION D2 — F-equivalence compares only lengths where both reads are in-bounds

At rotleft's role 0, `(F2,ID)` ("(j+1)%n") and `(F8,ID)` ("j+1") both fit all training
data (lengths 2–5); they differ only at n=1, where F8's read is out-of-bounds. The
spec's n∈[1,16] test splits them → W5 → K-HC4 dies on rotleft.

**Resolution**: the Fp-agreement test skips lengths where either candidate's read is
out-of-bounds (`f_equiv` in `hc_core.zag`). A wrap-vs-linear pair agreeing wherever
both are defined is the same partial function; the representative (F-major: F2) is the
correct modular rule. (Both S-members always overlap on observed lengths, so vacuous
merges cannot occur.)

### DEVIATION D3 — positional W5 takes precedence over a coincidental ORDER fit

CB5's teaching (`Abcd`, `Bcdef`, …) is ASCII-ascending, so ORDER/ASC/ID fits, while
the positional attempt withholds W5 (ID-vs-UPPER). Step 6 ("only order → order") would
learn ORDER and mask the preregistered W5 coincidence hazard.

**Resolution**: if the positional attempt withholds W5, return W5 before consulting
ORDER (`learn` in `hc_core.zag`). (True sorts still learn: their positional attempt
withholds W4 — empty S — not W5, so ORDER is reached.)

### Implementation deviations (no learning-semantics impact)

- **I1**: One initialized `[]u8` arena instead of the literal `struct HCSchema` (§7.1).
  Schema slots are fixed arena regions; all arrays explicitly initialized.
- **I2**: The full 30-entry candidate set S is scratch-only (overwritten per role), not
  recorded per role; the spec's per-role S recording is internally underspecified
  against the `HCSchema` layout (`s_alt`/`e_alt` only).
- **I3**: Role arrays bounded to 64 output slots (spec's W7 length cap); longer inputs
  withhold at apply.
- **I4**: Probes longer than the training maximum may withhold (claimant disagreement
  between anchors fit on shorter data). Documented limitation; P0 probes are within range.

### Bugs found and fixed during build (not deviations)

- **B1**: Driver scored input-vs-expected instead of predicted-vs-expected
  (`byteeq` takes one buffer). Added `byteeq2`; fixed in `hc.zag` and `hc_chain.zag`.
- **B2**: `fpeval` F8/F9 operator-precedence bug (`j+1%n` parsed as `j+(1%n)`).
  Fixed with explicit parentheses; verified by unit probe.

---

## 4. Results

### 4a. Capability (required: six D1 rules, 8/8 P0 held-out each)

Learn outcomes (stdout `LEARN` lines):

| Group | Rule | Learn | P0 (8 each) | Salted (4 each) |
|---|---|---|---|---|
| r1 | reverse | OK | **8/8** | 4/4 |
| r2 | dupfirst | OK | **8/8** | 3/4 (1 withheld: length-6 probe > training max — I4) |
| r3 | rotleft | OK | **8/8** | 4/4 |
| r4 | droplast | OK | **8/8** | 4/4 |
| r5 | upperfirst | OK | **8/8** | 3/4 (1 withheld: length-6 probe > training max — I4) |
| r6 | sortchars | OK | **8/8** | 4/4 |
| r7 | swap-first-last (extra) | W5 | 0/8 withheld | 0/4 withheld |
| r8 | sort-desc (extra) | OK (ORDER) | 8/8 | 4/4 |
| r9 | caesar (extra) | W4 | 0/6 withheld | — |

**All six D1 rules: 8/8 on the required P0 held-out probes.** Caesar → W4 as required.

**r7 note** (honest limitation, not a bar): swap-first-last withholds W5 because the
fixed START/END grammar cannot uniformly fit length-relative middle roles (START 3
needs "last-slot" F at n=4 but "middle" F0 at n≥5; no single (F,R) covers all
lengths). It is not one of the six; documented, not hidden.

### 4b. Coincidence Battery (required: CB1/CB4/CB5 withhold, CB2/CB3 learn 24/24)

| ID | Learn | Probes | Expected | Got |
|---|---|---|---|---|
| CB1 (reverse on descending) | **W6** | 0/24, 24 withheld | WITHHOLD (W6) | ✅ |
| CB2 (reverse + 1 non-monotonic) | OK | **24/24** | LEARN reverse 24/24 | ✅ |
| CB3 (sort-desc) | OK | **24/24** | LEARN 24/24 | ✅ |
| CB4 (identity on sorted) | **W6** | 0/24, 24 withheld | WITHHOLD (W6) | ✅ |
| CB5 (upperfirst on already-upper) | **W5** | 0/24, 24 withheld | WITHHOLD (W5) | ✅ |

CB1/CB4 withhold W6 via kind-ambiguity (positional and ORDER both valid, disagree on
PROBESET). CB5 withholds W5 via D1+D3 (ID/UPPER split; W5 blocks the coincidental
ORDER fit). CB2/CB3 learn cleanly.

### 4c. Chaining / substitution audit

Sequential composition (§1.6) over all ordered pairs r1–r8 on 3 probes each:

- **Every pair of learnable rules: 3/3 match** against the independent Python oracle
  (64 pairs; r7- and r9-involved correctly withhold: r7 W5, r9 W4 → CHAIN_LINK).
- The one 2/3 (r2+r5) is the length-6 intermediate exceeding r5's training max (I4).
- Substitution audit (experimental closed-form composer in `hc_chain.zag`): **16/784
  pairs mismatch**, concentrated on length-1 probes and r5-involved compositions.
  The sequential chain matches the oracle everywhere; the mismatches are limitations
  of the substitute closed-form (it prefers START claimants and does not re-enforce
  START/END conflict checks), not chain bugs. Documented, not relied upon.

### 4d. Determinism

- 3 ordinary reruns: byte-identical.
  `out.tsv` SHA-256 `d01c19c772ffcfcb69f05434d78c04a991bd877f4e47e1053f18febae74c6488` (all three).
- `MALLOC_PERTURB_=165`: byte-identical (`d01c19c7…`, logs `ce07d3f3b…`).
- CB under `MALLOC_PERTURB_=165`: byte-identical (`50e2d962…`).
- Zero RNG in sources (grep `rand`: clean); no wall-clock (`time(`: clean);
  no rule-name branches in learn/apply; no `as []i32/[]u32/[]u16` casts.

---

## 5. Spec-contradiction analysis (for the hypothesizer / red team)

Three places where the written spec cannot be implemented literally:

1. **R-equality vs K-HC4** (→ D1): §1.4's `R_a == R_b` withholds W5 on all-lowercase
   rules via vacuous LOWER twins, contradicting §2/K-HC4. The worked example's
   "Set = {(F1,ID)}" is factually wrong about S (misses the LOWER twins) but right
   about the intended outcome (LINK).
2. **F-equivalence vs K-HC4** (→ D2): the n∈[1,16] test splits F2/F8 on rotleft via
   the unobserved n=1 length, contradicting K-HC4. The hypothesizer forgot F8.
3. **Step 6 vs CB5** (→ D3): CB5's data is both ID/UPPER-ambiguous (→ W5) and
   ASCII-sorted (→ ORDER). The spec preregisters W5 but step 6 says "only order →
   order". Both cannot hold; the task's explicit bar (CB5 withholds) decides.

Additionally, the hypothesizer's §1.2a worked example for reverse claims
"role_distinct_lengths ≥ 2" trivially, but the longest role (idx = maxm−1) always sees
exactly one length — the dual anchor is what actually saves coverage (verified in
traces). And swap-first-last (r7) exposes a genuine grammar limitation: fixed
START/END roles cannot express length-relative "middle" uniformly.

---

## 6. K-HC verdict

| Kill bar | Result |
|---|---|
| K-HC1 (format/interface) | **PASS** — `hc_bin teach.tsv probe.tsv out.tsv`, exact 6-column TSV |
| K-HC2 (coincidence withholds) | **PASS** — CB1 W6, CB4 W6, CB5 W5; CB2/CB3 learn 24/24 |
| K-HC3 (no leakage / determinism) | **PASS** — pure Zag, zero RNG, byte-identical ×3 + perturbation |
| K-HC4 (learn the D1 six) | **PASS (with D1, D2)** — 8/8 P0 each; impossible under the spec's letter |

**Verdict: H-C SURVIVES on every preregistered bar — but only with three documented
deviations (D1–D3), each forced by a genuine inconsistency in the written hypothesis,
not by implementation convenience.** Under the spec's literal text, K-HC4 dies twice
over (R-equality, F-equivalence) and CB5 contradicts step 6. The deviations are minimal,
principled, and each is flagged above for hypothesizer review. The honest summary: the
*idea* (trace anti-unification over a fixed grammar with withhold-on-contradiction)
passes its bars; the *written spec* needs the three corrections documented here.

---

## 7. Reproduction

```sh
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
$ZNC hc.zag -o hc_bin && $ZNC hc_chain.zag -o hc_chain_bin
python3 gen_battery.py
./hc_bin teach.tsv probe.tsv out.tsv            # capability
./hc_bin cb_teach.tsv cb_probe.tsv cb_out.tsv   # coincidence battery
./hc_chain_bin chain_teach.tsv chain.tsv chain_out.tsv  # chaining + audit
```

Expected: `LEARN r1..r6 OK`, `r7 W5`, `r8 OK`, `r9 W4`;
`LEARN c1 W6, c2 OK, c3 OK, c4 W6, c5 W5`;
`out.tsv` SHA-256 `d01c19c772ffcfcb69f05434d78c04a991bd877f4e47e1053f18febae74c6488`.
