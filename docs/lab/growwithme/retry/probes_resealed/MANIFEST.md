# Re-seal manifest (2026-09-27)

Old probe ID → new paraphrase question text + SHA-256 of the new question text.
Keys are unchanged from the frozen set (see frozen `probe_keys.md`).

## COMP-01
old Q: Which znc pipeline pass must run before intrinsic-lower, and what breaks if the order is reversed?
new Q: Before intrinsic-lower, which znc pipeline pass has to run — and what fails when the order is flipped?
sha256: `a3ed5d7ffddfda024c2752245004866da3856390e8873f763c524473a39d4234`

## COMP-02
old Q: An audit entry shows stage=9 and a nonzero d2 word. What does this entry mark, and what does the d2 word carry?
new Q: You see an audit entry with stage=9 and d2 nonzero. What is this entry marking, and what rides in the d2 word?
sha256: `5e1e59eb9f4d3be39b82132dc1521ffca2ea6e70afd8652b3cf1714aeafc49ca`

## COMP-03
old Q: A tier-3 memory's cite count sits below the sweep's eviction floor. What happens to it at the consolidation sweep — deleted, kept, or something else?
new Q: A tier-3 memory's cite count is under the sweep's eviction floor. At the consolidation sweep is it deleted, kept, or what?
sha256: `c1ec46689d780d85262f5e4fc542442b1d9c8bf20bb123b282b4a3a298ea4421`

## COMP-04
old Q: A consolidation trace cites slot 12, but the decision never read slot 12. What does the G7 audit conclude about this turn?
new Q: A consolidation trace names slot 12, yet the decision never read slot 12. What is the G7 audit's verdict on the turn?
sha256: `2b6b8e36cb8e4ff58794b5c2e2b748bab1bb266546d5d7f3c19d101b4fee99dd`

## COMP-05
old Q: Leg M1's stdout SHA diverges from REPORT.md, but its verdicts reproduce. Under the scale-rot amendment, what must happen next and from what inputs?
new Q: M1's stdout SHA has drifted from REPORT.md while its verdicts still reproduce. Per the scale-rot amendment, what comes next and from which inputs?
sha256: `4ccac2388cbe4809f8ff062406dcccde071236f7f83714209876c569c52e6eea`

## COMP-06
old Q: A PENDING claim appears verbatim in a chat answer, but no probe answer states it as fact. Leak or not — and why?
new Q: A chat answer quotes a PENDING claim verbatim, though no probe answer states it as fact. Is that a leak? Explain.
sha256: `ceef10bb3a19fc243fa82c4c5c7e8da60a6c016286f2c362c1db99424506e14e`

## COMP-07
old Q: The researcher corrects a fact that consolidation had promoted to a strong tier. What must the audit show for this overwrite, and what would count as a violation?
new Q: A fact consolidation had promoted to a strong tier gets corrected by the researcher. What must the audit record for that overwrite, and what would be a violation?
sha256: `7d4a5da6f85fd71d123f2d8a8c2c1c5f8f4c5b3455bd247d8fa44552364c0dd2`

## COMP-08
old Q: A draft memo claims PENDING items auto-install after 3 sessions. Which taught facts does this contradict, and what is the required handling?
new Q: A draft memo asserts that PENDING items install themselves after 3 sessions. Which taught facts conflict with this, and how must it be handled?
sha256: `9a8342566e2cc06317bb15e5e4322cadcf02874ad2a2a7eb7b0fad4125d3ed4d`

## COMP-09
old Q: Where does the pinned toolchain live today, and why must lab builds use the pinned copy rather than a system install?
new Q: What is the pinned toolchain's current location, and why are lab builds required to use the pinned copy instead of a system install?
sha256: `b036620ac97a9d6985e6c2aec3c34ff41aa9fc07a93eff22ad936c652ce4d1bd`

## COMP-10
old Q: How many corroborating probes does tier-2 promotion currently need, and what changed?
new Q: Tier-2 promotion now needs how many corroborating probes, and what is the change from before?
sha256: `b309bd4ee9b642cecee0bc66fe05f0df380b60323c15e7e287df9e2f01148116`

## COMP-11
old Q: A 70KB slice needs indexing. What do you do, and which two taught rules govern the answer?
new Q: You must index a 70KB slice. What do you do, and which two taught rules apply?
sha256: `50aad9a5c9bfde09d8beb807894eb8788c3ddb6c0458197c8967b002061358ef`

## COMP-12
old Q: The S5 old design doc gives a different pipeline order (intrinsic-lower before macro-fuse). Which facts win, and why?
new Q: An old S5 design doc orders the pipeline differently (intrinsic-lower ahead of macro-fuse). Which facts prevail, and why?
sha256: `9a20803f7ff5cc0df9bd1a2be2ac6306408dc54fc29cb07c05c0f76a69b5fdcc`

## CORR-01
old Q: What is the current pinned znc toolchain path?
new Q: Give the present path of the pinned znc toolchain.
sha256: `20f9fa33d747f16d1cef8a85fa445d3c61adf7310afc56a4dfe68ae9c5f40135`

## CORR-02
old Q: What is tier 3 of the memory strength tiers called?
new Q: What name does tier 3 of the memory strength tiers carry now?
sha256: `a226382939cbfab983bc82504a0a228d5f2aa6fbe2f2d6e65e29198e1774d0f5`

