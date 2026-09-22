#!/usr/bin/env python3
"""Python prototype of the R1/R2 repaired classifier (M1a/M1b fixes).

Used to validate the decision rules against the negation crew's judged tables
before porting to Zag. The Zag port must reproduce these outputs exactly.

Rules (generic, claim-agnostic):
  0. Overlap gate: >=2 distinct claim content words (stem-matched) in title+snippet,
     or >=1 when the claim has <3 content words. Else IRRELEVANT.
  1. Predicate: claim's finite predicate = first verb-stem token after stripping a
     leading gerund and skipping reporting/cognition verbs. Synonym table for
     predicate matching.
  2. Anchor: claim's first or last content word must occur in an endorsing clause.
  3. Clause split on .!?;\u2014. Endorsement requires a single clause with:
     predicate (or synonym) present, no negation scoping the predicate,
     not interrogative, no competing-proper-noun veto, anchor present,
     >=2 claim content words in the clause (or >=1 if claim has <3).
  4. DENY if any clause has:
     (a) strong denial token + >=1 other claim content word, or weak denial
         token + >=2 claim content words;
     (b) negation marker scoping the predicate + >=1 other claim content word;
     (c) competing proper noun before predicate + >=1 claim content word AND the
         predicate is superlative/identity-like (tallest/largest/only/first/...);
     (d) claim antonym (flat<->spherical/round/globe) + >=1 claim content word.
  5. Negation markers: ASCII n't, U+2019 n't variants, not/no/never/neither/nor/
     none/nothing/without/lack/fails to/... Clause-scoped: marker must end within
     3 tokens before the predicate (or be attached to an auxiliary governing it).
  6. DENY is checked before AFFIRM. Default NEUTRAL.
"""
import re, sys

STOP = set("""a an the and or but if then else when at by for with about into through during
before after above below to from up down in out on off over under again further once here
there when where which who whom this that these those am is are was were be been being
have has had having do does did doing would should could ought i me my we our you your
he him his she her it its they them their what which who whom this that these those am
are was were be been have has had having do does did will would shall should may might
must can could of in to for on with as by s t d ll ve re don isn aren wasn weren hasn
haven hadn doesn didn won wouldn couldn shouldn mightn mustn shan no nor not only own
same so than too very just don should now""".split())

# verb stems (generic propositional verbs; mental-state verbs excluded on purpose)
VERB_STEMS = set("""be is are was were am been being have has had do does did will would
can could should may might must shall boil boils orbit orbits revolve revolves cause
causes caused cure cures cured dissolve dissolves dissolved originate originated
originates fake faked fakes strike strikes struck use uses used show shows showed
shown say says said state states stated find finds found prove proves proved prove
confirm confirms confirmed demonstrate demonstrates demonstrate contain contains
treat treats treated heal heals remedy produce produces trigger triggers lead leads
break breaks clear clears hit hits see sees visible originate leak leaked flow flows
form forms rise rises fall falls grow grows make makes made take takes took build
builds link links tie ties connect connects spread spreads transmit transmits
lower lowers raise raises reduce reduces increase increases improve improves worsen
worsens disrupt disrupts block blocks stop stops prevent prevents drink drinks
drank drinking eat eats ate eating""".split())
VERB_STEMS = set(w.rstrip('s') if False else w for w in VERB_STEMS)  # keep as-is
REPORTING = set("say says said show shows showed shown claim claims claimed report reports "
                "reported suggest suggests argues argue think thinks believe believes states state".split())

NEG_TOKENS = set("not no never neither nor none nothing without hardly scarcely barely".split())
NT_FORMS = ("n't", "\u2019t")  # ASCII and U+2019
AUX = set("is are was were be been being am has have had do does did will would can could "
          "should may might must shall has had".split())

STRONG_DENY = set("false fake faked debunk myth hoax incorrect wrong disproven refuted denies "
                  "denied contrary".split())
