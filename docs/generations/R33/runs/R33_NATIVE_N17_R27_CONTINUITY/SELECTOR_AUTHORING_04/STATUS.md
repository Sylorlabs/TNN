# R33-N17 selector authoring V4

Status: **COMPILED; EXECUTION PENDING**.

The frozen V4 source compiled successfully under the pinned macOS-arm64 Zag compiler. Binary SHA-256: `7896e52dca3cad189facbcb60b019083264ed8c7a0380e2ad6dbc588e249d0d8`; compile stderr is empty. The authoring probe has not yet executed, so no selector output, parent canary, digest, verifier, or continuity credit is claimed.

V4 is deliberately narrower than a continuity verifier. It traverses only
descriptor structures consumed by the recovered historical R26 digest:

- `entity_head.net.state_dict()` parameter-bearing module children;
- `graph.nodes[*]['views']` descriptors;
- `name_memory.docs` reducer argument dictionaries containing motif/count data;
- both abstraction-model `centroids` trees containing motif/weight data.

It imports the existing inert-map identity layer and must not execute Python,
pickle reducers/classes, historical verifiers, learner code, training, or
promotion. Successful execution is only selector/layout authoring evidence.
Canonical R27 must remain byte-identical before and after the probe.
