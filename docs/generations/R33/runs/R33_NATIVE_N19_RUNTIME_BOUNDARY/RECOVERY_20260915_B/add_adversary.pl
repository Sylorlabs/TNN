use strict; use warnings;
local $/; my $p=shift; open my $f,'<',$p or die $!; my $s=<$f>; close $f;
my $test=<<'ZAG';
fn n19_case_poisoned_append(root:[]u8,leaf:[]u8)i32 {
    let attempted:i64=0;let committed:i64=0;
    if(n19_write_fixture(root,leaf,&attempted,&committed)!=N19_OK){return 1;}
    let state:N19State=N19State{.sequence=7,.event_count=3,.journal_bytes=96,.audit_head=7,.poisoned=1,.recovered=0};
    let rc:i32=n19_append_existing_fixture(root,leaf,&state,&attempted,&committed);
    let fresh:N19State=n19_empty_state();let read:i32=n19_read_fixture(root,leaf,&fresh);
    _zag_print("N19_POISONED_APPEND,status,");n19_emit("poisoned_append",rc);
    if(rc!=N19_REFUSED_RECOVERY || attempted!=0 || committed!=0 || state.sequence!=7 || state.event_count!=3 || state.journal_bytes!=96 || state.audit_head!=7 || state.poisoned!=1 || state.recovered!=0 || read!=N19_OK || fresh.sequence!=1 || fresh.journal_bytes!=32){return 1;}
    let record:[]u8=n19_alloc(N19_RECORD_BYTES);if(record.len==0){return 1;}
    n19_encode(record,8,"blocked");let append:i32=n19_append(&state,record);n19_free(record);
    if(append!=N19_REFUSED_RECOVERY || state.sequence!=7 || state.poisoned!=1){return 1;}
    _zag_println("N19_POISONED_APPEND,failures,0");return 0;
}

ZAG
$s =~ s/fn main\(\)i32 \{/$test . 'fn main()i32 {'/e or die 'main';
$s =~ s/(fn main\(\)i32 \{)/$1\n    if(_zag_argc()==4 \&\& _zag_strcmp(_zag_arg(1),"case-poisoned-append")==1){return n19_case_poisoned_append(_zag_arg(2),_zag_arg(3));}/;
open my $o,'>',$p or die $!; print $o $s; close $o;
