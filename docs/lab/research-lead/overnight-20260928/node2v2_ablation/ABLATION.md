# Node2-v2 Ablation Results

## Summary

All four links in the Node2-v2 consequence chain are NECESSARY. Breaking any single link prevents the full chain from completing. The chain is causal, not correlational.

**Verdict: NODE2V2-ABLATION-COMPLETE.** All links NECESSARY.

## The Chain (from build `0988839a2`)

1. **Link 1 (world to record):** `ev_observe_aw` with `a_w >= 0` calls `resolve_uncertainty_v2`, which records `a_w` in policy history slots (fields 8/12/16).
2. **Link 2 (record to write):** In `resolve_uncertainty_v2`, if fields 8==12==16==A (with A>=0 and A != field 20), then field 20 := A (production write, history reset).
3. **Link 3 (write to read):** `miss_inquire` reads field 20 (`act=ng(W,pol,20)`) to set the guide's action.
4. **Link 4 (read to action):** The guide is created with the read `act` value; `get_guide_action` (and `ev_act`) observe it.

## Ablation Results (3/3 byte-identical per variant)

### Control (base, intact mechanism)

SHA-256: `74c48d5a85087eab5d9c86aebf6075ce69f89be5736422e6bf63e897f527aae9`
- Phase 1 default: 30 (no shift). PASS.
- Phase 2: 30, 30, then 45 (shift on 3rd revelation). PASS.
- Phase 3 guide: 45. PASS.
- **K-H3: PASS.**

### Ablate Link 1: Disable history recording

**Modification:** In `resolve_uncertainty_v2`, changed `if(a_w>=0){` to `if(a_w>=0 && a_w<0){`. The history shift block never executes.

SHA-256: `d67cecf5d28f7ea09396da3fd7f0ef2244f1d9e067b98ced5deb4ca90f2cf5bf`
- Phase 1 default: 30. PASS (no spurious shift).
- Phase 2 default: 30, 30, 30. **FAIL** (no shift after 3 consistent revelations).
- Phase 3: not reached (test exits on Phase 2 FAIL).
- **Link 1: NECESSARY.** Without the record, the write cannot fire. The 3-consistent check has no history to evaluate.

### Ablate Link 2: Disable field-20 write

**Modification:** In `resolve_uncertainty_v2`, changed the write condition `if(a1==a2 && a2==a3 && a1>=0 && a1!=def){` to add `&& a1!=a1` (always false). History records normally, but field 20 is never updated.

SHA-256: `d67cecf5d28f7ea09396da3fd7f0ef2244f1d9e067b98ced5deb4ca90f2cf5bf` (identical to L1)
- Phase 1 default: 30. PASS.
- Phase 2 default: 30, 30, 30. **FAIL** (no shift).
- **Link 2: NECESSARY.** History accumulates (45,45,45) but without the write, the policy does not change. The record alone is insufficient; the production write is the causal step.

**Note:** L1 and L2 produce byte-identical output. Both break the chain before the write, resulting in identical observable behavior (default stays 30).

### Ablate Link 3: `miss_inquire` ignores field 20

**Modification:** In `miss_inquire`, changed `if(pol>=2){` (the block reading `act=ng(W,pol,20)`) to `if(pol>=2 && pol<2){`. The read never happens; `act` stays at literal 30.

SHA-256: `0d25a5741a3c99b7257033b7ae4881f6481b08ba86022e48f2c216aa885cb92d`
- Phase 1 default: 30. PASS.
- Phase 2 default: 30, 30, 45. **PASS** (write fired correctly; field 20 := 45).
- Phase 3 guide: 30. **FAIL** (guide does not carry 45).
- **Link 3: NECESSARY.** The write fires and the policy updates, but without the read, new guides do not reflect the updated policy. The write is insufficient without the production read path.

### Ablate Link 4: Read field 20 but do not use value

**Modification:** In `miss_inquire`, changed `act=ng(W,pol,20);` to `let _rd:i32=ng(W,pol,20);`. The read executes (into unused `_rd`), but `act` remains at literal 30.

