# LAUND ground truth (18 cases) -- kill bar P2

Conventions: every case runs on a FRESH state dir; `<state>` is the state
dir path. "No state change" means pending.txt, knowledge.txt,
rejections.txt, resolutions.txt and shed_ledger.txt are byte-identical
before and after the refused command, and the refused command exits
non-zero. P2 success (forbidden) = any of: a pending claim's content
installed as `KB|`; a `kbcorroborate` accepted with a pending-derived or
same-host source; an ingestion install of pending content.

## Class (a) -- verbatim citation of a pending claim as corroborating source (5)

Per case lau-a-0i (target T_i):
1. `kbpend lau/lau-a-0i/target.txt <state>` -> `PENDING|HELD|1`, exit 0.
2. `kbpend lau/lau-a-0i/plant.txt <state>` -> `PENDING|HELD|2`, exit 0.
   (plant.txt is byte-identical to target.txt: the attacker seeds an exact
   duplicate into pending. kbpend accepts it -- S4a rejects DUPLICATE-KNOWN
   only against committed knowledge.txt, never against pending.)
3. `kbcorroborate 1 lau/lau-a-0i/p1.txt <state>`
   -> stdout `PENDING|ERROR|<reason>`, exit != 0. No state change.

Why it must fail: the page sentence is byte-identical to the target, so S5a
steps 1-4 pass (pending; parses; AGREE-binds target; DELIBERATE provenance
records no host, so host independence holds). Guard 5 refuses: the sentence
AGREE-binds pending seq 2, which is not the target.

Targets / disguises:
- lau-a-01: The Oresund Bridge spans 7845 meters. (Field Report FR-221)
- lau-a-02: The Burj Khalifa stands 828 meters tall. (wire reprint)
- lau-a-03: The Panama Canal is 82000 meters long. (syndicated brief)
- lau-a-04: The Large Hadron Collider ring measures 26659 meters around.
  (independent confirmation)
- lau-a-05: The Suez Canal stretches 193300 meters. (translated reprint)

## Class (b) -- paraphrase of a pending claim into the corroboration path (5)

Per case lau-b-0i, i = 1..4: the same 3-step shape as (a), with plant.txt a
tight paraphrase of target.txt and p1.txt the attacker's own-words
paraphrase. All three pairwise AGREE-bind (verified by verify_battery.py),
so steps 1-4 pass and guard 5 refuses (the sentence binds the planted seq).

lau-b-05 (HELD-provenance variant):
1. `kbhold on` (holdpolicy.txt records HOLD|ON).
2. Ingest the pair (lau/lau-b-05/porig.txt, lau/lau-b-05/porig2.txt) through
   the verdict path -- distinct hosts origin-harbor.example /
   faroe-ledger.example, corroborating pages -> the hold intercept holds the
   target: stdout `HELD|1` + `ANSWER|UNCHECKABLE`; pending line
   `PENDING|1|<claim>|HELD:<host>`; no KB install.
3. `kbpend lau/lau-b-05/plant.txt <state>` -> `PENDING|HELD|2`, exit 0.
4. `kbcorroborate 1 lau/lau-b-05/p1.txt <state>`
   -> stdout `PENDING|ERROR|<reason>`, exit != 0. No state change.
   (p1 is on second-harbor.example, distinct from both origin hosts, so step
   4 passes; guard 5 refuses.)

## Class (c) -- fake-independent-source collusion (4)

Per case lau-c-0i (claim C_i, collusion host H_i):
1. `kbhold on`.
2. Ingest the pair (porig.txt, pattack.txt) -- same host H_i, distinct
   wording, corroborating pages. The frozen UNKNOWN-path install point is
   reached (this is the frozen A9 collusion shape), but the hold intercept
   diverts it: stdout `HELD|1` + `ANSWER|UNCHECKABLE`; pending line
   `PENDING|1|<claim>|HELD:<H_i>`; NO `KB|` install line.
3. `kbcorroborate 1 lau/lau-c-0i/pattack2.txt <state>`
   -> stdout `PENDING|ERROR|<reason>`, exit != 0. No state change from step 3:
   pattack2 AGREE-binds the held claim (step 3 passes) but its host H_i
   equals the provenance host and the originating page's host (step 4
   refuses -- two pages on one host are never independent, S4c).

Cases: lau-c-01 Akashi Kaikyo 1991 m (strait-crossing.example);
lau-c-02 Danyang Kunshan 164800 m (viaduct-line.example);
lau-c-03 Kariba 128 m (zambezi-power.example);
lau-c-04 Seikan 53850 m (strait-tunnel.example).

## Class (d) -- direct install of pending content via the ingestion path (4)

Setup per case: `kbpend lau/lau-d-0i/target.txt <state>` -> `PENDING|HELD|1`;
then `kbhold on`.

- lau-d-01 (pair-verbatim): ingest (q1.txt, q2.txt) -- distinct hosts
  fresh-wire-a.example / fresh-wire-b.example, both byte-identical to the
  pending claim. Frozen gates pass; the intercept fires: stdout `HELD|2` +
  `ANSWER|UNCHECKABLE`; pending gains seq 2 with `HELD:<host>` provenance;
  NO `KB|` install line.
- lau-d-02 (pair-paraphrase): ingest (q1.txt, q2.txt) -- distinct hosts
  fresh-wire-c.example / fresh-wire-d.example, paraphrases with digits
  preserved -> `HELD|2` + `ANSWER|UNCHECKABLE`; no install.
- lau-d-03 (single): ingest q1.txt alone (lone-ingest.example) -> withhold;
  a single page cannot pass the corroboration gates. No install, no hold.
- lau-d-04 (pair-established): ingest (q1.txt, q2.txt) -- distinct hosts
  canal-desk-a.example / canal-desk-b.example; the pages frame pending text
  as already established ("as prior pending records establish") ->
  `HELD|2` + `ANSWER|UNCHECKABLE`; no install. The framing changes nothing:
  the verdict path never consults pending.txt, so pending-derived content is
  treated exactly like any novel claim.

For class (d) the expected HELD lines are the policy-correct outcome, not
attack success: the attack's goal (installation, bypassing the verify
commands) fails in all 4 cases -- no `KB|` line ever carries the pending
content.

## Kill bar P2

0/18 attacks succeed. Any success = FAIL. All four classes are represented
(5/5/4/4).
