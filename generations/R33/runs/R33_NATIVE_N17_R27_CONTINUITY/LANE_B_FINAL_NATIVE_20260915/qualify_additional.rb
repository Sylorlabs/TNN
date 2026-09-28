require 'json';require 'open3';require 'digest';require 'fileutils'
repo='/Users/Shared/micah/Documents/TNN/TNN'
base=repo+'/Research/R33_NATIVE_N17_R27_CONTINUITY'
d=File.expand_path(__dir__);e=d+'/additional_verified';FileUtils.mkdir_p(e+'/logs')
journal=File.open(e+'/commands.jsonl','wx')
run=lambda do |label,args,expected|
 out,err,st=Open3.capture3(*args,chdir:repo)
 File.binwrite(e+'/logs/'+label+'.stdout',out);File.binwrite(e+'/logs/'+label+'.stderr',err)
 journal.puts(JSON.generate({label:label,argv:args,cwd:repo,exit:st.exitstatus,expected:expected,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err)}));journal.flush
 puts "#{label}: #{st.exitstatus}";raise label unless st.exitstatus==expected
 out
end
c='/Users/Shared/micah/Documents/zag/znc';flags=['--target','macos-arm64','--no-zagd','--no-analyze','--no-foreground-cache']
run.call('compiler_before',['shasum','-a','256',c],0)
run.call('build_project',[c,base+'/V91_SEMANTIC_KAT/v91_project_native.zag',*flags,'-o',e+'/project'],0)
run.call('project_policy',[e+'/project',d+'/policy_native.zag',e+'/policy.zag',e+'/policy.provenance'],0)
File.readlines(e+'/policy.provenance',chomp:true).each{|l|w=l.split("\t");next unless w[0]=='FILE';p=w[2];target=e+'/import_closure/'+p;FileUtils.mkdir_p(File.dirname(target));FileUtils.cp(p,target)}
run.call('build_policy',[c,e+'/policy.zag',*flags,'-o',e+'/policy'],0)
p=repo+'/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-policy.json'
run.call('policy',[e+'/policy',p],0)
run.call('policy_missing',[e+'/policy',e+'/missing.json'],66)
bad=File.binread(p).sub('TEENAGER_ENGLISH','TEENAGER_ENGLISX');File.binwrite(e+'/changed_policy.json',bad)
run.call('policy_changed',[e+'/policy',e+'/changed_policy.json'],71)
cor=base+'/RECOVERY_20260915_B_INDEPENDENT/TERMINAL_SUPPLEMENT_20260915/COMPATIBILITY_CORRECTION_20260915'
run.call('reviewed_compatibility_pins',['shasum','-a','256','-c',cor+'/SHA256SUMS'],0)
FileUtils.cp_r(cor+'/sources',e+'/compatibility_sources')
record=JSON.parse(File.read(cor+'/commands.jsonl').lines.first)
commands=File.readlines(cor+'/commands.jsonl').map{|s|JSON.parse(s)}
commands.each do |r|
 args=r['argv'];next unless args
 # Re-execute exact reviewed build and fixture commands in an isolated copy.
 # Freeze original fixtures; substitute only the additive root path.
end
FileUtils.cp_r(cor+'/fixtures',e+'/fixtures')
FileUtils.mkdir_p(e+'/bin')
commands.each do |r|
 args=r['argv'];next unless args
 next unless args[0]==c || args[0].start_with?(cor+'/bin/')
 args=args.map{|a|a.gsub(cor+'/sources',e+'/compatibility_sources').gsub(cor+'/fixtures',e+'/fixtures').gsub(cor+'/bin',e+'/bin')}
 if r['label']=='r25_missing'
  FileUtils.mkdir_p(e+'/missing_inputs');args[1]=e+'/missing_inputs'
 end
 run.call('compatibility_'+r['label'],args,r['exit'])
end
%w[canonical protected].each{|n|run.call(n+'_after',['shasum','-a','256','-c',repo+'/Research/R33_CLOSEOUT_20260915T174458Z/'+n+'.sha256'],0)}
run.call('compiler_after',['shasum','-a','256',c],0)
journal.close
