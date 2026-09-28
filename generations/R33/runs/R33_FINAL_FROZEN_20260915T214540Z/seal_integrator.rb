require 'json'
require 'digest'
require 'fileutils'
require 'open3'
r=Dir.pwd
old=File.read('/tmp/r33_integrator_e').strip
e="#{r}/Research/R33_FINAL_FROZEN_#{Time.now.utc.strftime('%Y%m%dT%H%M%SZ')}"
FileUtils.mkdir_p(e)
Dir.glob(old+"/**/*").each{|p|next unless File.lstat(p).file?;t=p.sub(old,e);FileUtils.mkdir_p(File.dirname(t));FileUtils.cp(p,t)}
rel=e.delete_prefix(r+'/')
close=JSON.parse(File.read("#{e}/final_closeout.json"))
close['evidence_directory']=rel
close['date_utc']=Time.now.utc.to_s
close['execution_evidence_origin']=old.delete_prefix(r+'/')
close['independent_review']="#{rel}/INDEPENDENT_INTEGRATOR_REVIEW.md"
close['syntax_exclusions']=%w[architecture.json sibling.json learning.json].map{|x|"n17_fresh/r25_inputs/#{x}"}
write=lambda{|p,x|File.write(p,JSON.pretty_generate(x)+"\n")}
write.call("#{e}/final_closeout.json",close)
write.call('Research/R33_FINAL_CLOSEOUT.json',close)
%w[CURRENT_ENTRY_POINT.md WORKLOG.md].each{|f|File.open("Research/R33_CONTINUING_LIFE_V1/#{f}",'a'){|io|io.puts "\nFrozen authoritative closeout: [#{File.basename(e)}](../#{File.basename(e)}/final_closeout.json). R33 incomplete: V91 0/16 native generation, N17 26 unresolved rows and R25 native lineage blocked. Stable retained; R27 60423/0 unchanged; exposure=0; learner authority=false."}}
%w[R33_NATIVE_N17_R27_CONTINUITY R33_NATIVE_N19_RUNTIME_BOUNDARY].each{|n|p="Research/#{n}/STATUS.json";x=JSON.parse(File.read(p));x['final_frozen_closeout']="#{rel}/final_closeout.json";write.call(p,x)}
p='Research/R33_NATIVE_N17_R27_CONTINUITY/EVIDENCE_REGISTER.json';x=JSON.parse(File.read(p));x['final_frozen_closeout']="#{rel}/final_closeout.json";write.call(p,x)
File.open('Research/R33_NATIVE_N17_R27_CONTINUITY/V92_STATE_IMAGE_QUAL/README.md','a'){|io|io.puts "\nFinal frozen admission evidence: ../../#{File.basename(e)}/final_closeout.json. All 13 fresh modes passed; synthetic engineering scope only."}
FileUtils.mkdir_p("#{e}/final_documents")
%w[Research/R33_FINAL_CLOSEOUT.json Research/R33_CONTINUING_LIFE_V1/CURRENT_ENTRY_POINT.md Research/R33_CONTINUING_LIFE_V1/WORKLOG.md Research/R33_NATIVE_N17_R27_CONTINUITY/STATUS.json Research/R33_NATIVE_N17_R27_CONTINUITY/EVIDENCE_REGISTER.json Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/STATUS.json Research/R33_NATIVE_N17_R27_CONTINUITY/V92_STATE_IMAGE_QUAL/README.md].each{|p|t="#{e}/final_documents/#{p}";FileUtils.mkdir_p(File.dirname(t));FileUtils.cp(p,t)}
checks=[]
%w[immutable.before.sha256].each{|f|argv=['shasum','-a','256','-c',"#{e}/#{f}"];out,err,st=Open3.capture3(*argv);File.write("#{e}/seal_immutable.stdout",out);File.write("#{e}/seal_immutable.stderr",err);checks<<{argv:argv,exit:st.exitstatus};raise 'immutable failed' unless st.success?}
write.call("#{e}/SEAL_COMMANDS.json",checks)
invalid=[]
Dir.glob("#{e}/**/*.json").each{|p|begin;JSON.parse(File.read(p));rescue JSON::ParserError;invalid<<p.delete_prefix(e+'/');end}
raise invalid.inspect unless invalid.sort==close['syntax_exclusions'].sort
write.call("#{e}/FINAL_SYNTAX_REVIEW.json",{validator:'Ruby JSON.parse',status:'PASS',excluded_intentionally_invalid_negative_fixtures:invalid,python_executed:false})
FileUtils.cp('/tmp/r33_seal_integrator.rb',"#{e}/seal_integrator.rb")
files=Dir.glob("#{e}/**/*").select{|p|File.file?(p)&& !%w[FILES.json SHA256SUMS SEAL_VERIFIED.json].include?(File.basename(p))}.sort.map{|p|{path:p.delete_prefix(e+'/'),sha256:Digest::SHA256.file(p).hexdigest,bytes:File.size(p)}}
write.call("#{e}/FILES.json",files)
File.write("#{e}/SHA256SUMS",files.map{|x|"#{x[:sha256]}  #{e}/#{x[:path]}\n"}.join)
raise 'hash' unless files.all?{|x|Digest::SHA256.file("#{e}/#{x[:path]}").hexdigest==x[:sha256]}
write.call("#{e}/SEAL_VERIFIED.json",{files:files.length,status:'PASS',manifest_sha256:Digest::SHA256.file("#{e}/FILES.json").hexdigest,sha256sums_sha256:Digest::SHA256.file("#{e}/SHA256SUMS").hexdigest})
File.write('/tmp/r33_final_push_20260915_1409/integrator.final',"Bounded integration sealed: #{rel}/final_closeout.json\nV68/V73 original intended shapes repaired and pass on unchanged stable; V71, expanded V92/all fresh modes, continuing packet/refusal/continuation and learn-refusal, repaired N19 bounded review pass.\nR33 NOT COMPLETE: N17 26 unresolved rows, V91 native generator parity 0/16, R25 native lineage blocked. Exact historical receipt custody is witness only.\n#{files.length} frozen file hashes verified; JSON validated excluding three intentional malformed negative fixtures. Canonical R27 60423/0 unchanged, exposure=0, learner authority=false, successor=false, compiler promotion=false. No Python or LLM superiority claim.\n")
puts e
