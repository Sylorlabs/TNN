# Input Manifest

## Frozen sources (SHA-256)
- n5a.zag source: (see SHA_MANIFEST.md)
- Compiler: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
- Knowledge store: ~/workspace/tnn-lab/math_logic/round4/batteries/knowledge/KNOWLEDGE_STORE_NL.md
- PB1 battery: ~/workspace/tnn-lab/math_logic/round3/batteries/r3n/R3N_*.txt (24 files)
- PB4 battery: ~/workspace/tnn-lab/math_logic/round4/batteries/chain_nl/CHAIN_NL_*.txt (20 files)
- Sealed keys: round3/batteries/sealed/SEALED_R3N.sol, round4/batteries/sealed/CHAIN_NL_*.sol.json (read-only, never modified)

## Minimal fixtures (tests/)
- SUBST_MIN1.txt: n=2k → n^4=16k^4
- SUBST_NOVEL1.txt: m=5j → m^3=125j^3
- SUBST_NOVEL2.txt: q=3r → q^2=9r^2
- SUBST_NOVEL3.txt: a=2b → a^6=64b^6
- SUBST_NOVEL4.txt: t=4s → 8 divides t^3
- SUBST_NEST1.txt: x=a+b → (x+1)^2=((a+b)+1)^2
- SUBST_NEG1.txt: schema present, no equality (negative control)
- SUBST_NEG2.txt: unrelated equality (negative control)

All fixtures include the general substitution schema with $A/$B capture variables.
