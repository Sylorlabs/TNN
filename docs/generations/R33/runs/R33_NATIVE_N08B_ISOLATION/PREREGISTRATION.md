# R33-N08B: explicit socket syscall confinement correction

Identity `r33-native-n08b-explicit-socket-denial-v3`. One sole primary, the same
five known native engineering controls and15 successful-worker assertions as
N08/N08A. Incorporates the complete original N08 preregistration and N08A dyld
bootstrap correction with only the changes specified here. Neither old primary
is repeated; both negative results and their frozen sources remain unchanged.

N08A's first worker reached main and matched13/14 assertions; the socket syscall
did not return the required EPERM/EACCES. It did not attempt any connection and
its raw return was not captured. This is an unsatisfied stricter creation-denial
contract, not proof of actual network traffic or a protection-bypass exploit.

New platform policy explicitly denies system-socket, all network operations and
Darwin syscall entry97(socket),135(socketpair),450(socket_delegate), requesting
EPERM. Installed SDK syscall.h supplied the numeric ABI; installed Apple profiles
demonstrate system-socket/socket-domain, syscall-unix/syscall-number and errno
modifiers. The complete frozen dyld-support.sb remains unchanged. No new allow
rule, broad system profile or reduction of the original oracle is introduced.
Worker adds one raw socket-return telemetry line to distinguish failure causes.
Only test/source/result paths otherwise change to N08B. N08_WORKER_* low-level
markers stay deliberately identical as disclosed corrective-regression controls.

Success requires the original exact15 worker checks, all parent checks and all
five reaped children. Expected syscall-denial errors, protected canary checks,
descriptor closure, foreign executable refusal, denied launch,500ms timeout
and4096byte file ceiling remain fixed. Any unexpected outcome fails this primary
and stops subsequent modes; no oracle rewrite or failed-primary rerun.

Main-engineering review only; no independent certification, human grant, learner,
scientific population, training, R27 mutation or promotion. The Apple loader is
a pinned native OS-policy dependency; all new test/controller logic is Zag.
Preserve raw evidence, source/config/reservation/review/build freezes, actual
resources/counters, analysis including negatives, registries and continuation.
