use strict;use warnings;
my $e='Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_C/INDEPENDENT_NATIVE_LANE_C_2';
for my $set(qw(canonical protected closeout)) {
 open my $in,'<',"$e/$set.before.sha256" or die;
 my @files=map {chomp;s/^[a-f0-9]{64}  //;$_} <$in>;
 open my $out,'>',"$e/$set.after.sha256" or die;
 open my $hash,'-|','shasum','-a','256',@files or die;
 while(my $row=<$hash>){print $out $row;}close $hash or die;
}
