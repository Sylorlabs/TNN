# EVIDENCE: CV-1 decline-citation fix re-test (wave-20260924-1721pdt)

Worker: TNN RSI loop subsystem worker (implementation and testing only).
Date: 2026-09-24. Branch: tnn-native-lab. Pure Zag plus shell coreutils.

## 1. Provenance and commit order

- Prereg freeze: dad5ef955 (PREREG_CV1_CITE_1721.md, committed alone).
- Probe/key seal: b1951de11 (sealed/, committed alone, after the prereg).
- Implementation and evidence: this commit, after the seal.
- Order check: prereg commit strictly precedes seal commit strictly
  precedes first implementation commit. PASS (no UNVERIFIABLE ORDERING).

## 2. Toolchain and frozen fixtures

- Toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1 verified before
  use: sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (expected prefix 498abcb5).
- KB fixture impl/runs/kb.txt: sha256
  3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1
  (matches the frozen KB). gaz.txt copied alongside (sha256
  b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a).
- Build (pinned toolchain, same flags as 1421pdt):
  znc cv1c.zag --no-zagd --no-analyze --no-foreground-cache -o cv1c
  znc gate_op.zag --no-zagd --no-analyze --no-foreground-cache -o gate_op
  Both built clean, exit 0.

## 3. Implementation (impl/): byte-inherited, UNCHANGED

Base: byte copies of the 1421pdt committed sources (commit 5c53da6ba),
verified sha256-identical before building:

- cv1c.zag:
  6d8fb9f013ef3efa1bb44881f98cbeafcabd7110ae4fb7396a3e5721b34d7137
- gate_op.zag:
  730db584c81c5229fa110069e57b54f5a36b91b5ca8e080de2bb61c65349a33f
- R33_NATIVE_SHA256_V2.zag and R33_NATIVE_IO_V1.zag: byte-identical to the
  1421pdt committed blobs (imports required by both mains).
- runs/kb.txt, runs/gaz.txt: byte-identical to the 1421pdt fixtures.
- runs/inkb17.txt, runs/adv30.txt: the 1421pdt unsealed training inputs,
  reused byte-identical (unsealed training artifacts, not sealed probes).

The three prereg-specified rule edits on the adopted 1121pdt cv1.zag are
inherited unchanged (quoted from the 1421pdt record):

1. cv_cite: the 3-word cap is removed. Declines cite the full uncovered
   list.
2. deliberate_cv1: per-turn-word any-fact coverage flags (anyhit), set
   during the unchanged 38-fact coverage scan.
3. Decline path: names ALL turn content words with anyhit==0 (the global
   uncovered set), in turn order, in the frozen template sentence; the
   atomic-verification fail-closed path emits the no-verification text
   (names no words); the empty-uncovered fallback emits the truthful
   no-single-fact text (F9 keeps it off the sealed set).

The answer path (single-fact coverage, lowest-index selection, F8
verification, frozen emit) is byte-untouched. No probe-informed change of
any kind was made; the diff against the 1421pdt committed sources is empty
by construction (sha256-verified above).

## 4. Training battery (CVC-B5)

- INKB-17 (17 fresh in-KB questions, unsealed training inputs): candidate
  transcript byte-identical to the frozen baseline binary
  (tnn_chat_decline_frozen_ref) on identical inputs. sha256
  db6b707550865331666a2cf52d3c930a359c1d114ddf41f11a84656dbef4e7d5
  for both (matches the 1421pdt INKB sha: identical inputs, identical
  behavior). 17/17 PASS.
- ADV-30 (30 fresh adversarial training probes): 30/30 specific declines
  ([decline] marker, frozen template, at least one quoted word each),
  0 blanket refusals. All 105 distinct quoted words machine-checked absent
  from kb.txt (case-insensitive whole-word grep): 0 covered words named.

## 5. Disclosures

1. Python contact: none. No Python was invoked anywhere in this task
   (authoring checks used grep and awk only; scoring uses the Zag
   binaries and shell coreutils).
2. Author/implementer separation: the sealed set was authored and committed
   before implementation; the implementer attests it never opened, read, or
   listed sealed/ during implementation; the implementation is a byte-copy
   of the 1421pdt committed sources built after the seal commit; no
   implementation change followed the seal. The mechanism contains no
   per-probe branches.
3. No push to GitHub (local commits only). Google Drive untouched. No
   spend, no publish, no contact with outsiders, no irreversible
   commitments. Micah's frontier files untouched. The sealed judge queue
   untouched; no governance ruling made or prejudged.
