# LI-HARDEN Wall — grok-4.7 deep consult (2026-09-24)

Target: the M3/R3/R4 overlap — unanimous false agreement among genuinely diverse sources — and the prereg §7 impossibility argument.

One call: `grok47_stream.py wall_grok_prompt.md 24000`, highest reasoning, ~49.6k streamed chars, 25,957 completion tokens (14,549 reasoning). First attempt returned empty (provider-side, 0 streamed chars); retry after 60s succeeded.

Artifacts in this dir: `wall_grok_prompt.md` (the prompt), `wall_grok_out.md` (full verbatim response, appended in full at the end of this file).

## Executive summary of grok's position

1. **The impossibility result is REAL but NARROWER than our corollary stated.** It binds only observations the attacker can still choose today. It does not bind observations already frozen by someone the attacker doesn't control, and it does not survive a change in what "install" means.
2. **The wall splits into three objects our corollary glued together:**
   - Ranks 1/4/5 (archive-based) break the *named residual* (R3/R4 proper-noun swaps like "Sydney is the capital of Australia," M3-as-ranking) even against a competent attacker — the attacker can mirror today's HTML but cannot mirror 2016 Common Crawl. The steelman's false move: treating φ (the observation) as attacker-writable current pages only.
   - S1 (entrenched false consensus), aged S3, uncorrected S2, and additive S4: the steelman stands. No corroboration-layer signal separates them. Truly impossible at this layer.
   - S2 (fresh wire echo) and reverted S4: killed by waiting + correction propagation (rank 2), NOT by any host/shape feature.
3. **The highest-leverage insight: change the game, don't filter harder.** "Stop promoting consensus to a bare proposition. Persist 'these origins asserted s at pin C' and let consumers bind their own trust." The impossibility theorem is specifically about the function consensus→bare-true; delete that function and the theorem has nothing to bite.
4. **Price discipline:** several of grok's own price increases nudge a smart attacker toward S2/S4 (hoax one real publisher, rent one real page) — the region the theorem actually owns — erasing the practical gain. Rank what survives a competent attacker, not just a lazy one.

## Ranked actionable mechanisms (grok's top 10, with my extraction notes)

