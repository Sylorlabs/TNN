use strict;
use warnings;
use Digest::SHA qw(sha256_hex);
use JSON::PP;
use File::Path qw(make_path);
my $e='/tmp/r33_finish_recovery_20260915_b/compiler_probe';
my $s='/Users/Shared/micah/Documents/TNN/TNN/Research/R33_CONTINUING_LIFE_V1';
my $c='/Users/Shared/micah/Documents/zag/znc';
my @checks;
my $seq=0;
writebytes("$e/review.commands.jsonl","");
sub run {
 my @argv=@_;my $n=++$seq;my $out="$e/review_cmd$n.stdout";my $err="$e/review_cmd$n.stderr";
 my $pid=fork();die $! unless defined $pid;
 if(!$pid){open STDOUT,'>:raw',$out or die $!;open STDERR,'>:raw',$err or die $!;exec {$argv[0]} @argv;die $!;}
 waitpid($pid,0);my $status=$?;
 open my $log,'>>:raw',"$e/review.commands.jsonl" or die $!;
 print $log JSON::PP->new->canonical->encode({argv=>\@argv,exit=>$status>>8,signal=>$status&127,stdout=>$out,stderr=>$err}),"\n";close $log;
 $?=$status;return $status;
}
sub check {my($ok,$name)=@_;push @checks,{name=>$name,pass=>$ok?JSON::PP::true:JSON::PP::false};die "$name failed\n" unless $ok;}
sub readbytes {my($f)=@_;open my $h,'<:raw',$f or die "$f: $!";local $/;return <$h>;}
sub writebytes {my($f,$b)=@_;open my $h,'>:raw',$f or die "$f: $!";print $h $b;close $h;}
sub audit {
 my($n)=@_;my(%files,%spans,@emits);my $outhash;my $toolhash;
 for(split /\n/,readbytes("$e/$n.provenance.tsv")){
  my @r=split /\t/;
  if($r[0] eq 'FILE'){check(!exists $files{$r[2]},"$n unique file $r[2]");$files{$r[2]}=readbytes($r[2]);check(sha256_hex($files{$r[2]}) eq $r[1],"$n input native hash $r[2]");}
  elsif($r[0] eq 'IMPORT'){push @{$spans{$r[1]}},[$r[2],$r[3],$r[4]];}
  elsif($r[0] eq 'EMIT'){push @emits,$r[1];}
  elsif($r[0] eq 'OUTPUT_SHA256'){$outhash=$r[1];}
  elsif($r[0] eq 'TOOL_SHA256'){$toolhash=$r[1];}
 }
 check($toolhash eq sha256_hex(readbytes("$e/project")),"$n native tool binary hash");
 my $expected='';my %emitted;
 for my $f(@emits){check(!$emitted{$f}++,"$n single emission $f");my $b=$files{$f};my $at=0;
  for my $span(@{$spans{$f}||[]}){my($a,$z,$child)=@$span;check($a>=$at && $z<length($b),"$n ordered directive span");my $directive=substr($b,$a,$z-$a);check($directive=~/\A\@import\s*\(\s*"([^"\\:\x00-\x1f]+)"\s*\);?\z/,"$n exact import syntax");check($emitted{$child},"$n dependency emitted before caller");$expected.=substr($b,$at,$a-$at);$at=$z;}
  $expected.=substr($b,$at)."\n";
 }
 my $actual=readbytes("$e/$n.projected.zag");check($expected eq $actual,"$n independent byte-exact reconstruction");check(sha256_hex($actual) eq $outhash,"$n native output hash");check(keys(%files)==@emits,"$n entire closure emitted");
 return \%files;
}
for my $n(qw(v68 v73 v71)){audit($n);for(qw(direct.build projection projected.build projected)){check(readbytes("$e/$n.$_.exit") eq "0\n","$n $_ exit zero");}}
check(readbytes("$e/v68.direct.exit") eq "1\n",'V68 direct still fails');
check(readbytes("$e/v73.direct.exit") eq "1\n",'V73 direct still fails');
check(readbytes("$e/v71.direct.exit") eq "0\n",'V71 direct passes');
my $v68=readbytes("$e/v68.projected.stdout");check($v68=~/^CL_V68_FAILURES,0$/m && $v68=~/^CL_V68_OUTER_BYTES,245924$/m,'V68 full unchanged checks pass');
check($v68=~/^CL_V68_CHECK,learner_tamper_refused,2005,2005$/m && $v68=~/^CL_V68_CHECK,oversize_section_refused,2001,2001$/m,'V68 refusal checks preserved');
check(readbytes("$e/v73.projected.stdout") eq "V73_RC,245924\n",'V73 exact result');
check(readbytes("$e/v71.projected.stdout") eq readbytes("$e/v71.direct.stdout"),'V71 stdout parity');
my $files=audit('v68');
my $frozen='/Users/Shared/micah/Documents/TNN/TNN/Research/R33_CLOSEOUT_20260915T174458Z/sources';
for my $f(keys %$files){my $rel=$f;$rel=~s{^/Users/Shared/micah/Documents/TNN/TNN/}{};check(readbytes("$frozen/$rel") eq $files->{$f},"unchanged frozen bytes $rel");}
for my $name(qw(zag_checkpoint_sliceparam_repro_v73 zag_checkpoint_module_repro_v71)){check(readbytes("$s/$name.zag") eq readbytes("$frozen/Research/R33_CONTINUING_LIFE_V1/$name.zag"),"unchanged frozen $name");}
my $d="$e/fixtures";make_path($d);
writebytes("$d/lib.zag","const K:i32=112;\n");
writebytes("$d/left.zag",'@import("lib.zag")' . "\nfn left()i32{return K;}\n");
writebytes("$d/right.zag",'@import("./lib.zag")' . "\nfn right()i32{return K;}\n");
writebytes("$d/diamond.zag",'// @import("missing.zag")' . "\n" . '@import("left.zag")' . "\n" . '@import("right.zag")' . "\n" . 'fn main()i32{let s:[]u8="@import(\"missing.zag\")";return (left()!=112 || right()!=112 || s.len==0) as i32;}' . "\n");
my %refuse=(cycle=>'@import("cycle.zag")',missing=>'@import("nonexistent.zag")',alias=>'@import("lib.zag", L)',alias_as=>'@import("lib.zag") as L',package=>'@import("std:list")',escape=>'@import("l\\ib.zag")',nested=>'fn f()i32{@import("lib.zag") return 0;}',unclosed=>'/* unfinished',badstring=>'fn main()i32{let s:[]u8="unfinished;}',braces=>'}',embed=>'fn f()[]u8{return #embed("x");}',resource=>'@resource(close) fn f()i32{return 0;}',profile=>'script;',module=>'module x;');
for my $n(sort keys %refuse){writebytes("$d/$n.zag",$refuse{$n});unlink "$d/$n.out", "$d/$n.tsv";run("$e/project","$d/$n.zag","$d/$n.out","$d/$n.tsv");my $exit=$?>>8;check($exit!=0 && !-e "$d/$n.out" && !-e "$d/$n.tsv","refuse $n without publishing");}
unlink "$e/diamond.projected.zag", "$e/diamond.provenance.tsv";
run("$e/project","$d/diamond.zag","$e/diamond.projected.zag","$e/diamond.provenance.tsv");check($?==0,'diamond projection');my $df=audit('diamond');check(keys(%$df)==4,'diamond canonical duplicate suppression and ignored comment/string imports');
run($c,"$e/diamond.projected.zag",qw(--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache),'-o',"$e/diamond");check($?==0,'diamond stable compile');run("$e/diamond");check($?==0,'diamond const runtime');
run("$e/project","$d/diamond.zag","$d/lib.zag","$d/alias-output.tsv");check(($?>>8)==4 && readbytes("$d/lib.zag") eq "const K:i32=112;\n",'closure output collision refused');
unlink "$e/v73.repeat.zag", "$e/v73.repeat.tsv";
run("$e/project","$s/zag_checkpoint_sliceparam_repro_v73.zag","$e/v73.repeat.zag","$e/v73.repeat.tsv");check($?==0 && readbytes("$e/v73.repeat.zag") eq readbytes("$e/v73.projected.zag") && readbytes("$e/v73.repeat.tsv") eq readbytes("$e/v73.provenance.tsv"),'deterministic repeated projection');
writebytes("$d/blocks.zag",'/* nested /* @import("absent.zag") */ comment */' . "\nfn main()i32{return 0;}\n");unlink "$d/blocks.out", "$d/blocks.tsv";
run("$e/project","$d/blocks.zag","$d/blocks.out","$d/blocks.tsv");check($?==0 && readbytes("$d/blocks.out") eq readbytes("$d/blocks.zag")."\n",'block comments ignored and byte preserved (projection only; stable parser lacks block comments)');
writebytes("$d/existing.out","KEEP\n");run("$e/project","$d/diamond.zag","$d/existing.out","$d/unused.tsv");check(($?>>8)==21 && readbytes("$d/existing.out") eq "KEEP\n",'existing output never overwritten');
unlink "$d/symlink.out";symlink "$d/lib.zag","$d/symlink.out" or die $!;run("$e/project","$d/diamond.zag","$d/symlink.out","$d/unused.tsv");check(($?>>8)==21 && readbytes("$d/lib.zag") eq "const K:i32=112;\n",'output leaf symlink never followed');
writebytes("$e/review.json",JSON::PP->new->canonical->pretty->encode({checks=>\@checks,all_pass=>JSON::PP::true,python_used=>JSON::PP::false,original_direct_closed=>JSON::PP::false,projected_original_closed=>JSON::PP::true}));
print scalar(@checks)," independent review checks passed\n";
