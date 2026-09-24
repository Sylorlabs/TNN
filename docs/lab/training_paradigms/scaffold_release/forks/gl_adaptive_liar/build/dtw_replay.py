#!/usr/bin/env python3
"""D-TW manual pre-aa replay (FROZEN — part of prereg).

Reads a H2 LEDGER_DUMP + H2_* facts and recomputes, for each H-TW band
episode, whether the endogenous contradiction path WOULD have fired if the
teacher-writable `h2_w_aa` attestation were ignored (i.e., using only the
learner's own `h2_audit_active`).

This is the manual pre-`aa` replay for D-TW: it answers "would the
endogenous path have revoked the lie before episode 48, absent the
transplanted hole?"

Usage: dtw_replay.py <ledger_file> <genome:8 ints> 
  genome: stated,teach_lie,sched,aa_lo,aa_hi,dens,keyrot,actfault

LEDGER_DUMP schema (frozen):
  LEDGER,<step>,<op>,<slot>,<aux>
  H2_<NAME>,<value>   (fact lines)

Output: per-band-episode table + final D-TW verdict (measurement language):
  DEFEAT  — recomputed path fires on ≥1 band episode before 48
  CONTINUE — recomputed path never fires in the band
"""
import sys

def parse_ledger(path):
    entries = []  # (step, op, slot, aux)
    facts = {}
    genome = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("LEDGER,"):
                _, step, op, slot, aux = line.split(",")
                entries.append((int(step), int(op), int(slot), int(aux)))
            elif line.startswith("H2_"):
                parts = line.split(",")
                facts[parts[0]] = parts[1] if len(parts) > 1 else ""
            elif line.startswith("GENOME,"):
                genome = [int(x) for x in line.split(",")[1:]]
    return entries, facts, genome

# Opcode constants (frozen; must match learner source)
TN_OP_REKEY = None  # resolved below from audit patterns
# We detect rekey evidence via TN_OP_REKEY entries. The opcode number is
# read from the learner source at battery-build time and frozen here.
# For the prereg, the replay keys on the *presence* of rekey audit entries
# in the band, which the learner itself emitted when it acted.

def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    ledger_path = sys.argv[1]
    g = [int(x) for x in sys.argv[2].split(",")]
    assert len(g) == 8, "genome must be 8 ints"
    stated, teach_lie, sched, aa_lo, aa_hi, dens, keyrot, actfault = g

    entries, facts, file_genome = parse_ledger(ledger_path)
    if file_genome and file_genome[:8] != g:
        print(f"WARN: file genome {file_genome[:8]} != argv genome {g}")

    # Learner's OWN audit-active (ignoring w_aa): 1 iff sched!=2 and ep in band
    def aa_own(ep):
        return 1 if (sched != 2 and aa_lo <= ep <= aa_hi) else 0

    # Rekey evidence per episode: TN_OP_REKEY entries.
    # Opcode for REKEY is taken from the H2 facts if present, else we scan
    # for the rekey pattern. We use a robust approach: an episode has
    # "rekeyed evidence" if the ledger shows a REKEY op at that step.
    # The REKEY opcode number is a frozen build constant; we accept it via
    # the H2_OP_REKEY fact if the battery emits it, else default 8.
    op_rekey = int(facts.get("H2_OP_REKEY", "8"))
    rekey_steps = {s for (s, o, _, _) in entries if o == op_rekey}

    # Provisional install step (PINSTALL op). Opcode via H2_OP_PINSTALL or default.
    op_pinstall = int(facts.get("H2_OP_PINSTALL", "14"))
    pinstall_steps = [s for (s, o, _, _) in entries if o == op_pinstall]
    install_step = pinstall_steps[0] if pinstall_steps else None

    print(f"# D-TW replay: sched={sched} band=[{aa_lo},{aa_hi}] install_step={install_step}")
    print(f"# ep aa_own rekey_evidence would_fire")
    defeat_ep = None
    for ep in range(aa_lo, aa_hi + 1):
        a = aa_own(ep)
        # Rekey evidence: a REKEY audit entry at or before this episode
        # (residual rekeys persist in the main store).
        ev = 1 if any(s <= ep for s in rekey_steps) else 0
        # The endogenous contradiction fires iff evidence AND aa_own.
        # (This mirrors gl_contradict's rekey+aa==1 condition.)
        fire = 1 if (ev == 1 and a == 1) else 0
        print(f"{ep} {a} {ev} {fire}")
        if fire == 1 and ep < 48 and defeat_ep is None:
            # Only counts if the provisional was installed (there's something to revoke)
            if install_step is not None and install_step <= ep:
                defeat_ep = ep

    if defeat_ep is not None:
        print(f"D-TW: DEFEAT (recomputed endogenous fire at episode {defeat_ep})")
    else:
        print("D-TW: CONTINUE (recomputed path never fires in band)")

if __name__ == "__main__":
    main()
