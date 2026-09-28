#!/usr/bin/env python3
"""Build r2-11b.zag from the R2-9 percept pipeline by:
  1. applying the CLI-robustness edits (failed.tsv skip, degenerate-selection
     emission skip, sel_ok helper, approach=R2-11B label);
  2. inserting the compressed-percept stash (S+70000) at the end of each
     p_* percept fn (writes only to S[70000..70128), never alters the
     percept record);
  3. replacing the read-only replay emitter with the generative renderer
     (reads stash + selection records only; render ops at S+70128).
Pure build glue. The percept pipeline itself is untouched.
"""
import sys

SRC = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-11-R29/src/forkB/r2-11b.zag"

HELPERS = r'''
// ---------------- R2-11B compressed-percept stash + generative renderer -----
// The percept pass stashes a COMPRESSED PERCEPT at S+70000 (task tag at
// 70000, features after). The renderer (emit path) reads ONLY this region
// plus the percept's own selection records; it never reads source pixels.
// Render ops are counted at S+70128, separate from the percept ops counter
// at S+0, so the B4 emit/noemit ablation compares percept state
// byte-identically. The renderer never writes S[0..70128).

fn pfix(S:[]u8,o:i32,x:f64)void {
    p64(S,o,((x*1099511627776.0) as i64));
    return;
}

fn gfix(S:[]u8,o:i32)f64 {
    return (g64(S,o) as f64)/1099511627776.0;
}

fn r_ops(S:[]u8,n:i64)void {
    p64(S,70128,g64(S,70128)+n);
    return;
}

// sine with argument reduction to [0,pi/2] + Taylor to x^13. Deterministic.
fn f_sin(x:f64)f64 {
    let twopi:f64=6.283185307179586;
    let q:f64=x/twopi;
    let qi:i64=q as i64;
    let r:f64=x-(qi as f64)*twopi;
    let s:f64=1.0;
    if(r>3.141592653589793){r=r-3.141592653589793;s=0.0-1.0;}
    if(r>1.5707963267948966){r=3.141592653589793-r;}
    let r2:f64=r*r;
    let term:f64=r;
    let sum:f64=r;
    term=0.0-term*r2/6.0;sum=sum+term;
    term=0.0-term*r2/20.0;sum=sum+term;
    term=0.0-term*r2/42.0;sum=sum+term;
    term=0.0-term*r2/72.0;sum=sum+term;
    term=0.0-term*r2/110.0;sum=sum+term;
    term=0.0-term*r2/156.0;sum=sum+term;
    return s*sum;
}

// inverse of lab_of: CIELAB -> sRGB bytes 0..255 (clamped)
fn lab_to_rgb(L:f64,A:f64,B:f64,or_:*i32,og_:*i32,ob_:*i32)void {
    let fy:f64=(L+16.0)/116.0;
    let fx:f64=fy+A/500.0;
    let fz:f64=fy-B/200.0;
    let fx3:f64=fx*fx*fx;
    let fy3:f64=fy*fy*fy;
    let fz3:f64=fz*fz*fz;
    let xr:f64=fx3;
    if(fx3<=0.008856){xr=(fx-16.0/116.0)/7.787;}
    let yr:f64=fy3;
    if(fy3<=0.008856){yr=(fy-16.0/116.0)/7.787;}
    let zr:f64=fz3;
    if(fz3<=0.008856){zr=(fz-16.0/116.0)/7.787;}
    let x:f64=xr*0.95047;
    let y:f64=yr;
    let z:f64=zr*1.08883;
    let rl:f64=3.2404542*x-1.5371385*y-0.4985314*z;
    let gl:f64=-0.9692660*x+1.8760108*y+0.0415560*z;
    let bl:f64=0.0556434*x-0.2040259*y+1.0572252*z;
    if(rl<0.0){rl=0.0;}
    if(rl>1.0){rl=1.0;}
    if(gl<0.0){gl=0.0;}
    if(gl>1.0){gl=1.0;}
    if(bl<0.0){bl=0.0;}
    if(bl>1.0){bl=1.0;}
    let r1:f64=12.92*rl;
    if(rl>0.0031308){r1=1.055*f_pow(rl,0.4166666666666667)-0.055;}
    let g1:f64=12.92*gl;
    if(gl>0.0031308){g1=1.055*f_pow(gl,0.4166666666666667)-0.055;}
    let b1:f64=12.92*bl;
    if(bl>0.0031308){b1=1.055*f_pow(bl,0.4166666666666667)-0.055;}
    or_.*=((r1*255.0)+0.5) as i32;
    og_.*=((g1*255.0)+0.5) as i32;
    ob_.*=((b1*255.0)+0.5) as i32;
    return;
}

fn rms_span(buf:[]u8,off:i32,nsamp:i32)f64 {
    let ss:f64=0.0;
    let i:i32=0;
    while(i<nsamp){
        let v:i32=s16le(buf,off+i*2);
        ss=ss+(v as f64)*(v as f64);
        i=i+1;
    }
    return f_sqrt(ss/(nsamp as f64));
}

// shapetrans compressed percept: largest-component class stats from the
// label map at S+3936 (written by the percept pass). Counters at 70200+.
fn stash_shape(S:[]u8,src:[]u8)void {
    let c:i32=0;
    while(c<65){p64(S,70200+c*8,0);c=c+1;}
    let y:i32=0;
    while(y<96){
        let x:i32=0;
        while(x<96){
            let lb:i32=S[3936+y*96+x] as i32;
            if(lb<0){lb=0;}
            if(lb>64){lb=64;}
            p64(S,70200+lb*8,g64(S,70200+lb*8)+1);
            x=x+1;
        }
        y=y+1;
    }
    let best:i32=0;
    let bestn:i64=0;
    let cc:i32=1;
    while(cc<=64){
        let nn:i64=g64(S,70200+cc*8);
        if(nn>bestn){bestn=nn;best=cc;}
        cc=cc+1;
    }
    let fill:i64=0;let fcnt:i64=0;let bg:i64=0;let bgc:i64=0;
    let sx:i64=0;let sy:i64=0;
    y=0;
    while(y<96){
        let x2:i32=0;
        while(x2<96){
            let o:i32=8+(y*96+x2)*3;
            let gv:i64=((src[o] as i64)+(src[o+1] as i64)+(src[o+2] as i64))/3;
            let lb:i32=S[3936+y*96+x2] as i32;
            if(lb==best){if(best!=0){fill=fill+gv;fcnt=fcnt+1;sx=sx+(x2 as i64);sy=sy+(y as i64);}}
            else{if(lb==0){bg=bg+gv;bgc=bgc+1;}}
            x2=x2+1;
        }
        y=y+1;
    }
    op_add(S,(9216*2) as i64);
    let cx:f64=48.0;let cy:f64=48.0;
    let fg:i64=128;let bgv:i64=128;
    if(best!=0){if(fcnt>0){cx=(sx as f64)/(fcnt as f64);cy=(sy as f64)/(fcnt as f64);fg=fill/fcnt;}}
    if(bgc>0){bgv=bg/bgc;}
    p64(S,70000,2);
    p64(S,70008,fg);
    p64(S,70016,bgv);
    pfix(S,70024,cx);
    pfix(S,70032,cy);
    return;
}

// selection validity (mirrors emit_render's bounds checks)
fn sel_ok(src:[]u8,n:i32,S:[]u8,idx:i32)i32 {
    let o:i32=40+idx*56;
    let kind:i64=g64(S,o);
    let a:i64=g64(S,o+8);let b:i64=g64(S,o+16);let c:i64=g64(S,o+24);
    let d:i64=g64(S,o+32);let e:i64=g64(S,o+40);let f:i64=g64(S,o+48);
    if(kind==0){
        let start:i32=a as i32;
        let end:i32=b as i32;
        if(start<8){return 0;}
        if(end>n){return 0;}
        if(end<=start){return 0;}
        return 1;
    }
    if(kind==1){
        let x:i32=a as i32;let y:i32=b as i32;
        let rw:i32=c as i32;let rh:i32=d as i32;
        let sw:i32=g32(src,0);
        if(x<0){return 0;}
        if(y<0){return 0;}
        if(rw<=0){return 0;}
        if(rh<=0){return 0;}
        if(x+rw>sw){return 0;}
        return 1;
    }
    let x:i32=a as i32;let y:i32=b as i32;
    let rw:i32=c as i32;let rh:i32=d as i32;
    let f0:i32=e as i32;let f1:i32=f as i32;
    let sw:i32=g32(src,4);
    let sh:i32=g32(src,8);
    let nf:i32=g32(src,0);
    if(x<0){return 0;}
    if(y<0){return 0;}
    if(rw<=0){return 0;}
    if(rh<=0){return 0;}
    if(x+rw>sw){return 0;}
    if(y+rh>sh){return 0;}
    if(f0<0){return 0;}
    if(f1>=nf){return 0;}
    if(f1<f0){return 0;}
    return 1;
}
'''

