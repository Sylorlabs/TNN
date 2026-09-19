# N19 integration reconciliation — 2026-09-15

Current disposition: PASS_WITH_NARROW_SCOPE for the additive repaired candidate.
Historical BUILD_08 remains REQUEST_CHANGES: ordinary host-probe fsync/close
failure was misclassified as HOST_ABI. Historical files were not repaired or repinned.

Independent review is INDEPENDENT_REVIEW_V3.md (Lane C); this integration review
is a reconciliation, not a new independent scientific or terminal N17 review.
Fresh rebuild runtime SHA-256 c465815cba4abad84cc486a35693bf7aea225c7e1d5f58ae62e3e37c7b98b170,
qualifier be3b6b4ca27e3d7a9224179493f98360d0ae18f1450634c32a382a60d8b773ec,
and host tests c0885ffe5039c3a7edbfcde6373ce43ae5c2af1259dc26646054fa8e3570ec6f
exactly reproduce the independently reviewed repaired binaries.

Evidence: ../../Research/R33_CLOSEOUT_20260915T174458Z/final_closeout.json (repository-relative path: Research/R33_CLOSEOUT_20260915T174458Z).
Commands, exits and stdout/stderr hashes are in its command array. Fresh host
tests, five crash phases and separate recovery processes pass; all 11 supervised
children report second_wait=-10. RLIMIT_FSIZE=32 produces signal 25 and independently
observed file size 32, CPU 672 us, RSS 1490944 bytes. Closed-root host probe reports
IO -1905. Valid append/recovery, retained-root sequence and expected operational
refusals pass. Assertion refusal fixtures exit 0; rejected operational requests exit 1.

Only exercised owner-created local fixtures, direct-child successful reaping,
process-death recovery and mapping inputs are qualified. Exclusions: power-loss
durability, host-admin rollback protection, descendant groups, hostile concurrent
same-user races, exhaustive device/socket faults, CPU ceiling enforcement,
interrupted-wait fallback, and fresh-root identity authentication. No learner,
training, scientific exposure, successor promotion or full R33 closure is established.
