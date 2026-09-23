"""Shared audio analysis utilities for continuity round-2 machine tests.
Pure numpy/scipy. Deterministic. All measures per PREREG_ROUND2.md."""
import numpy as np
from scipy import signal as ssig

SR = 44100

def read_wav(path):
    """Return mono float64 samples in [-1,1]."""
    with open(path, 'rb') as f:
        b = f.read()
    assert b[0:4] == b'RIFF' and b[12:16] == b'fmt ', path
    # find data chunk
    pos = 12
    sr = None; ch = None
    while pos < len(b):
        cid = b[pos:pos+4]; sz = int.from_bytes(b[pos+4:pos+8], 'little')
        if cid == b'fmt ':
            ch = int.from_bytes(b[16:18], 'little')
            sr = int.from_bytes(b[24:28], 'little')
        if cid == b'data':
            raw = b[pos+8:pos+8+sz]
            break
        pos += 8 + sz + (sz & 1)
    assert sr == SR, (path, sr)
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768.0
    if ch == 2:
        x = x.reshape(-1, 2).mean(axis=1)
    return x

def bandpass(x, lo, hi):
    """FFT brickwall bandpass (deterministic, zero-phase)."""
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1.0 / SR)
    mask = (f >= lo) & (f <= hi)
    X[~mask] = 0.0
    return np.fft.irfft(X, n)

def env_1ms(x):
    """1 ms rectified envelope: max abs over non-overlapping 1 ms frames."""
    n1 = SR // 1000  # 44
    m = len(x) // n1
    return np.abs(x[:m * n1].reshape(m, n1)).max(axis=1)

def rms_10ms(x):
    """10 ms RMS over non-overlapping 10 ms frames."""
    n10 = SR // 100  # 441
    m = len(x) // n10
    fr = x[:m * n10].reshape(m, n10)
    return np.sqrt((fr ** 2).mean(axis=1))

def rms_1ms(x):
    n1 = SR // 1000
    m = len(x) // n1
    fr = x[:m * n1].reshape(m, n1)
    return np.sqrt((fr ** 2).mean(axis=1))

def stft_logmag(x, win_s=0.046, hop_s=0.010):
    """Log-magnitude STFT, Hann window. Returns (frames, bins)."""
    win = int(win_s * SR); hop = int(hop_s * SR)
    w = np.hanning(win)
    nfr = 1 + (len(x) - win) // hop
    out = np.empty((nfr, win // 2 + 1), dtype=np.float32)
    for i in range(nfr):
        seg = x[i * hop:i * hop + win] * w
        out[i] = np.log10(np.abs(np.fft.rfft(seg)) + 1e-9)
    return out

def spectral_flux(S):
    """Frame-to-frame L2 distance of log-mag spectra."""
    d = np.diff(S, axis=0)
    return np.sqrt((d ** 2).sum(axis=1))

def mann_whitney_u_greater(a, b):
    """One-sided Mann-Whitney U (a > b), normal approx with tie correction.
    Returns (U, z, p_one_sided)."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    n1, n2 = len(a), len(b)
    vals = np.concatenate([a, b])
    order = np.argsort(vals, kind='mergesort')
    ranks = np.empty(len(vals))
    i = 0
    tie_sum = 0.0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        r = (i + j) / 2.0 + 1
        ranks[order[i:j + 1]] = r
        t = j - i + 1
        tie_sum += t ** 3 - t
        i = j + 1
    R1 = ranks[:n1].sum()
    U1 = R1 - n1 * (n1 + 1) / 2.0
    mu = n1 * n2 / 2.0
    N = n1 + n2
    var = n1 * n2 / 12.0 * ((N + 1) - tie_sum / (N * (N - 1)))
    z = (U1 - mu) / np.sqrt(var) if var > 0 else 0.0
    from math import erf
    p = 0.5 * (1 - erf(z / np.sqrt(2)))
    return U1, z, p

def sign_test_greater(diffs):
    """One-sided paired sign test H1: median(diff) > 0. Returns (nplus, n, p)."""
    from math import comb
    d = [x for x in diffs if x != 0]
    n = len(d); k = sum(1 for x in d if x > 0)
    p = sum(comb(n, j) for j in range(k, n + 1)) / 2 ** n if n else 1.0
    return k, n, p

def wilcoxon_signed_rank(diffs, alternative='two-sided'):
    """Wilcoxon signed-rank via scipy; returns (stat, p)."""
    from scipy.stats import wilcoxon
    d = np.asarray(diffs, float)
    d = d[d != 0]
    if len(d) == 0:
        return 0.0, 1.0
    return wilcoxon(d, alternative=alternative)
