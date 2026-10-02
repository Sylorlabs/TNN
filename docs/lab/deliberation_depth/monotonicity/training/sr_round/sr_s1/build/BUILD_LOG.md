# SR-S1 build log — RESUME after daemon restart (2026-09-24 ~17:15 PDT)

Inherited state (verified, kept):
- src/train_sr1.zag — diffed against v2 train2.zag: identical except the
  §5b mask update block, log header (prereg SHA first), and params.txt
  handoff. Mask implements grok Q1 Scheme 1(a) exactly:
    k3==4||k3==6 (w5,w7): num=10*err*fk, theater coeff 0
    k3==1||k3==7 (w2,w8): num=2*err*fk+8*rise*fk (ordinary v2)
    k3==0 (w1): ordinary, num=0 iff f7(feats slot 6)==1000 (pin firewall)
    k3 in {2,3,5} (w3,w4,w6): num=0
    bias: ordinary v2. G-batch, anti-saturation clamp, telemetry: unchanged v2.
- MASK_INTEGERS.md — checked against grok_sr_Q1.txt Scheme 1(a) verbatim:
  B=5, num_i=10(C-Y)f_i, floor 4000, f5=280→|C-Y|≥15, full-error step −70,
  f7=1000→|C-Y|≥4, i∈{2,8}+b ordinary w/ theater, i=1 pin firewall,
  i∈{3,4,6} num=0, expected lock (w7≈−1500, w2∈[−400,−100], w6=0, w1≈1000),
  Stage-2 epoch reading (2 phase-passes = Phase A ep0+ep1). KEPT, not redone.

## Frozen pins (recorded BEFORE the first run)

prereg_sha        f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30
  (PREREG_SR.md FROZEN v1, commit cab05d07; matches file on disk and the
   train_sr1 log-header line)
grok_design_sha   08d09e6b82945388603ab5668584cc87471dea7c3dcbf67219722864ee69f579
  (GROK_SR_DESIGN.md, matches cab05d07 tree)
mask_integers_sha 473ff97a2123497baed76e999e4e0f3932ebf7b8203ece0c3760d36fac03d721
  (sr_s1/MASK_INTEGERS.md)
mask_code_sha     b5072de4ffd53cf876282b719f60f0f7317fc94c299ce2b4a1e5665c674f4a2b
  (sr_s1/src/train_sr1.zag)
killbar_table_sha 45993f7bd2415d19a16cdcb4dbbe66e2d2597cccc3800606a4fcfd824f6a83e3
  (§10 table extracted verbatim into work/KILLBAR_TABLE.txt)
init_sha          2f4c0b472797417bf0441eafa524c9f585613736dcede6a2f709acd3479ebcf9
  (canonical init vector "w1=1000,w2=0,...,w8=0,b=0" newline-terminated;
   v2 §4 frozen init)
features_sha      4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d
  (training/features/features.tsv — matches §2 frozen pin)
train2_ref_sha    2dcb9969e44e6ca037eb6c799cecef99b8f0d701e61c8e35f946f25b1420a7eb
  (v2/src/train2.zag — Stage-1 base behavior byte-reference)
v2_100x_ctl_sha   8c826a42cdac7ef942742816002a27fcdc6b6d8985ed73c5643d8ec
  (v2/params/mt2_params_100x.zag — CTL yardstick, §9)
znc_sha           498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 — pinned only)

