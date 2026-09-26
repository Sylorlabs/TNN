# Skeptic report: wave-20260926-0521pdt

The skeptic argues AGAINST: gaming, confounds, weak bars, cost. The
hardest attacks are pressed on the FIT precondition (3) qualification,
the 0221pdt python3-contact classification and whether its battery
results can be backfilled as evidence at all, and whether the 33/35
headline travels honestly. The standing provenance probe appears
verbatim once per item. No em-dashes are used in this file.

## Item 1. Fork battery 0521pdt

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer: the 35 named entries and their 33 RESULT files are new
measurements produced this wave in a fresh scratch dir; the instruments
are inherited byte-identical (harness source extracted from the 2321pdt
archive branch, built binary byte-identical to a2e6284c...; pinned znc
498abcb5...; probe source 3b29aa06...; the battery fixtures). New versus
inherited: the measurements are new, the instruments are inherited, and
the two live commits (d0076134d, 6c3c7b69c) are the only genuinely new
code under test.

Attacks:

1. The 33/35 headline is the laundering risk. 35 named entries cover
only 27 unique commits, and 8 of the 35 are named duplicates. Anyone
repeating "33 of 35 pass" without the duplicate caveat inflates the
apparent coverage. Precedents P1 and P8 require the verdict line to
carry entry count, unique-commit count, unique live-commit count, and
the duplicate caveat, and require that short forms never travel without
the caveat. The draft verdict complies on paper; the skeptic demands
the caveat travel in every downstream summary, not just the committed
file.

2. The 2 FAILs: calling them "extraction FAILs" is honest, but the
headline "33 PASS" can be misread as "the toolchain failed nowhere,"
which is true, or as "everything was tested," which is false. pull/1
and pull/2 remain uncovered. The extraction-FAIL caveat must travel
with the headline, and the next-wave pickup directive must keep
naming them until their trees gain the pinned toolchain path.

3. The transit wording in the results file leans on "0221pdt-tested"
for 1c3f9571, aaabb0b89, and 58dd10ae8. But the 0221pdt battery evidence
is superseded under item 4, so "0221pdt-tested" cannot serve as an
evidentiary premise. The skeptic requires the transit claim to be
re-anchored: these commits are transitively covered for current-tip
purposes because this wave verified their ancestry of the directly
tested tips d0076134d and 6c3c7b69c with merge-base --is-ancestor,
period. The 0221pdt-testing history may remain as a historical note,
explicitly marked superseded, never as the premise.

4. The local working copy was tested with its own znc and probe
directly rather than via git-show extraction. That matches prior-wave
practice and the working copy was at run-start HEAD with no tracked
modifications by the worker, but it is the one entry where the
measurement instrument and the measured tree are not separated. Noted
as a standing methodological asymmetry, not a finding.

5. The battery never executes the merged frontier code; the
toolchain-stability scope stamp is load-bearing. The skeptic insists it
travel with the verdict line verbatim.

## Item 2. FIT carry-over

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer: the 10 chain inputs are inherited byte-exact from the frozen
1421pdt/0221pdt records; the cited determinism numbers (2/2 binary
reproducibility, 9/9 rerun pairs, KB1/KB2/KB5 results and output
hashes) are inherited from certified prior re-runs. New this wave: the
sha256 measurements of all 10 inputs at d0076134d, the six
parent-to-merge diffs across the three merges in range
9526cdb5c..d0076134d, and the D1-hazard-closure verification. New
versus inherited: every byte of chain content is inherited; the
evidence that nothing changed is new.

Attacks:

1. This is the core contested call. Precondition (3) was recorded in the
1421pdt standing rule as a literal empty-diff check, and it passed
literally there. This wave the worker measured real deltas, then
re-read the rule as "no content changes" and declared a qualified PASS.
That is a post-hoc reinterpretation of a standing precondition. The
loop's hardest rule is "never weaken a frozen kill bar to force a
pass." The skeptic's position: either the precondition means what it
says and this wave orders a literal fresh re-run, or the judge openly
records the reinterpretation as a new precedent with its exact
boundary, so it can never quietly widen later.

2. The skeptic concedes the evidence on its own terms: zero
modifications, zero deletions, zero content changes to any frozen input
across all six diffs (independently re-verified this session); the
additions are the sha-verified D1 freeze the 1421pdt record itself
recommended; the znc "M" is a mode-only change with an identical blob
sha in all eight commits examined; the scratch additions are
byte-exact to frozen fixture shas. The cryptographic case is strong.
The skeptic's objection is procedural, not evidential: a qualified
precondition should not be self-certified as PASS by the same worker
that measured it without the debate recording the qualification's
boundary as precedent.

3. The determinism evidence is cited, not re-run. That is what the
carry-over rule permits, but it concentrates trust in the 1421pdt and
0221pdt records. The skeptic notes the chain of custody explicitly: the
9/9 byte-identical pairs and the 2/2 binary reproducibility come from
FIT_1421.md and TNCHAT_FIT_0221.md. If either record were ever
re-opened, this carry-over re-opens with it. The verdict line must not
imply a fresh re-run happened; the draft is explicit that none did,
which the skeptic credits.

