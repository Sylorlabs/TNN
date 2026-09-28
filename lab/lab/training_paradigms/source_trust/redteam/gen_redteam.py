#!/usr/bin/env python3
"""Wave-2 red-team attack corpora for the SOURCE-TRUST forks program.

Deterministic by construction: episodes are hand-designed arithmetic
patterns; zero RNG anywhere. Each stream emits:
  # comment lines, then one episode per line:
  ep etype src key val aux gt
gt: 1=true SAY, 0=false SAY, 2=WORLD (passthrough, never read by forks).

src ids are kept < 64 so Fork L's input guard (0<=src<64) never fires;
keys < 8192 (K folds by mod); all within every fork's capacity caps.

True value: tv(key) = 1000 + (key*37) % 8000.  False value: tv(key)+1.
"""
import os, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "streams")

def tv(key):
    return 1000 + (key * 37) % 8000

def fv(key):
    return tv(key) + 1

class Stream:
    def __init__(self, name, desc, aux_meanings):
        self.name = name
        self.desc = desc
        self.aux_meanings = aux_meanings
        self.eps = []          # (etype, src, key, val, aux, gt)
        self.sources = {}
        self.truevals = {}

    def say(self, src, key, val, aux, gt):
        self.eps.append((1, src, key, val, aux, gt))

    def world(self, key, val, aux=0):
        self.eps.append((2, 0, key, val, aux, 2))

    def honest(self, src, key, aux=1):
        """One honest episode: true SAY then WORLD confirmation."""
        self.say(src, key, tv(key), aux, 1)
        self.world(key, tv(key))

    def lie(self, src, key, aux=2):
        """One caught lie: false SAY then WORLD disagreement."""
        self.say(src, key, fv(key), aux, 0)
        self.world(key, tv(key))

    def write(self):
        os.makedirs(OUT, exist_ok=True)
        txt = os.path.join(OUT, self.name + ".txt")
        js = os.path.join(OUT, self.name + ".json")
        with open(txt, "w") as f:
            f.write("# %s\n# %s\n# episodes=%d\n" % (self.name, self.desc, len(self.eps)))
            f.write("# fmt: ep etype src key val aux gt\n")
            for i, (et, src, key, val, aux, gt) in enumerate(self.eps):
                f.write("%d %d %d %d %d %d %d\n" % (i + 1, et, src, key, val, aux, gt))
        with open(js, "w") as f:
            json.dump({
                "name": self.name, "description": self.desc,
                "aux_meanings": self.aux_meanings,
                "sources": self.sources,
                "truevals": {str(k): tv(k) for k in self.truevals},
                "episodes": [
                    {"ep": i + 1, "etype": et, "src": src, "key": key,
                     "val": val, "aux": aux, "gt": gt}
                    for i, (et, src, key, val, aux, gt) in enumerate(self.eps)
                ]}, f, indent=1)
        print("wrote %s (%d episodes)" % (self.name, len(self.eps)))
        return self.name


# ---- Task 1: Sybil-ring variants (KB-3 robustness) ----

def gen_v1_ring12():
    s = Stream("RT2-V1-ring12",
               "Sybil variant: 12-member ring, 5 claims x 5 SAYs (RT-T2 shape, bigger ring). No WORLD. Bar: 0 installs; KB-3: >=3 kills.",
               {"1-12": "ring member index"})
    ring = list(range(51, 63))
    for m in ring:
        s.sources[m] = "sybil ring member"
    for c in range(5):
        key = 1801 + c
        s.truevals[key] = True
        members = [ring[(c + j) % 12] for j in range(5)]
        for j, m in enumerate(members):
            s.say(m, key, fv(key), (m - 51) + 1, 0)
    return s

def gen_v2_ring4():
    s = Stream("RT2-V2-ring4",
               "Sybil variant: 4-member ring, 5 claims x 5 SAYs (smaller ring; 5th SAY repeats member 1). No WORLD. Bar: 0 installs; KB-3: >=3 kills.",
               {"1-4": "ring member index"})
    ring = [51, 52, 53, 54]
    for m in ring:
        s.sources[m] = "sybil ring member"
    for c in range(5):
        key = 1811 + c
        s.truevals[key] = True
        members = [ring[(c + j) % 4] for j in range(5)]
        for m in members:
            s.say(m, key, fv(key), (m - 51) + 1, 0)
    return s