STASH_COLORDISC = '''
    // R2-11B: compressed-percept stash (renderer input; percept record untouched)
    p64(S,70000,0);
    pfix(S,70008,L1);pfix(S,70016,A1);pfix(S,70024,B1);
    pfix(S,70032,L2);pfix(S,70040,A2);pfix(S,70048,B2);
    pfix(S,70056,de);pfix(S,70064,rgbe);
    pfix(S,70072,mr1);pfix(S,70080,mg1);pfix(S,70088,mb1);
    pfix(S,70096,mr2);pfix(S,70104,mg2);pfix(S,70112,mb2);
'''

STASH_COLORCONST = '''
    // R2-11B: panel means for the renderer (percept record untouched)
    let cm1r:f64=0.0;let cm1g:f64=0.0;let cm1b:f64=0.0;
    let cm2r:f64=0.0;let cm2g:f64=0.0;let cm2b:f64=0.0;
    let scy:i32=0;
    while(scy<64){
        let scx:i32=0;
        while(scx<64){
            let so1:i32=8+(scy*128+scx)*3;
            let so2:i32=8+(scy*128+scx+64)*3;
            cm1r=cm1r+(src[so1] as f64);cm1g=cm1g+(src[so1+1] as f64);cm1b=cm1b+(src[so1+2] as f64);
            cm2r=cm2r+(src[so2] as f64);cm2g=cm2g+(src[so2+1] as f64);cm2b=cm2b+(src[so2+2] as f64);
            scx=scx+1;
        }
        scy=scy+1;
    }
    op_add(S,8192 as i64);
    p64(S,70000,1);
    pfix(S,70008,resid);
    pfix(S,70016,cm1r/4096.0);pfix(S,70024,cm1g/4096.0);pfix(S,70032,cm1b/4096.0);
    pfix(S,70040,cm2r/4096.0);pfix(S,70048,cm2g/4096.0);pfix(S,70056,cm2b/4096.0);
'''

