"""MATH R4 battery data: CHAIN50_NL (deterministic templates, zero RNG).

6 raw-NL problems requiring >=50 steps (bound 160). Each is a long
single chain rendered from a deterministic template: the generator
instantiates the rule sentences and emits the reference trace from the
skeleton. Skeletons are sealed (sealed/CHAIN50_SKELETONS.json); the
verifier recomputes the shortest derivation length from the skeleton
and checks 50 <= steps <= 160.
"""

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)

CHAIN50 = [
{
 "id": "CHAIN50_NL_01",
 "title": "The lighthouse ledger",
 "frame": [
  "The lighthouse keeper logs the ship count every night.",
  "On night 1 the tally stands at 1.",
  "Each night he adds one to the previous night's tally.",
 ],
 "premise": "The tally after night 1 stands at 1.",
 "rule": lambda n: "If the tally after night %d stands at %d, then the tally after night %d stands at %d." % (n, n, n + 1, n + 1),
 "n_rules": 63,
 "target": "The tally after night 64 stands at 64.",
 "note": "lighthouse tally chain",
},
{
 "id": "CHAIN50_NL_02",
 "title": "The relay",
 "frame": [
  "Sixty-four runners line up for a relay, numbered 1 to 64.",
  "Runner 1 starts with the baton.",
  "Each runner who receives the baton passes it to the next-numbered runner.",
 ],
 "premise": "Runner 1 has the baton.",
 "rule": lambda n: "If runner %d has the baton, then runner %d has the baton." % (n, n + 1),
 "n_rules": 63,
 "target": "Runner 64 has the baton.",
 "note": "baton-passing chain",
},
{
 "id": "CHAIN50_NL_03",
 "title": "The tower of seals",
 "frame": [
  "The clerk must seal 56 documents in order, numbered 1 to 56.",
  "Document 1 is sealed at dawn.",
  "Each sealed document authorizes the clerk to seal the next-numbered document.",
 ],
 "premise": "Document 1 is sealed.",
 "rule": lambda n: "If document %d is sealed, then document %d is sealed." % (n, n + 1),
 "n_rules": 55,
 "target": "Document 56 is sealed.",
 "note": "document-sealing chain",
},
{
 "id": "CHAIN50_NL_04",
 "title": "The island chain",
 "frame": [
  "Seventy-two islands lie in a chain, numbered 1 to 72.",
  "A traveler stands on island 1.",
  "Each year the islanders finish one bridge: the bridge from island N to island N+1 lets a traveler on island N reach island N+1.",
 ],
 "premise": "The traveler can reach island 1.",
 "rule": lambda n: "If the traveler can reach island %d, then the traveler can reach island %d." % (n, n + 1),
 "n_rules": 71,
 "target": "The traveler can reach island 72.",
 "note": "island-reachability chain",
},
{
 "id": "CHAIN50_NL_05",
 "title": "The doubling granary",
 "frame": [
  "The miller stores grain in the granary, doubling it each day.",
  "On day 0 the granary holds 1 grain.",
 ],
 "premise": "The granary holds 1 grain on day 0.",
 "rule": lambda n: "If the granary holds %d %s on day %d, then the granary holds %d grains on day %d." % (2 ** n, "grain" if n == 0 else "grains", n, 2 ** (n + 1), n + 1),
 "n_rules": 55,
 "rule_range": range(0, 55),
 "target": "The granary holds 36028797018963968 grains on day 55.",
 "note": "doubling chain (exact powers of two)",
},
{
 "id": "CHAIN50_NL_06",
 "title": "The lineage scroll",
 "frame": [
  "The scroll records 64 generations of one family, numbered 1 to 64.",
  "The 1st generation are the founder's children, hence descendants of the founder.",
  "Each generation are the children of the previous generation.",
 ],
 "premise": "The 1st generation are descendants of the founder.",
 "rule": lambda n: "If the %s generation are descendants of the founder, then the %s generation are descendants of the founder." % (ordinal(n), ordinal(n + 1)),
 "n_rules": 63,
 "target": "The 64th generation are descendants of the founder.",
 "note": "ancestor-transitivity chain",
},
]

# Expected shortest-derivation step counts (linear chains: n_rules applications).
EXPECTED_STEPS = {
 "CHAIN50_NL_01": 63,
 "CHAIN50_NL_02": 63,
 "CHAIN50_NL_03": 55,
 "CHAIN50_NL_04": 71,
 "CHAIN50_NL_05": 55,
 "CHAIN50_NL_06": 63,
}
