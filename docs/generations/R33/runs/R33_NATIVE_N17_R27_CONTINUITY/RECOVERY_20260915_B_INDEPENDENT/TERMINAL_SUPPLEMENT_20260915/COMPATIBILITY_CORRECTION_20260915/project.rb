require 'json';require 'digest';require 'fileutils'
d=File.expand_path(__dir__);base=File.dirname(d)+'/sources';files=Dir.glob(base+'/N17/*.zag');constants={}
files.each do |path|
 File.read(path).scan(/^const\s+(\w+):(i32|i64)\s*=\s*(-?\d+)\s*;/) do |name,type,value|
 raise "duplicate #{name}" if constants.key?(name)
 n=Integer(value);bits=type=='i32' ? 32 : 64;raise name unless n>=-(2**(bits-1))&&n<2**(bits-1)
 constants[name]={type:type,decimal:value,declaration_file:File.basename(path)}
 end
end
FileUtils.mkdir_p(d+'/sources/N17');FileUtils.mkdir_p(d+'/bin');FileUtils.mkdir_p(d+'/evidence');FileUtils.mkdir_p(d+'/fixtures')
metadata=[]
files.each do |path|
 original=File.read(path);edits=[]
 original.to_enum(:scan,/^const\s+\w+:(?:i32|i64)\s*=\s*-?\d+\s*;/).each{m=Regexp.last_match;edits<<{start:m.begin(0),old:m[0],replacement:'',kind:'numeric_declaration_projection'}}
 original.to_enum(:scan,/"(?:\\.|[^"\\])*"|\/\/[^\n]*|\/\*.*?\*\/|\b[A-Za-z_]\w*\b/m).each do
  m=Regexp.last_match;token=m[0];next unless constants.key?(token);next if edits.any?{|e|m.begin(0)>=e[:start]&&m.begin(0)<e[:start]+e[:old].length}
  c=constants[token];edits<<{start:m.begin(0),old:token,replacement:"(#{c[:decimal]} as #{c[:type]})",kind:'exact_typed_scalar_projection'}
 end
 edits.sort_by!{|e|e[:start]};projected='';pos=0
 edits.each{|e|projected<<original[pos...e[:start]];e[:output_start]=projected.length;projected<<e[:replacement];pos=e[:start]+e[:old].length};projected<<original[pos..]
 reversed=projected.dup;edits.reverse_each{|e|raise 'replacement mismatch' unless reversed[e[:output_start],e[:replacement].length]==e[:replacement];reversed[e[:output_start],e[:replacement].length]=e[:old]};raise 'body changed' unless reversed==original
 File.write(d+'/sources/N17/'+File.basename(path),projected)
 metadata<<{file:File.basename(path),original_sha256:Digest::SHA256.hexdigest(original),projected_sha256:Digest::SHA256.hexdigest(projected),inverse_source_byte_equality:true,edits:edits}
end
%w[R33_NATIVE_IO_V1.zag R33_NATIVE_SHA256_V2.zag].each{|n|FileUtils.cp(base+'/'+n,d+'/sources/'+n);metadata<<{file:n,original_sha256:Digest::SHA256.file(base+'/'+n).hexdigest,projected_sha256:Digest::SHA256.file(d+'/sources/'+n).hexdigest,unchanged:true}}
File.write(d+'/NATIVE_SOURCE_CONVERSION.json',JSON.pretty_generate({identity:'N17_NATIVE_TYPED_NUMERIC_COMPATIBILITY_PROJECTION',decision:'REVIEWED_SOURCE_EQUIVALENT_CORRECTION',rule:'Replace only simple immutable numeric const declarations/references with exact declared numeric value cast to its declared i32/i64 type. No evaluation, rounding, source/spec inference or constraint weakening. String/comment tokens, hashes, literal limits, operators, branches, import paths and all other source bytes preserved. Inverse edit proof reconstructs each original source byte-for-byte.',relative_import_closure:'N17 child imports resolve inside this isolated correction; ../ native SHA/IO paths preserved.',constants:constants,files:metadata})+"\n")
puts "projected #{files.length} sources, #{constants.length} exact typed declarations; inverse source equality PASS"