4. The README.md uncommitted modification is documentation only, but it
means the fit_authority directory is not quiescent right now. The
skeptic accepts it does not touch any chain input, while noting that a
"never-pruned" authority path that is concurrently edited by another
worker is a coordination surface worth watching.

5. Cost check: a fresh re-run would cost one deterministic rebuild and
15 probe runs against byte-identical inputs. Cheap. The skeptic's
honest accounting: the re-run is affordable, but it would add zero
information given byte-exact inputs and recorded 9/9 determinism. The
real question is precedent hygiene, not compute.

## Item 3. Interactive TNN

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer: everything under judgment is inherited. The frozen binaries
(1ada2fae..., 20273a99...), the instrument sources, kb.txt, gaz.txt,
and the pinned znc all come from prior waves' certified records; their
shas were re-verified this wave. New this wave: only the negative
result, the entry-point greps on this tip returning zero. New versus
inherited: the absence finding is new; every artifact it is about is
inherited.

Attacks:

1. "EXISTS" is doing quiet work. The binaries are ELF x86-64 and their
shas match, but no probe chat was run this wave and no binary was
executed by this worker. Existence is verified by file plus sha256sum
only. The skeptic requires the verdict to say exactly that: runnable
artifacts exist and are sha-verified, not that interactivity was
demonstrated this wave.

2. The entry-point grep is a negative result from two regex passes. The
skeptic accepts it while noting the limit of the method: it finds
entry points matching known signature patterns. The one false positive
("repl" inside "replication"/"replay") was correctly identified and
followed up. No stronger claim than "no source-level chat/REPL/
interactive-loop entry point matching the checked signatures in
src/zag/ or units/ on this tip" is warranted, and the draft stays
inside that bound.

3. The confabulation caveat is load-bearing and must travel: these
instruments are supervised red-team probes, not an interactive TNN. Any
summary that drops the caveat turns a diagnostic instrument into a
product claim. The skeptic flags this as the highest-misuse-risk item
in the slate.

## Item 4. Backfill of wave-20260926-0221pdt

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer: the FORK_RESULTS_0221.md file is inherited, produced by the
incomplete 0221pdt wave and left untracked until now. New this wave:
the INCOMPLETE marking, the python3-contact breach disclosure, and the
supersession by the fresh 0521pdt re-run. New versus inherited: the
numbers are the incomplete wave's self-report; the judgment about
their evidentiary status is new.

Attacks:

1. The hardest question: can the 0221pdt battery results be backfilled
as evidence at all? The skeptic's answer: no. A python3 heredoc patched
the wave's driver text. The driver is the control surface of the entire
battery; a tainted driver taints the run's integrity claims even if the
worker attests the battery steps themselves were shell. The 0221pdt
numbers (35 entries, 33 PASS, 2 extraction FAILs) may be reported as
the wave's self-report for audit-trail completeness, but they carry
zero evidentiary weight: no coverage claim, no transit premise, no
lineage, no "0221pdt-tested" citation may rest on them.

2. Classification: breach versus disclosed contact. The COMP-2 precedent
(a python3 -c that read/wrote no file and contacted no artifact) was a
disclosed contact, not a breach. Here the heredoc wrote a wave
artifact. The pure-Zag rule's letter is absolute and names wave
artifacts among its protected surfaces. The skeptic supports the
coordinator's classification as a red-line breach disclosure against
that wave's driver evidence. The distinction from void-on-sight
matters: void-on-sight applies to preregs that pre-authorize Python
tooling; this was unapproved, self-disclosed, and not repeated. The
proportionate remedy is the one already executed: a fresh zero-Python
re-run that supersedes, not an erasure of the audit trail.

3. INCOMPLETE must mean incomplete. The wave had no debate and no
LOOP_STATE.md update. Committing its results file now is evidence
preservation, not certification. The backfill section must not carry a
verdict tag, because no verdict was rendered by a debate for that
wave. Any future reader must be able to tell at a glance that the
0221pdt battery numbers are superseded self-report, not certified
evidence.

4. The skeptic notes one residual risk: the transit wording in the
0521pdt results file cites "0221pdt-tested" premises (see item 1,
attack 3). The backfill ruling must explicitly sever that citation so
the transit claims rest on this wave's own ancestry evidence alone.

## Item 5. Documentation

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer: the README and AUTHORITY_MANIFEST.md edits are new, made by a
concurrent worker during the 0521pdt run and currently uncommitted. The
frozen shas they describe are inherited and unchanged. New versus
inherited: the prose is new; every frozen byte it documents is
inherited.

Attacks:

1. The skeptic's only real probe: do these edits touch the authority
path's frozen content? The README's "no residuals remain" fix removes
a stale note; the manifest's attribution correction (bf69a6f38 for the
kb.txt/gaz.txt addition) fixes a record-keeping nit where the shas
were correct either way. The four frozen chain inputs are untouched.
The skeptic accepts the maintenance classification.

2. The skeptic notes the edits are uncommitted and were made by a
concurrent worker during the fork run (mtimes 05:28 and 05:36 PDT,
attested in the fork results). That is a coordination fact, not a
finding against the edits. Recording them as maintenance keeps them
visible without pretending a debate certified them.

3. No verdict tag applies. If a future wave ever cites these docs as
evidence of anything beyond their shas, that citation would need its
own debate. The skeptic insists the "not a verdict" marking travel
with the record.
