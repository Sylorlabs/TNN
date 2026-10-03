# H-CAUSAL2 re-run report (wave-20260929-1421pdt)

## What this is

S8 re-run of the 1121pdt H-CAUSAL2 experiment under the re-frozen prereg
(PREREG_CAUSAL2.md, committed alone at 55fece368 BEFORE any re-run output).
The 1121pdt evidence is worker-reported data only; the outputs in this
wave's evidence/ directory are the certified wave evidence.

## Build

- Compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1, sha256 498abcb5
  (pinned; verified before use).
- Sources (inherited, unmodified, byte-identical to 1121pdt):
  - world2.zag sha256 3132619e39d55e62096397de4719399e13a775295ffa1d0ed1c2f9f964000fb7
  - learn2.zag sha256 fbd9427daeeeaf840c549c2e921c6302734c55df29f16c6a77899858e2ce6c1d
    (byte-identical to the first arc's causal_learn.zag at
    docs/lab/research-lead/overnight-20260928/causal/causal_learn.zag)
  - baselines2.zag sha256 98372e7685d2d43a91269af00a7ef2e81a0a5d3ddba3ad9259880bb8688cb900
    (byte-identical to the first arc's baselines.zag)
- Build note: the first two znc invocations on learn2.zag exited nonzero
  when stdout was piped through head (SIGPIPE artifact); a direct
  invocation with output to a file exited 0 and wrote the binary. No
  source was modified; the analyzer's E0101/A0102 notes are warnings
  under default settings. Binaries built in ~/workspace/rerun1421
  (scratch, not committed).

## World regeneration

- `./world2 <phase> [broken]`: phases 1,2,3 unbroken; phases 4,5,6 broken=1.
- T-lines regenerated from the world byte-match the frozen observation
  sequences committed in 1121pdt for all six cumulative logs
  (cum_A/B/B2/C1w/C1/C2). The world implements the prereg's dynamics.

## Learner and baseline re-execution

- `./learn2 cum_X.txt probe_X.txt` run twice per phase X in {A,B,B2,C1w,C1,C2}.
- `./baselines2 cum_X.txt probe_X.txt` once per phase.
- All 6 run outputs, all 6 rerun outputs, and all 6 baseline outputs are
  byte-identical to the 1121pdt committed evidence (verified by cmp).
  The re-run is a true replication: zero bytes differ.

## Kill-bar recomputation (independent, from this wave's evidence)

- K2-1: P-B2a (2,1,0) correct, P-B2b (0,0,0) correct. PASS.
- K2-2: P-A2 (0,1,0) via invented rule; B-memorize WITHHOLDs (unseen).
  P-B2c (0,0,1) via rule on an unseen lamp value while Bmem WITHHOLDs.
  PASS.
- K2-3: P-C2a (1,1,0), P-C2b (1,1,1), P-C2c (0,0,0) correct. Provenance
  shows AMBIGUOUS {s1,s2} at seq11, REFUTE s2 at seq12, SPLIT on s1,
  CONTEST with WITHHOLD at C1w, RESOLVE at seq15 with loser SUPERSEDED
  "valid only before seq 12", SPLIT on s2, MERGE at seq17. PASS.
- K2-4: P-B1 WITHHOLD (ambiguous: s1 s2 disagree). PASS.
- K2-5: on P-B2a learner (2,1,0) correct while B-unconditional (1,1,0)
  wrong; on P-A2 learner (0,1,0) while B-memorize WITHHOLDs. Learner
  correct-or-honest on all 15 scored probes. PASS.
- K2-6: rerun outputs byte-identical to run outputs, 6/6 phases. PASS.
- K2-7: grep of the frozen task-word list on learn2.zag returns 0 hits;
  sha256(learn2.zag) equals the first arc's learner. PASS. (Hygiene note:
  baselines2.zag contains one hit, the word "causal" in its own header
  comment; not a frozen task word, not dynamics.)
- K2-8: "REFUTE action 1 candidate s2 at seq 12 (episode 12)" present in
  run_B2/C1w/C1/C2; the lamp hypothesis is retained as REFUTED, not
  deleted. PASS.

## Caveats carried

- The prereg re-freeze was done with full knowledge of the 1121pdt
  measurements (S8 design); the prereg text is unchanged.
- The headline K2-1 probe P-B2a is answered by exact-episode recall of
  seq12; the rule-invention evidence is the H4/H5 split structure plus
  rule-answered generalization probes P-A2 and P-B2c. The bar as frozen
  is satisfied; the skeptic may weight the invention claim accordingly.
- Scope stays bounded: 3 variables, hand-fed phases, single binary
  condition. Classification L2 structural learning, not L3 (the
  hypothesis vocabulary was authored; the specific pressure-blocks-cool
  rule was not). This arc does not claim L3.
- Contest resolution uses a fixed support threshold (2 vs 1); not
  validated on noisy data.

No em-dashes in wave documentation. No Python anywhere in loop work.
Pure Zag, pure shell, git, sha256sum only.