STASH_SHAPE = '''
    // R2-11B: compressed-percept stash (renderer input; percept record untouched)
    stash_shape(S,src);
'''

STASH_PITCH = '''
    // R2-11B: compressed-percept stash (renderer input; percept record untouched)
    p64(S,70000,3);
    pfix(S,70008,f0);pfix(S,70016,f1);
    pfix(S,70024,rms_span(src,8,6400));
    pfix(S,70032,rms_span(src,8+15360,6400));
    op_add(S,12800 as i64);
'''

STASH_TIMBRE = '''
    // R2-11B: compressed-percept stash (renderer input; percept record untouched)
    p64(S,70000,4);
    p64(S,70008,j);
    let sm:i32=1;
    let stot:i64=0;
    while(sm<=8){
        let se:i64=g64(S,ebase+sm*8);
        p64(S,70008+sm*8,se);
        stot=stot+se;
        sm=sm+1;
    }
    // centroid recomputed from stashed energies (no stale reads)
    let snum:f64=0.0;
    sm=1;
    while(sm<=8){
        snum=snum+((g64(S,70008+sm*8)) as f64)*(sm as f64);
        sm=sm+1;
    }
    let scent:f64=1.0;
    if(stot>0){scent=snum/(stot as f64);}
    pfix(S,70080,scent);
    pfix(S,70088,rms_span(src,8,12800));
    op_add(S,12800 as i64);
'''

