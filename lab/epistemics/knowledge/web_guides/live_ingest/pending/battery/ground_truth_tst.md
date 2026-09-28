# TESTC ground truth (4 cases) -- kill bar P4

Setup (fresh state dir):
1. `kbpend` the 4 `claim.txt` lines in tst-01..tst-04 order
   -> stdout `PENDING|HELD|1` ... `PENDING|HELD|4`, exit 0.
2. For each case, run the frozen check program on the committed fixture
   input OUTSIDE the instrument (prereg S5b: the procedure is deliberate):
   `python3 tst/checks/<prog> tst/<cid>/fixture_input.txt`; the exit code is
   the test result.
3. `kbtest <seq> <PASS|FAIL> <proto-id> <state>` with the observed result.

| case   | proto    | fixture -> program      | exit | kbtest invocation        | expected resolution |
|--------|----------|-------------------------|------|--------------------------|---------------------|
| tst-01 | PRIME-IDX| `100 541` -> check_prime_idx.py | 0 | `kbtest 1 PASS PRIME-IDX` | `KB|<k>|The 100th prime number is 541.` installed; `RESOLVE|1|KB|TESTED|PRIME-IDX` |
| tst-02 | POW2     | `64 18446744073709551616` -> check_pow2.py | 0 | `kbtest 2 PASS POW2` | `KB|<k>|Two raised to the power of 64 equals 18446744073709551616.` installed; `RESOLVE|2|KB|TESTED|POW2` |
| tst-03 | FIB-IDX  | `30 832041` -> check_fib_idx.py | 1 | `kbtest 3 FAIL FIB-IDX` | `REJ|<r>|The 30th Fibonacci number is 832041.|TEST-FAILED:FIB-IDX`; `RESOLVE|3|REJ|CONTRADICTED|<detail carrying FIB-IDX>`; never installed |
| tst-04 | DIGSUM   | `987654321 44` -> check_digsum.py | 1 | `kbtest 4 FAIL DIGSUM` | `REJ|<r>|The sum of the digits of 987654321 is 44.|TEST-FAILED:DIGSUM`; `RESOLVE|4|REJ|CONTRADICTED|<detail carrying DIGSUM>`; never installed |

Truth notes (confirmed by running the check programs at authoring time):
the 100th prime is 541 and 2^64 = 18446744073709551616 (PASS); Fib(30) =
832040, not 832041, and the digit sum of 987654321 is 45, not 44 (FAIL).

P4 assertions: the two PASS resolutions carry kind `TESTED`,
byte-distinguishable from `CORROBORATED` in resolutions.txt; the two FAIL
resolutions carry kind `CONTRADICTED` (prereg S6 template) with the proto-id
in the detail, and the REJ reason is exactly `TEST-FAILED:<proto-id>`.
Over the combined HON+TESTC run phase, resolutions.txt holds exactly 8
`|CORROBORATED|` lines and 2 `|TESTED|` lines. Any mis-resolution = FAIL.
