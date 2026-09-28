# AUDIO LONG-HORIZON Corpus — Quota Table (v1 Seal)

**Seal date:** 2026-09-26  
**Prereg commit:** `1278e148dd5bbe6bbbd0516e1f66f730b5a21c2b`  
**Total clips sealed:** 359

## Quota Buckets

| Class | Quota | Built | Status | Sources | Per-source |
|-------|-------|-------|--------|---------|------------|
| Field (non-speech) | 100 | 100 | ✅ PASS | FSD50K, TAU, ESC-50, UrbanSounds | 25 each (25%) |
| Speech (conversational) | 150 | 76 | ❌ SHORTFALL | VoxCeleb1-mini, Earnings22 | 38 each (50%) |
| Child (vowel takes) | 50 | 52 | ⚠️ COUNT OK, ELIGIBILITY UNCONFIRMED | SpeechOcean, TomRoma, FSD50K, local kid | 13 each (25%) |
| Prosody (expressive) | 100 | 100 | ✅ PASS | RAVDESS, CREMA-D, MIR-1K, EmoV-DB | 25 each (25%) |
| **Total** | **400** | **328** | ❌ SHORTFALL 72 | | |

## Low-F0 Reference Subset (non-quota)

| Item | Count | Details |
|------|-------|---------|
| PTDB-TUG pairs | 31 | Male speakers M01-M10, 55-125 Hz F0 with laryngograph-derived reference |
| Total inband frames | 5,743 | b1(55-80): 3,791, b2(80-100): 1,088, b3(100-125): 864 |
| F0 column | 3 (index 2) | 10ms frames; doc says col1 but empirical data shows col3 |

## Shortfalls Requiring Micah-Approved Amendment

### 1. Speech Class (74 clips, 2 sources)
- **Built:** 76 clips (38 VoxCeleb1-mini + 38 Earnings22)
- **Quota:** 150 clips from ≥30 speakers
- **25% cap:** With 2 sources, max compliant is 38 clips (19 per source). Current 76 violates cap (50% per source).
- **Need:** 2 additional conversational speech sources, 74 more clips (38 per source × 2 = 76, total 152)
- **Speakers:** VoxCeleb1-mini provides 19 speakers; Earnings22 provides ~24-40 speakers across 5 calls (estimated). Total ≥30 likely met, but speaker IDs for Earnings22 are call-level, not individual.

### 2. Child Vowel-Take Eligibility
- **Built:** 52 child speech clips (13 SpeechOcean + 13 TomRoma + 13 FSD50K + 13 local kidb/kide)
- **Quota:** 50 "kidc.wav-class: child speech vowel takes"
- **Issue:** The 52 clips are verified real child speech, but NOT phonetically verified as "vowel takes". 
  - SpeechOcean, TomRoma, FSD50K: General child speech (sentences, not isolated vowels)
  - Local kidb/kide: 13 clips from same recording session as kidc.wav, chosen by RMS/HNR; may be vowel-like but not phonetically confirmed
- **Acoustic note:** kidc.wav has HNR -5.46 dB (aperiodic), centroid 2024 Hz, suggesting breathy/child vocalization rather than sustained vowels
- **Need:** Phonetic verification (requires listening or transcripts) OR accept as "child speech" with amendment

### 3. Total Count
- **Built:** 328 quota clips
- **Quota:** 400
- **Shortfall:** 72 clips (entirely due to speech shortfall)

## Diversity Compliance (25% cap)

| Class | Sources | Max per source | Compliant? |
|-------|---------|----------------|------------|
| Field | 4 | 25/100 = 25% | ✅ |
| Prosody | 4 | 25/100 = 25% | ✅ |
| Child | 4 | 13/52 = 25% | ✅ (count) |
| Speech | 2 | 38/76 = 50% | ❌ |

## Notes
- All 359 clips are genuinely recorded (no synthetic).
- All clips normalized to RIFF/WAV, PCM16, mono, 44.1 kHz via ffmpeg 8.1.2.
- Analyzer-first verification passed on all 359 (HNR, spectra, drift, loop, transients, hum, SHA).
- No trial binary has opened any corpus WAV as of seal.
