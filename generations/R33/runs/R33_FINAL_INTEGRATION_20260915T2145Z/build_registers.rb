require 'json';require 'digest';require 'time';require 'fileutils'
r=Dir.pwd;e=File.expand_path(__dir__);s=->(p){File.file?(p) ? Digest::SHA256.file(p).hexdigest : nil};entries=[]
add=lambda{|x,out,err,command_file=nil,exit_file=nil|entries<<x.transform_keys{|k|k.to_sym}.merge(stdout_file:out.delete_prefix(e+'/'),stderr_file:err.delete_prefix(e+'/'),stdout_sha256:s.call(out),stderr_sha256:s.call(err),command_sha256:command_file&&s.call(command_file),exit_sha256:exit_file&&s.call(exit_file))}
{'exits.csv'=>'commands.txt','additional.exits.csv'=>'additional.commands.txt','transport.exits.csv'=>'transport.commands.txt','final_transport.exits.csv'=>'final_transport.commands.txt'}.each do |csv,cmd|
 lines=File.readlines("#{e}/#{cmd}",chomp:true);File.readlines("#{e}/#{csv}",chomp:true).each_with_index do |line,i|
 w=line.split(',');label=w[0];expected=w.size==3 ? w[1].to_i : (label.include?('original_')&&label.end_with?('.run')||label.end_with?('.patch') ? 1 : 0);actual=w[-1].to_i
 x={phase:csv,label:label,exact_command:lines[i],exit:actual,expected:expected,role:(csv=='additional.exits.csv'&&label.start_with?('integration.') ? 'SUPPLEMENTAL_DUPLICATE_LABEL_RUN_EXCLUDED_FROM_FINAL_TRANSPORT_EVIDENCE' : 'BOUNDED_NATIVE_QUALIFICATION')}
 add.call(x,"#{e}/#{label}.stdout","#{e}/#{label}.stderr")
 end
end
File.readlines("#{e}/n17_fresh/commands.jsonl").each{|l|x=JSON.parse(l);add.call(x.merge(phase:'n17_fresh'),"#{e}/n17_fresh/logs/#{x['label']}.stdout","#{e}/n17_fresh/logs/#{x['label']}.stderr")}
File.readlines("#{e}/v91_fresh/commands.tsv").each{|l|label,actual,expected,role=l.strip.split("\t");stem="#{e}/v91_fresh/logs/#{label}";add.call({phase:'v91_fresh',label:label,argv:File.readlines(stem+'.argv',chomp:true),cwd:r,exit:actual.to_i,expected:expected.to_i,role:role},stem+'.stdout',stem+'.stderr',stem+'.argv',stem+'.exit')}
expect={};%w[results.results.txt supplement.results.txt].each{|f|File.readlines("#{e}/n19/#{f}").each{|l|m=l.match(/^(\S+) expected=(\d+) actual=(\d+)/);expect[m[1]]=m[2].to_i if m}}
Dir["#{e}/n19/logs/*.command"].sort.each{|p|label=File.basename(p,'.command').sub(/^\d+_/,'');stem=p.sub('.command','');add.call({phase:'n19',label:label,cwd:r,exact_command:File.read(p).strip,exit:File.read(stem+'.exit').to_i,expected:expect[label]},stem+'.stdout',stem+'.stderr',p,stem+'.exit')}
Dir["#{e}/verification/*.command"].sort.each{|p|stem=p.sub('.command','');add.call({phase:'final_verification',label:File.basename(stem),exact_command:File.read(p).strip,exit:File.read(stem+'.exit').to_i,expected:0},stem+'.stdout',stem+'.stderr',p,stem+'.exit')}
%w[compiler_compare/exits.csv controls.exits.csv].each do |csv|
 command_lines=File.readlines("#{e}/#{csv=='controls.exits.csv' ? 'controls.commands.txt' : 'compiler_compare/commands.txt'}",chomp:true)
 File.readlines("#{e}/#{csv}",chomp:true).each_with_index do |line,i|
  w=line.split(',');compiler=w[0];name=csv=='controls.exits.csv' ? 'controls' : w[1];operation=w[-2];actual=w[-1].to_i
  stem=csv=='controls.exits.csv' ? "#{e}/controls_#{compiler}" : "#{e}/compiler_compare/#{compiler}.#{name}"
  ext=operation=='build' ? 'build' : 'run';expected=operation=='build' ? (name=='import_const_values' ? 1 : 0) : (name=='controls' ? (compiler=='stable' ? 4 : 0) : (name=='scoping_block_shadow' ? 41 : 42))
  role=name=='import_const_values' ? 'IMPORT_ONLY_LIBRARY_NO_MAIN_EXCLUDED_AS_EXECUTABLE' : 'BOUNDED_COMPILER_COMPARISON_NOT_PROMOTION'
  add.call({phase:csv,label:"#{compiler}.#{name}.#{operation}",exact_command:command_lines[i],exit:actual,expected_intent:expected,role:role},stem+'.'+ext+'.stdout',stem+'.'+ext+'.stderr')
 end
