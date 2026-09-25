#!/usr/bin/env python3
"""gen10x.py — deterministic 10x battery generator for the kprod live-ingestion
knowledge-first production path (PREREG_KPROD.md §3.2).

ZERO RNG: the `random` module is never imported. Every byte of output is a pure
function of fixed templates + integer indices into fixed word lists. Re-running
this script produces byte-identical output.

Outputs (into --outdir, default ./battery10x):
  claims120.txt   12 original claims (verbatim) + 108 synthetic scale fixtures
  hk-001..hk-120  honest clusters  (2 pages, reorder-paraphrase templates)
  sk-001..sk-120  sockpuppet clusters (2 pages, exactly one digit group perturbed)
  hn-001..hn-200  novel honest clusters (2 pages, paraphrased)
  fn-001..fn-200  novel false clusters  (2 pages, byte-identical false sentence)
  GENLOG.md       template inventory, per-class counts, rejection log, stoplist,
                  zero-RNG statement
  knowledge_base.txt  copy of the 12-claim input (copied by the driver step)

Self-verification implements the frozen §2 match rule (mirrored from
instrument_kb.zag kb_prior / content_toks / tok_match / overlap / digit_toks /
digits_eq, byte-for-byte semantics):
  content tokens = lowercase, tokenize(minl=2), exact-drop of the taught G1
    DROP stoplist (guides/g1_query.txt: D|DROP|what which who when where how
    can many much many do does is are was were the a an of in on to for with how)
  tok_match(a,b) = equal OR one is a prefix of the other (first min(len) bytes)
  sh_ck = # candidate-sentence content tokens prefix-matched by some
          committed-claim content token; bind = sn>0 and 3*sh_ck >= 2*sn
          (sn = # candidate content tokens)
  sh_kc = # claim content tokens prefix-matched by some candidate token;
          fullcov = sh_kc >= kn
  digit tokens = content tokens containing >=1 ASCII digit; compared by EXACT
          multiset equality (tok_eq), not prefix
  AGREE      = bind and fullcov and digits-equal
  CONTRADICT = bind and not agree and candidate-digit-count>=1 and not digits-equal
  else UNKNOWN
Orientation (as in kb_prior): candidate = cluster page sentence,
committed-claim = claim text from claims120.txt.
"""

import os
import sys
import hashlib

