use strict;use warnings;
my $e='Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_C/INDEPENDENT_NATIVE_LANE_C_2';
open my $in,'<',"$e/sources/n19_qual_driver_v3_recovery.zag" or die;local $/;my $s=<$in>;
$s =~ s/fn main\(\)i32 \{/fn n19q_entry()i32 {/ or die;
$s .= <<'ZAG';

// Independent process-level exhaustion check: catches any remaining child,
// not merely the last known PID. Does not assert descendant adoption.
fn main()i32 {
    let rc:i32=n19q_entry();
    let status:*i32=_zag_malloc(8) as *i32;if(status==null as *i32){return 1;}
    status[0]=0;
    let remaining:i64=_zag_darwin_syscall(7,-1,status as i64,1,0,0,0);
    _zag_print("LANE_C_ALL_CHILDREN,wait_any,");n19q_println_i64(remaining);
    _zag_free(status as *i8);
    if(remaining!=-10){return 1;}
    return rc;
}
ZAG
open my $out,'>',"$e/sources/lane_c_all_children.zag" or die;print $out $s;
