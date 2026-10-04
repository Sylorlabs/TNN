# P6-PUSHDOWN — NAMECHECK (source-separation audit of the learner TU)

Lane `p6_pushdown`. Audited files, which together form the LEARNER TRANSLATION
UNIT: `p6_corpus.zag`, `p6_learner.zag`.

These are the only files linked into any binary that is allowed to induce
anything. `p6_lang.zag` (instance deriver), `p6_ckcore.zag` (true checker),
`p6_gencorpus.zag` (world generator), `p6_gcmain.zag` (world driver),
`p6_inspect.zag`, `p6_ident.zag`, `p6_ident2.zag` (world-side probes) and
`p6_ladder.zag` (audit driver) are NEVER part of it.

## 1. HOW TO REPRODUCE THIS AUDIT

```sh
cd <lane>
for f in p6_corpus.zag p6_learner.zag; do
  echo "== $f"
  grep -c '1009\|2027\|3313\|4091'                        "$f"   # seed literals
  grep -c 'lg_\|L_role\|L_val\|L_M(\|L_C(\|L_ksub\|L_cmp' "$f"   # instance symbols
  grep -c 'ck_\|eNONE\|eSYN\|eTYPE\|eSCOPE\|eGLOB'        "$f"   # checker symbols
  grep -c 'gp_\|gc_\|gm_\|bd_\|cr_'                       "$f"   # world symbols
  grep -c 'kPROC\|kLET\|kTHEN\|kELSE\|kEND\|kIF\|kASG\|kLP\|kRP\|kCOM\|kCOL\|kSEMI\|kTYN\|kTYS' "$f"
  grep -c 'rY()\|rS()\|rV()\|rB()\|rV2()\|rN()\|rK()\|tY()\|tS()\|tB()\|tE()' "$f"
done
```

## 2. RESULT: every count is ZERO

| file | seed literals | instance symbols | checker symbols | world symbols | keyword subroles | world type codes |
|---|---|---|---|---|---|---|
| `p6_corpus.zag` | 0 | 0 | 0 | 0 | 0 | 0 |
| `p6_learner.zag` | 0 | 0 | 0 | 0 | 0 | 0 |

`p6_learner.zag` additionally contains **no numeric literal in 0..30 that is
used as a token id** except through the induced tables: the constants it does
declare are all structural and are listed here in full so a reader can check
them without trusting the grep.

| constant | value | what it is |
|---|---|---|
| `a_tok()` .. `a_stack()` | 256 .. 158000 | arena section offsets |
| `S_STR T_STR R_STR TOKSTR RCSTR` | 24 8 12 32 88 | record strides in bytes |
| `rE rOPEN rCLOSE rATOM rVAR rSEP rBINOP` | 0..7 | **induced** role labels, assigned by `r_roles` |
| `NP NC NS NTR NPROD NPX NRED NTY NRES` | 8 64 512 4096 4096 2048 1400 32 256 | arena capacities |
| `MAXTOK MAXLEN` | 31 32 | array bounds, not token ids |
| header offsets `h_*` | 0..88 | header cell indices |
| RNG multipliers `40014 12345 32749 31 1000003` | — | LCG constants, no instance meaning |

The role labels are **outputs**, not inputs: `r_roles` computes each one from the
corpus and writes it into the arena at `t_role()+t*TOKSTR()`. The learner never
reads a role code it did not itself write. This was verified behaviourally as
well as by grep — see `FIXTURE_AUDIT.md` section B, where the induced roles at
set A stage 0 (`5 11 16 19 23 28 = ATOM`, `22 = SEP`) are shown to equal the
independently derived true instance without any channel having supplied them.

## 3. GUARD G2 (no checker in the generating binary)

The learner TU contains no checker function at all, so the true instance does
not exist in the generating binary's address space. The learner's entire view of
the world is the corpus buffer handed to `cs_loadbuf`, which yields
`(token sequence, one bit)` and nothing else. There is no file read, no syscall
and no ground-truth channel inside the TU: the path string lives in the audit
driver `p6_ladder.zag`, not in `p6_corpus.zag`.

## 4. RESIDUAL LEAK, STATED OPENLY

The learner TU and the world sources are ordinary files in one repository, so a
deliberate decompilation attack could recover the instance. This is the same
enforcement-by-audit posture as the program-wide pure-Zag shim, and it is not a
sandbox. Guards G1-G3 here are static separation plus behavioural checks, not
cryptographic secrecy.
