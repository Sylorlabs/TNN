import numpy as np
exec(open('hunt_fossils2.py').read().split('def cut_fossil')[0])
x,sr=load(SRC)
f0,rr=ac_f0_frames(x,sr)
voiced=(rr>0.6)&(f0>250)&(f0<1400)
n=1102;hop=441
corr=np.zeros(len(f0)-1); CH=2000
for c0 in range(0,len(f0),CH):
    c1=min(len(f0),c0+CH)
    idx=np.arange(n)[None,:]+hop*np.arange(c0,c1)[:,None]
    L=liftered_logspec(x[np.clip(idx,0,len(x)-1)].astype(np.float64))
    Ln=L/(np.linalg.norm(L,axis=1,keepdims=True)+1e-12)
    corr[c0:c1-1]=(Ln[:-1]*Ln[1:]).sum(axis=1)
    del L,Ln,idx
out=open('corrcheck_out.txt','w')
v=voiced[1:]
out.write('voiced corr pct '+str(np.percentile(corr[v],[50,90,95,99,99.5,100]))+'\n')
for th in (0.96,0.97,0.975,0.98,0.985):
    ok=voiced[1:]&(corr>th); best=cur=0
    for b in ok:
        cur=cur+1 if b else 0
        if cur>best: best=cur
    out.write('th=%.3f longest run %d frames (%d ms)\n'%(th,best,best*10))
out.close()