## CORR-03
old Q: What is the current scope of the indexed-table aliasing workaround?
new Q: What does the indexed-table aliasing workaround currently cover?
sha256: `d53fb31ebd91192e3f9850abb2479fcc255e0eafb68bd8c333c11848f4441802`

## CORR-04
old Q: What are the current write semantics of the audit ledger?
new Q: What are the audit ledger's write semantics now?
sha256: `395d4de88327675a034afce0d3b7295e552a1bfead4260986146943c94a36a36`

## CORR-05
old Q: How many corroborating probes does tier-2 promotion to tier 3 require?
new Q: How many corroborating probes are currently required to promote tier 2 to tier 3?
sha256: `94cde7def7f9b7a701d107a4e6cab1838a73bfda2f877ea353abb97cc173faf1`

## CORR-06
old Q: Is a bare `return` legal in a void fn?
new Q: Can a void fn legally use a bare `return`?
sha256: `ed06df8acc0b68a0240bb79c5edfe4d8de0a3ea25875e2ce2203046926f60f55`

## CRES-01
old Q: A contributor note says audit entries are 12 words long with the stage word at offset 40, contradicting the taught 16-word layout. How do you resolve this?
new Q: A contributor note claims audit entries are 12 words with the stage word at offset 40, against the taught 16-word layout. How is this resolved?
sha256: `991be5b866cc38160eb4777f340ee66163cafa541d34639bfc51f0199003acd2`

## CRES-02
old Q: A draft memo says PENDING items auto-install after 3 sessions without verification. Your response?
new Q: A draft memo states that PENDING items auto-install after 3 sessions with no verification. How do you respond?
sha256: `7b10dfdcd7f8689172962bec7a857f6072e1503e04904136d686ab7f86f12d34`

## CRES-03
old Q: An old design doc gives the pipeline order as parse → intrinsic-lower → macro-fuse → desugar → codegen. How do you resolve it?
new Q: An old design doc lists the pipeline order as parse, intrinsic-lower, macro-fuse, desugar, codegen. How do you resolve this?
sha256: `330dfd14c92d88551c99814de860d7eb52401eaf7064b6f1b81abe36ec473fdd`

## F1-01
old Q: State the full path of the pinned znc toolchain.
new Q: Give the complete filesystem path where the pinned znc toolchain is installed.
sha256: `4e1b6218c6856acc3254f3b851822a74ffe1df7cfe8c34d41615c70ec48a1691`

## F1-02
old Q: Where does `znc build` put its cache files?
new Q: In which location are the `.zagd` cache files written when you run `znc build`?
sha256: `e1ae69429703d6f977cda9ebbf22ca6b260b5eb906875be54752a4ccd466d220`

## F1-03
old Q: Which backend does the `--emit-wasm` flag target?
new Q: What compilation backend is selected by the `--emit-wasm` flag?
sha256: `1b33e986f816fe00de2989079130265cf51de6140085320073c992d8268a25eb`

## F1-04
old Q: What are the storage properties of Zag string literals?
new Q: Describe how Zag string literals are stored — mutability and section.
sha256: `152f733c96377c02e1a72efd180f55c8052dbeb53ab5ac4a30de2af405f611a9`

## F1-05
old Q: What is the preferred heap-allocator helper, and what naming rule applies to it?
new Q: Which heap-allocator helper should be preferred, and what must user functions avoid being named?
sha256: `ba97943dbb188fc7f60c768e8b042a7cdf9a52a704b6aef620bc621d1e073aa5`

## F1-06
old Q: Give the lab repo checkout path and branch used for TNN work.
new Q: Name the directory and branch of the lab repository checkout used for TNN work.
sha256: `507dff7aed434d15af3978d049ec4157f18b9ffcf190ade20fffa378e2325f61`

## F1-07
old Q: What does `_zag_arg(n)` return, and what must you never do with the result?
new Q: What kind of pointer does `_zag_arg(n)` hand back, and what is forbidden on it?
sha256: `5459253ea977b18693464439076efbcee79c676259bebe0058b5e2671dfb9df5`

## F1-08
old Q: What value does `_zag_strcmp(a, b)` return for equal strings?
new Q: When two strings are equal, what does `_zag_strcmp(a, b)` yield?
sha256: `0a98cee1a4a835702a9c7fc19cbe27b46ee89cf61a8b2b449bc322f9bf05e5c9`

## F1-09
old Q: How must a void function return in Zag?
new Q: What is the correct way to exit a void fn in Zag?
sha256: `fb13430fcc661af25f405e5b854b063af2d1bb9ba37d7bff6961bc9fdea568db`

## F1-10
old Q: What kind of shift is u64 `>>` in znc, and how do you get the other kind?
new Q: Is u64 `>>` in znc arithmetic or logical, and how do you obtain the other behavior?
sha256: `6ff6946e06786db77d933c02a8760536e94ecaa32df24650d9bd6a55dd64156d`

## F1-11
old Q: What is the largest indexable slice size, and what must be done with larger buffers?
new Q: Above what size does indexing a single slice panic, and how must oversized buffers be handled?
sha256: `a53233210006c643858d029abd5f55db51af34ff83f4c451e1a5a7758e73b4fb`

