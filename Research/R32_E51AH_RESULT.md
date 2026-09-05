# R32 E51AH — Grounded Preservation Replay Result

Executed and verified: 2026-09-04 Pacific (2026-09-05 UTC).

Status: authoritative, integrity-valid native development negative.

Frozen outcome: `PRESERVATION_REPLAY_DEVELOPMENT_FAILURE`.

R27 remains canonical; R32/E51 remains experimental. No promotion is authorized.

## Result

Neither grounded replay arm preserved all 12,622 frozen-union development
successes. The global replay arm preserved 12,386 and rescued six previously
unreachable trajectories. The local-384 replay arm preserved 12,501 and rescued
159, losing 121 prior successes. Its net increase of 38 development successes
does not satisfy the preregistered zero-preservation-loss gate.

All required integrity gates passed, the native process exited successfully,
and the independently rerun evidence verifier agreed with the native outcome.
Stage-109 validation and stage-110 confirmation each executed zero episodes.
This is a valid negative for the specified treatment, not an infrastructure
failure and not a held-out generalization result.

## Execution and evidence identity

| Item | Verified value |
| --- | --- |
| Repository / branch | `Sylorlabs/TNN` / `r32-agent-sequential-frontier` |
| Frozen parent | `80069f979084f0dcc6341fffe59b8e1a7ad2e7f1` |
| Authority commit | `09c5fcf63f295b52b6c82299d01ac340d554dd4e` |
| Scientific source commit | `c8f62bac285e72653bd6e9412498575ea8036b77` |
| Scientific source tree | `bef9b1172617efb2e77e6772eb18069a5c9fa8a8` |
| Actions run / attempt | `33944536498` / `1` |
| Workflow / job | `350693574` / `101248131899` |
| Run created | `2026-09-05T04:26:00Z` |
| Job started / completed | `2026-09-05T04:26:03Z` / `2026-09-05T04:44:32Z` |
| Native execution step | `2026-09-05T04:27:36Z` to `2026-09-05T04:44:29Z` |
| Native runtime | 1,013 seconds (16 minutes 53 seconds) |
| Native process exit code | `0` |
| Workflow conclusion | `success` |
| Artifact | `9963143498` |
| Artifact name | `r32-e51ah-native-c8f62bac285e72653bd6e9412498575ea8036b77` |
| Downloaded ZIP size | 3,582,842 bytes |

The exact ZIP, terminal run/job/artifact metadata, extracted evidence, and local
identity audit are preserved under:

`.scratch/e51ah/actions-33944536498-yhVo1A/`

The scientific evidence root within that directory is
`extracted/.scratch/e51ah/`. The committed machine-readable record is
`Research/R32_E51AH_EVIDENCE.json`; live execution state is in
`Research/R32_E51AH_EXECUTION_STATUS.json`.

## Fingerprints

| Evidence object | SHA-256 |
| --- | --- |
| Artifact ZIP; also matches GitHub digest | `00f98e3077fdd2f48d593303405e2da1b721c90caffef405742ce4307381990e` |
| Assembled E51AH source | `8ee32cdb8b51b4e996c8a42968227eae8c29879c62d5df3f4bd749263658cc23` |
| Linux native build 1 and build 2 | `7bbce4de66275e3178b762ff7801bcc65e4188f46fd08ed9ef3dc684128a4c5f` |
| Raw native ledger | `6db9df138b9c22f8a23dbba86a5925aa21fbadb778016ddff2e52394b08272fa` |
| Summary ledger | `fa0770803bb0499c5575706d3d7cb73a7c021496fcc5762bdfb3cd5d30f52c00` |
| Preregistration | `61f16da6cd428ddfb001c1fa784b35bc7e61f5f6669ff1c2158163d00c084477` |
| Implementation contract | `186799241b9ecfdb977489c77869ed579e7cc93915f00bccaf59f6167265d77d` |
| Hardcoding ledger | `5e2e2f9c4ed2d9690f01a935570c82b6b068f6eae3e82fcdb7da1fc6dac2fef5` |
| Official Linux compiler | `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` |
| Frozen assembled E51AD parent | `67ac4a8412e4098a9572a248bee2be1c9b6ea9699fd52cc568e5e25e1c132314` |
| Imported E45 core | `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0` |

The preregistration Git blob is `bd6f34e689b73004b7d3605fb37e63bba7a532c9`.
The persisted official compiler is
`Research/toolchain/znc_linux_x86_64_abed8aa1`, Git blob
`611b7f0c215385b7d3073bbebbf6078224c70b4c`, from compiler source commit
`abed8aa170ef1bc33e5aca68b99fcdd905a4545f`. The run used native Linux X64.
Earlier macOS-hosted compilation outputs are not these authoritative binaries;
no cross-platform binary-equality claim is made.

## Verification performed

The downloaded ZIP matched GitHub's reported digest and size. All 95 extracted
files matched the archive, and all 25 archived root-level tracked files matched
the frozen scientific commit. The source, authority, compiler, and binary
manifests contained 22, 8, 1, and 2 verified entries respectively. All 39
transitive source inputs matched both their recorded SHA/Git-blob identities
and the frozen parent revision. Baseline V1 remained identical to its authority
commit in both the artifact and local repository.

Some inherited source inputs are archived beneath `transitive_source`, not at
the artifact root. The compiler binary is not uploaded; its recorded identity
was checked against the persisted local compiler and frozen Git bytes. Neither
layout detail was treated as a scientific failure.

