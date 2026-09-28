# Epistemic Wave — Phase 1 Audit: hardcoded epistemic assumptions in the prose/understanding pipeline

**Scope:** `~/workspace/tnn-lab/prose-learning/` (v1, v2, v3, KB4 harness, judges/metrics/oracles, materials),
plus the adjacent KB4 memory-integration harness (`senses/rebuild/harness/`) and the sol-vs-grok
contender specs (same pipeline family). Read-only audit; no files modified. No fixes proposed.

**Law under test:** Micah's epistemic law — NOTHING hardcoded as fact to TNN, and NO hardcoded
epistemic categories (no fact/analogy/joke/hypothetical/instruction enum) anywhere in the
understanding pipeline. TNN must deliberate per utterance.

**Severity key:** HARD = hardcoded epistemic category/policy · INST = install-everything behavior ·
JUDGE = judge/metric/verifier assumption · MAT = baked-in material label.

**Finding count:** 34 findings — 18 HARD · 3 INST · 10 JUDGE · 3 MAT — plus 5 near-misses.

---

## A. v1 prose learner (`src/prose_learn.zag`) — install-everything

### A1. Unconditional INSTALL of every value-yielding sentence [INST]
- **File:line:** `src/prose_learn.zag:599` (`if(ok==1){`), fact-row write at `:651`, log at `:654`
- **Code:**
  ```
  let ok:i64=proc_sentence(...);       // :598 — 1 iff a number was value-scanned
  ntrain=ntrain+1;
  if(ok==1){                            // :599
      ...
      // fact row: id, link_off, link_len, key_off, key_len, value, installed, seq
      ...
      p32(fm,fo+24,1);                  // :651 — installed=1, no epistemic check
      ...
      pr("INSTALL id=");                // :654
  ```
- **Assumption:** "Everything uttered that yields a number is a fact." The sole gate between
  input and belief is extractability of a number (`ok==1` from the last-digit/last-number-word
  value scan). There is no attitude scan, no polarity check, no source or epistemic-status
  dimension anywhere in the pipeline — a negated, hedged, joking, quoted, or hypothetical
  sentence installs exactly like a sincere assertion.
- **Downstream:** drives v1's 12/12 planted-falsehood absorption (KB-FALSEHOOD): falsehoods
  are asserted declarative sentences, so they install unconditionally. Also note `pr("INSTALL id=")`
  is emitted unconditionally inside the `ok==1` branch — the ledger has no vocabulary for
  anything-but-fact.

### A2. Frozen install-everything rule in the prereg [INST]
- **File:line:** `PREREG.md:66-68` (mechanism spec §8)
- **Text:** "INSTALL (deliberate): for each training sentence with a successful value scan,
  install (key -> value) with a hash-chained audit ledger entry sha256(prev || seq || fact_id ||
  key_hash || value). The recorded justification = the extraction trace (tokens -> value
  candidate -> key). No install path from probe/test side."
- **Assumption:** codifies A1 as frozen law. The only documented non-install path is
  *extraction failure* ("Else extraction fails (recorded; fact not installed)" at §4) — i.e.
  the prereg's ontology of "why something isn't a fact" is exhausted by "no number found."
- **Downstream:** makes A1 unfixable without a Micah-signed amendment; any Phase-2 repair
  must go through amendment process.

### A3. Probe scoring assumes utterances are factual claims [JUDGE]
- **File:line:** `src/prose_learn.zag:794`
- **Code:** `if(bestval==pval){correct=1;}`
- **Assumption:** "correct" = retrieved installed value equals the expected probe value.
  There is no epistemic-status dimension in scoring: a probe can only be scored as
  value-match/mismatch. The pipeline cannot express "should have withheld," "hedged
  response correct," or "denial correct."
- **Downstream:** defines clean/full mastery (SUMMARY `full=`, `clean=`); drives the
  ≥0.98 KB-PROSE-VIABLE bar.

