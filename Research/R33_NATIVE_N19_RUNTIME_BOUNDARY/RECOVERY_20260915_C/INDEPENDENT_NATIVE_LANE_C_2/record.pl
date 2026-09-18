use strict;use warnings;use Digest::SHA qw(sha256_hex);use JSON::PP;
my $e='Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_C/INDEPENDENT_NATIVE_LANE_C_2';
sub bytes {open my $h,'<',$_[0] or die "$_[0]: $!";binmode $h;local $/;return <$h>;}
my @records;
for my $f(sort glob "$e/logs/*.command") {
 (my $stem=$f)=~s/\.command$//;
 my %r=(stem=>$stem,command=>bytes($f),exit=>0+bytes("$stem.exit"));
 for my $suffix(qw(command exit stdout stderr)) {$r{sha256}{$suffix}=sha256_hex(bytes("$stem.$suffix"));}
 push @records,\%r;
}
my $fail=0;my $results=bytes("$e/results.results.txt").bytes("$e/supplement.results.txt");
my $count=0;
while($results=~/^(\S+) expected=(\d+) actual=(\d+)$/mg) {$count++;$fail++ if $2!=$3;}
die "capture count mismatch $count ".scalar(@records) if $count!=@records;
die "unexpected exits $fail" if $fail;
my %audit=(disposition=>'PASS_BOUNDED_NATIVE_ENGINEERING',commands=>scalar(@records),unexpected_exits=>$fail,records=>\@records,scope_exclusions=>['descendants/process-group containment','actual OS EINTR storm and kernel stalls/failed kill','power-loss durability','administrator rollback and hostile same-user races','fresh-root authentication','exhaustive device/socket errors','full R33/N17 scientific qualification and learner authority']);
open my $out,'>',"$e/RECORD.json" or die;print $out JSON::PP->new->canonical->pretty->encode(\%audit);
print "commands=".scalar(@records)." unexpected_exits=$fail\n";
