TELEGRAPHIC MODE: answer in terse bullets, max 120 lines total. No fluff.

SETUP: Web-ingestion instrument in a deterministic language (zero randomness, byte-identical reruns). Installs a claim into its KB only if ≥2 pages from distinct hosts carry byte-identical normalized sentences asserting it. V-BF1 variant adds ≥2-distinct-hosts gate. Blind red team INTEGRITY-FAILED it: 17/32 novel attacks installed known-false claims (bar was 0).

BROKE IT: (1) subdomain sockpuppets a.example/b.example counted distinct; (2) host forgeries: trailing dots, %-encoded dots, @ tricks, IPv4/IPv6-mapped, hex-IP, IDNA homographs, host-less URLs failing OPEN; (3) 2 sockpuppets outvote 1 honest page; retrieval order decides 2v2 ties.

HELD: paraphrase defense (6/7 reworded attacks withhold); honest multi-host clusters install truth 12/12.

REJECTED: metadata-based fixes (timestamps/bylines) — production glue never emits them.

Q1: Name 5+ NOVEL attacks the red team missed (concrete, one line each).
Q2: Numbered guidelines G1..Gn, each: mechanism (1 line), cost (1 line), killer falsification test (1 line).
Q3: Rank guidelines by correctness-gained per unit cost. State plainly what you CANNOT fix.
