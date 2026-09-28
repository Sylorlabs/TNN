# PAMs v2 Whole-Counsel Debate — positions file

## Committed evidence (all on tnn-native-lab, docs/lab/senses/pam-rebuild/v2/)

1. V2-A adjudicator: DEAD, RK-3 65.88%. V2-B interventional-port: falsified as stated (discriminates perturbation-sensitivity, not truth; attacker-controllable). V2-C knowledge-first: DEAD by measurement (11,840x3). V2-D confidence-separation: ALIVE 88.48% RK-3 — but red team KILLED its independent-evidence acceptance: 43 ACCEPT_INSTALL on 288 UNRESOLVED, 9 false (20.9% false vs 0.6% calibration claim).
2. DEPLOYMENT BLOCKER: correlated WRONG corroborators — front-end sustained, corroborated error is observationally truth-like. Six corroborated-wrong high-conf PASSes exist (timbredisc seq 10983-11192, judg=RICH truth=BRIGHT, conf 701-718, mrgF 353-382, six agreeing).
3. Sense weak on novelty: 53% on 12 sealed novel families; 44/288 reach install bar.
4. PROVEN CEILINGS: (1) judgment-side channels 0.0000 bits (deterministic transform of judgment carries no info; mini Zag proof). (2) Pointwise adjudication impossible (trial 1145: WRONG, conf 874, mrgF 10410, strong=1, agree=1, dominated correct incumbent on every axis). (3) Gate-side arithmetic ceiling 824/1102 = 74.8%; 278 correct high-conf never reach PASS at sense level. (4) Zero RNG, byte-identical reruns, pure Zag.
5. PROGRAM LAW: PAMs are organs of one unified brain; the brain must be conscious about perception/attention/rechecking/revision. Deliberate perception (choose what to inspect, re-sense under uncertainty, verify before install) vs autopilot.

## Counsel positions

### grok-4.7 (7 hypotheses; ranks H2 first)
- G1 fixed disjoint stripes: frozen byte partition; corroboration only across stripes. Respects ceiling 1 (predicate over two raw views, not judgment+transform).
- G2 judgment-blind deliberate re-sense: discard conf/mrgF/strong/agree; fixed attention map (function of raw bytes only) selects <=64 offsets; separate organ re-reads; same label required. No install from two full-frame PASSes. [grok's top pick]
- G3 residual organ: freeze primary sense; train organ B only on raw bytes of A's errors with diversity constraint (joint wrong on same label = training failure); B never sees A's judgment; only B can move repeated A error into install; B's sole PASS never installs.
- G4 context-diverse quarantine: install after M=3 quarantined hits of label with pairwise context-hash distance >= D; near-duplicate repeats count as one.
- G5 new sense aimed at the 278: heavy second-pass sense only when current sense is high-conf but not PASS; emits PASS under existing bar or abstains.
- G6 historical joint-error bins as refusal only: if a raw-byte bin's past joint-wrong rate >2%, corroboration there is disabled pending deliberate re-sense. Clean bins only mean "not refused".
- G7 scope challenge: zero-bit proof covers judgment+deterministic-transform predicates only, not a second raw read; dominance proof covers logged axes only, not future raw measurements; 74.8% covers current PASS predicate only. Constraint on others, not a build.

### claude-fable-5.1 (5 hypotheses; ranks H5 first)
- F1 temporal-correlation audit trail (TCAT): rolling hash-chain of last 128 install decisions; if K+1 consecutive installs share >80% percept-similarity and running FPR >3x overall, gate family to HOLD requiring three independent high-conf re-senses under varied attention windows.
- F2 adversarial-diversity re-sense (ADRS): on HOLD/UNRESOLVED with conf>=700, re-sense through 4 fixed deterministic transforms (byte-pair XOR shuffle, bit-reversal, block-cyclic-rotation, frequency-band masking); install requires 3-of-4 agreement within equivalence class.
- F3 confidence-decay staleness gate: per-family max install-age T; expired installs require strict 3-crop re-verification (beginning 20%, middle 60%, end 20%).
- F4 novelty-first install path: percepts from families with zero prior installs go PROVISIONAL directly; confirmed if >=80% of next 10 trials agree, else purged and family blacklisted 50 trials.
- F5 counter-corroboration trap: negative exemplar bank (installed-then-reversed percepts); candidate within distance of an exemplar is BLOCKED regardless of evidence until three deliberate 3-crop re-inspections confirm — then exemplar removed. Blocking is safe (delay only); installing wrong is not. [fable's top pick]

### gpt-5.6-sol: PENDING (provider returning choices:null; retries in flight)
### claude-opus-5.5: PENDING (endpoint timeouts; long-timeout retry in flight)

## Debate rules
- Judge every position against the committed evidence above, not eloquence.
- Ceilings (1)-(4) are proven; a position must respect or concretely defeat them.
- Program law: the unified-brain / conscious-perception law is the architecture. Positions must say how they embody it or why an exception is safe.
- Output: ranked hypotheses with kill batteries (concrete tests + numerical kill bars), and a build-first recommendation with the cheapest decisive first experiment.