end
raise 'missing primary hashes' if entries.any?{|x|x[:role]!='SUPPLEMENTAL_DUPLICATE_LABEL_RUN_EXCLUDED_FROM_FINAL_TRANSPORT_EVIDENCE' && (x[:stdout_sha256].nil?||x[:stderr_sha256].nil?)}
File.write("#{e}/COMMAND_REGISTER.json",JSON.pretty_generate({schema:'R33_EXACT_NATIVE_COMMAND_EXIT_HASH_REGISTER_V1',commands:entries,command_count:entries.size,scope:'Fresh qualification/review and final verification; copied lane_witnesses/n17_lane_witness are prior witnesses and excluded from these fresh-command counts. Administrative setup/copy/JSON assembly orchestration is retained in scripts, not treated as model qualification.'})+"\n")
File.write("#{e}/FREEZE.json",JSON.pretty_generate({schema:'R33_FROZEN_FINAL_NATIVE_EVIDENCE_V1',frozen_at_utc:Time.now.utc.iso8601,evidence_manifest:'SHA256SUMS',compiler_sha256:s.call("#{e}/compiler.stable.znc"),final_closeout_sha256:s.call("#{e}/final_closeout.json"),command_register_sha256:s.call("#{e}/COMMAND_REGISTER.json"),scientific_exposure:0,canonical_r27_mutated:false,learner_authority_granted:false,r33_complete:false,manifest_exclusions:['SHA256SUMS','SHA256SUMS.verify.stdout','SHA256SUMS.verify.stderr','SHA256SUMS.verify.exit','SEAL.sha256','ARTIFACT_REGISTER.json'],exclusion_reason:'Manifest/register self-reference and post-manifest verification outputs only. ARTIFACT_REGISTER independently mirrors SHA256SUMS and is pinned by SEAL.'})+"\n")
# Whole evidence identities, including all binaries, source closures and raw outputs.
exclusions=%w[SHA256SUMS SHA256SUMS.verify.stdout SHA256SUMS.verify.stderr SHA256SUMS.verify.exit SEAL.sha256 ARTIFACT_REGISTER.json]
files=Dir.glob(e+'/**/*',File::FNM_DOTMATCH).select{|p|File.file?(p)&&!exclusions.include?(p.delete_prefix(e+'/'))}.sort
File.write("#{e}/SHA256SUMS",files.map{|p|"#{s.call(p)}  ./#{p.delete_prefix(e+'/')}\n"}.join)
File.write("#{e}/ARTIFACT_REGISTER.json",JSON.pretty_generate({schema:'R33_FROZEN_SHA256_ARTIFACT_IDENTITIES_V1',files:files.map{|p|{path:p.delete_prefix(e+'/'),bytes:File.size(p),sha256:s.call(p)}},manifest_sha256:s.call("#{e}/SHA256SUMS")})+"\n")