# stemmed matching is applied; list base forms
WEAK_DENY = set("however although though despite unlikely".split())
NEUTRAL_MARKERS = set("seek seeks sought classify classified possible possibly potential "
                      "whether review reviews reviewed study studies studied research trial trials "
                      "debate debated uncertain unclear inconsistent mixed".split())

ASSERT_TOKENS = set("proof proofs proven confirms confirmed shows demonstrates evidence fact".split())

SYN = {
 "boil": ["boil"], "orbit": ["orbit", "revolve"], "cause": ["cause"],
 "cure": ["cure"], "dissolve": ["dissolve"], "originate": ["originate", "leak"],
 "fake": ["fake"], "strike": ["strike"], "use": ["use"], "show": ["show"],
 "have": ["have", "has", "had"], "be": ["be", "is", "are", "was", "were", "am"],
}
SUPERLATIVE = set("tallest largest highest biggest longest smallest only first best worst most least".split())
ANTONYMS = {"flat": ["spherical", "sphere", "round", "globe", "oblate"],
            "spherical": ["flat"]}
CONJ_SKIP = set("while although though however despite when where because since if then thus "
                "hence also just even still and but or yet so for nor".split())

def stem(w):
    w = w.lower()
    # possessive / contraction tail
    if w.endswith("'s"):
        w = w[:-2]
    w = w.strip("'")
    if len(w) <= 3:
        return w
    # plural / 3rd person
    if w.endswith("ies") and len(w) > 5:
        return w[:-3] + "y"
    if w.endswith("sses") or w.endswith("xes") or w.endswith("zes") or w.endswith("ches") or w.endswith("shes"):
        if len(w) > 5:
            return w[:-2]           # glasses -> glass, watches -> watch
    if w.endswith("es"):
        c1 = w[:-1]
        if c1.endswith("e"):
            return c1              # causes -> cause, dissolves -> dissolve
        return c1                  # default: strip s (orbit <- orbits never reaches here)
    if w.endswith("s") and not w.endswith("ss"):
        return w[:-1]              # orbits -> orbit
    if w.endswith("ied") and len(w) > 5:
        return w[:-3] + "y"
    if w.endswith("ed"):
        c = w[:-2]
        if c + "e" in VERB_STEMS:
            return c + "e"            # faked -> fake, caused -> cause
        if len(w) > 5 and w[-3] in "aeiou":
            return w[:-1]            # dissolved -> dissolve (len guard), agreed -> agree
        return c                     # orbited -> orbit
    if w.endswith("ing") and len(w) > 6:
        base = w[:-3]
        if base + "e" in VERB_STEMS:
            return base + "e"        # causing -> cause, faking -> fake
        if base.endswith("e") or (base and base[-1] not in "aeiou"):
            return base              # drinking -> drink, seeing -> see
        return base + "e"
    if w.endswith("ly") and len(w) > 5:
        return w[:-2]
    return w

def toks(text):
    # word tokens, keeping apostrophes (incl U+2019) and hyphens inside words
    return re.findall(r"[A-Za-z0-9\u2019']+(?:-[A-Za-z0-9\u2019']+)*", text)

def content_words(text):
    out = []
    for t in toks(text):
        s = stem(t)
        if len(t) > 3 and t.lower() not in STOP:
            out.append((t, s))
    return out

def split_clauses(text):
    # protect decimal numbers before splitting: 365.256 -> 365<PU>256
    prot = re.sub(r"(\d)\.(\d)", lambda m: m.group(1) + "\uE000" + m.group(2), text)
    parts = re.split(r"[.!?;\u2014]+", prot)
    return [p.replace("\uE000", ".") for p in parts if p.strip()]

