# NAMECHECK: GEN-CYCLES

Worker: gen-cycles. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/gen_cycles/`
Task: implement the COMPOSE-CYCLES PREREG Section 11 generalization
(trial over re-applicable structure sequences with learned halting);
test on the fixpoint workload; regress U's 5 pairs + GEN's
diamond/fan-in/DAG/partial.

## Step 0: toolchain guard (worker governance)

- Safebin active: `export PATH="$HOME/safebin"` at session start.
- `which python3` returns nothing; `which python` returns nothing.
- All computational research operations in pure Zag via pinned safebin
  znc. Shell only for znc, binary runs, git ops, file assembly,
  byte-verification (cmp/sha256sum/diff/grep/sed).
- No forbidden interpreter invocation. Any such invocation would make
  this wave PROCESS-FAIL.

## Step 1: frozen source digests (verified before implementation)

U / COMPOSE-CYCLES sources (from the compose_cycles lane):
- ref_uc_uni.zag (frozen U): ec36df4a01cb1a2b93043184e6e2c84b07658fe7b0c317f9a489ffd6b7b4562e
- ref_uc_base.zag (canonical base): 736f12e7452fb0a95c2dbfc8115028a4e1afba9529cb6cd727acb65367799218
- cyc_base.zag (base + STEP class 4): 0a12cc9a4f9b10fc8c4ce2a2f65294d48d8d402f827ceeb9d3d6126e754cb125
- cyc_new.zag (fixpoint workload driver): 0b20e83e14f16cf5cb4e2a95c41860254aa67244bd59b9aace189e412485239b
- Canonical U outputs (built 2026-10-03 from ref_uc_base + ref_uc_uni):
  P1 ANS=65 TRIES=3; P2a ANS=2 TRIES=3; P2b ANS=2 TRIES=7 WIDEN=1;
  P3 ANS=2 TRIES=3; P5 ANS=3 TRIES=4. Saved as u_run1.txt (reference).
- COMPOSE-CYCLES fixpoint workload output (frozen U): cyc_run1.txt,
  ARM=UNI PROB=QC ANS=-2 TRIES=14, sha256
  93e5b0d9c7de054d91f5a1d73f0b3fb7358d73a8a17f117ff1f47e6de89320e2.

GEN sources (frozen, unmodified in this lane):
- d6_base.zag (GEN base): a53cdf0126ab1501fb70d9b14c2f745e0ef1838209753df8a0c6d0daf484bbcb
- d6_gen.zag (GEN composer, 270 lines; main at 240-270):
  d6f1f9d8f4747293bb7a8e99474660347dc24693f62f3d25caaf1d83c19c9d9a
- gg_new.zag (generality driver): 23e8d5bebe0b85cfc91b1129c088c46a3a64594fcbce7cb035f8a2191dbed8f9
- Recorded GEN outputs (regression targets):
  - diamond battery (P1,P2a,P2b,P3,Q1 diamond,census,Q2):
    gsf_diamond_run1.txt, sha256
    962ca4f0f65228d92b007b5194852f2778d7b52e583442e8bf687b451bc76f84
  - generality battery (Q1 fan-in, Q2 DAG-4, Q3 chain-3, Q4a/Q4b partial):
    gg_run1.txt, sha256
    4b81226d665735820fec1ec4c0dc3e0447b9947b8069f8618b8ad59e87740752

## Step 2: prereg commit order

- This NAMECHECK.md (Steps 0-2) + PREREG.md commit strictly precedes
  all implementation (new .zag files, builds, runs).
- C1 audits this via git log order.
