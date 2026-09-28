# Embedded CAVLC tables (verified 2026-09-26 against cynthia/codecs-in-markdown 05816ee).
# Key: (code_length, bit_string) -> value.
COEFF_TOKEN_NC0 = {(1, '1'): (0, 0), (2, '01'): (1, 1), (3, '001'): (2, 2), (5, '00011'): (3, 3), (6, '000011'): (4, 3), (6, '000100'): (2, 1), (6, '000101'): (1, 0), (7, '0000100'): (5, 3), (7, '0000101'): (3, 2), (8, '00000100'): (6, 3), (8, '00000101'): (4, 2), (8, '00000110'): (3, 1), (8, '00000111'): (2, 0), (9, '000000100'): (7, 3), (9, '000000101'): (5, 2), (9, '000000110'): (4, 1), (9, '000000111'): (3, 0), (10, '0000000100'): (8, 3), (10, '0000000101'): (6, 2), (10, '0000000110'): (5, 1), (10, '0000000111'): (4, 0), (11, '00000000100'): (9, 3), (11, '00000000101'): (7, 2), (11, '00000000110'): (6, 1), (11, '00000000111'): (5, 0), (13, '0000000001000'): (8, 0), (13, '0000000001001'): (9, 2), (13, '0000000001010'): (8, 1), (13, '0000000001011'): (7, 0), (13, '0000000001100'): (10, 3), (13, '0000000001101'): (8, 2), (13, '0000000001110'): (7, 1), (13, '0000000001111'): (6, 0), (14, '00000000001000'): (12, 3), (14, '00000000001001'): (11, 2), (14, '00000000001010'): (10, 1), (14, '00000000001011'): (10, 0), (14, '00000000001100'): (11, 3), (14, '00000000001101'): (10, 2), (14, '00000000001110'): (9, 1), (14, '00000000001111'): (9, 0), (15, '000000000000001'): (13, 1), (15, '000000000001000'): (14, 3), (15, '000000000001001'): (13, 2), (15, '000000000001010'): (12, 1), (15, '000000000001011'): (12, 0), (15, '000000000001100'): (13, 3), (15, '000000000001101'): (12, 2), (15, '000000000001110'): (11, 1), (15, '000000000001111'): (11, 0), (16, '0000000000000100'): (16, 0), (16, '0000000000000101'): (16, 2), (16, '0000000000000110'): (16, 1), (16, '0000000000000111'): (15, 0), (16, '0000000000001000'): (16, 3), (16, '0000000000001001'): (15, 2), (16, '0000000000001010'): (15, 1), (16, '0000000000001011'): (14, 0), (16, '0000000000001100'): (15, 3), (16, '0000000000001101'): (14, 2), (16, '0000000000001110'): (14, 1), (16, '0000000000001111'): (13, 0)}
COEFF_TOKEN_NC1 = {(2, '10'): (1, 1), (2, '11'): (0, 0), (3, '011'): (2, 2), (4, '0100'): (4, 3), (4, '0101'): (3, 3), (5, '00110'): (5, 3), (5, '00111'): (2, 1), (6, '000100'): (7, 3), (6, '000101'): (4, 2), (6, '000110'): (4, 1), (6, '000111'): (2, 0), (6, '001000'): (6, 3), (6, '001001'): (3, 2), (6, '001010'): (3, 1), (6, '001011'): (1, 0), (7, '0000100'): (8, 3), (7, '0000101'): (5, 2), (7, '0000110'): (5, 1), (7, '0000111'): (3, 0), (8, '00000100'): (5, 0), (8, '00000101'): (6, 2), (8, '00000110'): (6, 1), (8, '00000111'): (4, 0), (9, '000000100'): (9, 3), (9, '000000101'): (7, 2), (9, '000000110'): (7, 1), (9, '000000111'): (6, 0), (11, '00000001000'): (11, 3), (11, '00000001001'): (9, 2), (11, '00000001010'): (9, 1), (11, '00000001011'): (8, 0), (11, '00000001100'): (10, 3), (11, '00000001101'): (8, 2), (11, '00000001110'): (8, 1), (11, '00000001111'): (7, 0), (12, '000000001000'): (11, 0), (12, '000000001001'): (11, 2), (12, '000000001010'): (11, 1), (12, '000000001011'): (10, 0), (12, '000000001100'): (12, 3), (12, '000000001101'): (10, 2), (12, '000000001110'): (10, 1), (12, '000000001111'): (9, 0), (13, '0000000000001'): (15, 3), (13, '0000000000110'): (14, 2), (13, '0000000000111'): (14, 0), (13, '0000000001000'): (14, 3), (13, '0000000001001'): (13, 2), (13, '0000000001010'): (13, 1), (13, '0000000001011'): (13, 0), (13, '0000000001100'): (13, 3), (13, '0000000001101'): (12, 2), (13, '0000000001110'): (12, 1), (13, '0000000001111'): (12, 0), (14, '00000000000100'): (16, 3), (14, '00000000000101'): (16, 2), (14, '00000000000110'): (16, 1), (14, '00000000000111'): (16, 0), (14, '00000000001000'): (15, 1), (14, '00000000001001'): (15, 0), (14, '00000000001010'): (15, 2), (14, '00000000001011'): (14, 1)}
COEFF_TOKEN_NC2 = {(4, '1000'): (7, 3), (4, '1001'): (6, 3), (4, '1010'): (5, 3), (4, '1011'): (4, 3), (4, '1100'): (3, 3), (4, '1101'): (2, 2), (4, '1110'): (1, 1), (4, '1111'): (0, 0), (5, '01000'): (5, 1), (5, '01001'): (5, 2), (5, '01010'): (4, 1), (5, '01011'): (4, 2), (5, '01100'): (3, 1), (5, '01101'): (8, 3), (5, '01110'): (3, 2), (5, '01111'): (2, 1), (6, '001000'): (3, 0), (6, '001001'): (7, 2), (6, '001010'): (7, 1), (6, '001011'): (2, 0), (6, '001100'): (9, 3), (6, '001101'): (6, 2), (6, '001110'): (6, 1), (6, '001111'): (1, 0), (7, '0001000'): (7, 0), (7, '0001001'): (6, 0), (7, '0001010'): (9, 2), (7, '0001011'): (5, 0), (7, '0001100'): (10, 3), (7, '0001101'): (8, 2), (7, '0001110'): (8, 1), (7, '0001111'): (4, 0), (8, '00001000'): (12, 3), (8, '00001001'): (11, 2), (8, '00001010'): (10, 1), (8, '00001011'): (9, 0), (8, '00001100'): (11, 3), (8, '00001101'): (10, 2), (8, '00001110'): (9, 1), (8, '00001111'): (8, 0), (9, '000000111'): (13, 1), (9, '000001000'): (12, 0), (9, '000001001'): (13, 2), (9, '000001010'): (12, 1), (9, '000001011'): (11, 0), (9, '000001100'): (13, 3), (9, '000001101'): (12, 2), (9, '000001110'): (11, 1), (9, '000001111'): (10, 0), (10, '0000000001'): (16, 0), (10, '0000000010'): (16, 3), (10, '0000000011'): (16, 2), (10, '0000000100'): (16, 1), (10, '0000000101'): (15, 0), (10, '0000000110'): (15, 3), (10, '0000000111'): (15, 2), (10, '0000001000'): (15, 1), (10, '0000001001'): (14, 0), (10, '0000001010'): (14, 3), (10, '0000001011'): (14, 2), (10, '0000001100'): (14, 1), (10, '0000001101'): (13, 0)}
COEFF_TOKEN_NC3 = {(6, '000000'): (1, 0), (6, '000001'): (1, 1), (6, '000011'): (0, 0), (6, '000100'): (2, 0), (6, '000101'): (2, 1), (6, '000110'): (2, 2), (6, '001000'): (3, 0), (6, '001001'): (3, 1), (6, '001010'): (3, 2), (6, '001011'): (3, 3), (6, '001100'): (4, 0), (6, '001101'): (4, 1), (6, '001110'): (4, 2), (6, '001111'): (4, 3), (6, '010000'): (5, 0), (6, '010001'): (5, 1), (6, '010010'): (5, 2), (6, '010011'): (5, 3), (6, '010100'): (6, 0), (6, '010101'): (6, 1), (6, '010110'): (6, 2), (6, '010111'): (6, 3), (6, '011000'): (7, 0), (6, '011001'): (7, 1), (6, '011010'): (7, 2), (6, '011011'): (7, 3), (6, '011100'): (8, 0), (6, '011101'): (8, 1), (6, '011110'): (8, 2), (6, '011111'): (8, 3), (6, '100000'): (9, 0), (6, '100001'): (9, 1), (6, '100010'): (9, 2), (6, '100011'): (9, 3), (6, '100100'): (10, 0), (6, '100101'): (10, 1), (6, '100110'): (10, 2), (6, '100111'): (10, 3), (6, '101000'): (11, 0), (6, '101001'): (11, 1), (6, '101010'): (11, 2), (6, '101011'): (11, 3), (6, '101100'): (12, 0), (6, '101101'): (12, 1), (6, '101110'): (12, 2), (6, '101111'): (12, 3), (6, '110000'): (13, 0), (6, '110001'): (13, 1), (6, '110010'): (13, 2), (6, '110011'): (13, 3), (6, '110100'): (14, 0), (6, '110101'): (14, 1), (6, '110110'): (14, 2), (6, '110111'): (14, 3), (6, '111000'): (15, 0), (6, '111001'): (15, 1), (6, '111010'): (15, 2), (6, '111011'): (15, 3), (6, '111100'): (16, 0), (6, '111101'): (16, 1), (6, '111110'): (16, 2), (6, '111111'): (16, 3)}
COEFF_TOKEN_NCM1 = {(1, '1'): (1, 1), (2, '01'): (0, 0), (3, '001'): (2, 2), (6, '000010'): (4, 0), (6, '000011'): (3, 0), (6, '000100'): (2, 0), (6, '000101'): (3, 3), (6, '000110'): (2, 1), (6, '000111'): (1, 0), (7, '0000000'): (4, 3), (7, '0000010'): (3, 2), (7, '0000011'): (3, 1), (8, '00000010'): (4, 2), (8, '00000011'): (4, 1)}
COEFF_TOKEN_NCM2 = {(1, '1'): (0, 0), (2, '01'): (1, 1), (3, '001'): (2, 2), (5, '00001'): (3, 3), (6, '000001'): (4, 3), (7, '0001000'): (6, 3), (7, '0001001'): (5, 3), (7, '0001010'): (4, 2), (7, '0001011'): (3, 2), (7, '0001100'): (3, 1), (7, '0001101'): (2, 1), (7, '0001110'): (2, 0), (7, '0001111'): (1, 0), (9, '000000100'): (5, 2), (9, '000000101'): (4, 1), (9, '000000110'): (4, 0), (9, '000000111'): (3, 0), (10, '0000000100'): (7, 3), (10, '0000000101'): (6, 2), (10, '0000000110'): (5, 1), (10, '0000000111'): (5, 0), (11, '00000000100'): (8, 3), (11, '00000000101'): (7, 2), (11, '00000000110'): (6, 1), (11, '00000000111'): (6, 0), (12, '000000000100'): (8, 2), (12, '000000000101'): (8, 1), (12, '000000000110'): (7, 1), (12, '000000000111'): (7, 0), (13, '0000000000111'): (8, 0)}
RUN_BEFORE_ZL1 = {(1, '0'): 1, (1, '1'): 0}
RUN_BEFORE_ZL2 = {(1, '1'): 0, (2, '00'): 2, (2, '01'): 1}
RUN_BEFORE_ZL3 = {(2, '00'): 3, (2, '01'): 2, (2, '10'): 1, (2, '11'): 0}
RUN_BEFORE_ZL4 = {(2, '01'): 2, (2, '10'): 1, (2, '11'): 0, (3, '000'): 4, (3, '001'): 3}
RUN_BEFORE_ZL5 = {(2, '10'): 1, (2, '11'): 0, (3, '000'): 5, (3, '001'): 4, (3, '010'): 3, (3, '011'): 2}
RUN_BEFORE_ZL6 = {(2, '11'): 0, (3, '000'): 1, (3, '001'): 2, (3, '010'): 4, (3, '011'): 3, (3, '100'): 6, (3, '101'): 5}
RUN_BEFORE_ZL7 = {(3, '001'): 6, (3, '010'): 5, (3, '011'): 4, (3, '100'): 3, (3, '101'): 2, (3, '110'): 1, (3, '111'): 0, (4, '0001'): 7, (5, '00001'): 8, (6, '000001'): 9, (7, '0000001'): 10, (8, '00000001'): 11, (9, '000000001'): 12, (10, '0000000001'): 13, (11, '00000000001'): 14}
TOTAL_ZEROS_CHDC_TZ1 = {(1, '1'): 0, (2, '01'): 1, (3, '000'): 3, (3, '001'): 2}
TOTAL_ZEROS_CHDC_TZ2 = {(1, '1'): 0, (2, '00'): 2, (2, '01'): 1}
TOTAL_ZEROS_CHDC_TZ3 = {(1, '0'): 1, (1, '1'): 0}
TOTAL_ZEROS_TZ1 = {(1, '1'): 0, (3, '010'): 2, (3, '011'): 1, (4, '0010'): 4, (4, '0011'): 3, (5, '00010'): 6, (5, '00011'): 5, (6, '000010'): 8, (6, '000011'): 7, (7, '0000010'): 10, (7, '0000011'): 9, (8, '00000010'): 12, (8, '00000011'): 11, (9, '000000001'): 15, (9, '000000010'): 14, (9, '000000011'): 13}
TOTAL_ZEROS_TZ10 = {(2, '01'): 5, (2, '10'): 4, (2, '11'): 3, (3, '001'): 2, (4, '0001'): 6, (5, '00000'): 1, (5, '00001'): 0}
TOTAL_ZEROS_TZ11 = {(1, '1'): 4, (3, '001'): 2, (3, '010'): 3, (3, '011'): 5, (4, '0000'): 0, (4, '0001'): 1}
TOTAL_ZEROS_TZ12 = {(1, '1'): 3, (2, '01'): 2, (3, '001'): 4, (4, '0000'): 0, (4, '0001'): 1}
TOTAL_ZEROS_TZ13 = {(1, '1'): 2, (2, '01'): 3, (3, '000'): 0, (3, '001'): 1}
TOTAL_ZEROS_TZ14 = {(1, '1'): 2, (2, '00'): 0, (2, '01'): 1}
TOTAL_ZEROS_TZ15 = {(1, '0'): 0, (1, '1'): 1}
TOTAL_ZEROS_TZ2 = {(3, '011'): 4, (3, '100'): 3, (3, '101'): 2, (3, '110'): 1, (3, '111'): 0, (4, '0010'): 8, (4, '0011'): 7, (4, '0100'): 6, (4, '0101'): 5, (5, '00010'): 10, (5, '00011'): 9, (6, '000000'): 14, (6, '000001'): 13, (6, '000010'): 12, (6, '000011'): 11}
TOTAL_ZEROS_TZ3 = {(3, '011'): 7, (3, '100'): 6, (3, '101'): 3, (3, '110'): 2, (3, '111'): 1, (4, '0010'): 8, (4, '0011'): 5, (4, '0100'): 4, (4, '0101'): 0, (5, '00001'): 12, (5, '00010'): 10, (5, '00011'): 9, (6, '000000'): 13, (6, '000001'): 11}
TOTAL_ZEROS_TZ4 = {(3, '011'): 8, (3, '100'): 6, (3, '101'): 5, (3, '110'): 4, (3, '111'): 1, (4, '0010'): 9, (4, '0011'): 7, (4, '0100'): 3, (4, '0101'): 2, (5, '00000'): 12, (5, '00001'): 11, (5, '00010'): 10, (5, '00011'): 0}
TOTAL_ZEROS_TZ5 = {(3, '011'): 7, (3, '100'): 6, (3, '101'): 5, (3, '110'): 4, (3, '111'): 3, (4, '0001'): 10, (4, '0010'): 8, (4, '0011'): 2, (4, '0100'): 1, (4, '0101'): 0, (5, '00000'): 11, (5, '00001'): 9}
TOTAL_ZEROS_TZ6 = {(3, '001'): 9, (3, '010'): 7, (3, '011'): 6, (3, '100'): 5, (3, '101'): 4, (3, '110'): 3, (3, '111'): 2, (4, '0001'): 8, (5, '00001'): 1, (6, '000000'): 10, (6, '000001'): 0}
TOTAL_ZEROS_TZ7 = {(2, '11'): 5, (3, '001'): 8, (3, '010'): 6, (3, '011'): 4, (3, '100'): 3, (3, '101'): 2, (4, '0001'): 7, (5, '00001'): 1, (6, '000000'): 9, (6, '000001'): 0}
TOTAL_ZEROS_TZ8 = {(2, '10'): 5, (2, '11'): 4, (3, '001'): 7, (3, '010'): 6, (3, '011'): 3, (4, '0001'): 1, (5, '00001'): 2, (6, '000000'): 8, (6, '000001'): 0}
TOTAL_ZEROS_TZ9 = {(2, '01'): 6, (2, '10'): 4, (2, '11'): 3, (3, '001'): 5, (4, '0001'): 2, (5, '00001'): 7, (6, '000000'): 1, (6, '000001'): 0}
CBP_INTRA = [47, 31, 15, 0, 23, 27, 29, 30, 7, 11, 13, 14, 39, 43, 45, 46, 16, 3, 5, 10, 12, 19, 21, 26, 28, 35, 37, 42, 44, 1, 2, 4, 8, 17, 18, 20, 24, 6, 9, 22, 25, 32, 33, 34, 36, 40, 38, 41]
CBP_INTER = [0, 16, 1, 2, 4, 8, 32, 3, 5, 10, 12, 15, 47, 7, 11, 13, 14, 6, 9, 31, 35, 37, 42, 44, 33, 34, 36, 40, 39, 43, 45, 46, 17, 18, 20, 24, 19, 21, 26, 28, 23, 27, 29, 30, 22, 25, 38, 41]
#!/usr/bin/env python3
"""Pure-Python H.264 Constrained Baseline slice decoder oracle.

Task: universal-format intake order (Micah). Frozen prereg:
  docs/lab/universal_intake/h264/PREREG.md

This file is the B0 oracle: it must reconstruct all 8 frames of the fixture
and match ffmpeg's SHA-256 for every frame before any Zag decoder work begins.

Input: stream.in -- [u32be nNals][u32be len][NAL bytes]... (built by prep_stream.py
from docs/lab/universal_intake/fixtures/t.mp4; stream.in itself is a regenerable
intermediate and is NOT committed).

Modes:
  parse : canonical syntax-element dump to stdout (frozen format v1, see below).
          Used for B1 (Zag canonical dump must match bit-exactly).
  recon : decode pre-deblock frames; print per-frame SHA-256 (B2/B3 evidence).
  final : decode + deblock; print per-frame SHA-256 (B4 evidence).

Determinism: zero RNG; pure integer arithmetic; byte-identical reruns.

Canonical dump format v1 (frozen for B1):
  stream nals=<N>
  nal idx=<i> type=<t> len=<n>
  sps id=<i> profile=<p> level=<l> w=<w> h=<h>
  pps id=<i> sps=<i>
  slice nal=<i> idr=<0|1> type=<I|P> frame_num=<n> idr_pic_id=<n> qp=<SliceQPY> \
        deblock=<idc> alpha_off=<n> beta_off=<n>
  skip run=<n>
  mb a=<addr> type=<name> cbp=<0..47> qp=<QPY>
  i4 b=<blk> m=<mode>            (Intra4x4 pred mode per 4x4 block, block order)
  i16 m=<mode>                   (Intra16x16 pred mode)
  ichroma m=<mode>               (intra chroma pred mode)
  mv part=<mbPartIdx> sub=<subMbPartIdx> dx=<mvd_x> dy=<mvd_y> mx=<mvx> my=<mvy>
      (mvd in quarter-pel units; mvx/mvy reconstructed motion vector, quarter-pel)
  res comp=<y|cb|cr> b=<blk> tc=<TotalCoeff> t1=<TrailingOnes> tz=<totalZeros> \
      lv=<l_TC-1>,...,<l_0> rb=<r_TC-1>,...,<r_1>
      (levels/signs in decode order: trailing ones first; run_before likewise;
       comp=y covers Intra16x16DCLevel(b=16),Intra16x16ACLevel,LumaLevel4x4;
       comp=cb|cr covers ChromaDCLevel(b=4),ChromaACLevel)

Reference: cynthia/codecs-in-markdown @ 05816ee (ITU-T H.264 text).
Profile scope: Constrained Baseline, 4:2:0, frame-only, CAVLC, no MBAFF,
no slice groups, no data partitioning, no field coding.
"""
import sys, hashlib, struct

