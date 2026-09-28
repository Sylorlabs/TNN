# CREW C — SEALED HELD-OUT TARGET LIST

Frozen before the control path's target handling was built.
Dev targets are disjoint (descriptor-string level, verified).
No RNG in generation (closed-form sequences + fixed tables).

## Pitch (40, [80,1200] Hz, hit: |F0-t|/t <= 2%, bar >= 28/40)

- P00 `pitch:80`
- P01 `pitch:86`
- P02 `pitch:92`
- P03 `pitch:99`
- P04 `pitch:106`
- P05 `pitch:113`
- P06 `pitch:121`
- P07 `pitch:130`
- P08 `pitch:139`
- P09 `pitch:149`
- P10 `pitch:160`
- P11 `pitch:172`
- P12 `pitch:184`
- P13 `pitch:197`
- P14 `pitch:211`
- P15 `pitch:227`
- P16 `pitch:243`
- P17 `pitch:260`
- P18 `pitch:279`
- P19 `pitch:299`
- P20 `pitch:321`
- P21 `pitch:344`
- P22 `pitch:369`
- P23 `pitch:395`
- P24 `pitch:423`
- P25 `pitch:454`
- P26 `pitch:487`
- P27 `pitch:522`
- P28 `pitch:559`
- P29 `pitch:599`
- P30 `pitch:642`
- P31 `pitch:689`
- P32 `pitch:738`
- P33 `pitch:791`
- P34 `pitch:848`
- P35 `pitch:909`
- P36 `pitch:974`
- P37 `pitch:1044`
- P38 `pitch:1120`
- P39 `pitch:1200`

## Envelope (20: 7 flat / 7 rise / 6 decay, bar >= 14/20)

- E00 `env:flat`
- E01 `env:rise`
- E02 `env:decay`
- E03 `env:flat`
- E04 `env:rise`
- E05 `env:decay`
- E06 `env:flat`
- E07 `env:rise`
- E08 `env:decay`
- E09 `env:flat`
- E10 `env:rise`
- E11 `env:decay`
- E12 `env:flat`
- E13 `env:rise`
- E14 `env:decay`
- E15 `env:flat`
- E16 `env:rise`
- E17 `env:decay`
- E18 `env:flat`
- E19 `env:rise`

## Rhythm (20: 10 even / 10 swing21, bar >= 14/20)

- R00 `rhy:even`
- R01 `rhy:swing21`
- R02 `rhy:even`
- R03 `rhy:swing21`
- R04 `rhy:even`
- R05 `rhy:swing21`
- R06 `rhy:even`
- R07 `rhy:swing21`
- R08 `rhy:even`
- R09 `rhy:swing21`
- R10 `rhy:even`
- R11 `rhy:swing21`
- R12 `rhy:even`
- R13 `rhy:swing21`
- R14 `rhy:even`
- R15 `rhy:swing21`
- R16 `rhy:even`
- R17 `rhy:swing21`
- R18 `rhy:even`
- R19 `rhy:swing21`

## Prosody C-R2 (20, CV% in [0.3,25], diagnostic, bar >= 14/20)

- S00 `prosody:0.3`
- S01 `prosody:0.38`
- S02 `prosody:0.48`
- S03 `prosody:0.6`
- S04 `prosody:0.76`
- S05 `prosody:0.96`
- S06 `prosody:1.21`
- S07 `prosody:1.53`
- S08 `prosody:1.93`
- S09 `prosody:2.44`
- S10 `prosody:3.08`
- S11 `prosody:3.88`
- S12 `prosody:4.9`
- S13 `prosody:6.19`
- S14 `prosody:7.81`
- S15 `prosody:9.85`
- S16 `prosody:12.44`
- S17 `prosody:15.69`
- S18 `prosody:19.81`
- S19 `prosody:25.0`

## Compositionality C-R1 (10 pairs, diagnostic)

- X00 `pitch:880+env:decay`
- X01 `pitch:110+env:rise`
- X02 `pitch:660+env:decay`
- X03 `rhy:swing21+pitch:990`
- X04 `rhy:even+pitch:150`
- X05 `pitch:440+env:rise`
- X06 `rhy:swing21+env:decay`
- X07 `pitch:1200+env:rise`
- X08 `pitch:80+env:decay`
- X09 `rhy:even+env:rise`

## Arms

- C0 (null): descriptor replaced by frozen constant `pitch:220+env:flat+rhy:even`
- C1 (shuffle guard): frozen derangement — pitch cyclic shift by 17; env flat->rise, rise->decay, decay->flat; rhy even<->swing21. Zero fixed points verified.

## Dev targets (disjoint, pre-freeze use only)

- `pitch:95`
- `pitch:165`
- `pitch:275`
- `pitch:390`
- `pitch:520`
- `pitch:700`
- `pitch:950`
- `pitch:1100`
- `env:flat`
- `env:rise`
- `env:decay`
- `env:flat`
- `env:rise`
- `rhy:even`
- `rhy:swing15`
- `rhy:swing30`
- `prosody:1.0`
- `prosody:8.0`
- `pitch:330+env:rise`
- `rhy:swing30+pitch:520`