## F1-12
old Q: How are i32 struct fields laid out, and how do you size `_zag_malloc` for a struct?
new Q: At what stride do i32 struct fields sit, and how do you compute the `_zag_malloc` size for a struct?
sha256: `ee8a0fd3559d86c701abef5f8a64ac1fb2aca65a3516669d24931c127ffdebc0`

## F1-13
old Q: What goes wrong when freeing through a nested struct value field?
new Q: What heap failure results from freeing through a nested struct's value field?
sha256: `e770fe54ee711d4d93035efe7efc45384330d7d08f7b0f4b0e73af12856ff14a`

## F1-14
old Q: What is the safe pattern for indexed tables given the `as []i32` cast defect?
new Q: Given the `as []i32` cast defect, what pattern is safe for indexed tables?
sha256: `08d9b319da393ba183db3515c80d4a5abb7b47754b38312e2730b75d988cbe3c`

## F1-15
old Q: What is the rule for function definition order in Zag sources, and why?
new Q: In what order must functions be defined in a Zag source, and what happens otherwise?
sha256: `662a3b41f321ec6242e2be995636a0ceaedd183c040575b9b309f9dbc34cb79b`

## F1-16
old Q: State the taught ordering constraint between the MACRO-FUSE and INTRINSIC-LOWER passes and its consequence.
new Q: Which of MACRO-FUSE / INTRINSIC-LOWER must come first in the pipeline, and what does reversing them do?
sha256: `900e5c0151a575a097dbe046fb5c81a0ac0211da7f77c7397e4c3e43f8b673a5`

## F1-17
old Q: When is a ledger entry with stage=9 a promotion candidate?
new Q: Under what condition is a stage=9 ledger entry a promotion candidate?
sha256: `cfffacd1685ae63536f28f6f416f43c156e6370b19bf69ee0e9d42d4ccb71c75`

## F1-20
old Q: What is the lab rule on which znc install builds must use?
new Q: Which znc installation are lab builds required to use?
sha256: `d831711750594c695ab2c4f87acf58d22fbc982dda0b1a6d4c58dfb685dccadc`

## F2-01
old Q: How does the deliberate memory substrate organize its records?
new Q: How are records arranged inside the deliberate memory substrate?
sha256: `8a94b442770dc3b4b04d4067e5f560b56dcd43437b9dbd31d475a58ec5e9c4ea`

## F2-02
old Q: List the memory strength tiers by number and name.
new Q: Enumerate the memory strength tiers, giving each number and name.
sha256: `a155676b4d24c2d6fc6c60982da54b879f46f0f9a44ddb78ac2028b2073cee25`

## F2-03
old Q: How far can promotion move a record in one step?
new Q: What is the maximum tier movement promotion allows in a single step?
sha256: `f72da7e3a51e616b03e9e8229e5d1966e5697dc03081fdcb4cabb5640fbb91f0`

## F2-04
old Q: What does the audit ledger record for each consolidation decision?
new Q: For every consolidation decision, what does the audit ledger capture?
sha256: `a82f734abfbffb45e08322af0faeabdde00a4d053a7c73b036a9be8778702214`

## F2-05
old Q: When does consolidation run?
new Q: At what point does consolidation execute?
sha256: `2d46ad4f5527801524f0beda8fbc200935ccbd9b2de3e23fbbd931a7d53f72f2`

## F2-06
old Q: Which records does the consolidation sweep drop?
new Q: What kind of records does the consolidation sweep discard?
sha256: `6c9ae94d94769c43453f0532c4f4cf0617908858030eba929f42deada7f57264`

## F2-07
old Q: What does a tier-2 record need for promotion to tier 3?
new Q: What is required to promote a tier-2 record to tier 3?
sha256: `9468488f1a3ca748ef1396e41b0a3c67a4f543ada6949e73f41b1e7c9f4fc11f`

## F2-08
old Q: What are the write semantics of the audit ledger?
new Q: Describe the audit ledger's write semantics.
sha256: `914a0cf509fe418f3b8411573b8f75a206df7daaa41d2f5aae118b0e409cf4d4`

## F2-09
old Q: What provenance does each memory record carry?
new Q: Which provenance fields ride along with each memory record?
sha256: `6114d4650c33e0ae3b303b0655feaa8875d237e7a36d7ab9a616651b00c48c8b`

## F2-10
old Q: How is a memory's strength set — and what is explicitly forbidden?
new Q: What determines a memory's strength, and what determination method is banned?
sha256: `a31a9fb2ddcb28d387f8317d616dc7352a40e6cb04ff663202a68b664af0fba0`

## F2-11
old Q: What does scoped deletion remove?
new Q: What exactly disappears under scoped deletion?
sha256: `911ec12313779a9c8e8d3815471a6dd794cbc8b838289c646681a73d5a15ae46`

## F2-12
old Q: What information is recorded in the correction-state mirror?
new Q: What does the correction-state mirror keep track of?
sha256: `2de0ed2bbbdbf0a7b1e3b63ed1512e515d494abd2a43b3e90f89ae2209393d77`

## F2-13
old Q: State the taught survival condition for a tier-3 memory at the consolidation sweep.
new Q: What must hold for a tier-3 memory to survive the consolidation sweep?
sha256: `a008949056e78c7a461a395148107b694f777c54a77a84ff1dd590786a492ca5`

