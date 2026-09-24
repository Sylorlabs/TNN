# VERDICT_HL13.md — HL-13 operator-coincidence provenance

**Workstream:** LI-HARDEN WALL-HL13. **Date:** 2026-09-24.
**Mechanism:** pure-Zag verdict-layer gate (`verdictp` mode, `build/hl13.zag`).
**Pipeline contract:** `PIPELINE_METADATA_SPEC.md`.
**Cross-check:** WALL-FABLE consult (`liharden/consults/FABLE_WALL.md`) frames
this independently as W3, Tier 3 detection-only, and confirms the blocker is
the metadata-pipeline governance decision, not verdict logic.

## 1. Mechanism

`hl13.zag` derives from Crew B's frozen `corrob.zag`. Modes
`verdict`/`verdictd`/`verdictm` are byte-behavior-identical (the HL-13 code
paths are only reachable in `verdictp`; the battery's `verdict` column
reproduces the Crew B baseline exactly). New mode `verdictp`:

1. Parses metadata lines (`A| CG| L| T| SH| PB| R| NS|`) per page into a
   separate table — P/H/S parsing is untouched.
2. After contradiction and dissent, computes, for each gate feature, the
   maximum share of winning-quorum members carrying an identical non-empty
   normalized value.
3. Emits `INFO|OPCOIN|a=N|cg=N|l=N|t=N|sh=N|pb=N|r=N|ns=N` (audit trail).
4. Blocks with `GATE|OPCOIN|<features>|<pids>` iff **≥2 features** reach
   share ≥3 within the winning quorum (fable W3 rule).

Gate features: author (A), CMS fingerprint (CG), link target (L),
timestamp (T), WHOIS registrant email (R), nameserver apex (NS).
SH/PB are report-only. Missing metadata never coincides. Duplicate keys:
last wins. Zero randomness in the decision path; 52/52 case×mode pairs
byte-identical across reps.

Policy exclusions (verdict-side, raw values kept in audit):
- **R:** WHOIS privacy-proxy strings (`redacted for privacy`,
  `whoisguard`, `domains by proxy`, …) treated as missing — millions of
  unrelated honest domains share them.
- **NS:** public-DNS provider apexes (`cloudflare.com`, `amazonaws.com`
  incl. `awsdns`, `google.com`, `googledomains.com`) treated as missing —
  shared DNS hosting is normal honest infrastructure (fable W11).

## 2. Calibration

| Parameter | Value | Basis |
|-----------|-------|-------|
| OPCOIN_MIN_SHARE | 3 | quorum-sized: fires on 3/3 ring quorums |
| OPCOIN_MIN_DIMS | 2 | fable W3 ≥2-features rule; measured: the 1-dim rule falsely blocked an honest shared-byline quorum (X_MFORGE_frame), the 2-dim rule keeps all 5 attack kills and removes that false positive |
| wc floor | 3 | gate requires a 3-member winning quorum |

The `INFO|OPCOIN` share report lets any alternative (share, dims)
threshold be re-derived from logs without rebuilding.

## 3. Measured evidence (battery 2026-09-24)

26 cases × 2 modes (`verdict` baseline, `verdictp`) × 2 reps = 104 runs,
52/52 decision-identical across reps, zero stderr.

| Case | Baseline | verdictp | Gate |
|------|----------|----------|------|
| R3_ring3 (glue residual) | INSTALL (false) | **blocked** | A+CG+L+T |
| R4_ring4 (glue residual) | INSTALL (false) | **blocked** | A+CG+L+T |
| M3_false_majority (glue residual) | INSTALL (false) | **blocked** | A+CG+L+T |
| E_LD3_distinct_cites | INSTALL (false) | **blocked** | A+CG+T |
| E_TS3_staggered_time | INSTALL (false) | **blocked** | A+CG+L |
| X_MDIV_partial (A diversified) | INSTALL (false) | **blocked** | CG+L+T+R+NS |
| X_MDIV_full (A/CG/L/T diversified, shared infra) | INSTALL (false) | **blocked** | **R+NS** |
| H1–H12 Crew B honest | 12/12 install | **12/12 install** | — |
| X_HMETA_honest (diverse + privacy/Cloudflare) | install | **install** | — |
| X_MFORGE_frame (shared byline only) | install | **install** | — |
| X_MDIV_hard (fully diversified incl. R/NS) | install (false) | install (false) | — |
| R2 / P3 / M1 / M2b | withheld (contradiction) | unchanged | — |

