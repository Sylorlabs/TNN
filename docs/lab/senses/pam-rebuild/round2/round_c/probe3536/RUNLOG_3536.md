# RUNLOG — PAM round-2 probe crew P-C: H-PAM-35 / H-PAM-36 cheap probes

Date: 2026-09-24. Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Scratch: `~/workspace/pam_probes_3536/` (never /tmp). Pure Zag, zero RNG.

## 1. Prereg extraction (by script, from frozen Round-C commits)

- `extract_preregs.py` fetched, via the GitHub REST API (`gh-api`), from:
  - prereg-alone commit `0db769f2` → `docs/lab/senses/pam-rebuild/round2/round_c/PREREG_ROUNDC_PROBES.md`
    (covers H-PAM-29..34; confirmed it does NOT contain 35/36 probe preregs)
  - evidence commit `64daa8b6` → `docs/lab/senses/pam-rebuild/round2/round_c/preregs/PREREG_HPAM35.md`
    (blob b0debc116caaab39c91d712af6ee18608047cd81) and `PREREG_HPAM36.md`
    (blob 2691e0169e6fd972439e9609f8f3246600ff2349), both marked DRAFT (not frozen)
  - same commit → `grok_objections_roundc.md` (blob 72dd55375d69170d64dd12314341c3e9ea08f78d),
    read before building; `HYPOTHESES_ROUND_C.md` §7/§8 (blob 824c1a1a0c4c99df32d7178bc2111f41303eeb90)
- Review: drafts complete in structure but unpinned (no fixture counts, no
  latency bound, no search budgets, no exact formulas). Amended → new FROZEN
  versions committed ALONE (no code) as commit
  `0a48bdbad25cbc358b7836e7cd34a33b248c7cfa` on `tnn-native-lab`:
  `preregs/PREREG_HPAM35_FROZEN.md`, `preregs/PREREG_HPAM36_FROZEN.md`.

## 2. Build

```
cd ~/workspace/pam_probes_3536
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 hpam3536_probe.zag -o hpam3536_probe
# znc: warning: zagd unavailable; foreground compilation continues without background planning
# znc: wrote native binary hpam3536_probe (77256 bytes main, 0 external tools)
```
Clean first-try build (no errors). Binary NOT committed (stays in scratch).

## 3. Runs (3× per mode, stdout SHA-compare)

```
./hpam3536_probe 35 > outputs/o35_1.txt   # rc=0
./hpam3536_probe 35 > outputs/o35_2.txt   # rc=0
./hpam3536_probe 35 > outputs/o35_3.txt   # rc=0
SHA-256 (all three): 60cd2abe393fcb5eae42a6a86d9f51ea3435f1ae8e5d1bd10c5f61fbba14280b

./hpam3536_probe 36 > outputs/o36_1.txt   # rc=0
./hpam3536_probe 36 > outputs/o36_2.txt   # rc=0
./hpam3536_probe 36 > outputs/o36_3.txt   # rc=0
SHA-256 (all three): d71bb9be0751d9004437f51f787fcfc99958b870bc8c4fc4af678330c54d1af3
```
3/3 byte-identical per mode. No VOID.

## 4. WG3 source audit

`wg3_audit.sh` run against `hpam3536_probe.zag` → `wg3_audit.txt`:
CLEAN — adversary fixture fns (`adv_low`, `adv36_conf`, `adv36_meas`, `forge`,
`oracle`) take only scalar args; CAP constants flow only to tag/verify paths;
NONCE constants appear only inside harness-side `wstep`; `wstep` call sites all
in m36 harness sections.

## 5. Results vs bars

### H-PAM-35 (mode 35, SHA 60cd2abe…)
| check | measured | bar | result |
|---|---|---|---|
| (a) low→sink flows | 0/760 admitted (D1 0/240, IF1 0/80, IF2 0/80, IF3 0/80, IF4 0/80, IF5 0/40→80, G1 0/120) | 0 | PASS |
| (b) gadget w/o verdict | 0 (in (a)) | 0 | PASS |
| (c1) verdict gates | H2 0/40 admitted | 0 | PASS |
| (c2) honest latency | H1 60/60 admitted, max delay 0 | ≥57/60, delay 0 | PASS (no demote) |
Non-vacuity: sinks fire on valid tags (H1 60/60); tag binds content (G1 replay
40/40 refused); verdict bit genuinely gates (H2 0/40).

### H-PAM-36 (mode 36, SHA d71bb9be…)
| check | measured | bar | result |
|---|---|---|---|
| (a) frozen | 0/60 false admits | 0 | PASS |
| (b) RC reactive | 0/60 false admits; 0 W-recoveries in 300k evals | 0 | PASS |
| (c) WG independence | WG1 120/120 identical; WG2 0/200000 | identical, 0 | PASS |
| (d) honest | 60/60 admitted | ≥57/60 | PASS |
| WG3 audit | CLEAN | clean | PASS |
Non-vacuity: honest admits 60/60 (predicate not always-refuse); frozen blind
guess is the optimal blind strategy (uniform honest reading; joint hit prob
≈2.25e-6/trial); RC preimage is 64-bit (budget-infeasible).

## 6. Verdicts

- **H-PAM-35: TESTED-survived** — capability-typed inertness holds its cheap
  probe: 760 adversarial low→sink presentations (direct, 5 IF paths, 3 gadget
  shapes incl. tag replay) all refused; honest high path 60/60 at delay 0.
- **H-PAM-36: TESTED-survived** — commit-then-sample holds its cheap probe:
  frozen 0/60, reactive 0/60, sample channel empirically disjoint (WG1/WG2/WG3).
  33-renamed check: structure differs from H-33 (author-written percept bytes;
  sample is a pure independence bit, no content endorsement) — not a rename.

## 7. Residuals (recorded, not patched)

- 35: Zag cannot make `HighVal` construction private — tag unforgeability
  carries the barrier in the toy; a real implementation needs a language-level
  private constructor. IF enumeration fixed at 5 paths; latency measured
  against an oracle trainer (triage trap deferred to a real trainer).
- 36: toy disjointness rests on harness ownership of W/NONCE; a real
  deployment must exhibit a physical/organizational channel with the same
  property (open construction question).