## F2-14
old Q: State the taught G7 neuter-audit failure condition for a turn.
new Q: Under what condition does the G7 neuter audit fail a turn?
sha256: `8c9fa48f055043ac962919624b94e7463448eae04ae290808ddb32bb61f49aea`

## F2-15
old Q: Where are deliberation traces stored?
new Q: Where do deliberation traces live?
sha256: `51846c1382d1c4acb3a28f47629f4cc3bc3b98b2488b6a0cfc8043d2a03587ec`

## F2-16
old Q: Can the researcher see a memory's strength tier?
new Q: Is a memory's strength tier visible to the researcher?
sha256: `6aaf5297aa4b59b74ad1a09f488781d50c9d166f8fef21d7137956d3d24275ed`

## F2-17
old Q: What state does the substrate capture at each session boundary?
new Q: What does the substrate snapshot at every session boundary?
sha256: `a2613b392406d82f7b24748944b2a7b418b606f4beda9487d6136c4dbce6daef`

## F2-20
old Q: What is force-pin and what are its visibility properties?
new Q: Describe force-pin and whether it is visible and audited.
sha256: `8c922d4f22aec2fbf976d1f785023d36f99f0e5cf16ad544119fb7de92a7d84c`

## F3-01
old Q: Through which gates does every intake turn pass, in order?
new Q: Name the gates every intake turn traverses, in sequence.
sha256: `7ce5894ba5a3209e264e0a8f48803ee88a3df17c028e7794a4c576f34a8590d2`

## F3-02
old Q: What inputs does G6 reject?
new Q: Which inputs get rejected by G6?
sha256: `8adc46e8061a5e2d1b063c4c0e76a498f9507c3385f20e0f68b3ae291aafa79c`

## F3-03
old Q: What is the entity scanner's job?
new Q: What task does the entity scanner perform?
sha256: `21d10b041ab7ef4dac69717fbdf7c99a9fec8ad42b22a3fb30a3555827d48181`

## F3-04
old Q: What is a unit?
new Q: Define a unit.
sha256: `102665a82e731e7f49685a3c7ccbc56310a3ba70b74a812efb9a5f334c94a222`

## F3-05
old Q: What does the correction-state mirror flag?
new Q: What gets flagged by the correction-state mirror?
sha256: `ca77cc7d395282a82875956a1a7882511ce59c68be9993e2735c9e7d169bcd9c`

## F3-06
old Q: How does scoped deletion work?
new Q: Explain the mechanics of scoped deletion.
sha256: `3c32b0886f7cca028f1183540cd8728cb699f5f1acc146a79176d5a4d896bd2b`

## F3-07
old Q: What sources may chat answers be generated from?
new Q: From which sources are chat answers allowed to be generated?
sha256: `2f96ed0acf8ab5983245b0a722217f87b981e488f7bd4fa203a8b4ee2cf99d1c`

## F3-08
old Q: What is preferred over a low-confidence guess?
new Q: What should be given instead of a low-confidence guess?
sha256: `109c3ba20c4f81be9371700a15f1ef793f761348d9a85351a4266131bbc3cb3e`

## F3-09
old Q: What text normalization does intake perform before unit extraction?
new Q: How does intake normalize text before extracting units?
sha256: `6f4df33c2607630aaec567917a6c8405a724a45f883c46c7afaf868d7fe5f2b8`

## F3-10
old Q: What triggers consolidation — session boundaries or chat turns?
new Q: Is consolidation triggered by session boundaries or by chat turns?
sha256: `8fe09c464baf76ac174b93b9ca8e5ae59240e2bb44b65169b788cf424a717c7a`

## F3-11
old Q: State the taught SCALE-ROT amendment rerun rule.
new Q: What does the SCALE-ROT amendment say about rerunning legs?
sha256: `4e62cc4028905fb3f02bb15b957203486de119ba3b8730da292f8fa736d72903`

## F3-12
old Q: State the taught leak-check rule for PENDING items in chat answers.
new Q: What is the leak-check rule for PENDING items appearing in chat answers?
sha256: `99e669b78b54fbd35d1a68da4b3837823a9d51747d7f3c52540373a84ccf4403`

## F3-13
old Q: What does every consolidation decision emit?
new Q: What is emitted for each consolidation decision?
sha256: `2ca426938a9ba31817ba358166ee787726cc1e18ef28eed5c8e536788bcb6eb7`

## F3-14
old Q: What trace visibility does the researcher have?
new Q: What can the researcher see of deliberation traces?
sha256: `836fb419300ee3dfa8ea647355c8c39017f4293ce9afd752b8fc46f6326b04d8`

## F3-15
old Q: What happens to sources larger than the session's intake budget?
new Q: How does intake handle a source exceeding the session's intake budget?
sha256: `e351ba0d83bb20eae079fab6cbec593397418835434aaec2411f2c89d51fb846`

## F3-16
old Q: Under what condition does a PENDING item get installed?
new Q: When, if ever, is a PENDING item installed?
sha256: `b4942e453769a7276c9e78294a058fd4c9f83578a47ffca177a61997f584a815`

