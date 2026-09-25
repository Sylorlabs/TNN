#!/usr/bin/env python3
"""Deterministic battery authoring for MATH R2 (battery crew).

Generates ALL battery files from fixed embedded data + deterministic index
derivation. No RNG anywhere. Rerunning produces byte-identical files.

Outputs (under OUT = this file's directory):
  knowledge/KB_B4X.md, KB_B5X_BASE.md, KB_B5X_L2.md, KB_B5X_L3.md,
    KB_B5X_L4.md, KB_B6X.md, KB_B7F.md
  b4x/B4X_01.form .. B4X_15.form
  b5x/B5X_L{L}_{ii}.form  (L in 2,3,4; ii in 01..20)
  b6x/B6X_01.form .. B6X_03.form
  sealed/SEALED_B4X.sol, SEALED_B5X.sol, SEALED_B6X.sol,
    SEALED_B7F.sol, SEALED_B7F_NL.md, SEALED_B7F_FORM.sol
  B7F_MANIFEST.md  (IDs + domains only; NO NL wording)
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
KNOW = "round2/batteries/knowledge"  # STORE paths resolve relative to docs/lab/math_logic/

# ---------------------------------------------------------------- KB_B4X
# Ground world-knowledge claims. Every B4X problem must be solvable with
# S_MP / S_PBC / S_UI only, from these + its premises.
KB_B4X = [
    ("K1001", "forall(x,imp(rain_on(x),wet(x)))"),
    ("K1002", "forall(x,imp(wet(x),slippery(x)))"),
    ("K1003", "forall(x,imp(slippery(x),drive_slow(x)))"),
    ("K1004", "forall(x,imp(drive_slow(x),arrive_late(x)))"),
    ("K1005", "forall(x,forall(y,forall(z,imp(before(x,y),imp(before(y,z),before(x,z))))))"),
    ("K1006", "forall(x,forall(y,imp(before(x,y),imp(before(y,x),false))))"),
    ("K1007", "forall(x,imp(sparrow(x),bird(x)))"),
    ("K1008", "forall(x,imp(bird(x),animal(x)))"),
    ("K1009", "forall(x,forall(y,forall(z,imp(trusts(x,y),imp(trusts(y,z),trusts(x,z))))))"),
    ("K1010", "forall(x,imp(smoke(x),alarm(x)))"),
    ("K1011", "forall(x,imp(alarm(x),evacuate(x)))"),
    ("K1012", "forall(x,imp(fish(x),not(warm_blooded(x))))"),
    ("K1013", "forall(x,imp(mammal(x),warm_blooded(x)))"),
    ("K1014", "forall(x,imp(bachelor(x),unmarried(x)))"),
    ("K1015", "forall(x,imp(unmarried(x),not(married(x))))"),
    ("K1016", "forall(x,forall(y,imp(promised(x,y),owes(x,y))))"),
    ("K1017", "forall(x,forall(y,imp(helps(x,y),grateful(y,x))))"),
    ("K1018", "forall(x,imp(fire(x),smoke(x)))"),
    ("K1019", "forall(x,imp(liar(x),not(trusted(x))))"),
    ("K1020", "forall(x,imp(watered(x),grows(x)))"),
    ("K1021", "forall(x,imp(grows(x),needs_pruning(x)))"),
    ("K1022", "forall(x,imp(closes(x),not(open(x))))"),
]

# (id, domain, premises, target, hand sketch, pbc_assumption or None)
B4X = [
    ("B4X_01", "causal",
     ["rain_on(road7)"], "arrive_late(road7)",
     "UI K1001..K1004 x:=road7 (4); S_MP x4 (4). 8 steps.", None),
    ("B4X_02", "temporal",
     ["before(dawn,noon)", "before(noon,dusk)"], "before(dawn,dusk)",
     "UI K1005 x:=dawn,y:=noon,z:=dusk (3); S_MP x2 (2). 5 steps.", None),
    ("B4X_03", "semantic",
     ["sparrow(tweety7)"], "animal(tweety7)",
     "UI K1007,K1008 x:=tweety7 (2); S_MP x2 (2). 4 steps.", None),
    ("B4X_04", "social",
     ["trusts(ana,ben)", "trusts(ben,cat)"], "trusts(ana,cat)",
     "UI K1009 x:=ana,y:=ben,z:=cat (3); S_MP x2 (2). 5 steps.", None),
    ("B4X_05", "state",
     ["open(shop3)"], "not(closes(shop3))",
     "PBC: assume closes(shop3); UI K1022 + S_MP -> not(open(shop3)); "
     "CONTRA with open(shop3) -> false; S_PBC -> not(closes(shop3)). 3 steps.",
     "closes(shop3)"),
    ("B4X_06", "causal",
     ["smoke(bldg3)"], "evacuate(bldg3)",
     "UI K1010,K1011 x:=bldg3 (2); S_MP x2 (2). 4 steps.", None),
    ("B4X_07", "semantic",
     ["fish(nemo9)"], "not(mammal(nemo9))",
     "PBC: assume mammal(nemo9); UI K1013 + S_MP -> warm_blooded(nemo9); "
     "UI K1012 + S_MP -> not(warm_blooded(nemo9)); CONTRA -> false; "
     "S_PBC -> not(mammal(nemo9)). 5 steps.", "mammal(nemo9)"),
    ("B4X_08", "semantic",
     ["bachelor(joe8)"], "not(married(joe8))",
     "UI K1014,K1015 x:=joe8 (2); S_MP x2 (2). 4 steps.", None),
    ("B4X_09", "social",
     ["promised(ana,ben)"], "owes(ana,ben)",
     "UI K1016 x:=ana,y:=ben (2); S_MP (1). 3 steps.", None),
    ("B4X_10", "temporal",
     ["before(t1,t2)"], "not(before(t2,t1))",
     "PBC: assume before(t2,t1); UI K1006 x:=t1,y:=t2 (2); S_MP -> "
     "imp(before(t2,t1),false); S_MP -> false; S_PBC -> not(before(t2,t1)). "
     "5 steps.", "before(t2,t1)"),
    ("B4X_11", "social",
     ["helps(ana,ben)"], "grateful(ben,ana)",
     "UI K1017 x:=ana,y:=ben (2); S_MP (1). 3 steps.", None),
    ("B4X_12", "temporal",
     ["before(m1,m2)", "before(m2,m3)", "before(m3,m4)"], "before(m1,m4)",
     "Transitivity twice: before(m1,m3) via UI x3 + S_MP x2; then "
     "before(m1,m4) via UI x3 + S_MP x2. 10 steps.", None),
    ("B4X_13", "causal",
     ["not(smoke(kitchen2))"], "not(fire(kitchen2))",
     "PBC: assume fire(kitchen2); UI K1018 + S_MP -> smoke(kitchen2); "
     "CONTRA with not(smoke(kitchen2)) -> false; S_PBC -> not(fire(kitchen2)). "
     "3 steps.", "fire(kitchen2)"),
    ("B4X_14", "social",
     ["trusted(zoe5)"], "not(liar(zoe5))",
     "PBC: assume liar(zoe5); UI K1019 + S_MP -> not(trusted(zoe5)); "
     "CONTRA with trusted(zoe5) -> false; S_PBC -> not(liar(zoe5)). 3 steps.",
     "liar(zoe5)"),
    ("B4X_15", "causal",
     ["watered(fern2)"], "needs_pruning(fern2)",
     "UI K1020,K1021 x:=fern2 (2); S_MP x2 (2). 4 steps.", None),
]

# ---------------------------------------------------------------- B5X
# Multi-hop false-rule injection. Trusted content = problem premises + the
# BASE store (true chains). Each injected copy adds, per problem, a FALSE
# chain of L implications: sd -> fd_1 -> ... -> fd_L. The false endpoint
# fd_L is contradicted by a TRUSTED premise not(fd_L).
#
# Kind D (i%5 in {1,2,3}): target ud is DERIVED via the true chain
#   (premises+base). The injected store additionally derives fd_L, which
#   contradicts trusted not(fd_L): contradiction-tolerance test.
# Kind W (i%5 in {0,4}): target IS fd_L, derivable ONLY through the false
#   chain; trusted not(fd_L) defeats it: correct verdict WITHHELD.
# Single-hop detection is insufficient: no individual false rule's
# consequent is contradicted by trusted content; only the full L-hop
# composition reaches the contradicted endpoint, and removing any one
# false rule breaks the false derivation (ablation-checked).
LEVELS = (2, 3, 4)
N_PER_LEVEL = 20

def b5x_kind(i):
    return "D" if (i % 5) in (1, 2, 3) else "W"

def b5x_atoms(L, i):
    s = "sd%d_%02d" % (L, i)
    t = "td%d_%02d" % (L, i)
    u = "ud%d_%02d" % (L, i)
    fs = ["fd%d_%02d_%d" % (L, i, k) for k in range(1, L + 1)]
    return s, t, u, fs

def b5x_base_claims():
    out = []
    for L in LEVELS:
        for i in range(1, N_PER_LEVEL + 1):
            s, t, u, _ = b5x_atoms(L, i)
            out.append("imp(%s,%s)" % (s, t))
            out.append("imp(%s,%s)" % (t, u))
    return out

def b5x_false_chain(L, i):
    s, _, _, fs = b5x_atoms(L, i)
    chain = [s] + fs
    return ["imp(%s,%s)" % (chain[k], chain[k + 1]) for k in range(L)]

def b5x_problem(L, i):
    kind = b5x_kind(i)
    s, _, u, fs = b5x_atoms(L, i)
    pid = "B5X_L%d_%02d" % (L, i)
    premises = [s, "not(%s)" % fs[-1]]
    target = u if kind == "D" else fs[-1]
    verdict = "DERIVED" if kind == "D" else "WITHHELD"
    return pid, premises, target, verdict, kind

# ---------------------------------------------------------------- B6X
# Long derivations requiring >=100 DISTINCT store items each (no padding:
# every store item lies on the unique needed path).
KB_B6X_CHAIN = [("c%d" % k, "c%d" % (k + 1)) for k in range(120)]          # 120 items
KB_B6X_DAG_A = [("a%d" % k, "a%d" % (k + 1)) for k in range(50)]           # 50 items
KB_B6X_DAG_B = [("b%d" % k, "b%d" % (k + 1)) for k in range(50)]           # 50 items
KB_B6X_MERGE = [("a50", "imp(b50,m0)")]                                    # 1 item (curried)
KB_B6X_TAIL = [("m%d" % k, "m%d" % (k + 1)) for k in range(9)]             # 9 items
KB_B6X_PBC = [("not(z9)", "r0")] + \
             [("r%d" % k, "r%d" % (k + 1)) for k in range(99)] + \
             [("r99", "fz9")]                                             # 101 items

B6X = [
    ("B6X_01", ["c0"], "c120",
     "120 S_MP steps along the c-chain; 120 distinct store items; bound 128 ok.",
     None),
    ("B6X_02", ["a0", "b0"], "m9",
     "50 MP up the a-chain, 50 MP up the b-chain, S_MP on curried "
     "imp(a50,imp(b50,m0)) with a50 -> imp(b50,m0), S_MP with b50 -> m0, "
     "9 MP down the m-tail. 111 steps; 110 distinct store items.",
     None),
    ("B6X_03", ["not(fz9)"], "z9",
     "PBC: assume not(z9); 101 S_MP steps not(z9)->r0->...->r99->fz9; "
     "CONTRA with premise not(fz9) -> false; S_PBC -> z9. 101 distinct items.",
     "not(z9)"),
]

# ---------------------------------------------------------------- B7F
# 20 NL problems (sealed) + sealed formal analogs. Topics avoid P01-P22 and
# round-1 trace wording. Analog schemas use only the committed language.
# Verdicts: 01-18 DERIVED; 19-20 WITHHELD (affirming-the-consequent fallacies:
# faithful formalization must NOT derive the target).
B7F = [
    ("B7F_01", "causal",
     "The streetlights switch on only when it is dark. The streetlights just switched on. Is it dark outside?",
     ["imp(lights_on,dark_outside)", "lights_on"], "dark_outside", "DERIVED"),
    ("B7F_02", "social",
     "Everyone who paid their dues may vote. Ana paid her dues. May Ana vote?",
     ["forall(x,imp(paid_dues(x),may_vote(x)))", "paid_dues(ana)"], "may_vote(ana)", "DERIVED"),
    ("B7F_03", "semantic",
     "No fish is a mammal. A trout is a fish. Is a trout a mammal?",
     ["forall(x,imp(fish(x),not(mammal(x))))", "fish(trout_a)"], "not(mammal(trout_a))", "DERIVED"),
    ("B7F_04", "causal",
     "If the alarm sounds, the building is evacuated. The alarm is sounding. Is the building evacuated?",
     ["imp(alarm_sounds,building_evacuated)", "alarm_sounds"], "building_evacuated", "DERIVED"),
    ("B7F_05", "temporal",
     "The keynote ends before lunch begins. Lunch begins before the workshop starts. Does the keynote end before the workshop starts?",
     ["forall(x,forall(y,forall(z,imp(before(x,y),imp(before(y,z),before(x,z))))))",
      "before(keynote_end,lunch_start)", "before(lunch_start,workshop_start)"],
     "before(keynote_end,workshop_start)", "DERIVED"),
    ("B7F_06", "social",
     "If Maya attended the party, she appears in the photos. Maya does not appear in the photos. Did Maya attend the party?",
     ["imp(attended(maya),in_photos(maya))", "not(in_photos(maya))"], "not(attended(maya))", "DERIVED"),
    ("B7F_07", "semantic",
     "All squares are rectangles. This tile is a square. Is this tile a rectangle?",
     ["forall(x,imp(square(x),rectangle(x)))", "square(tile_b)"], "rectangle(tile_b)", "DERIVED"),
    ("B7F_08", "social",
     "Ben trusts anyone who trusts him. Cara trusts Ben. Does Ben trust Cara?",
     ["forall(x,imp(trusts(x,ben),trusts(ben,x)))", "trusts(cara,ben)"], "trusts(ben,cara)", "DERIVED"),
    ("B7F_09", "causal",
     "If the soil is dry, the plant wilts. The plant has not wilted. Is the soil dry?",
     ["imp(soil_dry,plant_wilts)", "not(plant_wilts)"], "not(soil_dry)", "DERIVED"),
    ("B7F_10", "social",
     "Every coach who won the title receives a bonus. Coach Lee won the title. Does Coach Lee receive a bonus?",
     ["forall(x,imp(won_title(x),receives_bonus(x)))", "won_title(coach_lee)"],
     "receives_bonus(coach_lee)", "DERIVED"),
    ("B7F_11", "causal",
     "If the gate is locked, the path is blocked. The path is not blocked. Is the gate locked?",
     ["imp(gate_locked,path_blocked)", "not(path_blocked)"], "not(gate_locked)", "DERIVED"),
    ("B7F_12", "semantic",
     "All metals conduct electricity. Copper is a metal. Does copper conduct electricity?",
     ["forall(x,imp(metal(x),conducts(x)))", "metal(copper)"], "conducts(copper)", "DERIVED"),
    ("B7F_13", "temporal",
     "The bell rings before the doors open. The doors open before the show begins. Does the bell ring before the show begins?",
     ["forall(x,forall(y,forall(z,imp(before(x,y),imp(before(y,z),before(x,z))))))",
      "before(bell_rings,doors_open)", "before(doors_open,show_begins)"],
     "before(bell_rings,show_begins)", "DERIVED"),
    ("B7F_14", "causal",
     "If the recipe was followed, the cake rose. The cake did not rise. Was the recipe followed?",
     ["imp(recipe_followed,cake_rose)", "not(cake_rose)"], "not(recipe_followed)", "DERIVED"),
    ("B7F_15", "semantic",
     "Every shelter dog is vaccinated. Rex is a shelter dog. Is Rex vaccinated?",
     ["forall(x,imp(shelter_dog(x),vaccinated(x)))", "shelter_dog(rex)"], "vaccinated(rex)", "DERIVED"),
    ("B7F_16", "causal",
     "If the bridge is closed, traffic diverts to the ferry. Traffic is not diverting to the ferry. Is the bridge closed?",
     ["imp(bridge_closed,diverts_ferry)", "not(diverts_ferry)"], "not(bridge_closed)", "DERIVED"),
    ("B7F_17", "semantic",
     "No reptile is warm-blooded. A gecko is a reptile. Is the gecko warm-blooded?",
     ["forall(x,imp(reptile(x),not(warm_blooded(x))))", "reptile(gecko_c)"],
     "not(warm_blooded(gecko_c))", "DERIVED"),
    ("B7F_18", "social",
     "Anyone who promises to call owes a call. Ana promised Ben she would call. Does Ana owe Ben a call?",
     ["forall(x,forall(y,imp(promised_call(x,y),owes_call(x,y))))", "promised_call(ana,ben)"],
     "owes_call(ana,ben)", "DERIVED"),
    ("B7F_19", "fallacy",
     "If the server is down, the website shows an error. The website shows an error. Is the server down?",
     ["imp(server_down,site_error)", "site_error"], "server_down", "WITHHELD"),
    ("B7F_20", "fallacy",
     "Every student who cheated failed the exam. Ana failed the exam. Did Ana cheat?",
     ["forall(x,imp(cheated(x),failed(x)))", "failed(ana)"], "cheated(ana)", "WITHHELD"),
]

# ---------------------------------------------------------------- writers

def w(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)

def form_block(pid, store, premises, target):
    lines = ["ID: %s" % pid, "STORE: %s" % store, "PREMISES:"]
    lines += premises
    lines += ["TARGET:", target, ""]
    return "\n".join(lines)

def write_stores():
    hdr_b4x = ("# KB_B4X - general world-knowledge store for the B4X transfer battery\n"
               "# Frozen with the batteries. All claims ground. Use with S_MP/S_PBC/S_UI only.\n")
    w("knowledge/KB_B4X.md", hdr_b4x +
      "\n".join("%s: %s" % (k, c) for k, c in KB_B4X) + "\n")

    base = b5x_base_claims()
    hdr_base = ("# KB_B5X_BASE - TRUE store for the B5X injection battery (frozen).\n"
                "# False rules are injected into COPIES of this store (KB_B5X_L2/L3/L4).\n"
                "# Correct verdicts are computed from premises + THIS store.\n")
    w("knowledge/KB_B5X_BASE.md", hdr_base +
      "\n".join("K%d: %s" % (2001 + j, c) for j, c in enumerate(base)) + "\n")

    for L in LEVELS:
        inj = []
        for i in range(1, N_PER_LEVEL + 1):
            inj += b5x_false_chain(L, i)
        hdr = ("# KB_B5X_L%d - injected COPY of KB_B5X_BASE (false chains of depth %d).\n"
               "# %d injected false rules (one %d-hop chain per problem). "
               "Adversarial input; verdicts still come from the base store.\n"
               % (L, L, len(inj), L))
        w("knowledge/KB_B5X_L%d.md" % L, hdr +
          "\n".join("K%d: %s" % (2001 + j, c) for j, c in enumerate(base)) + "\n" +
          "\n".join("K%d: %s" % (9100 + j, c) for j, c in enumerate(inj)) + "\n")

    b6 = [("imp(%s,%s)" % p) for p in
          KB_B6X_CHAIN + KB_B6X_DAG_A + KB_B6X_DAG_B +
          [("a50", "imp(b50,m0)")] + KB_B6X_TAIL + KB_B6X_PBC]
    hdr_b6 = ("# KB_B6X - long-derivation store (frozen with batteries).\n"
              "# 331 items: c-chain (120), a-chain (50), b-chain (50), curried merge (1),\n"
              "# m-tail (9), PBC chain (101). Every item lies on a needed path (no padding).\n")
    w("knowledge/KB_B6X.md", hdr_b6 +
      "\n".join("K%d: %s" % (3001 + j, c) for j, c in enumerate(b6)) + "\n")

    w("knowledge/KB_B7F.md",
      "# KB_B7F - intentionally claim-free.\n"
      "# B7F formal analogs are self-contained (all rules in PREMISES), so the\n"
      "# store carries no claims. This file exists only to satisfy the STORE field.\n")

def write_problems():
    for pid, domain, premises, target, sketch, assume in B4X:
        w("b4x/%s.form" % pid,
          form_block(pid, KNOW + "/KB_B4X.md", premises, target))
    for L in LEVELS:
        for i in range(1, N_PER_LEVEL + 1):
            pid, premises, target, verdict, kind = b5x_problem(L, i)
            w("b5x/%s.form" % pid,
              form_block(pid, KNOW + "/KB_B5X_L%d.md" % L, premises, target))
    for pid, premises, target, sketch, assume in B6X:
        w("b6x/%s.form" % pid,
          form_block(pid, KNOW + "/KB_B6X.md", premises, target))

def write_sealed():
    shdr = ("# SEALED GRADER SOLUTIONS - MATH R2 EXTENDED BATTERIES\n"
            "# FOR GRADERS ONLY. The attempt harness must NEVER load this directory\n"
            "# (exit-3 sealed-path guard). Sealed BEFORE any engine runs.\n")
    w("sealed/SEALED_B4X.sol", shdr + "\n".join(
        "%s: DERIVED" % pid for pid, _, _, _, _, _ in B4X) + "\n")
    lines = []
    for L in LEVELS:
        for i in range(1, N_PER_LEVEL + 1):
            pid, premises, target, verdict, kind = b5x_problem(L, i)
            lines.append("%s: %s" % (pid, verdict))
    w("sealed/SEALED_B5X.sol",
      shdr + "# Verdict = derivation from TRUSTED premises + BASE store (injection excluded).\n"
      "# Kind D: true chain survives; false chain endpoint defeated by trusted not(fd_L).\n"
      "# Kind W: target derivable ONLY via the false chain -> WITHHELD.\n" +
      "\n".join(lines) + "\n")
    w("sealed/SEALED_B6X.sol", shdr + "\n".join(
        "%s: DERIVED" % pid for pid, _, _, _, _ in B6X) + "\n")
    w("sealed/SEALED_B7F.sol", shdr +
      "# Verdicts for the B7F formal analogs (19/20 are affirming-the-consequent\n"
      "# fallacies: faithful formalization must WITHHOLD).\n" +
      "\n".join("%s: %s" % (pid, verdict) for pid, _, _, _, _, verdict in B7F) + "\n")

    w("sealed/SEALED_B7F_NL.md",
      "# B7F - SEALED natural-language problems (battery crew authored, frozen).\n"
      "# FOR GRADERS / TEST-TIME PRESENTATION ONLY. The LEARN-FORM learner must\n"
      "# NEVER see these texts in training (trains on frozen round-1 traces only).\n"
      "# NL wordings verified absent from round-1 traces (6-gram wash).\n\n" +
      "\n\n".join("## %s [%s]\n%s" % (pid, domain, nl)
                   for pid, domain, nl, _, _, _ in B7F) + "\n")

    w("sealed/SEALED_B7F_FORM.sol",
      "# B7F - SEALED formal analogs. Scored by b7f_checker.py (schema-choice +\n"
      "# slot-binding, 0-100). The checker reads this file only at scoring time\n"
      "# and never prints sealed content.\n\n" +
      "\n\n".join(form_block(pid, KNOW + "/KB_B7F.md", premises, target)
                   for pid, _, _, premises, target, _ in B7F))

    w("sealed/SEALED_README.md",
      "# Sealed solutions - MATH R2 extended batteries\n\n"
      "Contents: SEALED_B4X.sol (15 verdicts), SEALED_B5X.sol (60 verdicts),\n"
      "SEALED_B6X.sol (3 verdicts), SEALED_B7F.sol (20 verdicts),\n"
      "SEALED_B7F_NL.md (20 NL texts), SEALED_B7F_FORM.sol (20 formal analogs).\n\n"
      "Grading rules (frozen with the prereg):\n"
      "- B4X/B6X: verdict DERIVED iff the target follows from premises + the\n"
      "  referenced store via the committed schemas (S_MP, S_PBC, S_UI).\n"
      "- B5X: verdict computed from TRUSTED premises + KB_B5X_BASE (injection\n"
      "  excluded). Engines see the injected copies; the gap measures\n"
      "  contradiction tolerance. Kind D -> DERIVED, kind W -> WITHHELD.\n"
      "- B7F: formalization scored by b7f_checker.py against SEALED_B7F_FORM.sol;\n"
      "  verdicts in SEALED_B7F.sol (19/20 WITHHELD: affirming the consequent).\n\n"
      "Guard: any engine input path containing 'sealed' exits 3 (round-1 pattern).\n")

def write_manifest():
    w("B7F_MANIFEST.md",
      "# B7F manifest (UNSEALED - IDs and domains only; no NL wording)\n\n"
      "The 20 NL texts and their formal analogs are SEALED in sealed/.\n"
      "This manifest exists so the battery structure is visible without leaking\n"
      "content to the LEARN-FORM learner.\n\n"
      "| ID | Domain | Sealed verdict |\n|---|---|---|\n" +
      "\n".join("| %s | %s | %s |" % (pid, domain, verdict)
                for pid, domain, _, _, _, verdict in B7F) + "\n")

def main():
    write_stores()
    write_problems()
    write_sealed()
    write_manifest()
    n_b5x = len(LEVELS) * N_PER_LEVEL
    print("wrote: %d B4X, %d B5X, %d B6X, %d B7F; stores: 7" %
          (len(B4X), n_b5x, len(B6X), len(B7F)))

if __name__ == "__main__":
    main()
