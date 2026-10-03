# AUDIT-Q0 — Baseline audit: does any imagination mechanism already exist?

Date: 2026-09-22. Prereg: `PREREG.md` (frozen 2026-09-22, commit
`6603e8dd6a025d722c8ede5e607acad6f26f72a3`).

## Finding: NONE — no offline sensory-imagination mechanism exists

Searched for: a scene buffer, an offline simulation partition, any
construct-then-query sensory representation, any "imagine/visualize in
head" construct. All repo `.zag`/`.md` under `senses/` were searched
(2026-09-22); only the `b_percept` machinery below is human-style sensory
code, and it is live-classification only.

### What DOES exist (evidence it is not imagination)

| File | Line(s) | What it is |
|---|---|---|
| `senses/rebuild/b_percept/percept.zag` | 1–24 (header) | "Handles + fixed relation tables + composition ONLY. This file touches NO fixture bytes and performs NO arithmetic on raw sensory numbers." |
| `senses/rebuild/b_percept/percept.zag` | 32–282 | Handle vocabulary + fixed tables only: color handles (1000–1071, 2000–2004), shape tuples (3000s/3100s/3200s), pitch/timbre/motion handles, `pc_color_dist`, `pc_pitch_cmp`, `pc_shape_decide`. No scene store, no construct op, no offline query. |
| `senses/rebuild/b_percept/sense.zag` | 4, 29, 153–180 | Wiring only: "parse args, read the fixture, hand bytes to the transducer"; fixture bytes → transducer → percept vote. Live input in, classification out. |
| `senses/rebuild/b_percept/transducer.zag` | (698 lines) | Raw-number transducer: RGB/PCM/frame bytes → percept handles. |
| `senses/rebuild/b_percept/PERCEPT_DESIGN.md` | "The boundary (load-bearing)" | States the contract: transducer converts numbers to handles; `percept.zag` "reads no fixtures"; `sense.zag` "loads fixture bytes, calls the transducer, asks the percept side for the decision, prints the report." |
| `senses/rebuild/b_percept/PERCEPT_DESIGN.md` | Vocabulary table | 155 fixed handles: 72+5 color, 4+3+4 shape, 48 pitch, 4 timbre + 3 timbre-evidence, 9+3 motion = 155. |

No file under `senses/` (or elsewhere in `~/workspace/tnn-lab` outside
`imagination/`) defines: a persistent scene buffer, a construct-then-query
representation, an offline simulation partition, or any op that builds,
retains, edits, and queries an internal sensory scene. The b_percept
machinery classifies LIVE transducer input into handles and discards it.

## Verdict

Q0 audit result: **NONE FOUND** — the recon result (2026-09-22) stands.
Per Micah's order ("if not done then it needs to be"), the mechanism had
to be built: `imagination/src/imagine.zag`.

---

## Appendix A — Signed-sentinel audit of `imagine.zag` (2026-09-22)

`ig_get32` (`imagine.zag` lines 37–40) reconstructs words WITHOUT sign
extension: a stored `-1` reads back as `4294967295`. Every `-1` use was
audited:

| Site | Lines | Behavior with unsigned read | Verdict |
|---|---|---|---|
| Human STRUCT `-1` rel-target installs (scenes 9–12, `ig_q1_scN` and mirrored `ig_q1_pre`) | 1519, 1540–1541, 1561–1563, 1583, 1585, 1731, 1742–1743, 1753–1755, 1764, 1766; also scene-10 edit `ig_eattr(ar,2,4,-1)` | target slot reads as 4294967295 | deterministic |
| `ig_q_support` human chain, line 379: `if (cur < 0 \|\| cur >= ig_n(ar))` | 377–380 | `cur < 0` is DEAD for unsigned reads (4294967295 is never < 0); the `cur >= ig_n(ar)` disjunct catches it → returns 0 (unsupported) | correct outcome, dead first disjunct (documented, not changed — frozen code) |
| `ig_q_topmost` human chain, line 465: `if (cur < 0 \|\| cur >= n)` | 462–466 | same: `cur >= n` catches → `cur = i; guard = 99`, chain walk terminates | deterministic, no hang |
| `ig_q_relation` human, lines 416/419: `ta == b`, `tb == a` | 414–420 | 4294967295 never equals a small element index → falls through to zone-based relation | deterministic |

No signed sentinel reaches any arithmetic (no `z == 0` style check on a
`-1`-capable slot in a path that could read 4294967295: machine STRUCT
`z` slots (line ~388) only ever hold non-negative cm values in Q1–Q3).
No hang, no miscompare, no nondeterminism. The `cur < 0` disjuncts are
latent-dead under unsigned reads; behavior is fully defined by the
`cur >= n` disjunct. Flagged here rather than "fixed" because the code is
frozen post-build; any change would need a dated amendment.

## Appendix B — Pitch-handle wording gap (spec vs code)

`PREREG.md` says human AUDIO uses "pitch-bin handle 4000–4047 (bin =
round(12·log2(f/110)), clamped)". The implementation stores the ordered
bin INDEX (0..47, e.g. 15–27 in the Q1 scenes) in the pitch slot, with
timbre handles 5000–5003 beside it. Pitch order IS handle order per
b_percept (`pc_pitch_cmp`), and the index range is disjoint from machine
Hz values, so mode vocabulary stays disjoint — but the `4000–4047`
wording in the prereg does not match the code. Flagged for GEN-2
assessment; not silently corrected.
