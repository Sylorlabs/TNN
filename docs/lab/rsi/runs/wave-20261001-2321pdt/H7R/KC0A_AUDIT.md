# K-C0A AUDIT: zero new semantic cases (H7R, wave-20261001-2321pdt)

Scope: the code appended to the adopted prototype substrate for this experiment:
h7r_consumer.zag (the re-derivation consumer, frozen spec H7R_PREREG.md section 2)
and h7r_driver.zag (sealed worlds plus measurement). The substrate itself
(substrate_proto.zag) is extracted byte-identical from commit a11dde4b9
(sha256 77303b829516e95489a0c9be97dbbe0d7a1bf8cb84b2b8025591bb609772eede,
verified equal to the committed TNN3-SUBSTRATE file) and unmodified.

Definition used: a semantic case is a branch in the adopted code whose condition
tests domain content (a world relation code, entity id, or fact value) rather than
structural metadata (node tags, field offsets, edge types, ticket markers,
status codes, loop bounds) or live learner state positions. Measurement scoring
(comparing a probe result against the world's expected value) is not a semantic
case: it changes no architecture behavior, only pass/fail flags.

## Finding: zero new semantic cases. PASS.

### 1. Authorship separation (prereg section 2c, literal grep)

`grep -c "lb_ticket_new\|lb_step_add" h7r_driver.zag` = 0. The sealed driver
never authors tickets. All ticket authoring (5 calls: 2 lb_ticket_new,
3 lb_step_add) lives in h7r_consumer.zag, the frozen-spec generic consumer, whose
ticket content is read from learner state (fact fields, stale ticket steps).

Note: dev_checks.zag (adopted substrate) authors tickets in dv_v1 as an
explicitly labeled stand-in for the service check; it is substrate
re-verification (B1/V1 re-runs), not part of the sealed experiment's authorship
claim.

### 2. Consumer conditionals: all structural

Every `if(` in h7r_consumer.zag branches on: BUILD_ROOT presence, edge
liveness/type/target, node tag (1/904), ticket markers (-41/-43), ticket status
(0/1/2), allocation failure, or the substrate's own supersession signal
(is_superseded). The single value comparison (h7_respec: spec == ng(W,oldn,28))
tests a ticket operand spec against a live learner-state value (the superseded
fact's field28), never against a domain constant. No world-table constant
(61/62/63, keys 101-126, values 201-256) appears anywhere in the consumer.

### 3. Driver conditionals: scaffolding, structural, or measurement

- World tables (h7w_R, h7w_ck, h7w_cvold, h7w_cvnew, h7w_dk, h7w_duold, h7w_dunew):
  branch only on the world index (wn == 1 / wn == 2). Domain constants appear
  solely as return values, never in a test. Classification: world-selection
  scaffolding.
- Ticket counting scans (h7_rdcount, h7_bcount): tag/marker/edge-type checks.
  Structural.
- h7_linkok: edge/tag/supersession checks are structural; the final check that
  the linked new fact carries this event's (k, vnew) is measurement scoring.
- h7_sigdiff, h7_probe: measurement.
- Protocol asserts and bar checks (h7r_main, h7w_run): comparisons of counts,
  probe values, and bar thresholds against expected values. Measurement only;
  they set ok/pass flags and emit text.

No architecture branch anywhere in the appended code tests a domain constant.
In particular, no branch discriminates on the relation codes 61/62/63, on any
key, or on any fact value to select behavior.

### 4. No new types or markers

- Node tags written by appended code: only 902 (probe frame node; pre-existing).
  Tickets/cells/facts reuse 904/101-104/1.
- Edge types used: 4 (ET_REF), 10 (ET_MEM). Pre-existing.
- Relation markers: -41 (R_BUILD), -43 (R_REDERIVE) only, both from the package.
  No -44, no new codes.
- Ticket status value 2 ("superseded by re-derivation", h7_rederive_one) is
  learner-state bookkeeping in the consumer, read only by white-box asserts;
  lb_run and every substrate scan treat it as non-pending, identical to 1.

### 5. Method note

Audit performed by committed-source grep on the exact files built into
h7r_proto.zag (grep outputs quoted above, verified against the committed
sources). The frozen tnn2.zag core is untouched; the prototype substrate is the
TNN3-SUBSTRATE package as committed, adopted read-only.
