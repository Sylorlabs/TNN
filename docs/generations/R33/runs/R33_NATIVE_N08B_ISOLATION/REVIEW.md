# N08B main-agent pre-exposure review

Reviewed N08A's complete first-worker capture and actual source: it tested
socket creation, not network connection. This correction strengthens the policy
rather than loosening that oracle. Three exact Darwin syscall IDs are taken from
the installed SDK. Apple's installed profiles establish the syscall-number and
errno grammar and show distinct system-socket/network permissions. Numeric97,
135,450 avoid unverified symbolic names in the profile. All socket traffic paths
remain denied by network rules; creation must now meet the original denial test.

The dyld-bootstrap copy is unchanged. Test cases, error predicate, limits,
preimages, allowed input and no-fallback launcher remain N08A behavior. Only
new identity paths, restrictive rules and raw socket-return logging change.
Worker and supervisor remain separate native executables. No actual parent or
credential enters a fixture. Old39-file N08 and40-file N08A artifact sets verify.

Prospective main-agent engineering review, not an independent or complete
security assessment. A source rule does not establish runtime enforcement;
the separately frozen sole primary must demonstrate it. No scientific or human
authority gate is discharged by this review.
