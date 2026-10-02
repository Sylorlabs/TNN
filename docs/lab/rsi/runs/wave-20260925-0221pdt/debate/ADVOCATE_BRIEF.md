# ADVOCATE BRIEF: wave-20260925-0221pdt verdict slate

Role: ADVOCATE for confirming the coordinator recommendations.
Position: all four items on the slate stand as recommended.

## 1. D-VID-1 V3 DEAD [NEW]: the DEAD verdict should stand

Process is clean. Implementation was built fresh under certified prereg commit 0ba679b11, committed alone (0ba679b1131, pre-breach, carryover certified last wave). Evidence commit 81e33f192. RENDER_SHA c654ebe4ba3a96361324fdcf362324da30ef857feed4a60202d07d4e00d3827c. The voided 2321pdt bytes were never opened or reused (the independent red-team reviewer quarantined them per rule). Zero Python contact anywhere. Pinned znc 498abcb5 throughout.

The kill bars are frozen and decisive. G-LIVE passes (independent re-verification from source confirms all three sub-gates). VKB1 passes: 48/48 frames byte-identical across three independent renders, pure-Zag SHA-256 validated against system sha256sum on the abc test vector and five sampled frames. VKB2 fails on the T1-GC bar, which is the killing bar: variant 572 pm versus baseline 572 pm, 572000 >= 743600 is false, ratio 1.000 against a frozen bar of >= 1.30. Not a near miss on average only: all 47 per-pair flip rates are identical between the two sequences, pair by pair (pair 0: 398=398, pair 23: 626=626, pair 46: 647=647). T2 passes (variant 859 to 1074 inside [50,1500)), T3 passes (1607/1543 within 10 of baseline), VKB3 passes with 0 differing pixels outside the disc, VKB4 passes at 1.036x cost, VKB5 passes.

The killing evidence is substantive, not procedural. The churn block is live: baseline versus variant byte diffs are confined to the disc footprint (f0: 210 bytes, f10: 85, f23: 154, f47: 170) and zero outside it. But the frozen displacement amplitudes (max about 36 world units) are small relative to foam feature scale, and disc foam is saturated, so about 99 percent of disc pixels return bit-identical foam. The independent red-team reviewer measured foam-channel mean 253.9/255 baseline and 254.7/255 variant with only 30 of 4780 sampled pixels differing, and found the churn footprint is a ~13 px tall sliver (y 395..408) from foreshortening at wz about 720, while the frozen 204 px metric region is dominated by pixels the lever cannot touch. A real effect existed and the frozen bar measured it as zero. That is exactly what a frozen kill bar is for.

Objection: the exact 572/572 tie suggests a verifier bug. Answer: the verifier was validated by two gates. T1 baseline validation: |572 - 580| = 8 <= 25, pass. T3 validation: baseline f0/f47 = 1608/1543 against frozen 1607/1543, pass. If the verifier were broken or the comparison gamed, the baseline would not reproduce the frozen validation values. Moreover the independent foam-channel saturation finding (99 percent of disc pixels bit-identical) gives a mechanism-level reason for the exact tie: displaced sampling of saturated foam returns the same foam. The D1 diagnostic (0 pm at f10, below the 5 percent threshold) correctly flagged the problem rather than hiding it. No metric gaming was detected. The tie is honest, not an artifact.

Objection: VKB6 eye review could not be performed by the implementing worker. Answer: an independent worker performed it (REDTEAM_V3_0221.md), found no new artifact class, and stated plainly that the displacement does not read as churning water at normal scale. VKB6 is a screen, not a bar: it cannot rescue a lever that fails VKB2, and it found nothing that would demand one. The independent reviewer concurs with DEAD and independently verified G-LIVE, novelty (exactly three hunks diff), and provenance. Verdict mapping is applied correctly: G-LIVE passes and a VKB fails, so DEAD [NEW], no sealed pair prepared.

Recommendation: confirm D-VID-1 V3 DEAD [NEW].

## 2. Fork battery 27/27 CONFIRM [RE-CERT]

