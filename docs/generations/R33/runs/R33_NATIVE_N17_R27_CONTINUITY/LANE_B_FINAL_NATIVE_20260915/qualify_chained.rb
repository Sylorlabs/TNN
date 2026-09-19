require 'json';require 'digest';require 'open3';require 'fileutils'
repo='/Users/Shared/micah/Documents/TNN/TNN';base=repo+'/Research/R33_NATIVE_N17_R27_CONTINUITY';d=File.expand_path(__dir__)+'/chained_final'
FileUtils.mkdir_p(d+'/sources');FileUtils.mkdir_p(d+'/logs')
log=File.open(d+'/commands.jsonl','wx')
run=lambda do |label,args,expected|
 out,err,st=Open3.capture3(*args,chdir:repo);File.binwrite(d+'/logs/'+label+'.stdout',out);File.binwrite(d+'/logs/'+label+'.stderr',err)
 log.puts(JSON.generate({label:label,argv:args,cwd:repo,exit:st.exitstatus,expected:expected,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err)}));log.flush
 puts "#{label}: #{st.exitstatus}";raise label unless st.exitstatus==expected;out
end
changes=[]
replace=lambda do |text,old,new|
 raise 'nonunique source edit' unless text.scan(Regexp.new(Regexp.escape(old))).size==1
 changes<<{old:old,new:new};text.sub(old,new)
end
r26=File.binread(base+'/r26_digest.zag');r27=File.binread(base+'/r27_digest.zag')
File.binwrite(d+'/sources/r26.original.zag',r26);File.binwrite(d+'/sources/r27.original.zag',r27)
lib26=r26[0...r26.rindex('fn main()i32')]
lib26=replace.call(lib26,'@import("identity.zag")','@import("../../../identity.zag")')
lib26=replace.call(lib26,'fn r26_build(finalize:i32)i32 {','fn r26_build(finalize:i32,fresh_digest:[]u8)i32 {'+"\n    if(fresh_digest.len!=64 || finalize!=1){return 98;}")
old='_zag_print("R26_NATIVE_DIGEST,");_zag_println(text);nio_free(text);r26_free(&b);mi_loaded_close(&p);return 0;'
new='if(text.len!=64){nio_free(text);r26_free(&b);mi_loaded_close(&p);return 98;}let copy_at:i32=0;while(copy_at<64){fresh_digest[copy_at]=text[copy_at];copy_at=copy_at+1;}'+old
lib26=replace.call(lib26,old,new)
File.binwrite(d+'/sources/r26_fresh_library.zag',lib26)
lib27=replace.call(r27,'@import("identity.zag")','@import("r26_fresh_library.zag")')
lib27=replace.call(lib27,'fn r27_build(finalize:i32)i32 {','fn r27_build(finalize:i32)i32 {'+"\n    if(r26_selftest()!=0){return 79;}let fresh_r26:[]u8=nio_alloc(64);if(fresh_r26.len!=64){return 79;}let dependency_rc:i32=r26_build(1,fresh_r26);if(dependency_rc!=0){nio_free(fresh_r26);return dependency_rc;}")
lib27=replace.call(lib27,'r27_add(&b,"44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649");','r27_add(&b,fresh_r26);nio_free(fresh_r26);')
File.binwrite(d+'/sources/r27_chained.zag',lib27)
File.write(d+'/SOURCE_TRANSFORM.json',JSON.pretty_generate({scope:'Additive engineering variant; R26 output bytes copied directly into R27 preimage, no expected digest input or CLI-supplied dependency',changes:changes,r26_before:Digest::SHA256.hexdigest(r26),r26_after:Digest::SHA256.hexdigest(lib26),r27_before:Digest::SHA256.hexdigest(r27),r27_after:Digest::SHA256.hexdigest(lib27),removed_r26_main:r26[r26.rindex('fn main()i32')..-1],original_sources_mutated:false})+"\n")
c='/Users/Shared/micah/Documents/zag/znc';flags=['--target','macos-arm64','--no-zagd','--no-analyze','--no-foreground-cache']
run.call('build_project',[c,base+'/V91_SEMANTIC_KAT/v91_project_native.zag',*flags,'-o',d+'/project'],0)
run.call('project_chained',[d+'/project',d+'/sources/r27_chained.zag',d+'/chained.zag',d+'/chained.provenance'],0)
File.readlines(d+'/chained.provenance',chomp:true).each{|l|w=l.split("\t");next unless w[0]=='FILE';p=w[2];target=d+'/import_closure/'+p;FileUtils.mkdir_p(File.dirname(target));FileUtils.cp(p,target)}
run.call('build_chained',[c,d+'/chained.zag',*flags,'-o',d+'/chained'],0)
out=run.call('chained_digest',[d+'/chained','digest'],0)
raise 'comparison' unless out.lines.include?("R26_NATIVE_DIGEST,44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649\n") && out.lines.include?("R27_NATIVE_DIGEST,562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04\n")
run.call('chained_usage',[d+'/chained'],64)
run.call('chained_bad_mode',[d+'/chained','unadmitted'],64)
%w[canonical protected].each{|n|run.call(n+'_after',['shasum','-a','256','-c',repo+'/Research/R33_CLOSEOUT_20260915T174458Z/'+n+'.sha256'],0)}
run.call('compiler_after',['shasum','-a','256',c],0)
log.close
