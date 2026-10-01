# Mini-Lifetime Integration Report

Date: 2026-10-01. Worker: Mini-Lifetime Integration Worker (subagent).
Status: MINI-LIFETIME-INTEGRATION-COMPLETE. 3/3 byte-identical per arm.
Verdict: MINI-LIFETIME-INTEGRATION-COMPLETE.

## Question

Can the separately validated mechanisms (rebinding, consequence
substrate, provenance, structural protection) be integrated into one
continuing learner without interference, and does the integrated system
outperform the parts on a persistent mini-lifetime?

## Arms

- **Arm A**: frozen TNN-2 baseline (verbatim base SHA-256 a29972ca...).
- **Arm B**: base + structural rebinding (from 91585087c).
- **Arm C**: base + rebinding + shared consequence substrate store
  (sub_note/sub_consec/withhold) + provenance treatment (field-16 source
  tags, external-only bootstrap) + structural protection (PRO edges on
  MAP reference).

All arms run the same 5-phase driver, no resets, one continuous learner.

## Driver phases

1. Teach A: decoy chain (2->21->22) + main chain (1->11->12->13->14),
   promote MAPs via query.
2. Interference: 150 unrelated teach events.
3. Teach B: isomorphic chain (101->111->112->113->114), query B
   (transfer; measure trial-stat delta).
4. Contradiction: observe (1,1,999) contradicting taught (1,1,11),
   re-query A (revision).
5. Retention: re-query A and B.
Withholding probe: 5 queries on untaught (9999,88).

## Results

### Per-arm comparison table

| Metric | Arm A (frozen) | Arm B (rebind) | Arm C (integrated) |
|---|---|---|---|
| P1-MAIN ans | 14 | 14 | 14 |
| P1-MAIN tried | 3 | 3 | 3 |
| P1 live / edges | 58 / 45 | 67 / 48 | 69 / 72 |
| P2 live / edges | 208 / 199 | 217 / 202 | 219 / 202 |
| P3-B ans | 114 | 114 | 114 |
| P3-B tried | 3 | 2 | 2 |
| P3-B dtried | 0 | -1 | -1 |
| P3 live / edges | 253 / 226 | 249 / 223 | 252 / 239 |
| P4 contradict rv | 0 | 0 | 0 |
| P4-A ans | 14 | 14 | 14 |
| P5-A ans | 14 | 14 | 14 |
| P5-B ans | 114 | 114 | 114 |
| WH-0..4 ans | -2 x5 | -2 x5 | -2,-2,-2,-3,-3 |
| Final live / edges | 269 / 240 | 265 / 237 | 265 / 262 |

### Findings

**Transfer (P3-B tried)**: Arms B and C both achieve 2 tries vs Arm A's
3, a 33% reduction. The rebind mechanism works identically in the
integrated arm (C) as in the standalone arm (B). No interference from
substrate, provenance, or protection.

**Withholding (WH probe)**: Only Arm C withholds. After 3 consecutive
misses on (9999,88), queries 4 and 5 return -3 (WITHHOLD) without trial.
Arms A and B run all 5 trials (ans=-2 each). The shared consequence
substrate drives withholding in the integrated learner.

**Retention (P5)**: All arms retain A=14 and B=114. No arm forgets. The
protection mechanism does not change retention outcomes at this scale
(150 interference events insufficient to pressure eviction).

**Revision (P4)**: All arms return rv=0 and A=14 after contradiction.
The contradiction is handled by base machinery (fact shadowing, not
graph revision) identically across arms. Provenance tags do not alter
this path.

**Memory growth**: Final nodes similar (265-269). Arm C has more edges
(262 vs 240/237) from substrate records (tag 61) and PRO edges. The
overhead is bounded and does not grow with events (records keyed by
pursuit, edges by MAP).

**Compute/event**: Measured via trial-stat delta. P3-B: A=3, B=2, C=2.
Withholding saves 2 full trials in C's WH probe.

## Integration assessment

The four mechanisms compose without interference:
- Rebind transfer benefit preserved in C (2 vs 3 tries).
- Substrate withholding active only in C (-3 on repeated misses).
- Provenance and protection do not regress rebind, retention, or
  revision.
- No new modes, bridges, handlers, or semantic cases. Arm C adds
  ~250 lines (substrate store, rebind, protection, provenance tags,
  merged ev_query) with 0 new node types, 0 new edge types, 0 new
  fields (field 16 repurposed for source tags on FACTs only).

## Limits

- Scale: 150 interference events, ~270 nodes. Below eviction pressure;
  protection benefit not measurable here.
- Revision: contradiction did not trigger graph revision (rv=0) in any
  arm; the test exercises fact shadowing only.
- Examples-to-criterion: P1-MAIN required 3 tries in all arms (no
  difference); the driver has no learning-curve loop.
- Predictive accuracy: N/A (no prediction mechanism in these arms).

## Architecture accounting (Arm C)

- Cognition source lines added: ~250 (substrate 79, rebind 54,
  protection 68, provenance tags 7, merged ev_query 52).
- New hardcoded semantic cases: 0.
- New modes: 0. New bridges: 0. New task-specific handlers: 0.
- New node types: 0 (tag 61 substrate records use existing storage).
- New edge types: 0 (ET_PRO=9 existing).
- New fields: 0 (field 16 repurposed on tag-1 FACTs).
- Learner-owned: MAP graphs, rebind bindings, substrate records,
  PRO edges, source tags (values, not policy).

## Reproducibility

- 3/3 byte-identical per arm (sha256: A 25749820f2c4a025,
  B de6a9e18ed2d731d, C a0673125573b7da1).
- Pure Zag via pinned znc. Safebin active. Zero Python.
- Sources: mli_full_A.zag, mli_full_B.zag, mli_full_C.zag.
- Binaries: mli_bin_A, mli_bin_B, mli_bin_C.
