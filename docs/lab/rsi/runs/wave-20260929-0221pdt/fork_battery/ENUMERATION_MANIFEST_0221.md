# ENUMERATION_MANIFEST_0221.md

Wave: wave-20260929-0221pdt. Run-start pin: a014dc1d96d0935f4e4d53888b3e488e3ce1f459.
Origin tip at run start: bedf8b4aab0110e3c115fb1bca3903551a32577e (unchanged; HEAD ref -> 27a4271f unchanged).
Enumeration method: the 2321pdt 61-entry table carried forward verbatim, with two changes: (a) new local archive
tnn-native-lab-wave-archive-wave-20260928-2321pdt at a014dc1d9 (newly enumerated archive, LIVE entry); (b) local-tnn-native-lab
now tested at the new run-start tip a014dc1d9 (LIVE), and its prior-wave pin fab33cb4c (already tested LIVE at 2321pdt)
moves to the fixture set under the explicit renamed entry local-2321pdt-tip (this replaces the 2321pdt convention of
folding the prior live pin under an archive wave name, which was confusing; the rename is declared here). Total: 63 named entries.
Live entries (2): arch-wave-20260928-2321pdt (a014dc1d9), local-tnn-native-lab (a014dc1d9).
Fixture entries (61): all other named entries, pinned to their prior-tested SHAs; the 59 carried fixture SHAs are
byte-identical to the 2321pdt table (verified by comm against batch_2321.sh); duplicate SHA groups named in
FORK_BATTERY_0221.md.
Zero new remote refs since 2321pdt (read-only git ls-remote at run start: origin/tnn-native-lab bedf8b4a, HEAD 27a4271f,
fs-gr1, r2-7, reorg/phase-0-1, wg-freeze, pull/1, pull/2, pull/3 heads all at their 2321pdt pins).
Zero Python; pure shell, git, sha256sum, pinned znc, frozen pure-Zag harness.

Anomaly recorded: at run start a ref named tnn-native-lab-wave-archive-20260928-2321pdt (short name, no "wave-" infix)
appeared in ref listings (git branch -a and git for-each-ref) but never resolved (rev-parse and show-ref failed; no
file on disk; no packed-refs entry), then vanished from listings minutes later. The resolving archive ref is
tnn-native-lab-wave-archive-wave-20260928-2321pdt at a014dc1d9. The phantom was transient, is recorded here as a
listing anomaly, and is not evidence; the battery pins SHAs, so no entry depended on the phantom name.