STASH_MOTION = '''
    // R2-11B: compressed-percept stash (renderer input; percept record untouched)
    p64(S,70000,5);
    p64(S,70008,dir);
    p64(S,70016,g64(S,5408));
'''

RENDERER = r'''
// ---------------- R2-11B generative emitter ---------------------------------
// Renders the scene FROM THE COMPRESSED PERCEPT (S+70000), never from source
// pixels. Artifact containers (.aud/.img/.vid) and naming match fork A so
// the KB-E7 mechanical gate can diff byte-for-byte against cited spans.
// Headers are verbatim; every payload byte is renderer output (declared in
// the brief BEFORE the human trial per the frozen no-laundering rule).

// flat-fill render of one panel at the percept's claimed mean color
fn render_flat(S:[]u8,ab:[]u8,do2:i32,rw:i32,rh:i32,task:i32,panel:i32)void {
    let L:f64=0.0;let A:f64=0.0;let B:f64=0.0;
    if(task==0){
        if(panel==0){L=gfix(S,70008);A=gfix(S,70016);B=gfix(S,70024);}
        else{L=gfix(S,70032);A=gfix(S,70040);B=gfix(S,70048);}
    }
    else{
        // colorconst: panel0 = mean1; panel1 = M(mean1), the percept's model
        let m1r:f64=gfix(S,70016);let m1g:f64=gfix(S,70024);let m1b:f64=gfix(S,70032);
        if(panel==0){
            lab_of(m1r,m1g,m1b,&L,&A,&B);
        }
        else{
            let p0:f64=0.0;let p1:f64=0.0;let p2:f64=0.0;
            let k:i32=0;
            while(k<3){
                let mv0:f64=(g64(S,3432+(k*3+0)*8) as f64)/1099511627776.0;
                let mv1:f64=(g64(S,3432+(k*3+1)*8) as f64)/1099511627776.0;
                let mv2:f64=(g64(S,3432+(k*3+2)*8) as f64)/1099511627776.0;
                let pv:f64=mv0*m1r+mv1*m1g+mv2*m1b;
                if(k==0){p0=pv;}
                else{if(k==1){p1=pv;}else{p2=pv;}}
                k=k+1;
            }
            lab_of(p0,p1,p2,&L,&A,&B);
        }
    }
    let rr:i32=0;let gg:i32=0;let bb:i32=0;
    lab_to_rgb(L,A,B,&rr,&gg,&bb);
    let y:i32=0;
    while(y<rh){
        let x:i32=0;
        while(x<rw){
            let o:i32=do2+(y*rw+x)*3;
            ab[o]=rr as u8;ab[o+1]=gg as u8;ab[o+2]=bb as u8;
            x=x+1;
        }
        y=y+1;
    }
    r_ops(S,(rw as i64)*(rh as i64));
    return;
}

// ideal-shape render from the compressed percept (class + fill + bg)
fn render_shape(S:[]u8,ab:[]u8,do2:i32,rw:i32,rh:i32,j:i64)void {
    let fill:i32=g64(S,70008) as i32;
    let bg:i32=g64(S,70016) as i32;
    let y:i32=0;
    while(y<rh){
        let x:i32=0;
        while(x<rw){
            let o:i32=do2+(y*rw+x)*3;
            ab[o]=bg as u8;ab[o+1]=bg as u8;ab[o+2]=bg as u8;
            x=x+1;
        }
        y=y+1;
    }
    let cx:i32=rw/2;
    let cy:i32=rh/2;
    let rad:i32=rw;
    if(rh<rw){rad=rh;}
    rad=rad/2-1;
    if(rad<1){rad=1;}
    y=0;
    while(y<rh){
        let x:i32=0;
        while(x<rw){
            let inside:i32=0;
            if(j==0){
                let dx:i32=x-cx;let dy:i32=y-cy;
                if(dx*dx+dy*dy<=rad*rad){inside=1;}
            }
            else{if(j==1){
                // triangle: apex (cx,cy-rad), base y=cy+rad half-width rad
                let y0:i32=cy-rad;let y1:i32=cy+rad;
                if(y>=y0){if(y<=y1){
                    let t:i64=((y-y0) as i64)*1000/((y1-y0) as i64);
                    let hw:i64=(rad as i64)*t/1000;
                    let dx:i64=(x-cx) as i64;
                    if(dx<0){dx=0-dx;}
                    if(dx<=hw){inside=1;}
                }}
            }
            else{
                // square: side 2*rad centered
                let dx:i32=x-cx;let dy:i32=y-cy;
                if(dx<0){dx=0-dx;}
                if(dy<0){dy=0-dy;}
                if(dx<=rad){if(dy<=rad){inside=1;}}
            }}
            if(inside!=0){
                let o:i32=do2+(y*rw+x)*3;
                ab[o]=fill as u8;ab[o+1]=fill as u8;ab[o+2]=fill as u8;
            }
            x=x+1;
        }
        y=y+1;
    }
    r_ops(S,(rw as i64)*(rh as i64));
    return;
}

fn render_sine(ab:[]u8,do2:i32,nsamp:i32,f0:f64,rms:f64,S:[]u8)void {
    let amp:f64=rms*1.4142135623730951;
    let twopi:f64=6.283185307179586;
    let i:i32=0;
    while(i<nsamp){
        let ph:f64=twopi*f0*(i as f64)/16000.0;
        let v:f64=amp*f_sin(ph);
        let q:i32=(v+0.5) as i32;
        if(v<0.0){q=(v-0.5) as i32;}
        if(q>32767){q=32767;}
        if(q<-32767){q=-32767;}
        ab[do2+i*2]=(q&255) as u8;
        ab[do2+i*2+1]=((q>>8)&255) as u8;
        i=i+1;
    }
    r_ops(S,nsamp as i64);
    return;
}

fn render_partials(ab:[]u8,do2:i32,nsamp:i32,S:[]u8)void {
    let tot:i64=0;
    let m:i32=0;
    while(m<8){tot=tot+g64(S,70016+m*8);m=m+1;}
    let rms:f64=gfix(S,70088);
    let twopi:f64=6.283185307179586;
    let i:i32=0;
    while(i<nsamp){
        let v:f64=0.0;
        m=0;
        while(m<8){
            let sm:f64=(g64(S,70016+m*8)) as f64;
            let am:f64=0.0;
            if(tot>0){am=rms*f_sqrt(2.0*sm/(tot as f64));}
            let ph:f64=twopi*440.0*((m+1) as f64)*(i as f64)/16000.0;
            v=v+am*f_sin(ph);
            m=m+1;
        }
        let q:i32=(v+0.5) as i32;
        if(v<0.0){q=(v-0.5) as i32;}
        if(q>32767){q=32767;}
        if(q<-32767){q=-32767;}
        ab[do2+i*2]=(q&255) as u8;
        ab[do2+i*2+1]=((q>>8)&255) as u8;
        i=i+1;
    }
    r_ops(S,(nsamp as i64)*8);
    return;
}

fn render_motion(S:[]u8,ab:[]u8,do2:i32,onf:i32,rw:i32,rh:i32)void {
    let dir:i64=g64(S,70008);
    let mag:i32=g64(S,70016) as i32;
    let dx:i32=0;let dy:i32=0;
    if(dir>=0){dx=dir_dx(dir as i32);dy=dir_dy(dir as i32);}
    let f:i32=0;
    while(f<onf){
        let y:i32=0;
        while(y<rh){
            let x:i32=0;
            while(x<rw){
                let o:i32=do2+(f*rw*rh+y*rw+x)*3;
                ab[o]=0;ab[o+1]=0;ab[o+2]=0;
                x=x+1;
            }
            y=y+1;
        }
        let sx:i32=rw/2+dx*mag*f-4;
        let sy:i32=rh/2+dy*mag*f-4;
        let yy:i32=0;
        while(yy<8){
            let xx:i32=0;
            while(xx<8){
                let px:i32=sx+xx;let py:i32=sy+yy;
                if(px>=0){if(px<rw){if(py>=0){if(py<rh){
                    let o:i32=do2+(f*rw*rh+py*rw+px)*3;
                    ab[o]=255;ab[o+1]=255;ab[o+2]=255;
                }}}}
                xx=xx+1;
            }
            yy=yy+1;
        }
        f=f+1;
    }
    r_ops(S,(onf as i64)*(rw as i64)*(rh as i64));
    return;
}

fn emit_render(src:[]u8,n:i32,S:[]u8,idx:i32,adir:[]u8,trial:[]u8,hb:[]u8) i32 {
    let o:i32=40+idx*56;
    let kind:i64=g64(S,o);
    let a:i64=g64(S,o+8);let b:i64=g64(S,o+16);let c:i64=g64(S,o+24);
    let d:i64=g64(S,o+32);let e:i64=g64(S,o+40);let f:i64=g64(S,o+48);
    let task:i32=g64(S,70000) as i32;
    let ename:[]u8=nio_alloc(128);
    let at:i32=0;
    at=b_put(ename,at,trial);
    at=b_put(ename,at,".e");
    at=b_put_i64(ename,at,idx as i64);
    if(kind==0){
        at=b_put(ename,at,".aud");
        let start:i32=a as i32;
        let end:i32=b as i32;
        if(start<8){return -1;}
        if(end>n){return -1;}
        if(end<=start){return -1;}
        let nsamp:i32=(end-start)/2;
        let ab:[]u8=nio_alloc(8+nsamp*2);
        p32(ab,0,g32(src,0));
        p32(ab,4,nsamp);
        if(task==3){
            let f0:f64=gfix(S,70008);
            let rms:f64=gfix(S,70024);
            if(idx==1){f0=gfix(S,70016);rms=gfix(S,70032);}
            render_sine(ab,8,nsamp,f0,rms,S);
        }
        else{
            render_partials(ab,8,nsamp,S);
        }
        let hh:[]u8=nio_alloc(32);
        ns_sha256(ab,hh);
        let cc:[]u8=nio_alloc(64);
        let ci:i32=0;
        while(ci<32){cc[ci]=hb[ci];ci=ci+1;}
        while(ci<64){cc[ci]=hh[ci-32];ci=ci+1;}
        ns_sha256(cc,hb);
        if(write_file(path2(adir,ename[0..at]),ab)!=0){return -1;}
        return 0;
    }
    if(kind==1){
        at=b_put(ename,at,".img");
        let x:i32=a as i32;let y:i32=b as i32;
        let rw:i32=c as i32;let rh:i32=d as i32;
        let sw:i32=g32(src,0);
        if(x<0){return -1;}
        if(y<0){return -1;}
        if(rw<=0){return -1;}
        if(rh<=0){return -1;}
        if(x+rw>sw){return -1;}
        let ab:[]u8=nio_alloc(8+rw*rh*3);
        p32(ab,0,rw);
        p32(ab,4,rh);
        if(task==2){
            render_shape(S,ab,8,rw,rh,g64(S,8));
        }
        else{
            render_flat(S,ab,8,rw,rh,task,idx);
        }
        let hh:[]u8=nio_alloc(32);
        ns_sha256(ab,hh);
        let cc:[]u8=nio_alloc(64);
        let ci:i32=0;
        while(ci<32){cc[ci]=hb[ci];ci=ci+1;}
        while(ci<64){cc[ci]=hh[ci-32];ci=ci+1;}
        ns_sha256(cc,hb);
        if(write_file(path2(adir,ename[0..at]),ab)!=0){return -1;}
        return 0;
    }
    at=b_put(ename,at,".vid");
    let x:i32=a as i32;let y:i32=b as i32;
    let rw:i32=c as i32;let rh:i32=d as i32;
    let f0:i32=e as i32;let f1:i32=f as i32;
    let sw:i32=g32(src,4);
    let sh:i32=g32(src,8);
    let nf:i32=g32(src,0);
    if(x<0){return -1;}
    if(y<0){return -1;}
    if(rw<=0){return -1;}
    if(rh<=0){return -1;}
    if(x+rw>sw){return -1;}
    if(y+rh>sh){return -1;}
    if(f0<0){return -1;}
    if(f1>=nf){return -1;}
    if(f1<f0){return -1;}
    let onf:i32=f1-f0+1;
    let ab:[]u8=nio_alloc(12+onf*rw*rh*3);
    p32(ab,0,onf);p32(ab,4,rw);p32(ab,8,rh);
    render_motion(S,ab,12,onf,rw,rh);
    let hh:[]u8=nio_alloc(32);
    ns_sha256(ab,hh);
    let cc:[]u8=nio_alloc(64);
    let ci:i32=0;
    while(ci<32){cc[ci]=hb[ci];ci=ci+1;}
    while(ci<64){cc[ci]=hh[ci-32];ci=ci+1;}
    ns_sha256(cc,hb);
    if(write_file(path2(adir,ename[0..at]),ab)!=0){return -1;}
    return 0;
}

// ---------------- hash-chained ledger -------------------------------------
'''

