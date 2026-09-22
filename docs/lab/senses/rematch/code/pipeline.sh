#!/bin/bash
cd ~/workspace/senses-rematch
log() { echo "[$(date -u +%FT%TZ)] $*"; }
log "PIPELINE START"
python3 resume_gen.py TRAIN_T3 20260922 50 2>&1
log "T3 gen done rc=$?"
python3 run_all.py data/TRAIN_T3 runs_TRAIN_T3.jsonl primary 2>&1
log "T3 runs done rc=$?"
python3 resume_gen.py TRAIN_T4 20260922 100 2>&1
log "T4 gen done rc=$?"
python3 run_all.py data/TRAIN_T4 runs_TRAIN_T4.jsonl primary 2>&1
log "T4 runs done rc=$?"
python3 resume_gen.py TEST_FRESH 20260923 1 2>&1
log "TEST_FRESH gen done rc=$?"
python3 run_all.py data/TEST_FRESH runs_TEST_FRESH.jsonl primary 2>&1
log "TEST_FRESH runs done rc=$?"
log "PIPELINE COMPLETE"
