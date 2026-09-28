#!/usr/bin/env python3
"""Build round-3 verdict-level TSV from curated differential items."""
import sys
sys.path.insert(0, "/tmp/r3")
from ou_ref import annotate

SCAF = "prove france capital today; france capital france capital france capital; "

items = [
 # id, trailing clause, expected, rationale
 ("r3s01", "she told me the answer; no, i meant the other one?", "19",
  "Sentence break (;) resets R3 reported scope per S2; second sentence operative self-correction; v4 behavior expected."),
 ("r3s02", "she told me the answer. no, i meant the other one?", "19",
  "Sentence break (.) resets reported scope; operative; v4 behavior expected."),
 ("r3s03", "she told me the answer\nno, i meant the other one?", "19",
  "Newline is a clause boundary but NOT a sentence boundary per S2 (split on ?.!; only); reported scope persists -> non-operative; v4 behavior expected."),
 ("r3s04", "i never lied; i meant moby dick?", "19",
  "Negation is clause-local (R2/R5); neg in clause 1 must not leak into clause 2; operative i-meant; v4 behavior expected."),
 ("r3s05", "maybe she left; i meant moby dick?", "19",
  "Hedge is clause-local (R2/R6); hedge in clause 1 must not leak; operative; v4 behavior expected."),
 ("r3s06", "no; i meant moby dick?", "19",
  "Bare no alone in clause 1 has no O-pattern (st=7); clause-2 i-meant operative; v4 behavior expected."),
 ("r3b01", "\"if\" i meant moby dick?", "19",
  "Cond word quoted but trigger not; R4 has no quote carveout per S2 -> hypothetical; v4 behavior expected."),
 ("r3b02", "\"maybe\" i meant moby dick?", "19",
  "Quoted hedge still hedges per S2 (no quote carveout in R6); v4 behavior expected."),
 ("r3b03", "maybe i never meant moby dick?", "19",
  "Stacked hedge+negation; R5 fires (order R3->R4->R5); negated; v4 behavior expected."),
 ("r3b04", "she said maybe i meant moby dick?", "19",
  "Stacked reported+hedged; R3 fires first; reported; v4 behavior expected."),
 ("r3m01", "no, i meant moby dick; actually, we meant the whaling tale?", "16",
  "Two independent operative triggers; protection engages as designed; correction bid expected."),
 ("r3m02", "\"no, i meant moby dick\", no, i meant pride and prejudice?", "16",
  "First trigger quoted (st=2), second operative (st=1); annotations independent; protection engages on the second."),
 ("r3m03", "she told me no, i meant moby dick; no, i meant pride and prejudice?", "16",
  "Reported first clause (st=3), operative second clause (st=1); sentence break resets R3; protection engages on second."),
 ("r3m04", "no, i meant moby dick; she told me no, i meant pride and prejudice?", "16",
  "Operative first clause, reported second; protection engages on the first."),
 ("r3o01", "my correction, moby dick?", "16",
  "O4 label use: article + comma -> operative; correction bid expected."),
 ("r3o02", "a correction; moby dick?", "16",
  "O4: article + clause-final (semicolon ends clause) -> operative; correction bid expected."),
 ("r3o03", "this correction?", "16",
  "O4: article + last token of clause -> operative per S2 reading 2 (battery note)."),
 ("r3o04", "your correction?", "19",
  "O4: non-article prev + last token -> non-operative per S2 reading 2; v4 behavior expected."),
 ("r3o05", "a correction moby dick?", "19",
  "O4: article but byte after is space and not last token -> attributive-ish; non-operative; v4 behavior expected."),
 ("r3o06", "do you know the correction?", "19",
  "S2-DESIGN GAP probe: article + clause-final -> code+spec say operative (st=1), but a human reads it as a question about a correction, not a performed correction. Expect v6=16 flip if protection engages."),
 ("r3r01", "the friend of the author said no, i meant moby dick?", "16",
  "'author' not in S2 third-person list and 'friend' 4 tokens before verb -> not reported per S2; meant operative (O3); correction bid expected."),
 ("r3r02", "no, i meant moby dick, the author said?", "16",
  "S2-DESIGN GAP probe: speech verb AFTER trigger is outside R3 scope (before-trigger only); code+spec say operative. Expect v6=16."),
 ("r3r03", "the author said that no, i meant moby dick?", "16",
  "S2-DESIGN GAP probe: 'author' not in frozen third-person subject list -> not reported per S2; operative. Expect v6=16."),
 ("r3n01", "oh no, i meant moby dick?", "16",
  "R5 no-exception: 'no' followed by i -> discourse, never negator; O1 with particle 'oh'; operative."),
 ("r3n02", "not no, i meant moby dick?", "19",
  "'not' before the no/meant clause... check: clause tokens [not,no,i,meant,moby,dick]; meant: 'not' at ti-3 -> negated st=5; no: O1? tokens before=[not] not particle -> st=7. Non-operative; v4 behavior expected."),
 ("r3h01", "i could have meant moby dick?", "19",
  "Hedged (could) per R6; v4 behavior expected."),
 ("r3q01", "don't no, i meant moby dick?", "16",
  "Apostrophe guard: n't contraction does not toggle quotes; no operative via O1."),
 ("r3q02", "''no, i meant moby dick?''", "16",
  "Double single-quote toggles twice -> trigger unquoted; O1 operative."),
 ("r3f01", "correction?", "16",
  "Lone clause-initial 'correction' -> O4 operative (st=1); evidence fires with empty topic."),
 ("r3f02", "no?", "19",
  "Lone 'no' -> no O-pattern (st=7); v4 behavior expected."),
]

rows = ["id\tquery\texpected_bid\treadings\trationale"]
for iid, clause, exp, rat in items:
    q = SCAF + clause
    sts, toks = annotate(q)
    trig = [(t, s) for t, s in zip(toks, sts) if s != 0]
    rows.append(f"{iid}\t{q}\t{exp}\t2/0\t{rat} [probe: {trig}]")

with open("/tmp/r3/r3_items.tsv", "w") as f:
    f.write("\n".join(rows) + "\n")
print(f"wrote {len(items)} items")
for iid, clause, exp, rat in items:
    sts, toks = annotate(SCAF + clause)
    trig = [(t, s) for t, s in zip(toks, sts) if s != 0]
    print(iid, "->", trig)