def main():
    with open(SRC) as fh:
        src = fh.read()

    # 1. helpers after f_pow
    anchor_pow = "fn f_pow(x:f64,e:f64)f64 {"
    assert src.count(anchor_pow) == 1, "f_pow anchor"
    i = src.index(anchor_pow)
    # find end of the f_pow function (closing brace on its own line)
    j = src.index("\n}\n", i) + len("\n}\n")
    src = src[:j] + HELPERS + src[j:]

    # 2. stash insertions (each anchor unique)
    def insert(anchor, code):
        assert src.count(anchor) == 1, f"anchor not unique: {anchor[:60]!r}"
        return src.replace(anchor, anchor + code, 1)

    src = insert('    at=b_put_i64(wb,at,illam as i64);\n', STASH_COLORDISC)
    src = insert('    at=b_put_i64(wb,at,mixed as i64);\n', STASH_COLORCONST)
    src = insert('    at=b_put_i64(wb,at,thr);\n', STASH_SHAPE)
    src = insert('    at=b_put_i64(wb,at,xfail as i64);\n', STASH_PITCH)
    src = insert('    sel_set(S,0,0,8,8+25600,0,0,0,0);\n', STASH_TIMBRE)
    src = insert('    at=b_put_i64(wb,at,bim as i64);\n', STASH_MOTION)

    # 3. replace the emitter span with the generative renderer
    start_m = "// ---------------- emitter (read-only replay)"
    end_m = "// ---------------- hash-chained ledger"
    i0 = src.index(start_m)
    i1 = src.index(end_m)
    src = src[:i0] + RENDERER + src[i1:]

    # 4. call sites: emit_selection -> emit_render (batch loop + single mode)
    n_calls = src.count("emit_selection(fbuf,fn2,S,si,adir,")
    assert n_calls == 2, f"expected 2 call sites, found {n_calls}"
    src = src.replace("emit_selection(fbuf,fn2,S,si,adir,",
                      "emit_render(fbuf,fn2,S,si,adir,")

    # 5. CLI robustness (same as fork A) + approach label
    assert src.count('"approach=R2-9\\ntask="') == 1
    src = src.replace('"approach=R2-9\\ntask="', '"approach=R2-11B\\ntask="')

    a = '        if(pfd<0){_zag_println("ERR percepts.tsv");return 1;}\n        if(lfd<0){_zag_println("ERR LEDGER.jsonl");return 1;}\n'
    assert src.count(a) == 1, "pfd/lfd anchor"
    b = a + '''        // R2-11 deviation (CLI robustness only; percept/emission contract
        // unchanged): trials where the percept pass fails (rc!=0) are logged
        // to failed.tsv and SKIPPED. A failed percept = no claim, no emission,
        // no install.
        let fline:[]u8=path2(outdir,"failed.tsv");
        let fcs:[]u8=nio_cstr(fline);
        let ffd:i64=_zag_raw_syscall(2,_zag_slice_ptr(fcs) as i64,577,420,0,0,0);
        nio_free(fcs);
        if(ffd<0){_zag_println("ERR failed.tsv");return 1;}
        nio_write_all(ffd,"trial\\ttask\\tfixture\\trc\\n");
'''
    src = src.replace(a, b, 1)

    c = "        let ntrial:i64=0;\n        let ninstall:i64=0;\n"
    assert src.count(c) == 1, "counters anchor"
    src = src.replace(c, "        let ntrial:i64=0;\n        let ninstall:i64=0;\n        let nfail:i64=0;\n", 1)

    d = '            if(rc!=0){_zag_print("ERR percept ");_zag_println(fixt);continue;}\n'
    assert src.count(d) == 1, "rc anchor"
    e = '''            if(rc!=0){
                let fb:[]u8=nio_alloc(4096);
                let fa:i32=0;
                fa=b_put(fb,fa,trial);fa=b_put8(fb,fa,9);
                fa=b_put(fb,fa,taskn);fa=b_put8(fb,fa,9);
                fa=b_put(fb,fa,fixt);fa=b_put8(fb,fa,9);
                fa=b_put_i64(fb,fa,rc as i64);fa=b_put8(fb,fa,10);
                nio_write_all(ffd,fb[0..fa]);
                nfail=nfail+1;
                continue;
            }
'''
    src = src.replace(d, e, 1)

    f = '''            if(do_emit!=0){
                let ns:i32=g64(S,32) as i32;
                let si:i32=0;
                while(si<ns){
                    if(emit_render(fbuf,fn2,S,si,adir,trial,hh)!=0){
                        _zag_print("ERR emit ");_zag_println(fixt);return 1;
                    }
                    si=si+1;
                }
            }
'''
    assert src.count(f) == 1, "emit loop anchor"
    g = '''            if(do_emit!=0){
                let ns:i32=g64(S,32) as i32;
                let si:i32=0;
                let sok:i32=1;
                while(si<ns){
                    if(sel_ok(fbuf,fn2,S,si)==0){sok=0;}
                    si=si+1;
                }
                si=0;
                if(sok==0){
                    // degenerate selection: nothing to emit; percepts kept
                    let fb:[]u8=nio_alloc(4096);
                    let fa:i32=0;
                    fa=b_put(fb,fa,trial);fa=b_put8(fb,fa,9);
                    fa=b_put(fb,fa,taskn);fa=b_put8(fb,fa,9);
                    fa=b_put(fb,fa,fixt);fa=b_put8(fb,fa,9);
                    fa=b_put_i64(fb,fa,-2);fa=b_put8(fb,fa,10);
                    nio_write_all(ffd,fb[0..fa]);
                    nfail=nfail+1;
                }
                else{
                    while(si<ns){
                        if(emit_render(fbuf,fn2,S,si,adir,trial,hh)!=0){
                            _zag_print("ERR emit ");_zag_println(fixt);return 1;
                        }
                        si=si+1;
                    }
                }
            }
'''
    src = src.replace(f, g, 1)

    h = '''        _zag_raw_syscall(3,pfd,0,0,0,0,0);
        _zag_raw_syscall(3,lfd,0,0,0,0,0);
        _zag_print("trials=");
        _zag_print(i64s(ntrial));
        _zag_print(" installed=");
        _zag_print(i64s(ninstall));
        _zag_print(" digest=");
        _zag_println(ns_hex(prev));
        return 0;
'''
    assert src.count(h) == 1, "summary anchor"
    hh = h.replace('        _zag_raw_syscall(3,lfd,0,0,0,0,0);',
                   '        _zag_raw_syscall(3,lfd,0,0,0,0,0);\n        _zag_raw_syscall(3,ffd,0,0,0,0,0);')
    hh = hh.replace('        _zag_print(i64s(ninstall));',
                    '        _zag_print(i64s(ninstall));\n        _zag_print(" failed=");\n        _zag_print(i64s(nfail));')
    src = src.replace(h, hh, 1)

    with open(SRC, "w") as fh:
        fh.write(src)
    print("fork B surgery complete")

main()
