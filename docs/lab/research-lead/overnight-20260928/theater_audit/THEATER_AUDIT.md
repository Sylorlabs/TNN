# Theater Audit: TNN-2 Learner-State Inventory

**Status:** AUDIT ONLY. Read-only white-box of frozen TNN-2 (`tnn2_build/tnn2.zag`, 1591 lines). No fixes proposed.

**Theater rule (Micah):** "A value stored in learner state with no exercised production write path is theater."

**Extended rule for this audit:** A value with no production read path is also theater (it cannot affect any decision). Classification:
- **GENUINE:** production read path AND exercised production write path
- **WRITE-ONLY:** written in production, never read in production (telemetry theater)
- **READ-ONLY:** read in production, never rewritten (researcher default in disguise)
- **DEAD:** neither read nor written in production (pure decoration)

---

## 1. Theater inventory (6 instances)

### T1. MISS_POLICY node (tag 901, node 1, field 20)

**Location:** `tnn2_init` line 908 creates node 1 with tag 901. `mp_get` (line 916) reads field 20. `mp_set` (line 917) writes field 20.

**Production read path:** NONE. `mp_get` is called only at line 1011 (test code `t_...`).

**Production write path:** NONE. `mp_set` is called only at line 1010 (test code).

**Classification:** DEAD.

**Claim undermined:** Any claim that TNN-2 has a "learner-owned miss policy" or "policy node" for trial dispatch. The node exists in learner state but `mp_run` (line 668) never reads it; it calls `t2_trial` directly with caller-supplied flags. This was previously identified as D6 in the criterion mechanism analysis (`8a2ff4b77`).

### T2. P-INV bootstrap threshold (tag 903 node, field 20)

**Location:** `k_get` (lines 753-762). Searches for live tag-903 node; if absent, creates one with default value 3 (line 760: `ns(W,kn,0,903)`, `write_node(W,kn,3,0,0,0)`).

**Production read path:** YES. Line 775 (`bootstrap_miss`): `let k:i32=k_get(W); if(cnt>=k){...}`.

**Production write path:** NONE. No function ever updates the tag-903 node's field 20 after creation. The value 3 is written once at bootstrap and never changes.

**Classification:** READ-ONLY (researcher default in disguise).

**Claim undermined:** Any claim that the P-INV threshold is "learner-owned" or "adaptive." It is the source literal 3 with extra steps: stored in learner state to look like a parameter, but no experience ever changes it. Previously identified as D7 in `8a2ff4b77`.

### T3. Trial statistics (header field 16)

**Location:** `t2_try_verify` writes to local buffer `st` (lines 499, 506: tried/rejected counts). Line 664: `hs(W,16,get32(st,0)*1024+get32(st,4))` packs into header field 16.

**Production read path:** NONE. The only read is line 1232 (`t_t2_trial_reject` test): `let st:i32=hg(W,16)`.

**Production write path:** YES. Line 664 in the trial path.

**Classification:** WRITE-ONLY (telemetry theater).

**Claim undermined:** Any claim that trial statistics "inform" later decisions. The counts are recorded into persistent header state but no production function reads them back. They are write-only telemetry. Noted in D1 of `8a2ff4b77` ("those counts are never read back by any decision").

### T4. Event log (header field 28 + `ls()` log storage)

**Location:** `log_ev` (lines 285-290). Writes event records via `ls(W,l,...)` and advances `hs(W,28,l+1)`. Called from 9 production sites (lines 308, 818, 828, 831, 832, 842, 854, 856, 862).

**Production read path:** NONE. `hg(W,28)` is read only at line 286 for bounds checking before writing. The log contents (`ls(W,l,0..28)`) are never read by any production function.

**Production write path:** YES. Nine production call sites.

**Classification:** WRITE-ONLY (telemetry theater).

**Claim undermined:** Any claim that TNN-2 "logs experience for later learning" or that the event log participates in cognition. It is a write-only debug trace. No decision reads it.

### T5. UNCERTAINTY nodes (tag 30)

**Location:** `miss_inquire` (lines 796-811) creates UNCERTAINTY node `u` (tag 30) with field4=-4 and (s,r,2,0) via `write_node`. Links guide `g` to `u` via edge type 1.

**Production read path:** NONE for the node's fields. `ev_act` (lines 859-899) traverses edges from POLICY_ROOT to find guide candidates and reads the GUIDE's field4 (context) and field20 (action). It never reads the UNCERTAINTY node's fields (field4, or the s/r/o stored via write_node).

**Production write path:** YES. Line 797-799 in `miss_inquire`.

**Classification:** WRITE-ONLY (structural theater).

**Claim undermined:** Any claim that UNCERTAINTY nodes carry "uncertainty magnitudes" or "inquiry criteria" that guide action selection. The node is created and linked, but its stored fields do not affect `ev_act`'s decision. The guide linkage matters (edge traversal), but the UNCERTAINTY node's own field values are inert. The only read of tag-30 fields is line 1244 in test code (`t_t2_inquire`).

### T6. Eviction history records (tag 3 nodes, header field 12)

**Location:** `rec_evict` (lines 250-253, called from eviction path). Creates tag-3 node `h` copying (s,r,o,clock) from evicted node, links to header field 12 chain: `ns(W,h,4,hg(W,12)); hs(W,12,h)`.

