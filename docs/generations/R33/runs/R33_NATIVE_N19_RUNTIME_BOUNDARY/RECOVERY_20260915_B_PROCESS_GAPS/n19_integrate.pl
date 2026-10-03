use strict;use warnings;local $/;my $p=shift;open my $f,'<',$p or die $!;my $s=<$f>;close $f;
$s =~ s/if\(cleanup==pid\)\{again=/if(cleanup==pid || cleanup==-10){again=/;
$s =~ s/(        \/\/ Never turn fallback.*?\n)        return result;/$1        if((cleanup==pid || cleanup==-10) \&\& again==-10 \&\& (killed==0 || killed==-3)){result.exit_code=125;result.signal=0;}\n        return result;/s;
$s =~ s/if\(r.exit_code!=-1 \|\| r.cpu_us/if(r.exit_code!=125 || r.cpu_us/;
my $test=<<'ZAG';
fn n19q_already_reaped_test()i32 {
    let status:*i32=_zag_malloc(8) as *i32;let usage:*i64=_zag_malloc(256) as *i64;
    if(status==null as *i32 || usage==null as *i64){return 1;}
    let pid:i64=_zag_darwin_fork();if(pid==0){_zag_exit(77);}
    if(pid<1){return 1;}
    let first:i64=_zag_darwin_syscall(7,pid,status as i64,0,usage as i64,0,0);
    if(first!=pid){return 1;}
    let r:N19QualRun=n19q_collect(pid,status,usage,null as *N19WaitFault);
    let again:i64=_zag_darwin_syscall(7,pid,status as i64,1,0,0,0);
    _zag_print("N19_ALREADY_REAPED,post_wait,");n19q_println_i64(again);
    _zag_free(status as *i8);_zag_free(usage as *i8);
    return (r.exit_code!=125 || r.cpu_us!=0 || r.peak_rss!=0 || again!=-10) as i32;
}
ZAG
$s =~ s/fn n19q_wait_tests\(\)i32 \{/$test . 'fn n19q_wait_tests()i32 {'/e;
$s =~ s/(fn n19q_wait_tests\(\)i32 \{\n    let failed:i32=0;)/$1\n    failed=failed+n19q_already_reaped_test();/;
open my $o,'>',$p or die $!;print $o $s;close $o;