## F3-17
old Q: What determinism property does the dialogue stack have?
new Q: What determinism guarantee does the dialogue stack provide?
sha256: `b03b66fda9c0f7cb34f3062a9af4130943822f4c4744aa7f25004f028635f88a`

## F3-18
old Q: When a researcher correction contradicts a source packet, which wins?
new Q: If a researcher correction conflicts with a source packet, which one prevails?
sha256: `3298c23ab47a25d39243e6091a485aea90030ce6240de7f70ef60cba1029122f`

## F4-01
old Q: Give the full audit entry layout with word offsets.
new Q: Lay out the complete audit entry format, with every word offset.
sha256: `7b2a73508006ae7c0f0e1be676b9c09174ec80334a48537a012d20afdd182f3d`

## F4-02
old Q: When is a consolidation trace "causally consulted" under G7, and what fails the audit?
new Q: What makes a consolidation trace "causally consulted" under G7, and what does the audit fail?
sha256: `281438b9bcb4e95647522628ef8049e768d70fbabc2049f1588e5a21971b91bc`

## F4-03
old Q: How are a session's outputs frozen?
new Q: How does a session's output get frozen?
sha256: `e43d8ad07bacab077d6db9fd7a89475be8ba42423f18d2176b4829f056d34480`

## F4-04
old Q: What must hold before scoring, regarding reruns?
new Q: What rerun condition must be met before scoring may begin?
sha256: `9ee58cb299649a2d72510854fc4a21758c4634edb3ef52d336d27a36bbec850e`

## F4-05
old Q: What does the red team receive — and what is withheld from it?
new Q: What is given to the red team, and what is kept from it?
sha256: `7a5dddaefae10b2055e7b434f9f4e4a4a769ed79d0c698aa556fc9561fffd705`

## F4-06
old Q: What does an erase-price audit contain?
new Q: What goes into an erase-price audit?
sha256: `7b415c33ee3256a7a9255d6357c328e8e911641f836f2ca13de7c48c25adf35b`

## F4-07
old Q: How are bypass attempts treated?
new Q: What happens to bypass attempts?
sha256: `9ea3c26cf924af65c6b720a4b9375070854f05580953919b2124c841935b9765`

## F4-08
old Q: What does the PENDING audit scan for, and what is a hit?
new Q: What is the PENDING audit looking for, and what counts as a hit?
sha256: `124f9788c9631258970de0c9a1e827d805e7e81d49303895d99e823e19b435c0`

## F4-09
old Q: Who sees the probe keys, and when are they sealed?
new Q: Who is allowed to see probe keys, and at what point are they sealed?
sha256: `f53b00b2b32e4b09526eba0430e8f56db46c426f8e6cb82299c8ee2a78f2290e`

## F4-10
old Q: What snapshots are committed, and at what granularity?
new Q: Which snapshots get committed, and how fine-grained are they?
sha256: `e88767eb35c2b352736b524ec91c1cf2662a94e568385dfcbed21f307a1ce482`

## F4-11
old Q: What must happen when a contradiction source appears?
new Q: What is required when a contradiction source shows up?
sha256: `344aff8835139c47e1f93824a39793a82c465b78c24946f3546216909017b529`

## F4-12
old Q: What is a silent overwrite of a contradicted fact?
new Q: How is silently overwriting a contradicted fact classified?
sha256: `2fd550ac23cbc9e7f4bf9ec3d864c2cc13144b77a00ab929a2f7e87f21c1618c`

## F4-13
old Q: What researcher review is a validity gate before implementation?
new Q: Which researcher review gates validity before implementation starts?
sha256: `3766484ec41b28b688e3e5e539956ee22221a27139b8474c9f1df5d0dac68e9c`

## F4-14
old Q: What does the intervention audit test?
new Q: What is the intervention audit testing?
sha256: `f32797cf39ccbcb8732dc6ea943bcb4366772325e8744cf95b1a108f6047995e`

## F4-15
old Q: What do audit entries with stage=9 mark?
new Q: What is marked by audit entries carrying stage=9?
sha256: `d93c604666d266076a1f9eaa3ca2d7cf03514742d40ea06efc263258c8a6dd73`

## F4-16
old Q: What does the d2 word of an audit entry carry?
new Q: What information sits in an audit entry's d2 word?
sha256: `c17510fbb4ecc0ffb648fe17203b1c4872556667b27ed88e97eab86d3d93becd`

## F4-17
old Q: What voids a determinism claim?
new Q: What invalidates a determinism claim?
sha256: `40b4a420980d11c2b38c60462de2c1469dee0934bb8ed1025962bb8da36bd991`

## F4-20
old Q: How are voided runs and killed hypotheses handled differently?
new Q: What is the different handling for a voided run versus a killed hypothesis?
sha256: `e8514107a14b556c95eb8036ec181b259b955765e11d14e8ece2caab2621537b`

## F5-01
old Q: List the znc compile pipeline stages in order.
new Q: Enumerate the stages of the znc compile pipeline in order.
sha256: `2daafac74c70c1016defa59624b693c1999f77bada3d65a73242b776e967f1e5`

## F5-02
old Q: How does the consolidation sweep compute the eviction floor, and what happens to tier-3 records below it?
new Q: How is the eviction floor computed at the consolidation sweep, and what is the fate of tier-3 records under it?
sha256: `ad2e3241f601b424d512814559df9343fc269e667b2916614d6f29b78091eae7`