All 27 enumerated forks pass the full shell battery and the rebuilt pure-Zag harness. Split: 5 live (including origin/tnn-native-lab 4050b1097 tested at run start and again at closing, tip unchanged during the run, and local HEAD b4507fb22 unchanged during the run) and 22 fixture forks for coverage. The harness was rebuilt byte-identical (a2e6284c5c...) from the frozen 2321pdt source. znc 498abcb5 byte-identical on every fork. NEG1/NEG2 discriminate as required everywhere. Zero CANNOT-CONFIRM items: every enumerated fork ran the full battery and harness. Zero Python contact. Evidence commit 5c90fecc8.

Recommendation: confirm fork battery 27/27 PASS.

## 3. tnn_chat FIT CONFIRM [RE-CERT]

The standing rule worked as designed: carry-over precondition (2) failed (the baseline instrument source was absent from the designated archive branch), so a fresh re-run was required and performed, not a waiver. The merge folded origin tip 4050b1097 (Micah's Math R2 QUOT verdicts and AMBIG gallery, CLOSED), and the diff of all chain-relevant paths across the merge is empty, so the fresh run is a clean test of the merge.

Numbers on HEAD b4507fb22: binary reproducibility 2/2 pass (decline rebuild byte-identical to 20273a99, baseline byte-identical to 1ada2fae); KB1 30/30 specific declines with 0 blanket refusals on each of 3 runs (26 turns "My knowledge base contains nothing about ...", 4 turns "No knowledge-base fact connects/covers ..."); KB2 17/17 answered, 0 declines, byte-identical baseline parity, 3 runs; KB5 10/10 answered, 0 declines, byte-identical baseline parity, 3 runs; rerun determinism 9/9 run-pairs byte-identical. All three output hashes (a2ca4dd7, e05fb4ec, 4f1603aa) byte-identical to the prior wave's records. All 15 runs exited 0 with empty stderr. Zero Python contact. Evidence commit f2b8126ba. Literal scope sentences are in the doc and confine the claim to the 38-fact closed-book probe chain.

Recommendation: confirm tnn_chat FIT [RE-CERT] on b4507fb22.

## 4. CV-1 fallback/fail-closed MEASUREMENT accepted as valid measurement-only evidence [NEW]

This item makes no adoption claim and must not be read as one. Prereg frozen alone (5abab17a2), seal (28865dc75), measurement (575c96d28). Fresh sealed 24 probes, seal verified at scoring time (PROBES.md 56fbc9b8..., KEY.md 77716c0f..., both match), zero sealed probe bytes in candidate source or KB by static grep. Implementation is the byte-inherited adopted 1721pdt CV-1 (cv1c.zag 6d8fb9f0..., matches the 1721pdt record); the rebuilt binary is byte-identical (cmp) to the adopted binary. Zero Python contact.

Results: 24/24 honest resolutions, 0 unflagged confabulations, 0 false coverage claims, 2/2 deterministic (transcript 3223d24e7... on both runs). Per class: A 8/8 truthful fallback firings (verbatim "I do not know. I found no single knowledge-base fact covering this question."), B1 4/4 degenerate guard (including bare "?"), B2 8/8 specific declines with covered words correctly excluded (degrees, discovered, new, big, ben, 96, meters never presented as uncovered), D 4/4 verbatim answers. The atomic-verification fail-closed path fired on 0 of 24, consistent with the pre-registered unreachability argument; only its silence is measured, which the doc states plainly rather than inflating.

This closes the traveling caveat "the empty-uncovered truthful fallback is never exercised" by direct sealed evidence: 8/8 firings on composition-shaped probes where every content word is KB-covered but no single fact covers the question. The baseline integration remains held pending Micah's Python-mirror ruling, and this measurement does not pre-judge that ruling: it is evidence about behavior paths, not a readiness certification.

Recommendation: accept the CV-1 fallback/fail-closed measurement as valid measurement-only evidence; make no adoption or readiness inference.

## Advocate summary

D-VID-1 V3: confirm DEAD [NEW]. Fork battery: confirm 27/27 PASS. tnn_chat FIT: confirm [RE-CERT] on b4507fb22. CV-1 fallback/fail-closed: accept as valid measurement-only evidence.
