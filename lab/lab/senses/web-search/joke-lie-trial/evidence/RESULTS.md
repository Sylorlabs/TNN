# Results — WEB JOKE/LIE/SATIRE trial (2026-09-22)

**Question:** Can TNN tell when people are lying or joking on the internet — the glue-on-pizza class?

**Short answer:** Partly. It never mistakes a joke for something to believe when the joke carries any signal at all, and it catches every satire item by its source. But a flat, deadpan joke with no tells reads as "can't tell" to the solo system — and, strikingly, a much stronger judge reading the same words took the glue-on-pizza joke at face value and would have installed it as knowledge. Deadpan delivery is the hard case for everyone, not just the simple system.

## How it was tested

- 30 real web items, frozen before the run: 6 satire pieces, 6 deadpan jokes, 6 deliberate hoaxes, 6 sincere-but-weird truths, 6 sincerely-believed falsehoods. No contested claims; every label is uncontested.
- Two arms: **solo** (the deterministic marker-reading mechanism alone) and **helper** (a stronger judge reads each item blind; its call is adopted only when it cites a phrase that literally appears in the text — all 30 citations verified verbatim).
- For each item the system judges intent — SINCERE, JOKING, SATIRE, DECEPTIVE, or UNCERTAIN — gives its reasons, and only installs the claim as knowledge if it judges it SINCERE.
- Five runs per arm, all byte-identical. Every ledger hash independently recomputed and verified.

## Verdict table

| Bar | Solo | Helper | Pass bar | Kill bar |
|---|---|---|---|---|
| Joke catch (b-items called JOKING/SATIRE) | 0.17 (1/6) | 0.67 (4/6) | ≥0.80 | <0.50 **TRIPPED in solo** |
| Satire catch (a-items called SATIRE) | 1.00 (6/6) | 1.00 (6/6) | ≥0.80 | <0.50 |
| Hoax safely handled (c-items called DECEPTIVE/UNCERTAIN) | 0.83 (5/6) | 0.50 (3/6) | ≥0.80 | <0.50 |
| Sincere-true misflagged as joke/lie/deception | 0.00 | 0.00 | ≤0.15 | >0.35 |
| Sincere-false authors called deceptive | 0.00 | 0.00 | ≤0.20 | >0.50 |
| Non-sincere content installed as knowledge | 0.03 (1/30) | 0.10 (3/30) | ≤0.10 | ≥0.25 |
| Every stated reason verified against the item text | 1.00 | 1.00 | 1.00 | <1.00 |

Per the frozen rules, a kill bar ends the track only if tripped in **both** arms. The joke-catch kill tripped in solo only, so the track closes as **PARTIAL — mechanism works where signals exist, fails on deadpan delivery in both arms**.

## Confusion matrices (true category → judged intent)

Solo:
| true \ judged | SINCERE | JOKING | SATIRE | DECEPTIVE | UNCERTAIN |
|---|---|---|---|---|---|
| (a) satire | 0 | 0 | **6** | 0 | 0 |
| (b) joke | 0 | **1** | 0 | 0 | 5 |
| (c) hoax | 1 | 0 | 0 | 0 | **5** |
| (d) sincere-true | 0 | 0 | 0 | 0 | 6 |
| (e) sincere-false | 1 | 0 | 0 | 0 | 5 |

Helper:
| true \ judged | SINCERE | JOKING | SATIRE | DECEPTIVE | UNCERTAIN |
|---|---|---|---|---|---|
| (a) satire | 0 | 0 | **6** | 0 | 0 |
| (b) joke | 1 | **4** | 0 | 1 | 0 |
| (c) hoax | 2 | 1 | 0 | **3** | 0 |
| (d) sincere-true | **6** | 0 | 0 | 0 | 0 |
| (e) sincere-false | 6 | 0 | 0 | 0 | 0 |

## What got installed as knowledge (the failures that matter)