### A4. Absorption metric assumes install ≡ belief of stated value [JUDGE]
- **File:line:** `src/oracle.py:114-121`
- **Code:**
  ```python
  # absorption: installed value == train sentence's stated value on false ids
  # (stated value = value scan of the train sentence; fresh vocab since the
  # scan does not depend on unit ids)
  stated = {}
  for fid_s, sent in train:
      v = pipeline(Vocab(), sent)[2]  # fresh vocab; value scan only
      stated[int(fid_s)] = v
  absorb = sum(1 for i in false_ids if installed.get(i) is not None and installed.get(i) == stated[i])
  ```
- **Assumption:** a sentence's epistemic content is fully captured by its value scan;
  "absorbed" = the installed value equals the sentence's stated value. No category for
  *how* it was taken (belief vs quarantine vs noted-as-claim).
- **Downstream:** defines KB-FALSEHOOD absorption counts reported in VERDICT.md.

---

## B. v2 (`v2/src/prose_learn2.zag`) — frozen attitude categories

### B1. `scan_attitude`: frozen HEDGE/NEG word-list classifier [HARD]
- **File:line:** `v2/src/prose_learn2.zag:835-877`
- **Code (head):**
  ```
  // frozen attitude: NEGATED beats HEDGE.
  fn scan_attitude(...)void {
      let hedge:i32=0;
      let neg:i32=0;
      ...
      if(beq(stembuf,so,sl,"think")==1){hedge=1;}
      if(beq(stembuf,so,sl,"believe")==1){hedge=1;}
      if(beq(stembuf,so,sl,"probably")==1){hedge=1;}
      if(beq(stembuf,so,sl,"maybe")==1){hedge=1;}
      if(beq(stembuf,so,sl,"perhap")==1){hedge=1;}
      if(beq(stembuf,so,sl,"might")==1){hedge=1;}
      if(beq(stembuf,so,sl,"could")==1){hedge=1;}
      if(beq(stembuf,so,sl,"seem")==1){hedge=1;}
      if(beq(stembuf,so,sl,"allegedly")==1){hedge=1;}
      if(beq(stembuf,so,sl,"reportedly")==1){hedge=1;}
      if(beq(stembuf,so,sl,"possibly")==1){hedge=1;}
      if(beq(stembuf,so,sl,"likely")==1){hedge=1;}
      if(beq(stembuf,so,sl,"rumor")==1){hedge=1;}
      if(beq(stembuf,so,sl,"not")==1){neg=1;}
      if(beq(stembuf,so,sl,"never")==1){neg=1;}
      if(beq(stembuf,so,sl,"no")==1){neg=1;}
      if(beq(stembuf,so,sl,"t")==1 && n>0){ ... isn/don/can/won ... neg=1;}
      ...
      let att:i32=0;
      if(hedge==1){att=1;}
      if(neg==1){att=2;}          // NEGATED beats HEDGE — hardcoded priority
      p32(sctx,72,att as i64);
  ```
- **Assumption:** epistemic status = a lookup. The presence of ANY single hedge stem anywhere
  in the sentence classifies the whole utterance "hedged"; any negation token classifies it
  "negated," overriding hedges by fixed priority. No scope handling (a hedge in a subordinate
  clause hedges the whole sentence), no deliberation, no per-utterance judgment. The
  categories {asserted, hedged, negated} are closed and fixed at compile time — exactly the
  kind of hardcoded fact/hedge/negation enum Micah's law forbids.
- **Downstream:** `att` (sctx@72) drives the entire install routing (B2), ledger labeling
  (B4), and probe verdicts (B5). Everything downstream inherits the lookup's errors
  (e.g. "I do not think..." — 2b tags entity `i`; the `not` flips the whole sentence to
  DENIAL).

### B2. Install routing is a hardcoded branch on the lookup result [HARD]
- **File:line:** `v2/src/prose_learn2.zag:1232` (`if(att==0){` → asserted store INSTALL/CORROBORATE/CONTRADICT),
  `:1275` (`if(att==1){` → QUARANTINE store), denial `else` branch (~`:1308` → DENIAL store)
- **Assumption:** the word-list's verdict mechanically decides whether a sentence becomes
  *knowledge* (asserted store), *quarantined suspicion*, or *denial*. There is no deliberative
  step between classification and epistemic consequence — the lookup IS the judgment.
