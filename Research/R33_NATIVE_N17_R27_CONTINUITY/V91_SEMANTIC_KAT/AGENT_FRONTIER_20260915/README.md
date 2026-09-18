# V91 recovery lane

This directory is reserved for the additive V91 semantic-generator recovery pass.

Run `../run_v91_text_recovery_scan.zsh` from a native execution window. The scanner searches repository text and archive text members for generator, dataset, RNG, sampling, model-forward, and tokenizer/BPE semantics. Historical Python is treated as inert text and is never executed.

Do not convert intended semantic-row recovery into a generator-parity claim. Actual V91 parity remains fail-closed until the exact generation semantics reproduce the historical outputs without hardcoded oracle strings.