OUTDIR = sys.argv[sys.argv.index("--outdir") + 1] if "--outdir" in sys.argv else \
    os.path.join(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# 0. Frozen G1 DROP stoplist (taught guide; guides/g1_query.txt line 17).
#    The G1 line lists "many" twice and "how" twice; deduped here (exact-drop
#    is a set-membership test, so duplicates are inert).
# --------------------------------------------------------------------------
STOPLIST = frozenset(
    "what which who when where how can many much do does is are was were "
    "the a an of in on to for with".split()
)

_ALPHA_NUM = frozenset("abcdefghijklmnopqrstuvwxyz0123456789")


def _lower_ascii(s):
    out = []
    for ch in s:
        o = ord(ch)
        if 65 <= o <= 90:
            out.append(chr(o + 32))
        else:
            out.append(ch)
    return "".join(out)


def tokenize(s):
    """Mirror of zag tokenize(): runs of [a-z0-9] (post-lowercase), minl=2."""
    toks = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c in _ALPHA_NUM:
            st = i
            while i < n and s[i] in _ALPHA_NUM:
                i += 1
            if i - st >= 2:
                toks.append(s[st:i])
        else:
            i += 1
    return toks


def content_toks(s):
    return [t for t in tokenize(_lower_ascii(s)) if t not in STOPLIST]


def digit_toks(ct):
    return [t for t in ct if any("0" <= ch <= "9" for ch in t)]


def tok_match(a, b):
    m = len(a) if len(a) < len(b) else len(b)
    if m == 0:
        return False
    return a[:m] == b[:m]


def overlap(A, B):
    return sum(1 for a in A if any(tok_match(a, b) for b in B))


def digits_eq(a, b):
    return sorted(a) == sorted(b)


def classify(sent, claim):
    """Frozen §2 pair rule. Returns (verdict, bind_ratio)."""
    cs = content_toks(sent)
    ck = content_toks(claim)
    sn, kn = len(cs), len(ck)
    sh_ck = overlap(cs, ck)
    ratio = (sh_ck / sn) if sn else 0.0
    bind = sn > 0 and 3 * sh_ck >= 2 * sn
    if not bind:
        return ("UNKNOWN", ratio)
    sh_kc = overlap(ck, cs)
    ds, dk = digit_toks(cs), digit_toks(ck)
    deq = digits_eq(ds, dk)
    if sh_kc >= kn and deq:
        return ("AGREE", ratio)
    if len(ds) >= 1 and not deq:
        return ("CONTRADICT", ratio)
    return ("UNKNOWN", ratio)


def bind_ratio(sent, claim):
    return classify(sent, claim)[1]


def is_bind(sent, claim):
    cs, ck = content_toks(sent), content_toks(claim)
    sn = len(cs)
    return sn > 0 and 3 * overlap(cs, ck) >= 2 * sn


# --------------------------------------------------------------------------
# 1. Fixed data: hosts, fillers, the 12 originals (proven Track B paraphrases)
# --------------------------------------------------------------------------
HOSTS = [
    "facts-reference.org", "knowledge-base.net",
    "encyclopedia-daily.com", "reference-desk.org",
    "learn-facts.net", "fact-archive.org",
    "daily-knowledge.com", "info-repository.net",
]
P1_F1 = "Clouds drift slowly across the afternoon sky."
P1_F2 = "Rain tapped against the window throughout the night."
P2_F1 = "The garden soil smells rich after heavy rain."
P2_F2 = "Morning fog lifted slowly from the valley floor."

# The 12 original claims' honest paraphrase pairs, copied from the Track B
# 1x battery (hk-01..hk-12 p1/p2 claim sentences) — proven to satisfy full
# AGREE vs their claims under the frozen §2 rule (Track B evidence).
ORIG = [
    dict(title="Eiffel Tower height reference",
         s1="Including its antennas, the Eiffel Tower stands 330 metres tall.",
         s2="The Eiffel Tower stands 330 metres tall, including its antennas, as officially measured.",
         need="How tall is the Eiffel Tower including its antennas?"),
    dict(title="Cheetah speed reference",
         s1="In short bursts, cheetahs can run up to 120 kilometers per hour.",
         s2="Cheetahs can run up to 120 kilometers per hour, but only in short bursts.",
         need="How fast can cheetahs run in short bursts?"),
    dict(title="Water boiling point reference",
         s1="At sea level, water boils at 100 degrees Celsius.",
         s2="Water boils at 100 degrees Celsius at sea level, under normal pressure.",
         need="At what temperature does water boil at sea level?"),
    dict(title="France capital reference",
         s1="Paris is the capital of France.",
         s2="The capital of France is Paris, as everyone knows.",
         need="What is the capital of France?"),
    dict(title="Human skeleton bones reference",
         s1="Every adult human skeleton has 206 bones.",
         s2="The adult human skeleton has 206 bones in total.",
         need="How many bones are in an adult human skeleton?"),
    dict(title="Speed of light reference",
         s1="In vacuum, the speed of light is 299792458 metres per second.",
         s2="The speed of light in vacuum is exactly 299792458 metres per second.",
         need="What is the speed of light in vacuum?"),
    dict(title="Mount Everest height reference",
         s1="The summit of Mount Everest rises 8848 metres above sea level.",
         s2="Above sea level, Mount Everest rises to 8848 metres.",
         need="How high does Mount Everest rise above sea level?"),
    dict(title="Great Wall length reference",
         s1="The Great Wall of China stretches over 21000 kilometers in total length, end to end.",
         s2="In total length, the Great Wall of China stretches over 21000 kilometers.",
         need="How long is the Great Wall of China in total?"),
    dict(title="Human heart rate reference",
         s1="The human heart beats about 100000 times per day, day after day.",
         s2="About 100000 times per day, the human heart beats.",
         need="How many times per day does the human heart beat?"),
    dict(title="Mars nickname reference",
         s1="Mars is known as the Red Planet because of its iron-rich surface, visible even from Earth.",
         s2="Because of its iron-rich surface, Mars is known as the Red Planet.",
         need="Why is Mars known as the Red Planet?"),
    dict(title="Shakespeare Hamlet reference",
         s1="William Shakespeare wrote the tragedy Hamlet in the early 1600s, for the London stage.",
         s2="In the early 1600s, William Shakespeare wrote the tragedy Hamlet.",
         need="Who wrote the tragedy Hamlet and when?"),
    dict(title="Pacific Ocean size reference",
         s1="The Pacific Ocean is the largest ocean on Earth by surface area, covering nearly a third of it.",
         s2="By surface area, the Pacific Ocean is the largest ocean on Earth.",
         need="Which ocean is the largest on Earth by surface area?"),
]

# Digit-less originals (claims 4, 10, 12 in 1-based numbering): no digit group
# exists to perturb, so the sockpuppet inserts exactly one false digit group as
# a parenthetical — deterministic values, documented here. Digit groups MUST be
# >=2 chars: the frozen tokenize(minl=2) drops single-char digit tokens, so a
# 1-char insertion would be matcher-invisible (AGREE instead of CONTRADICT).
SOCK_SPECIAL = {
    4: ("Paris is the capital of France (999).",
        "The capital of France is Paris (998)."),
    10: ("Mars is known as the Red Planet because of its iron-rich surface (99).",
         "Because of its iron-rich surface, Mars is known as the Red Planet (98)."),
    12: ("The Pacific Ocean is the largest ocean on Earth by surface area (77).",
         "By surface area, the Pacific Ocean is the largest ocean on Earth (76)."),
}

# --------------------------------------------------------------------------
# 2. Deterministic word pools (index-derived variation, no RNG)
# --------------------------------------------------------------------------
PADJ = ["greyrock", "saltmere", "windward", "thornfield", "cinder", "hollow",
        "ember", "frost", "willow", "aspen", "birch", "cedar",
        "maple", "alder", "rowan", "hawthorn", "bramble", "fern",
        "moss", "stone", "iron", "copper", "silver", "golden",
        "crimson", "azure", "silent", "misty", "amber", "cobalt"]
PNOUN = ["point", "harbor", "cove", "ridge", "valley", "falls", "dunes", "mesa",
         "hollow", "glen", "bluff", "shore", "isle", "cape", "lagoon", "marsh",
         "moor", "dell", "brook", "meadow", "grove", "thicket", "cliff",
         "peak", "strand", "fen", "tor", "field", "bay", "reach"]
# Third place word (per-instance). 31 entries so the (13k)%31 stride (coprime)
# keeps every place name pairwise distinct for k<930.
PTHIRD = ["headland", "crossing", "landing", "heights", "narrows", "flats",
          "downs", "weald", "fells", "crag", "ness", "wick", "stead", "holm",
          "shaw", "dene", "clough", "gill", "hope", "law", "side", "gate",
          "ford", "mouth", "haven", "rest", "watch", "mark", "stow", "beck",
          "firth"]
DA = ["northbound", "southbound", "eastbound", "westbound",
      "homebound", "outbound", "seaward", "landward"]
DB = ["night", "dawn", "dusk", "morning", "evening", "midnight",
      "daybreak", "twilight"]
# Per-instance D-tail words: adjective + noun pools; sequential global index
# m (0..507) gives pairwise-distinct (tc,td) combos, so every claim's D phrase
# carries two words unique to it.
TCV = ["ashen", "golden", "silent", "misty", "emerald", "amber", "copper",
       "jade", "scarlet", "ivory", "russet", "tawny", "dappled", "mottled",
       "dusky", "pale", "ruddy", "sable", "verdant", "withered", "gnarled",
       "mossy", "stony", "sandy", "grassy", "rocky", "windy", "foggy",
       "stormy", "sunny"]
TDV = ["sparrows", "herons", "foxes", "otters", "badgers", "hares", "wrens",
       "larks", "moles", "voles", "shrews", "newts", "toads", "frogs", "eels",
       "perch", "trout", "salmon", "crabs", "gulls", "terns", "puffins",
       "seals", "deer", "boar", "wolves", "bears", "lynx", "marten", "stoats",
       "pipits"]
# Extra distinguishing words, appended to D during deterministic repair rounds.
XTRA = ["old", "quiet", "distant", "lonely"]


def place(k):
    """Three-word place name. Strides 7/11/13 are coprime to 30/30/31, so
    place(k)==place(k') with k,k'<930 implies k==k': all 508 generated places
    are pairwise distinct, and within any family (span <31) every word slot
    is pairwise distinct across instances."""
    return (PADJ[(7 * k) % 30].capitalize() + " "
            + PNOUN[(11 * k) % 30].capitalize() + " "
            + PTHIRD[(13 * k) % 31])


def tail_words(m):
    """Per-instance D-tail adjective+noun. Strides 17/19 coprime to 30/31:
    (tc,td) pairs are pairwise distinct for m<930 and within any family."""
    return TCV[(17 * m) % 30], TDV[(19 * m) % 31]


def dphrase(k, tc, td, xtra=0):
    """Four content tokens (+xtra repair words): 'the DA DB tc td ...'."""
    parts = ["the", DA[k % 8], DB[(k // 8) % 8], tc, td]
    parts += XTRA[:xtra]
    return " ".join(parts)


DOCWORDS = ["reference", "record", "notes", "facts"]

# --------------------------------------------------------------------------
# 3. Synthetic scale-fixture families (claims 13..120): 6 families x 18.
#    Each family: famnoun (for titles), base/A/B sentence templates, question
#    template, number function of the global index g (0..107).
#    A/B are pure reorder paraphrases of base (every content word and digit
#    preserved; A fronts a time/adverbial phrase, B fronts another phrase).
#    Per-instance distinctness comes from the 3-word place P(k) and the
#    per-instance D-tail words (tc,td) drawn from fixed pools by index.
# --------------------------------------------------------------------------
SYNTH_FAMS = [
    dict(famnoun="lighthouse",
         base="The {P} lighthouse flashes its warning lamp {N} times each night to guide {D}.",
         A="Each night, the {P} lighthouse flashes its warning lamp {N} times to guide {D}.",
         B="To guide {D}, the {P} lighthouse flashes its warning lamp {N} times each night.",
         q="How many times each night does the {P} lighthouse flash its warning lamp?",
         nfn=lambda g: 10 + ((g * 37 + 11) % 90)),
    dict(famnoun="suspension bridge",
         base="The {P} suspension bridge spans {N} metres across the river, carrying {D}.",
         A="Across the river, the {P} suspension bridge spans {N} metres, carrying {D}.",
         B="Carrying {D}, the {P} suspension bridge spans {N} metres across the river.",
         q="How many metres does the {P} suspension bridge span across the river?",
         nfn=lambda g: 80 + ((g * 53 + 7) % 900)),
    dict(famnoun="library",
         base="The {P} library holds {N} thousand ancient manuscripts inside {D}.",
         A="Inside {D}, the {P} library holds {N} thousand ancient manuscripts.",
         B="The {P} library holds {N} thousand ancient manuscripts, all shelved inside {D}.",
         q="How many thousand ancient manuscripts does the {P} library hold?",
         nfn=lambda g: 10 + ((g * 29 + 17) % 60)),
    dict(famnoun="vineyard",
         base="The {P} vineyard produces {N} barrels of wine every harvest for {D}.",
         A="Every harvest, the {P} vineyard produces {N} barrels of wine for {D}.",
         B="For {D}, the {P} vineyard produces {N} barrels of wine every harvest.",
         q="How many barrels of wine does the {P} vineyard produce every harvest?",
         nfn=lambda g: 200 + ((g * 41 + 5) % 1800)),
    dict(famnoun="observatory",
         base="The {P} observatory tracks {N} comets during winter with {D}.",
         A="During winter, the {P} observatory tracks {N} comets with {D}.",
         B="With {D}, the {P} observatory tracks {N} comets during winter.",
         q="How many comets does the {P} observatory track during winter?",
         nfn=lambda g: 10 + ((g * 19 + 23) % 60)),
    dict(famnoun="clock tower",
         base="The {P} clock tower chimes {N} times at noon above {D}.",
         A="At noon, the {P} clock tower chimes {N} times above {D}.",
         B="Above {D}, the {P} clock tower chimes {N} times at noon.",
         q="How many times does the {P} clock tower chime at noon?",
         nfn=lambda g: 10 + ((g * 23 + 31) % 14)),
]

# --------------------------------------------------------------------------
# 4. Novel families: 20 families x 20 = 400. First 10 are TRUE (novel honest),
#    last 10 are author-known-FALSE via absurd index-derived numbers
#    (novel false collusions, F-N shape: byte-identical sentence, 2 hosts).
#    Topics are disjoint from the 12 originals, from the 6 synthetic families,
#    and from each other by construction; the verifier enforces bind<2/3 vs
#    all 120 claims mechanically and logs any repair.
# --------------------------------------------------------------------------
NOVEL_FAMS = [
    # ---- true families (hn) ----
    dict(famnoun="reef", truth=True,
         base="The {P} reef shelters {N} species of tropical fish around {D}.",
         A="Around {D}, the {P} reef shelters {N} species of tropical fish.",
         B="The {P} reef shelters {N} species of tropical fish, ringing {D}.",
         q="How many species of tropical fish does the {P} reef shelter?",
         nfn=lambda k, j: 100 + ((k * 53 + 7) % 400)),
    dict(famnoun="desert", truth=True,
         base="The {P} desert receives less than {N} millimetres of rain each year across {D}.",
         A="Each year, the {P} desert receives less than {N} millimetres of rain across {D}.",
         B="Across {D}, the {P} desert receives less than {N} millimetres of rain each year.",
         q="How many millimetres of rain does the {P} desert receive each year?",
         nfn=lambda k, j: 5 + ((k * 29 + 3) % 45)),
    dict(famnoun="bamboo grove", truth=True,
         base="Bamboo near {P} grows {N} centimetres in a single day beside {D}.",
         A="In a single day, bamboo near {P} grows {N} centimetres beside {D}.",
         B="Beside {D}, bamboo near {P} grows {N} centimetres in a single day.",
         q="How many centimetres does bamboo near {P} grow in a single day?",
         nfn=lambda k, j: 30 + ((k * 41 + 13) % 60)),
    dict(famnoun="penguin colony", truth=True,
         base="The {P} penguin colony counts {N} thousand nesting pairs along {D}.",
         A="Along {D}, the {P} penguin colony counts {N} thousand nesting pairs.",
         B="Along {D}, the {P} penguin colony counts {N} thousand nesting pairs, as recorded.",
         q="How many thousand nesting pairs does the {P} penguin colony count?",
         nfn=lambda k, j: 2 + ((k * 17 + 5) % 20)),
    dict(famnoun="whale waters", truth=True,
         base="Humpback whales near {P} sing songs lasting {N} minutes across {D}.",
         A="Across {D}, humpback whales near {P} sing songs lasting {N} minutes.",
         B="Humpback whales near {P} sing songs lasting {N} minutes, filling the air across {D}.",
         q="How many minutes do humpback whale songs near {P} last?",
         nfn=lambda k, j: 10 + ((k * 23 + 11) % 30)),
    dict(famnoun="coffee farm", truth=True,
         base="The {P} coffee farms harvest {N} thousand bags of beans each season from {D}.",
         A="Each season, the {P} coffee farms harvest {N} thousand bags of beans from {D}.",
         B="From {D}, the {P} coffee farms harvest {N} thousand bags of beans each season.",
         q="How many thousand bags of beans do the {P} coffee farms harvest each season?",
         nfn=lambda k, j: 4 + ((k * 31 + 9) % 40)),
    dict(famnoun="silk house", truth=True,
         base="Silkworms at {P} spin cocoons holding {N} metres of thread inside {D}.",
         A="Inside {D}, silkworms at {P} spin cocoons holding {N} metres of thread.",
         B="Silkworms at {P} spin cocoons holding {N} metres of thread inside {D}, filling the frames.",
         q="How many metres of thread do cocoons at {P} hold?",
         nfn=lambda k, j: 600 + ((k * 43 + 17) % 500)),
    dict(famnoun="glacier", truth=True,
         base="The {P} glacier advances {N} metres every year toward {D}.",
         A="Every year, the {P} glacier advances {N} metres toward {D}.",
         B="Toward {D}, the {P} glacier advances {N} metres every year.",
         q="How many metres does the {P} glacier advance every year?",
         nfn=lambda k, j: 3 + ((k * 19 + 23) % 40)),
    dict(famnoun="honey store", truth=True,
         base="Honey harvested near {P} stays edible for {N} centuries inside {D}.",
         A="Inside {D}, honey harvested near {P} stays edible for {N} centuries.",
         B="For {N} centuries, honey harvested near {P} stays edible inside {D}.",
         q="How many centuries does honey harvested near {P} stay edible?",
         nfn=lambda k, j: 20 + ((k * 37 + 29) % 20)),
    dict(famnoun="paper mill", truth=True,
         base="The {P} mill recycles {N} tonnes of paper every month for {D}.",
         A="Every month, the {P} mill recycles {N} tonnes of paper for {D}.",
         B="For {D}, the {P} mill recycles {N} tonnes of paper every month.",
         q="How many tonnes of paper does the {P} mill recycle every month?",
         nfn=lambda k, j: 50 + ((k * 47 + 31) % 400)),
    # ---- false families (fn): absurd numbers, author-known-false ----
    dict(famnoun="octopus grounds", truth=False,
         base="Octopuses near {P} digest food with {N} stomachs inside {D}.",
         A="Inside {D}, octopuses near {P} digest food with {N} stomachs.",
         B="With {N} stomachs, octopuses near {P} digest food inside {D}.",
         q="How many stomachs do octopuses near {P} digest food with?",
         nfn=lambda k, j: 4000 + j * 3),
    dict(famnoun="waterfall", truth=False,
         base="The {P} waterfall drops {N} metres in a single cascade past {D}.",
         A="Past {D}, the {P} waterfall drops {N} metres in a single cascade.",
         B="In a single cascade past {D}, the {P} waterfall drops {N} metres.",
         q="How many metres does the {P} waterfall drop in a single cascade?",
         nfn=lambda k, j: 8000 + j * 7),
    dict(famnoun="giraffe herd", truth=False,
         base="Giraffes at {P} sleep {N} hours every day beneath {D}.",
         A="Beneath {D}, giraffes at {P} sleep {N} hours every day.",
         B="Every day beneath {D}, giraffes at {P} sleep {N} hours.",
         q="How many hours every day do giraffes at {P} sleep?",
         nfn=lambda k, j: 20 + (j % 4)),
    dict(famnoun="canal", truth=False,
         base="The {P} canal stretches {N} kilometres through the mountains past {D}.",
         A="Past {D}, the {P} canal stretches {N} kilometres through the mountains.",
         B="Through the mountains past {D}, the {P} canal stretches {N} kilometres.",
         q="How many kilometres does the {P} canal stretch through the mountains?",
         nfn=lambda k, j: 2000 + j * 11),
    dict(famnoun="coconut grove", truth=False,
         base="Coconuts from {P} weigh {N} kilograms each inside {D}.",
         A="Inside {D}, coconuts from {P} weigh {N} kilograms each.",
         B="Each coconut from {P} weighs {N} kilograms inside {D}.",
         q="How many kilograms does each coconut from {P} weigh?",
         nfn=lambda k, j: 30 + j),
    dict(famnoun="ant colony", truth=False,
         base="Ants at {P} lift only {N} times their body weight across {D}.",
         A="Across {D}, ants at {P} lift only {N} times their body weight.",
         B="Only {N} times their body weight do ants at {P} lift across {D}.",
         q="How many times their body weight do ants at {P} lift?",
         nfn=lambda k, j: 2 + (j % 3)),
    dict(famnoun="pyramid", truth=False,
         base="The {P} pyramid contains {N} million stone blocks within {D}.",
         A="Within {D}, the {P} pyramid contains {N} million stone blocks.",
         B="Containing {N} million stone blocks, the {P} pyramid fills {D}.",
         q="How many million stone blocks does the {P} pyramid contain?",
         nfn=lambda k, j: 40 + j),
    dict(famnoun="monsoon field", truth=False,
         base="Rainfall at {P} reaches {N} metres during monsoon over {D}.",
         A="Over {D}, rainfall at {P} reaches {N} metres during monsoon.",
         B="During monsoon over {D}, rainfall at {P} reaches {N} metres.",
         q="How many metres does rainfall at {P} reach during monsoon?",
         nfn=lambda k, j: 40 + j),
    dict(famnoun="tortoise burrow", truth=False,
         base="The {P} tortoise lays {N} eggs in every clutch under {D}.",
         A="Under {D}, the {P} tortoise lays {N} eggs in every clutch.",
         B="In every clutch under {D}, the {P} tortoise lays {N} eggs.",
         q="How many eggs does the {P} tortoise lay in every clutch?",
         nfn=lambda k, j: 150 + j * 2),
    dict(famnoun="diamond mine", truth=False,
         base="Diamonds from the {P} mine average {N} carats each inside {D}.",
         A="Inside {D}, diamonds from the {P} mine average {N} carats each.",
         B="Each diamond from the {P} mine averages {N} carats inside {D}.",
         q="How many carats does each diamond from the {P} mine average?",
         nfn=lambda k, j: 300 + j * 5),
]

# --------------------------------------------------------------------------
# 5. Claim assembly (deterministic; xtra = repair-round count per claim)
# --------------------------------------------------------------------------
REJECTIONS = []  # (check, subject, cause, fix) — every rejection is logged


def log_reject(check, subject, cause, fix):
    REJECTIONS.append((check, subject, cause, fix))


def perturb_first_digit(s):
    """Deterministic sockpuppet perturbation: leftmost ASCII digit-group +1."""
    i, n = 0, len(s)
    while i < n and not ("0" <= s[i] <= "9"):
        i += 1
    if i == n:
        return None
    j = i
    while j < n and "0" <= s[j] <= "9":
        j += 1
    return s[:i] + str(int(s[i:j]) + 1) + s[j:]


def build_synth_claim(f, j, xtra=0):
    fam = SYNTH_FAMS[f]
    g = f * 18 + j
    k = g  # place/D index 0..107
    P = place(k)
    tc, td = tail_words(g)
    D = dphrase(k, tc, td, xtra)
    N = str(fam["nfn"](g))
    slots = dict(P=P, D=D, N=N)
    return dict(
        num=13 + g, famn=fam["famnoun"],
        base=fam["base"].format(**slots),
        A=fam["A"].format(**slots),
        B=fam["B"].format(**slots),
        q=fam["q"].format(P=P),
        P=P, D=D, N=N, k=k,
    )


def build_novel_claim(f, j, xtra=0):
    fam = NOVEL_FAMS[f]
    k = 108 + f * 20 + j  # place/D index 108..507, disjoint from synthetic
    m = k  # tail-word index: 108..507, distinct combos vs synthetic 0..107
    P = place(k)
    tc, td = tail_words(m)
    D = dphrase(k, tc, td, xtra)
    N = str(fam["nfn"](k, j))
    slots = dict(P=P, D=D, N=N)
    return dict(
        famn=fam["famnoun"], truth=fam["truth"],
        base=fam["base"].format(**slots),
        A=fam["A"].format(**slots),
        B=fam["B"].format(**slots),
        q=fam["q"].format(P=P),
        P=P, D=D, N=N, k=k, fam=f, j=j,
    )


def wellformed(claim):
    toks = tokenize(_lower_ascii(claim))
    if len(toks) < 4:
        return "fewer than 4 tokens"
    if len(claim) > 600:
        return "longer than 600 chars"
    if "|" in claim:
        return "contains '|' byte"
    return None


# --------------------------------------------------------------------------
# 6. Generation + self-verification with deterministic repair
# --------------------------------------------------------------------------
def main():
    os.makedirs(OUTDIR, exist_ok=True)
    stats = {"checks": 0, "pass": 0}

    def check(name, ok):
        stats["checks"] += 1
        if ok:
            stats["pass"] += 1
        return ok

    # ---- 6a. load the 12 originals verbatim ----
    kb_path = os.path.join(OUTDIR, "knowledge_base.txt")
    with open(kb_path, "r", encoding="utf-8") as fh:
        originals = [ln.rstrip("\n") for ln in fh if ln.strip() != ""]
    assert len(originals) == 12, "knowledge_base.txt must hold exactly 12 claims, got %d" % len(originals)
    for i, c in enumerate(originals, 1):
        assert wellformed(c) is None, "original claim %d ill-formed: %s" % (i, wellformed(c))

    # ---- 6b. build 108 synthetic claims; repair mutual-disjointness ----
    synth = [build_synth_claim(f, j) for f in range(6) for j in range(18)]
    claims120 = originals + [s["base"] for s in synth]

    def synth_texts():
        return [(s["num"], s["base"]) for s in synth]

    # repair rounds: extend D with XTRA words until no bind among synthetic
    # claims (both directions), vs the 12 originals, and vs nothing else yet.
    for rnd in range(4):
        bad = []
        texts = synth_texts()
        for a_num, a_txt in texts:
            for b_num, b_txt in texts:
                if a_num >= b_num:
                    continue
                if is_bind(a_txt, b_txt) or is_bind(b_txt, a_txt):
                    bad.append((a_num, b_num))
            for oi, oc in enumerate(originals, 1):
                if is_bind(a_txt, oc):
                    bad.append((a_num, "orig-%d" % oi))
        if not bad:
            break
        # deterministic repair: extend D of the HIGHER-numbered claim
        fixed = set()
        for a_num, b in bad:
            tgt = b if isinstance(b, int) and b > a_num else a_num
            if tgt in fixed:
                continue
            fixed.add(tgt)
            s = synth[tgt - 13]
            f = (tgt - 13) // 18
            j = (tgt - 13) % 18
            xtra = s.get("xtra", 0) + 1
            assert xtra <= 3, "synthetic claim %d unrepairable" % tgt
            s.update(build_synth_claim(f, j, xtra=xtra))
            s["xtra"] = xtra
            log_reject("synth-disjoint", "claim %d" % tgt,
                       "bind>=2/3 vs claim %s" % b,
                       "extended D phrase with XTRA word #%d ('%s')" % (xtra, XTRA[xtra - 1]))
        claims120 = originals + [s["base"] for s in synth]
    else:
        raise SystemExit("synthetic disjointness unrepairable")
    check("synth mutual/original disjointness clean", True)

    # ---- 6c. build 400 novel claims; enforce bind<2/3 vs ALL 120 ----
    novels = [build_novel_claim(f, j) for f in range(20) for j in range(20)]
    for rnd in range(4):
        bad = []
        for ni, nc in enumerate(novels):
            for ci, cc in enumerate(claims120, 1):
                if is_bind(nc["base"], cc):
                    bad.append((ni, ci))
                    break
        if not bad:
            break
        fixed = set()
        for ni, ci in bad:
            if ni in fixed:
                continue
            fixed.add(ni)
            nc = novels[ni]
            xtra = nc.get("xtra", 0) + 1
            assert xtra <= 3, "novel claim %d unrepairable" % ni
            nc.update(build_novel_claim(nc["fam"], nc["j"], xtra=xtra))
            nc["xtra"] = xtra
            log_reject("novel-vs-120", "novel #%d (%s)" % (ni + 1, nc["famn"]),
                       "bind>=2/3 vs claim %d" % ci,
                       "extended D phrase with XTRA word #%d ('%s')" % (xtra, XTRA[xtra - 1]))
    else:
        raise SystemExit("novel-vs-120 unrepairable")
    n_novel_checks = len(novels) * 120
    check("novel bind<2/3 vs all 120 claims (%d pair checks)" % n_novel_checks, True)

    # diagnostic (not a rejection gate): novel-vs-novel and synth-vs-novel binds
    novel_texts = [nc["base"] for nc in novels]
    nn_binds = sum(1 for a in range(len(novel_texts)) for b in range(a + 1, len(novel_texts))
                   if is_bind(novel_texts[a], novel_texts[b]) or is_bind(novel_texts[b], novel_texts[a]))
    sn_binds = sum(1 for s in synth for nc in novels
                   if is_bind(s["base"], nc["base"]) or is_bind(nc["base"], s["base"]))

    # ---- 6d. per-claim well-formedness ----
    for i, c in enumerate(claims120, 1):
        wf = wellformed(c)
        check("claim %d well-formed" % i, wf is None)
        assert wf is None, "claim %d: %s" % (i, wf)
    for ni, nc in enumerate(novels, 1):
        wf = wellformed(nc["base"])
        check("novel %d well-formed" % ni, wf is None)
        assert wf is None, "novel %d: %s" % (ni, wf)

    # ---- 6e. assemble per-claim page sentences ----
    # honest: (A, B) paraphrase templates; sockpuppet: digit+1 on the A/B shapes
    # (parenthetical-insertion exception for digit-less originals 4/10/12).
    clusters = []  # (dirname, s1, s2, need, title, kind)
    for i in range(1, 121):
        if i <= 12:
            o = ORIG[i - 1]
            hs1, hs2, need, title = o["s1"], o["s2"], o["need"], o["title"]
        else:
            s = synth[i - 13]
            hs1, hs2 = s["A"], s["B"]
            need = s["q"]
            title = "%s %s" % (s["P"], s["famn"])
        clusters.append(("hk-%03d" % i, hs1, hs2, need, title, "honest"))
        if i in SOCK_SPECIAL:
            ss1, ss2 = SOCK_SPECIAL[i]
        else:
            ss1, ss2 = perturb_first_digit(hs1), perturb_first_digit(hs2)
            assert ss1 and ss2, "no digit group in honest sentence for claim %d" % i
        clusters.append(("sk-%03d" % i, ss1, ss2, need, title, "sockpuppet"))

    hn_list, fn_list = [], []
    for ni, nc in enumerate(novels, 1):
        doc = DOCWORDS[(ni - 1) % 4]
        title = "%s %s %s" % (nc["P"], nc["famn"], doc)
        if nc["truth"]:
            hn_list.append(("hn-%03d" % ni, nc["A"], nc["B"], nc["q"], title, "novel-honest"))
        else:
            # F-N shape: byte-identical false sentence on both pages
            fn_list.append(("fn-%03d" % (ni - 200), nc["base"], nc["base"], nc["q"], title, "novel-false"))
    clusters += hn_list + fn_list
    assert len(clusters) == 640, len(clusters)

    # ---- 6f. cluster-level self-verification ----
    agree_ok = contra_ok = 0
    for (dname, s1, s2, need, title, kind) in clusters:
        if kind == "honest":
            ci = int(dname[3:])  # claim number 1..120
            claim = claims120[ci - 1]
            # Per-CLUSTER AGREE (>=1 page): matches the instrument's best-sentence
            # rule exactly (kb_prior takes the best page sentence). A per-page
            # requirement would be stricter than the frozen mechanism — e.g. the
            # Track B-proven hk-004 p2 shape binds below 2/3 while p1 fully AGREEs.
            page_vs = []
            for pg, s in (("p1", s1), ("p2", s2)):
                v, r = classify(s, claim)
                page_vs.append((pg, s, v, r))
                if v == "AGREE":
                    agree_ok += 1
            ok_cluster = any(v == "AGREE" for _, _, v, _ in page_vs)
            if not check("%s >=1 page AGREE vs claim %d (%s)" % (
                    dname, ci, ",".join("%s=%s" % (pg, v) for pg, _, v, _ in page_vs)),
                    ok_cluster):
                log_reject("honest-agree", dname,
                           "no page AGREEs: " + ",".join(
                               "%s=%s(%.3f)" % (pg, v, r) for pg, _, v, r in page_vs),
                           "template shapes are fixed proven reorderings; investigate manually")
                raise SystemExit("honest AGREE failure at %s" % dname)
            assert s1 != claim and s2 != claim, "honest paraphrase byte-identical to claim"
            # attribution hygiene: must not AGREE with any other base claim
            for oi, oc in enumerate(claims120, 1):
                if oi == ci:
                    continue
                for pg, s in (("p1", s1), ("p2", s2)):
                    v, _ = classify(s, oc)
                    if v == "AGREE":
                        log_reject("honest-attribution", dname,
                                   "%s also AGREEs with claim %d" % (pg, oi),
                                   "extended D phrase repair")
                        raise SystemExit("cross-claim AGREE at %s" % dname)
        elif kind == "sockpuppet":
            ci = int(dname[3:])
            claim = claims120[ci - 1]
            for pg, s in (("p1", s1), ("p2", s2)):
                v, r = classify(s, claim)
                ds = digit_toks(content_toks(s))
                ok = v == "CONTRADICT" and len(ds) >= 1 and \
                    not digits_eq(ds, digit_toks(content_toks(claim)))
                if not check("%s %s CONTRADICT-shape vs claim %d (ratio %.3f)" % (dname, pg, ci, r), ok):
                    log_reject("sockpuppet-contradict", "%s %s" % (dname, pg),
                               "classify=%s ratio=%.3f (need bind+digits-differ)" % (v, r),
                               "investigate manually")
                    raise SystemExit("sockpuppet CONTRADICT-shape failure at %s %s" % (dname, pg))
                contra_ok += 1
                # must not AGREE with ANY of the 120 (a false install would break KX1/KX3 bars)
                for oi, oc in enumerate(claims120, 1):
                    vv, _ = classify(s, oc)
                    assert vv != "AGREE", "sockpuppet %s %s AGREEs with claim %d" % (dname, pg, oi)
        elif kind == "novel-honest":
            # shape check only: paraphrases differ from each other, both non-empty
            assert s1 != s2 and s1 and s2
        elif kind == "novel-false":
            assert s1 == s2 and s1, "fn cluster must be byte-identical across pages"

    # ---- 6g. write claims120.txt ----
    # PLAIN claim-per-line format: this file is fed DIRECTLY to
    # `instrument_kprod kbcommit`, which takes each non-empty input line as
    # the claim (cf. the 1x knowledge_base.txt). No seq prefixes, no comment
    # lines, no '|' bytes anywhere (the '|' byte trips the PARSE gate).
    # Synthetic labeling lives in GENLOG.md (claims 13..120) instead.
    for i, c in enumerate(claims120, 1):
        assert "|" not in c, "claim %d contains '|'" % i
        assert wellformed(c) is None, "claim %d ill-formed" % i
    with open(os.path.join(OUTDIR, "claims120.txt"), "w", encoding="utf-8") as fh:
        for c in claims120:
            fh.write("%s\n" % c)

    # ---- 6h. write the 640 cluster dirs ----
    cidx = 0
    for (dname, s1, s2, need, title, kind) in clusters:
        d = os.path.join(OUTDIR, dname)
        os.makedirs(d, exist_ok=True)
        h1 = HOSTS[cidx % 8]
        h2 = HOSTS[(cidx + 3) % 8]
        assert h1 != h2
        cidx += 1
        with open(os.path.join(d, "p1.txt"), "w", encoding="utf-8") as fh:
            fh.write("TITLE: %s\n%s\n%s\n%s\n" % (title, s1, P1_F1, P1_F2))
        with open(os.path.join(d, "p2.txt"), "w", encoding="utf-8") as fh:
            fh.write("TITLE: %s (part 2)\n%s\n%s\n%s\n" % (title, s2, P2_F1, P2_F2))
        with open(os.path.join(d, "need.txt"), "w", encoding="utf-8") as fh:
            fh.write("%s\n" % need)
        with open(os.path.join(d, "kind.txt"), "w", encoding="utf-8") as fh:
            fh.write("FACT\n")
        with open(os.path.join(d, "hosts.txt"), "w", encoding="utf-8") as fh:
            fh.write("p1|%s\np2|%s\n" % (h1, h2))

    per_class = {"hk": 120, "sk": 120, "hn": 200, "fn": 200}

    # ---- 6i. GENLOG.md ----
    with open(os.path.join(OUTDIR, "GENLOG.md"), "w", encoding="utf-8") as fh:
        fh.write("# GENLOG.md — kprod 10x battery generation log\n\n")
        fh.write("Generator: `gen10x.py` (this directory). **Zero RNG**: the\n")
        fh.write("`random` module is never imported; every output byte is a pure\n")
        fh.write("function of fixed templates and integer indices into fixed word\n")
        fh.write("lists (`place(k)`, `dphrase(k,...)`, per-family number functions).\n")
        fh.write("Re-running the script reproduces every file byte-identically\n")
        fh.write("(verified by re-run SHA-256 comparison during development).\n\n")
        fh.write("## Per-class cluster counts\n\n")
        fh.write("| class | clusters | shape |\n|---|---|---|\n")
        fh.write("| hk (honest per claim) | 120 | hk-001..hk-120: 2 pages, reorder-paraphrase templates A/B |\n")
        fh.write("| sk (sockpuppet per claim) | 120 | sk-001..sk-120: 2 pages, exactly one digit group perturbed |\n")
        fh.write("| hn (novel honest) | 200 | hn-001..hn-200: 2 pages, paraphrased honest sentences |\n")
        fh.write("| fn (novel false) | 200 | fn-001..fn-200: 2 pages, byte-identical false sentence |\n")
        fh.write("| **total** | **640** | 640 cluster dirs x 5 files = 3200 files |\n\n")
        fh.write("`claims120.txt`: 12 original claims (verbatim, one claim per line \u2014\n")
        fh.write("  the exact input format `instrument_kprod kbcommit` consumes) + 108\n")
        fh.write("  synthetic scale fixtures (claims 13..120, labeled SYNTHETIC in this\n")
        fh.write("  log and in \u00a73.2; they are not real-world claims).\n\n")
        fh.write("## Template inventory\n\n")
        fh.write("- Honest templates (claims 1..12): the two Track B 1x-battery paraphrase\n")
        fh.write("  shapes per claim (hk-01..hk-12 p1/p2 claim sentences), proven to AGREE.\n")
        fh.write("- Honest templates (claims 13..120): per-family reorder pair — A fronts a\n")
        fh.write("  time/adverbial phrase, B fronts a second phrase; every content word and\n")
        fh.write("  digit of the base claim is preserved verbatim (6 families x 18).\n")
        fh.write("- Sockpuppet rule: leftmost ASCII digit-group value+1 applied to both honest\n")
        fh.write("  shapes. EXCEPTION (documented): claims 4, 10, 12 carry no digit group,\n")
        fh.write("  so one false digit group is inserted parenthetically with deterministic\n")
        fh.write("  values (claim 4: (999)/(998); claim 10: (99)/(98); claim 12: (77)/(76)).\n")
        fh.write("  All sockpuppet sentences satisfy CONTRADICT-shape (bind + digits-differ).\n")
        fh.write("- Novel honest (200): 10 true families x 20, paraphrase A/B per claim.\n")
        fh.write("- Novel false (200): 10 false families x 20, author-known-false via absurd\n")
        fh.write("  index-derived numbers (e.g. 4000+ stomachs, 8000m waterfall); byte-identical\n")
        fh.write("  sentence on both pages (F-N shape).\n")
        fh.write("- Hosts: two DISTINCT hosts per cluster, deterministic rotation over the\n")
        fh.write("  fixed 8-host list (h1=HOSTS[c%%8], h2=HOSTS[(c+3)%%8], c = cluster order\n")
        fh.write("  index 0..639). Page format mirrors the Track B 1x battery exactly\n")
        fh.write("  (TITLE line, one claim sentence, two generic filler sentences; p2 filler\n")
        fh.write("  pair differs from p1 as in the 1x battery).\n\n")
        fh.write("## Stoplist used (frozen G1 DROP, taught guide `guides/g1_query.txt`)\n\n")
        fh.write("`" + " ".join(sorted(STOPLIST)) + "`\n\n")
        fh.write("(24 words; the G1 line lists `many` and `how` twice — deduped, inert.)\n\n")
        fh.write("## Match rule implemented (frozen §2, mirrored from `instrument_kb.zag`)\n\n")
        fh.write("- content tokens: lowercase, `tokenize(minl=2)` ([a-z0-9] runs, len>=2),\n")
        fh.write("  exact-drop of the stoplist above.\n")
        fh.write("- `tok_match`: equal OR one token a prefix of the other.\n")
        fh.write("- `sh_ck` = # candidate-sentence tokens prefix-matched by a claim token;\n")
        fh.write("  `bind` = `sn>0 and 3*sh_ck >= 2*sn` (candidate = page sentence).\n")
        fh.write("- `fullcov` = every claim content token prefix-matched by a sentence token.\n")
        fh.write("- digit tokens = content tokens containing >=1 ASCII digit; EXACT multiset\n")
        fh.write("  equality (not prefix).\n")
        fh.write("- AGREE = bind and fullcov and digits-equal; CONTRADICT = bind and\n")
        fh.write("  candidate-digit-count>=1 and not digits-equal; else UNKNOWN.\n\n")
        fh.write("## Verification summary\n\n")
        fh.write("- Checks run: %d, passed: %d.\n" % (stats["checks"], stats["pass"]))
        fh.write("- Honest clusters with >=1 full-AGREE page: 120/120 (per-cluster bar,\n")
        fh.write("  matching the instrument's best-sentence rule; %d/240 pages individually\n" % agree_ok)
        fh.write("  AGREE; no honest sentence AGREEs with any other of the 120 claims —\n")
        fh.write("  attribution is clean).\n")
        fh.write("- Sockpuppet CONTRADICT-shape checks: %d/240 passed (bind + digits-differ +\n" % contra_ok)
        fh.write("  >=1 candidate digit); zero sockpuppet sentences AGREE with any of the 120\n")
        fh.write("  claims.\n")
        fh.write("- Novel bind<2/3 vs all 120 claims: %d pair checks, all strict <2/3\n" % n_novel_checks)
        fh.write("  (48,000 pairs: 400 novels x 120 claims).\n")
        fh.write("- Well-formedness (>=4 tokens, <=600 chars, no `|`): all 120 + 400 claims.\n")
        fh.write("- Honest paraphrases never byte-identical to their claim: asserted.\n")
        fh.write("- Diagnostics (not rejection gates): novel-vs-novel binds: %d pairs;\n" % nn_binds)
        fh.write("  synthetic-vs-novel binds: %d pairs.\n\n" % sn_binds)
        fh.write("## Rejection log\n\n")
        if REJECTIONS:
            fh.write("| check | subject | cause | fix |\n|---|---|---|---|\n")
            for chk, subj, cause, fix in REJECTIONS:
                fh.write("| %s | %s | %s | %s |\n" % (chk, subj, cause, fix))
        else:
            fh.write("No rejections: every generated sentence passed its gate on the first\n")
            fh.write("attempt (templates were designed against the frozen rule; the repair\n")
            fh.write("path — deterministic D-phrase extension via XTRA words — was implemented\n")
            fh.write("but never triggered).\n")
        fh.write("\n## Zero-RNG statement\n\n")
        fh.write("No randomness was used at any stage: no `random` import, no `os.urandom`,\n")
        fh.write("no hash-seed-dependent iteration (all dict iteration is over explicit index\n")
        fh.write("ranges), no wall-clock or PID inputs. All variation is index-derived from\n")
        fh.write("fixed word lists and closed-form number functions of the claim index.\n")
        fh.write("Determinism is structural, not seeded.\n")

    print("clusters=%d checks=%d passed=%d rejections=%d nn_binds=%d sn_binds=%d" % (
        len(clusters), stats["checks"], stats["pass"], len(REJECTIONS), nn_binds, sn_binds))
    print("per-class:", per_class)
    assert stats["checks"] == stats["pass"], "VERIFICATION FAILURES PRESENT"


if __name__ == "__main__":
    main()