def gen_v3_stagger():
    s = Stream("RT2-V3-stagger",
               "Sybil variant: 8 members enter staggered; each newcomer opens a NEW key, two incumbents co-assert. 8 keys x 3 SAYs. No WORLD. Bar: 0 installs; KB-3: >=3 kills.",
               {"1": "key opener (newcomer)", "2": "incumbent co-assertion"})
    ring = list(range(51, 59))
    for m in ring:
        s.sources[m] = "sybil ring member"
    for i, m in enumerate(ring):
        key = 1901 + i
        s.truevals[key] = True
        s.say(m, key, fv(key), 1, 0)
        s.say(ring[(i + 1) % 8], key, fv(key), 2, 0)
        s.say(ring[(i + 2) % 8], key, fv(key), 2, 0)
    return s

def gen_v4_sleeper():
    s = Stream("RT2-V4-sleeper",
               "Sybil variant: 8-member ring behaves honestly first (18 world-confirmed true claims per member, each co-asserted with an honest outsider), then 5 false claims x 5 ring SAYs. Tests whether farmed independence defeats structural Sybil defenses. Bar: 0 installs; KB-3: >=3 kills.",
               {"1": "honest-phase true claim", "2": "ring attack SAY"})
    ring = list(range(51, 59))
    outs = [11, 12, 13, 14]
    for m in ring:
        s.sources[m] = "sybil ring member (sleeper)"
    for h in outs:
        s.sources[h] = "honest outsider"
    key = 3000
    # honest phase: 18 VINDs per ring member, each co-asserted with an outsider
    for rnd in range(18):
        for j, m in enumerate(ring):
            key += 1
            s.truevals[key] = True
            h = outs[(rnd + j) % 4]
            s.say(m, key, tv(key), 1, 1)
            s.say(h, key, tv(key), 1, 1)
            s.world(key, tv(key))
    # attack phase: 5 false claims x 5 ring SAYs, rotating window (RT-T2 shape)
    # NOTE: keys 3201+ are disjoint from the honest phase (3001-3144).
    for c in range(5):
        akey = 3201 + c
        s.truevals[akey] = True
        members = [ring[(c + j) % 8] for j in range(5)]
        for m in members:
            s.say(m, akey, fv(akey), 2, 0)
    return s

def gen_v5_onekey():
    s = Stream("RT2-V5-onekey",
               "Sybil variant: single key, 25 SAYs from 8 rotating members. Tests whether per-key containment (S R7) lets a fork survive a one-key ring. Bar: 0 installs; KB-3: >=3 kills.",
               {"1-8": "ring member index"})
    ring = list(range(51, 59))
    for m in ring:
        s.sources[m] = "sybil ring member"
    key = 3201
    s.truevals[key] = True
    for i in range(25):
        m = ring[i % 8]
        s.say(m, key, fv(key), (m - 51) + 1, 0)
    return s


# ---- Task 2: attacks on L ----

def gen_l_dot():
    s = Stream("L-DOT",
               "Denial-of-truth vs L: poison source P1 (trust 333) pre-asserts 10 TRUE claims; honest H (trust 954) then asserts them. Control: 10 truths with no pre-taint. Rescue: H2,H3 (trust 954) assert pre-tainted truths. Measures whether an adversary can force WITHHOLD of true corroborated claims.",
               {"1": "honest farm", "2": "poison lie", "3": "poison pre-taint (true claim)",
                "4": "honest truth after pre-taint", "5": "honest truth, no pre-taint (control)",
                "6": "rescue assertion by 2nd/3rd honest source"})
    H, H2, H3, P1 = 10, 11, 12, 20
    s.sources[H] = "honest H"
    s.sources[H2] = "honest H2"
    s.sources[H3] = "honest H3"
    s.sources[P1] = "poison P1"
    key = 4000
    for src, base in ((H, 4001), (H2, 4021), (H3, 4041)):
        for i in range(20):
            s.honest(src, base + i, 1)
    # P1: one caught lie -> trust 333
    s.lie(P1, 4100, 2)
    # Phase C: pre-tainted truths (keys 5001-5010)
    for i in range(10):
        k = 5001 + i
        s.say(P1, k, tv(k), 3, 1)
        s.say(H, k, tv(k), 4, 1)
        s.world(k, tv(k))
    # Phase D: control truths, no pre-taint (keys 5011-5020)
    for i in range(10):
        k = 5011 + i
        s.say(H, k, tv(k), 5, 1)
        s.world(k, tv(k))
    # Phase E: rescue — H2, H3 assert pre-tainted keys 5001-5005
    for i in range(5):
        k = 5001 + i
        s.say(H2, k, tv(k), 6, 1)
        s.say(H3, k, tv(k), 6, 1)
    return s