# ---------------- misc tables ----------------
# 4x4 zigzag scan: scan position -> raster index (y*4+x)
ZSCAN4 = [0,1,4,8,5,2,3,6,9,12,13,10,7,11,14,15]

# Table 8-16 alpha'/beta' indexed 0..51
ALPHA_T = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,5,6,7,8,9,10,12,13,
           15,17,20,22,25,28,32,36,40,45,50,56,63,71,80,90,101,113,127,144,
           162,182,203,226,255,255]
BETA_T  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,3,3,3,3,4,4,4,
           6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13,14,14,15,15,
           16,16,17,17,18,18]
# Table 8-17 tC0': [bS][indexA]
TC0_T = {
 1: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,
     1,1,1,1,1,1,1,2,2,2,2,3,3,3,4,4,4,5,6,6,7,8,9,10,11,13],
 2: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,
     1,1,1,1,1,2,2,2,2,3,3,3,4,4,5,5,6,7,8,8,10,11,12,13,15,17],
 3: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,
     1,2,2,2,2,3,3,3,4,4,4,5,6,6,7,8,9,10,11,13,14,16,18,20,23,25],
}
# Table 8-15 QPC from qPI
QPC_T = list(range(30)) + [29,30,31,32,32,33,34,34,35,35,36,36,37,37,37,38,38,38,39,39,39,39]
# normAdjust4x4 v matrix (8-315), rows m=0..5, cols: (0,0)->0, (1,1)->1, else->2
V_NORM = [[10,16,13],[11,18,14],[13,20,16],[14,23,18],[16,25,20],[18,29,23]]
def level_scale_4x4(m, i, j):
    v = V_NORM[m]
    if (i & 1) == 0 and (j & 1) == 0: return v[0]
    if (i & 1) == 1 and (j & 1) == 1: return v[1]
    return v[2]

