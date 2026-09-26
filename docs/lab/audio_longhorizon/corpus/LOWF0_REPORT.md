# Low-F0 Reference Report (PTDB-TUG)

**Speakers:** M01-M10 (male, ages 22-40)  
**Pairs:** 31 microphone + laryngograph-derived F0  
**Source:** https://www2.spsc.tugraz.at/databases/PTDB-TUG/

## F0 Reference Format
- **File:** `.f0` ASCII, 4 columns, 10ms frames (100 fps)
- **Column 3 (index 2):** F0 in Hz (empirical; documentation says col1 but data shows col3)
- **Column 4:** Peak-normalized autocorrelation (0-1)
- **Columns 1-2:** Always 0.0 (unused)
- **Documentation discrepancy:** PTDB-TUG_REPORT.pdf §2 says "pitch, voicing decision, RMS, peak-norm autocorr respectively" (implying col1=pitch), but empirical data shows F0 values (55-125 Hz) in column 3. Using column 3.

## Coverage (55-125 Hz band)
- **Total inband frames:** 5,743
- **b1 (55-80 Hz):** 3,791 frames
- **b2 (80-100 Hz):** 1,088 frames  
- **b3 (100-125 Hz):** 864 frames

## Selected Pairs (by inband fraction)
Top: M09_sa1 (66.2%), M03_sa2 (65.3%), M03_sa1 (64.0%), M09_sa2 (59.2%), M06_sa2 (59.0%)

## Sentences
- sa1, sa2: All 10 speakers (TIMIT dialect sentences)
- si453-460: M01 only
- si642-644: M02 only

## Usage
Microphone WAVs normalized to 44.1kHz mono PCM16. Original .f0 preserved alongside (10ms frames align to original 48kHz; resampling does not affect F0 reference validity for 55-125 Hz band).
