# V1-NOVEL evidence — crew V1 (R1 novelty predicate), 2026-09-24

Two hypotheses implemented, attacked, ZD-checked, and long-horizon soaked.
NO WINNER DECLARED (per PREREG_H1EVO §4).

## Variants

- `v0/` — read-only copy of `~/workspace/ob2_repairatk/vb/` (control).
- `v0_run/` — writable build-scratch copy of v0 (sources byte-identical;
  only `lh_stream.zag` added). Used for LH control runs.
- `h_organ/` — H-organ: PAM owns the novelty judgment. `ob_pam.zag` gains a
  PAM-local contradiction register (`PAM_CONTRA`, policy+1 words, 0=empty)
  + `pam_note/has/clear_contradiction` + `pam_is_novel` (frozen predicate:
  no live/dead PAM row for the policy AND no unresolved contradiction
  record). Arbiter M_COMMIT queries `pam_is_novel` BEFORE appending the
  gated row (novelty judged on prior rows + records); mode = FRESH iff
  novel else REVISE; REVISE-admit clears the mark. M_REVOKE kill (rc==MA_OK)
  informs the organ via `pam_note_contradiction`.
- `h_arbiter/` — H-arbiter: arbiter owns the novelty judgment. New
  arbiter-side register arena (`arb_new_contra`, threaded through
  `arb_process`/`arb_handle_one`) + `arb_contra_note/has/clear` +
  `arb_is_novel` (PAM rows read as published trace + own register). Same
  trigger/clear points as H-organ. All `arb_process` callers updated
  (tests, r1/r2/r3 probes).

Design note (caught during build): the novelty query MUST precede
`arb_pam_claim`'s row append — the row being gated must not count as "a PAM
row for that policy", or nothing is ever novel. First H-organ build had it
after the append (r1b withheld); fixed, verified.

## R1a' / R1b' / R1c' (`r1p_atk.zag`, 3x byte-identical)

| cell | H-organ | H-arbiter |
|---|---|---|
| R1a' contradicted reinstall WITHHOLDs via REVISE (no install, no pin, reason UNCORROBORATED, mark retained) | HOLDS (killbar 0) | HOLDS (killbar 0) |
| R1b' novel claim ADMITs (FRESH) | HOLDS (killbar 0) | HOLDS (killbar 0) |
| R1c' paired 2nd verdict == lone verdict (both ADMIT; 2nd routes REVISE, corroborated by 1st) | HOLDS (killbar 0) | HOLDS (killbar 0) |
| r1d mechanism: REVISE-admitted commit clears the contradiction mark | HOLDS | HOLDS |

stdout SHA (both hypotheses, 3x each):
`72161c1f51d6bf7ce4c575f0d8c824f481edf45f2a31566784b053218e78fed1`
— the two hypotheses are byte-identical on all R1' cells.

## ZD — zero drift (unit suites + R2a-d)

| suite | V0 sha | H-organ | H-arbiter |
|---|---|---|---|
| ob_test_fl2 | f078ba64935d7b1e06f60dcc24daafc9ec8884f4248862666c7d98ccc54743ba | identical | identical |
| ob_test_pam | 7c0a819aa39ae13f4d55233867bb3f6de8eb3d75d813b55b64690b24eeb9a20f | identical | identical |
| ob_test_mem | 983eca4d60580139372899717de502ba9af81adebc0323352cc39ea22654d5ad | identical | identical |
| ob_test_arbiter | de350664875173d566fc2cbd02e923b2670bb7f01fc5b6866ad65b656664cef3 | identical | identical |
| r2_atk (R2a-d, all killbars 0) | 12d356dc4c423ff106429bcaf7cef421ef4349f4 | identical | identical |

V0 arbiter sha matches the frozen repair-attack baseline
(de350664875173d566fc2cbd02e923b2). All suites OB_FAILURES,0.
Note: `test_commit_pin`'s seeded priors (jf=1 x2) now route the commit
through REVISE; they corroborate (conf within tol) so the verdict and the
audit bytes are unchanged — comment updated in both variants.

## LH — long horizon (`lh_stream.zag`; 12-ep cycle: propose/revoke/drifted
## commit/novel commits/corroborated re-admit/propose/promote/commit/revoke/
## novel commits; 10x=300 eps, 100x=3000 eps)

| bar | V0 | H-organ | H-arbiter |
|---|---|---|---|
| 10x no panic | pass (sha 59cdc894fdda08a2, 3x) | pass (sha 71f11ed68be524ae, 3x) | pass (sha 71f11ed68be524ae, 3x) |
| 100x no panic | pass (sha b2d5441fe5fd337d, 3x) | pass (sha 43eca53e96330c6c, 3x) | pass* (sha 43eca53e96330c6c, 5/6) |
| cross-horizon prefix (100x first 300 eps == 10x) | identical | identical | identical |
| new failure mode at 100x | none | none | none |

10x summaries — V0: `LH_SUMMARY,64,50,64,0,214,-1`;
H-organ/H-arbiter: `LH_SUMMARY,64,43,57,7,221,8` (identical to each other).
Decision-field diff V0 vs H-*: divergences ONLY at eps 2,14,26,38,50,62,74
(the pre-saturation k==2 drifted contradicted recommits: V0 admits,
H-* withhold+drop). Post PAM-row saturation (64 rows) all variants drop
identically. The repair's behavioral delta is exactly 7 withheld installs;
7 fewer live slots (43 vs 50) is the cumulative consequence.
100x summaries — V0: `LH_SUMMARY,64,50,64,0,820,-1`;
H-organ/H-arbiter: `LH_SUMMARY,64,43,57,7,827,8` — same 7-withhold delta,
no widening at scale. H-organ vs H-arbiter 100x outputs byte-identical.

*H-arbiter 100x: 6 runs, 5 byte-identical; run 3 had torn stdout framing
(`LH,2514,64,LH,2899,…` — ~384 steady-state lines dropped/spliced mid-line)
with decisions and the summary line intact and matching. Classified as a
transient I/O artifact, not a decision nondeterminism: single occurrence,
framing-only, 5/6 identical including the 3-run bar.

## What separates the hypotheses

On all measured behavior (R1a'/b'/c', r1d, ZD suites, R2a-d, LH 10x/100x
per-episode decisions, contradiction occupancy = 8 in both at 10x and
100x) H-organ and H-arbiter are BYTE-IDENTICAL. They compute the same
frozen predicate over the same information; they differ only in
OWNERSHIP/placement: contradiction records + novelty judgment live in the
PAM organ (H-organ) vs in a dedicated arbiter-side register with PAM rows
read as published trace (H-arbiter). No horizon data separates them
verdict-wise — the choice is architectural (organ autonomy vs router-held
state), for Micah/the integrator, not empirical. If a future path ever
writes organ rows without the arbiter seeing them (or vice versa), the two
placements could diverge; no such path exists in this tree.

## Out of scope / not touched

N-AUTH not implemented. M_COMMIT-never-sets-ast seam untouched (H-OB-79…
backlog numbering: no new backlog entries raised; none needed). R3 probes
left at V0-broken behavior (r3a killbars fire, r3b panics — reproduced
identically in h_arbiter; V2's scope). Static grep rng/rand/seed clean on
all new/changed sources. znc pitfalls honored ([]u8 arenas + LE accessors,
.* only on pointers, no nio_free of _zag_arg, no slice >2^25, no `};`).
Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.
Binaries in /tmp (lh10_*, lh100_*, horg_*, harb_*, v0_*); sources above.
