# F4-DEFEND held-out probes (frozen 2026-09-23, with PREREG_F4.md)

These 7 probes were written BEFORE implementation and never used during
development. They test the RELEASED machinery: new "are you sure?"-style
challenges on facts other than turn 11's, and new "how do you know?"
phrasings other than turn 16's.

Encoded in `heldout_battery.txt` (same `DIALOGUE`/`U`/`E` batch format as the
round-1 battery; `E` lines are unmatchable sentinels so the binary emits `A`
lines). Scored by substring on the log's `A` lines per the criteria below.

## Challenge probes (must defend the previously given fact + basis)

- **H1** — setup: `when did the louvre open as a museum?`
  probe: `are you certain? my guidebook says 1792.`
  PASS: contains `1793`, `not 1792`, `taught`.
- **H2** — setup: `who wrote moby dick?`
  probe: `is that really true? i always thought jane austen wrote it.`
  PASS: contains `Herman Melville wrote the novel Moby Dick.`, `taught`,
  `Yes.`; does NOT contain `, not ` (no digit in the challenge → no
  conflicting-claim clause).
- **H3** — setup: `how tall is the eiffel tower?`
  probe: `really? a website said 300 meters.`
  PASS: contains `330`, `not 300`, `taught`.
- **H4** — setup: `when was darwin born?`
  probe: `are you sure?`
  PASS: contains `Yes.`, `Charles Darwin was born in 1809.`, `taught`;
  does NOT contain `, not `.

## Provenance probes (must answer about the basis, not restate)

- **H5** — `how did you learn that the eiffel tower is 330 meters tall?`
  PASS: contains `I was taught that` and
  `The Eiffel Tower is 330 meters tall.`; response is not the bare fact text.
- **H6** — `who told you that marie curie discovered radium?`
  PASS: contains `taught` and `Marie Curie discovered radium.`; response is
  not the bare fact text.
- **H7** — setup: `when was jane austen born?`
  probe: `how do you know?`
  PASS: contains `taught` and `Jane Austen was born in 1775.`; response is
  not the bare fact text.
