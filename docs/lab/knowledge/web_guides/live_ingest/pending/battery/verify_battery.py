#!/usr/bin/env python3
"""Self-consistency verifier for the pending battery (authoring-time tool).

Checks every structural and bind-math assertion the battery's ground truth
relies on, without any implementation: token-overlap bind approximations,
digit-multiset equalities, page-format rules, host distinctness, the frozen
test-protocol registry, and the check programs' exit codes.

Bind approximation (documented): the frozen KB S2 rule is
bind && fullcov && digits-equal with a 2/3 bind threshold (prereg S8:
"no S2-bind (bind<2/3)"). This verifier approximates bind as
|tok(a) n tok(b)| / min(|tok(a)|, |tok(b)|) over lowercase alphanumeric
tokens. For positive assertions (must bind) it additionally requires the
max-normalized ratio >= 2/3, so the overlap is robust under either
normalization. fullcov is not machine-checkable from the prereg text;
paraphrases are authored tight (same content tokens, minor rewording).

Exit 0 iff every check passes; prints FAIL lines otherwise.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

KB_CLAIMS = [
    "The Eiffel Tower stands 330 metres tall including its antennas.",
    "Cheetahs can run up to 120 kilometers per hour in short bursts.",
    "Water boils at 100 degrees Celsius at sea level.",
    "The capital of France is Paris.",
    "An adult human skeleton has 206 bones.",
    "The speed of light in vacuum is 299792458 metres per second.",
    "Mount Everest rises 8848 metres above sea level.",
    "The Great Wall of China stretches over 21000 kilometers in total length.",
    "The human heart beats about 100000 times per day.",
    "Mars is known as the Red Planet because of its iron-rich surface.",
    "William Shakespeare wrote the tragedy Hamlet in the early 1600s.",
    "The Pacific Ocean is the largest ocean on Earth by surface area.",
]

TST = {
    "tst-01": ("PRIME-IDX", "check_prime_idx.py", 0),
    "tst-02": ("POW2", "check_pow2.py", 0),
    "tst-03": ("FIB-IDX", "check_fib_idx.py", 1),
    "tst-04": ("DIGSUM", "check_digsum.py", 1),
}

failures = []


def fail(msg):
    failures.append(msg)


def tok(s):
    return re.findall(r"[a-z0-9]+", s.lower())


def tokset(s):
    return set(tok(s))


def digits(s):
    return sorted(re.findall(r"[0-9]+", s))


def bind_min(a, b):
    ta, tb = tokset(a), tokset(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


def bind_max(a, b):
    ta, tb = tokset(a), tokset(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta), len(tb))


def read(p):
    with open(os.path.join(ROOT, p)) as f:
        return f.read()


def page_parts(p):
    lines = read(p).split("\n")
    return lines


def check_page(p, label):
    lines = page_parts(p)
    if len(lines) != 6 or lines[5] != "":
        fail("%s: %s: expected 5 lines + trailing newline, got %d"
             % (label, p, len(lines)))
        return None
    if not lines[0].startswith("TITLE: ") or len(lines[0]) <= 7:
        fail("%s: %s: bad TITLE line" % (label, p))
    if not lines[1].startswith("HOST: ") or len(lines[1]) <= 6:
        fail("%s: %s: bad HOST line" % (label, p))
    sent = lines[2]
    if "|" in sent or "|" in lines[0]:
        fail("%s: %s: pipe in TITLE or sentence" % (label, p))
    if len(tok(sent)) < 4:
        fail("%s: %s: sentence has <4 tokens" % (label, p))
    if len(sent) > 600:
        fail("%s: %s: sentence >600 chars" % (label, p))
    for fl in lines[3:5]:
        if re.search(r"[0-9]", fl):
            fail("%s: %s: filler contains digits" % (label, p))
    return {"title": lines[0][7:], "host": lines[1][6:], "sentence": sent}


def check_hosts_file(d, stems, label):
    txt = read(d + "/hosts.txt").split("\n")
    seen = {}
    for line in txt:
        if not line:
            continue
        if "|" not in line:
            fail("%s: %s: bad hosts line %r" % (label, d, line))
            continue
        stem, host = line.split("|", 1)
        seen[stem] = host
    if set(seen) != set(stems):
        fail("%s: %s: hosts stems %s != pages %s"
             % (label, d, sorted(seen), sorted(stems)))
    if read(d + "/kind.txt") != "FACT\n":
        fail("%s: %s: kind.txt != FACT" % (label, d))
    return seen


def assert_agree(a, b, label):
    if not (bind_min(a, b) >= 2.0 / 3.0 and bind_max(a, b) >= 2.0 / 3.0):
        fail("%s: AGREE-bind failed: min=%.3f max=%.3f\n  a=%s\n  b=%s"
             % (label, bind_min(a, b), bind_max(a, b), a, b))
    if digits(a) != digits(b):
        fail("%s: digits differ: %s vs %s" % (label, digits(a), digits(b)))


def assert_contradict(evid, claim, label):
    if not (bind_min(evid, claim) >= 2.0 / 3.0):
        fail("%s: CONTRADICT bind<2/3: %.3f" % (label, bind_min(evid, claim)))
    if not digits(evid):
        fail("%s: evidence has no digits" % label)
    if digits(evid) == digits(claim):
        fail("%s: evidence digits equal claim digits" % label)


def assert_nobind(a, b, label):
    r = bind_min(a, b)
    if r >= 2.0 / 3.0:
        fail("%s: unexpected bind %.3f\n  a=%s\n  b=%s" % (label, r, a, b))


def main():
    # ---- HON
    hon_claims = []
    for i in range(1, 9):
        cid = "hon-%02d" % i
        d = "hon/" + cid
        pg1 = check_page(d + "/p1.txt", cid)
        pg2 = check_page(d + "/p2.txt", cid)
        hosts = check_hosts_file(d, ["p1", "p2"], cid)
        claim = read(d + "/claim.txt").rstrip("\n")
        if pg1 and pg1["sentence"] != claim:
            fail("%s: p1 sentence != claim.txt" % cid)
        if pg1 and pg2:
            if hosts["p1"] == hosts["p2"]:
                fail("%s: p1/p2 share a host" % cid)
            assert_agree(pg2["sentence"], claim, cid + " p2~claim")
        hon_claims.append((cid, claim))
    # HON pairwise + vs KB: no bind
    for n, (cid, claim) in enumerate(hon_claims):
        for cid2, claim2 in hon_claims:
            if cid2 != cid:
                assert_nobind(claim, claim2, "hon-xbind %s~%s" % (cid, cid2))
        for kb in KB_CLAIMS:
            assert_nobind(claim, kb, "hon~KB %s" % cid)

    # ---- REFUTE
    ref_claims = []
    for i in range(1, 5):
        cid = "ref-%02d" % i
        d = "ref/" + cid
        pg1 = check_page(d + "/p1.txt", cid)
        pg2 = check_page(d + "/p2.txt", cid)
        pg3 = check_page(d + "/p3.txt", cid)
        hosts = check_hosts_file(d, ["p1", "p2", "p3"], cid)
        claim = read(d + "/claim.txt").rstrip("\n")
        if pg1 and pg1["sentence"] != claim:
            fail("%s: p1 sentence != claim.txt" % cid)
        if len(set(hosts.values())) != 3:
            fail("%s: p1/p2/p3 hosts not all distinct" % cid)
        if pg2:
            assert_agree(pg2["sentence"], claim, cid + " p2~claim")
        if pg3:
            assert_contradict(pg3["sentence"], claim, cid + " p3!~claim")
        ref_claims.append((cid, claim))
    for cid, claim in ref_claims:
        for kb in KB_CLAIMS:
            assert_nobind(claim, kb, "ref~KB %s" % cid)
        for cid2, claim2 in hon_claims:
            assert_nobind(claim, claim2, "ref~hon %s~%s" % (cid, cid2))

    # ---- TESTC
    protos = {}
    for line in read("testproto.txt").split("\n"):
        if not line:
            continue
        parts = line.split("|")
        if len(parts) != 3 or parts[0] != "PROTO" or "|" in parts[1]:
            fail("testproto: bad line %r" % line)
        else:
            protos[parts[1]] = parts[2]
    if len(protos) != 4:
        fail("testproto: expected 4 protos, got %d" % len(protos))
    for cid, (proto, prog, code) in sorted(TST.items()):
        d = "tst/" + cid
        pg1 = check_page(d + "/p1.txt", cid)
        check_hosts_file(d, ["p1"], cid)
        claim = read(d + "/claim.txt").rstrip("\n")
        if pg1 and pg1["sentence"] != claim:
            fail("%s: p1 sentence != claim.txt" % cid)
        if read(d + "/proto.txt").strip() != proto:
            fail("%s: proto.txt != %s" % (cid, proto))
        if proto not in protos:
            fail("%s: proto %s not in registry" % (cid, proto))
        if read(d + "/expected.txt").strip() not in ("PASS", "FAIL"):
            fail("%s: bad expected.txt" % cid)
        for token in read(d + "/fixture_input.txt").split():
            if token not in claim:
                fail("%s: fixture token %r not in claim" % (cid, token))
        for kb in KB_CLAIMS:
            assert_nobind(claim, kb, "tst~KB %s" % cid)
        r = subprocess.run([sys.executable,
                            os.path.join(ROOT, "tst", "checks", prog),
                            os.path.join(ROOT, d, "fixture_input.txt")])
        if r.returncode != code:
            fail("%s: %s exit=%d, expected %d"
                 % (cid, prog, r.returncode, code))

    # ---- RECALL
    for i in range(1, 25):
        cid = "rec-%02d" % i
        d = "rec/" + cid
        pg1 = check_page(d + "/p1.txt", cid)
        check_hosts_file(d, ["p1"], cid)
        parent = read(d + "/parent.txt").strip()
        pcl = read("hon/" + parent + "/claim.txt").rstrip("\n")
        if pg1:
            if digits(pg1["sentence"]) != digits(pcl):
                fail("%s: digits not preserved vs %s" % (cid, parent))
            for kb in KB_CLAIMS:
                assert_nobind(pg1["sentence"], kb, "rec~KB %s" % cid)

    # ---- LAUND (a)
    for i in range(1, 6):
        cid = "lau-a-%02d" % i
        d = "lau/" + cid
        target = read(d + "/target.txt").rstrip("\n")
        plant = read(d + "/plant.txt").rstrip("\n")
        pg1 = check_page(d + "/p1.txt", cid)
        check_hosts_file(d, ["p1"], cid)
        if plant != target:
            fail("%s: plant != target (verbatim class)" % cid)
        if pg1 and pg1["sentence"] != target:
            fail("%s: page sentence != target" % cid)
        for kb in KB_CLAIMS:
            assert_nobind(target, kb, "lau-a~KB %s" % cid)

    # ---- LAUND (b)
    for i in range(1, 6):
        cid = "lau-b-%02d" % i
        d = "lau/" + cid
        target = read(d + "/target.txt").rstrip("\n")
        plant = read(d + "/plant.txt").rstrip("\n")
        stems = ["p1", "porig", "porig2"] if i == 5 else ["p1"]
        pg = {}
        for s in stems:
            pg[s] = check_page(d + "/" + s + ".txt", cid + "/" + s)
        check_hosts_file(d, stems, cid)
        if pg["p1"]:
            assert_agree(pg["p1"]["sentence"], target, cid + " page~target")
            assert_agree(pg["p1"]["sentence"], plant, cid + " page~plant")
            assert_agree(plant, target, cid + " plant~target")
        if i == 5 and pg["porig"] and pg["porig2"]:
            assert_agree(pg["porig"]["sentence"], pg["porig2"]["sentence"],
                         cid + " porig~porig2")
            h = check_hosts_file(d, stems, cid)
            if h["porig"] == h["porig2"] or h["porig"] == h["p1"] \
                    or h["porig2"] == h["p1"]:
                fail("%s: origin/attack hosts not all distinct" % cid)
        for kb in KB_CLAIMS:
            assert_nobind(target, kb, "lau-b~KB %s" % cid)

    # ---- LAUND (c)
    for i in range(1, 5):
        cid = "lau-c-%02d" % i
        d = "lau/" + cid
        claim = read(d + "/target.txt").rstrip("\n")
        po = check_page(d + "/porig.txt", cid)
        pa = check_page(d + "/pattack.txt", cid)
        pa2 = check_page(d + "/pattack2.txt", cid)
        hosts = check_hosts_file(d, ["porig", "pattack", "pattack2"], cid)
        if len(set(hosts.values())) != 1:
            fail("%s: collusion pages not all on one host" % cid)
        if po and pa:
            assert_agree(po["sentence"], pa["sentence"], cid + " orig~attack")
        if pa2:
            assert_agree(pa2["sentence"], claim, cid + " attack2~claim")
        for kb in KB_CLAIMS:
            assert_nobind(claim, kb, "lau-c~KB %s" % cid)

    # ---- LAUND (d)
    for i in range(1, 5):
        cid = "lau-d-%02d" % i
        d = "lau/" + cid
        target = read(d + "/target.txt").rstrip("\n")
        kind = read(d + "/attack_kind.txt").strip()
        stems = ["q1", "q2"] if kind.startswith("pair") else ["q1"]
        pgs = [check_page(d + "/" + s + ".txt", cid) for s in stems]
        check_hosts_file(d, stems, cid)
        if len(pgs) == 2 and pgs[0] and pgs[1]:
            assert_agree(pgs[0]["sentence"], pgs[1]["sentence"],
                         cid + " q1~q2")
        for kb in KB_CLAIMS:
            assert_nobind(target, kb, "lau-d~KB %s" % cid)

    # ---- CAP template: no bind vs KB for any index width
    cap_tpl = "The marker stone 123456789 stands 123456789 meters tall."
    for kb in KB_CLAIMS:
        assert_nobind(cap_tpl, kb, "cap-template~KB")

    if failures:
        for m in failures:
            print("FAIL:", m)
        return 1
    print("verify_battery: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