def gen_l_des():
    s = Stream("L-DES",
               "Tripwire desensitization vs L: M farms 200 OKs (trust 995); control F (fresh) lies -> withhold; M lies -> INSTALL; WORLD -> PEND (trust must read 333); M corrects -> regime restored (995); M re-lies -> INSTALL (correct-and-re-lie cycle); then no-correct PEND + 17 OKs -> 900 -> lie INSTALLs (17-OK rebuild path). Verifies tripwire math empirically and measures both drip rates.",
               {"1": "honest farm", "2": "lie", "3": "novel truth probe (reads trust)",
                "4": "correction (states world value)"})
    M, F = 30, 31
    s.sources[M] = "long-honest M"
    s.sources[F] = "fresh F"
    for i in range(200):
        s.honest(M, 6001 + i, 1)
    # control: fresh source lies -> WITHHOLD (trust 500)
    s.say(F, 6301, fv(6301), 2, 0)
    # M lies on fresh key -> INSTALLs (trust 995 buys one pre-evidence install)
    s.say(M, 6302, fv(6302), 2, 0)
    s.world(6302, tv(6302))
    # probe: M novel truth -> WITHHOLD, warrant must read t=333
    s.say(M, 6303, tv(6303), 3, 1)
    # M corrects -> INSTALL, PEND expunged, regime restored
    s.say(M, 6302, tv(6302), 4, 1)
    # probe: trust back to ~995?
    s.say(M, 6304, tv(6304), 3, 1)
    # correct-and-re-lie cycle 2
    s.say(M, 6305, fv(6305), 2, 0)
    s.world(6305, tv(6305))
    s.say(M, 6305, tv(6305), 4, 1)
    # correct-and-re-lie cycle 3 (no probe, pure rate)
    s.say(M, 6306, fv(6306), 2, 0)
    s.world(6306, tv(6306))
    s.say(M, 6306, tv(6306), 4, 1)
    # no-correct path: lie, PEND stands, 17-OK rebuild, lie again
    s.say(M, 6307, fv(6307), 2, 0)
    s.world(6307, tv(6307))
    s.say(M, 6308, tv(6308), 3, 1)   # WITHHOLD expected, t=333
    for i in range(17):
        s.honest(M, 6310 + i, 1)     # rebuild to exactly 900
    s.say(M, 6327, fv(6327), 2, 0)   # INSTALL expected at t=900
    s.world(6327, tv(6327))
    s.say(M, 6328, tv(6328), 3, 1)   # WITHHOLD expected, t=333
    return s