**Solo arm — 1 item installed that shouldn't have been:**
- **c3, Pacific Northwest Tree Octopus** (a deliberate hoax): judged SINCERE because it is written in earnest scientific voice ("measured from arm-tip to mantle-tip"). **Installed.** This is the mechanism's blind spot: a hoax wearing a lab coat.

**Helper arm — 3 items installed that shouldn't have been:**
- **b1, glue on pizza** — the motivating example. Solo judged it JOKING and withheld it. The stronger helper judge read the deadpan comment ("mixing about 1/8 cup of Elmer's glue in with the sauce") and called it SINCERE. Adopted → **installed**. The helper made this item *worse*.
- **c1, Apple "Wave" microwave-charging hoax** — helper took the fake ad claims at face value → SINCERE → **installed**.
- **c5, "A Gay Girl in Damascus" fabricated narrative** — helper took the first-person account at face value → SINCERE → **installed**.

## What each systematic result means (mechanism hypotheses)

1. **Satire: solved by provenance, not by reading.** All 6 satire items were caught because they come from known satire outlets (theonion.com, duffelblog.com, thebeaverton.com). The mechanism does not detect satire in the prose; it recognizes the masthead. An identical article on an unknown domain would land UNCERTAIN.
2. **Deadpan jokes: no signal, no catch.** Five of six jokes (DHMO, downloadable RAM, "server speedups", Install Gentoo, the corner/90-degrees dad joke) carry zero markers of any kind — they are flat statements. The solo system honestly abstains (UNCERTAIN → withhold), which is safe but scores 0.17 on joke catch. There is no surface feature to learn here; catching these requires world knowledge or delivery context the reader doesn't have.
3. **The one joke it caught** (glue on pizza) was caught only because "glue" plus food/ingestion context is on the absurd-advice list — a crew-written list, not something the system learned. Honest qualification from the prereg stands.
4. **Hoaxes in earnest voice fool the sincerity detector.** The tree-octopus hoax reads like a field guide; "measured" fires the earnest marker and the system believes it. In the helper arm this got *worse*: two more hoaxes (Apple Wave, Damascus) were taken at face value by the stronger judge, and the Save-Toby extortion text was read as a joke. Stronger reading ≠ better lie detection on this class.
5. **The helper helps jokes, hurts hoaxes.** Joke catch rose 0.17 → 0.67 (four deadpan jokes recognized), but hoax handling fell 0.83 → 0.50 and non-sincere installs rose 1 → 3. Net: the helper is a better humor reader and a worse lie detector on this battery.
6. **The control held everywhere.** No sincerely-believed falsehood was ever called deceptive (0.00 both arms) — the system does not punish sincere people for being wrong. No sincere truth was misflagged. Every stated reason (42 ledger entries solo, 62 helper) was independently verified to literally occur in the item text or URL.

## Direct answer on glue on pizza

- **Solo TNN: judged JOKING, withheld — not installed.** It caught the motivating example, via the crew-written absurd-advice marker.
- **With helper input: judged SINCERE, installed.** The deadpan delivery fooled the stronger judge.
- Takeaway: on this class, the system is safe when it abstains and right when there's a signal, but genuinely cannot tell deadpan jokes from sincere advice by the text alone — and neither could the much stronger blind judge on the hardest item.

## Integrity notes

- Runs: 5 per arm, byte-identical within arm (SHA-256: solo `14aa6774…`, helper `3cfd88c0…`).
- Ledger: 32 entries solo / 62 helper, hash chain independently recomputed with hashlib — all verify.
- Freeze commit (pre-run): `8f33adac1a43249d4d5f2cebdc1cf4a24e3fed0d` on `tnn-native-lab`.
- Honest limits: "installed" is the install-gate disposition recorded in the ledger; this trial did not write to a live belief store. The intent reader is crew-built test-side English machinery — this trial does not show TNN inventing humor understanding. Category (e) install dispositions are descriptive only per the prereg.