**Closure:** 7 false installs closed (R3, R4, M3, E_LD3, E_TS3,
X_MDIV_partial, X_MDIV_full). Against the convergence draft's seven glue
residuals specifically: **3/7** (R3, R4, M3). **Honest cost: 0/15**
(12/12 Crew B baseline + 3 enriched honest fixtures install).

## 4. Marginal gain of the R/NS features (the parent's question)

Counterfactual from the measured share vectors (4-feature ≥2-rule vs
6-feature ≥2-rule):

- **+1 kill:** X_MDIV_full — the attacker who diversifies all content
  metadata (A/CG/L/T all share=1) but reuses one registrar account and
  one DNS provider (r=3, ns=3) is now blocked (`GATE|OPCOIN|R+NS`).
  Without R/NS this evasion is completely invisible to the verdict layer.
- **+0 honest cost:** X_HMETA_honest (all three pages `REDACTED FOR
  PRIVACY` + `cloudflare.com`) measures r=0, ns=0 after the proxy
  exclusion and provider whitelist — the realistic honest
  shared-infrastructure shape does NOT fire. H1–H12 (`META=NONE`)
  unaffected.
- The ≥2-dims rule itself (vs the earlier 1-dim calibration) removed the
  X_MFORGE_frame false positive (shared wire byline, A-only) with zero
  kills lost — every blocked attack coincides on ≥2 features.

Net assessment: R/NS are worth including. They are cheap (~$0.01/query),
deterministic when cached/versioned, and convert the full-diversification
evasion from "passes silently" into "blocked on infrastructure reuse" —
provided the proxy-exclusion and provider-whitelist policies ship with
them. Without those two policies, R/NS as lone gate features would tax
honest shared infrastructure (WHOIS privacy, Cloudflare); the ≥2-feature
rule plus the exclusions is what makes them safe.

## 5. Red-team (self)

- **X_MDIV_full** (diversify A/CG/L/T, reuse R/NS): blocked — the lazy
  operator is caught (fable's F_M3_NAIVE equivalent).
- **X_MDIV_hard** (diversify everything incl. 3 registrant emails, 3 DNS
  providers): **installs — the hardened wall stands** (fable's
  F_M3_HARDENED prediction confirmed). Adaptation cost per fable: ~2h +
  ~$50. This is the structural ceiling: no host/metadata predicate
  separates a fully-diversified operator ring from honest corroboration.
- **Forgery direction:** R/NS are fetcher-observed (WHOIS/RDAP/DNS), not
  page-asserted — the attacker cannot forge them in HTML, only diversify
  by changing infrastructure (the cost-raising property).
- **Threshold evasion:** share floor is 3 = quorum size; a 2-member
  coincidence never fires (wc≥3 required). Splitting a ring across
  >3 domains to dodge the share count costs the attacker quorums.

## 6. Structural limitation (stated plainly)

HL-13 is Tier 3 **detection-only / cost-raising** (fable W3: KEEP as
cost-raiser $10→~$60, not a seal). A fully diversified operator ring is
host/metadata-shape-identical to honest corroboration — no verdict-layer
predicate closes it. Timestamp handling is exact normalized equality
(zero-width cluster); a calibrated time-window cluster is future work.
The mechanism raises attacker cost and catches lazy operators; it does
not hermetically seal the wall.

## 7. The actual blocker (pipeline governance)

The verdict layer is done and calibrated. It is inert on production
traffic until the fetch pipeline emits metadata — today the production
glue is forbidden to emit it. `PIPELINE_METADATA_SPEC.md` is the
concrete contract (fields, format, trust levels, ~$0.03/quorum WHOIS
cost, fail-open semantics, raw-value emission with verdict-side
policy). The governance call goes to Micah; the verdict mechanism and
the spec are built regardless.

## 8. Reproducibility

- Source: `build/hl13.zag` (+ `build/R33_NATIVE_IO_V1.zag`); no binaries
  or `.zagd` in the repo.
- Build: pinned `znc_linux_x86_64_abed8aa1`, `hl13.zag -o hl13_bin`
  (warnings inherited from Crew B code).
- Battery: `run_hl13_battery.sh` → `evidence/battery_hl13/` (104 runs);
  fixtures in `fixtures_rt/`; frozen cases referenced, never modified.
- Determinism: 52/52 case×mode pairs byte-identical across reps;
  zero RNG in any decision path.
