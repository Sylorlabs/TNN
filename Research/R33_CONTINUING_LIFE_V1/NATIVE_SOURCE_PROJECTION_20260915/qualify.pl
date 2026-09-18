use strict;
use warnings;
use Digest::SHA qw(sha256_hex);
use JSON::PP;
use File::Find;
my $e='/tmp/r33_finish_recovery_20260915_b/compiler_probe';
my $s='/Users/Shared/micah/Documents/TNN/TNN/Research/R33_CONTINUING_LIFE_V1';
my $a="$s/NATIVE_SOURCE_PROJECTION_20260915";
my $c='/Users/Shared/micah/Documents/zag/znc';
my $j=JSON::PP->new->canonical->pretty;
my(@cmd,@hashcmd);
sub bytes {open my $h,'<:raw',$_[0] or die $!;local $/;return <$h>;}
sub nativehash {
 my($f)=@_;my @argv=("$e/project",'--hash',$f);open my $h,'-|',@argv or die $!;local $/;my $out=<$h>;close $h;my $exit=$?>>8;push @hashcmd,{argv=>\@argv,exit=>$exit,stdout=>$out};die "hash $f failed" unless $exit==0 && $out=~/\A[0-9a-f]{64}\n\z/;$out=~s/\n\z//;die "native hash mismatch $f" unless $out eq sha256_hex(bytes($f));return $out;
}
sub run {
 my($name,$expected,@argv)=@_;my $out="$e/$name.stdout";my $err="$e/$name.stderr";
 my $pid=fork();die $! unless defined $pid;if(!$pid){open STDOUT,'>:raw',$out or die $!;open STDERR,'>:raw',$err or die $!;exec {$argv[0]} @argv;die $!;}
 waitpid($pid,0);my $status=$?;my $exit=$status>>8;
 push @cmd,{argv=>\@argv,exit=>$exit,signal=>$status&127,expected_exit=>$expected,stdout=>$out,stderr=>$err};
 open my $h,'>',"$e/$name.exit" or die $!;print $h "$exit\n";close $h;
 die "$name unexpected exit $exit" unless $exit==$expected && ($status&127)==0;
}
my @original=(map{"$s/$_.zag"}qw(common storage checkpoint outer_learner_packet_bridge_v68_tests zag_checkpoint_sliceparam_repro_v73 zag_checkpoint_module_repro_v71));
push @original,"$s/../R33_NATIVE_SHA256_V2.zag","$s/../R33_NATIVE_IO_V1.zag";
my %before=map {$_=>nativehash($_)} ($c,@original);
my @flags=qw(--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache);
run('project.build',0,$c,"$a/project.zag",@flags,'-o',"$e/project");
for my $p(['v68','outer_learner_packet_bridge_v68_tests',1],['v73','zag_checkpoint_sliceparam_repro_v73',1],['v71','zag_checkpoint_module_repro_v71',0]){
 my($n,$file,$direct)=@$p;
 run("$n.direct.build",0,$c,"$s/$file.zag",@flags,'-o',"$e/$n.direct");
 run("$n.direct",$direct,"$e/$n.direct");
 unlink "$e/$n.projected.zag","$e/$n.provenance.tsv";
 run("$n.projection",0,"$e/project","$s/$file.zag","$e/$n.projected.zag","$e/$n.provenance.tsv");
 run("$n.projected.build",0,$c,"$e/$n.projected.zag",@flags,'-o',"$e/$n.projected");
 run("$n.projected",0,"$e/$n.projected");
}
run('review',0,'/usr/bin/perl',"$a/review.pl");
my %after=map {$_=>nativehash($_)} ($c,@original);
for(keys %before){die "original changed $_" unless $before{$_} eq $after{$_};}
my @reviewcmd=map {JSON::PP->new->decode($_)} split /\n/,bytes("$e/review.commands.jsonl");
my %artifacts;
my @paths=glob("$e/*");push @paths,glob("$e/fixtures/*"),glob("$a/*");
for my $f(@paths){next unless -f $f && !-l $f;next if $f=~/\/(qualification\.json|qualification\.sha256|qualification\.stdout|qualification\.stderr)$/;$artifacts{$f}=nativehash($f);}
my $result={compiler=>$c,compiler_sha256=>$before{$c},original_sha256_before=>\%before,original_sha256_after=>\%after,original_bytes_unchanged=>JSON::PP::true,commands=>\@cmd,review_commands=>\@reviewcmd,native_hash_invocations=>\@hashcmd,artifact_sha256=>\%artifacts,review=>JSON::PP->new->decode(bytes("$e/review.json")),claims=>{direct_original_v68_pass=>JSON::PP::false,direct_original_v73_pass=>JSON::PP::false,direct_original_v71_pass=>JSON::PP::true,projected_original_v68_pass=>JSON::PP::true,projected_original_v73_pass=>JSON::PP::true,projected_original_v71_pass=>JSON::PP::true,test_checks_modified=>JSON::PP::false,stable_compiler_modified=>JSON::PP::false,scientific_exposure=>0,learner_authority_granted=>JSON::PP::false,canonical_r27_mutated=>JSON::PP::false},scope=>'Exact tested flat local import closure; lexical dot/dotdot normalization; trusted unchanged regular input files, no input symlink or module/resource/alias semantics claim. Outputs O_EXCL; existing leaf files and symlinks refused; trusted parent directories. Added newline separator per emitted file.'};
open my $h,'>',"$e/qualification.json" or die $!;print $h $j->encode($result);close $h;
my $qh=nativehash("$e/qualification.json");open my $q,'>',"$e/qualification.sha256" or die $!;print $q "$qh  $e/qualification.json\n";close $q;
print "qualified unchanged roots, compiler and byte-preservation review; machine record $e/qualification.json\n";
