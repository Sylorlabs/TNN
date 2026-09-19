use strict;use warnings;use JSON::PP;use Digest::SHA qw(sha256_hex);
sub raw{open my $f,'<',$_[0] or die $!;binmode $f;local $/;my $s=<$f>;close $f;return $s;}
my $e='Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_B_PROCESS_GAPS';my $r=decode_json(raw("$e/RECORD.json"));my $n=0;
for my $c(@{$r->{commands}}){die 'empty argv' unless @{$c->{argv}};for my $key(qw(command_file stdout stderr exit_file)){my $i=$c->{$key};die "$i->{path}:hash" unless sha256_hex(raw($i->{path})) eq $i->{sha256};}if($c->{final_integrated}){$n++;}}
die "final count$n" unless $n==93;
for my $i(@{$r->{sources}},@{$r->{binaries}},$r->{compiler},@{$r->{coordination}->{c_durable_witness}}){die "$i->{path}:hash" unless sha256_hex(raw($i->{path})) eq $i->{sha256};}
print "record identities and argv normalized; final_commands=$n; durable_C_sources=6\n";
