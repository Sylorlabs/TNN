#!/usr/bin/env python3
"""Part 2: white-box the intake loss. Residual-domain analysis from the .npz models.
Where does the cry peak doubling come from: quantization, plm, or LPC feedback?
"""
import wave, json
import numpy as np

SR = 44100

def load_wav(p):
    w = wave.open(p, 'rb')
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)
    w.close(); return x

def load_npz(path):
    m = dict(np.load(path, allow_pickle=True))
    for k in ('q', 'uni', 'bg'):
        if k in m: m[k] = m[k].astype(np.int64)
    for k in ('P', 'K', 'pT', 'NBINS', 'ob0', 'ob1', 'frlen', 'n', 'sr'):
        m[k] = int(m[k])
    return m

def f0_ac(x, lo=60, hi=1500):
    x = x - x.mean(); n = len(x)
    lmin = max(2, int(SR / hi)); lmax = min(n - 1, int(SR / lo))
    lags = np.arange(lmin, lmax + 1)
    r = np.array([np.dot(x[:n - l], x[l:]) for l in lags])
    r /= (r[0] + 1e-30)
    # first local max above 0.3
    for i in range(1, len(r) - 1):
        if r[i] > 0.3 and r[i] >= r[i-1] and r[i] >= r[i+1]:
            y0, y1, y2 = r[i-1], r[i], r[i+1]
            den = (y0 - 2*y1 + y2)
            d = 0.5 * (y0 - y2) / den if abs(den) > 1e-12 else 0.0
            return float(SR / (lags[i] + max(-1.0, min(1.0, d))))
    return 0.0

def hnr_ac(x):
    f0 = f0_ac(x)
    if f0 <= 0: return float('-inf')
    x = x - x.mean(); n = len(x); lag = int(round(SR / f0))
    if lag >= n or lag < 1: return float('-inf')
    rho = min(np.dot(x[:n-lag], x[lag:]) / (np.dot(x, x) + 1e-30), 0.999999)
    if rho <= 0: return float('-inf')
    import math
    return float(10 * math.log10(rho / (1 - rho)))

def lpc_residual(x, a):
    P = len(a); n = len(x); res = np.zeros(n)
    res[:P] = x[:P]
    for i in range(P, n):
        res[i] = x[i] - np.dot(a, x[i-P:i][::-1])
    return res

def synth(a, rv):
    P = len(a); n = len(rv); est = np.zeros(n)
    for i in range(n):
        take = min(i, P)
        pred = np.dot(a[:take], est[i-1::-1][:take]) if take else 0.0
        est[i] = pred + rv[i]
    return est

FX = '/home/hatch/workspace/rawbyte_longmem'
out = {}
for name in ['strike', 'cry', 'clang', 'vowel']:
    x = load_wav(f'{FX}/fixture_{name}.wav')
    m = load_npz(f'{FX}/m5g_{name}.npz')
    P, K = m['P'], m['K']
    a, proto, q = m['a'], m['proto'], m['q']
    n = len(x); nr = n - P
    res_true = lpc_residual(x, a)          # what the intake actually heard
    plm = m['plm']; T0, NBINS = float(m['T0']), m['NBINS']
    boost = float(m.get('boost', 1.0))
    use_h = (m['pT'] > 0 and T0 > 0 and len(plm) == NBINS and 1.5 < boost < 10.0)
    bins = (np.floor((np.arange(nr) / T0) % 1.0 * NBINS).astype(np.int64)) % NBINS
    nres_true = res_true[P:] - (plm[bins] if use_h else 0.0)
    qres_held = proto[q[:nr]]               # quantized noise residual (held)
    qerr = nres_true - qres_held
    # model residual as re-emit uses it (noise proto + plm, head quirk aside)
    rv_held = np.zeros(n); rv_held[P:] = qres_held + (plm[bins] if use_h else 0.0)
    rv_held[:P] = proto[q[:P]] + (plm[(np.floor((np.arange(P) / T0) % 1.0 * NBINS).astype(np.int64)) % NBINS] if use_h else 0.0)
    y_nodecay = synth(a, rv_held)
    yq = np.clip(np.round(y_nodecay), -32768, 32767)
    # LPC synthesis peak gain (impulse response)
    imp = np.zeros(512); imp[0] = 1000.0
    ir = synth(a, imp)
    # quantization SNR in residual domain
    sig = float(np.sqrt(np.mean(nres_true**2)))
    err = float(np.sqrt(np.mean(qerr**2)))
    row = dict(
        f0_fixture=round(f0_ac(x), 2), hnr_fixture=round(hnr_ac(x), 2),
        f0_py_reemit=round(f0_ac(yq), 2),
        n=int(n), P=int(P), K=int(K), pT=int(m['pT']), T0=round(T0, 3),
        NBINS=int(NBINS), boost=round(boost, 3), use_h=bool(use_h),
        res_true_peak=int(np.abs(res_true).max()),
        res_true_rms=round(float(np.sqrt(np.mean(res_true**2))), 1),
        nres_rms=round(sig, 1),
        quant_err_rms=round(err, 1),
        quant_snr_db=round(20 * np.log10(sig / (err + 1e-30)), 2),
        held_resid_peak=int(np.abs(rv_held).max()),
        py_reemit_peak=int(np.abs(yq).max()),
        py_reemit_corr=round(float(np.corrcoef(x, yq)[0, 1]), 5),
        lpc_impulse_peak_gain=round(float(np.abs(ir).max()) / 1000.0, 2),
        plm_peak=int(np.abs(plm).max()) if len(plm) else 0,
        plm_rms=round(float(np.sqrt(np.mean(plm**2))) if len(plm) else 0.0, 1),
        proto_spread=round(float(proto.max() - proto.min()), 1),
    )
    # where is the fixture peak, and what does the model hold there?
    ip = int(np.abs(x).argmax())
    row['fixture_peak_idx'] = ip
    row['res_true_at_peak'] = round(float(res_true[ip]), 1)
    if ip >= P:
        row['held_resid_at_peak'] = round(float(rv_held[ip]), 1)
        row['q_idx_at_peak'] = int(q[ip - P])
        row['proto_at_peak'] = round(float(proto[q[ip - P]]), 1)
    out[name] = row
    print(f"== {name} ==")
    print(f"  f0 fixture={row['f0_fixture']} reemit={row['f0_py_reemit']}  hnr fixture={row['hnr_fixture']}")
    print(f"  pT={row['pT']} T0={row['T0']} boost={row['boost']} use_h={row['use_h']}")
    print(f"  res_true peak={row['res_true_peak']} rms={row['res_true_rms']} | nres rms={row['nres_rms']} quant_err rms={row['quant_err_rms']} SNR={row['quant_snr_db']} dB")
    print(f"  held_resid peak={row['held_resid_peak']} plm peak={row['plm_peak']} plm rms={row['plm_rms']} proto spread={row['proto_spread']}")
    print(f"  fixture peak idx={ip} res_true there={row['res_true_at_peak']} held_resid there={row.get('held_resid_at_peak')} (q={row.get('q_idx_at_peak')} proto={row.get('proto_at_peak')})")
    print(f"  py_reemit peak={row['py_reemit_peak']} corr={row['py_reemit_corr']} | LPC impulse peak gain={row['lpc_impulse_peak_gain']}")
json.dump(out, open('/tmp/intake/whitebox.json', 'w'), indent=1)
print('wrote /tmp/intake/whitebox.json')
