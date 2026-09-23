# Derivation (glue): case_r24_rk3_ext.txt = frozen case rows + |t1|agree|strong from frozen sweep.jsonl, keyed by seq.
import json, hashlib
case_p='/home/hatch/workspace/ceiling_test/frozen/case_r24_rk3.txt'
sweep_p='/home/hatch/workspace/ceiling_test/scratch/sweep.jsonl'
out_p='/home/hatch/workspace/ceiling_test/runs/exp_c/case_r24_rk3_ext.txt'
sw={}
for line in open(sweep_p):
    r=json.loads(line); sw[r['seq']]=(r['t1'],r['agree'],r['strong'])
n=0
with open(case_p) as fin, open(out_p,'w') as fout:
    for line in fin:
        line=line.rstrip('\n')
        seq=int(line.split('|',1)[0])
        t1,ag,st=sw[seq]
        fout.write("%s|%d|%d|%d\n" % (line,t1,ag,st)); n+=1
h=hashlib.sha256(open(out_p,'rb').read()).hexdigest()
print("rows:",n,"sha256:",h)
