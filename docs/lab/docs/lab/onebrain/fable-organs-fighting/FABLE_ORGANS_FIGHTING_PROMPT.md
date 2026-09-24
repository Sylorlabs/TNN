You are claude-fable-5.1, consulted as a deep auditor for the TNN (native AI) research program. This is ONE batched round — be maximally thorough. Reason as deeply as you can; length is welcome.

# Background

TNN is a from-scratch AI built in pure Zag (a native compiled language, deterministic — no randomness anywhere in decision paths, byte-identical reruns required). Its post-toy architecture has five organs:

1. **Deliberate memory substrate** — conscious, deliberate KB control; silent overwrite is unacceptable; append-only audit ledger with replay to exact state.
2. **Eliminative hypothesis logic** — corroborated elimination of hypotheses.
3. **Deliberate consolidation/promotion** — moves content from provisional to committed through gates.
4. **Symbolic recall and trace composition** — retrieval and composition of memory traces.
5. **Native structural revision** — deliberate revision of committed content (kill/pin/promote/revoke operations).

The "one-brain" program integrates all five into ONE shared ledger/state (parallel deliberation over one brain, not manager-and-staff agents). At the seams the organs FIGHT: conflicting judgments, contradictory claims, promotion-vs-revocation clashes (e.g., the memory organ holds a force-pinned fact while the revision organ is asked to kill it; the consolidation organ wants to promote a provisional that the hypothesis organ just contradicted).

# What is already proven (do not re-litigate these; build on them)

A frozen preregistered battery (frozen §3 per-law battery + §4.2 formal verdict, commit 20ef2fda...) returned the formal verdict **NEEDS A COMPOSITION LAW**: the B0 baseline passes; no integrity-invariant (I1–I6) violation occurs under any tested law; no attack fails under every candidate law; **8 of 10 scored attacks are law-dependent** — their outcome flips depending on which composition law you pick. Composition does not break, but no safe default semantics can yet be declared. Two implementation variants were tested: B (with a since-fixed arbiter defect: its M_COMMIT-through-REVISE path was not FRESH) is the provisional seam-coherence leader at 10/11 vs A's 8/11.

Concrete seam battles already tested (all with preregistered kill bars, byte-identical reruns):
- A2i/A2ii: force-pin semantics (C1 vs C8). A3a: provisional visibility (evidence says provisional content must not become permanent without a gate). A4a/A4b: revocation vs promotion races. A5: provisional destruction/distrust. A6a: learner-pin under contradiction — resolved by PYCC (pin-yields-to-corroborated-contradiction): corroborated contradiction suspends the pin; single-source contradiction does not. A6b: pin/quarantine meet-state.
- Provenance is a missing law: forged REVOKE, spoofed EXT_FORCE_PIN, and forged challengers all EXECUTE against both variants because no law authenticates provenance (finding, not yet law).
- A deterministic SHA-256 hash-chained tamper-evident ledger (C5) is built over the canonical composition ledger: 132/132 tamper probes detected, verdicts unchanged.
- Figure-it-out vs fixed-precedence was tested (A7/C10): both violation-clean; fixed-precedence judgment 20/20 vs deliberative figure-it-out 19/20, the 1-point gap entirely attributable to the (then-unfixed) B arbiter residual. Prediction: deliberation reaches 20/20 with the fix.

# The human's standing laws (treat as constraints, not suggestions)

- TNN must be an "it-can-figure-it-out machine," NOT a rigid needs-policy-for-every-edge-case machine. When in doubt, test both — figure-it-out wins ties.
- More deliberation depth must NEVER make things worse (better or same, never worse). Depths must never be overconfident, period.
- TNN must be scaffold-and-release to not lie: provisional/constructed content must never leak into committed belief without verification.
- Everything is reversible by TNN itself; the only true lock is an audited human/trainer force-pin.
- The ledger is append-only and tamper-evident; conflicts must be ledgered as conflicts, never silently overwritten.

# Your task — three questions, answered thoroughly

**Q1. When organs fight, how should the conflict resolve — figure-it-out deliberation vs rigid policy?**
Be specific, not philosophical. For each major conflict class below, say which mechanism should win and WHY, with the failure mode that decides it:
  (a) memory-substrate pin vs revision-organ kill/revoke on the same slot;
  (b) consolidation wanting to promote a provisional that hypothesis-logic just contradicted;
  (c) recall/composition surfacing a quarantined or provisional trace as a premise in a new deliberation;
  (d) two organs issuing contradictory judgments about the same claim in the same episode (tie).
Steel-man the rigid-policy side honestly for each — where does figure-it-out genuinely risk silent corruption, infinite deliberation, or availability collapse? Where does rigid policy genuinely risk freezing a wrong answer or killing honest throughput?

**Q2. What composition principles keep organ conflicts from corrupting the shared ledger?**
Propose a ranked set of principles (aim for 5–9, ordered by load-bearing importance). For each: the principle stated as a checkable rule, the exact corruption it prevents, and the organ fight that motivated it. Mark clearly which principles are *mechanism* (native crews can build and test them) vs *governance* (they need the human's signature before adoption — e.g., anything that changes what a force-pin means, or who may override whom).

**Q3. What concrete experiments would discriminate?**
For your top 3 principles and for the figure-it-out-vs-policy call in Q1, sketch the falsification battery a native crew would run: fixtures, the exact kill bar, what a PASS vs FAIL vs law-dependent outcome looks like, and which already-tested findings (above) each experiment builds on or re-uses. Assume the crews can build anything in deterministic pure Zag, must preregister kill bars, and require 3× byte-identical reruns.

# Output format

1. Conflict-class rulings (Q1): a table — conflict class | recommended resolver (deliberation/policy/hybrid) | deciding failure mode | steelmanned counter-case.
2. Ranked composition principles (Q2): numbered, each with rule / prevents / motivated-by / mechanism-vs-governance.
3. Discrimination batteries (Q3): one per item, with fixtures, kill bars, and predicted outcomes under each candidate law where relevant.
4. A short "what I would NOT do" section: the tempting-but-wrong resolutions and why they fail.
5. Open questions you could not settle from the evidence given — stated as questions, not hedged conclusions.