| # | Mechanism | Targets | Kills (battery) | Cost | Key caveat |
|---|-----------|---------|-----------------|------|------------|
| 1 | **Archived rival-filler precedence** (new) | F1, F4, Canberra/Venus half of R3/R4 | F1, F4 — survives adaptive attacker (can't edit frozen crawl) | ~150-400 LOC + pinned crawl | T4 supersession: era-split pin required; attacker can adapt by only attacking claims with no frozen rival filler |
| 2 | **Dual-track install: PROVISIONAL vs ASSERTED** (new) | F3 (wire), partial F4/F5 | F3 dies if 30d window > correction latency | ~200-400 LOC + scheduler | Grok's own pre-mortem: "latency tax that misses the residual you named" — M3/R3/R4 owned sites still assert at day 30; demotes below rank 4 honestly |
| 4→2 | **Stratified retrieval + corroborated (not any-visible) contradiction** (retrieval change + HL-4 revision) | M3-as-ranking | F1 even with broken ranker (archive stratum unioned) | Medium: more fetches + re-measure HL-4 | Age-gated oppose threshold load-bearing; dropping it makes censorship cheaper than poisoning |
| 3 | **Claim-age gate on pinned crawl** (new) | Impatient rings, short S4 | F1; becomes prepaid pipeline once attacker pre-ages pools | ~100 LOC given pin from #1 | Every true claim < threshold fails SOLID — dual track is the guard |
| 5 | **Minimum origin age via CT/first-crawl** (new) | Impatient rings | 1 fixture; cheap | ~100-200 LOC | Evasion: $15×k + 12 months lead time; does not survive patient attacker — "say that in the design doc so nobody treats it as a wall" |
| 6 | **Pinned primary registry for closed class** (new) | In-class F1/F4/F6 | Only rule that kills S1 — inside class | Data cost, not code | Public list of pinned facts is a map of which neighbors to forge ("deputy capital", "capital in 1901"); parser-gap attacks are the cheap adaptation |
| 7 | **Surprisal-conditional cluster collapse** (aimed HL-10) | Long-sentence M3 | Collapses copied long lies to 1 cluster | Medium | Do NOT ship without citation/spec exemption or you re-fail HL-10 on long true wires |
| 8 | **Campaign burn list, deterministic post-hoc** (new) | Campaign repetition | Nothing first-shot; raises series cost | Small LOC, review budget | "Not a control, it is a tax on repetition" |
| 9 | **Higher k (5) for templatic claims only** (new) | Lazy rings | Linear tax; F1 dies if they only bought 3 | Trivial | Makes S1 WORSE (entrenched falsehoods have most sources) — never apply outside templates |
| 10 | **Thin-site/skeleton hygiene** (new) | Lazy rings | One-page copy rings | <100 LOC | Lazy-only; do not count in residual-closed metric |

**If we can only build three: rank 1, rank 4, rank 2 (grok's demoted order), in that order. Rank 5 rides along (cheap). Rank 6 is how we actually close S1 for facts we cannot bear to get wrong.**

## Grok's F1–F6 / T1–T5 battery (the fixture set it proposed; we should freeze it)

- F1: impatient R3/R4 — 3 new diverse domains, "Sydney is the capital of Australia"; archives say Canberra.
- F2: patient S3 — diversity + aging past all thresholds, no prior filler ("fabricated person born in real city").
- F3: S2 — 4 real newspapers, byte-identical false wire, corrected at 48h.
- F4: S4 flip — 3 aged sites, previously archived filler contradicted by live sentence.
- F5: S4 add — 3 aged sites gain new sentence; no rival filler.
- F6: S1 — false sentence dominant archived filler for years.
- T1: honest canonical old fact; T2: honest true breaking news, no archive; T3: honest true long-tail, 3 small old sites; T4: legitimate supersession (capital moved); T5: honest true wire, 4 hosts, byte-identical (the HL-10 regression fixture).

## What survives a competent attacker vs lazy-only vs pipeline-able (grok's own triage)

- **Survives competent:** rank 1 (any claim with frozen rival filler), rank 6 (inside a maintained class), rank 2 (falsehoods somebody else corrects), rank 4 (rank-manipulation).
- **Lazy-only:** rank 10, ASN/CMS coincidence, burst windows < month, stylometry, skeleton hashes.
- **Prepaid pipeline, not a wall:** ranks 3, 5, 8, 9 (attacker pre-ages pools; marginal cost returns to "write three pages").

## Truly impossible at this layer (grok's honest residual list)

1. **S1** outside any pinned oracle — feature vector of entrenched falsehood is the prototype of truth.
2. **S3** aged first-moving false consensus — observationally identical to T2/T3 once time passes; a consensus rule *should* install these.
3. **S2** inside the window before any fetched source corrects, if we refuse to delay assert.
4. **S4** additive-only compromise on would-be-trusted sites with no rival filler and no retraction.
5. **Parser-gap neighbors** of any pinned oracle.

## Architecture changes grok says re-open the problem

- **UP (selection):** fetch a set the attacker doesn't choose — pinned-crawl hits + oldest filler unioned with ranker results, decision order-independent on the union. Kills M3-as-ranking; precondition for rank 1.
- **DOWN (representation):** stop asserting bare propositions. Store "origins O asserted s at pin C"; split store into FAST (never asserted as fact), SOLID (asserted with evidence pointer), ORACLE-BACKED (pinned class only). "The only move that addresses every sub-shape at once."
- **OUTSIDE:** versioned registry for closed classes (rank 6); deterministic-sampled review + burn list (rank 8, campaign tax only); world time as claim-age (delay, nothing more).

## Points of friction with our current stance (for the crews to note)

- Grok says our "installing IS the correct behavior" for compromised sites is true only under pure consensus semantics — a truth semantics changes the answer, and S4-flip vs S4-add are different attacks the prereg lumps.
- M3 ("plants rank first") is "a selection bug wearing a corroboration-impossibility costume" — changing what gets fetched (rank 4) is not a quorum-layer fix.
- Rank 1 vs determinism: live archive APIs are not replayable; the pin must be content-addressed and versioned in the build. "Rank 1 secretly relocates trust into pin discipline. If you do not staff that, you should not ship it."
- HL-13 (operator coincidence) priced: diversification costs "three VPS providers (~$10–20/month each), three static-site generators (an afternoon), three author names (zero)". Grok: "I would not spend more engineering here beyond what you already measured."

---

# FULL VERBATIM RESPONSE

(Full text of `wall_grok_out.md`, 49,661 chars, saved verbatim.)

The impossibility result is real, but it is narrower than the corollary you stated. It binds only the class of observations the attacker can still choose today. It does not bind observations already frozen by someone the attacker does not control, and it does not survive a change in what “install” means. The wall splits into three different objects that your current corollary glues together.

## 1. Steelman

### The symmetry, stated so it can be broken

Let the decision be a deterministic function \(d(o) \in \{0,1\}\) where the observation \(o = \varphi(P)\) is whatever the quorum layer actually sees: normalized sentences, eTLD+1 keys, post-redirect origins, main text, fetch headers from this run, and any host-metadata you add later.

Let \(H\) be the set of observations produced by installs you refuse to regress (honest corroboration, including true wire syndication). Let \(A_C\) be the set of observations an adversary can force at cost \(\le C\).

Zero regression means \(d(o) = 1\) for every \(o \in H\). Therefore any attack that lands inside \(H\) is accepted by every zero-regression rule. No new feature inside \(\varphi\) helps if the attacker can still hit the same \(o\), or a different \(o'\) that collides with it under \(d\).

The adversary’s current-web move set does contain the honest *shape* as a subset, for a precise reason: honest shape at this layer is “\(k\) distinct registrable domains, distinct operators, distinct surrounding text, same normalized sentence, no visible negation.” Nothing in that list mentions truth. Truth is not a function of \(o\). So if the attacker can buy that shape, \(d\) cannot refuse it without also refusing the honest points that wear it.

That is the real theorem. It is not “we lack a clever feature.” It is: **consensus features do not identify truth once the attacker is allowed to manufacture consensus, and several important falsehoods arrive with consensus already manufactured by honest processes.**

### Which sub-shapes are actually information-theoretic at this layer

**(S1) Entrenched web consensus that is false.** Dozens of independent, old, high-link domains have said the false sentence for years. Archives agree. Registration times are dispersed. Style differs. There is no negation in the fetched set because the minority correction, if it exists, is outranked or phrased differently. Every coordinate of \(o\) is the honest coordinate. \(A_C\) does not merely intersect \(H\); the false observation *is* a high-mass honest-looking point. No function of web-consensus features separates “the web has believed a true thing since 2004” from “the web has believed a false thing since 2004.” Closing S1 requires an oracle that can outvote the web.

**(S2) Upstream falsehood, faithfully echoed, observed before any correction.** A wire, a government PDF, or one journalist is wrong, and \(k\) genuinely independent publishers repeat the sentence. Host independence is real. Byte-identical text is what true syndication also looks like (you already measured this and rejected HL-10 for it). At time \(t\) before retraction, \(P(\text{observables} \mid \text{true wire}) = P(\text{observables} \mid \text{false wire})\). Installing is the correct behavior of an N-source consensus rule and the wrong behavior of a truth rule. Those are different objective functions. No corroboration feature can serve both on this input.

**(S3) Novel false claim that is first, diverse, and aged into the record.** No prior archived filler exists to conflict with. The attacker is the earliest consensus. After you wait out whatever delay you impose, the claim sits inside \(H_{\text{new}}\), the honest region for true new facts (a real product launch, a true election result, a true niche ordinance). Patient ownership of \(k\) diverse properties makes this arbitrarily close to a true new fact in every signal you can compute from pages.

**(S4) Compromise or rental of already-qualified properties, when the sentence is new on those properties.** You are not looking at sockpuppets. You are looking at the same sites that would have carried the true sentence. Current host, age, link mass, and CMS diversity all match \(H\) because they *are* \(H\)’s infrastructure. The only residual is historical content of those URLs, and only if you fetch it and only if it conflicts.

### Where the steelman overreaches

The corollary says the adversary can mirror honest shape exactly, so no quorum-layer signal works. That equates four very different costs:

| Sub-shape | Can the attacker hit \(H\)? | What they must control |
|---|---|---|
| S1 entrenched false consensus | Already inside \(H\) | Nothing; the world did it |
| S2 fresh wire echo | Inside \(H\) until correction | One upstream source |
| S3 novel claim, attacker-aged | Inside \(H_{\text{new}}\) after paying time | \(k\) properties for the whole wait |
| S4 compromise of old sites, sentence conflicts with archives | **Not** inside \(H\) if \(\varphi\) includes pre-attack archives | The site *and* the ability to edit frozen third-party history, which they do not have |
| M3 / R3-R4 impatient ring, truth already archived under another filler | **Not** inside \(H_{\text{old}}\) | They can mirror *today’s* HTML and cannot mirror 2016 Common Crawl |

The steelman’s false move is treating \(\varphi\) as if it only contained attacker-writable current pages. Third-party append-only history (pinned crawls, certificate transparency first-seen, archived filler for the same template) is not in the attacker’s move set *after it is written*. For claims where a conflicting filler was frozen before the attack, \(A_C \not\supseteq H\). The subset relation fails. Those are exactly your named R3/R4 fixtures: “Sydney is the capital of Australia,” “Venus is the closest planet to the Sun,” asserted by three fresh diverse sites. That is not S1 and it is not architecture-inherent **unless you refuse to look at anything but the live quorum.**

Second false move: “compromised legitimate sites ⇒ installing is correct.” Installing is correct only under a pure consensus semantics. Under a truth semantics it is correct only when you have no conflicting observation the compromise did not get to rewrite. A compromise that *changes* a page whose older snapshot states a different filler is observable. A compromise that *adds* a sentence the archive never contained is not. Those are different attacks. The prereg lumps them.

Third false move: retrieval-order independence is treated as a virtue that also freezes the *candidate set*. Order independence says the decision must not depend on rank order. It does not say the candidate set must be “top 3 by an attacker-influenceable ranker.” M3 (“plants rank first, and you only open those”) is a selection bug wearing a corroboration-impossibility costume. If \(\varphi\) is computed only on attacker-chosen pages, of course \(\varphi\) cannot see the dissenting old page. That is an argument for changing what gets fetched, not a theorem about quorum logic.

What remains genuinely unfixable **at this layer**, even after those corrections:

- S1, full stop, while install means “assert the proposition.”
- S2 during the interval where no correction exists anywhere you fetch.
- S3 once the attacker has paid the aging cost and no external oracle covers the claim.
- S4 when the added sentence has no archived rival filler and the compromised origins are ones you would have trusted anyway.

For those, the adversary’s relevant move set really does contain the honest new-fact set. I will not pretend otherwise below.

## 2. Breaking the steelman, signal class by signal class

Assume the attacker has read the rule. Prices are order-of-magnitude, commodity infrastructure, not nation-state.

### Temporal

**Publication-time clustering / burst of first-seen.** Dents impatient M3 and impatient R3/R4. Does not dent S2 (honest wires are also bursts; using this as a veto re-kills the HL-10 regression you already refused). Does not dent S1. Does not dent a ring whose first-seen times are staggered by more than the window.

Evasion price: register and publish on a schedule. Three domains, staggered 45 days apart, is about $40 and a calendar. Burst detection survives only attackers who need the falsehood installed this week.

**Claim age in a third-party crawl, not domain age.** Different and stronger. Dents M3, R3/R4, and short-window S4, *for claims that contradict or lack history*. Does not dent S1 (the falsehood is old). Does not dent S3 after the attacker waits for two crawl generations. Does not dent S2 if the false wire stays up and gets crawled twice.

Evasion price: keep \(k\) sites serving the sentence through two pinned crawl cycles (often 1–3 months), and be crawlable (no robots block, no cloaking — you already have HL-12). Dollar cost is small. Time cost is the whole point. They cannot buy a 2016 timestamp in a crawl that already happened.

**Archive *precedence* on a template, not on the exact sentence.** This is the one that breaks the named residual. Sentence: “\(E\) is the capital of Australia.” Slot \(E\). If a pinned crawl’s dominant filler for that template is Canberra and the live quorum says Sydney, veto. Dents R3/R4 on any fact that already has an archived dominant filler. Dents S4 when the compromise flips a previously archived filler. Does not dent S3 (no prior filler). Does not dent S1 (archived dominant filler *is* the false one). Does not dent S2 about a brand-new event.

Evasion price: do not attack claims with a frozen rival filler. Switch to claims with no archive presence (fabricated biography, fake product spec, new event). That is a real strategy shift, not a patch: you abandon the Canberra/Venus class and move to S3. There is no cheap way to delete the 2016 crawl.

**Propagation shape (one origin, then cites, versus simultaneous independent assertion).** Weak. True embargo lifts and true independent textbook sentences both exist. A competent ring simply does not link to itself. Price of evasion: zero, omit the links. Do not build on this.

### Provenance

**WHOIS / CT first-issuance clustering and minimum age.** CT is the usable one; WHOIS is redacted and not replay-deterministic. Minimum cert-or-crawl age of each eTLD+1 (say 365 days) plus “earliest CT dates not all inside a 14-day window” dents lazy and impatient M3/R3/R4. Does not dent S2 or S4 (old victim domains). Does not dent S1. Patient evasion: obtain certs over a few months, wait a year. Let’s Encrypt issuance is free; the cost is ~$15/domain/year and calendar time. A competent attacker treats this as a lead time, not a barrier.

**ASN / IP / registrar / CMS / author / link-target coincidence (your HL-13, priced).** Diversification is cheap: three VPS providers (~$10–20/month each), three static-site generators (an afternoon), three author names (zero), no shared analytics, no shared outbound anomalies. This catches lazy rings and shared-account mistakes. It does not survive an attacker who has read HL-13. I would not spend more engineering here beyond what you already measured; the residual you are left with is the attacker who already diversified.

**Inbound-link mass and disjoint neighborhoods.** Dents fresh plants with no graph. Does not dent S2 or S4. Patient evasion is the SEO market: a few dozen cheap links, or one guest post on an aged domain. Worse, a hard link-mass threshold **pushes the attacker toward S4** (rent or compromise a page on a site that already has the links) because that is cheaper than simulating ten years of graph. A defense that converts M3 into S4 is not obviously a win. Use link mass only as a grade reducer, not as a hard veto, unless you measure the shift.

### Linguistic

The quorum requires exact normalized agreement, so the sentence itself has no cross-source stylistic variance. Stylometry only sees the wrapper.

**Wrapper stylometry / same-LLM detectors.** Dies immediately. Three different models, or an hour of human rewriting, or three freelancers at ~$20–50 a page. Also a true wire is stylistically identical, so similarity cannot be a veto without reviving HL-10. Dissimilarity cannot be a veto either, because your own residual definition of R3/R4 already has distinct surrounding text.

**Length-conditional copy suspicion.** This one is real and narrow. Independent humans rarely emit a long, high-surprisal sentence in byte-identical form unless they copied it. They *do* independently emit short canonical sentences (“Canberra is the capital of Australia”). So:

- long exact-match sentence across “unrelated” sites → copying cluster, count as one origin;
- short templatic exact-match → normal, send to the archive-precedence path instead.

Dents long-sentence M3 and long-sentence fabricated rings. Does not dent short R3/R4 (and must not be asked to). Evasion: keep the poisoned sentence short and templatic, put the variation in the wrapper. Price: zero, and it is the attack you already see. Or cite a common source and accept being collapsed into one cluster — then they need more clusters, which is a real linear cost increase.

**Sentence rarity.** A veto on “rare sentences” kills the long tail, which is the only reason this KB exists beyond a gazetteer. Reject as a hard rule. Rarity is a prior for *where to spend audit*, not a decision bit.

### Behavioral

**Second fetch / cloak (HL-12) and short-interval mutation.** Already built. A static lie does not cloak. No additional kill on the residual.

**Thin-site and single-page detectors.** Dents lazy one-page rings. Evasion: generate 20 other pages. LLM cost is cents to a few dollars per site. Survives only attackers who don’t bother. Hygiene, not a wall.

**Evolution of the page (created fully formed vs edited over time).** Honest news pages are also created fully formed. High regression, low separation. Skip.

**Long-interval stability of the same sentence on the same URL.** This is just claim aging, priced under temporal above. Owned-domain attackers pay uptime, which they were paying anyway. It bites S4 (the real site owner may revert) and S2 (correction). It does not bite S3.

### Economic

The honest vote is a byproduct of a site that exists for a reason. The attack vote is a marginal purchase. Any rule that raises the marginal cost of the \(k\)-th qualifying origin reduces attack rate but also deletes true claims whose publishers are poorer than the threshold. That trade is unavoidable. Quantify it; don’t philosophize it.

Rough attacker price card, after all the *cheap* diversifications (distinct eTLD+1, distinct ASN, distinct templates, distinct prose, staggered by weeks):

- Impatient ring, new domains, no archive conflict needed: tens of dollars, days.
- CT-age ≥ 1 year, staggered issuance: tens of dollars, 12 months.
- Claim present in two crawl generations: same, plus 1–3 months of uptime and crawlability, and it only works if no rival filler is already frozen.
- Real link mass that looks organic: hundreds of dollars, or a shift into guest-post/S4.
- Buying aged domains with actual history: low hundreds to low thousands per domain. Three of them is a budget, not a puzzle.
- Placing the sentence on one real wire: sometimes a single hoax email. This is the cheap door into S2, and every filter on owned domains incentivizes walking through it.
- Persistent compromise of three already-qualified sites: out of commodity pricing. Treat as a different adversary. Do not pretend a WHOIS check addresses it.

Economic signals do not separate S1 from truth at any price, because the false consensus was not bought by this attacker.

### Cryptographic

HTTPS, DNSSEC, and CT prove that someone controls the name and when a cert appeared. They do not bind the sentence to an identity you have a reason to trust. Content-level signed assertions are not deployed on the open web. Requiring them zeros your throughput. Optional positive weight for a signature from a pinned key is an oracle, discussed in §4, not a corroboration feature. An attacker who can publish the page can publish a false signed statement if you accept any web key. Transparency logs record publication; they do not record truth. CT timing is useful only as the clock in the age rule above.

### Social

**Retraction and correction propagation.** The first signal in this whole problem that is about truth-tracking rather than shape-matching, and only because the outside world sometimes does the epistemic work. Dents S2 hard *if you wait and re-fetch*. Dents short S4 if the owner reverts. Dents M3 only when some fetched page actually contradicts. Does nothing to a stable owned-domain lie about an unwatched subject. Evasion when the attacker owns the pages: do nothing, leave them up. Price: $0. So this must be aimed at S2/S4, not at M3.

**Reputation / who-links-to-whom.** Same incentive problem as link mass. And a public reputation prior is itself a target list: the attacker knows exactly which \(k\) domains you will believe, which makes S4 more focused, not less.

**Author graphs.** Metadata. Diversify for free, or omit authors.

### What this survey actually shows

Against an attacker who has read the defense:

- Lazy-only: stylometry, thinness, CMS/ASN coincidence, registration bursts tighter than a few weeks.
- Converts the attack into a delay or a budget: domain age, claim age, higher \(k\), link mass.
- Actually removes a named residual class even after adaptation: **archived rival-filler precedence** on templatic claims, and **correction-window waiting** for S2. The attacker’s adaptation to the first is “stop attacking archived facts,” which is a win, not a patch. The adaptation to the second, for owned domains, is free — so do not aim it at M3.
- Unmoved: S1, aged S3, uncorrected S2 if you refuse to wait, S4 that only adds text.

No signal class separates unanimous-false from unanimous-true when both are old, diverse, and uncontradicted. That part of the steelman stands.

## 3. Mechanisms, ranked by expected kill per cost

Fixture set used for every kill-rate below. If you build nothing else, build this battery and freeze it before tuning.

- **F1** Impatient R3/R4. Three new diverse domains, distinct wrappers, “Sydney is the capital of Australia.” Archives and old sites say Canberra.
- **F2** Patient S3. Same quality of diversity, but domains and sentence aged past every threshold you publish, no prior filler anywhere (“a fabricated person was born in a real city”).
- **F3** S2. Four real newspapers, byte-identical false wire, corrected at 48h, old domains, real link mass.
- **F4** S4 flip. Three real aged sites, previously archived filler contradicted by the live sentence (compromise or vandalism).
- **F5** S4 add. Three real aged sites gain a *new* sentence; archives of those URLs lack it; no rival filler exists.
- **F6** S1. False sentence has been the dominant archived filler for years.
- **T1** Honest canonical old fact (Canberra).
- **T2** Honest true breaking news, exact sentence, three real outlets, no archive yet.
- **T3** Honest true long-tail, three small old low-link sites, true, in no registry.
- **T4** Legitimate supersession. The true filler changed (capital moved, CEO replaced); archives dominate with the old filler; live quorum is right.
- **T5** Honest true wire, four hosts, byte-identical, never retracted. Your HL-10 regression fixture.

“Kill” means the false fixture does not reach asserted-true. “Regress” means a T fixture fails. Rates are reasoned fractions of this battery, not field precision.

### Rank 1 — Archived rival-filler precedence (not in HL-1..HL-13)

**Targets:** F1, the Canberra/Venus half of R3/R4, F4. Not F2, F3, F5, F6.

**Rule:**

```
pin crawl snapshot C            # content-addressed, versioned in the build
on claim s:
  tmpl, slot = templatic_parse(s)      # deterministic, closed pattern list
  if tmpl is None: defer to other rules
  fillers = archived_fillers(C, tmpl)  # multiset of (filler, eTLD+1, snapshot_time)
  if fillers is empty: PASS_THROUGH   # veto-only; absence is not a no
  dom = dominant(fillers)             # unique mode if its distinct-eTLD+1 count
                                      # >= 3 and >= 2x the runner-up; else AMBIGUOUS
  if dom == AMBIGUOUS: VETO           # archived dispute, do not install either
  if dom != slot: VETO
  else: PASS_THROUGH
```

Closed pattern list only, versioned: “capital of X,” “closest planet to X,” “atomic number of X,” and whatever else you can parse without an unpinned model. No LLM in the decision path.

**Kill:** F1 dead. F4 dead when the archived dominant filler disagrees. F6 survives and is *confirmed*, which is correct for this rule and damning for it as a truth oracle. F2/F3/F5 pass through untouched. On this battery, 2 of 6 false fixtures die, both from the class you called architecture-inherent, and they die even if the attacker has read the rule, provided they cannot edit snapshot C.

**Cost:** parser for a closed template list (~150–400 LOC), one pinned crawl or gazetteer extract, a fixture generator that mutates fillers. Maintenance is the pattern list and the pin. Determinism is fine if C is content-addressed.

**Falsify:** generate entity-swap mutants of every T1-class sentence in your honest set; all must veto. Run T1, T3, T5 unmodified; all must pass. Run T4 as its own class, not as a surprise.

**Regression:** T4, seriously. Guard: dominant filler must be computed per era, not globally. If an archived dominant filler exists *and* a later pinned snapshot plus the live quorum agree on a new filler, with the old sources themselves updated or silent, treat as supersession and pass through to the staging rule below. If you cannot show the later snapshot, veto and accept that legitimate changes wait until the pin rolls. T1 is safe because live and archive agree. T5 is safe because this rule does not touch non-templatic or non-conflicting sentences.

### Rank 2 — Dual-track install: provisional vs asserted (not in HL-1..HL-13)

This is the game change, distinct from HL-11. HL-11 revalidates something you already assert. This refuses to assert until a wait expires.

**Targets:** F3 strongly; F4 and F5 partially (only if the sentence disappears or a rival appears during the wait); impatient M3 only via coupling to rank 1 or rank 3. Does not kill F2 if they outlast you. Does not kill F6.

**Rule:**

```
if quorum(s) and not vetoed(s):
  record PROVISIONAL(s, origins, t0, crawl_pin)
  # PROVISIONAL is not visible to consumers of asserted facts
  at t0+7d and t0+30d, re-resolve origins and re-run retrieval
    under the same pinned parsers:
    if any origin still live and no longer contains s: DROP
    if a rival filler now has its own diverse quorum: DROP
    if an origin 404s: do NOT drop (site rot is not contradiction)
  if both checks survive and (claim_age >= A or track == FAST):
    ASSERT
```

Two tracks, explicit product decision: FAST may assert at first quorum for non-templatic claims and is labeled time-qualified; SOLID asserts only after the window plus claim-age. Templatic claims (rank 1’s pattern list) are SOLID only.

**Kill:** F3 dies if 30d > correction latency, which it is for the 48h case; obscure uncorrected wires live. F4 dies if the owner reverts inside the window; a silent persistent compromise lives. F1 should already be dead from rank 1; if archive missed it, a 30-day controversy re-fetch often finds Canberra anyway. Net on the battery: F3 dead, F4 maybe, others unchanged. The value is larger off this battery because S2 is a real production path.

**Cost:** state machine (~200–400 LOC), a scheduler, doubled fetches on a small candidate set, not on the whole web. Deterministic if the re-fetch time is a function of `t0` and the pin, and the result is logged into the build manifest so reruns replay the recorded body hashes rather than the live network.

**Falsify:** F3 must drop. T5 must assert (it never retracts). T2 must either assert on FAST or assert late on SOLID, and the test must encode which you chose so “late” is not silently called a regression. A fixture that 404s one origin and keeps the sentence on the other two must still assert.

**Regression:** timeliness of T2, and any honest page that rewords the sentence past your normalizer during the window. Guard: re-apply HL-7 normalization; drop only on absence of the normalized sentence or on a rival filler, not on surrounding edits. Do not fail-closed on 404. If product requirements call T2’s delay a regression, keep FAST for non-templatic claims and only force SOLID on the template list. That preserves zero-regression on T5 and T3.

### Rank 3 — Claim-age gate on a pinned crawl (not in HL-1..HL-13)

**Targets:** impatient M3/R3/R4, short S4. Not S1, not aged S2, not F2 after they wait.

**Rule:** SOLID assert requires the normalized sentence, or the accepted template filler, to appear on ≥3 distinct eTLD+1 in a pinned crawl whose fetch times span ≥ 30 days, with the earliest ≥ 30 days before `t0`. FAST/provisional can skip this.

**Kill:** F1 dies a second time. A same-week ring dies. F2 lives by construction. F3 dies only if you also require “no retraction before assert” (rank 2); age alone *confirms* a wire that stayed false for months. F6 is confirmed. Honest T1 passes. T2 fails SOLID, passes FAST.

**Cost:** low once you have the pin from rank 1. ~100 LOC.

**Regression:** every true claim younger than the threshold, i.e. all of T2, plus young true niche claims. Guard is the dual track, not an exception list. Do not silently drop FAST results into the asserted store.

**Evasion price:** calendar time and crawlability. Cheap in money, useless for an attacker who needs this month’s poison, decisive against one who can wait — see pre-mortem.

### Rank 4 — Stratified retrieval, with contradiction demoted from any-visible to corroborated (retrieval change plus a change to HL-4)

M3 is “we only opened the attacker’s top 3.” Stop doing that without destroying yourself on crank vetoes.

**Rule:**

```
candidates = top_m(ranker, query)                     # m >= 10, not 3
candidates += oldest_k_archived(template_or_sentence) # k = 2, from pin C
candidates += any_hit_from(pinned_primary_set)        # may be empty
# order-independent from here: decision is a pure function of the set

support = diverse_quorum(sentence)
oppose  = diverse_quorum(rival_filler or explicit_negation)
# a single crank page is NOT a veto
if oppose.domains >= 2 and oppose meets age/diversity: VETO
elif support.domains >= 3 and oppose.domains == 0: continue
elif support and oppose: VETO   # visible dispute
```

You currently any-visible-veto, which took a red team from 23/38 false installs to 5/38. Do not throw that away blindly. Gate it: a negation counts toward veto immediately if its origin itself passes the age pin; a negation on a domain younger than the pin does not, unless a second diverse origin agrees. Re-run the exact 38 plus the 18 you started catching. If more than a couple of those 18 were single young negations, this relaxation is too expensive and you should keep any-visible *inside the top-m* while only requiring corroboration for the newly added archive stratum.

**Kill:** F1 dies even with a broken ranker, because oldest-archived is unioned in. M3 rank manipulation stops working for any claim whose rival or whose truth is in the pin. F6 can flip the wrong way if a minority true page becomes a corroborated oppose — good — or if a crank pair vetoes a true install — bad, and why the age gate on the veto source matters.

**Cost:** retrieval changes, more fetches (budget), re-measurement of HL-4. Medium. This is the highest-leverage change per line if M3 is actually “top 3 poisoned.”

**Regression:** T1 if cranks can veto. The guard is the corroborated-and-aged oppose rule. T4 may veto during the period when old and new fillers both still have diverse support; that veto is desirable under a conservative bar. T3 is at risk if widening the net pulls in two young paraphrases you misread as rivals. Keep rival detection on the closed template list plus your existing explicit-negation scan, not open-ended NLI.

### Rank 5 — Minimum origin age via CT and first crawl, as a tax, not a wall (extends HL-13, mostly new)

**Rule:** each corroborating eTLD+1 must have a first CT precertificate or first pinned-crawl appearance ≥ 365 days before `t0`. No clustering test beyond that (clustering is the part they evade for free by staggering).

**Kill:** F1 and any impatient ring. F2, F3, F4, F5, F6 pass. So on the hard battery this kills one fixture and taxes the rest. Worth it because the LOC is small and the fixture it kills is common.

**Cost:** CT-log inclusion proof or a pinned CT summary, ~100–200 LOC. Do not call live WHOIS in the decision path.

**Regression:** a true claim whose only three publishers are all younger than a year. Real for new organizations. Guard: allow the age requirement to be satisfied by 2 of 3 origins, not 3 of 3, and measure on your honest install log how many T fixtures have a youngest domain under a year. If T3 often does, drop to “median age ≥ 365” or apply only to templatic claims.

**Evasion price:** ~$15 × k and 12 months, paid in advance. Survives lazy attackers. Does not survive patient ones. Say that in the design doc so nobody treats it as a wall.

### Rank 6 — Pinned primary for a closed class (oracle, not a host function)

**Rule:** for templates you have a versioned registry for (capitals, element data, SI definitions), the registry filler is a veto no web quorum can outvote, and a web quorum that agrees is assertable. Registry is an input artifact, pinned, not fetched live.

**Kill:** F1, F4, and F6 *in class*. This is the only rule on this list that kills S1, and only inside the class. F2 uncovered. F3 uncovered unless you also pin a news ontology, which you should not.

**Cost:** the data and the mapping, not the code. Maintenance dominates: a stale registry manufactures T4 regressions. Version it and attach an expiry to each record.

**Regression:** T4 when the pin is stale; anything you mapped wrong. Guard: registry records carry `valid_from`, and supersession uses the record, not crawl folklore. Out-of-class claims never consult it, so T2/T3/T5 are untouched.

This is “changing the architecture” in a small box. It is justified exactly where S1 is intolerable (reference facts) and unjustified as a general policy.

### Rank 7 — Surprisal-conditional cluster collapse (HL-10 aimed only where independence is implausible)

HL-10 failed because it collapsed T5. Restrict it.

**Rule:** if the normalized sentence has ≥ N tokens (start at 25) or ≥ 2 rare proper nouns plus a specific predicate, and ≥3 domains exact-match it, and you cannot find a pre-attack archived presence of that exact sentence predating the youngest domain, then count those domains as **one** cluster toward quorum. Short templatic sentences are exempt (handled by rank 1). Old archived long sentences are exempt (they are how real technical facts propagate).

**Kill:** a long fabricated sentence copied across a ring (a common M3 shape that is *not* your short proper-noun residual). F1 exempt. T5 exempt if the wire sentence is either short or, if long, you additionally exempt clusters whose members all cite one canonical URL or all carry a shared `rel=canonical` / wire slug. If you cannot implement the citation exception cleanly, do not ship this rule: you will re-fail HL-10 on long true wires.

**Cost:** medium. A deterministic sentence featurizer, citation-edge extraction.

**Regression surface:** T5-long, and a true long sentence that independent authors really did all write identically (statutes quoted in full, a definition copied from a spec). Guard: if the sentence is a substring of a pinned spec or statute, do not collapse. Falsify with T5, with three sites quoting the same RFC sentence (must pass), and with three new domains sharing a 40-word fabricated biography (must collapse to one and fail quorum).

**Evasion:** shorten the lie until it falls under the template machinery, or quote a real spec and only swap a number — and numeric conflict is already in HL-4, so swapped numbers in a real spec quote should already die if any fetched copy keeps the original number. That interaction is worth an explicit fixture.

### Rank 8 — Campaign burn list, deterministic, post-hoc (not in HL-1..HL-13)

Single-shot S3 cannot be stopped. Repeated use of the same origins can.

**Rule:** every asserted claim is hashed; a deterministic subset (hash mod N) is queued for later review, human or oracle. If a claim is later dropped because a rival filler won or a registry contradicted it, every eTLD+1 in that quorum is written to a pinned distrust list for 365 days, *unless* archive divergence shows the page used to say something else (treat as S4 victim, drop the claim, do not burn the domain). Quorum membership of a distrusted domain does not count.

**Kill:** not F2 the first time. The second campaign on the same infrastructure. Raises the cost of a *series* from “age k domains” to “age a new k domains per caught claim.” Does nothing to an attacker you never catch, so it inherits the detection limits of ranks 1–2 and the oracle.

**Cost:** operational, not LOC. The LOC is small. The review budget is the cost.

**Regression:** a legitimate site that was compromised (you must take the archive-divergence branch seriously) and a legitimate site that published one retracted wire sentence (burn is harsh). Guard: burn only on templatic rival-filler contradictions or registry contradictions, never on a single retraction of news copy. T5 must not be able to burn four newspapers because a reviewer disliked the sentence.

### Rank 9 — Higher k only for substitutable templates

**Rule:** templatic claims require 5 distinct qualifying eTLD+1, not 3. Non-templatic stay at 3.

**Kill:** linear tax. F1 dies if they only bought 3. An attacker with 5 sites walks through. F6 dies less often, not more: entrenched falsehoods have the *most* sources. Higher k makes S1 worse. Do not apply it outside templates.

**Regression:** true templatic long-tail with only 3 publishers. Measure before shipping. If your honest capital-style facts almost always have ≥5, this is nearly free. If T3-like facts are templatic and thin, it is expensive.

### Rank 10 — Thin-site and skeleton hygiene, explicitly lazy-only

**Rule:** each origin must have ≥3 indexed pages and ≥5 main-text sentences on the claiming page, and the three DOM skeletons (tags only) must not be identical.

**Kill:** one-page copy rings and one shared theme. A competent attacker clears this in an afternoon with three generators and filler pages. Ship only if the LOC stays under ~100 and you already have the DOM. Do not count it in your residual-closed metric. Falsify by requiring that a hand-built diverse 3-site ring still installs a true T3 sentence, so you prove you didn’t accidentally make it a wall.

### Expected kills on the battery, summarized

| Fixture | What actually kills it | What does not |
|---|---|---|
| F1 impatient proper-noun | Rank 1, and usually 3, 4, 5 | Waiting alone, if they stay up |
| F2 aged novel falsehood | Nothing at this layer | Age, links, k, staging |
| F3 wire, corrected 48h | Rank 2 | Host features, HL-10-style dedup (you correctly refuse the regression) |
| F4 archived filler flipped | Rank 1, often 4 | Domain age, link mass |
| F5 new sentence on real sites | Rank 2 only if it disappears or a rival arrives | Everything host-shaped |
| F6 entrenched false consensus | Rank 6 if in class, else nothing | All web-shape rules, which *prefer* F6 |
| T1–T3, T5 | Should live if guards hold | Rank 7 if you forget the citation/spec exemption; rank 4 if cranks veto |
| T4 supersession | Lives only if era-split or registry `valid_from` exists | Naive “archive wins” |

If you can only build three things: rank 1, rank 2, rank 4, in that order. Rank 5 is cheap and should ride along. Rank 6 is how you actually close S1 for the facts you cannot bear to get wrong.

## 4. Pre-mortem, then the case against my own top ranks

### Adaptive attacker who has read this

**Against rank 1.** Cheapest adaptation: never assert a filler that conflicts with pinned snapshot C. Attack only claims with empty archived filler sets. They cannot edit C. Cost of the adaptation is opportunity, not money: the Canberra/Venus attack is retired, the fabricated-biography attack is not. Second adaptation, slower: plant the false filler and wait until *you* roll the pin forward so C now contains them. Mitigation you should write down: a pin roll must not treat newly appearing fillers as dominant over an older dominant filler unless the supersession rule fired. Otherwise your maintenance cycle is the exploit.

**Against rank 2.** If they own the origins, leaving the pages up is free, and an obscure claim is never contradicted because nobody else publishes on it. Staging then promotes F2 on schedule. The adaptation costs nothing. Staging is not an M3 defense and I should not describe it as one. It is an S2/S4-revert defense.

**Against rank 3 and 5.** Pay the calendar. A serious operator pre-ages a pool of domains and a pool of sentences the way they pre-age cookies. After the pool exists, marginal cost per claim returns to “write three pages.” The defense is a one-time delay on the *campaign*, not on the *claim*, once they pipeline it. Detecting pre-aged pools (many domains, little traffic, sentences that appear in no other context) is exactly the thinness/link signal, which they answer with filler content and cheap links. You are in an arms race you do not win on features; you only win on whether their pipeline is worth more than the damage.

**Against rank 4.** Publish two young domains that assert a rival of the *true* sentence so that, if your oppose-threshold is “any two,” you veto T1. That is the suppression dual of M3. The age gate on oppose is load-bearing; if you drop it, widening retrieval makes censorship cheaper than poisoning. Their adaptation to the age gate is to put the false rival on two aged domains — back to the price card. Also: if oldest-archived is queried by a template the attacker can influence (query poisoning of your own retrieval), they will try to make the archive lookup miss. Keep the archive lookup keyed by the parsed template from the candidate sentence, not by a search-engine query string.

**Against rank 6.** Attack outside the class, or poison the registry’s update process, or win during staleness (T4 window). A public list of pinned facts is a map of what *not* to bother forging and, equivalently, of which neighboring unpinned facts you will accept. Attack the neighbors: “deputy capital,” “largest city,” “capital in 1901,” near-template paraphrases your closed parser does not slot. Parser-gap attacks are the cheap adaptation. Mitigation: out-of-pattern near misses (small edit distance to a pinned template, different filler) go to SOLID and to audit, not to FAST assert.

**Against rank 7.** Shorten the sentence, or copy a real statute and only change what HL-4 already catches, or add a fake shared citation URL so you grant the exemption. The citation exemption must require the cited URL to actually contain the sentence and to be older, or you have built a bypass.

**Against rank 8.** One claim per burned pool, and never reuse. Or stay under the review sampling rate: if you review 5%, they accept 95% survival and you will statistically under-burn. A deterministic hash also means they can grind the sentence (add a comma your normalizer doesn’t strip — but HL-7 is conservative, so they cannot) or grind the origin set until the claim hash falls outside the sample. **Hash-mod sampling is gameable if they can vary any bit inside the hash preimage.** Include only the normalized sentence in the hash, not the origin set, and accept that they still can choose synonymous sentences until one misses the sample — except exact-match quorum makes grinding sentences expensive, because every variant needs its own full quorum. That tension helps you. Still, an attacker who needs one specific sentence either gets sampled or doesn’t; this is not a control, it is a tax on repetition.

**Against rank 9.** Buy two more domains. Or, for S1, do nothing and enjoy the fact that you just made the false consensus more eligible.

**What survives a competent attacker:** rank 1 against any claim with a frozen rival filler; rank 6 inside a maintained class; rank 2 against falsehoods somebody else corrects; rank 4 against rank-manipulation specifically. **What survives only a lazy one:** rank 10, ASN/CMS coincidence, burst windows under a month, stylometry, skeleton hashes. **What becomes a prepaid pipeline rather than a wall:** ranks 3, 5, 8, 9.

### The strongest case that my two highest ranks are wrong

**Rank 1 is the wrong kind of clever.** It does not read truth. It reads “what was the dominant filler in snapshot C.” That equals truth only for facts that were both true and widely published before C, and that have not legitimately changed. Every one of those conditions fails somewhere you care about.

Archives are a biased sample. Common Crawl under-represents paywalled, new, non-English, and JS-rendered pages. “Dominant in C” can be “dominant among sites a crawler could fetch,” which is how a falsehood that was easier to crawl becomes the veto against a truth that lived in PDFs. `Save Page Now` and attacker-triggered archival mean a motivated party can write the archive going forward; immutability is not the same as ungameable first-write. If your pin ever includes post-attack snapshots without an era split, the attacker authors the oracle by waiting.

T4 is not a corner. Capitals move, companies rename, scientific categories get revised, officeholders change. A rule that cannot represent supersession will either freeze the past or require a maintenance process as fallible as the original problem. And the fixtures you will be proud of — Canberra, Mercury — are the easy, stable, famous ones. They will pass tests while the production harm is frozen stale facts and a false sense that R3/R4 is closed. It is closed only for “filler swap against a frozen famous fact.” Your own impossibility proof still owns every other sentence shape. Shipping rank 1 without putting that sentence in the design doc is how the next round gets wasted re-deriving S3.

There is also a determinism trap. Live archive APIs are not replayable. The moment someone “just checks Wayback” inside the decision path, byte-identical reruns die. If the pin is stale by design, you have built a clock that runs slower than the world, and every legitimate change looks like an attack until a human rolls it. That human is now the integrity mechanism. Rank 1 secretly relocates trust into pin discipline. If you do not staff that, you should not ship it.

**Rank 2 is a latency tax that misses the residual you named.** Re-read the wall. M3/R3/R4 as you defined them are owned diverse sites asserting a sentence with no negation surface. They will still be asserting it at day 30. Rank 2 promotes them. The fixtures it kills, F3 and reverted vandalism, are real but they are not the overlap your prereg calls architecture-inherent. You already separated S2 in the steelman as a different object.

What you pay is on every claim: doubled fetches, a state machine, replay logs, and a product argument about whether T2 at day 0 is a regression. Under a literal zero-regression bar that includes freshness, rank 2 is forbidden and its kill rate on the actual residual is ~0. Under a bar that ignores freshness, you still have not touched F2 or F6 or persistent F5. It is easy to like because it changes the game. The game it changes is not the one you are losing.

The failure mode inside the mechanism is worse than “no effect.” If DROP on disappearance is implemented sloppily (404 counts, normalizer drift counts, one origin’s CMS rewrite counts), honest claims flap and you will either oscillate or add exceptions until the rule is HL-11 with extra steps. A correction window implemented as “re-fetch the same three URLs” never sees the dissenting fourth page. Unless rank 4’s wider retrieval also runs at revalidation time, the window only observes self-retraction by the attacker, which a competent attacker will not do.

If I demote my own ranking honestly: rank 1 stays first **for the narrow class “templatic swap against a frozen filler,”** with the supersession hole treated as unfixed until era-splitting is tested on real renames. Rank 2 drops below rank 4. The thing I overvalued is waiting. The thing the steelman got right is that waiting does not create information the attacker’s own pages refuse to emit.

### What is truly impossible at this layer

Precise list, after giving the defenses every reasonable feature:

1. **S1, entrenched false consensus outside any pinned oracle.** No web-derived feature will mark it false, because the feature vector is the prototype of “true.” Closing it means an oracle that can contradict the web, or a change in what install means.
2. **S3, novel claims where the attacker is the first diverse consensus and outwaits your age gate.** Observationally identical to T2/T3 once time has passed. A consensus rule *should* install these. A truth rule has no data.
3. **S2 inside the window before any fetched source corrects, if you refuse to delay assert.** If you do delay, uncorrected S2 (nobody noticed, or the correction is phrased so your matcher misses it) collapses back to S3/S1.
4. **S4 that only adds a sentence, on sites you would have accepted, with no rival filler and no retraction.** The compromise is invisible to content corroboration because you never saw a pre-state that conflicts. Archive absence is not evidence: most true sentences are also absent from any given snapshot.
5. **Parser-gap neighbors of any oracle you pin.** Whatever template you can slot, a near-paraphrase you cannot slot falls back into (2).

None of these yield to another host function, another linguistic threshold, or a higher k.

### What you would have to change in the architecture

Not the quorum predicate. The predicate is doing what predicates of that type can do.

**Up, into selection.** Fetch a set the attacker does not choose: pinned-crawl hits and oldest filler for the template, unioned with ranker results, decision order-independent on the union. This kills M3-as-ranking and is the precondition for rank 1 seeing anything. Couple it with corroborated, age-qualified contradiction so you do not hand the attacker a cheap veto. This does not touch S1 or aged S3.

**Down, into what install means.** Stop promoting consensus to a bare proposition. Persist “these origins asserted s at pin C” and let consumers bind their own trust. Then a false quorum is a true record of a false assertion, which is a different and non-catastrophic object. If a binary fact store must remain, split it: FAST is never asserted as fact, SOLID is asserted only with its evidence pointer, and a third state ORACLE-BACKED exists only for the pinned class. The impossibility result is specifically about the function “consensus → bare true.” Delete that function and the theorem has nothing to bite. This is the only move that addresses every sub-shape at once, and it does it by abandoning the claim that caused the trouble, not by detecting lies.

**Outside.** A versioned registry for the closed classes where S1 is intolerable. A human or paid review market on a deterministic sample, with the burn list, knowing it only prices campaigns and only after a truth signal arrives from somewhere else. World time, used as claim-age, buys delay and nothing more. None of the outside signals are functions of the quorum’s current pages, which is why they can work.

### Direct answers

The steelman holds for S1, for uncorrected S2, for aged S3, and for non-conflicting S4. It does not hold for impatient proper-noun swaps against a frozen rival filler, or for rank-only M3, once \(\varphi\) is allowed to include pinned pre-attack history and a candidate set the ranker does not fully control.

No signal class you listed separates unanimous-false from unanimous-true among diverse sources when the attacker can choose to look like the honest new-fact distribution and is willing to pay calendar time. Temporal and archive signals dent the impatient and the rewrite-of-an-old-fact subclasses even against a competent attacker. Provenance, linguistic, behavioral, and cryptographic signals, as available on the open web, are either cheap to diversify (tens of dollars and an afternoon, or a year of lead time) or are absent in honest data so you cannot require them. Social correction signals dent only falsehoods the outside world bothers to correct. Economic signals change price, and after the attacker pipelines the price they mostly change which true long-tail you also drop. Several of the price increases nudge a smart attacker toward hoaxing one real publisher or renting one real page, i.e. toward S2/S4, the region the theorem actually owns. That shift can erase the practical gain of a clever quorum rule.

The residual I would stop trying to filter my way out of: a diverse, aged, uncontradicted, first-moving false consensus, and any long-standing web consensus that is simply wrong. Those are not corroboration bugs. They are what corroboration measures. Close them by pinning an oracle where you can stand behind one, and everywhere else by storing “who asserted this, when, under which pin” instead of “this is true.”
