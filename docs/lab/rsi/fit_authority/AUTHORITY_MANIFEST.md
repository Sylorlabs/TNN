# FIT Authority Manifest

Frozen authority path: `docs/lab/rsi/fit_authority/` (never pruned). Every file below is byte exact to its frozen sha. Verification: `sha256sum` against this manifest.

| File | Frozen sha256 | Lines | Canonical source |
|---|---|---|---|
| tnn_chat.zag | c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c |  | baseline probe instrument, frozen wave 20260925-0221pdt |
| tnn_chat_decline.zag | a87011fe10dbc5bac5b0d6e36391033974acfcc46b852618989e3e800cbc3e4b |  | decline probe instrument, frozen wave 20260925-0221pdt |
| kb.txt | 3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1 | 38 | closed book knowledge base, copied byte exact from docs/lab/dialogue/kb.txt, frozen shas match FIT evidence wave-20260925-0221pdt and wave-20260925-1421pdt |
| gaz.txt | b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a | 27 | gazetteer, copied byte exact from docs/lab/dialogue/gaz.txt, frozen shas match FIT evidence wave-20260925-0221pdt and wave-20260925-1421pdt |

kb.txt and gaz.txt were added to this authority path in wave 20260925-1721pdt as the D1 residual from the 1421pdt authority freeze (commit b650ea46f). They were copied with shell cp only, no edits, and sha256 verified before commit.

This is not a candidate verdict and it is not merge review of the merged-in work; it certifies the 38-fact closed-book probe chain only.
