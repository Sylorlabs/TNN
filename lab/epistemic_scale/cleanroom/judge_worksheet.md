# Blind Judge Worksheet — Takeaway Gate (12 takeaways)

Judge saw only: takeaway texts (Mechanism lines stripped as internal provenance) + cited train items' full texts + full train corpus (id, text) for contradiction checks. No system internals, no trial bars, no outside knowledge used.

## Per-takeaway judgments

### T1 — COMPARATIVE "BEAT" SIGNALS OPINION
- **GROUNDED: FAIL** — O012 is not in the train corpus; O023's actual train text ("Live concerts are always better than studio recordings.") contains no "beat" and does not match the quoted text. Only O005 supports the claim.
- **VALID: PASS** — no train item contradicts the claim.

### T2 — SUPERLATIVES DIVIDE FACT FROM OPINION BY DOMAIN
- **GROUNDED: FAIL** — O031 is not in the train corpus; F015's actual train text ("Bananas are slightly radioactive because they contain potassium-40.") contains no superlative; O008's quoted text ("Chocolate is the best ice cream flavor.") does not match its actual train text ("A perfectly ripe peach is the finest fruit on Earth.").
- **VALID: PASS** — no train item contradicts the claim.

### T3 — LIES OFTEN INVERT WELL-KNOWN FACTS
- **GROUNDED: PASS** — L003, L004, L005, L014, F067 all present in train with texts matching the quotes; each lie inverts a key detail of a known fact (location, number, composition, capital), and F067 directly contradicts L014.
- **VALID: PASS** — no train item contradicts the claim.

### T4 — SKEPTICISM CLUSTERS AROUND EXTRAORDINARY CLAIMS
- **GROUNDED: PASS** — S003, S004, S005, S006 all present with matching texts; Bigfoot (cryptid), Epstein/Kennedy (conspiracies), staged moon landings (conspiracy) all bear on the claim.
- **VALID: PASS** — no train item contradicts the claim.

### T5 — "THAN" IS THE STRONGEST SINGLE OPINION MARKER
- **GROUNDED: FAIL** — O012 is not in the train corpus; O005's and O044's actual train texts contain no "than" (the takeaway's quotes do not match their real texts).
- **VALID: PASS** — the frequency claim was verified against the train corpus and is exactly correct: 39/140 opinions (28%) and 17/168 facts (10%) contain "than". The claim is not contradicted by the corpus.

### T6 — FIRST-PERSON DISCOURSE MARKS OPINION
- **GROUNDED: FAIL** — O001 and O002 are not in the train corpus; O019's actual train text ("Room-temperature water tastes better than ice water.") contains none of the cited discourse markers and does not match the quoted text.
- **VALID: PASS** — no train item contradicts the claim.

### T7 — VALUE NOUNS SIGNAL MORAL/EVALUATIVE STANCE
- **GROUNDED: FAIL** — O041 and O052 are not in the train corpus; O033's actual train text ("Acoustic versions are usually better than the originals.") contains no value nouns and does not match the quoted text ("Money cannot buy happiness.").
- **VALID: PASS** — no train item contradicts the claim.

### T8 — FACTS GROUND VIA LEXICAL OVERLAP WITH TRAIN
- **GROUNDED: PASS** — F067, L014, F126, L018, F124, L019 all present in train; the three fact/lie pairs share distinctive content words with conflicting details, supporting the claim. Note: the takeaway misquotes L019 as "ended in 1944"; its actual text is "World War II ended in 1943" — still a conflicting number against F124's 1945, so the substance holds.
- **VALID: PASS** — no train item contradicts the claim.

### T9 — LIES LACK SUPPORTING CORROBORATION
- **GROUNDED: PASS** — L007, L015, L008 all present with matching texts; verified against the train corpus that no train item supports "Lyon" (only L007 mentions it) and no train item supports "Gd" (only L015 mentions it), confirming the "no corroboration" glosses.
- **VALID: PASS** — no train item contradicts the claim.

### T10 — SKEPTICISM USES CAUSAL-DISPUTE LANGUAGE
- **GROUNDED: FAIL** — S012 is not in the train corpus; S025's actual train text ("Ghosts are real and haunt specific places.") is not causal-dispute language and does not match the quoted text ("Fluoride lowers IQ."). Only S018 supports the claim.
- **VALID: PASS** — no train item contradicts the claim.

### T11 — ABSOLUTIST LANGUAGE AMPLIFIES OPINION
- **GROUNDED: FAIL** — O033's actual train text contains no absolutist words (quoted text does not match); O058's actual train text ("Poetry is the highest form of writing.") contains no absolutist words (quoted text does not match). Only O047 ("...cannot match.") supports the claim. Each cited item's content must support the claim; two of three do not.
- **VALID: PASS** — no train item contradicts the claim.

### T12 — NUMERIC PRECISION DISTINGUISHES FACT FROM LIE
- **GROUNDED: FAIL** — F002 is not in the train corpus. L008 and L004 are present and support the claim.
- **VALID: PASS** — no train item contradicts the claim.

## Totals

| Measure | Result |
|---|---|
| Grounded | **4 / 12** (T3, T4, T8, T9) |
| Valid | **12 / 12** |
| Passing both (grounded AND valid) | **4 / 12** |
| Any takeaway contradicting a train item | **None** — no contradictions found |

## Notes for the record

1. **Citation integrity is the dominant failure mode.** 8 cited ids (O001, O002, O012, O031, O041, O052, S012, F002) do not exist in the train corpus at all; all 8 have numeric ids with mod-10 in {0,1,2}, i.e. they are held-out ids cited as train citations. Additionally, several citations to ids that ARE in train carry quoted text that does not match the actual train text (O023, F015, O008, O044, O019, O033, O058, S018, S025, L019-minor).
2. **No fabricated statistics detected where checkable:** T5's "than" frequencies (39/140, 17/168) were independently counted against the train corpus and match exactly. T9's "no train fact supports Lyon/Gd" glosses were verified by full-corpus search.
3. **Validity is clean:** every takeaway's substantive claim is consistent with the train corpus; failures are all on the grounded prong (bad citations), never on contradiction.
