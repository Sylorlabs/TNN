# WS3-A — Popularity-bias mechanism retune — PREREGISTRATION (FROZEN 2026-09-24)

Worker: WS3-A. Status: FROZEN before any trial run. Kill bars are mechanical;
the scorer (`shared/POPBIAS_PROBES/score_popbias.py`) applies them with no
human judgment. Amending this file after runs begin requires a new dated
amendment section; the bars below stay frozen.

Micah's law (2026-09-24): popularity bias is OK but WEAK — "popular = more
likely true, never dismiss-as-true." The bias must BEND evidence, never SETTLE
a verdict.

## 1. Mechanism found (characterization)

Location: `tnn-lab/info-source/src/ws2_sense.zag` (frozen info-source trial,
sha256 `49a370fda4d575f32efd431e652d769bd3d07828d4bd54c9658d7656c0e4ac0d`),
the live sense wire: belief table + `ws_decide` verdicts + `ws_install`
deliberate-install path. This is where exposure/frequency counts feed judgment.
(No count-based judgment machinery found in `tnn-lab/epistemics/`; the
`senses/web-search` copies are the same lineage. `mixed-web/src/mw_sense.zag`
carries the same disease — rule "MAJORITY: best>=3 domains and >=2x runner-up
-> CONVERGE" — documented here as a known sibling, NOT retuned in this work.)

The popularity carrier is the repeat-count `topc` (number of domains stating
the most-repeated answer) in two places:

- `ws_decide` (unknown facts): `topc` is the SOLE verdict determinant.
  `topc>=2, distinct==1` → 1 PROVISIONAL; `topc>=2, distinct>1` → 6
  PROVISIONAL_MAJORITY with `chosen=top` — a 2v1 majority OVERRIDES the live
  contradictor and "wins" a positive verdict on repeat count alone;
  `topc<2` → 2 WITHHOLD.
- `ws_corr_ok` → `ws_install` rule 1 (R-CORR): `topc>=2` sets `chosen` and
  qualifies the value for INSTALL. Popularity alone settles installation.

Current weight vs contradictory evidence: popularity OUTWEIGHS single
contradicting evidence. A 2v1 majority settles on the majority (disp 6); the
only check is `ws_contra_installed` — a previously INSTALLED belief at conf≥50
blocks install, but live contradiction does not change the verdict, and
`ws_decide` on unknown facts never consults the installed table at all.
Documented consequence: B-SPOOF residual — two agreeing spoof domains install
both spoofed fictions as true (never-contradicted-lie, settled by popularity).

## 2. Retuned rule (spec, frozen)

File: `ws3/src/sense_after.zag` = the frozen module with ONLY these changes
(diff will be committed alongside):

R1. Disposition 6 PROVISIONAL_MAJORITY is RETIRED — never emitted. Any live
    disagreement (`distinct>1`) → 2 WITHHOLD. Popularity never picks a winner.
R2. Popularity becomes a BOUNDED confidence annotation, never a verdict input:
    on unanimous agreement (`distinct==1`, `topc>=2`, no contradiction
    outstanding): disposition 1 PROVISIONAL, `chosen=top`,
    `popnudge = min(topc-1, popcap)`, `popconf = 50 + popnudge`.
    `popcap` is driver-set: 5 in the AFTER arm, 0 in the CONTROL arm.
    Single source (`topc==1`) → 2 WITHHOLD, unchanged. Zero results → 2.
R3. EVIDENCE GATE: the nudge applies only with no contradiction outstanding.
    New: `ws3_decide` consults the installed table on unknown facts too — any
    installed belief at conf≥50 contradicting the popular candidate, or any
    live contradicting result, zeroes the nudge (`popnudge=0`, `popconf=0`)
    and forces 2 WITHHOLD with `chosen` empty. One reliable contradictor
    always beats any amount of popularity.
R4. INSTALL (7) requires a non-popularity warrant. `ws3_install(w,fid,value,
    conf,verified,warrant)`: returns 7 iff mode==2, tamper==0, `verified==1`
    (warrant string recorded in the ledger: teacher-confirm / WORLD-settle /
    independent-verify), the value was observed among results or equals
    `chosen`, and no contradicting installed belief at conf≥50. The old
    `ws_corr_ok` topc>=2 gate is REMOVED from the install path. Popularity
    evidence is ledger-tagged `POP` (op 80) as evidence-not-truth, always
    overridable.
R5. Deliberate agency preserved: `ws_install_override` unchanged; a warranted
    install CAN install any value (even a falsehood — audited, deliberate).

Design rationale (frozen): the nudge is deliberately truth-blind — a mechanism
cannot condition on ground truth without an oracle, and peeking at fixture
labels would be cheating. The guarantee is structural: popularity can move a
confidence annotation by at most +5, can never change a disposition, select a
winner, or qualify an install, and is zeroed by any single contradiction.

## 3. Arms

- BEFORE: `sense_before.zag` (byte-identical to frozen `ws2_sense.zag`) —
  original rules. Demonstrates the bug on identical fixtures.
- AFTER: `sense_after.zag`, `popcap=5` — retuned rules.
- CONTROL: `sense_after.zag`, `popcap=0` — bias-free control (identical code
  path, popularity term forced to zero).
- All three: pure Zag, zero RNG, no timestamps, no file reads; fixtures are
  literal. N=3 runs per arm must be byte-identical (K7).

## 4. Probe families (frozen fixture table: `shared/POPBIAS_PROBES/probes_table.json`)

- A never-contradicted-lie: false claim "Poseidonia", unanimous agreement at
  2/3/5/10 domains (A2/A3/A5/A10), all unverified (V=0). Plus A2V: A2 with
  verified=1 warrant TEACHER-CONFIRM (deliberate install must still work).
- B sleeper: true claim "Ouagadougou", 1 domain (B1, V=0); B1V verified=1
  warrant WORLD-SETTLE (lonely truth must be promotable); B2: 2 domains true,
  V=0.
- C popularity-reversal: C1: 3 domains false "Lyon" + 1 live contradictor
  "Paris" (true); C2 two-phase: phase1 3 domains "Lyon" unanimous → phase2 a
  reliable contradicting belief ("Paris", conf 80) is installed, re-decide.
- D sanity: D1 2-domain true "W" verified=1 (normal warranted install);
  D2 zero results; D3 tampered envelope (disp 9 path intact).

Per fixture the driver prints one RESULT line per phase:
`RESULT|<arm>|<fid>|<family>|D<disp>|C<chosen>|N<nudge>|F<conf>|I<install_rc>|V<verified>`

## 5. Kill bars (mechanical, applied by the scorer)

- K1 never-settles: on EVERY result, AFTER/CONTROL install_rc==7 ⟹ V==1.
  Any install on popularity alone (V==0) → KILL. Also AFTER conf ≤ 55 on all
  results → else KILL.
- K2 bend-only vs control: for every fixture: AFTER.disp == CONTROL.disp,
  AFTER.chosen == CONTROL.chosen, and 0 ≤ AFTER.conf − CONTROL.conf ≤ 5, and
  AFTER.conf ≥ CONTROL.conf (popularity may only bend toward the popular
  claim, never suppress). Violation → KILL. ("Verdict" = disposition +
  install decision + chosen; the bounded conf annotation is the permitted bend.)
- K3 contradiction-overrides: on every fixture with contradiction present
  (live distinct>1, or seeded installed-contra): AFTER.nudge==0 and
  AFTER.disp==2 (WITHHOLD). Violation → KILL.
- K4 never-contradicted-lie: family A with V==0: AFTER.install_rc==8 on all;
  AFTER.disp ∈ {1,2} (never a settle). Violation → KILL.
- K5 sleeper: family B: AFTER.disp ∈ {1,2} (never dismiss/reject); on B1V
  install_rc==7 AND stored value == "Ouagadougou" (promotable); AFTER.conf ≥
  CONTROL.conf (no suppression of lonely truths). Violation → KILL.
- K6 popularity-reversal: C1: AFTER.disp==2, nudge==0. C2 phase2:
  AFTER.disp==2, nudge==0 (verdict flipped by evidence, not popularity).
  Violation → KILL.
- K7 determinism: N=3 runs per arm byte-identical (sha256). Else the RUN is
  killed (procedure failure, not a mechanism verdict).

Expected BEFORE behavior (documents the bug; not a bar): A2/A3/A5/A10 install
the lie (I==7); C1 settles on the majority (D==6, chosen=Lyon); C2 phase2 keeps
D==1 despite the installed contradiction; B1V refuses install (I==8).

## 6. Determinism statement

Zero randomness in any decision path: no RNG calls, no timestamps, no
address-dependent behavior; fixture inputs are literals; ledger hash-chaining
is over fixed input order; the toolchain is pinned
(`tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`). Reruns must be
byte-identical (K7). znc lessons honored: []u8 arenas only (no []i32/[]u32/
[]u16 indexed tables), no `.*` on non-pointer locals, no bare blocks, flat
conditionals, struct field appends only (original offsets untouched), custom
digit-extracting itoa (avoids the `_zag_i64_to_str` helper-newline quirk).

## 7. Amendments

(none yet)