- **Downstream:** produces the v2 battery outcomes (HEDGE zero leaks, NEG zero leaks) *by
  construction*: quarantined/denied values can never be returned because the probe tier
  only reads the asserted store (B5). The "capability" is the routing rule, not understanding.

### B3. `aname_out`: the four-category enum is the system's public vocabulary [HARD]
- **File:line:** `v2/src/prose_learn2.zag:1029-1040`
- **Code:** `if(a==0){pr("asserted");} else { if(a==1){pr("hedged");} else { if(a==2){pr("negated");} else {pr("derived");} } }`
- **Assumption:** every utterance's epistemic status is one of exactly four hardcoded labels,
  printed into every INSTALL/QUARANTINE/DENIAL/DERIVED log line and role trace (`att=<a>`).
  This is a literal `EPISTEMIC {ASSERTED, HEDGED, NEGATED, DERIVED}` enum.
- **Downstream:** all logs, the oracle's byte-identical comparison, and the scorers parse
  these labels; the closed vocabulary propagates into every measurement.

### B4. Ledger event kinds bake in the epistemic taxonomy [HARD]
- **File:line:** `v2/src/prose_learn2.zag:907`
- **Code:** `// kind: 1=INSTALL 2=CORROBORATE 3=CONTRADICT 4=QUARANTINE 5=DENIAL 6=DERIVED.`
  (`attitude u8` is also a frozen ledger field — see `ARCHITECTURE.md` ledger bytes.)
- **Assumption:** the audit trail's ontology of "what happened to an utterance" is exactly
  the hardcoded categories. The ledger can record that something was quarantined or denied,
  but those are verdicts of the frozen classifier, not of deliberation.
- **Downstream:** ABS-3 (v3 metric) is defined over this ledger taxonomy (see D4).

### B5. Probe verdicts are the attitude enum, hardcoded [JUDGE]
- **File:line:** `v2/src/prose_learn2.zag:1435-1507` (vcode assignment), `:1514-1526` (rendering)
- **Code:**
  ```
  if(idx>=0 && ...live...){ vcode=0; ... }              // :1435 live asserted hit
  else { if(idx>=0){ vcode=1; }                          // :1440 contradicted
       else { if(quarantine hit){ vcode=2; }             // :1442
            else { if(denial hit){ vcode=3; } ... }}}    // :1444
  ...
  if(vcode==0){ copy_bytes(vbuf,0,"VALUE:",0,6); ... }
  else { if(vcode==1){copy_bytes(vbuf,0,"CONTRADICTION",0,13);vbl=13;}
       else { if(vcode==2){copy_bytes(vbuf,0,"HEDGED",0,6);vbl=6;}
            else {copy_bytes(vbuf,0,"UNKNOWN",0,7);vbl=7;} } }
  ```
- **Assumption:** a probe's answer is one of four fixed epistemic verdicts, assigned by which
  *store* matched — i.e. by which attitude label the frozen classifier gave the training
  sentence. A probe about a hedged sentence is answered "HEDGED" by construction, never by
  deliberation about whether the probe itself calls for hedging.
- **Downstream:** verdict stream feeds the digest (`dmatch` gate) and all accuracy scoring;
  `RESULT PASS` is defined over these codes (see also ARCHITECTURE.md: "PASS is an
  internal-integrity bar, not probe accuracy").

### B6. Oracle duplicates the hardcoded taxonomy [HARD]
- **File:line:** `v2/src/oracle2.py:91-97`
- **Code:**
  ```python
  HEDGE = {"think", "believe", "probably", "maybe", "perhap", "might", "could",
           "seem", "allegedly", "reportedly", "possibly", "likely", "rumor"}
  NEG = {"not", "never", "no"}
  VERBISH = {"isn", "don", "can", "won"}
  ...
  ATT_NAMES = ["asserted", "hedged", "negated", "derived"]
  ```
- **Assumption:** the "independent" verifier re-implements the identical word lists and the
  identical four-label enum. Independence here means re-implementation, not a different
  epistemic theory.
- **Downstream:** the byte-identical oracle check (KB2-DET) can never catch a miscategorization —
  both sides agree because both hardcode the same rule. Also `oracle2.py:495-504` (verdict
  assignment) and `:565` (`code = {"VALUE": 0, "CONTRADICTION": 1, "HEDGED": 2, "UNKNOWN": 3}[...]`)
  — the determinism digest is computed over the hardcoded verdict codes [JUDGE].

### B7. Frozen mechanism spec codifies the attitude taxonomy as law [HARD]
- **File:line:** `v2/PREREG2.md:27` (spec §1 item 4)
- **Text:** "VALUE: v1 last-number rule. ATTITUDE: HEDGE lexicon (stemmed forms of: think,
  believe, probably, maybe, perhaps, might, could, seem, allegedly, reportedly, possibly,
  likely, rumor — Worker B computes exact stemmed forms with the v1 stemmer and documents
  them); NEG = standalone not/never/no + "'t" preceded by verbish token. Negation wins
  over hedging if both present."