Build dirs: build/train_a, build/train_b (A/B). Mirrored src tree
(training/src/*.zag) + train_sr1.zag; @import resolves against cwd
(AGENTS.md: znc resolves @import relative to cwd).
Arena compliance: all large tables on []u8 arenas w/ au_get32/au_get64 LE
accessors (inherited from train2.zag); no `as []i32` casts in mask code;
weights arena = 8×8 bytes []u8 (no consecutive same-size casts).

## 2026-09-24 resume: params.txt writer bug fix (build note, not prereg amendment)
First 10x attempt panicked AFTER a successful 60-epoch run (log + params.zag
complete): the params.txt path writer scanned `params_path[pi]!=0` for a NUL
terminator, but _zag_arg slices are not NUL-terminated (AGENTS.md) → slice
index out of bounds at pi=len. Fixed to bound by params_path.len (pi<ppl).
Training loop untouched. Rebuilt A/B.
mask_code_sha (fixed) de0825ec71bcb9294e0df4631e80f0962beec0d5ec99409314f8013d882a8635
train binary A/B  480a96a04860d8aeb0c5a5e3350a71b59a02c5933058ef10064ac6f7e9cf0809 (cmp identical)

## 2026-09-24 ~17:24 PDT: COORDINATOR RULING on the 10× go/no-go (recorded verbatim)

"I verified the raw log (log_10x_a.tsv): w7 = 3035→1785→535 across epochs 57–59, clean −1250/epoch steps matching the diagnosed 5-wrong-pin pull. grok's w7<0 point estimate assumed ~30 wrong pins; the frozen data has 1985 correct / 5 wrong, so the bar's premise was wrong while the bar's intent (separator channel live and responsive) is satisfied — w5=+32886 theater-detached, w6≡0, theater fired 29/60 epochs, mcC=0.884. RULING: bounded gate-extension — run up to 5 more Stage-1 epochs (60–64) from the epoch-60 snapshot; stop as soon as w7<0. If w7<0 within that window, the literal §5b go/no-go is satisfied and you proceed to 100× Stage 1 (600 epochs total incl. the extension epochs) then the Stage-2 disconnect. If w7≥0 after epoch 64, STOP and report back — the dynamics differ from the diagnosis. This ruling adjudicates a gate criterion only; kill bars B1–B13 and §11 are untouched."

## Resume method: deterministic forward run (build note, not a prereg amendment)

train_sr1.zag has NO params-resume path — it inits from the frozen v2 §4
vector (w1=1000, rest 0, b=0) and is fully deterministic (zero RNG, fixed
file order, fixed init, integer arithmetic; A/B byte-identical). Running
passes=11 (66 epochs) from frozen init therefore reproduces the 10× run's
epochs 0–59 byte-identically and extends with epochs 60–65 — EXACTLY what
a resume-from-epoch-60-snapshot would produce, with zero changes to the
frozen mask code (mask_code_sha unchanged). Verification: (i) 11× log rows
0–59 byte-identical to committed log_10x_a.tsv; (ii) epoch-59 weight row =
committed params_10x_a.txt. The gate reads epochs 60–64 only; epoch 65 is
free deterministic telemetry. If w7<0 at epoch 60 (predicted ≈−715 from the
−1250/epoch pull), the gate clears at the first extension epoch.
No driver change, no new binary: the committed A/B binaries are reused
(cmp-verified before the run).

## 2026-09-24 ~17:30 PDT: gate-extension run COMPLETE — gate NOT cleared

Run: passes=11 (66 epochs), A/B byte-identical, rc=0 both.
- Determinism: 11× log rows 0–59 byte-identical to committed log_10x_a.tsv;
  epoch-59 weight row = committed params_10x_a.txt. Extension epochs are
  exactly what a resume-from-snapshot would produce.
- Gate window epochs 60–64: w7 = 1833, 1833, 1833, 3083, 1833 — ALL ≥ 0.
  (My build-log prediction of ≈−715 at epoch 60 was WRONG: actual +1833.)
- RULING OUTCOME: w7≥0 after epoch 64 → STOP per the ruling. No 100× run.
  No Stage-2 run. Full dynamics characterization in
  analysis/GO_NOGO_EXT.md.
- Headline finding: the −1250/epoch steps are PHASE-C-LOCAL, not secular.
  Pin cells: Phase A 1950 correct/0 wrong, Phase B 35/0, Phase C 0/5
  (frozen features.tsv). w7's feature IS the pin flag → Phase A/B correct
  pins push w7 UP (×10 boost), Phase C wrong pins pull DOWN; net ≈ +48/pass.
  Pass-end w7 crossed zero UPWARD at pass 4 (−629…−312 → +314…+583,
  monotonic rise over 7 passes). The 10× cutoff caught the oscillation
  trough. G-batch drags b → −27401, keeping correct pins underconfident
  (mcC=0.884 — the diagnosis's C=1000-saturation premise is refuted), so the
  upward driver STRENGTHENS with |b| while the 5-pin pull is constant: no
  reversal mechanism; continued Stage 1 cannot clear w7<0. Bar-premise
  failure (grok's ~30-wrong-pin estimate vs 5 in the frozen data), not a
  mechanism failure — the bar's intent (separator live/responsive) is met.
- Coordinator decision pending: (a) waive/clarify the literal bar via prereg
  note → 100× + Stage 2; (b) kill SR-S1 at the gate; (c) amend Stage-1
  design (not recommended without amendment). Crew holds until ruling.

## Stage-2 driver: train_sr2.zag WRITTEN and §5b-verified, HELD (unbuilt/unrun)

src/train_sr2.zag — SIGNAL_DISCONNECT per §5b: init from Stage-1 snapshot
txt (9 lines w1..w8,b); mask code path ABSENT (audit: no 10*err boost, no
theater-coeff-0, no pin firewall, no zeroed indices — only descriptive
comments mention the mask); ordinary v2 update `num=2*err*fk+8*rise*fk`
on ALL indices (theater everywhere, w1/w4/w6 unfrozen); G-batch, clamp,
telemetry, DIV2=40000, tdiv unchanged v2; EXACTLY 2 epochs (Phase A
ep0+ep1 — the §5b reading pinned in MASK_INTEGERS.md); then FREEZE with
zero gradient steps after (only the params .zag + .txt and log writers
run). Log header: prereg SHA first, stage=2 mask=OFF, init weights
verbatim, B10b freeze note. Built from train_sr1.zag by copy + surgical
edits (signature/init/header/update-block/loop/main); verified by grep
audit 2026-09-24 ~17:28 PDT. NOT compiled, NOT run — held pending the
coordinator's gate ruling. B10b audit items (i)–(iii) and the crutch
diagnostic (|Δw1|, w7 drift) plus held-out calibration will be executed
if/when Stage 2 is green-lit.

## 2026-09-24 ~17:35 PDT: COORDINATOR SECOND GATE RULING on §5b w7<0 (recorded verbatim)

"Second gate ruling on §5b w7<0. FINDINGS: (1) The bar's premise is refuted by the frozen data itself — phase-local pin census (f7=1000, released, train): Phase A 1950 correct/0 wrong, Phase B 35/0, Phase C 0/5. grok's ~30-wrong-pin estimate was wrong; with 5 wrong pins confined to Phase C and ×10 boost on correct pins, w7's net drift is upward (+48/pass, crossing zero upward at pass 4). No Stage-1 continuation can clear w7<0 — this is structural to the data, not a transient. (2) The bar's intent, stated in §5b's own parenthetical '(separator moved)', IS satisfied: w7 is the most responsive channel (−830→+3083 range across passes), w5=+36811 theater-detached, w6≡0 all epochs, w3≡w4≡0, theater fired, mcC=0.884 non-degenerate. All mask behaviors verify. (3) The go/no-go exists to prevent burning 100× on a dead intervention; the intervention is demonstrably alive. (4) The arm's falsification clause applies to post-freeze eval, which has not been reached — no kill bar B1–B13 has been failed. RULING: the literal w7<0 gate is WAIVED via this recorded prereg note, premise-refutation documented above. The arm proceeds to 100× Stage 1 + Stage-2 disconnect + 37-leg eval. Kill bars B1–B13 and §11 adjudication are untouched and will kill the arm honestly if the mask design fails post-freeze. This ruling and its basis are presented to Micah at final adjudication for overrule."

Crew note: this note does not change any code, constants, or curriculum —
it adjudicates the gate criterion only. 100× Stage 1 (600 epochs) proceeds
from frozen init via the verified deterministic-forward method; epochs 0–65
must byte-match committed logs/log_11x_a.tsv.

## Resume integrity check (2026-09-24 ~17:35 PDT, before the 100× run)

- 7 committed blobs verified byte-identical against tnn-native-lab
  (logs/log_11x_a.tsv, params/params_11x_a.zag.txt, src/train_sr1.zag,
  src/train_sr2.zag, MASK_INTEGERS.md, work/KILLBAR_TABLE.txt,
  analysis/GO_NOGO_EXT.md) — fetched via raw.githubusercontent and
  sha256sum-compared.
- mask_code_sha (fixed) de0825ec71bcb9294e0df4631e80f0962beec0d5ec99409314f8013d882a8635
  — build/train_a/train_sr1.zag matches.
- A/B binaries cmp-identical: 480a96a04860d8aeb0c5a5e3350a71b59a02c5933058ef10064ac6f7e9cf0809
  (matches pinned value).
- 11× log opens with prereg SHA f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30.
- Resume = deterministic-forward: passes=100 from frozen init (600 epochs,
  incl. the extension epochs by byte-identical reproduction).

## 2026-09-24 ~17:38 PDT: 100× Stage 1 COMPLETE (passes=100, 600 epochs)

Run: train_sr1 A/B (committed binaries, no rebuild), passes=100 from frozen
init — deterministic-forward resume; rc=0 both (RC_A=0, RC_B=0).
- A/B byte-identical: logs, params .zag, params .txt (cmp, all three).
- Resume integrity: 100× log rows 0–65 byte-identical to committed
  logs/log_11x_a.tsv (diff-clean) — the extension epochs reproduced exactly;
  epoch-59 row = committed params_10x. Gate window epochs 60–64 unchanged
  (w7 = 1833,1833,1833,3083,1833).
- Logs open with prereg SHA f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30
  and the mask-integers line.
- Epoch-599 (Stage-1 end) weights: w1=416189, w2=−174847, w3=0, w4=0,
  w5=386783, w6=0, w7=−75612, w8=611, b=−333764; mcC=912, mcW=190, mcA=853.
  (Telemetry per B11 — not evidence. Note for the disconnect reading: w7
  went strongly negative in the late Stage-1 regime; the crutch diagnostic
  and the 37-leg eval adjudicate whether the mask was load-bearing.)

## 2026-09-24 ~17:38 PDT: Stage-2 driver BUILT (train_sr2.zag, A/B)

- Built in build/stage2_a, build/stage2_b from byte-identical src
  (sha256 ec279b02c37ef6854ec6e275dbe2abea75407f69ae9c72bf6106bea6d1142c41
  = committed blob). Pinned znc only; analyzer warnings (4, non-fatal —
  same class as the train_sr1 build); rc=0 both.
- A/B binaries cmp-identical: sha256
  90bd98a0871bb71d15d9fe48f1b24fd4d2351899ad6a2d9906cfa1b8bcada2ff (179334 bytes each).
- Re-audit vs §5b (this session, before build): mask code path ABSENT
  (only descriptive comments mention it; update block is
  num=2*err*fk+8*rise*fk on ALL k3 in 0..7); init from Stage-1 snapshot
  txt (9 lines w1..w8,b); EXACTLY 2 epochs `while(ep2<2)`, ph=0 (Phase A
  ep0+ep1), no pass loop, no phases B/C; G-batch v2 + clamp unchanged;
  FREEZE then only writers (params .zag + .txt, log .tsv) — zero gradient
  steps after. Log header carries prereg SHA, stage=2 mask=OFF, B10b note.

## 2026-09-24 ~17:40 PDT: Stage-2 SIGNAL_DISCONNECT COMPLETE — FREEZE

Run: train_sr2 A/B from the Stage-1 snapshot (params_100x_a.zag.txt);
rc=0 both. EXACTLY 2 ordinary v2 epochs (Phase A ep0+ep1), then FREEZE.
A/B byte-identical (logs, params .zag, params .txt).
- Log header: prereg SHA first, stage=2 mask=OFF, init weights verbatim =
  Stage-1 snapshot (416189,-174847,0,0,386783,0,-75612,611,-333764),
  B10b freeze note.
- Epoch 0: w1=422572 w2=-174831 w3=0 w4=32 w5=388463 w6=11757 w7=-75262
  w8=611 b=-323265; mcC=934; theater v2=0 (did NOT fire); gviol=18.
- Epoch 1 (FROZEN): w1=427072 w2=-174815 w3=0 w4=64 w5=389795 w6=20957
  w7=-75262 w8=611 b=-315596; mcC=939; v2=0; gviol=18; 0 clamp bindings.

### B10b audit (PASS)
(i) Mask code path absent: source audit (pre-build) — no 10*err boost, no
    theater-coeff-0, no pin firewall, no zeroed indices; update block is the
    byte-exact ordinary v2 rule on ALL indices. Stage-2 log header documents
    mask=OFF with the ordinary update rule; the logged init weights =
    snapshot, and w3/w4/w6 MOVED during Stage 2 (unfrozen — mask behavior
    absent). (ii) Frozen params = post-Stage-2 snapshot: params txt 9 lines
    == epoch-1 weight row, verified line-by-line. (iii) Zero gradient steps
    after freeze: exactly 2 data rows; the loop ends and only the snapshot
    writers run — structural, no flag needed.

### Crutch diagnostic (reported, not a kill bar)
Disconnect point → frozen: |Δw1| = |427072−416189| = 10883 (> 100 on the
literal reading — 2.6% of |w1|, movement concentrated in Stage-2 epoch 0).
w7: −75612 → −75262 → −75262: +350 toward 0 in epoch 0 (0.46% of |w7|),
then flat — NOT a crutch-collapse toward zero; the separator channel
survived disconnect essentially unchanged.
|Δw6| = +20957 (0 → 11757 → 20957): the crush coordinate, held at 0 all of
Stage 1, reattached the moment it was unfrozen — theater did NOT fire
(v2=0 both epochs), so this is the calibration term pulling w6 in. Flagged
telemetry for the eval reading (B2/B5/B13 adjudicate).
mcC: 912 → 934 → 939 across disconnect — no collapse on training telemetry
(B11: telemetry, not evidence).
