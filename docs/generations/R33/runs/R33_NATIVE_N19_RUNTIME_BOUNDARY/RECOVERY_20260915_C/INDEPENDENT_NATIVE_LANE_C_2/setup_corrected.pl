use strict; use warnings;
my $base='Research/R33_NATIVE_N19_RUNTIME_BOUNDARY';
my $e="$base/RECOVERY_20260915_C/INDEPENDENT_NATIVE_LANE_C_2";
mkdir "$e/$_" or die $! for qw(sources logs bin roots);
for my $f (glob "$base/RECOVERY_20260915_B_PROCESS_GAPS/sources/*.zag") { system('cp',$f,"$e/sources/")==0 or die; }
for my $set(qw(canonical protected closeout)) {
 open my $in,'<',"$base/RECOVERY_20260915_B_PROCESS_GAPS/$set.before.sha256" or die;
 my @files=map { chomp; s/^[a-f0-9]{64}  //; $_ } <$in>;
 open my $out,'>',"$e/$set.before.sha256" or die;
 for my $f(@files) { open my $h,'-|','shasum','-a','256',$f or die; while (my $row=<$h>) { print $out $row; } close $h or die; }
}
system("git diff --binary > $e/git.before.diff")==0 or die;
system("find $base/RECOVERY_20260915_B $base/RECOVERY_20260915_B_INDEPENDENT $base/RECOVERY_20260915_B_PROCESS_GAPS -type f -exec shasum -a 256 {} + > $e/recovery.before.sha256")==0 or die;
open my $in,'<',"$base/RECOVERY_20260915_C/INDEPENDENT_FRESH_1409/run.zsh" or die;
local $/; my $s=<$in>;
$s =~ s{RECOVERY_20260915_C/INDEPENDENT_FRESH_1409}{RECOVERY_20260915_C/INDEPENDENT_NATIVE_LANE_C_2}g;
$s =~ s/"\" > "\$E\/results.summary.txt"/"\$i" > "\$E\/results.summary.txt"/;
$s =~ s/run canonical_preserved/run recovery_preserved 0 shasum -a 256 -c "\$E\/recovery.before.sha256"\nrun canonical_preserved/;
open my $out,'>',"$e/run.zsh" or die;print $out $s;