## F5-03
old Q: What is a scale leg, and where is its stdout SHA recorded?
new Q: Define a scale leg and say where its stdout SHA is stored.
sha256: `1a9ecd1bd3bc46cf8d920cb77dd23e6a9f437a84fdf4589d133dd0b46ffd57c2`

## F5-04
old Q: What is the scope of the PENDING leak check?
new Q: How far does the PENDING leak check reach?
sha256: `5b6aeaf6fbf7839354e23afd2161a9565a225f2bebab668ff47472d0965d2cc5`

## F5-05
old Q: At which fact counts do scale legs run?
new Q: Which fact counts do scale legs use?
sha256: `e8c211fd76d9d7cc897138b9541e2076038212a70357b26fe3f57c8d67f24749`

## F5-06
old Q: What does the 100x leg demonstrate?
new Q: What is shown by the 100x leg?
sha256: `c2600be3e58113c2ba2ac986801e667777563276d9247b4d6e796b5242566276`

## F5-07
old Q: What chunking rule follows from the slice index ceiling?
new Q: Given the slice index ceiling, what is the chunking rule?
sha256: `46b947d2ef30ebffb32f769af9e2da39b1dc51395ae67e56a6ef185afead2058`

## F5-08
old Q: What are MALLOC_PERTURB_ runs for?
new Q: What purpose do MALLOC_PERTURB_ runs serve?
sha256: `0d874cbba7d829ce45c49e9a8d1ea285ecf0734dc64cadeea468a5c9e1fff174`

## F5-09
old Q: State the offset rule for consecutive `as []i32` casts.
new Q: What is the offset rule for back-to-back `as []i32` casts?
sha256: `7696b0672256ce922c6d3ab113ee556a1e3dd10e5c9d0b5a7cb035477296bfb9`

## F5-10
old Q: What is the arena workaround?
new Q: Describe the arena workaround.
sha256: `6e16b2439332258c6d41d790497cf444bbb8f4859722b4f026441f5dd94bd59d`

## F5-11
old Q: What caused the dialogue-74 panic?
new Q: What was behind the dialogue-74 panic?
sha256: `add59d94aae98d8679072859a53f537342869331f7ac97feeda759a3e26fadf5`

## F5-12
old Q: What beats surface patches for behavioral defects?
new Q: For behavioral defects, what outperforms surface patches?
sha256: `8e891b65b0c846bd6ec82658a72b56d50d8654efc9270795b70811a8f2a6cb98`

## F5-13
old Q: Why is the pipeline order load-bearing?
new Q: In what sense is the pipeline order load-bearing?
sha256: `675189ae0421e1b31f7152d057f0a4780fdeb876e189d6d15b21951eacf8358f`

## F5-16
old Q: At what granularity is determinism verified?
new Q: How fine-grained is determinism verification?
sha256: `4edce163750c799eb9d28a6dac305137b2deb2c7c7b92641496cafc19768cc4b`

## F5-17
old Q: State the M1 stdout SHA anomaly.
new Q: Describe the M1 stdout SHA anomaly.
sha256: `04d8b0fa2ae2b8c3184020533624b5288218c1fdb935f56be49bfee4c5dff224`

## F5-18
old Q: What does rerun-by-name use?
new Q: What inputs does rerun-by-name draw on?
sha256: `ccbfd43fc367e805a05c938a17f123550617323bddc1e0dc30b8380c7e5c25f0`

## F5-19
old Q: Who signs amendments, and what is the status of unsigned ones?
new Q: Who must sign amendments, and what happens to ones left unsigned?
sha256: `9a6cc79a4ee04a1493fdac1d141e7b74ed4999e1d71f23296b29facf3849c394`

## F5-20
old Q: What evidence ships with every scale claim?
new Q: What must accompany every scale claim?
sha256: `9240872218b059ae703a73da7ca8a118bf1d6b130533054c7e0df7da094964f4`

## F6-01
old Q: What is the lab's file-naming convention for frozen documents?
new Q: How are frozen documents named in the lab's convention?
sha256: `3843d778622fbba7016e8f4c111e91e4f1fdf6b579b8c455661ccbb6afc21325`

## F6-02
old Q: Why do session scripts use turn numbers?
new Q: What is the point of turn numbers in session scripts?
sha256: `104084215fa0a80bc6db7225726c75cbf7229662e98eb003b9f2fe38c13c1678`

## F6-03
old Q: Are fact IDs renumbered when a correction lands?
new Q: Does a correction cause fact IDs to be renumbered?
sha256: `5274f4cf26d4418372ea6096d84b8a8666af230cdf169c528f2fb4d34b92ccfb`

## F6-05
old Q: When does the last consolidation before S7 run?
new Q: When is the final consolidation before S7 executed?
sha256: `7c38587fae07a24b86b33a0d276bbbc1dea85a12d2f5620607591f465867b7a5`

## F6-06
old Q: What is allowed in S7?
new Q: Which activities are permitted during S7?
sha256: `e465ef6e45d01426c2088fb6ef64ef1fcf2ca549e5bb98a873df52b6f0306bf4`

## F6-07
old Q: What does the S7 probe cover?
new Q: What ground does the S7 probe cover?
sha256: `b8bcf5963a9e1866163f33145fcc0570275a56b64641216a5828ef174fd3edde`