**Production read path:** NONE. No production function traverses the header field 12 chain or reads tag-3 node fields.

**Production write path:** YES. Line 251-252 on every eviction.

**Classification:** WRITE-ONLY (telemetry theater).

**Claim undermined:** Any claim that TNN-2 "remembers evicted knowledge" or that eviction history informs later decisions. The records are written and immediately forgotten by the architecture.

---

## 2. Genuine learner state (both paths exercised)

For completeness, the following persistent state IS read and written in production:

| Element | Read path | Write path |
|---------|-----------|------------|
| POLICY_ROOT (node 0, tag 900, field 20) | `miss_inquire` L800, `ev_act` L861 | `miss_inquire` L804 (lazy init) |
| FACT nodes (tag 1) | `activate` L815, `ev_observe` L840, P-INV L767 | `ev_teach`/`ev_teach_in` |
| GUIDE nodes (tag 2) | `ev_act` L869-896 (field4 context, field20 action) | `miss_inquire` L807-810 |
| MAP nodes (tag 20) | `revise_on_contradict` L690 (revision targeting) | `promote_graph` |
| Edge store (all types) | `bid`/`evcount` L229-245, `activate`, `ev_act` | `link_edge` throughout |
| Header 0 (clock) | `decay`, `ref_prot` | `hs(W,0,...)` L298,814,837,860 |
| Header 8 (evict ptr) | eviction scan | L273 |
| Header 20/24 (node/edge counts) | allocation bounds | `alloc_node`, `link_edge` |
| Context stack (hdr 32-48) | `ev_act` L870 via `ctx_get` | `ctx_push` L292 |

**Note on MAP nodes:** They are genuine for the revision path (read at L690 to find which MAP licenses a contradicted fact). However, the MAP's executable content (field20 = graph root) is never executed by the query path in frozen TNN-2 (confirmed by transfer analysis `475c57e23`: "No query path executes stored graphs"). The node is not theater, but its primary purpose is unexercised. This is an architectural limitation, not theater.

**Note on POLICY_ROOT write path:** The production write at L804 is lazy initialization (creates a guide node if `pr<2`), not a learned update from experience. The pointer changes, but not because the learner revised its policy based on outcomes. Genuine by the letter of the rule (both paths exercised), but the write is structural bootstrap, not learning.

---

## 3. Claim implications

### Claims that theater inflates

1. **"Learner-owned policy"**: T1 (MISS_POLICY) is the most direct inflation. A node labeled as a policy, sitting in learner state, that no production code reads. If cited in a mechanism report as a "policy node," it would falsely suggest learner-owned policy machinery.

2. **"Adaptive threshold"**: T2 (tag-903 k=3) looks like a tunable parameter in learner state. It is a constant. Any report listing it among "learner-held parameters" without noting the absent write path would be misleading.

3. **"Experience logging for learning"**: T4 (event log) and T6 (eviction history) create the appearance of a system that records experience for later use. Neither is ever read. They are debug traces, not memory.

4. **"Uncertainty representation"**: T5 (UNCERTAINTY nodes) suggests the system represents uncertainty as a first-class learner-state object that guides inquiry. The node's fields do not affect the inquiry decision; `ev_act` keys off guide edges and context, not uncertainty magnitudes.

5. **"Trial statistics inform search"**: T3 (header field 16) suggests the system tracks its own trial performance. Nothing reads it.

### What remains after removing theater

The genuine learner state is: facts, guides, MAPs (for revision), edges (for bid magnitudes), clock/counters, context stack, and POLICY_ROOT (bootstrap pointer). This is the actual substrate on which any learner-ownership claim must rest.

The DOF map (`d2af26581`) found 0 pure learner-owned decisions and 5 mixed. The theater audit is consistent: the mixed decisions (bid magnitudes, eviction victim selection, activation winner) operate on genuine state (edge counts, node liveness). The theater nodes (T1-T6) contribute zero to those decisions.

---

## 4. Standing architectural metric implications

For every new mechanism report, Micah requires 12 fields. Theater affects two directly:

- **LEARNER-OWNED STRUCTURAL DECISIONS:** Must exclude T1-T6. A decision attributed to the MISS_POLICY node, the P-INV threshold, the event log, trial stats, UNCERTAINTY fields, or eviction history is attributing to theater. Current TNN-2 count remains 0.

- **LEARNER-INTERNAL CRITERIA:** Must exclude T1, T2, T5. None of these nodes carries a criterion that affects a production decision. Current TNN-2 count remains 0.

The remaining 10 fields are unaffected by this audit, but reports should note where previously-cited "learner-state parameters" were theater (T1, T2 especially, as they look the most like parameters).

---

## 5. Method

Systematic scan of all node-creation sites (`ns(W,*,0,TAG)`) and all header field accesses (`hs`/`hg`) in `tnn2.zag`. For each persistent element, searched for all callers of its accessor functions and all direct field reads/writes. Classified test-only callers (`t_*` functions, lines 920+) as non-production. Verified against the criterion mechanism analysis (`8a2ff4b77`) for D6/D7 and extended to full schema.

**Verdict: THEATER-AUDIT-COMPLETE.** 6 theater instances inventoried. 0 fixes proposed.
