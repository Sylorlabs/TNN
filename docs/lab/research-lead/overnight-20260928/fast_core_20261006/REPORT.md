# Frozen TNN-2 interface audit - expected is selection feedback

Date2026-10-06. Prereg e74248485. Engine source compression_exec/tnn2_frozen_ref.zag
prefix unchanged byte-for-byte. This executes a frozen integrated reference engine,
not an artificial replacement learner. It is not proof latest production is identical.

QUESTION: does expected influence first returned answer, or only post-return learning?
Same four observed facts produce two valid path terminals31 and32; query relation99
has no observed semantics. All five arms start independently with identical facts.

| expected / flags | returned answer | learned MAP count | trial tried / rejected |
|---|---:|---:|---:|
|31 /0|31|1|1 /0|
|32 /0|32|1|2 /1|
|-2 /0|-2|0|6 /6|
|-2 /1(masked)|31|1|1 /0|
|9999 /0|-2|0|6 /6|

Header16 encodes tried*1024+rejected. Results identical under subject/relation ID
rename offset1000. Once31 is learned for relation99, repeated query with expected32
returns31 from activation; novel relation100 with expected32 returns32.

CAUSAL INTERPRETATION: expected changes first candidate acceptance, promotion and
returned answer before query completion. In this API it is supervised search feedback,
not strictly post-return/post-hoc-only relative to the reported answer. Masking removes
that answer condition and accepts first executable route; this is a source-order
choice, not evidence the unknown query was correctly understood.

WORLD LIMIT: the observations do not identify what relation99 should mean. No
learner can infer a unique intended endpoint without extra semantics/evidence.
Therefore absence of autonomous answer here is NOT a general TNN intelligence failure.
Providing answers is legitimate during acquisition; evaluating uncached autonomous
behavior while providing those answers would be a misleading capability test.

What killed: literal post-hoc-only interpretation of this reference's expected field.
Not killed: supervised learning, graph execution, current production TNN, general
adaptive architecture. Cached reuse31 after feedback changes also does not establish
revision: expected32 is not an observation/contradiction event in the tested protocol.

Verification: three fresh compile-gated runs; nonempty byte-identical stdout, compiler,
original prefix/source/binary/output hashes recorded; PURE-ZAG-CLEAN. No legacy
script, stale binary, production edit, or score suppressions. Prefix cmp verified.
No performance/scaling claim. Synthetic small world, not independent human replication.

NEXT: training observations with feedback, then heldout queries with expected-2 and
identifiable transferable query semantics; facts-retained/MAP-erased versus intact.
First qualify core's representation can express that law. Do not project microlearner
120/120 or protocol972/972 into this engine without an actual adapter and test.
