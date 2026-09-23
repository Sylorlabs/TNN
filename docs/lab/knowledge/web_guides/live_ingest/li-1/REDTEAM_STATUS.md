# LI-1 red-team status accounting (authoritative, 2026-09-23)

Frozen manifest: `li-1/redteam_urls.txt` (12 URLs: rt01–rt05 injection,
rt06–rt08 confident-falsehood, rt09–rt12 single-source).

Authoritative first-attempt accounting (per Micah's checkpoint, supersedes
the stale `REDTEAM_REPORT.md`, which says only rt01/rt02/rt06 were fetched):

| id   | class            | original first attempt | snapshot file (this run) | fidelity            | test input? |
|------|------------------|------------------------|--------------------------|---------------------|-------------|
| rt01 | injection        | SUCCESS                | redteam/rt01.txt         | VERIFIED (byte-identical to preserved original `diag/redteam_real/snap/rt01.txt`) | YES |
| rt02 | injection        | SUCCESS                | redteam/rt02.txt         | VERIFIED (byte-identical to preserved original `diag/redteam_real/snap/rt02.txt`) | YES |
| rt03 | injection        | FAIL                   | — (retry content excluded) | n/a | NO |
| rt04 | injection        | FAIL                   | — (retry content excluded) | n/a | NO |
| rt05 | injection        | FAIL                   | — (no snapshot; retry also failed) | n/a | NO |
| rt06 | confident-falsehood | FAIL                | — (later content excluded; original FAIL stands) | n/a | NO |
| rt07 | confident-falsehood | SUCCESS             | — (original not preserved; retry-derived snapshot excluded) | n/a | NO |
| rt08 | confident-falsehood | SUCCESS             | — (original not preserved; retry-derived snapshot excluded) | n/a | NO |
| rt09 | single-source    | SUCCESS                | — (original not preserved; retry-derived snapshot excluded) | n/a | NO |
| rt10 | single-source    | SUCCESS (result `2340581592313211114`, lines 0–2299) | redteam/rt10.txt | RECONSTRUCTED-ORIGINAL: transcribed from preserved output of the original result ID; audit 2026-09-23 — 42/42 page footers present exactly once, 13/13 verbatim probes incl. trailing whitespace, clean chunk junctions, TITLE+transform byte-identity; not byte-provable vs an independent copy | YES (with caveat) |
| rt11 | single-source    | SUCCESS (result `5757845057035512191`, lines 0–238) | redteam/rt11.txt | RECONSTRUCTED-ORIGINAL: from captured original output, frozen `strip_markers.py`; re-transform byte-identical (5441 bytes); not byte-provable vs an independent copy | YES (with caveat) |
| rt12 | single-source    | SUCCESS (result `3560362855816963204`, lines 0–506) | redteam/rt12.txt | RECONSTRUCTED-ORIGINAL: from captured original output, frozen `strip_markers.py`; re-transform byte-identical (19417 bytes); not byte-provable vs an independent copy | YES (with caveat) |

Excluded snapshots live in `li-1/corpus_snap_full/redteam_excluded/` with
their retry-derived raw files, retained only as disclosure evidence. They
must NOT be used as red-team test input.

## Invalid later attempts (all excluded, all disclosed)

- rt03 retry → browser result `69557981142849860` (invalid; page also tripped
  the runtime prompt-injection notice — page data only, not instructions).
- rt04 retry → browser result `7627594516466729635` (invalid).
- rt05 retry → failed again (invalid; original status remains FAIL).
- rt06 later content (preserved in `diag/redteam_real/snap/rt06.txt`) —
  original attempt FAILED, later content excluded.
- rt07 refetch → browser result `6007855530313988274` (invalid; original
  succeeded but no preserved original capture exists).
- rt08 refetch → browser result `5896485642089691237` (invalid; same).
- rt09 refetch → browser result `5448457127052353481` (invalid; same).
- rt10: the manifest URL was opened once more in this continuation but the
  runtime returned the SAME original result ID `2340581592313211114`; no new
  fetch occurred. Reconstruction uses only that original result's output.

## Coverage consequence

The confident-falsehood class (rt06–rt08) has ZERO usable test pages
(rt06 original FAIL; rt07/rt08 originals not preserved). The red-team test
can therefore exercise injection (rt01, rt02) and single-source (rt10, rt11,
rt12) only. This gap is disclosed, not papered over.

## Reconciliation with stale REDTEAM_REPORT.md

`REDTEAM_REPORT.md` states only rt01/rt02/rt06 were fetched. That report is
stale and conflicts with the authoritative checkpoint above; it is retained
as a historical artifact and explicitly superseded by this file.
