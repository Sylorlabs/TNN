# ENUMERATION_MANIFEST_2321.md

Wave: wave-20260929-2321pdt. Driver: batch_2321.sh, derived from the
frozen batch_1721.sh by mechanical edit only (wave name, scratch path
~/workspace/fb2321pdt, run-start pin, live/fixture rotation); the 75
run-line bodies are otherwise byte-identical in form. run_one.sh is
byte-identical to the frozen instrument (sha256
4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978).
Pinned-commit discipline: every extraction is by pinned SHA, never by
live ref.

Run-start pin: fed72668cb37cf6b75e82f0acae537e2529855b8 (tip at battery
start; mid-battery lane commits inert).

Rotation from 1721pdt (73 entries) to 2321pdt (75 entries):

- NEW LIVE: arch-wave-20260929-1721pdt at
  7c11ac5af742085f3d81355fab3863b204d32d6a (newly enumerated archive;
  local pin branch tnn-native-lab-wave-archive-2321pdt-pin1721 created
  this wave at that SHA; the pre-existing branch
  tnn-native-lab-wave-archive-20260929-1721pdt points at dff8c200, the
  1721pdt wave's own end-of-wave tag, and was left untouched).
- NEW LIVE: local-tnn-native-lab at fed72668 (run-start pin).
- Was LIVE at 1721pdt, now FIXTURE: arch-wave-20260929-1421pdt at
  347260cee1; local-1721pdt-tip at 7c11ac5af (was LIVE local pin;
  duplicate-SHA group {arch-wave-20260929-1721pdt, local-1721pdt-tip}).
- All other 1721pdt entries carried forward unchanged.

Duplicate-SHA groups (carried forward from 1721pdt, plus the new one):
{arch-wave-20260929-1721pdt, local-1721pdt-tip} at 7c11ac5af (new);
{arch-wave-20260929-1121pdt, local-1421pdt-tip} at d18f7f68d;
{arch-wave-20260929-0821pdt, local-1121pdt-tip} at 5f86e6cb2;
{arch-wave-20260929-0221pdt, local-0521pdt-tip} at d2fdf122; plus the
older groups recorded in the 1721pdt manifest (unchanged).

Scratch-dir note: ~/workspace/fb2321pdt was previously used by
yesterday's wave-20260928-2321pdt (same wave-id clock time, different
day). Two stale RESULT.txt files from that wave were found in E/
(arch-20260924-0521pdt, arch-20260927-0521pdt, both PASS, dated Sep 29
06:24 UTC). They are NOT part of this wave's 75-entry enumeration, were
not re-run, and are excluded from the tally. Future waves should use a
day-qualified scratch name to avoid the collision.

Remote: read-only ls-remote at battery start showed zero new refs since
1721pdt (origin/tnn-native-lab bedf8b4a, HEAD 27a4271f, all pins
unchanged). The rh-fs-gr1 entry (remote fs-gr1 at 23f6c0f9) was already
enumerated at 1721pdt and re-ran here (slow remote extraction, PASS).
