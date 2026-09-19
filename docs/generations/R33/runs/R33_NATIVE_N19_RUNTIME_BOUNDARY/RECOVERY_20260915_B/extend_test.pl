use strict; use warnings; local $/; my $p=shift; open my $f,'<',$p or die $!; my $s=<$f>; close $f;
$s =~ s/let state:N19State=N19State\{\.sequence=7,\.event_count=3,\.journal_bytes=96,\.audit_head=7,\.poisoned=1,\.recovered=0\};/let state:N19State=n19_empty_state();\n    if(n19_case_failed_recovery_atomicity(\&state)!=N19_OK){return 1;}/ or die 'state';
my $add=<<'ZAG';
    let rootfd:i64=n19_open_root(root);if(rootfd<0){return 1;}
    let direct:i32=n19_append_existing_fixture_at(rootfd,leaf,&state,&attempted,&committed);
    let closed:i32=n19_close(rootfd);
    let after:N19State=n19_empty_state();let reread:i32=n19_read_fixture(root,leaf,&after);
    if(direct!=N19_REFUSED_RECOVERY || closed!=N19_OK || attempted!=0 || committed!=0 || reread!=N19_OK || after.sequence!=1 || after.journal_bytes!=32 || state.sequence!=7 || state.event_count!=3 || state.journal_bytes!=96 || state.audit_head!=7 || state.poisoned!=1 || state.recovered!=0){return 1;}
ZAG
$s =~ s/(    let record:\[\]u8=n19_alloc\(N19_RECORD_BYTES\);if\(record.len==0\)\{return 1;\})/$add$1/ or die 'record';
open my $o,'>',$p or die $!; print $o $s; close $o;
