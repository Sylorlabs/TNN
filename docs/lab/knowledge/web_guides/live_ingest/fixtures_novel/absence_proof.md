# Absence proof — novel facts provably absent from the LI-1 corpus

Method (2026-09-23, after fixture generation, before measurement runs):
1. `knowledge_ledger_full.txt` (LI-1 scale-up knowledge ledger): downloaded
   from the branch; SHA-256
   `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
   (empty file). All 60 fixture facts are trivially absent.
2. `corpus_snap/` (pilot, 19 snapshot files) and `corpus_snap_full/`
   (scale-up, 194 snapshot files): downloaded byte-identical from the branch.
   24 distinctive probes grepped case-insensitively (`grep -ril -f
   absence_probes.txt`) across all 213 files. Probes: the beacon mint-token
   stem `NF20260923`, `fixture beacon`, `beacon ledger`, `PREREG_LI_NF`,
   `8640`, `Guaylupo`, `Contender Series`, `Bayern Munich Women`,
   `Vanuatu Women`, `HB Koege`, `Starlink V3`, `hummingbirds live 40 years`,
   `Eiffel Tower is 500`, `Sound travels faster than light`,
   `visible from the Moon with the naked eye`, `Octopuses have two hearts`,
   `90 degrees Celsius at sea level`, `born with 206 bones`,
   `never strikes the same place twice`, `third gravity assist`,
   `suborbital trajectories`, `unanimous decision`, `novel-facts fixture`,
   `ground-truth verdicts`, `distractor sentences`.

Result: **zero hits** in all 213 snapshot files and the (empty) knowledge
ledger.

Construction guarantees:
- Beacon tokens NF20260923-BEACON-001..032 were minted at fixture-build time
  (2026-09-23), after every corpus snapshot was taken; no corpus byte can
  contain them.
- Structural facts (A13–A16, B13–B20) describe the fixture corpus itself,
  which did not exist when the corpus was snapshotted.
- Real-world facts (A17–A20, B21–B24) were verified by web search on
  2026-09-23 (ESA announcement for Juice; SpaceX/New Scientist for Starship;
  MMA Junkie for DWCS 93; LiveScore for UWCL scores) and are absent from the
  corpus by the grep above.
