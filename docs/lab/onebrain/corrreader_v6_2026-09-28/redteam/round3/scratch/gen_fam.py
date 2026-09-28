#!/usr/bin/env python3
"""Round-3 fuzz families: NEW bug classes (scope/reset, blocker interaction,
multi-trigger, O4 punctuation, R1 guard edges, R5 no-exceptions)."""
import itertools, random

Q = []
def add(q): Q.append(q)

# ---------- F1: scope / reset ----------
# R3 verb before/after sentence boundaries
for sep, name in [(";", "semi"), (".", "period"), ("?", "qmark"), ("!", "bang")]:
    add(f"she told me the answer{sep} no, i meant the other one?")
    add(f"my friend said hello{sep} actually, we meant goodbye?")
    add(f"the teacher thinks paris{sep} correction: lyon?")
# newline: clause boundary but NOT sentence boundary per S2
add("she told me the answer\nno, i meant the other one?")
add("my friend said hello\nactually, we meant goodbye?")
add("if i agree\nno, i meant moby dick?")
# R4 cond across boundaries
for sep in [";", ".", "?", "!"]:
    add(f"unless it rains{sep} i meant moby dick?")
    add(f"i meant moby dick{sep} unless it rains?")
add("unless it rains\ni meant moby dick?")
# comma does NOT reset sentence scope (reported spans commas)
add("she told me, after a long pause, no, i meant moby dick?")
add("if, after all, i meant moby dick, forgive me?")
# clause-local rules must NOT leak across clause boundaries
add("i never lied; i meant moby dick?")      # neg in clause 1, trigger in clause 2
add("maybe she left; i meant moby dick?")    # hedge in clause 1
add("i never lied. i meant moby dick?")
add("perhaps he left! i meant moby dick?")
add("i never lied? i meant moby dick?")
add("i never lied\ni meant moby dick?")      # newline IS clause boundary
# O-patterns must not leak across clauses either
add("no; i meant moby dick?")                # no alone in clause 1 -> st7; meant clause 2
add("well; no, i meant moby dick?")

# ---------- F2: blocker interaction ----------
add('"if" i meant moby dick?')               # quoted cond, unquoted trigger
add('"maybe" i meant moby dick?')            # quoted hedge
add('"she told me" no, i meant moby dick?')  # quoted verb phrase
add("'unless' i meant moby dick?")
add("maybe i never meant moby dick?")        # hedge + negated (R5 wins order)
add("if i never meant moby dick?")           # cond + negated (R4 first)
add("she said maybe i meant moby dick?")     # reported + hedged (R3 first)
add("she said i never meant moby dick?")     # reported + negated
add("if she said i meant moby dick?")        # cond + reported
add('"no," she said, "i meant moby dick"?') # quoted trigger + reported verb
add("i said \"no, i meant moby dick\" loudly?")  # first-person + quoted trigger

# ---------- F3: multi-trigger ----------
add("no, i meant moby dick; actually, we meant the whaling tale?")
add("correction: moby dick; no, i meant pride and prejudice?")
add('"no, i meant moby dick", no, i meant pride and prejudice?')
add("she told me no, i meant moby dick; no, i meant pride and prejudice?")
add("no, i meant moby dick; she told me no, i meant pride and prejudice?")
add("maybe i meant moby dick; no, i meant pride and prejudice?")
add("no, i meant moby dick; maybe i meant pride and prejudice?")
add("correction: first; correction: second?")
add("i meant moby dick and she meant the whaling tale?")
add("no no, i meant moby dick?")
add("no, no, i meant moby dick?")

# ---------- F4: O4 punctuation / edges ----------
add("the correction: moby dick?")
add("my correction, moby dick?")
add("a correction; moby dick?")
add("this correction?")
add("that correction?")
add("your correction?")
add("our correction?")
add("the correction?")
add("a correction ?")
add("correction : moby dick?")
add("a correction : moby dick?")
add("the correction, moby dick, is noted?")
add("correction moby dick?")
add("a correction moby dick?")
add("pre-correction: moby dick?")
add("correction!?")
add("the final correction?")
add("his correction: moby dick?")
add("the correction. moby dick?")

# ---------- F5: R1 apostrophe-guard edges ----------
add("don't no, i meant moby dick?")
add("teachers' no, i meant moby dick?")
add("teachers no, i meant moby dick?")
add("'no, i meant moby dick?")
add("no, i meant moby dick'?")
add("''no, i meant moby dick?''")
add("'tis no, i meant moby dick?")
add("rock 'n' roll; no, i meant moby dick?")
add("it''s no, i meant moby dick?")
add("say 'no', i meant moby dick?")

# ---------- F6: R5 no-exceptions ----------
add("no, i meant moby dick?")
add("oh no, i meant moby dick?")
add("no no, i meant moby dick?")
add("i said no, i meant moby dick?")
add("i said no, we meant moby dick?")
add("there is no way i meant moby dick?")
add("no way i meant moby dick?")
add("no money, i meant moby dick?")
add("no, no way i meant moby dick?")
add("i do not think no, i meant moby dick?")
add("not no, i meant moby dick?")
add("never no, i meant moby dick?")

# ---------- F7: discourse particles ----------
for p in ["well","oh","uh","um","ah","okay","ok","right","so"]:
    add(f"{p}, no, i meant moby dick?")
    add(f"{p} no, i meant moby dick?")
for p in ["hmm","er","hey","wow","oops","like","actually"]:
    add(f"{p}, no, i meant moby dick?")
add("right no, i meant moby dick?")
add("so no, i meant moby dick?")
add("well oh uh, no, i meant moby dick?")

# ---------- F8: R3 subject/verb edges ----------
add("my very good friend said no, i meant moby dick?")  # friend 4 before said
add("my good friend said no, i meant moby dick?")        # friend 3 before said
add("friend said no, i meant moby dick?")                # friend 1 before
add("said no, i meant moby dick?")                       # no subject
add("the man she told me said no, i meant moby dick?")
add("i told my friend no, i meant moby dick?")           # verb after i; friend after verb
add("we said no, we meant moby dick?")
add("you said no, i meant moby dick?")
add("according to my friend i meant moby dick?")         # no comma
add("according even to my friend i meant moby dick?")
add("according to my friend. i meant moby dick?")        # sentence break
add("i meant moby dick according to my friend?")          # according AFTER (gap)

# ---------- F9: R6 edges ----------
add("i think i meant moby dick?")
add("we think we meant moby dick?")
add("i guess i meant moby dick?")
add("i believe i meant moby dick?")
add("i suppose i meant moby dick?")
add("think i meant moby dick?")
add("i think; i meant moby dick?")
add("maybe, i meant moby dick?")
add("i meant moby dick, maybe?")
add("could i have meant moby dick?")
add("i could have meant moby dick?")

# ---------- F10: misc tokenizer edges ----------
add("NO, I MEANT MOBY DICK?")
add("No, I Meant Moby Dick?")
add("no,i meant moby dick?")
add("no ,i meant moby dick?")
add("no   i   meant   moby dick?")
add("no\ti meant moby dick?")
add("no- i meant moby dick?")
add("no42 i meant moby dick?")
add("(no, i meant moby dick?)")
add("[no, i meant moby dick?]")
add("...no, i meant moby dick?")
add("no, i meant moby-dick?")
add("i meant 42?")

with open("/tmp/r3/fuzz_fam.txt", "w") as f:
    for q in Q:
        f.write(q + "\n")
print(f"wrote {len(Q)} family queries")