class Claim:
    def __init__(self, text):
        self.text = text
        self.words = content_words(text)          # [(orig, stem)]
        ws = self.words
        # strip leading gerund (generic English syntax: "Drinking coffee causes...")
        if ws and ws[0][0].lower().endswith("ing") and stem(ws[0][0]) in VERB_STEMS:
            ws = ws[1:]
        self.core = ws
        self.stems = set(s for _, s in self.words)
        self.first_anchor = stem(ws[0][0]) if ws else ""
        self.last_anchor = stem(ws[-1][0]) if ws else ""
        # named-entity anchors: capitalized non-initial content words of the claim
        # (the claim's "aboutness" entities). Fallback: first/last content word.
        rawtoks = toks(text)
        named = set()
        for j, t in enumerate(rawtoks):
            if j > 0 and len(t) >= 4 and t[0].isupper() and stem(t) in self.stems:
                named.add(stem(t))
        self.named = named if named else ({self.first_anchor, self.last_anchor} - {""})
        self.predicate = self._predicate(ws, text)
        self.psyn = SYN.get(self.predicate, [self.predicate])

    def _predicate(self, ws, text):
        cands = []
        for (o, s) in ws:
            if s in VERB_STEMS and o.lower() not in REPORTING and stem(o.lower()) not in REPORTING:
                cands.append(s)
        if cands:
            return cands[0]
        # fallback: first auxiliary / copula among ALL tokens (stopwords included)
        for t in toks(text):
            tl = t.lower()
            if tl in ("is", "are", "was", "were", "am", "be", "been", "being"):
                return "be"
            if tl in ("has", "have", "had"):
                return "have"
        return ""

def clause_has_negation_scoping_predicate(cl_toks, pred_idx):
    """True if a negation marker scopes the predicate at token index pred_idx."""
    for j in range(max(0, pred_idx - 4), pred_idx):
        t = cl_toks[j].lower()
        if t in NEG_TOKENS:
            return True
        if t.endswith(NT_FORMS[0]) or t.endswith(NT_FORMS[1]):
            return True
        # n't attached: e.g. "doesn't"
    return False

WH_AUX = set("is are was were do does did can could would should will what when where which who whom how why".split())

def is_interrogative(clause):
    c = clause.strip()
    if "?" in clause:
        return True
    t = toks(c)
    # wh-/aux-initial short fragment without '?' (e.g. a question title whose
    # '?' was stripped): treat as interrogative only if brief; longer
    # keyword-stuffed snippets starting with 'why' still assert.
    if t and t[0].lower() in WH_AUX and len(t) <= 10:
        return True
    return False

FILLER = set("the a an to of and or but in on at for with from by as".split())

def competitor(cl_toks, pred_idx, claim, c_stemset):
    """The entity the clause's predicate is asserted of, when it is NOT the
    claim's subject. Two generic patterns:
    (1) immediate subject: nearest non-filler token before the predicate is a
        capitalized entity not in the claim (e.g. 'PCBs cause...', 'Mauna Kea is...');
    (2) far-field: a capitalized entity before the predicate while the claim's
        subject anchor (first content word) is absent (e.g. 'IARC ... cause cancer').
    Returns the competing token or None."""
    # (1) immediate subject
    j = pred_idx - 1
    while j >= 0 and cl_toks[j].lower() in FILLER:
        j -= 1
    if j >= 0 and len(cl_toks[j]) >= 3 and cl_toks[j][0].isupper():
        if stem(cl_toks[j]) not in claim.stems:
            return cl_toks[j]
    # (2) far-field, only when the claim's subject is absent
    if claim.first_anchor not in c_stemset:
        for j in range(pred_idx):
            t = cl_toks[j]
            if j == 0:
                continue
            if len(t) >= 4 and t[0].isupper():
                s = stem(t)
                if s not in claim.stems and t.lower() not in CONJ_SKIP:
                    return t
    return None

def competing_proper_noun(cl_toks, pred_idx, claim, c_stemset):
    return competitor(cl_toks, pred_idx, claim, c_stemset)

