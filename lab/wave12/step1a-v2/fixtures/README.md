# fixtures

Deterministic, RNG-free audit fixtures for the RNGSCAN v2 rounds.

- `state1.bin`: 1,048,576 bytes of `S` (0x53)
  sha256: `844b0df82fccb18c9abd93af5714be1dce7fc7b9cbacfee5bc718a017baccb44`
- `state2.bin`: 1,048,576 bytes of `T` (0x54) — the alternate state
  sha256: `ce2442b8b1c15414ca16f054e5331fc8019d24fd50813f43cc9881f7f19d765c`
- `input.bin`: 65,536 bytes of `I` (0x49)
  sha256: `9ce267663a0fed025ba2eb83802c945c939a7d30e2bac57437cee708196d0307`

Regenerate (byte-identical):

    head -c 1048576 /dev/zero | tr '\0' 'S' > state1.bin
    head -c 1048576 /dev/zero | tr '\0' 'T' > state2.bin
    head -c 65536 /dev/zero | tr '\0' 'I' > input.bin
