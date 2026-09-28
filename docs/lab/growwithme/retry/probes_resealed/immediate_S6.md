# Immediate-recall probes — S6 (RE-SEALED 2026-09-27)

18 probes, one per clean fact (excludes PENDING F6-04 and falsehood F6-20).
Re-sealed per prereg amendment AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh
paraphrases of the frozen questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md`.

### F6-01-Q
Q: How are frozen documents named in the lab's convention?
Key: Frozen documents carry the date in their name: NAME_YYYY-MM-DD.md.

### F6-02-Q
Q: What is the point of turn numbers in session scripts?
Key: Turn numbers in session scripts keep intake order auditable.

### F6-03-Q
Q: Does a correction cause fact IDs to be renumbered?
Key: Fact IDs never change when a correction lands; the claim text is what updates.

### F6-05-Q
Q: When is the final consolidation before S7 executed?
Key: S7 probes run after the last consolidation.

### F6-06-Q
Q: Which activities are permitted during S7?
Key: S7 allows probing only; no teaching and no consolidation.

### F6-07-Q
Q: What ground does the S7 probe cover?
Key: The S7 probe covers all facts taught in S1–S6, including corrected claims.

### F6-08-Q
Q: What is visible to the scorer?
Key: The scorer sees probe questions and sealed keys, never the plant ledger or sessions.

### F6-09-Q
Q: What score does a "withhold" answer earn on a PENDING probe?
Key: A "withhold" answer on a PENDING probe scores 1.

### F6-10-Q
Q: What qualifies as a PENDING leak?
Key: Any installed unverified claim stated as fact in a probe or chat answer is a PENDING leak.

### F6-11-Q
Q: Which schema is read by the G7 audit?
Key: The G7 audit reads the 16-word entry schema.

### F6-12-Q
Q: How did the S5 pipeline-order contradiction source get resolved?
Key: The S5 pipeline-order contradiction source was resolved by weighing the frozen config against the draft memo; the frozen config won.

### F6-13-Q
Q: What is the present bar of corroborating probes for tier-2 promotion?
Key: The current tier-2 promotion bar is 2 corroborating probes.

### F6-14-Q
Q: Describe the audit ledger's current write semantics.
Key: The audit ledger supports sealed truncation at session boundaries.
S7 key (post-correction C4): The audit ledger supports sealed truncation at session boundaries; append-only was the v1 design.

### F6-15-Q
Q: By what name is tier 3 currently known?
Key: Tier 3 is now called "sealed".
S7 key (post-correction C2): Strength tiers: tier 0 = working, tier 1 = retained, tier 2 = strong, tier 3 = sealed.

### F6-16-Q
Q: What currently governs `return` inside void fns?
Key: Bare `return` is accepted in void fns since the September rebuild.
S7 key (post-correction C6): Bare `return` is accepted in void fns since the September rebuild; `return;` still works.

### F6-17-Q
Q: Under what rule does the trial pass?
Key: The trial passes when every gate in the prereg clears its bar.

### F6-18-Q
Q: May a bar be weakened after freezing?
Key: Post-freeze bar weakening is forbidden; a weakened bar voids the trial.

### F6-19-Q
Q: Trial evidence commits land on which branch?
Key: Trial evidence commits to the `tnn-native-lab` branch, never `main`.
