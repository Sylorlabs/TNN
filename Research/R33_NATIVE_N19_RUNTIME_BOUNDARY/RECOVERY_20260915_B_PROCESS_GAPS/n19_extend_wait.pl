use strict;use warnings;local $/;my $p=shift;open my $f,'<',$p or die $!;my $s=<$f>;close $f;open my $h,'<','/tmp/n19_wait_helpers.zag' or die $!;my $helpers=<$h>;close $h;
$s =~ s/    if\(pid>0\)\{.*?\n    nio_free\(b\);/    if(pid>0){result=n19q_collect(pid,status,usage,null as *N19WaitFault);}\n    nio_free(b);/s or die 'collect';
$s =~ s/let enforced:i32=\([^\n]+ as i32;/let enforced:i32=n19q_resource_accept(\&r,size);/ or die 'predicate';
$s =~ s/fn main\(\)i32 \{/$helpers . "fn main()i32 {\n    if(_zag_argc()==2 \&\& _zag_strcmp(_zag_arg(1),\"wait-tests\")==1){return n19q_wait_tests();}\n    if(_zag_argc()==2 \&\& _zag_strcmp(_zag_arg(1),\"resource-predicate-tests\")==1){return n19q_resource_predicate_tests();}"/e or die 'main';
open my $o,'>',$p or die $!;print $o $s;close $o;