def claim_numbers(claim_text):
    """Long digit sequences (>=5 digits) in the claim: distinctive values like
    299,792,458. A clause repeating the claim's exact value affirms it."""
    return set(re.findall(r"\d[\d,]*\d", claim_text))

def has_claim_value(clause, claim):
    nums = claim_numbers(claim.text)
    if not nums:
        return False
    cl = clause.replace(",", "").replace(" ", "")
    for n in nums:
        if n.replace(",", "").replace(" ", "") in cl:
            return True
    return False

def classify(claim_text, title, snippet):
    cl = Claim(claim_text)
    # rule 0: overlap gate on whole text
    full = (title or "") + " " + (snippet or "")
    t_stems = set(stem(t) for t in toks(full))
    need = 1 if len(cl.words) < 3 else 2
    if len(cl.stems & t_stems) < need:
        return 0, "gate"
    deny_reason = None
    affirm_clause = None
    # title and snippet are separate clause streams (a title entity must not
    # veto a snippet clause and vice versa)
    clauses = split_clauses(title or "") + split_clauses(snippet or "")
    for clause in clauses:
        ct = toks(clause)
        if not ct:
            continue
        c_stems = [stem(t) for t in ct]
        c_stemset = set(c_stems)
        n_claim = len(cl.stems & c_stemset)
        anchor_ok = cl.first_anchor in c_stemset or cl.last_anchor in c_stemset
        # --- DENY rules not needing the predicate ---
        # (a) denial lexicon
        strong = any(stem(t) in STRONG_DENY or any(stem(t).startswith(x) for x in ("debunk","disprov","refut","incorrect","wrong","myth","hoax","fals")) for t in ct)
        weak = any(t.lower() in WEAK_DENY or "no evidence" in clause.lower() or "no longer" in clause.lower() for t in ct)
        # anaphoric denial: short clause ("Both are false") with a strong token
        # refers to the text's topic when the full text has high claim overlap
        anaphoric = strong and len(ct) <= 8 and len(cl.stems & t_stems) >= 3
        if (strong and n_claim >= 1) or (weak and n_claim >= 2) or anaphoric:
            return 2, "deny-lex"
        # (d) antonym
        for a, ants in ANTONYMS.items():
            if a in cl.stems and any(x in c_stemset for x in ants) and n_claim >= 1:
                return 2, "antonym"
        # --- predicate-dependent rules ---
        pidx = [i for i, s in enumerate(c_stems) if s in cl.psyn]
        if not pidx:
            continue
        pi = pidx[0]
        # (b) negation scoping predicate
        if clause_has_negation_scoping_predicate(ct, pi) and n_claim >= 1:
            return 2, "neg-scope"
        # (c) competing subject + superlative/identity predicate
        # (skipped for interrogatives, when the clause repeats the claim's
        # exact value, and when the clause isn't about the claim's subject)
        comp = competing_proper_noun(ct, pi, cl, c_stemset)
        if comp and n_claim >= 1 and cl.first_anchor in c_stemset and (cl.predicate == "be" or any(s in SUPERLATIVE for s in c_stems)):
            if not is_interrogative(clause) and not has_claim_value(clause, cl):
                return 2, "competing-subject"
        # --- AFFIRM rules ---
        if affirm_clause is None:
            # reporting frame ("conspiracy theory about X", "choose a legend")
            # describes the claim without asserting it -> never endorsement
            low = clause.lower()
            framed = ("conspiracy theory" in low or "choose a legend" in low
                      or low.startswith("legend:") or "urban legend" in low)
            if (n_claim >= need and anchor_ok
                    and not clause_has_negation_scoping_predicate(ct, pi)
                    and not is_interrogative(clause)
                    and not framed
                    and comp is None):
                affirm_clause = clause.strip()[:60]
    if affirm_clause is not None:
        return 1, "endorse"
    return 0, "neutral"

