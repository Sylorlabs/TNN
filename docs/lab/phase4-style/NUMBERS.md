# NUMBERS.md — phase 4 style attribution: every measured number

Pullable summary of all quantitative results. Corpus: 48 training utterances
(12/person), 12 asked probes, 18 stream lines, 6 red-team probes.
Determinism: 12/12 scripts byte-identical across 3 runs (2 plain + 1
MALLOC_PERTURB_=165).

## Claim A — asked attribution

| Metric | Value |
|---|---|
| Correct | 12/12 |
| Wrong-person attributions | 0 |
| Withholds | 0 |
| Kill bar (≥10/12, 0 wrong) | HOLD |

## Claim B — spontaneous attribution

| Metric | Value |
|---|---|
| Clean lines volunteered correctly | 8/12 |
| Clean lines silent (threshold conservatism) | 4/12 |
| Wrong-person volunteers on clean/drift | 0 |
| Drift lines correct-or-silent | 2/2 |
| Unknown lines silent | 0/2 (both volunteered as p4) |
| False volunteers total | 2 |
| Mimicry envelope | 1 silent, 1 volunteered true style (p1) |
| Kill bar (≥10/12, no false volunteers) | FAIL |

## Claim C — mechanism

| Metric | Value |
|---|---|
| All-lesioned attributions | 0/12 (all WITHHOLD) |
| K-C1 bar | HOLD |
| LEX margin shrink, decisive probes | 26.0 pts (38→15, 48→21, 51→23) |
| LEX margin shrink, control probes | 3.5 pts |
| CASE margin shrink, decisive probes | 11.0 pts |
| CASE margin shrink, control probes | 0.7 pts |
| LEN margin shrink, decisive probes | 5.5 pts (not validated) |
| LEN margin shrink, control probes | −7.0 pts |
| PUNCT decisive probes | 0 (removal ≈ no-op) |
| STRUCT decisive probes | 0 (removal ≈ no-op) |
| K-C2' bar (≥1 family validated) | HOLD (LEX, CASE) |
| K-D determinism | 12/12 scripts × 3 runs byte-identical |

## Accuracy under lesion (asked probes)

| Run | Accuracy |
|---|---|
| lesion_none | 12/12 (100.0%) |
| lesion_LEN | 12/12 (100.0%) |
| lesion_CASE | 11/12 (91.7%) |
| lesion_PUNCT | 11/12 (91.7%) |
| lesion_LEX | 11/12 (91.7%) |
| lesion_STRUCT | 12/12 (100.0%) |
| lesion_all | 0/12 (0.0%, all WITHHOLD) |

## Red team

| Probe | Expected | Got | rel | Verdict |
|---|---|---|---|---|
| RT1 mimic (p1→p4, leaky) | envelope | p1 | 29 | envelope |
| RT2 mimic (p4→p1, leaky) | envelope | p4 | 50 | envelope |
| RT3 drift (p2 casual) | p2 or silent | p2 | 16 | PASS |
| RT4 drift (p3 blunt) | p3 or silent | p3 | 39 | PASS |
| RT5 content trap | p3 (not p1) | p3 | 74 | PASS |
| RT6 unknown (asked) | WITHHOLD | WITHHOLD | 2 | PASS |

## Learned style ledgers (n=12 each)

Feature order: words, wlen×100, up%, lo%, bang%, ques%, stop%, comma%,
hedge%, caps3%, frag%, digit%.

| Person | Vector |
|---|---|
| p1 terse | 4,462,0,1,0,0,0,0,0,0,1,0 |
| p2 formal | 13,566,1,0,0,0,0,0,0,0,0,0 |
| p3 hedged | 12,431,0,1,0,0,0,0,11,0,0,0 |
| p4 excited | 8,456,17,0,7,0,0,0,0,14,0,0 |

## Corpus hashes (sha256, sealed before the run)

```
1a430811a80cf46337c98afdbd24dbed0cba1e75cf11c67d9783bf834a5893a2  train.txt
f221e84161077bab32f5737273171a8c0daf52c4c4c444a0d2ea276411d30883  asked.txt
57ecdec81fabffdc8d7b08809a73147e90264ad3e07d04a0a0ca941adddba12c  watch.txt
61b22da04277b79f5a0f5230b339747a17beffb3c76518c35c750d631889d64b  redteam.txt
6eeb096a947ef15147408f24418cac6ae593d329fa141a60117ec38f71c19444  lesion_all.txt
```

## Result hashes (sha256 of run-1 stdout, byte-identical across 3 runs)

```
f2e3776b0f3c97c1e050209fafafa846bf0d640f1234822f90b9e20867eff412  train.r1
a021096271bcb126cf8f676461d459d614c748d3ad9d925c493b8f2e53eb912f  asked.r1
69cb49526d766af1cacdc7bc9bf77e6b0bd93e55a9b701446eddbbc64e0dbf7f  watch.r1
2822dac8fa95ebb424750ab41c9edfae36ad75050832a81540b8253566833f4d  profiles.r1
0a362a313a5b7291857d9a3fd228462d0e20fefdacfb2d09b49834fb1b613f70  lesion_none.r1
b77c5fca04d0539ff46824fb6c03bd0e92c1daa80ea520de9ef8a0d35a2c39df  lesion_LEN.r1
6aadad5501bd31fa14cf093a54d2f1c3b31e90233b27fe83bcb03827616a581e  lesion_CASE.r1
f55a6879d6f7c8067979255debdc7f8e28b4926a9b17dcff37d2ceb8405bb914  lesion_PUNCT.r1
36efbba3eacc7b761791d823f2876e9c74e3602b0d7e335c8f2dbd5f730ec836  lesion_LEX.r1
692e0498e055768be47a77f4f93ad856736c18293539a87a0c09c262d6200dab  lesion_STRUCT.r1
f267e3f86941b7112661c7554ba4879a6fd1f8e62949ea21d42f3b741e889925  lesion_all.r1
c0ad8889b6b7d9d08df3926e1802864f18d6d429ae05c1847dd7ccc8069f79d4  redteam.r1
```

(Full per-probe traces: `results/*.r1`, machine-readable verdict:
`results/score_report.json`.)
