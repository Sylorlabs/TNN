#!/usr/bin/env python3
"""H1 prototype: practice-trace induction learner (decision-list rule learner).
Mirrors the design to be ported to Zag. Run with: h1proto.py chat
Protocol: banner line, then one input line -> exactly one 'A ...' reply line.
"""
import sys, os, re

# ---------------- constants ----------------
H = 64            # outcome window (ticks)
TOL = 10          # mismatch tolerance
SPLIT_GAP = 10    # min discriminative gap for a split
MAX_RULES = 256
DEATH_OUTCOME = -200
DEATH_WINDOW = 4  # (retained for reference; attribution is now death-tick only)
VOID_STABLE = 20  # consecutive ticks a unique void candidate must persist
STORM_PENALTY = 10  # outcome penalty per exposed tick (storm ACTIVE & unsheltered)
# Rationale: energy delta alone cannot teach storm safety because EAT (+30)
# masks storm damage (-4/tick). Without an exposure term, "eat through the
# storm" looks energetically fine and the outcome statistics can never favor
# sheltering. The penalty makes storm harm visible to the statistics, which is
# what the prereg's "storm safety must emerge from learned practice outcome
# statistics" requires. F scenarios never see an ACTIVE storm (storms at
# 900+), so the term is inert there.

# features (indices)
F_MOTE_DIR, F_MOTE_DIST, F_ONCELL, F_STORM, F_ZONE, F_SHELTER, \
    F_NCRYS, F_HASWARD, F_CRYDIR, F_WARDDIR, F_ENERGY = range(11)
NFEATS = 11

# feature value enums
MOTE_DIR = {"NONE": 0, "LEFT": 1, "RIGHT": 2, "HERE": 3}
MOTE_DIST = {"NONE": 0, "D0": 1, "D12": 2, "D36": 3, "D7P": 4}
ONCELL = {"EMPTY": 0, "MOTE": 1, "CRYSTAL": 2, "WARD": 3}
STORM = {"NONE": 0, "FAR": 1, "NEAR": 2, "SOON": 3, "ACTIVE": 4}
NCRYS = {"N0": 0, "N1": 1, "N2": 2}
ENERGY = {"LOW": 0, "OK": 1, "HIGH": 2}

# ---------------- OBS parsing (positional, grammar-based) ----------------
def parse_obs(line):
    # OBS t=.. pos=.. E=.. inv=.. storm_in=.. zone=.. shelter=.. motes=.. crystals=.. ward=..
    f = line.split(" ")
    assert f[0] == "OBS" and len(f) == 11, line[:60]
    def val(i):
        return f[i].split("=", 1)[1]
    t = int(val(1)); pos = int(val(2)); E = int(val(3))
    inv = [int(x) for x in val(4).split(",")]
    si = val(5)
    zone = int(val(6)); shelter = int(val(7))
    motes = []
    for tok in val(8).split(","):
        p, s = tok.split(":")
        p = int(p)
        if s == "a":
            motes.append((p, True, 0))
        else:
            motes.append((p, False, int(s[1:])))
    cr = val(9)
    crystals = [] if cr == "none" else [int(x) for x in cr.split(",")]
    w = val(10)
    wards = [] if w == "none" else [int(x) for x in w.split(",")]
    return dict(t=t, pos=pos, E=E, inv=inv, si=si, zone=zone,
                shelter=shelter, motes=motes, crystals=crystals, wards=wards)

def storm_bucket(si):
    if si == "ACTIVE":
        return STORM["ACTIVE"]
    if si == "none":
        return STORM["NONE"]
    n = int(si)
    if n > 30:
        return STORM["FAR"]
    if n >= 6:
        return STORM["NEAR"]
    return STORM["SOON"]

# ---------------- learner ----------------
class Rule:
    __slots__ = ("conds", "action", "n", "total", "deaths", "seed", "rid", "_mismatch")
    def __init__(self, conds, action, pred, rid, seed=False):
        # conds: list of (feat, op, value); op 0='=', 1='!='
        self.conds = list(conds)
        self.action = action
        self.n = 1
        self.total = pred  # seed hypothesis
        self.deaths = 0
        self.seed = seed
        self.rid = rid
        self._mismatch = None
    def pred(self):
        return self.total / self.n
    def matches(self, feats):
        for (f, op, v) in self.conds:
            if op == 0:
                if feats[f] != v:
                    return False
            else:
                if feats[f] == v:
                    return False
        return True