The committed `.github/scripts/e51ah_verify.py` was run independently against
the downloaded evidence and returned `verified=true`, no errors, and the same
outcome as the run. A subsequent identity audit confirmed the regenerated
evidence-check report still matched the archived bytes. No experimental binary
was rerun locally. The separate archive auditor passed six synthetic rejection
tests; those fixtures are infrastructure tests, not experimental evidence.

## Stage-108 development

The development population contains 12,960 episodes and 220,320 states:
12,336 slot-covered trajectories, 286 direct-required trajectories, and 338
union-neither trajectories with positive candidate utility. There are zero
union-neither/no-warrant trajectories in this development partition; that is
not a claim that the entire population contains no no-unique cases.

The frozen union covers 12,622 episodes and misses 338. Counts below come from
`e51ah_development_arm`; lost successes, total reachability, and net change are
derived by subtraction/addition against that same development control.

| Arm | Treatment | Preserved / 12,622 | Lost | Rescued / 338 | Total / 12,960 | Net vs union | Gate |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | Parent critical-only global | 11,823 | 799 | 246 | 12,069 | -553 | 0 |
| 2 | Count-matched critical-only global | 11,828 | 794 | 249 | 12,077 | -545 | 0 |
| 3 | Grounded replay global | 12,386 | 236 | 6 | 12,392 | -230 | 0 |
| 4 | Grounded replay local-384 | 12,501 | 121 | 159 | 12,660 | +38 | 0 |

Recorded margin losses for arms 1/2/3/4 are 6,757,704; 6,575,981; 91,387,599;
and 31,729,273. These are the frozen development diagnostics, not replacement
criteria for the preservation gate.

Replay therefore changed fitted behavior and reduced preservation losses
relative to the critical-only controls, but did not eliminate them. In
particular, the local replay arm's positive development total cannot be used
to relax the zero-loss rule or open validation retrospectively.

### Training support and model identity

The parent critical set has 624 records. Replay has exactly one isolated record
for each of the 12,960 development trajectories. Candidate-0 replay targets have
6,277 positive, 6,677 negative, and six neutral values; candidate-1 targets have
6,512 positive, 6,429 negative, and 19 neutral values. Record isolation, target
support, and replay-kind coverage passed.

The count-matched arm repeats 624 critical records for 20 complete cycles plus
a 480-record prefix. Thus 480 records receive 21 copies and 144 receive 20.
This is a record-count control, not an exactly uniform weighting control.

Global residual parameter counts are 66; the local conditional residual adds
2,112 parameters on the fixed 32-cell substrate. Forward/reverse identity and
local strict-loss gates passed. Residual hashes were:

| Model | Hash |
| --- | ---: |
| Parent residual | 1188771988 |
| Count-matched residual | 859476167 |
| Replay global | 345099260 |
| Replay local | 1440881524 |

The terminal controller remained at hash `238967492`, and the direct controller
at `1790306570`. Final frozen-controller and all-four-residual immutability
gates passed. UNKNOWN stayed exactly zero with no learned head; the native
ledger reports no evaluator truth, ambiguity labels, or mode/resource identity
exposed to the learner, and no topology/graph change.

## Opening gates, completion, and sealed exposure

Required parent, reconstruction, source, partition/domain, support, fit-identity,
model-freeze, and final integrity gates all passed. World assignment failures
were zero. Native terminal reproduction was 4,200/4,200 known and
1,200/1,200 no-unique full-tape reachability.

Neither replay arm passed development eligibility, so the selected replay arm
is `-1` and `e51ah_development_open_gate=0`. Validation executed `0/5400`,
confirmation executed `0/10800`, and both winner IDs are `-1`. Stages 109/110
remain sealed, not merely unreported. Their integrity flags do not mean those
populations were evaluated. No E51AH held-out oracle/expressivity result exists.

`TNN_R32_E51AH_EXECUTION_COMPLETE=1` is present exactly once, with process exit
code zero. The separately named `e51ah_completion_gate=0` is the return value
reserved by the frozen source for exact confirmed rescue, not an execution
failure. Likewise, the standalone-exit text marker is not the process exit code.

## Causal closure and limitations

This closes the hypothesis that the specified one-record-per-trajectory
grounded replay treatment, with these fixed features, targets, sampler,
optimization doses, and global/local residual geometry, is sufficient to
preserve every frozen-union success while rescuing a miss on stage 108.

It does not reject preservation learning generally, prove current-state feature
aliasing, establish memory necessity, or show that all other objectives and
optimization schemes fail. The empty union-neither/no-warrant stratum limits
coverage; cyclic count matching is imperfect; and only one development
population was evaluated for E51AH. Existence of a successful resource-feasible
state does not establish safe online stopping, continual learning, transfer,
composition, or general autonomous cognition.

Historical E51AE/E51AG oracle counters were assigned success by construction.
Their measured learned/control comparisons remain evidence, but the counters
do not independently establish candidate expressivity. E51AH corrected its own
oracle before execution, but the sealed branch did not execute and supplies
no new expressivity evidence.

The next justified work is a separately preregistered, bounded diagnostic
distinguishing current-state discrimination and short-context information from
remaining sampling, objective, optimization, and routing-geometry explanations.
The E51AC–E51AH arc synthesis records that next-step rationale. No new scientific
experiment is frozen or dispatched by this result report, and E51AH must not be
retuned or rerun to search for a more favorable outcome.
