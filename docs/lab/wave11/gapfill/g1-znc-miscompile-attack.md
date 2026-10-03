# G1 — znc miscompile of variation/seam code as an attack vector

## 1. Slice
Gap-fill G1 (T3): a znc codegen defect silently reordering the RNG fence or
breaking byte-identical replay in the variation seam — every source-level
guarantee in T1–T3 rests on a compiler no slice adversarially tests.

## 2. Falsifiable claim
The build-time differential-semantics canary specified below catches every
member of the planted miscompile battery (fence-check reorder/drop, selector
tie-break flip, audit-marker drop, verdict-seal flip) with correct
compiler-vs-source attribution, on the fixed input/state corpus, before any
variation trial binary ships. One escape or one misattribution kills it.

## 3. Design
**3a. Seam corpus.** Enumerate exactly the functions where a silent semantic
change is an integrity break, not a crash: the Arm B fence allow/deny check,
the Arm C state→variant selector, the sealed-verdict firewall crossing, the
ledger canonical encoder (`docs/lab/wave11/t3-integrity-redteam/findings/04-ledger-forgery.md`
§3 fixes the encoder as load-bearing). All are pure functions — no entropy
inputs allowed in the corpus, per Law 1.

**3b. Differential build (compiler-vs-source discriminator).** Compile the SAME
source twice under znc: once release/hot, once zero-opt/cold, flags otherwise
identical. Any observable divergence on the same inputs is by construction a
codegen defect, not a source defect — the source is bit-identical. (VERIFY
FIRST: znc must expose two distinct opt levels; if not, pivot to §3e before
spending anything. The characterized defect is hot-path-only,
`docs/lab/units/arms/C-W/BUILD_LOG.md` ZNC-2026-09-19-001 note, so the cold
build is the reference and the hot build is the suspect.)

**3c. Corpus + ground truth.** Fixed input/state vectors: hand-computed
truth-table rows (a human verifies a dozen rows on paper — authoritative
ground truth no compiler touches), plus boundary rows (fence
`site=MAX`/`MAX+1`, class flips, selector ties). Run both binaries hot (tight
loop, documented warmup — the defect only fires on the hot path) and record:
fence allow/deny, selector variant ids, fence marker traces (§3d), canonical
ledger bytes. Diff byte-for-byte.

**3d. Fence-order instrumentation.** Compile a traced variant where each fence
check appends a marker to a buffer in evaluation order:

```zag
fn fence_allows(site:u32, cls:u32) -> u8 {
  if site > MAX_ENTROPY_SITE { return 0; }  trace(1);
  if cls != CLS_EXPRESSION   { return 0; }  trace(2);
  if !allow_table[site]      { return 0; }  trace(3);
  return 1;
}
```

Reordered or dropped markers between opt levels = fence-order miscompile
caught, with the exact check named. Deny-by-default ordering is load-bearing;
the trace makes reordering visible.

**3e. Attribution protocol.** On divergence: (i) re-run hand-computed rows —
if the cold build disagrees with paper, the SOURCE is wrong (fix source, not
a compiler story); (ii) metamorphic rephrase — rewrite the suspect function
with identical semantics (swap commutative branches, invert comparisons),
rebuild at release opts: if divergence MOVES, it's codegen; if it PERSISTS,
it's source. AGENTS.md's znc lessons (002 slice-pointer, 003 field sizes,
004 local-struct slice alias) are the pattern library for what "moves" looks
like.

**3f. Runtime self-check.** Embed the golden rows in the shipped binary; the
binary executes them at startup before the first episode and refuses to run
on mismatch — catches build skew (wrong binary shipped) that build-time tests
can't.

## 4. Kill bar
Blind battery of 12 planted miscompiles — 4 fence reorder/drop, 4 selector
tie-break flips, 2 audit-marker drops, 2 verdict-seal flips — modeled on the
001 hot-path pattern. The canary dies if ANY fires: one escape undetected,
one misattribution (compiler blamed for a source bug or vice versa), or one
false flag on the 200-row clean baseline. All 12/12 caught, 12/12 attributed,
0/200 false flags — or the design is not trial-ready.

## 5. Honesty notes
- Weakest point: COMMON-MODE backend bugs. Both builds share znc's backend;
  a backend defect firing identically at both opt levels passes the
  differential silently. Only the hand-computed rows catch that class, and
  they cover a dozen rows, not the corpus. This design narrows the
  optimizer-attack surface; it does not certify the backend.
- The defect is hot-path-only: if the canary's warmup doesn't push the seam
  onto the same hot path production uses, it can pass while production
  miscompiles. Warmup fidelity is a parameter, not a proof.
- Corpus coverage is finite — a miscompile keyed on an input shape outside
  the corpus escapes. The battery is 12 plants, not an enumeration.
- The N-version reference and the traced variant are themselves znc-compiled;
  the only non-compiler ground truth is the paper rows. I am NOT claiming a
  verified compiler or a complete miscompile oracle — this is a tripwire on
  the exact seam where a silent miscompile becomes an integrity break
  (slices 04 and 12 show what breaks when the seam lies).
- Assumes distinct znc opt levels exist. If they don't, §3b collapses and the
  design must be re-authored around N-version source formulation.

## 6. Next build step
Build the minimal differential canary on ONE real function — the Arm B fence
check — plus one planted fence-drop miscompile modeled on the 001 hot-path
pattern, and confirm the canary catches it with correct attribution. In the
same sitting, verify znc exposes two distinct opt levels. If the plant
escapes or the levels don't exist, the design is dead before it scales —
that single experiment is the whole bet.