MB_TYPE_I = {0:'I_4x4', 25:'I_PCM'}
for _n in range(1, 25):
    MB_TYPE_I[_n] = 'I_16x16'
MB_TYPE_P = {0:'P_L0_16x16', 1:'P_L0_16x8', 2:'P_L0_8x16', 3:'P_8x8', 4:'P_8x8ref0', 30:'P_Skip'}
SUB_MB_TYPE_P = {0:'P_L0_8x8', 1:'P_L0_8x4', 2:'P_L0_4x8', 3:'P_L0_4x4'}
# (w,h) of sub-mb partitions
SUB_PARTS = {0:[(0,0,8,8)], 1:[(0,0,8,4),(0,4,8,4)], 2:[(0,0,4,8),(4,0,4,8)],
             3:[(0,0,4,4),(4,0,4,4),(0,4,4,4),(4,4,4,4)]}
# mb partition layout for P mb_types: list of (x,y,w,h) in MB
MB_PARTS = {0:[(0,0,16,16)], 1:[(0,0,16,8),(0,8,16,8)], 2:[(0,0,8,16),(8,0,8,16)],
            3:[(0,0,8,8),(8,0,8,8),(0,8,8,8),(8,8,8,8)],
            4:[(0,0,8,8),(8,0,8,8),(0,8,8,8),(8,8,8,8)]}

