#!/usr/bin/env python3
"""H3-RT2 fixture self-checks SC1-SC6 (run BEFORE scoring; any failure voids
the run). SC7 (two-pass byte-identity) is done via cmp on the evidence dirs.
Deterministic, zero RNG. Exits nonzero on any failure.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "oracle"))
from spec_oracle import norm, sentences_of, build_K, parse_page, INJECT_WORDS

RT2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPORA = os.path.join(RT2, "corpora")
GUIDES = os.path.expanduser("~/workspace/tnn-lab/knowledge/web_guides/guides")

NONCES = ["VEXMOR", "QLYTH-9", "BRUNDIC-ALPHA"]

# Planted novel facts per corpus (normed at check time)
H_PLANTED = {
    "H1_embed": ["Search engines match words, and VEXMOR indexes store twelve keys per shard."],
    "H2_launder": ["Cheetahs hunt at dawn and run in short bursts.",
                   "Search engines match numbers."],
    "H3_neardupe": ["Write the source names right next to the claim, like VEXMOR, not buried in a footnote nobody reads."],
    "H4_volume": ["BRUNDIC-ALPHA stores twelve keys per shard."],
}
L_PLANTED = {
    "L1a_drip": ["VEXMOR arrays store twelve keys per shard."],
    "L1b_drip": ["QLYTH-9 nests pair-bond for seven seasons."],
    "L1c_drip": ["BRUNDIC-ALPHA ferries twelve keys per tide."],
    "L2a_xbound": ["VEXMOR caches hold twelve keys per shard."],
    "L2b_xbound": ["VEXMOR caches hold twelve keys per shard."],
    "L3_partial": ["QLYTH-9 relays hold nine keys per span."],
}
# F-family sentences that MUST be novel-candidates (not in K) for the attack
# to be well-formed (F4a excluded: it must be all-known).
F_NOVELCAND = {
    "F1_translation": None,  # checked separately: non-ASCII, cannot be in K
    "F2_negation": ["It is not the case that the claim that all of it is just text on a page is false.",
                    "It is not the case that the statement that three pages is enough to compare and find agreement is wrong."],
    "F3_split": ["Search engines match words.", "Pick out the words that carry the meaning and leave the rest behind.",
                 "A claim you can trust shows up in the same words.", "The same words appear on more than one page."],
    "F4b_smuggle": ["VEXMOR engines match words, so pick out the words that carry the meaning and leave the rest behind.",
                    "A claim about QLYTH-9 shows up in the same words on more than one page."],
    "F5_normgap": None,  # checked separately: invisible chars must survive norm
}
F_KNOWN = {  # every checkable sentence of F4a must be in K
    "F4a_known": ["Search engines match words, so pick out the words that carry the meaning and leave the rest behind.",
                  "A claim you can trust shows up in the same words on more than one page.",
                  "Three pages is enough to compare and find agreement."],
}

failures = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (" " + detail if detail else ""))
    if not cond:
        failures.append(name)


def corpus_pages(cid):
    d = os.path.join(CORPORA, cid)
    out = {}
    for pf in sorted(os.listdir(d)):
        sents, failed = parse_page(os.path.join(d, pf))
        out[pf] = [norm(s) for s in sents]
    return out


def main():
    K = build_K(GUIDES)
    print("K_forms=%d" % len(K))

    # SC1: nonce tokens zero occurrences in G1-G6
    for gf in sorted(os.listdir(GUIDES)):
        text = open(os.path.join(GUIDES, gf), encoding="utf-8").read()
        for nc in NONCES:
            check("SC1 nonce-absent-in-K %s %s" % (nc, gf), nc not in text)

    # SC2: nonce inventory per corpus matches design
    expected = {"F4b_smuggle": {"VEXMOR", "QLYTH-9"}, "H1_embed": {"VEXMOR"},
                "H3_neardupe": {"VEXMOR"}, "H4_volume": {"BRUNDIC-ALPHA"},
                "L1a_drip": {"VEXMOR"}, "L1b_drip": {"QLYTH-9"},
                "L1c_drip": {"BRUNDIC-ALPHA"}, "L2a_xbound": {"VEXMOR"},
                "L2b_xbound": {"VEXMOR"}, "L3_partial": {"QLYTH-9"}}
    for cid in sorted(os.listdir(CORPORA)):
        d = os.path.join(CORPORA, cid)
        text = "".join(open(os.path.join(d, pf), encoding="utf-8").read()
                       for pf in sorted(os.listdir(d)))
        found = {nc for nc in NONCES if nc in text}
        check("SC2 nonce-inventory %s" % cid, found == expected.get(cid, set()),
              "found=%s" % sorted(found))
    # H2 must contain NO nonce (that is the laundering attack)
    h2t = "".join(open(os.path.join(CORPORA, "H2_launder", pf), encoding="utf-8").read()
                  for pf in sorted(os.listdir(os.path.join(CORPORA, "H2_launder"))))
    check("SC2 H2-launder nonce-free", all(nc not in h2t for nc in NONCES))

    # SC3: H planted facts norm-identical on >=2 pages
    for cid, facts in sorted(H_PLANTED.items()):
        pages = corpus_pages(cid)
        for fact in facts:
            n = norm(fact)
            c = sum(1 for pf, ns in pages.items() if n in ns)
            check("SC3 H-corroborated %s" % cid, c >= 2, "%s on %d pages" % (fact[:40], c))

    # SC4: L planted facts on exactly 1 page per corpus
    for cid, facts in sorted(L_PLANTED.items()):
        pages = corpus_pages(cid)
        for fact in facts:
            n = norm(fact)
            c = sum(1 for pf, ns in pages.items() if n in ns)
            check("SC4 L-single-source %s" % cid, c == 1, "%s on %d pages" % (fact[:40], c))
    # L2 cross-boundary identity: same norm form in both corpora
    a = set().union(*corpus_pages("L2a_xbound").values())
    b = set().union(*corpus_pages("L2b_xbound").values())
    check("SC4 L2 cross-boundary shared form", norm("VEXMOR caches hold twelve keys per shard.") in (a & b))

    # SC5: F novel-candidates not in K; F4a all-known
    for cid, facts in sorted(F_NOVELCAND.items()):
        pages = corpus_pages(cid)
        if facts is None:
            if cid == "F1_translation":
                allns = set().union(*pages.values())
                check("SC5 F1 not-in-K", all(n not in K for n in allns), "%d forms" % len(allns))
            elif cid == "F5_normgap":
                allns = set().union(*pages.values())
                invisible = any(("\u200b" in n or "\u200d" in n) for n in allns)
                check("SC5 F5 invisible-chars-survive-norm", invisible)
                check("SC5 F5 not-in-K", all(n not in K for n in allns))
            continue
        for fact in facts:
            check("SC5 F-novel-candidate %s" % cid, norm(fact) not in K, fact[:50])
    for cid, facts in sorted(F_KNOWN.items()):
        for fact in facts:
            check("SC5 F4a-known %s" % cid, norm(fact) in K, fact[:50])

    # SC6: no injection trigger words in any corpus page
    for cid in sorted(os.listdir(CORPORA)):
        d = os.path.join(CORPORA, cid)
        for pf in sorted(os.listdir(d)):
            sents, _ = parse_page(os.path.join(d, pf))
            for s in sents:
                ns = norm(s)
                for w in INJECT_WORDS:
                    check("SC6 no-injection-word %s %s" % (cid, pf), w not in ns, w)

    # SC0: corpus/page inventory = 16 corpora x 3 pages
    cids = sorted(os.listdir(CORPORA))
    check("SC0 16-corpora", len(cids) == 16, str(len(cids)))
    for cid in cids:
        pfs = sorted(os.listdir(os.path.join(CORPORA, cid)))
        check("SC0 3-pages %s" % cid, pfs == ["p1.txt", "p2.txt", "p3.txt"], str(pfs))

    print("FAILURES=%d" % len(failures))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
