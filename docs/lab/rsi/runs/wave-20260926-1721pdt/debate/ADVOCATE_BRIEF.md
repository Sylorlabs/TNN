# Advocate brief: wave-20260926-1721pdt (four motions, argue FOR)

Role: advocate. Every verdict line below is labeled [RE-CERT] or [VACUOUS]
where it belongs. Nothing this wave is a new candidate.

## M1: Fork battery CONFIRM [RE-CERT]

The battery passes everything it tests, with uniform evidence and a
clean provenance chain.

1. 39 named entries, 37 PASS, 2 extraction FAIL. All 37 PASS entries
share byte-identical evidence: extracted znc sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(37/37), probe sha
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
(37/37), B2 bin sha
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
(37/37), E0002 on NEG1 (37/37), char-1 diff on NEG2 (37/37),
R32_ZNC_PROBE_OK (37/37). No toolchain divergence anywhere.

2. The 2 extraction FAILs (rh-pull-1-head at 5802fec8, rh-pull-2-head at
4b76bb59) fail for the identical cause recorded in every recent wave:
trees lack src/tools/toolchain/znc_linux_x86_64_abed8aa1, non-TNN
research-doc repos. This is a property of those forks' contents, not a
toolchain regression, and the scope stamp discloses it openly.

3. Spot re-run of three 1421pdt entries was run BEFORE any 1421pdt
verdict was cited: live tnn-native-lab at b6f96edaf PASS, fixture
wt-forktest-tnn-native-lab at bd3097874 PASS, pull/1 extraction FAIL on
identical cause. All three were parsed with the fixed sed parser
(never cut -d= -f2). The prior wave's cited verdicts are confirmed on
the corrected instrument.

4. Harness provenance is clean: pure-Zag fork_battery.zag extracted
read-only from the 2321pdt archive, sha
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
(matches expected); rebuilt binary sha
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
(byte-identical to prior waves; build is deterministic). Pure-Zag,
zero-Python attestation holds.

5. Live/fixture discipline: 4 live, 3 unique live commits
(45d449a56, a222f8f17, 39bf8d5d4), duplicates named per P8. Origin tip
re-check: 39bf8d5d490a04b22afecdee0d1fa139d4858949 at start and close,
no mid-wave move. Local HEAD unmoved at 45d449a56. Nothing arrived
after the testing window.

6. The coverage delta versus 1421pdt (39/4/3 versus 40/6/5) has a named
explanation, not a shrug: (a) the 1421pdt close's queued pickups
006dfe027944f395a47ae8fe6e3329a9d7634e and
7c19065e7b1ce13f6479ba50b4f35e110156c734 are now ancestors of the
merged run-start tip 45d449a56, so they no longer count as separate
named entries; (b) one entry is newly enumerated this wave
(arch-wave-0926-1421 at a222f8f178, the pre-merge 1421pdt archive
state); (c) the 1421pdt run-start tip entry is now a fixture ancestor
of the merged tip. 31 unique commits are tested; 8 are named
duplicates, all disclosed per P8.

Advocate position: CONFIRM [RE-CERT].

## M2: Interactive TNN CONFIRM [RE-CERT]

1. Zero new chat/REPL entry points in the 135-commit merge range
28ec31ab0..45d449a56. The grep over src/zag and units returned exactly
one file, the known false positive (substring "repl" inside "replay"
and "replication" in
units/teachers/learner/forcepin/PINS_RDTDT_BRIEF.md), disclosed openly.

2. Follow-up grep for entry-point signatures
(fn main, stdin, readline, interactive_loop, repl_loop) over src/zag
and units: zero files. Added-file scan over the full range filtered on
chat|repl|interactive: only pre-existing tnn_chat material, no
chat/repl-named file added to src/ or units/.

3. The wave delta added zero files under src/ or units/ at all. There
is no vector by which a new interactive surface could have entered the
source tree this wave.

4. Frozen instruments verified by sha256, all match: baseline probe
1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c,
decline-gate probe
20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7,
pinned znc 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
The git diff over docs/lab/rsi/fit_authority/ and src/tools/toolchain/
across the delta is empty: the wave merge altered no FIT chain input.

5. On the manifest gap: the worker disclosed explicitly that
docs/lab/rsi/fit_authority/SHA256SUMS does not exist and that the pins
live in fit_authority/README.md, stable across waves. Disclosure of the
gap is the honest move; the shas were independently recomputed and
match. Availability was verified read-only; no probe chat was run
because the standing rule schedules one only on change, and no change
was found.

Advocate position: CONFIRM [RE-CERT].

## M3: No-new-candidates stand-down CONFIRM [RE-CERT]

Five independent signals converge on zero:

1. Exactly one commit in docs/lab/rsi/ during the 14:21 to 17:21 PDT
window: e8b913584, the 1421pdt evidence batch (process evidence, not a
candidate).
2. Name-status grep over the window for prereg|design: zero hits.
3. Prereg inventory unchanged; newest remains PREREG_DP1_1721 from
wave-20260925-1721pdt (2026-09-25, before the window).
4. Every file newer than 14:21 PDT under docs/lab/rsi/ belongs to the
committed 1421pdt evidence batch; no new prereg drafts or design notes
on disk.
5. 27 untracked entries, zero matching prereg|design; all are older-wave
build artifacts and frame/binary residue by path.

Per-lane standing is unchanged: G1 STAND DOWN, D-VID-1 STAND DOWN,
CV-P barred pending his ruling 6, COMP-2 ruling 6 open with P11
unresolved, B1-class P9 reformulation not found, ST-1 DEAD. The only
loop-work mechanism material in the merge range is the known DP-1 pair
(18ad30fe3/02d1dcb31 from 2026-09-25), already queue-HELD, repaired
under P18 in 1421pdt, and not re-judged here. DP-1 stays HELD
[RE-CERT]; presenting the repaired sealed pair to his ears is a
future-wave queue decision, not this wave's. His six governance
rulings are untouched and not narrowed.

Advocate position: CONFIRM [RE-CERT].

## M4: Prereg commit-order self-check: VACUOUS

No loop candidates were proposed this wave, so no prereg/impl commits
exist to order. The self-check is labeled vacuous per P17: a recorded
null, not a pass.

Advocate position: record as VACUOUS [VACUOUS].