class H1:
    def __init__(self):
        self.rules = []
        self.next_rid = 0
        self.void_a = None      # inferred left void cell
        self.mseen = [0]*24
        self.triples = []       # (feats tuple, action, outcome or None)
        self.pending = []       # (deadline_tick, E_fire, [rule_ids], triple_idx)
        self.ep_idx = 0         # episodes seen
        self.training = True
        self.in_episode = False
        self.card_lines = []
        self.ep_len = 0
        self.last_t = None
        self.last_exec_rids = []  # (tick, [rids]) for death attribution
        self.visited = [0]*24     # cells the learner has safely occupied
        self.evidence = [0]*24    # cells with any occupancy evidence
        self._void_cand = None
        self._void_stable = 0
        self.exposed_ticks = []  # ticks where storm ACTIVE and unsheltered
        self.tracefile = os.environ.get("H1_TRACEFILE")
        self._seed_rules()

    # ---------- seeding (Sessions 2-4 procedures) ----------
    def add_rule(self, conds, action, pred, seed=False):
        r = Rule(conds, action, pred, self.next_rid, seed)
        self.next_rid += 1
        self.rules.append(r)
        return r

    def _seed_rules(self):
        EQ, NE = 0, 1
        M, D, O, S, Z, SH, NC, HW, CD, WD, EN = range(11)
        # S2 forage
        self.add_rule([(O, EQ, ONCELL["MOTE"])], 2, 30, seed=True)
        self.add_rule([(M, EQ, MOTE_DIR["LEFT"])], 0, -1, seed=True)
        self.add_rule([(M, EQ, MOTE_DIR["RIGHT"])], 1, -1, seed=True)
        # S3 ward-build
        self.add_rule([(O, EQ, ONCELL["CRYSTAL"]), (NC, NE, NCRYS["N2"]),
                       (WD, EQ, 0)], 3, -1, seed=True)
        self.add_rule([(NC, EQ, NCRYS["N2"]), (HW, EQ, 0), (WD, EQ, 0)], 5, -1, seed=True)
        self.add_rule([(HW, EQ, 1), (WD, EQ, 0)], 4, -1, seed=True)
        self.add_rule([(CD, EQ, 1), (NC, NE, NCRYS["N2"]), (WD, EQ, 0),
                       (S, NE, STORM["NONE"])], 0, -1, seed=True)
        self.add_rule([(CD, EQ, 2), (NC, NE, NCRYS["N2"]), (WD, EQ, 0),
                       (S, NE, STORM["NONE"])], 1, -1, seed=True)
        # S4 shelter: go to ward at NEAR/SOON/ACTIVE; wait on ward
        for wv, act in ((1, 0), (2, 1)):
            for sb in (STORM["NEAR"], STORM["SOON"], STORM["ACTIVE"]):
                self.add_rule([(WD, EQ, wv), (S, EQ, sb)], act, -1, seed=True)
        for sb in (STORM["NEAR"], STORM["SOON"], STORM["ACTIVE"]):
            self.add_rule([(O, EQ, ONCELL["WARD"]), (S, EQ, sb)], 6, 0, seed=True)

    # ---------- abstraction ----------
    def _reach(self, cell, pos):
        if self.void_a is not None:
            return (cell < self.void_a) == (pos < self.void_a)
        return abs(cell - pos) <= 2

    def abstract(self, o):
        pos = o["pos"]
        best = None; bestd = None
        for (p, act, dor) in o["motes"]:
            if not act:
                continue
            if not self._reach(p, pos):
                continue
            d = abs(p - pos)
            if bestd is None or d < bestd:
                bestd = d; best = p
        if best is None:
            mote_dir = MOTE_DIR["NONE"]; mote_dist = MOTE_DIST["NONE"]
        elif bestd == 0:
            mote_dir = MOTE_DIR["HERE"]; mote_dist = MOTE_DIST["D0"]
        else:
            mote_dir = MOTE_DIR["LEFT"] if best < pos else MOTE_DIR["RIGHT"]
            mote_dist = MOTE_DIST["D12"] if bestd <= 2 else (MOTE_DIST["D36"] if bestd <= 6 else MOTE_DIST["D7P"])
        on = ONCELL["EMPTY"]
        if any(p == pos and a for (p, a, d) in o["motes"]):
            on = ONCELL["MOTE"]
        elif pos in o["crystals"]:
            on = ONCELL["CRYSTAL"]
        elif pos in o["wards"]:
            on = ONCELL["WARD"]
        storm = storm_bucket(o["si"])
        ncr = min(sum(1 for c in o["inv"] if c == 0), 2)
        hasw = 1 if 3 in o["inv"] else 0
        cdir = 0; cbest = None; cbestd = None
        if ncr < 2:
            for c in o["crystals"]:
                if not self._reach(c, pos):
                    continue
                d = abs(c - pos)
                if cbestd is None or d < cbestd:
                    cbestd = d; cbest = c
            if cbest is not None:
                cdir = 3 if cbestd == 0 else (1 if cbest < pos else 2)
        wdir = 0
        if o["wards"]:
            w = o["wards"][0]
            wdir = 3 if w == pos else (1 if w < pos else 2)
        E = o["E"]
        en = ENERGY["LOW"] if E < 40 else (ENERGY["HIGH"] if E > 150 else ENERGY["OK"])
        return (mote_dir, mote_dist, on, storm, o["zone"], o["shelter"],
                ncr, hasw, cdir, wdir, en)

    # ---------- void inference ----------
    # The void is an adjacent cell pair that never hosts motes. Evidence for a
    # cell = a mote was seen there, the learner safely stood there, or a
    # crystal/ward was seen there. The void is the unique adjacent pair with
    # zero evidence and evidence on both sides. The uniqueness requirement is
    # conservative: it commits only after the same unique candidate persists
    # for VOID_STABLE consecutive ticks, and self-corrects if the learner ever
    # survives occupying an inferred void cell.
    def void_update(self, o):
        pos = o["pos"]
        self.visited[pos] = 1
        for c in o["crystals"]:
            self.evidence[c] = 1
        for w in o["wards"]:
            self.evidence[w] = 1
        for (p, a, d) in o["motes"]:
            self.evidence[p] = 1
        if self.void_a is not None:
            # self-correction: occupancy evidence inside an inferred void cell
            # refutes the inference (motes/crystals/wards never occur in the
            # true void; surviving there refutes it too). Reset and re-infer.
            if (self.evidence[self.void_a] or self.evidence[self.void_a + 1]):
                self.void_a = None
                self._void_cand = None
                self._void_stable = 0
            return
        cands = []
        for c in range(23):
            if self.evidence[c] == 0 and self.evidence[c+1] == 0:
                if any(self.evidence[:c]) and any(self.evidence[c+2:]):
                    cands.append(c)
        if len(cands) == 1 and cands[0] == self._void_cand:
            self._void_stable += 1
        elif len(cands) == 1:
            self._void_cand = cands[0]
            self._void_stable = 1
        else:
            self._void_cand = None
            self._void_stable = 0
        if self._void_stable >= VOID_STABLE:
            self.void_a = self._void_cand

    # ---------- episode boundary ----------
    def episode_start(self):
        self.in_episode = True
        self.pending = []
        self.last_t = None
        self.last_exec_rids = []
        self.ep_len = 0
        # The void is per-scenario: reset inference each episode. Carrying a
        # stale void_a into a new layout makes unreachable motes look
        # reachable and lures the learner into the true void.
        self.void_a = None
        self.visited = [0]*24
        self.evidence = [0]*24
        self._void_cand = None
        self._void_stable = 0
        self.exposed_ticks = []
        if self.card_lines:
            m = re.search(r"episode (\d+) ticks", self.card_lines[0])
            if m:
                self.ep_len = int(m.group(1))

    def rules_by_id(self, rid):
        for r in self.rules:
            if r.rid == rid:
                return r
        return None

    def episode_end(self, died):
        # (narrow death attribution as above)
        if died:
            if self.last_exec_rids:
                death_rids = self.last_exec_rids[-1][1]
                for rid in death_rids:
                    r = self.rules_by_id(rid)
                    if r:
                        r.deaths += 1
                        r.n += 1
                        r.total += DEATH_OUTCOME
                if self.pending:
                    ti_max = max(ti for (_, _, _, ti) in self.pending)
                    self.triples[ti_max] = (self.triples[ti_max][0],
                                            self.triples[ti_max][1], DEATH_OUTCOME)
        self.pending = []
        self.in_episode = False
        self.card_lines = []  # cards belong to the episode that just ended
        if self.training:
            self.refine()
        self.ep_idx += 1
        if self.training and self.ep_idx == 24:
            self.training = False
            self.refine()
            self.rules = [r for r in self.rules if r.seed or r.n > 1]

    def _exposed_in(self, t0, t1):
        # count exposed ticks e with t0 < e <= t1
        c = 0
        for e in self.exposed_ticks:
            if e > t0 and e <= t1:
                c += 1
        return c

    # ---------- conflict resolution (prereg: zero-death filter, then max
    # predicted energy delta, then lowest action) ----------
    def _resolve(self, firing, vetoed):
        firing = [r for r in firing if r.action not in vetoed]
        if not firing:
            return 6, []
        if any(r.deaths == 0 for r in firing):
            firing = [r for r in firing if r.deaths == 0]
        best = None
        for r in firing:
            if best is None:
                best = r
            elif r.total * best.n > best.total * r.n:
                best = r
        cands = [r for r in firing if r.total * best.n == best.total * r.n]
        action = min(r.action for r in cands)
        proposers = sorted(r.rid for r in firing
                           if r.action == action and r.total * best.n == best.total * r.n)
        return action, proposers

    # ---------- per-tick decision ----------
    def decide(self, o):
        self.void_update(o)
        feats = self.abstract(o)
        pos = o["pos"]
        t, E = o["t"], o["E"]
        if o["si"] == "ACTIVE" and o["shelter"] == 0:
            self.exposed_ticks.append(t)
        for (dl, Ef, rids, ti) in list(self.pending):
            if dl == t:
                out = (E - Ef) - STORM_PENALTY * self._exposed_in(dl - H, dl)
                for rid in rids:
                    r = self.rules_by_id(rid)
                    if r:
                        pred_before = r.pred()
                        r.n += 1
                        r.total += out
                        if abs(out - pred_before) > TOL:
                            r._mismatch = ti
                self.triples[ti] = (self.triples[ti][0], self.triples[ti][1], out)
                self.pending.remove((dl, Ef, rids, ti))
        firing = [r for r in self.rules if r.matches(feats)]
        vetoed = set()
        action, proposers = self._resolve(firing, vetoed)
        # Step veto: never step into an inferred void cell. If the chosen move
        # is vetoed, re-resolve excluding it; fall back to WAIT if no move is
        # safe. This is reachability machinery (uses the inferred void), not a
        # handcrafted avoidance policy: it blocks only steps into void cells.
        while action in (0, 1) and self.void_a is not None:
            dest = pos + (-1 if action == 0 else 1)
            if dest == self.void_a or dest == self.void_a + 1:
                vetoed.add(action)
                action, proposers = self._resolve(firing, vetoed)
            else:
                break
        if action in (0, 1) and action in vetoed:
            action, proposers = 6, []
        ti = len(self.triples)
        self.triples.append((feats, action, None))
        self.pending.append((t + H, E, proposers[:8], ti))
        self.last_exec_rids.append((t, proposers))
        if len(self.last_exec_rids) > DEATH_WINDOW:
            self.last_exec_rids.pop(0)
        if self.tracefile:
            with open(self.tracefile, "a") as f:
                f.write(f"{t} {action} [{','.join(str(x) for x in proposers)}]\n")
        if os.environ.get("H1_FIRELOG"):
            with open(os.environ["H1_FIRELOG"], "a") as f:
                f.write(f"t={t} pos={pos} act={action} feats={feats} voida={self.void_a}\n")
                for r in firing:
                    f.write(f"  rid={r.rid} act={r.action} deaths={r.deaths} "
                            f"mean={r.pred():.1f} n={r.n} "
                            f"conds={r.conds}\n")
        return action

    # ---------- splitter ----------
    def refine(self):
        for r in list(self.rules):
            ti = r._mismatch
            if ti is None:
                continue
            r._mismatch = None
            if len(r.conds) >= 4:
                continue
            self._try_split(r, ti)
        while len(self.rules) > MAX_RULES:
            cands = [x for x in self.rules if not x.seed]
            if not cands:
                break
            cands.sort(key=lambda x: (x.n, -x.rid))
            self.rules.remove(cands[0])

    def _try_split(self, r, ti):
        feats_m, act_m, _ = self.triples[ti]
        used = set(f for (f, op, v) in r.conds)
        sup = [(f, o) for (f, a, o) in self.triples
               if a == r.action and o is not None and r.matches(f)]
        if len(sup) < 4:
            return
        best_f = None; best_gap = 0
        for fidx in range(NFEATS):
            if fidx in used:
                continue
            groups = {}
            for (f, o) in sup:
                groups.setdefault(f[fidx], []).append(o)
            if len(groups) < 2:
                continue
            maj_v = max(groups, key=lambda v: len(groups[v]))
            g_mm = groups.get(feats_m[fidx], [])
            g_mj = groups[maj_v]
            if not g_mm or feats_m[fidx] == maj_v:
                continue
            gap = abs(sum(g_mm)/len(g_mm) - sum(g_mj)/len(g_mj))
            if gap > best_gap:
                best_gap = gap; best_f = fidx
        if best_f is None or best_gap <= SPLIT_GAP:
            return
        c1 = r.conds + [(best_f, 0, feats_m[best_f])]
        c2 = r.conds + [(best_f, 1, feats_m[best_f])]
        def stats(conds):
            n = 0; tot = 0
            rr = Rule(conds, r.action, 0, -1)
            for (f, a, o) in self.triples:
                if a == r.action and o is not None and rr.matches(f):
                    n += 1; tot += o
            return n, tot
        n1, t1 = stats(c1); n2, t2 = stats(c2)
        if n1 == 0 or n2 == 0:
            return
        parent_deaths = r.deaths
        r.conds = c1; r.n = n1; r.total = t1; r.deaths = parent_deaths
        r2 = Rule(c2, r.action, 0, self.next_rid)
        r2.n = n2; r2.total = t2
        # Death history is inherited by both children: a refined killer is
        # still a killer until its own record proves otherwise. (Without this,
        # splits laundered death records back to zero and killer rules re-fired.)
        r2.deaths = parent_deaths
        self.next_rid += 1
        self.rules.append(r2)

    # ---------- P1 ----------
    def answer_p1(self):
        ep = 0; storms = []; preplaced = False
        if len(self.card_lines) >= 1:
            m = re.search(r"episode (\d+) ticks", self.card_lines[0])
            if m:
                ep = int(m.group(1))
        if len(self.card_lines) >= 3:
            storms = [int(x) for x in re.findall(r"\d+", self.card_lines[2])]
        if len(self.card_lines) >= 4:
            preplaced = ";" in self.card_lines[3]
        inep = [s for s in storms if s < ep]
        if not inep:
            return "1"
        skills = []
        if inep[0] > 30:
            skills.append(1)
        if not preplaced:
            skills.append(2)
        skills.append(3)
        skills.append(1)
        for _ in inep[1:]:
            skills.append(3)
            skills.append(1)
        return ",".join(str(s) for s in skills)

    def dump_rules(self, path):
        names = ["MOTE_DIR", "MOTE_DIST", "ONCELL", "STORM", "ZONE", "SHELTER",
                 "NCRYS", "HASWARD", "CRYDIR", "WARDDIR", "ENERGY"]
        with open(path, "w") as f:
            for r in self.rules:
                cs = " & ".join(f"{names[ff]}{'=' if op==0 else '!='}{v}"
                                for (ff, op, v) in r.conds)
                f.write(f"rid={r.rid} act={r.action} n={r.n} mean={r.pred():.1f} "
                        f"deaths={r.deaths} seed={r.seed} [{cs}]\n")

    # ---------- main chat loop ----------
    def handle(self, line):
        if line.startswith("OBS "):
            if not self.in_episode:
                self.episode_start()
            o = parse_obs(line)
            a = self.decide(o)
            self.last_t = o["t"]
            return f"A {a}"
        if line.startswith("CARD "):
            if self.in_episode:
                died = not (self.ep_len and self.last_t == self.ep_len - 1)
                self.episode_end(died)
            # episode_end cleared card_lines; accumulate this episode's cards
            self.card_lines.append(line)
            return "A card noted"
        if "Which sub-skills" in line:
            ans = "A " + self.answer_p1()
            self.card_lines = []  # consume the cards; next episode starts fresh
            if self.in_episode:
                self.episode_end(died=False)
            return ans
        if self.in_episode:
            died = not (self.ep_len and self.last_t == self.ep_len - 1)
            self.episode_end(died)
            self.card_lines = []
        return "A noted"


def main():
    assert len(sys.argv) > 1 and sys.argv[1] == "chat"
    sys.stdout.write("H1 practice-trace induction learner ready\n")
    sys.stdout.flush()
    h = H1()
    try:
        for line in sys.stdin:
            line = line.rstrip("\n")
            if not line:
                continue
            sys.stdout.write(h.handle(line) + "\n")
            sys.stdout.flush()
    except BrokenPipeError:
        pass
    finally:
        dp = os.environ.get("H1_DUMPRULES")
        if dp:
            h.dump_rules(dp)

if __name__ == "__main__":
    main()
