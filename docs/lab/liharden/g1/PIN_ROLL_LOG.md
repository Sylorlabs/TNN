# PIN ROLL LOG — g1 archived rival-filler precedence

The pin is the trust relocation (BEYOND.md §7 caveat 1). Whoever rolls the pin
is now the integrity mechanism. This log is the governance record for rolls.

## Roll 1 — pinset v1 (2026-09-24)

- **Version:** 1. **Eras:** {1}.
- **Records:** `capital of australia|canberra|1|4`,
  `closest planet to sun|mercury|1|6`.
- **Basis:** pinned era-1 crawl (pre-2020). Dominant fillers taken from the
  frozen archive snapshot; domain counts are archive-domain counts, not live
  quorum votes.
- **Authorized by:** LI-HARDEN g1 build crew, per LI-HARDEN round-2 synthesis
  ("BUILD for pinned classes").
- **Digest:** ENDSET `11c75bf9…f7887d0` (full hex in `pins/pinset_v1.txt`).

## Roll 2 — pinset v2 (2026-09-24), SUPERSEDES v1

- **Version:** 2. **Eras:** {1, 2}.
- **Added record:** `capital of australia|sydney|2|3`.
- **Basis:** era-2 crawl generation shows the capital moved to Sydney; the
  era-2 archive's dominant filler for `capital of australia` is now Sydney
  (3 archive domains).
- **Era-split discipline:** era-1 records are RETAINED, not rewritten. The
  veto rule compares against the max era only; history stays auditable.
- **Authorized by:** LI-HARDEN g1 build crew (supersession test fixture).
  In production this roll requires the governed process: two independent
  crawl generations confirming the change + a named roll author. A roll on a
  single generation's say-so is how an attacker would try to move the pin —
  the two-generation rule is the defense.
- **Stale-pin behavior:** any client still on v1 WITHHOLDs `T4_supersede`
  with `ARCHVETO`. That freeze is the price of pin discipline; the remedy is
  rolling the pin, not weakening the rule.
- **Digest:** ENDSET `61ea36b7…afb41b633a03` (full hex in `pins/pinset_v2.txt`).

## Roll policy (standing)

1. Pins are content-addressed (per-record sha256) and versioned. Never edit a
   published version; roll a new one.
2. Era-split, never overwrite: new truth = new era, old era retained.
3. Two-generation confirmation before any era roll that moves a dominant filler.
4. A rejected pin set (digest mismatch) fails the mechanism closed
   (`WITHHOLD|PINFAIL`), never open.