# ---------------- bit reader ----------------
class BitReader:
    def __init__(self, data):
        self.d = data
        self.pos = 0  # bit position
        self.nbits = len(data) * 8
    def left(self):
        return self.nbits - self.pos
    def u(self, n):
        v = 0
        for _ in range(n):
            if self.pos >= self.nbits:
                raise ValueError('bitstream overread at bit %d' % self.pos)
            byte = self.d[self.pos >> 3]
            v = (v << 1) | ((byte >> (7 - (self.pos & 7))) & 1)
            self.pos += 1
        return v
    def ue(self):
        n = 0
        while True:
            b = self.u(1)
            if b: break
            n += 1
            if n > 32: raise ValueError('ue overflow')
        return (1 << n) - 1 + (self.u(n) if n else 0)
    def se(self):
        v = self.ue()
        return (v + 1) // 2 if (v & 1) else -(v // 2)
    def vlc(self, table):
        # table: {(length, bitstring): value}; incremental match
        bits = ''
        for ln in range(1, 33):
            bits += '1' if self.u(1) else '0'
            key = (ln, bits)
            if key in table:
                return table[key]
        raise ValueError('VLC decode failure after 32 bits at bit %d' % (self.pos - 32))

def rbsp_unescape(nal):
    out = bytearray()
    i = 0
    n = len(nal)
    while i < n:
        if i + 2 < n and nal[i] == 0 and nal[i+1] == 0 and nal[i+2] == 3:
            out += b'\x00\x00'
            i += 3
        else:
            out.append(nal[i])
            i += 1
    return bytes(out)
# ---------------- parameter sets ----------------
class SPS:
    pass
class PPS:
    pass

def parse_hrd(br):
    cpb_cnt_minus1 = br.ue()
    br.u(4); br.u(4)
    for _ in range(cpb_cnt_minus1 + 1):
        br.ue(); br.ue(); br.u(1)
    br.u(5); br.u(5); br.u(5); br.u(5)

def parse_vui(br):
    if br.u(1):  # aspect_ratio_info_present_flag
        if br.u(8) == 255:
            br.u(16); br.u(16)
    if br.u(1): br.u(1)  # overscan
    if br.u(1):  # video_signal_type
        br.u(3); br.u(1)
        if br.u(1): br.u(8); br.u(8); br.u(8)
    if br.u(1): br.ue(); br.ue()  # chroma loc
    if br.u(1):  # timing
        br.u(32); br.u(32); br.u(1)
    nal_hrd = br.u(1); vcl_hrd = br.u(1)
    if nal_hrd: parse_hrd(br)
    if vcl_hrd: parse_hrd(br)
    if nal_hrd or vcl_hrd: br.u(1)
    br.u(1)  # pic_struct_present_flag
    if br.u(1):  # bitstream_restriction_flag
        br.u(1); br.ue(); br.ue(); br.ue(); br.ue(); br.ue(); br.ue()

def parse_sps(nal):
    br = BitReader(rbsp_unescape(nal[1:]))
    s = SPS()
    s.profile_idc = br.u(8)
    br.u(8)  # constraint flags
    s.level_idc = br.u(8)
    s.sps_id = br.ue()
    if s.profile_idc in (100,110,122,244,44,83,86,118,128,138,144):
        raise ValueError('high profile SPS not supported')
    s.log2_max_frame_num_minus4 = br.ue()
    s.pic_order_cnt_type = br.ue()
    if s.pic_order_cnt_type == 0:
        s.log2_max_pic_order_cnt_lsb_minus4 = br.ue()
    elif s.pic_order_cnt_type == 1:
        br.u(1); br.se(); br.se(); n = br.ue()
        for _ in range(n): br.se()
    s.max_num_ref_frames = br.ue()
    br.u(1)  # gaps_in_frame_num_value_allowed_flag
    s.pic_width_in_mbs_minus1 = br.ue()
    s.pic_height_in_map_units_minus1 = br.ue()
    s.frame_mbs_only_flag = br.u(1)
    if not s.frame_mbs_only_flag: br.u(1)
    s.direct_8x8_inference_flag = br.u(1)
    s.frame_cropping_flag = br.u(1)
    if s.frame_cropping_flag:
        for _ in range(4): br.ue()
    if br.u(1): parse_vui(br)
    return s