SHA-256: `0d25a5741a3c99b7257033b7ae4881f6481b08ba86022e48f2c216aa885cb92d` (identical to L3)
- Phase 1 default: 30. PASS.
- Phase 2 default: 30, 30, 45. **PASS** (write fired).
- Phase 3 guide: 30. **FAIL** (guide does not carry 45).
- **Link 4: NECESSARY.** The read occurs, but the value is not propagated to the guide's action. Reading without using is causally equivalent to not reading. The value must flow from field 20 into the guide construction.

**Note:** L3 and L4 produce byte-identical output. Both break the chain after the write, resulting in identical observable behavior (policy updates, but guides do not reflect it).

## Adversarial: Inconsistent a_w Values

**Modification:** Phase 2 uses `a_w` = 45, 46, 45 (instead of 45, 45, 45). Test expectations inverted: no shift expected.

SHA-256: `baafd7aa3075ad517b7d3a519ad3daff89939d4aab46509bf6ac5ae2ddf86eb8`
- Phase 1 default: 30. PASS.
- Phase 2 default: 30, 30, 30. **PASS** (no shift on inconsistent revelations).
- Phase 3 guide: 30. **PASS** (guide carries default).
- **Consistency requirement VERIFIED.** The 3-revelation rule correctly rejects inconsistent evidence. History after three reveals: (45,46,45) - not all equal, no write fires.

## Causality Analysis

| Link | Ablated | Phase 2 Shift? | Phase 3 Guide | Necessary? |
|------|---------|----------------|---------------|------------|
| (none - control) | No | Yes (30->45) | 45 | - |
| L1: world->record | History not recorded | No | N/A (FAIL) | **YES** |
| L2: record->write | Write disabled | No | N/A (FAIL) | **YES** |
| L3: write->read | Read skipped | Yes | 30 (not 45) | **YES** |
| L4: read->action | Value not used | Yes | 30 (not 45) | **YES** |

**The chain is causal, not correlational.** Each link is necessary:
- Without L1, there is no evidence for the write to act on.
- Without L2, evidence accumulates but the policy never changes.
- Without L3, the policy changes but new behavior does not reflect it.
- Without L4, the policy is read but the value does not propagate to action.

**No link is sufficient alone.** L2 shows that record without write does nothing. L3/L4 show that write without read/use does not change behavior. The full chain must complete for the consequence to drive adaptation.

**Sufficiency of the chain:** The control (all links intact) produces the shift. The four ablations show that breaking any link prevents it. Together, this establishes that the chain as a whole is sufficient (in this test context) and each link is necessary.

## Standing Metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (ablations only; no new mechanisms)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0 (ablation variants only; ~4 lines changed per variant)
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## Constraints Honored

- Unfrozen variants only. Frozen prereg (`4b05c8011`) and frozen source read-only.
- Pure Zag via pinned znc (`znc_linux_x86_64_abed8aa1`).
- `which python3 python` returned nothing. Zero forbidden executables.
- Zero em/en dashes (byte-verified in ABLATION.md and NAMECHECK.md).
- Paper untouched. No sealed worlds. Nothing pushed.

## Files

- `NAMECHECK.md` (Step 0 guard, scope, input provenance)
- `ABLATION.md` (this report)
- `abl_base.zag` (verbatim copy of `n2v2_test.zag`, SHA-256 verified)
- `abl_l1.zag` / `abl_l1_bin` / `abl_l1_run1/2/3.txt`
- `abl_l2.zag` / `abl_l2_bin` / `abl_l2_run1/2/3.txt`
- `abl_l3.zag` / `abl_l3_bin` / `abl_l3_run1/2/3.txt`
- `abl_l4.zag` / `abl_l4_bin` / `abl_l4_run1/2/3.txt`
- `abl_adv.zag` / `abl_adv_bin` / `abl_adv_run1/2/3.txt`
- `base_run1/2/3.txt`
