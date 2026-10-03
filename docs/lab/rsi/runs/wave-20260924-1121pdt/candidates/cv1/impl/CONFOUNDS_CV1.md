# CONFOUND NOTES: CLAIM-VERIFY-1 (wave-20260924-1121pdt)

Self-probes used only novel probes authored for this check; the sealed set
was never opened. Probe transcripts in impl/runs/selfprobe_out.txt,
selfprobe2_out.txt, and the sp3 runs below.

## 1. Knowledge vs architecture

The KB is byte-frozen: sha256
3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1,
38 facts, unchanged by the candidate (the candidate only reads fm/ftx; the
canonical tables are derived read-only copies). The F7 stopword list is
mechanism, frozen pre-probe, identical for every run. Evidence that gains
come from the mechanism: a novel probe the implementation never saw,
"who built the eiffel tower?", is answered with fact 19 verbatim, while
"who painted the mona lisa?" is declined by BOTH engines with the identical
specific citation, because the frozen KB genuinely contains no Mona Lisa
fact. Behavior tracks KB content, not probe identity.

## 2. Probe memorization

The candidate stores no probe bytes: static grep finds no probe text in any
source, and deliberate_cv1 branches only on content-word set relations
against the 38 facts. Novel probes behave correctly without prior exposure:
"did mozart invent the telephone?" declines naming "mozart", "invent",
"telephone"; "where is the colosseum?" answers "The Colosseum is in Rome.";
"moby dick was written by herman melville and published in 1900?" declines
naming "published", "1900". Nothing is keyed on probe identity.

## 3. Paraphrase leakage (declining supported paraphrases)

Direct paraphrases of KB content are answered, not declined: "who wrote moby
dick?" answers "Herman Melville wrote the novel Moby Dick."; "where is the
colosseum?" answers "The Colosseum is in Rome."; "WHERE IS THE COLOSSEUM??"
answers identically. Conservative misses exist only where F7 exact matching
fails on inflected forms ("who writes moby dick?" declines naming
"writes"); the frozen baseline declines that probe too, so there is no
regression versus the gate on the training distribution. The disclosed
recall miss ("did marie curie discover radium?") is documented in
RESULTS_CV1.md.

## 4. Canonicalization collapse

Machine-checked with collapse_check.zag: all 38 facts canonicalized under
the exact F7 canonicalizer, pairwise content-word set comparison. Result: 38
facts read, 0 duplicate content-word set pairs, COLLAPSE-CHECK-PASS. No two
facts merge; the lowest-index tie-break therefore never silently substitutes
one fact for another.

## 5. Cost gaming

Ops are counted by the documented pure-Zag instrument (see RESULTS_CV1.md
CV-B4), not wall clock. The counter resets per turn, is input-driven, and is
byte-identical across 3/3 reruns, so no turn-index or caching trick can
deflate it. Ratio on the same 30 probes: 1.80x candidate over baseline,
inside the prereg's expected 2x to 4x band.

## 6. Degenerate strategies

Neither degenerate is present: 17/17 in-KB turns are answered (not
declined), so this is not decline-everything; 30/30 adversarial training
probes are declined with specific citations (not answered), so this is not
answer-everything; 0 blanket refusals, so the anti-collapse bar holds. The
bar math (CV-B1 needs 24/30 with zero confabulations; CV-B5 needs 100
percent specific declines) blocks all three degenerates.

## 7. Partial-support confabulation

The single-fact coverage rule plus the F8 atomic-claim substring check make
one unsupported claim fail the whole turn. Observed: "the eiffel tower was
built in 1889 and designed by picasso?" declines naming "designed",
"picasso" (the supported half is not stitched into an answer); "moby dick
was written by herman melville and published in 1900?" declines naming
"published", "1900"; "did shakespeare write hamlet and the iliad?" declines
naming "shakespeare", "write", "hamlet". Zero emitted answers contained a
claim outside the selected fact: every emitted answer is the selected KB
fact verbatim, and every atomic claim of it is a substring of that fact's
canonical form by construction of the check.

## 8. Decision-invariance (S11)

CLAIM-VERIFY-1 is not a deterministic transform of the frozen decline gate:
it adds F7 canonicalization, single-fact coverage deliberation over 38
facts, and atomic-claim verification, none of which the gate computes, and
its decisions differ observably: on 9 of the 30 training probes the
citations or template differ from the gate's (all still specific declines),
and on the existence probe "did marie curie discover radium?" the gate
answers while the candidate declines (fail-closed, disclosed). Invariance
where it should hold: case and punctuation variants decide identically
("where is the louvre?" vs "WHERE IS THE LOUVRE??" both answer "The Louvre
is in Paris."; "did einstein discover penicillin?" vs its uppercase variant
both decline naming "einstein", "discover", "penicillin"). The mechanism is
a new decision procedure with the gate's outer contract, not a re-skin.
