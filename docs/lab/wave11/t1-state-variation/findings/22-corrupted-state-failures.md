# Slice 22 — Corrupted-state failure modes (Track 1: state-dependent deterministic variation)

## 1. Slice
Failure-mode analysis for the Track 1 variation state variables: corruption (bad write),
staleness (missed update), and adversarial influence — detector, deterministic graceful
degradation to NULL variation, and attack-surface enumeration.

## 2. Falsifiable claim
A state-variation TNN that (i) checksums every variation state variable at rest, (ii) range-checks
each against its prereg-declared domain, (iii) cross-checks consistency between related variables
at the deterministic render-gate, and (iv) separates variation state strictly downstream of
verdicts, will: detect 100% of single-variable corruptions and stale uses across 10,000
fault-injection trials per variable class; degrade to NULL variation (fixed default expression)
on every detected fault with zero verdict/memory/refusal/ledger changes; and replay the degraded
output byte-identically from the logged fault record.

## 3. Design
Variation inputs are render-only: salience weights (emphasis/order), elaboration budget (depth),
recency weights, active context pointer, render-phase episode watermark. Verdict paths never read
them (invariant: `variation_read_set ∩ verdict_write_set = ∅`, enforced by prereg enumeration).

(a) Corruption detector (runs once, at the deterministic render-gate, before any rendering):
```
fn render_gate(s: *State, L: *Audit) -> u32 {   // returns corruption bitmask, 0 = clean
  var mask: u32 = 0; var i: u32 = 0;
  while i < s.nvars {
    let d = VAR_TABLE[i];                        // prereg: name, lo, hi, horizon
    let v = s.vars[i];
    if v < d.lo or v > d.hi { mask |= (1 << i); } // range check
    if fnv1a(s.seg[i]) != s.csum[i] { mask |= (1 << i); } // checksum at rest
    if L.clock - s.updated_ep[i] > d.horizon { mask |= (1 << i); } // staleness
    i += 1;
  }
  if abs(sum(s.salience) - 1.0) > EPS { mask |= SAL_MASK; }       // cross-var
  if s.budget > s.budget_cap or s.budget_cap < 0 { mask |= BUD_MASK; }
  if s.ctx_ptr != L.active_ctx { mask |= CTX_MASK; }              // ctx vs ledger
  return mask;
}
```
Checksums are written by the same lawful update path that writes the variable (single
writer: the variation-update op, audited); a bad write from any other path breaks the checksum.
(b) Graceful degradation: if `mask != 0`, variation is disabled for this turn — output =
`default_render(verdict, input)`: fixed templates, ledger order, prereg-default depth. Never
RNG, never a verdict change (verdicts are already decided upstream; NULL variation is a pure
function of the verdict). (c) Degradation is deterministic and logged: the mask, input hash,
and output hash are appended as one `OP_STATE_DEGRADED` audit entry; replay re-applies the
same mask at the same gate and reproduces the same bytes.

## 4. Kill bar
Run the fault-injection trial: 10,000 injected faults per class (bit flips in each variation
state word, frozen-stale watermarks, salience/budget saturation, checksum-only rewrites, and
injection at every pipeline phase). Kill the design if ANY of: (1) a fault goes undetected
(detector miss) AND produces non-NULL variation output; (2) any fault changes a verdict, memory
decision, integrity refusal, or ledger content vs the fault-free control; (3) degraded output
differs between live run and replay-from-log on any trial; (4) staleness longer than the declared
horizon is used by rendering on any trial. Zero misses, zero verdict changes, byte-identical
replays — or the mechanism dies.

## 5. Honesty notes
Checksums catch bad writes, not lawful-looking bad values — an attacker who can both write a
variable AND recompute its checksum (i.e., a memory-write attacker) defeats detection; the
threat model here is external-input influence and internal bugs, and a post-hoc ledger replay
still exposes such an attacker because the append-only audit shows the write. The detector runs
at one gate: a variable corrupted *after* the gate but *before* rendering is missed — the fix is
placing the gate immediately before the render call with no interleaved writes, which the
builder must guarantee, not assume. The sensor-deceivable hole (accepted program hole) means
salience is legitimately influenced by spoofed observations — that is lawful state, not
corruption, and this design does not claim to detect it. I am NOT claiming protection against
an adversary with arbitrary internal write access; I am claiming bounded, provable behavior
for everything short of that.

## 6. Next build step
Build the fault-injection harness first, before the real variation mechanism: a minimal render
pipeline with the five variation variables, the render-gate above in Zag, and the 10,000-fault
injection trial with the kill bar wired in as assertions. If the harness cannot be killed by
control experiments (injecting faults with the detector disabled must produce detected verdict
drift), the trial is broken — fix it before testing the real mechanism.

### Attack surface (worst case must be: at most boring phrasing)
- **Salience weights** — attacker-reachable via crafted inputs (accepted sensor-deceivable
  hole). Worst case: skewed emphasis/ordering of a truthful verdict. Still the same verdict.
- **Elaboration budget** — partially reachable (long inputs push depth); clamped to prereg
  range, out-of-range → NULL variation. Worst case: terse default phrasing.
- **Recency/ordering weights** — reachable via salience. Worst case: different presentation
  order of identical content.
- **Context pointer** — internal only; cross-checked against ledger. Worst case on corruption:
  NULL variation for one turn. Not attacker-influenced by input alone.
- **Memory strength / judgment weights** — NOT in the variation input set; any prereg that
  adds them is rejected by the separation invariant. Worst case if leaked in: unverifiable —
  hence forbidden, not mitigated.
