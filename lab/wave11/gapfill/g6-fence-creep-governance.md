# G6 — Fence-creep / amendment-process governance (T2 gap fill)

## 1. Slice
T2 gap: governance of the prereg-enumerated RNG injection-point set — per-point re-approval
enforcement, cross-amendment diff-audit, and detection of entropy laundering (boundary
widening one reasonable amendment at a time). This slice is governance, not AI decision machinery.

## 2. Falsifiable claim
A governance gate that (a) requires every enumerated injection point to be explicitly
re-authorized per amendment with logged attribution, (b) diff-audits the point set across
amendments, and (c) flags boundary-widening automatically, catches 20/20 of preregistered
synthetic entropy-laundering sequences with zero false accepts on 20/20 benign
re-authorization sequences. One missed laundering sequence or one false accept kills it.

## 3. Design
Per-amendment manifest (checked into git beside the amendment file, hashed into the
attestation header of slice 09's build gate):

```zag
struct InjPoint { id: i64; fn_sig: u64;          // fn + arg-type hash
                  rng_region: u64;              // hash of allowlist subgraph consuming rng
                  auth: Authority; }            // {who: Attrib, date, amendment_id}
struct AmendManifest { amend_id: Str; supersedes: Str;
                      points: [InjPoint];      // EVERY point, re-listed
                      justification: [Str]; }  // one line per point, why still fenced-needed
```

(a) Per-point re-approval. Rule: an amendment authorizes exactly the points it enumerates —
default-deny, sunset-by-default. A point absent from the new manifest loses its authorization;
builds attesting it fail the slice 09 gate. Re-enumeration must cite the original authorizing
amendment (`supersedes`) and carry fresh logged attribution (`auth.who`, coordinator or Micah).
(b) Diff-audit. `diff_points(old: AmendManifest, new: AmendManifest) -> Diff` computes
{added, removed, region_widened}: a point is `region_widened` if `rng_region` changed or the
fn signature hash changed to a superset (e.g. "tie-break among equal" → "tie-break among
top-k"). Any `added` or `region_widened` entry auto-flags: build blocked until a second
approver (Micah, per the 2026-09-20 amendment's review clause) co-signs a widening entry
{what, why safe, paired probe}. `removed` entries auto-pass — shrinkage is always safe.
(c) Laundering catch. Every flagged widening must ship a paired outcome-independence probe:
differential run (≥200 cells, Arm B vs seeded-identical replay) asserting zero divergence in
verdict records, memory-op sequences, refusal triples, ledger bytes (slice 01's K1/K2).
Probe result is part of the manifest; a widening without a passing probe = amendment
invalid, build blocked.

## 4. Kill bar
Governance is dead if ANY fires: (i) <20/20 synthetic laundering sequences caught by the
diff-audit (20 preregistered widenings: 6 fn-sig expansions, 6 allowlist-subgraph growths,
8 "reasonable" justifications without probe results); (ii) ≥1 false accept among 20 benign
re-authorizations (identical set re-listed, fresh attribution); (iii) one amendment ships an
Arm B build whose attested point set differs from the manifest on file; (iv) one widening
enters a canonical-path build (slice 09 K-gates fire transitively — containment stands).

## 5. Honesty notes
Weakest point: the manifest and diff run OUTSIDE the build — a coordinator who forges the
manifest defeats everything, same trust assumption as slice 09's honest-build-driver note.
Mitigation: manifest hash chain committed to git and verified at startup (slice 09 honesty
note), plus the probe result is mechanically checkable — a widening without a real probe
run cannot fabricate passing differential numbers without breaking replay checks.
Second: "reasonable justification" is judgment, not math; the design converts it into a
probe obligation rather than trying to judge reasonableness directly. I am NOT claiming
this stops a malicious Micah or a malicious coordinator — it makes creep VISIBLE and
mechanically auditable, so each widening is an explicit, attributable, probe-backed act.
Scope: covers only the injection-point set; does NOT cover seed-schedule secrecy (A1/A2)
or chooser/logger desync (A3) — those are t3 slice 12's battery.

## 6. Next build step
Build the manifest schema + `diff_points` + the flag rule, and run the 40-sequence
synthetic battery (20 laundering, 20 benign) BEFORE any new amendment is drafted — the
first missed widening or first false accept is the single most informative outcome.
