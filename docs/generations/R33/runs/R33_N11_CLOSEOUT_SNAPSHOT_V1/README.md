# Historical N11 closeout snapshot

This directory preserves the ten files bound by the original N11 closeout
before September 6 progress-report maintenance changed live state/navigation.
Every entry in `CLOSEOUT.sha256` verified from this directory before the live
changes. `CLOSEOUT.sha256` is byte-identical to
`../R33_N11_CLOSEOUT.sha256`; neither manifest was repinned.

Verify the historical snapshot from this directory with
`shasum -a 256 -c CLOSEOUT.sha256`.

The copied experiment manifests retain their original paths relative to the
main repository; their referenced experiment payloads have not been duplicated
here. Verify those manifests from the main repository root. The experimental
source, result and artifact files remain unchanged there.

The snapshot is historical evidence, not the active registry or a rollback of
the live journal. Current navigation is `../R33_PROGRESS_SUMMARY_20260906.md`.