## F6-08
old Q: What does the scorer see?
new Q: What is visible to the scorer?
sha256: `b1430370d2050a18fb1a61de5557e6be22093df887e6af28b24139a4a087513a`

## F6-09
old Q: How is a "withhold" answer on a PENDING probe scored?
new Q: What score does a "withhold" answer earn on a PENDING probe?
sha256: `410cdc78e41d901efe06bb1524679209e385f2c2f54fed180831908ef4419e52`

## F6-10
old Q: What counts as a PENDING leak?
new Q: What qualifies as a PENDING leak?
sha256: `e0510f4174807ecbb86ef887ba4a7c8110caeb30f3b238c26cdf7f8e096bc190`

## F6-11
old Q: Which schema does the G7 audit read?
new Q: Which schema is read by the G7 audit?
sha256: `33108d87646a2b3965915a43ad55eedbcc7a26efd869de993c2e31882cd4e958`

## F6-12
old Q: How was the S5 pipeline-order contradiction source resolved?
new Q: How did the S5 pipeline-order contradiction source get resolved?
sha256: `8b24bee7f1df1449290afeb35f15aa5d79b52511ab26a21c5c7b473ce5a51fa4`

## F6-13
old Q: What is the current tier-2 promotion probe bar?
new Q: What is the present bar of corroborating probes for tier-2 promotion?
sha256: `68a1b49ce24c576d2b021856e8d54ba4863b5217a0a5f8fdc9fcb1a4bddc2528`

## F6-14
old Q: What are the current write semantics of the audit ledger?
new Q: Describe the audit ledger's current write semantics.
sha256: `3fa20f1fb391978afc4e81cece4fc4275b9ffc8a2d884c2caf3710a0b0bb2378`

## F6-15
old Q: What is the current name of tier 3?
new Q: By what name is tier 3 currently known?
sha256: `2182ce1619d217efe57af875fc9e3441b63d5899f841e00d6cb30235fcfdc5f0`

## F6-16
old Q: What is the current rule for `return` in void fns?
new Q: What currently governs `return` inside void fns?
sha256: `cf9f4bf4fce40c5983223dde7a6214fc6ff2244d3d669d80502ddc371be64317`

## F6-17
old Q: What is the trial pass rule?
new Q: Under what rule does the trial pass?
sha256: `e120da8592ca323b938802e7e6326ac9f8df339cfb0ed6ffa75d778a1d8ad0c8`

## F6-18
old Q: Is post-freeze weakening of a bar permitted?
new Q: May a bar be weakened after freezing?
sha256: `c0c753c7a58bf0bfc7280ac7a88dd01d253c0612b6189b274bf3a05d917609e7`

## F6-19
old Q: Which branch receives trial evidence commits?
new Q: Trial evidence commits land on which branch?
sha256: `d223539768748630448809c1e7bbb8f3c13e9860728710a38405913be87f4d8e`

## FALSE-01
old Q: Is the pinned znc toolchain installed system-wide at `/usr/bin/znc`, making a pinned copy unnecessary?
new Q: The pinned znc toolchain is installed system-wide at `/usr/bin/znc`, so no pinned copy is needed — true or false?
sha256: `4d434239b840c7f0d699a2be48a8d29e689ce0b385e412d85e6461832c60c50e`

## FALSE-02
old Q: Are strength tiers assigned by the formula tier = min(3, floor(cite_count / 10))?
new Q: Strength tiers come from the formula tier = min(3, floor(cite_count / 10)) — correct?
sha256: `af12c00d0e8dd6328f9a2b7a7e8e4c09e9efd89b00264716c6c8821b7416d0fa`

## FALSE-03
old Q: May chat answers draw on PENDING items when confidence is high?
new Q: When confidence is high, may chat answers use PENDING items?
sha256: `4099f221719340a40665371be999ff2fc390a5f7f6e80f3feb072150360d2f32`

## FALSE-04
old Q: May probe keys be refined after the run to fix scoring disputes?
new Q: Is it permissible to refine probe keys after the run to settle scoring disputes?
sha256: `a6988df7080752295cadd4b55ce2d0e8c94ad6d5854cfd57d578e6dc74991dda`

## FALSE-05
old Q: Are scale legs rerun from the latest sources rather than the frozen config?
new Q: Scale legs are rerun from the latest sources, not the frozen config — true?
sha256: `1f8bee50bb9d6b5b1bbb9e619ee24bb3c84089c29aa50ce9111efdc687343a97`

## FALSE-06
old Q: Did a 200x scale leg run last week, with its results installed as knowledge?
new Q: A 200x scale leg ran last week and its results are installed knowledge — true or false?
sha256: `0dfadc6bf18ba71ceaa8a17a4b9a159b148ebd7b95d41b64bae92e5cee3e4cbc`

## PEND-01
old Q: Is it true that znc's `--fast-math` flag miscompiles signed division on ARM hosts?
new Q: Does znc's `--fast-math` flag really miscompile signed division on ARM hosts?
sha256: `d40dc7300a0e229947c491915bd9db1ce9a0c08967304548f277e3f3a789840d`

