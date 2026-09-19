use strict;use warnings;local $/;my($p,$kind)=@ARGV;open my $f,'<',$p or die $!;my $s=<$f>;close $f;my $hpath=$kind eq 'cpu'?'/tmp/n19_cpu_helpers.zag':'/tmp/n19_cpu_supervisor.zag';open my $h,'<',$hpath or die $!;my $ht=<$h>;close $h;
my $dispatch=$kind eq 'cpu'?'if(_zag_argc()==4 && _zag_strcmp(_zag_arg(1),"case-cpu-ceiling")==1){return n19_case_cpu_ceiling();}':'if(_zag_argc()==4 && _zag_strcmp(_zag_arg(1),"cpu-ceiling")==1){return n19q_cpu(_zag_arg(2),_zag_arg(3));}';
$s =~ s/fn main\(\)i32 \{/$ht . "fn main()i32 {\n    $dispatch"/e or die 'main';
if($kind ne 'cpu'){
$s =~ s/let again:i64=0;/if(cleanup==-4){\n            let drain_calls:i32=0;\n            while(cleanup==-4 \&\& drain_calls<65){cleanup=_zag_darwin_syscall(7,pid,status as i64,0,usage as i64,0,0);drain_calls=drain_calls+1;}\n            _zag_print("N19_WAIT_DRAIN,calls,");n19q_println_i64(drain_calls as i64);\n        }\n        let again:i64=0;/ or die 'drain';
$s =~ s/fault.real_waits!=1/fault.real_waits!=(cleanup==65?0:1)/; # avoid ternary unsupported: replace below
$s =~ s/\(cleanup==65\?0:1\)/want_real/g;
$s =~ s/let failed:i32=\(again/let want_real:i32=1;if(cleanup==65){want_real=0;}\n    let failed:i32=(again/;
$s =~ s/failed=failed\+n19q_wait_test\(0,3,-9,0\);/failed=failed+n19q_wait_test(0,3,-9,0);\n    failed=failed+n19q_wait_test(65,65,0,0);/;
}
open my $o,'>',$p or die $!;print $o $s;close $o;
