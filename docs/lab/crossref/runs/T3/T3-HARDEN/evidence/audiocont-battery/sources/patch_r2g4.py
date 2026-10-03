#!/usr/bin/env python3
"""Restructure bridge_world / bridge_ocean GBMODE==1 control in r2g.zag.

Control = core [t0,t1] placement-identical to standard (same salts, same
spans, const gain via the m[48] flag) + fresh-salt wings [t0-2,t0] and
[t1,t1+2] so captured material runs continuously through the nominal edges.
No insertion/removal is authored at t0/t1 in the control."""
P = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/r2g/r2g.zag"
src = open(P).read()

def rep(old, new, n=1):
    global src
    c = src.count(old)
    assert c == n, f"expected {n}, found {c} for: {old[:70]!r}"
    src = src.replace(old, new)

rep("""    scatter(h,m,nsamp,c_wash,e0,ew,1.1,salt+3,0.16);
    scatter(h,m,nsamp,c_rumble,e0,ew,2.2,salt+1,0.10);
    scatter(h,m,nsamp,c_swell,e0,e1,3.5,salt,0.30);
    scatter(h,m,nsamp,c_crack,e0,e1,1.7,salt+2,0.12);
    put64(m,48,0);
}""",
"""    if(bm==1){
        // wings: fresh-salt material so the texture runs through t0/t1
        let w0:f64=t0-2.0; if(w0<0.0){w0=0.0;}
        let w1:f64=t1+2.0; if(w1>30.0){w1=30.0;}
        scatter(h,m,nsamp,c_wash,w0,t0,1.1,salt+101,0.16);
        scatter(h,m,nsamp,c_rumble,w0,t0,2.2,salt+102,0.10);
        scatter(h,m,nsamp,c_swell,w0,t0,3.5,salt+103,0.30);
        scatter(h,m,nsamp,c_crack,w0,t0,1.7,salt+104,0.12);
        scatter(h,m,nsamp,c_wash,t1,w1,1.1,salt+105,0.16);
        scatter(h,m,nsamp,c_rumble,t1,w1,2.2,salt+106,0.10);
        scatter(h,m,nsamp,c_swell,t1,w1,3.5,salt+107,0.30);
        scatter(h,m,nsamp,c_crack,t1,w1,1.7,salt+108,0.12);
    }
    // core: identical placements to standard (same salts, same spans)
    scatter(h,m,nsamp,c_wash,t0,wt1,1.1,salt+3,0.16);
    scatter(h,m,nsamp,c_rumble,t0,wt1,2.2,salt+1,0.10);
    scatter(h,m,nsamp,c_swell,t0,t1,3.5,salt,0.30);
    scatter(h,m,nsamp,c_crack,t0,t1,1.7,salt+2,0.12);
    put64(m,48,0);
}""")

rep("""    let e0:f64=t0; let e1:f64=t1; let ew:f64=wt1;
    if(bm==1){
        e0=t0-2.0; if(e0<0.0){e0=0.0;}
        e1=t1+2.0; if(e1>28.0){e1=28.0;}
        ew=wt1+2.0; if(ew>28.0){ew=28.0;}
        put64(m,48,1);
    }
    scatter(h,m,nsamp,c_wash,e0,ew,0.9,salt+3,0.20);
    scatter(h,m,nsamp,c_wind,e0,ew,1.4,salt+1,0.055);  // breath / air
    run_feet(h,m,nsamp,c_thump,e0,e1,1.2,salt,0.10);    // shuffling feet
    scatter(h,m,nsamp,c_laugh,e0,e1,0.9,salt+2,0.09);   // distant play
    put64(m,48,0);
}""",
"""    if(bm==1){
        put64(m,48,1);
        // wings: fresh-salt material so the texture runs through t0/t1
        let w0:f64=t0-2.0; if(w0<0.0){w0=0.0;}
        let w1:f64=t1+2.0; if(w1>28.0){w1=28.0;}
        scatter(h,m,nsamp,c_wash,w0,t0,0.9,salt+101,0.20);
        scatter(h,m,nsamp,c_wind,w0,t0,1.4,salt+102,0.055);
        run_feet(h,m,nsamp,c_thump,w0,t0,1.2,salt+103,0.10);
        scatter(h,m,nsamp,c_laugh,w0,t0,0.9,salt+104,0.09);
        scatter(h,m,nsamp,c_wash,t1,w1,0.9,salt+105,0.20);
        scatter(h,m,nsamp,c_wind,t1,w1,1.4,salt+106,0.055);
        run_feet(h,m,nsamp,c_thump,t1,w1,1.2,salt+107,0.10);
        scatter(h,m,nsamp,c_laugh,t1,w1,0.9,salt+108,0.09);
    }
    // core: identical placements to standard (same salts, same spans)
    scatter(h,m,nsamp,c_wash,t0,wt1,0.9,salt+3,0.20);
    scatter(h,m,nsamp,c_wind,t0,wt1,1.4,salt+1,0.055);  // breath / air
    run_feet(h,m,nsamp,c_thump,t0,t1,1.2,salt,0.10);    // shuffling feet
    scatter(h,m,nsamp,c_laugh,t0,t1,0.9,salt+2,0.09);   // distant play
    put64(m,48,0);
}""")

open(P, "w").write(src)
print("bridge control restructure OK")