def gen_l_frm():
    s = Stream("L-FRM",
               "Framing vs L: honest H farms 50 OKs; adversary forges SAYs under H's id (false claim -> forged; WORLD disagrees -> PEND; forged defiant restatement -> MAL). Then H's genuine novel truth, world-known truth, 17-OK rebuild, and a second framing cycle. Tests whether a forged MAL permanently burns an honest source.",
               {"1": "honest farm", "2": "FORGED claim under H id (false)",
                "3": "FORGED defiant restatement under H id",
                "4": "H genuine novel truth", "5": "H genuine world-known truth"})
    H = 40
    s.sources[H] = "honest H (framing victim)"
    for i in range(50):
        s.honest(H, 7001 + i, 1)
    # frame 1
    s.say(H, 7101, fv(7101), 2, 0)   # forged lie; installs on H's name
    s.world(7101, tv(7101))          # PEND on H's record
    s.say(H, 7101, fv(7101), 3, 0)   # forged defiance -> MAL
    s.say(H, 7102, tv(7102), 4, 1)   # genuine novel truth -> WITHHOLD?
    s.world(7103, tv(7103))          # world-first
    s.say(H, 7103, tv(7103), 5, 1)   # genuine world-known truth -> INSTALL?
    for i in range(17):
        s.honest(H, 7110 + i, 1)     # rebuild toward 900
    # frame 2 (persistent suppression)
    s.say(H, 7130, fv(7130), 2, 0)
    s.world(7130, tv(7130))
    s.say(H, 7130, fv(7130), 3, 0)
    s.say(H, 7131, tv(7131), 4, 1)
    return s


# ---- Task 4: cross-fork campaign ----

def gen_cross():
    s = Stream("CROSS",
               "Cross-fork adversarial campaign: honest baseline, Sybil ring (4 members x 3 claims), trust-farm betrayal (20 honest -> lie -> WORLD -> lie), trusted-source laundering (liar X caught; trusted T repeats X's lie), K-sized slow drip (1 lie + 6 honest x3). All forks observe the same stream; warrant quality compared.",
               {"1": "honest", "2": "sybil SAY", "3": "betrayal lie", "4": "laundered repeat",
                "5": "drip lie", "6": "drip honest"})
    H1, H2, H3 = 1, 2, 3
    B, T, X, D = 4, 5, 55, 6
    ring = [51, 52, 53, 54]
    s.sources[H1] = "honest H1"
    s.sources[H2] = "honest H2"
    s.sources[H3] = "honest H3"
    s.sources[B] = "betrayer B"
    s.sources[T] = "trusted T"
    s.sources[X] = "liar X"
    s.sources[D] = "dripper D"
    for m in ring:
        s.sources[m] = "sybil"
    # phase 0: honest baseline
    for i in range(10):
        s.honest(H1, 6001 + i, 1)
        s.honest(H2, 6011 + i, 1)
    for i in range(5):
        s.honest(H3, 6021 + i, 1)
    # phase 1: sybil ring, 3 claims x 4 SAYs
    for c in range(3):
        k = 6101 + c
        for m in ring:
            s.say(m, k, fv(k), 2, 0)
    # phase 2: betrayal — 20 honest, lie, WORLD, lie again
    for i in range(20):
        s.honest(B, 6201 + i, 6)
    s.say(B, 6301, fv(6301), 3, 0)
    s.world(6301, tv(6301))
    s.say(B, 6302, fv(6302), 3, 0)
    s.world(6302, tv(6302))
    # phase 3: laundering — X lies twice on 6391 (2nd restatement after WORLD
    # disagree earns an open LIE in S; low trust in K/L), then X originates a
    # lie on fresh key 6401; trusted T (10 solo honest) repeats X's lie verbatim.
    s.say(X, 6391, fv(6391), 3, 0)
    s.world(6391, tv(6391))
    s.say(X, 6391, fv(6391), 3, 0)
    s.world(6391, tv(6391))
    s.say(X, 6401, fv(6401), 3, 0)
    for i in range(10):
        s.honest(T, 6411 + i, 1)
    s.say(T, 6401, fv(6401), 4, 0)
    # phase 4: slow drip, K-sized (1 lie + 6 honest) x3
    for i in range(6):
        s.honest(D, 6501 + i, 6)
    lk = 6510
    for cyc in range(3):
        lk += 1
        s.say(D, lk, fv(lk), 5, 0)
        s.world(lk, tv(lk))
        for i in range(6):
            lk += 1
            s.honest(D, lk, 6)
    return s


GENS = [gen_v1_ring12, gen_v2_ring4, gen_v3_stagger, gen_v4_sleeper,
        gen_v5_onekey, gen_l_dot, gen_l_des, gen_l_frm, gen_cross]

if __name__ == "__main__":
    names = [g().write() for g in GENS]
    print("streams:", names)