## PEND-02
old Q: Is it true that tier-3 memories can self-repair bit-rot without a consolidation pass?
new Q: Can tier-3 memories genuinely self-repair bit-rot with no consolidation pass?
sha256: `089467e3d769a0d12252ee29f778dbb3b4b35caec35a56064ec7dffc8b199d02`

## PEND-03
old Q: Is it true that G6 admissibility checks can be skipped for researcher chat turns?
new Q: Is it acceptable to skip G6 admissibility checks on researcher chat turns?
sha256: `76a86fde4412600f23a3e29dadc6d0e77a02c4c05bd8232512857200d73cbb17`

## PEND-04
old Q: Is it true that intervention audits are unnecessary when every decision carries a trace?
new Q: When every decision carries a trace, are intervention audits truly unnecessary?
sha256: `cbbd51f65a076fc84d529195e90f5394172db5ac41ada8595552fe4262febf95`

## PEND-05
old Q: Is it true that the 12-leg scale-rot amendment will halve rerun costs once signed?
new Q: Will the 12-leg scale-rot amendment really halve rerun costs once it is signed?
sha256: `d02cc46cecf7514f8d4e6ef24a8043aeaa242e4e11e4af71bd785b456443001e`

## PEND-06
old Q: Is it true that review-style sessions boost long-horizon recall by 10 points?
new Q: Do review-style sessions actually lift long-horizon recall by 10 points?
sha256: `c3f670429af2d5ab2918c10bac00082a12fac122490c9fc38266f5a48e0f181c`

## POST-P1
old Q: Given the five znc pipeline stages in order, which pass must run before intrinsic-lower, and what breaks if the order is reversed?
new Q: With the five znc pipeline stages in order, which pass must precede intrinsic-lower, and what breaks if they are swapped?
sha256: `9f4d241114a69e232153ceb6fb791e2973198445e5f9153bc7e6c12222415742`

## POST-P2
old Q: Given the 16-word audit entry layout, when is a stage=9 entry a promotion candidate, and what does its d2 word carry?
new Q: Given the 16-word audit entry layout, under what condition is a stage=9 entry a promotion candidate, and what does its d2 word hold?
sha256: `a5ec818116c07a0cb8721aebe5ec84105734a7232e68f8d87d687bb97e264a7b`

## POST-P3
old Q: Given the sweep's eviction-floor mechanics, what happens to a tier-3 memory whose cite count sits below the floor?
new Q: Given how the sweep's eviction floor works, what becomes of a tier-3 memory whose cite count is below the floor?
sha256: `47206f2a2b0028f419279067f73a75f652970a7588e11c744389a7281736eb53`

## POST-P4
old Q: Given the G7 causal-consultation rule, what does the neuter audit conclude about a turn whose trace cites a slot consolidation never read?
new Q: Under the G7 causal-consultation rule, what does the neuter audit conclude when a turn's trace cites a slot that consolidation never read?
sha256: `51ff88be1118c1df85e2f103c62cc3df0b1a012924f7ee0caeb5c5c8cf94b341`

## POST-P5
old Q: Given the definition of a scale leg, what does the scale-rot amendment require when leg M1's stdout SHA diverges from REPORT.md while verdicts reproduce?
new Q: Given what a scale leg is, what does the scale-rot amendment require when M1's stdout SHA diverges from REPORT.md while verdicts still reproduce?
sha256: `739ef819ae0217601cf21bd7dea9fab18932bdcd9d7dff34f21395bc31751b30`

## POST-P6
old Q: Given the leak check's scope, does a PENDING claim stated in a chat answer trip the check when all probe answers are clean?
new Q: Given the leak check's reach, does a PENDING claim uttered in a chat answer trip the check even if every probe answer is clean?
sha256: `a6a780aaff66ea8ad8b9e218637a1c51a85ecbd0a41b8e33847a839cc914e1aa`

## PRE-P1
old Q: Which znc pipeline pass must run before intrinsic-lower, and what breaks if the order is reversed?
new Q: Which pipeline pass has to precede intrinsic-lower, and what breaks when the order is reversed?
sha256: `b184987fef0d3f7846c72beab9e999bc7d2ee6852f51c5f2f21090ed74072045`

## PRE-P3
old Q: A tier-3 memory's cite count sits below the sweep's eviction floor. What happens to it at the consolidation sweep?
new Q: A tier-3 memory's cite count is below the sweep's eviction floor. What happens to it during the consolidation sweep?
sha256: `69ee1313c79eafda915ec5ba2abfde977deb33bd45cee9db3124488fad1f5bb9`

## PRE-P5
old Q: Leg M1's stdout SHA diverges from REPORT.md but its verdicts reproduce. What does the scale-rot amendment require?
new Q: M1's stdout SHA diverges from REPORT.md though its verdicts reproduce. What does the scale-rot amendment demand?
sha256: `c19e74ed39bd2ec812e3beb98b0055225cc84cfd31c4c075dd9f51903a903d77`

## PRE-P6
old Q: A PENDING claim appears verbatim in a chat answer, but no probe answer states it as fact. Leak or not — and why?
new Q: A chat answer contains a PENDING claim verbatim, while no probe answer states it as fact. Leak or not, and why?
sha256: `84d5f2c8917b7d364bbdb3de206ca146ad17a504f973a6aaa1187a0f556195bd`