def parse_pps(nal):
    br = BitReader(rbsp_unescape(nal[1:]))
    p = PPS()
    p.pps_id = br.ue()
    p.sps_id = br.ue()
    p.entropy_coding_mode_flag = br.u(1)
    p.pic_order_cnt_present_flag = br.u(1)
    p.num_slice_groups_minus1 = br.ue()
    if p.num_slice_groups_minus1 != 0:
        raise ValueError('slice groups not supported')
    p.num_ref_idx_l0_active_minus1 = br.ue()
    p.num_ref_idx_l1_active_minus1 = br.ue()
    p.weighted_pred_flag = br.u(1)
    p.weighted_bipred_idc = br.u(2)
    p.pic_init_qp_minus26 = br.se()
    p.pic_init_qs_minus26 = br.se()
    p.chroma_qp_index_offset = br.se()
    p.deblocking_filter_control_present_flag = br.u(1)
    p.constrained_intra_pred_flag = br.u(1)
    p.redundant_pic_cnt_present_flag = br.u(1)
    return p

class SliceHeader:
    pass

def parse_slice_header(br, nal_type, sps, pps):
    h = SliceHeader()
    h.nal_type = nal_type
    h.idr = (nal_type == 5)
    h.first_mb_in_slice = br.ue()
    h.slice_type = br.ue()
    h.pps_id = br.ue()
    h.frame_num = br.u(sps.log2_max_frame_num_minus4 + 4)
    if not sps.frame_mbs_only_flag:
        raise ValueError('field coding not supported')
    if h.idr:
        h.idr_pic_id = br.ue()
    else:
        h.idr_pic_id = -1
    if sps.pic_order_cnt_type == 0:
        br.u(sps.log2_max_pic_order_cnt_lsb_minus4 + 4)
    # redundant_pic_cnt_present_flag == 0 in fixture
    h.is_p = (h.slice_type % 5 == 0)
    h.is_i = (h.slice_type % 5 == 2)
    if h.idr:
        h.no_output_of_prior_pics_flag = br.u(1)
        h.long_term_reference_flag = br.u(1)
    elif h.is_p:
        h.num_ref_idx_active_override_flag = br.u(1)
        if h.num_ref_idx_active_override_flag:
            h.num_ref_idx_l0_active_minus1 = br.ue()
        else:
            h.num_ref_idx_l0_active_minus1 = pps.num_ref_idx_l0_active_minus1
        # ref_pic_list_reordering
        if br.u(1):  # ref_pic_list_reordering_flag_l0
            while True:
                idc = br.ue()
                if idc == 3: break
                br.ue()  # abs_diff_pic_num_minus1 / long_term_pic_num
        # weighted_pred_flag == 0 -> no pred_weight_table
        if pps.redundant_pic_cnt_present_flag: raise ValueError('no')
        # dec_ref_pic_marking (nal_ref_idc != 0)
        if br.u(1):  # adaptive_ref_pic_marking_mode_flag
            while True:
                op = br.ue()
                if op == 0: break
                br.ue()
                if op in (1, 3): br.ue()
                if op == 2: br.ue()
    h.slice_qp_delta = br.se()
    h.SliceQPY = 26 + pps.pic_init_qp_minus26 + h.slice_qp_delta
    if pps.deblocking_filter_control_present_flag:
        h.disable_deblocking_filter_idc = br.ue()
        if h.disable_deblocking_filter_idc != 1:
            h.slice_alpha_c0_offset_div2 = br.se()
            h.slice_beta_offset_div2 = br.se()
        else:
            h.slice_alpha_c0_offset_div2 = 0
            h.slice_beta_offset_div2 = 0
    else:
        h.disable_deblocking_filter_idc = 0
        h.slice_alpha_c0_offset_div2 = 0
        h.slice_beta_offset_div2 = 0
    return h
# ---------------- CAVLC ----------------
COEFF_TABLES = [None, None, None, None]  # filled below by nC range
def coeff_table_for_nc(nc):
    if nc == -1: return COEFF_TOKEN_NCM1
    if nc < 2: return COEFF_TOKEN_NC0
    if nc < 4: return COEFF_TOKEN_NC1
    if nc < 8: return COEFF_TOKEN_NC2
    return COEFF_TOKEN_NC3

TZ_TABLES_4X4 = {1:TOTAL_ZEROS_TZ1, 2:TOTAL_ZEROS_TZ2, 3:TOTAL_ZEROS_TZ3,
    4:TOTAL_ZEROS_TZ4, 5:TOTAL_ZEROS_TZ5, 6:TOTAL_ZEROS_TZ6, 7:TOTAL_ZEROS_TZ7,
    8:TOTAL_ZEROS_TZ8, 9:TOTAL_ZEROS_TZ9, 10:TOTAL_ZEROS_TZ10, 11:TOTAL_ZEROS_TZ11,
    12:TOTAL_ZEROS_TZ12, 13:TOTAL_ZEROS_TZ13, 14:TOTAL_ZEROS_TZ14, 15:TOTAL_ZEROS_TZ15}
TZ_TABLES_CHDC = {1:TOTAL_ZEROS_CHDC_TZ1, 2:TOTAL_ZEROS_CHDC_TZ2, 3:TOTAL_ZEROS_CHDC_TZ3}
RB_TABLES = {1:RUN_BEFORE_ZL1, 2:RUN_BEFORE_ZL2, 3:RUN_BEFORE_ZL3, 4:RUN_BEFORE_ZL4,
             5:RUN_BEFORE_ZL5, 6:RUN_BEFORE_ZL6, 7:RUN_BEFORE_ZL7}

def cavlc_block(br, nC, maxNumCoeff):
    """Decode one residual block. Returns dict(tc,t1,tz,levels,runs,coeff)
    levels/runs in decode order (index 0 = first decoded = highest scan pos);
    coeff = list length maxNumCoeff in scan order (index 0 = DC)."""
    tc, t1 = br.vlc(coeff_table_for_nc(nC))
    levels = []
    for _ in range(t1):
        levels.append(1 if br.u(1) == 0 else -1)
    suffixLength = 1 if (tc > 10 and t1 < 3) else 0
    for i in range(t1, tc):
        lp = 0
        while br.u(1) == 0:
            lp += 1
            if lp > 30: raise ValueError('level_prefix runaway')
        if lp == 14 and suffixLength == 0: lss = 4
        elif lp >= 15: lss = lp - 3
        else: lss = suffixLength
        ls = br.u(lss) if lss > 0 else 0
        levelCode = ((15 if lp > 15 else lp) << suffixLength) + ls
        if lp >= 15 and suffixLength == 0: levelCode += 15
        if lp >= 16: levelCode += (1 << (lp - 3)) - 4096
        if i == t1 and t1 < 3: levelCode += 2
        if levelCode & 1: lv = (-levelCode - 1) >> 1
        else: lv = (levelCode + 2) >> 1
        levels.append(lv)
        if suffixLength == 0: suffixLength = 1
        if abs(lv) > (3 << (suffixLength - 1)) and suffixLength < 6:
            suffixLength += 1
    if tc == 0 or tc == maxNumCoeff:
        tz = 0
    else:
        tztab = (TZ_TABLES_CHDC if maxNumCoeff == 4 else TZ_TABLES_4X4)[tc]
        tz = br.vlc(tztab)
    runs = []
    zerosLeft = tz
    for _ in range(tc - 1):
        if zerosLeft > 0:
            r = br.vlc(RB_TABLES[7 if zerosLeft > 6 else zerosLeft])
        else:
            r = 0
        runs.append(r)
        zerosLeft -= r
        if zerosLeft < 0: raise ValueError('run_before exceeds zerosLeft')
    if tc > 0:
        runs.append(zerosLeft)
    coeff = [0] * maxNumCoeff
    cn = -1
    for i in range(tc - 1, -1, -1):
        cn += runs[i] + 1
        if cn >= maxNumCoeff: raise ValueError('coeffNum overflow')
        coeff[cn] = levels[i]
    return {'tc':tc, 't1':t1, 'tz':tz, 'levels':levels, 'runs':runs, 'coeff':coeff}