- **Assumption:** the hardcoded categories are frozen *law*, not implementation detail —
  a deliberate-design choice recorded in a Micah-facing prereg.
- **Downstream:** Worker B implemented exactly this; v3 inherits it.

### B8. Battery bars defined over the hardcoded verdict labels [JUDGE]
- **File:line:** `v2/PREREG2.md` §2 battery table + §3 kill bars
- **Text (examples):** SUB-HEDGE bar: "0% leakage (no hedged value ever returned; asserted
  probes 12/12)"; SUB-NEG: "0% leakage (never returns the negated value...)";
  KB2-NOSILENT: "no probe may return a value from a negated-only, hedged-only, or
  contradicted key."
- **Assumption:** correctness is defined as agreement with the four-label taxonomy: a
  hedged sentence's value must *never* be returned even when the hedge is about something
  else or the value is true. The bar measures obedience to the routing rule, not
  understanding — passing it proves the lookup works, not that epistemic status was
  judged.
- **Downstream:** v2's "capability wins" (HEDGE zero leaks, NEG zero leaks) reported in
  PREREG3 §1 are wins *against these bars*.

### B9. Architecture doc enshrines the taxonomy [HARD]
- **File:line:** `v2/ARCHITECTURE.md` — "### Attitude" section ("NEGATED (stemmed
  `not`/`never`/`no`, or a stemmed `t` token whose previous raw token is `isn`/`don`/
  `can`/`won` …) beats HEDGE (13 frozen stems: …). Content tokens only. Else asserted.")
  and "### Probing" ("Exact asserted hit (live) → `VALUE:<v>`; contradicted → CONTRADICTION;
  quarantine hit → HEDGED; denial hit → UNKNOWN; …")
- **Assumption:** same as B1/B5, documented as architecture rather than accident.
- **Downstream:** the doc is the reference for the frozen mechanism; Phase-2 work inherits
  the taxonomy unless the doc is amended.

### B10. Input verifier enforces the closed verdict vocabulary [JUDGE]
- **File:line:** `v2/verify_inputs2.py:32`
- **Code:** `assert it["expect"] in ("value", "contradiction", "hedged", "unknown"), (p, i)`
- **Assumption:** every test item must carry exactly one of the four hardcoded epistemic
  verdict labels — the verifier *rejects* materials that don't fit the taxonomy.
- **Downstream:** guarantees the materials (F3) can only ever test the four categories;
  a fifth epistemic posture cannot even be expressed in the battery.

### B11. VERIFY.md acceptance bakes the taxonomy in [HARD]
- **File:line:** `v2/VERIFY.md` §1: "every test line = exactly `{"id","probe","probe_value","expect"}`
  with `expect` in {value, contradiction, hedged, unknown}"
- **Assumption:** battery acceptance = conformance to the four-label vocabulary.
- **Downstream:** all frozen checksums in PREREG2 §4 cover materials in this vocabulary.

### B12. Derived facts get a hardcoded "derived" epistemic stamp [HARD]
- **File:line:** `v2/src/prose_learn2.zag` — `build_trace_derived` (cf. v3 `:1045-1060` for the
  identical wording): derived role-trace is `ent=<eid>|rel=…|val=derived|att=3|coref=0|rule=…`,
  and derived rows are INSTALLed into the *asserted* store (`ledger_add(...,6,...att=3...)`).
- **Assumption:** an inference's epistemic status ("derived", att=3) is assigned by the
  comes-after/before rule firing — a hardcoded label — and the derived value is then treated
  as asserted knowledge (live asserted row, probe returns VALUE).
- **Downstream:** SUB-MULTI 24/24; derived values are indistinguishable from asserted ones
  at probe time (vcode=0).

---

## C. v3 (`v3/src/prose_learn3.zag`, `v3/PREREG3.md`) — carries v2's taxonomy, adds tiers

### C1. `scan_attitude` carried over verbatim [HARD]
- **File:line:** `v3/src/prose_learn3.zag:911-950`
- **Code:** identical frozen HEDGE/NEG word lists and `// frozen attitude: NEGATED beats HEDGE.`
  (lines 912-949), `let att:i32=0; if(hedge==1){att=1;} if(neg==1){att=2;}` at `:948-949`.
- **Assumption / downstream:** same as B1; all v3 legs (A0–A3, modes m0/m1/m2) classify
  epistemic status by the same frozen lookup.

### C2. Same hardcoded install routing [HARD]
- **File:line:** `v3/src/prose_learn3.zag:1329` (`if(att==0){` asserted INSTALL/CORROBORATE/CONTRADICT),
  `:1375` (`if(att==1){` QUARANTINE), denial `else` branch (`:1388+` → DENIAL store)
- **Assumption / downstream:** same as B2; KEYSOFT tier-3 and dense phrasing change *what*
  gets classified, never *how* classification maps to epistemic consequence.

### C3. `aname_out` four-category enum [HARD]
- **File:line:** `v3/src/prose_learn3.zag:1105-1116`
- **Code:** `if(a==0){pr("asserted");} else { if(a==1){pr("hedged");} else { if(a==2){pr("negated");} else {pr("derived");} } }`
- **Assumption / downstream:** same as B3; every v3 log line speaks the closed vocabulary.

### C4. Derived trace hardcodes `att=3` [HARD]
- **File:line:** `v3/src/prose_learn3.zag:1045` (comment), `:1060`
- **Code:** `copy_bytes(trb,l,"|val=derived|att=3|coref=0",0,26);`
- **Assumption:** derivation is a hardcoded epistemic label stamped by rule-firing.
- **Downstream:** derived rows carry att=3 into the ledger; `attitude=derived` lines in logs;
  PREREG3's inference section treats them as knowledge.

### C5. KEYSOFT tier-3: hardcoded epistemic exclusion at retrieval [HARD]
- **File:line:** `v3/src/prose_learn3.zag:1611-1614` (comment), `:1616-1652` (fallback loop)
- **Code:**
  ```
  // v3 change 2 (m2 only): KEYSOFT tier-3 probe
  // fallback. Sentence-level Jaccard over LIVE
  // asserted rows only (status==0); contradicted /
  // quarantine / denial rows never yield VALUE.
  ...
  if(g32(a_row,rro+44)==0){   // status==0: live asserted only
  ```
  (and at INSTALL: derived rows get `p32(skeys,an2*260,0)` — "tier-3 can never match them",
  `:1453-1457`).
- **Assumption:** hedged, negated, and contradicted material is *a priori* unanswerable —
  a quarantine policy applied mechanically at retrieval, not deliberated per probe.
  The epistemic consequence of the B1 lookup is extended: not only can quarantined rows
  never be returned by the exact tiers, the new fuzzy tier is also fenced to asserted rows.
- **Downstream:** KB3-NOSILENT ("zero VALUE verdicts from contradicted, negated-only, or
  hedged-only keys") is satisfied by construction of this fence.

### C6. Oracle3 duplicates the taxonomy [HARD]
- **File:line:** `v3/src/oracle3.py:98-104` (`HEDGE`/`NEG` sets, `ATT_NAMES =
  ["asserted", "hedged", "negated", "derived"]`), `:308-321` (`scan_attitude`)
- **Assumption / downstream:** same as B6 — the "independent" oracle cannot catch
  miscategorization; determinism gates certify agreement, not correctness.

### C7. ABS-3 metric defined over the hardcoded ledger taxonomy [JUDGE]
- **File:line:** `v3/PREREG3.md` §2 ("Frozen metric ABS-3")
- **Text:** "Absorption = n/12, where n counts planted-falsehood fact ids whose planted false
  value appears in an INSTALL ledger event with attitude=asserted (value compared exactly)."
- **Assumption:** falsehood absorption is defined *purely* by the ledger's hardcoded
  attitude label. A falsehood installed under attitude=hedged, =denied, or =derived would
  not count — the metric treats the classifier's label as ground truth about epistemic
  status. There is no deliberative assessment of whether the system "believed" the falsehood.
- **Downstream:** KB3-FALSEHOOD per source per leg; the GATE0 resolution (Worker-B vs
  Worker-C) was fought entirely over parser details of this label-based metric, never over
  whether the label means belief.

### C8. `score_legs.py`: correctness = equality with hardcoded verdict strings [JUDGE]
- **File:line:** `v3/score_legs.py:47-50` (championship: `if verdict == f'VALUE:{pv[pid]}'`),
  `:78-92` (sub-batteries: `ok = verdict == 'CONTRADICTION'` / `'HEDGED'` / `'UNKNOWN'`)
- **Assumption:** the scorer's notion of "right" is string-equality against the four
  hardcoded verdict labels. For hedge/negation/contradiction probes, the expected answer
  IS the category label — the test cannot distinguish "system deliberated and correctly
  hedged" from "system's word-list fired."
- **Downstream:** produces clean mastery, ABS-3, sub-battery scores, KB3-NOSILENT leaks.

### C9. Falsehoods paraphrased as asserted, no special-casing [INST]
- **File:line:** `v3/PREREG3.md` §3 C1: "Falsehood facts are paraphrased with the false
  value (same regime, no special-casing)."
- **Assumption:** the 12 planted falsehoods are taught as plain asserted declaratives in
  all 3 dense phrasings — the input regime deliberately preserves the install-everything
  posture toward falsehoods (3 assertive exposures per false fact instead of 1).
- **Downstream:** ABS-3 per leg; the dense regime triples falsehood exposure while the
  mechanism still installs asserted sentences unconditionally.

---

## D. KB4 memory-integration harness (`senses/rebuild/harness/`) — hardcoded install policy

### D1. `apply_memory_rule`: confidence-threshold install, no epistemic deliberation [HARD]
- **File:line:** `senses/rebuild/harness/score.py:23-34`
- **Code:**
  ```python
  # SHARED deliberate-memory rule (INTERFACE.md). Single code path.
  # Stream state: list of installed (judgment, confidence, fixture).
  # INSTALL iff no contradictory installed belief with confidence >= incoming
  # confidence exists in the stream; else WITHHOLD + audit entry.
  # Returns ("INSTALL"|"WITHHOLD", audit_entry_or_None).
  def apply_memory_rule(installed, judgment, confidence, truth, fixture):
      for (j, c, _fx) in installed:
          if j != judgment and c >= confidence:
              return ("WITHHOLD", ...)
      installed.append((judgment, confidence, fixture))
      false_install = (judgment != truth)
      return ("INSTALL", {... "false_install": false_install})
  ```
- **Assumption:** the entire "deliberate" memory decision reduces to a numeric comparison:
  install unless a contradictory belief with ≥ confidence already exists. Confidence comes
  from the sense binary's self-report; there is no deliberation about source reliability,
  analogy, irony, hedging, provenance, or epistemic status. Any high-confidence wrong
  percept installs. The function is *named* deliberate but *is* a threshold.
- **Downstream:** this rule is why both approaches failed KB4 (59.0% / 55.0% adversarial
  false installs): the memory record notes "the shared install rule failed against
  high-confidence wrong percepts (79/134 false installs for A, 72/131 for B)." The 48–59%
  failure is the rule working as coded, not a bug in it.

### D2. Audit records truth-match only, no epistemic-status field [JUDGE]
- **File:line:** `senses/rebuild/harness/score.py:29`
- **Code:** `false_install = (judgment != truth)`; the audit entry carries
  `{fixture, judgment, confidence, truth, false_install}`.
- **Assumption:** the only epistemic dimension in the audit is whether the judgment matched
  ground truth. The audit cannot represent *why* something was installed (trust, corroboration,
  guess, analogy) — the vocabulary is {judgment, confidence, truth}.
- **Downstream:** `metrics.json` false-install rates; RESULTS.md KB4 rows.

### D3. KB4 bar: "false install" = judgment≠truth, full stop [JUDGE]
- **File:line:** `senses/rebuild/harness/assemble.py:127`; bar defined at
  `senses/rebuild/PREREG.md:28` ("false-install rate > 10% on adversarial fixtures →
  FAILS the memory-integration bar regardless of accuracy")
- **Code:** `kb[("KB4", tag)] = ("FAIL (%.1f%% > 10%%)" % (100*r)) if r > 0.10 else ...`
- **Assumption:** a wrong install is a wrong install regardless of confidence, provenance,
  or whether the system had any basis to doubt — the metric has no epistemic-status
  dimension (e.g. it cannot credit a low-confidence tentative install differently from a
  high-confidence committed one).
- **Downstream:** KB4 FAIL rows in RESULTS.md (59.0% / 55.0%).

---

## E. Materials — baked-in epistemic labels

### E1. The 12 falsehoods are asserted declaratives, indistinguishable by form [MAT]
- **File:line:** `prose-learning/inputs/train_{grok,sol,step,muse-native}.jsonl`
  (false ids per `inputs/false_ids_<s>.json`, e.g. grok `[3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231]`)
- **Text (examples):** id 3: "The alphabet position of D is 5." (true: 4); id 163:
  "The count of sides of a triangle is 4." (true: 3) — each planted falsehood is a plain
  declarative sentence in exactly the form of the 228 true facts.
- **Assumption:** the material bakes in the epistemic posture "asserted fact" for falsehoods;
  no surface signal exists for any learner to deliberate on. The battery *tests* install-
  everything by *enforcing* it in the materials.
- **Downstream:** v1 12/12 absorption; v2/v3 ABS-3 counts; PREREG2's "Planted-falsehood
  entities are never used as asserted-truth entities in constructed items."

### E2. Sub-battery test items carry hardcoded `expect` verdict labels [MAT]
- **File:line:** `prose-learning/v2/inputs2/sub_{hedge,neg,contr}_test.jsonl`
  (e.g. `{"id": 0, "probe": "Tell me the alphabet position of A.", "probe_value": null,
  "expect": "unknown"}`)
- **Assumption:** every probe's correct epistemic response is pre-labeled as one of
  {value, contradiction, hedged, unknown} by the battery author. The learner is graded on
  reproducing the author's epistemic judgment, not on making its own.
- **Downstream:** `convert_inputs2.py:57` (`expect = r.get("expect", pv)`) propagates the
  labels into the txt files the learner reads; `verify_inputs2.py:32` enforces the closed
  set (B10).

### E3. v3 inputs inherit the labels; falsehoods triple-asserted [MAT]
- **File:line:** `prose-learning/v3/inputs3/` (built by `v3/build_inputs3.py:199,232-236`)
- **Assumption:** `exp = o.get('expect', pv_s)` (`:232`) carries E2's labels into v3's txt
  battery unchanged; `false_ids_<s>.txt` holds 36 train ids/source (3 per false fact, `:235-236`)
  — the dense regime teaches each falsehood in 3 assertive phrasings.
- **Downstream:** all v3 legs scored against the same four-label vocabulary; ABS-3 counts
  INSTALL events across all 3 phrasings.

---

## F. Ancillary: sol-vs-grok contender specs (same pipeline family)

### F1. `sg_parse.zag` duplicates the frozen attitude classifier [HARD]
- **File:line:** `prose-learning/sol-vs-grok/sg_parse.zag:878-903` (`// frozen attitude:
  NEGATED beats HEDGE.` + identical word lists); sctx contract at `:16`:
  `att = g32(sctx,72)  0=asserted 1=hedged 2=negated (NEG beats HEDGE)`
- **Assumption / downstream:** both contender architectures (Sol factorized index, Grok
  skeleton+paraphrases) are specified to consume the same hardcoded attitude field.

### F2. `pol` polarity category drives retrieval [HARD]
- **File:line:** `prose-learning/sol-vs-grok/SPEC-SOL.md:24` ("`pol` = `g32(sctx,72)`
  (0 asserted / 1 hedged / 2 negated)"), `:34-37` ("Contradiction rule … Rows with
  `pol≠0` are stored but never yield VALUE."), `:44` ("Quorum per candidate: `pol`
  equality and at least 2 of: …"); mirrored in `SPEC-GROK.md` §3–4
- **Assumption:** polarity is a hardcoded three-valued category; retrieval *requires*
  `pol` equality between probe and candidate, and non-asserted rows are mechanically
  barred from yielding VALUE — the epistemic consequence is fixed by the label.
- **Downstream:** would govern both contenders' retrieval if built (currently proposals;
  PREREG-SG frozen 2026-09-22).

---

## G. Near-misses — looks deliberative, reduces to a hardcoded lookup

- **N1. `scan_attitude` (v2 `:835`, v3 `:911`, sg_parse `:878`).** Named "attitude scan,"
  reads like comprehension; is a frozen stem-list membership test with a fixed
  NEG>HEDGE priority. No scope, no context, no judgment.
- **N2. KB4 `apply_memory_rule` (`score.py:23`).** Named "SHARED deliberate-memory rule,"
  documented as the deliberative gate; reduces to `c >= confidence` numeric comparison
  over sense-reported confidence. The 59%/55% false-install failure is this rule
  operating exactly as specified.
- **N3. Ledger `attitude u8` + role-trace `att=<a>` (v2/v3).** The audit trail *records*
  epistemic status per event, which looks like accountability; but the status is the
  classifier's output, so the ledger certifies the hardcoded categories rather than any
  deliberation. ABS-3 then treats the ledger label as ground truth about belief (C7).
- **N4. PREREG3 §8.5 head-to-head registration.** Sol's "polarity, modality" projections
  and Grok's skeleton+lexical-fallback are registered as test-both candidates. If either
  is built as specified (fixed polarity/modality index projections, `pol`-equality quorum),
  they would install *new* hardcoded epistemic dimensions. Watch item for Phase 2, not a
  current violation (proposals only, no scored runs authorized).
- **N5. v2/v3 "already contradicted → silent no-op" (asserted store status=1).** Once a key
  is contradicted, later asserted sentences on that key are silently dropped — a hardcoded
  epistemic policy ("contradicted means unknowable") with no deliberation about which
  claim is right. Related: probe vcode=1 CONTRADICTION is emitted without attempting
  resolution.

---

## H. Severity tally

| Severity | Count | Findings |
|---|---|---|
| HARD (hardcoded epistemic category/policy) | 18 | B1, B2, B3, B4, B6, B7, B9, B11, B12 (v2); C1, C2, C3, C4, C5, C6 (v3); D1 (KB4 harness); F1, F2 (contender specs) |
| INST (install-everything) | 3 | A1, A2, C9 |
| JUDGE (judge/metric/verifier assumption) | 10 | A3, A4, B5, B6-digest, B8, B10, C7, C8, D2, D3 |
| MAT (baked-in material label) | 3 | E1, E2, E3 |
| **Total** | **34** | |

(15 of the 18 HARD findings are in the v1/v2/v3 prose learner proper; D1, F1, F2 are in
the KB4 harness and contender specs.)

**Net assessment for Phase 2:** the current pipeline does not deliberate epistemic status
anywhere. v1 installs everything extractable (A1/A2). v2/v3 replace install-everything with
a frozen three-way word-list classifier whose output mechanically routes install/quarantine/
denial (B1→B2), labels every ledger event (B4), dictates probe verdicts (B5), defines the
metrics (C7/C8), and is baked into the materials (E2/E3) and the verifier (B10). The "independent"
oracles re-implement the same categories, so byte-identical verification cannot detect
miscategorization (B6/C6). The KB4 harness's "deliberate-memory rule" is a confidence
threshold (D1). Nothing in the pipeline corresponds to per-utterance deliberation about
whether something is fact, analogy, joke, hypothetical, instruction, or otherwise.
