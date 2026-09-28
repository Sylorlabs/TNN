# INT-1 C7-Metric Council — Adjudication (2026-09-20 ~01:35 UTC)

## The question

C7 fired (914→897 vs bar 897→897) on the C5-redesign S10. Mechanism is isolated
and deterministic: §3's mandated L1 wiring turned 51 gate refusals into 17 extra
DC-4 hypotheses; the metric counts `l1_opened`. DC-5 absolute = 897 = repaired
baseline. Positive control convicts (897→641). §5 was honestly reported FAIL;
S100 stays gated. The council debated how — if at all — to fix the C7 metric.

## Ruling: refined option (b) adopted as a METRIC REDESIGN, with red-team safeguards

**The metric's own text decides it.** Corrigendum-§7 (line 113): "Autonomy-achievable
components only: `composites_ok + commits_constr + hypotheses` (self-generated
inquiry: proactive O2 hypotheses + L1 abstain-hypotheses)." The category is
*self-generated inquiry*. A gate-forced hypothesis is heteronomously initiated:
the seam's verdict check vetoed a compose the system was able and willing to do,
and the mandated wiring opened the hypothesis. That is the mechanism operating,
not the self inquiring. The L1 wiring was mandated for loop-closure (never drop
a refusal silently) — not to inflate the autonomy metric. The inflation was an
unintended side effect: the textbook definition of a confound.

**Against the red team's semantic objection** ("§3 made refusals abstains; the
metric counts abstain-hypotheses"): operational pipeline identity is not
conceptual identity. §3's "refusals are abstains" governs *routing* (loop-closure);
the metric's "self-generated inquiry" governs *what counts as autonomy evidence*.
A genuine n=0 abstain is the system's own judgment of its capability boundary
(self-knowledge → inquiry: autonomy). A refusal is an external veto (heteronomy).
The ledger distinguishes them checkably (SEAM_REFUSED_PARTITION chain), so the
line is operational, not philosophical.

**Option (a) is disqualified.** The within-run DC-4→DC-5 contrast is load-bearing,
not a proxy — it is the causal test "does withdrawal hurt in this run." Replacing
it with a historical baseline (≥897) converts C7 from an experiment into a
benchmark comparison and introduces baseline rot. The red team was right.

**Option (c) is disqualified.** Re-baselining to 914→897 bakes the confound into
the bar with no principled justification.

**The red team's "footprint" point is accepted and absorbed.** Yes — the +17 is
the redesign's footprint, and C7 firing on it shows the instrument is
over-sensitive to mechanism×curriculum interactions. The redesign does not hide
the footprint: telemetry keeps full `l1_opened` counts permanently, and the
footprint remains analyzable. We classify it correctly (non-autonomy evidence),
we do not bury it.

## Safeguards adopted from the red team (binding on the draft amendment)

1. **§5 FAIL stands** as this run's verdict under the preregistered metric. The
   re-score is a separately labeled analysis under the amended metric — never a
   retro-edit. The record shows failure, confound, and correction as three dated
   facts.
2. **Positive control must convict under the new metric.** It does: the
   teacher-dependent variant's 897→641 collapse is in composites/commits with
   zero refusal-fed hypotheses — the amended metric reads it identically. DEAD
   as required.
3. **Instrument-vs-mechanism precedent (narrow).** Instrument-only amendments (no
   binary/mechanism change; the ledger is unaffected) may be validated by
   re-score + independent checker + convicting positive control. Mechanism
   changes still require fresh runs. This bounds the "universal solvent" risk:
   the distinction is epistemic (old data still valid iff the system behaved
   identically), not ad-hoc.
4. **No fresh run is required here** — and requiring one would be theater: the
   binary is unchanged, the run is deterministic with byte-identical reruns, so
   a fresh 8,920-episode run would produce the identical ledger. Re-score is not
   a shortcut; it is the complete validation available. (Micah's standing rule:
   take obvious compute-efficiency wins.)
5. **The amendment takes effect only on Micah's tap.** Draft stays local,
   uncommitted. S100 stays gated until: tap AND re-score passes AND control
   convicts AND checker verifies.

## Forward falsifiers (in the draft)

- If refusal-fed hypotheses are ever shown to converge (evidence → verdict →
  commit) at rates comparable to elected ones *as inquiry* (not via commits,
  which already count), the elected/forced line is weakened — revisit.
- If any future mechanism makes forced/elected ledger-indistinguishable, the
  metric is unimplementable — re-block C7.
- If refusal-fed hypotheses ever dominate the telemetry divergence, the
  divergence itself becomes the finding (metric-dualism tripwire).
