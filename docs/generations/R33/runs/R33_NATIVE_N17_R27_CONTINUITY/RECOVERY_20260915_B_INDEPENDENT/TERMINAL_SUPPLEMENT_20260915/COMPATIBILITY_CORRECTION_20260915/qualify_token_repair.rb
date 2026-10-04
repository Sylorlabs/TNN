require 'open3';require 'json';require 'digest'
d=File.expand_path(__dir__);root=d+'/fixtures';log=File.open(d+'/token_repair_commands.jsonl','wx')
run=lambda do |label,argv,expected|
 o,e,s=Open3.capture3(*argv);File.write(d+'/evidence/'+label+'.stdout',o);File.write(d+'/evidence/'+label+'.stderr',e);log.puts(JSON.generate({label:label,argv:argv,exit:s.exitstatus,expected:expected,stdout_sha256:Digest::SHA256.hexdigest(o),stderr_sha256:Digest::SHA256.hexdigest(e)}));log.flush;puts "#{label}: #{s.exitstatus} expected #{expected}";raise o+e unless s.exitstatus==expected
end
%w[repaired_exact_source_gate forbidden_selector_tests].each{|n|run.call('build_'+n,['/Users/Shared/micah/Documents/zag/znc',d+'/sources/N17/'+n+'.zag','--target','macos-arm64','--no-zagd','--no-analyze','--no-foreground-cache','-o',d+'/bin/'+n],0)}
run.call('all_known_selectors',[d+'/bin/forbidden_selector_tests'],0)
g=d+'/bin/repaired_exact_source_gate';run.call('repaired_selftest',[g,'selftest'],0)
%w[ultralytics transformers torchvision.models openai whisper speech_recognition librosa.feature.mfcc].each_with_index do |token,i|
 leaf='forbidden_'+i.to_s+'.py';File.binwrite(root+'/'+leaf,token);run.call('repaired_unadmitted_token_'+i.to_s,[g,root,leaf],71)
end
[['missing','absent.py',66],['empty','empty.py',68],['oversized','oversize.py',68],['nonregular','directory.py',67],['symlink','symlink.py',66],['invalid_leaf','../escape.py',66],['malformed','malformed.py',71]].each{|label,leaf,rc|run.call('repaired_'+label,[g,root,leaf],rc)}
run.call('repaired_excerpt',[g,'/private/tmp/r33_finish_recovery_20260915_b/n17','excerpt.txt'],71)
%w[canonical protected].each{|n|run.call(n+'_final',['shasum','-a','256','-c','Research/R33_CLOSEOUT_20260915T174458Z/'+n+'.sha256'],0)}
log.close