# ---------------- macroblock layer ----------------
class MBInfo:
    pass

def more_rbsp_data(br):
    # True iff remaining bits are more than just rbsp trailing bits
    pos = br.pos
    n = br.nbits
    # find first '1' at or after pos
    p = pos
    while p < n:
        byte = br.d[p >> 3]
        if (byte >> (7 - (p & 7))) & 1:
            break
        p += 1
    # remaining = bits [pos, p) are zeros then a 1 at p (or p == n)
    # rbsp trailing = single 1 followed by zeros to byte end
    if p >= n:
        return False
    # check bits after p are all zero
    q = p + 1
    while q < n:
        byte = br.d[q >> 3]
        if (byte >> (7 - (q & 7))) & 1:
            return True
        q += 1
    return False

# neighbor 4x4-block derivation (§6.4.11.4 equivalent on frame grid)
# H.264 luma4x4BlkIdx uses 8x8-grouped order (NOT raster):
#   0  1 | 4  5
#   2  3 | 6  7
#  ------+------
#   8  9 |12 13
#  10 11 |14 15
def _l4_xy(idx):
    return ((idx % 2) + 2 * ((idx // 4) % 2),
            ((idx // 2) % 2) + 2 * (idx // 8))

def _l4_idx(x, y):
    return 4 * ((y // 2) * 2 + (x // 2)) + (y % 2) * 2 + (x % 2)

def neigh_block_4x4(mbAddr, blkIdx, mbW, nMB, mbs, side):
    # side: 'A' left, 'B' above; returns (mbAddrN, luma4x4BlkIdxN) or (None, None)
    x, y = _l4_xy(blkIdx)
    if side == 'A':
        if x > 0: return mbAddr, _l4_idx(x - 1, y)
        na = mbAddr - 1
        if mbAddr % mbW == 0: return None, None
        return na, _l4_idx(3, y)
    else:
        if y > 0: return mbAddr, _l4_idx(x, y - 1)
        na = mbAddr - mbW
        if na < 0: return None, None
        return na, _l4_idx(x, 3)

def parse_mb_layer(br, h, sps, pps, mbAddr, mbs, dump):
    d = []  # per-MB detail lines; 'mb' line emitted first
    mbW = sps.pic_width_in_mbs_minus1 + 1
    nMB = mbW * (sps.pic_height_in_map_units_minus1 + 1)
    mb = MBInfo()
    mb.addr = mbAddr
    mb.skip = False
    mb.i4modes = [-1] * 16
    mb.i16mode = -1
    mb.chroma_mode = -1
    mb.mvs = []
    mb.res = []
    mb.tcL = [0] * 16
    mb.tcC = [[0] * 4, [0] * 4]
    mb.mvgrid = [None] * 16
    mb.intra = False
    mb.is_i16 = False
    mb.pcm = None

    t = br.ue()
    if h.is_p and t <= 4:
        name = MB_TYPE_P[t]
    else:
        ti = t - 5 if h.is_p else t
        if ti < 0 or ti > 25:
            raise ValueError('bad mb_type %d in %s slice' % (t, 'P' if h.is_p else 'I'))
        name = MB_TYPE_I[ti]
    mb.name = name
    mb.mb_type_val = t

    if name in ('P_L0_16x16', 'P_L0_16x8', 'P_L0_8x16', 'P_8x8', 'P_8x8ref0'):
        mb.intra = False
        # partitions
        parts = []  # (mbPartIdx, subIdx, x4, y4, w4, h4)
        if name in ('P_8x8', 'P_8x8ref0'):
            sub_types = []
            for k in range(4):
                st = br.ue()
                if st not in SUB_MB_TYPE_P:
                    raise ValueError('bad sub_mb_type %d' % st)
                sub_types.append(st)
            for k in range(4):
                bx = (k % 2) * 2; by = (k // 2) * 2
                for s, (sx, sy, sw, sh) in enumerate(SUB_PARTS[sub_types[k]]):
                    parts.append((k, s, bx + sx // 4, by + sy // 4, sw // 4, sh // 4))
        else:
            tmap = {'P_L0_16x16': 0, 'P_L0_16x8': 1, 'P_L0_8x16': 2}[name]
            for k, (px, py, pw, ph) in enumerate(MB_PARTS[tmap]):
                parts.append((k, -1, px // 4, py // 4, pw // 4, ph // 4))
        nRef = h.num_ref_idx_l0_active_minus1 + 1
        # ref idx
        for (k, s, x4, y4, w4, h4) in parts:
            if s <= 0:  # once per mbPartIdx
                if nRef > 1 and name != 'P_8x8ref0':
                    br.ue()  # ref_idx_l0 (always 0 in fixture)
        # mvd + mv reconstruction
        for (k, s, x4, y4, w4, h4) in parts:
            dx = br.se(); dy = br.se()
            px, py = mv_predict(mbAddr, mbs, mb, x4, y4, w4, h4, mbW, nMB)
            mx = px + dx; my = py + dy
            mb.mvs.append({'part': k, 'sub': s, 'dx': dx, 'dy': dy,
                           'mx': mx, 'my': my})
            d.append('mv part=%d sub=%d dx=%d dy=%d mx=%d my=%d'
                     % (k, s, dx, dy, mx, my))
            for yy in range(y4, y4 + h4):
                for xx in range(x4, x4 + w4):
                    mb.mvgrid[yy * 4 + xx] = (mx, my)
        # coded block pattern
        cbp = CBP_INTER[br.ue()]
        mb.cbp = cbp
        mb.qp_delta = br.se() if (cbp & 15) or (cbp >> 4) else 0
        mb.qp_delta_present = bool((cbp & 15) or (cbp >> 4))
    elif name == 'I_4x4':
        mb.intra = True
        for b in range(16):
            na, ba = neigh_block_4x4(mbAddr, b, mbW, nMB, mbs, 'A')
            nb, bb = neigh_block_4x4(mbAddr, b, mbW, nMB, mbs, 'B')
            dcFlag = False
            modes = []
            for (nx, bx) in ((na, ba), (nb, bb)):
                if nx is None:
                    dcFlag = True; modes.append(2)
                elif nx == mbAddr:
                    # same MB: use already-decoded modes from current MB
                    modes.append(mb.i4modes[bx])
                elif nx >= len(mbs) or mbs[nx] is None:
                    dcFlag = True; modes.append(2)
                elif mbs[nx].name != 'I_4x4':
                    modes.append(2)
                else:
                    modes.append(mbs[nx].i4modes[bx])
            pred = min(modes)
            if br.u(1):
                mode = pred
            else:
                rem = br.u(3)
                mode = rem + (1 if rem >= pred else 0)
            mb.i4modes[b] = mode
            d.append('i4 b=%d m=%d' % (b, mode))
        mb.chroma_mode = br.ue()
        d.append('ichroma m=%d' % mb.chroma_mode)
        cbp = CBP_INTRA[br.ue()]
        mb.cbp = cbp
        mb.qp_delta = br.se() if (cbp & 15) or (cbp >> 4) else 0
        mb.qp_delta_present = bool((cbp & 15) or (cbp >> 4))
    elif name == 'I_16x16':
        mb.intra = True
        mb.is_i16 = True
        ti = (t - 5 if h.is_p else t) - 1
        mb.i16mode = ti & 3
        q = ti >> 2
        cbpC = q % 3; cbpY = 15 if q >= 3 else 0
        mb.cbp = cbpY | (cbpC << 4)
        d.append('i16 m=%d' % mb.i16mode)
        mb.chroma_mode = br.ue()
        d.append('ichroma m=%d' % mb.chroma_mode)
        mb.qp_delta = br.se()
        mb.qp_delta_present = True
    elif name == 'I_PCM':
        mb.intra = True
        while br.pos & 7:
            br.u(1)
        raw = bytes(br.u(8) for _ in range(256 + 128))
        mb.pcm = raw
        mb.cbp = 47
        mb.qp_delta = 0
        mb.qp_delta_present = False
    else:
        raise ValueError('unhandled mb name %s' % name)

    if mb.qp_delta_present:
        qp_prev = mbs_qp_prev(mbs, h)
        mb.qp = ((qp_prev + mb.qp_delta + 52 + 52) % 52)
    else:
        mb.qp = mbs_qp_prev(mbs, h)
    # residual
    parse_residual(br, h, mb, mbs, mbAddr, mbW, nMB, d)
    if dump is not None:
        dump.append('mb a=%d type=%s cbp=%d qp=%d' % (mbAddr, mb.name, mb.cbp, mb.qp))
        dump.extend(d)
    return mb

def mbs_qp_prev(mbs, h):
    for mb in reversed(mbs):
        if mb is not None:
            return mb.qp
    return h.SliceQPY

def skip_mb(h, mbAddr, mbs, mbW, nMB):
    mb = MBInfo()
    mb.addr = mbAddr
    mb.skip = True
    mb.name = 'P_Skip'
    mb.cbp = 0
    mb.qp = mbs_qp_prev(mbs, h)
    mb.i4modes = [-1] * 16
    mb.i16mode = -1
    mb.chroma_mode = -1
    mb.mvs = []
    mb.res = []
    mb.tcL = [0] * 16
    mb.tcC = [[0] * 4, [0] * 4]
    mb.intra = False
    mb.is_i16 = False
    mb.pcm = None
    mb.qp_delta = 0
    mb.qp_delta_present = False
    # P_Skip: mv = predictor for 16x16 partition
    px, py = mv_predict(mbAddr, mbs, mb, 0, 0, 4, 4, mbW, nMB)
    mb.mvgrid = [(px, py)] * 16
    return mb

def mv_predict(mbAddr, mbs, curmb, x4, y4, w4, h4, mbW, nMB):
    # neighbor partitions via 4x4 luma block grid (frame coding)
    mbx = mbAddr % mbW; mby = mbAddr // mbW
    mbH = nMB // mbW
    pts = {'A': (mbx * 4 + x4 - 1, mby * 4 + y4),
           'B': (mbx * 4 + x4, mby * 4 + y4 - 1),
           'C': (mbx * 4 + x4 + w4, mby * 4 + y4 - 1),
           'D': (mbx * 4 + x4 - 1, mby * 4 + y4 - 1)}
    vals = {}
    for k, (ax, ay) in pts.items():
        v = None
        if 0 <= ax < mbW * 4 and 0 <= ay < mbH * 4:
            nAddr = (ay // 4) * mbW + (ax // 4)
            if nAddr < len(mbs) and mbs[nAddr] is not None:
                blk = (ay % 4) * 4 + (ax % 4)
                v = mbs[nAddr].mvgrid[blk]  # None if intra / not yet decoded
        vals[k] = v
    if vals['C'] is None:
        vals['C'] = vals['D']
    av = [vals[k] for k in ('A', 'B', 'C') if vals[k] is not None]
    if not av:
        return (0, 0)
    xs = sorted(v[0] for v in av); ys = sorted(v[1] for v in av)
    return (xs[1], ys[1])

def _side_n(nx, bx, mbs, mbAddr, cur_tc_arr, is_luma, comp):
    # (available, n) for one neighboring 4x4 block per H.264 9.2.1 steps 5-6.
    # n = 0 if neighbor MB is skip or its CBP bit says no coeffs here;
    # n = 16 for I_PCM; else the neighbor block's TotalCoeff (AC count).
    if nx is None:
        return (False, 0)
    if nx == mbAddr:
        return (True, cur_tc_arr[bx])
    if nx >= len(mbs) or mbs[nx] is None:
        return (False, 0)
    nmb = mbs[nx]
    mt = nmb.name
    if mt == 'P_Skip':
        return (True, 0)
    if mt == 'I_PCM':
        return (True, 16)
    if is_luma:
        if not ((nmb.cbp & 15) & (1 << (bx >> 2))):
            return (True, 0)
        return (True, nmb.tcL[bx])
    else:
        if (nmb.cbp >> 4) != 2:
            return (True, 0)
        return (True, nmb.tcC[comp][bx])

def _combine_nC(aA, nA, aB, nB):
    # 9.2.1 step 7: both -> rounded avg; one -> that one; neither -> 0.
    # (The -1/-2 values are ONLY for ChromaDCLevel, handled at call site.)
    if aA and aB:
        return (nA + nB + 1) >> 1
    if aA:
        return nA
    if aB:
        return nB
    return 0

def nc_luma(mbAddr, b, mbs, mbW, cur_tcL):
    # normative nC for luma 4x4 block b (also used for Intra16x16DCLevel, b=0)
    na, ba = neigh_block_4x4(mbAddr, b, mbW, None, mbs, 'A')
    nb, bb = neigh_block_4x4(mbAddr, b, mbW, None, mbs, 'B')
    aA, nA = _side_n(na, ba, mbs, mbAddr, cur_tcL, True, 0)
    aB, nB = _side_n(nb, bb, mbs, mbAddr, cur_tcL, True, 0)
    return _combine_nC(aA, nA, aB, nB)

def nc_chroma(mbAddr, b, comp, mbs, mbW, cur_tcC):
    # normative nC for chroma 4x4 block b (2x2 grid), component comp
    bx = b % 2; by = b // 2
    if bx > 0:
        aA, nA = True, cur_tcC[b - 1]
    else:
        if mbAddr % mbW == 0:
            aA, nA = False, 0
        else:
            aA, nA = _side_n(mbAddr - 1, b + 1, mbs, mbAddr, cur_tcC, False, comp)
    if by > 0:
        aB, nB = True, cur_tcC[b - 2]
    else:
        na = mbAddr - mbW
        if na < 0:
            aB, nB = False, 0
        else:
            aB, nB = _side_n(na, b + 2, mbs, mbAddr, cur_tcC, False, comp)
    return _combine_nC(aA, nA, aB, nB)

def parse_residual(br, h, mb, mbs, mbAddr, mbW, nMB, d):
    cbpY = mb.cbp & 15; cbpC = mb.cbp >> 4
    is_i16 = mb.is_i16
    if mb.skip or mb.pcm is not None:
        return
    if is_i16:
        # Intra16x16DCLevel: nC derived with luma4x4BlkIdx = 0 (9.2.1 steps 1-7)
        r = cavlc_block(br, nc_luma(mbAddr, 0, mbs, mbW, mb.tcL), 16)
        mb.res.append({'comp': 'y', 'b': 16, **r})
        dump_res(d, 'y', 16, r)
    if (not is_i16) or cbpY:
        for b in range(16):
            # CodedBlockPatternLuma bit (b>>2): one bit per 8x8 group
            if cbpY & (1 << (b >> 2)):
                if is_i16:
                    r = cavlc_block(br, nc_luma(mbAddr, b, mbs, mbW, mb.tcL), 15)
                else:
                    r = cavlc_block(br, nc_luma(mbAddr, b, mbs, mbW, mb.tcL), 16)
                mb.tcL[b] = r['tc']
                mb.res.append({'comp': 'y', 'b': b, **r})
                dump_res(d, 'y', b, r)
    if cbpC:
        for comp, cn in (('cb', 0), ('cr', 1)):
            r = cavlc_block(br, -1, 4)
            mb.res.append({'comp': comp, 'b': 4, **r})
            dump_res(d, comp, 4, r)
        # chroma AC (maxNumCoeff = 15: DC is separate)
        if cbpC == 2:
            for comp, cn in (('cb', 0), ('cr', 1)):
                for b in range(4):
                    r = cavlc_block(br, nc_chroma(mbAddr, b, cn, mbs, mbW, mb.tcC[cn]), 15)
                    mb.tcC[cn][b] = r['tc']
                    mb.res.append({'comp': comp, 'b': b, **r})
                    dump_res(d, comp, b, r)

def dump_res(dump, comp, b, r):
    lv = ','.join(str(x) for x in r['levels'])
    rb = ','.join(str(x) for x in r['runs'])
    dump.append('res comp=%s b=%d tc=%d t1=%d tz=%d lv=%s rb=%s'
                % (comp, b, r['tc'], r['t1'], r['tz'], lv, rb))

def parse_slice(br, h, sps, pps, dump):
    mbW = sps.pic_width_in_mbs_minus1 + 1
    mbH = sps.pic_height_in_map_units_minus1 + 1
    nMB = mbW * mbH
    mbs = [None] * nMB
    addr = h.first_mb_in_slice
    skip_run = 0
    if h.is_p:
        skip_run = br.ue()
        if dump is not None: dump.append('skip run=%d' % skip_run)
    while addr < nMB:
        if h.is_p and skip_run > 0:
            mb = skip_mb(h, addr, mbs, mbW, nMB)
            skip_run -= 1
            if dump is not None:
                dump.append('mb a=%d type=P_Skip cbp=0 qp=%d' % (addr, mb.qp))
        else:
            mb = parse_mb_layer(br, h, sps, pps, addr, mbs, dump)
        mbs[addr] = mb
        addr += 1
        if h.is_p and addr < nMB and more_rbsp_data(br):
            skip_run = br.ue()
            if dump is not None: dump.append('skip run=%d' % skip_run)
    return mbs
# ---------------- driver ----------------
def load_stream(path):
    data = open(path, 'rb').read()
    n = struct.unpack('>I', data[:4])[0]
    off = 4
    nals = []
    for _ in range(n):
        ln = struct.unpack('>I', data[off:off + 4])[0]
        off += 4
        nals.append(data[off:off + ln])
        off += ln
    return nals

def decode_stream(nals, dump):
    sps = None; pps = None
    frames = []  # list of dicts: kind, mbs, h, sps, pps, nal_idx
    if dump is not None: dump.append('stream nals=%d' % len(nals))
    for i, nal in enumerate(nals):
        t = nal[0] & 31
        if dump is not None: dump.append('nal idx=%d type=%d len=%d' % (i, t, len(nal)))
        if t == 7:
            sps = parse_sps(nal)
            if dump is not None: dump.append('sps id=%d profile=%d level=%d w=%d h=%d'
                                 % (sps.sps_id, sps.profile_idc, sps.level_idc,
                                    (sps.pic_width_in_mbs_minus1 + 1) * 16,
                                    (sps.pic_height_in_map_units_minus1 + 1) * 16))
        elif t == 8:
            pps = parse_pps(nal)
            if dump is not None: dump.append('pps id=%d sps=%d' % (pps.pps_id, pps.sps_id))
        elif t in (1, 5):
            br = BitReader(rbsp_unescape(nal[1:]))
            h = parse_slice_header(br, t, sps, pps)
            if dump is not None: dump.append(
                'slice nal=%d idr=%d type=%s frame_num=%d idr_pic_id=%d qp=%d '
                'deblock=%d alpha_off=%d beta_off=%d'
                % (i, 1 if h.idr else 0, 'P' if h.is_p else 'I', h.frame_num,
                   h.idr_pic_id, h.SliceQPY, h.disable_deblocking_filter_idc,
                   h.slice_alpha_c0_offset_div2, h.slice_beta_offset_div2))
            mbs = parse_slice(br, h, sps, pps, dump)
            frames.append({'nal': i, 'h': h, 'mbs': mbs, 'sps': sps, 'pps': pps})
        elif t == 6:
            pass  # SEI ignored
        else:
            raise ValueError('unexpected NAL type %d' % t)
    return frames

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'parse'
    path = sys.argv[2] if len(sys.argv) > 2 else 'stream.in'
    nals = load_stream(path)
    dump = [] if mode == 'parse' else None
    frames = decode_stream(nals, dump)
    if mode == 'parse':
        sys.stdout.write('\n'.join(dump) + '\n')
    elif mode == 'recon':
        for f in frames:
            pic = reconstruct(f)
            sys.stdout.write('frame nal=%d sha=%s\n'
                             % (f['nal'], hashlib.sha256(pic_to_bytes(pic)).hexdigest()))
    elif mode == 'final':
        for f in frames:
            pic = reconstruct(f)
            deblock(pic, f)
            sys.stdout.write('frame nal=%d sha=%s\n'
                             % (f['nal'], hashlib.sha256(pic_to_bytes(pic)).hexdigest()))

if __name__ == '__main__':
    main()
