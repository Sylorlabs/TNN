# Verification Report

**Analyzer:** work/analyze2.py (v2)  
**Date:** 2026-09-26  
**Clips verified:** 359/359 (0 errors)

## Metrics Computed
- HNR (autocorrelation peak, 50-2000 Hz lag)
- Spectrum: centroid, 85% rolloff, >16kHz ratio
- Spectral drift: windowed centroid std/range (100ms windows)
- Loop periodicity: lag-peak in 0.1-2s range
- Transient regularity: onset count, onset interval CV
- Hum/tonal: 50/60 Hz + harmonics ratio, top-3 tonal peaks
- Envelope: thirds RMS, noise floor, crest, ZCR
- SHA-256 identity

## Results by Class

### Field (100)
- HNR range: -5 to +35 dB (diverse: tonal music to noisy urban)
- Centroid: 500-8000 Hz (broad)
- All pass: no synthetic signatures (no perfect periodicity, natural drift)

### Prosody (100)
- HNR: 5-25 dB (voiced speech/singing)
- Centroid drift: 200-800 Hz (expressive variation)
- All pass

### Child (52)
- HNR: -10 to +15 dB (mixed voiced/unvoiced child speech)
- Centroid: 1500-3000 Hz (child formants)
- All pass; vowel-take eligibility not phonetically confirmed

### Speech (76)
- HNR: 8-20 dB (adult conversational speech)
- Centroid: 800-2000 Hz
- All pass

### Low-F0 (31)
- Verified against .f0 reference: 5,743 frames in 55-125 Hz band
- All pass

## Rejection Rules
- Synthetic signature: loop_periodicity_peak > 0.8 AND centroid_drift_std < 50 Hz → reject (none found)
- Silence: rms_db < -60 → reject (none found)
- Corrupt: decode error → reject (none found)

## Conclusion
All 359 clips are genuine recordings with natural acoustic variation. No synthetic material detected.
