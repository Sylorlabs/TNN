require 'json';require 'digest';require 'open3'
base=File.dirname(File.expand_path(__dir__));dest=File.expand_path(__dir__)
edits=[]
adapt=lambda do |input,output,&block|
 original=File.binread(input);text=block.call(original.dup)
 File.binwrite(output,text)
 diff,err,st=Open3.capture3('diff','-u',input,output)
 raise err unless [0,1].include?(st.exitstatus)
 edits<<{original:input,original_sha256:Digest::SHA256.hexdigest(original),derived:output,derived_sha256:Digest::SHA256.hexdigest(text),diff:diff,diff_argv:['diff','-u',input,output],diff_exit:st.exitstatus}
end
replace=lambda do |text,from,to|
 raise "not unique: #{from}" unless text.scan(Regexp.new(Regexp.escape(from))).size==1
 text.sub!(from,to)
end
adapt.call(base+'/r26_digest.zag',dest+'/r26_output.zag') do |s|
 replace.call(s,'@import("identity.zag")','@import("../identity.zag")')
 s=s.split("\nfn main()i32 {",2).first+"\n"
 replace.call(s,'fn r26_build(finalize:i32)i32 {','fn r26_build_output(finalize:i32,out:[]u8)i32 {\n    if(out.len!=64){return 79;}'.gsub('\\n',"\n"))
 replace.call(s,'_zag_print("R26_NATIVE_DIGEST,");_zag_println(text);nio_free(text);r26_free(&b);mi_loaded_close(&p);return 0;', 'if(text.len!=64){nio_free(text);r26_free(&b);mi_loaded_close(&p);return 98;}let output_index:i32=0;while(output_index<64){out[output_index]=text[output_index];output_index=output_index+1;}_zag_print("R26_NATIVE_DIGEST,");_zag_println(text);nio_free(text);r26_free(&b);mi_loaded_close(&p);return 0;')
 s
end
adapt.call(base+'/r27_digest.zag',dest+'/r27_fused.zag') do |s|
 replace.call(s,'@import("identity.zag")','@import("r26_output.zag")')
 replace.call(s,'fn r27_build(finalize:i32)i32 {',"fn r27_build(finalize:i32)i32 {\n    let native_base_digest:[]u8=nio_alloc(64);if(native_base_digest.len!=64){return 79;}if(r26_selftest()!=0){nio_free(native_base_digest);return 78;}let base_result:i32=r26_build_output(1,native_base_digest);if(base_result!=0){nio_free(native_base_digest);return base_result;}")
 replace.call(s,'r27_add(&b,"44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649");','r27_add(&b,native_base_digest);nio_free(native_base_digest);')
 s
end
File.write(dest+'/FUSED_SOURCE_ADAPTATION.json',JSON.pretty_generate({purpose:'Remove cached R26 digest preimage literal. Native R26 recomputation publishes caller-owned 64-byte ASCII digest only after successful preimage finalization. R27 consumes that fresh output in the same process; original routines/selectors/guards retained.',changes:edits,scope_exclusions:['Independent review of the new fused adapter has not occurred.','No R25 recursion, standalone R25/R26 file linkage, lineage suite or runtime equivalence is inferred.','R26 and R27 independently reload the same hash-bound immutable map.','Existing source-specific canonical JSON float spellings and fixed accepted-parent selectors remain bounded to this parent.','Some inherited error paths leak short-lived allocations; no hostile-host or OOM containment claim.']})+"\n")
