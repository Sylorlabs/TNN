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