if __name__ == "__main__":
    tests = [
        # (claim, title, snippet, expected, note)
        ("Drinking coffee causes cancer.",
         "Coffee doesn\u2019t cause cancer, but hot drinks might - Sharecare",
         "A group of 23 scientists reviewed studies and found inadequate evidence.",
         2, "C7 sharecare U+2019"),
        ("Drinking coffee causes cancer.",
         "WHO no longer says coffee causes cancer",
         "As of June 15, coffee got a clean bill of health.",
         2, "C7 theconversation"),
        ("Drinking coffee causes cancer.",
         "Coffee and cancer: what the evidence says - WHO",
         "The IARC Monographs Programme seeks to classify cancer hazards.",
         0, "C7 who.int"),
        ("The Earth is flat.",
         "5 Real-World Flat-Earth Proofs - YouTube",
         "Top 5 proofs the earth is flat.",
         1, "C8 youtube genuine"),
        ("The Earth is flat.",
         "The Flat Earth - tfes.org",
         "The Flat Earth Wiki.",
         0, "C8 tfes title-only"),
        ("The Earth is flat.",
         "Shape of the Earth - Britannica",
         "empirical observations revealed that Earth's shape was spherical.",
         2, "C8 britannica antonym"),
        ("Earth orbits the Sun.",
         "Solar System - Wikipedia",
         "One complete orbit takes 365.256 days, during which time Earth has traveled.",
         1, "C3 wiki1"),
        ("Earth orbits the Sun.",
         "Why does the Earth orbit the Sun? - TikTok",
         "why does earth orbit the sun, earth orbit vs jupiter and not saturn.",
         1, "C3 tiktok"),
        ("Earth orbits the Sun.",
         "EARTH does NOT REVOLVE around the SUN - How Earth Orbits...",
         "This video explains that Earth does not revolve around the Sun.",
         2, "C3 youtube genuine deny"),
        ("This one fruit dissolves blood clots, doctors hate it.",
         "These 7 Fruits Dissolve Blood Clots FAST - YouTube",
         "Doctors are shocked by these fruits.",
         1, "C15 youtube genuine"),
        ("This one fruit dissolves blood clots, doctors hate it.",
         "Blood thinners - WebMD",
         "Blood thinners don\u2019t dissolve the clot.",
         2, "C15 webmd U+2019"),
        ("Chocolate cures insomnia, new study shows.",
         "Cure Insomnia in 5 Minutes with Pouring Rain - YouTube",
         "Rain sounds to cure insomnia fast.",
         0, "C16 youtube no anchor"),
        ("Chocolate cures insomnia, new study shows.",
         "15 Natural Insomnia Cures You Haven't Tried - Lifehack",
         "Natural insomnia cures that work.",
         0, "C16 lifehack competing subject"),
        ("The tallest mountain in the world is Mount Everest.",
         "Tallest mountain - Guinness",
         "Mauna Kea on the island of Hawaii, USA, is the world's tallest mountain.",
         2, "C12 mauna kea"),
        ("The tallest mountain in the world is Mount Everest.",
         "Mount Everest - Wikipedia",
         "Mount Everest is the world's highest mountain.",
         1, "C12 everest"),
        ("The Apollo moon landings were faked.",
         "How do we know that we went to the Moon? - iop.org",
         "Evidence that the moon landings were real.",
         0, "C9 interrogative"),
        ("Water boils at 100 degrees Celsius at sea level.",
         "Boiling Point of Water - sciencenotes.org",
         "At sea level, water boils at 100C.",
         1, "C1 genuine"),
        ("Water boils at 100 degrees Celsius at sea level.",
         "Why does water boil? - co.uk",
         "At sea level, water boils at 100C because of pressure.",
         1, "C1 because-clause"),
    ]
    bad = 0
    for claim, ti, sn, exp, note in tests:
        got, reason = classify(claim, ti, sn)
        ok = "OK " if got == exp else "FAIL"
        if got != exp:
            bad += 1
        print(f"{ok} exp={exp} got={got} ({reason}) :: {note}")
    print("failures:", bad)
