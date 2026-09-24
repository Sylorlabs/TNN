# C12 source SHA inventory

Frozen real organ sources — byte-identical copies used by the C12 harness.
Verified 2026-09-24 against `~/workspace/ob2_collusion/src_ref/`,
`~/workspace/ob2_collusion/build/`, and `~/workspace/ob2_repairatk/vb/`
(identical in all three; prefixes recorded in the prereg checkpoint).

| file | SHA-256 |
|---|---|
| src/ob_arbiter.zag | c0e6d26c5707d4f490a357282d440824b6730a4877c902e61d9a3ded4ecb5c31 |
| src/ob_common.zag  | 123deb0d880b0b673b64cb85a3eebd2cbcd3188ed324af0b61e81557e4039c73 |
| src/ob_fl2.zag     | 71c31add2aff606fee673438aa4fe8d674bb35b7193d784947a83aa4373c77db |
| src/ob_mem.zag     | 6144812a858d557c2204aca3183263af494c001c268cd18b991ba80731adc246 |
| src/ob_pam.zag     | 4fd59016b9561f226bf24e56d063d209e7d602b47e70167727d2e147f7777fd0 |
| src/ob_tn.zag      | 81962428d22091bfde7686ac5feca2a986202eac48b7a1b44b22b2ec8b64a3e4 |

Harness + binary (built 2026-09-24, znc pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`):

| artifact | SHA-256 |
|---|---|
| c12.zag (987 lines) | 2d19b694af6b62de7b10200bd329a6cf76be58538564e0b669bf87184b4891a9 |
| c12_bin | 89b6a5beb57d83ee60ce780722e1c14013692b34c0331c9b394127a880c180e1 |

The harness imports only the six frozen sources above; no other code
is on the promotion/quorum path. N-AUTH is not implemented (parked).
