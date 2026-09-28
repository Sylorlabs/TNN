use strict;use warnings;
my $e='Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_C/INDEPENDENT_NATIVE_LANE_C_2';
sub readall {open my $h,'<',$_[0] or die;local $/;return <$h>;}
my $s=readall("$e/sources/n19_runtime_boundary_v6_recovery.zag");
my $ref=readall('Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_B_INDEPENDENT/sources/independent_corners.zag');
$ref =~ /(fn independent_corners\(.*?)(?=fn main\(\))/s or die;
my $fn=$1;
$s =~ s/fn main\(\)i32 \{/$fn\nfn main()i32 {\n    if(_zag_argc()==3 \&\& _zag_strcmp(_zag_arg(1),"independent-corners")==1){return independent_corners(_zag_arg(2));}/ or die;
open my $out,'>',"$e/sources/lane_c_v6_corners.zag" or die;print $out $s;
