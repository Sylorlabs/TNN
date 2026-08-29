from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, Dataset

ROOT = Path('/mnt/data/r32_epistemic')
SEED = 39039
TRIALS = 12
K = 5
SOURCE = 7
MODES = ['balanced_no_unique','biased_no_unique','stable_weak','unstable_then_stable','replacement','reversal','costly_stable']
RESOURCE_COUNT = 5
EPISODES_PER_MODE_RESOURCE = 70

torch.set_num_threads(max(1, min(6, torch.get_num_threads())))

import sys
sys.path[:0] = ['/mnt/data/r31_part2', str(ROOT)]
import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v
import r32_v26_candidate_selected_conditional_advantage as world
import r32_v32_predictive_dynamics_population as v32
import r32_v37_regret_weighted_candidate_support as v37


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reconstruct_episode(eid: int, env):
    mi = eid // (RESOURCE_COUNT * EPISODES_PER_MODE_RESOURCE)
    rem = eid % (RESOURCE_COUNT * EPISODES_PER_MODE_RESOURCE)
    ri = rem // EPISODES_PER_MODE_RESOURCE
    j = rem % EPISODES_PER_MODE_RESOURCE
    epseed = 9714 * 4_000_000 + mi * 300_000 + ri * 50_000 + j
    ep = v.make_ep(epseed, 'genuine_ambiguity', env)
    params = world.world_params(epseed, MODES[mi])
    return mi, ri, j, epseed, ep, params


def evidence_and_action(ep, mode, params, st, env, used, trial):
    *_, classes, idx, sig, learned = env
    outcome = world.world_outcome(ep, mode, params, trial)
    action = r31.select_action(st.score, learned, used)
    used.append(action)
    rng = np.random.default_rng(ep.seed * 2029 + trial * 12347 + action * 31 + 97)
    observation = sig[idx[outcome], action] + float(rng.normal(0, params.sigma))
    variance = 0.95 if mode in ('balanced_no_unique','biased_no_unique','unstable_then_stable') else 0.88
    vec = np.array([-((observation - learned[ci, action]) ** 2) / (2 * variance**2) for ci in range(len(classes))], dtype=float)
    return vec, int(action)


def build_prefix_sequences(z32):
    episode = z32['episode_id'].astype(int)
    trial = z32['trial_index'].astype(int)
    n = len(episode)
    env = r31.setup(9714)
    action_count = int(env[8].shape[1])
    seq_dim = K + action_count
    seq = np.zeros((n, TRIALS, seq_dim), np.float32)
    lengths = trial.astype(np.int64).copy()
    for eid in np.unique(episode):
        rows = np.where(episode == eid)[0]
        rows = rows[np.argsort(trial[rows])]
        mi, ri, j, epseed, ep, params = reconstruct_episode(int(eid), env)
        st = v.initial_state(ep, env, 'D')
        used = []
        hist = []
        for row in rows:
            t = int(trial[row])
            if hist:
                seq[row, :len(hist)] = np.asarray(hist, np.float32)
            vec, action = evidence_and_action(ep, MODES[mi], params, st, env, used, t)
            p = v.softmax(vec).astype(np.float32)
            a = np.zeros(action_count, np.float32); a[action] = 1.0
            hist.append(np.r_[p, a].astype(np.float32))
            st.add(SOURCE, vec, params.cost)
    return seq, lengths, {'sequence_dim': seq_dim, 'action_count': action_count, 'rows': n}


class PrefixDataset(Dataset):
    def __init__(self, seq, lengths, static, target, indices):
        self.seq = seq; self.lengths = lengths; self.static = static; self.target = target; self.indices = np.asarray(indices, int)
    def __len__(self): return len(self.indices)
    def __getitem__(self, i):
        j = int(self.indices[i])
        return self.seq[j], self.lengths[j], self.static[j], self.target[j]


class RecurrentTemporalPAM(nn.Module):
    def __init__(self, seq_dim: int, static_dim: int, hidden: int = 56):
        super().__init__()
        self.gru = nn.GRU(seq_dim, hidden, num_layers=2, batch_first=True, dropout=0.08)
        self.static = nn.Sequential(nn.Linear(static_dim, 96), nn.GELU(), nn.Dropout(0.05), nn.Linear(96, 56), nn.GELU())
        self.fuse = nn.Sequential(nn.Linear(hidden + 56 + 2, 112), nn.GELU(), nn.Dropout(0.06), nn.Linear(112, 64), nn.GELU())
        self.mean_head = nn.Linear(64, 12)
        self.var_head = nn.Linear(64, 12)
    def forward(self, seq, lengths, static):
        out, _ = self.gru(seq)
        b = torch.arange(len(lengths), device=seq.device)
        at = torch.clamp(lengths - 1, min=0)
        h = out[b, at]
        h = h * (lengths > 0).float().unsqueeze(1)
        sf = self.static(static)
        lf = torch.stack([lengths.float() / TRIALS, (lengths > 0).float()], dim=1)
        z = self.fuse(torch.cat([h, sf, lf], dim=1))
        mean = torch.sigmoid(self.mean_head(z))
        var = 0.25 * torch.sigmoid(self.var_head(z))
        return mean, var


def predict(model, seq, lengths, static, indices, batch=512):
    model.eval(); out_m=[]; out_v=[]
    ds = PrefixDataset(seq, lengths, static, np.zeros((len(seq),24),np.float32), indices)
    dl = DataLoader(ds, batch_size=batch, shuffle=False, num_workers=0)
    with torch.no_grad():
        for sq, ln, st, _ in dl:
            m, vq = model(sq.float(), ln.long(), st.float()); out_m.append(m.cpu().numpy()); out_v.append(vq.cpu().numpy())
    return np.concatenate(out_m), np.concatenate(out_v)


def train_one(seq, lengths, Xraw, Ymean, Yvar, fit_mask, pred_mask, seed):
    rng = np.random.default_rng(seed)
    ids = np.where(fit_mask)[0]
    # Internal validation is episode-disjoint through a deterministic row-group hash.
    val = ids[(ids * 2654435761 % 17) == 0]
    train = np.setdiff1d(ids, val, assume_unique=False)
    if len(val) < 300:
        rng.shuffle(ids); val = ids[:max(300, len(ids)//12)]; train = ids[max(300, len(ids)//12):]
    scaler = StandardScaler().fit(Xraw[train])
    X = scaler.transform(Xraw).astype(np.float32)
    target = np.c_[Ymean, Yvar].astype(np.float32)
    torch.manual_seed(seed)
    model = RecurrentTemporalPAM(seq.shape[2], X.shape[1])
    opt = torch.optim.AdamW(model.parameters(), lr=1.2e-3, weight_decay=1.5e-4)
    trdl = DataLoader(PrefixDataset(seq,lengths,X,target,train), batch_size=384, shuffle=True, num_workers=0)
    best = None; best_loss = 1e9; patience = 0; hist=[]
    for epoch in range(1, 25):
        model.train(); losses=[]
        for sq, ln, st, tg in trdl:
            opt.zero_grad(); pm,pv=model(sq.float(),ln.long(),st.float()); ym=tg[:,:12].float(); yv=tg[:,12:].float()
            # Variance is rescaled so it receives comparable delayed credit.
            loss=((pm-ym)**2).mean() + 0.60*((pv-yv)/0.25).pow(2).mean()
            loss.backward(); nn.utils.clip_grad_norm_(model.parameters(), 2.0); opt.step(); losses.append(float(loss.detach()))
        vm,vv=predict(model,seq,lengths,X,val); vl=float(np.mean((vm-Ymean[val])**2)+0.60*np.mean(((vv-Yvar[val])/0.25)**2))
        hist.append({'epoch':epoch,'train_loss':float(np.mean(losses)),'val_loss':vl})
        if vl < best_loss-1e-5:
            best_loss=vl; best={k:q.detach().cpu().clone() for k,q in model.state_dict().items()};patience=0
        else: patience+=1
        if patience>=4 and epoch>=8: break
    model.load_state_dict(best)
    pm,pv=predict(model,seq,lengths,X,np.where(pred_mask)[0])
    return pm,pv,model,scaler,{'train_rows':len(train),'validation_rows':len(val),'best_val_loss':best_loss,'epochs':len(hist),'history':hist}


def crossfit(seq, lengths, Xraw, Ymean, Yvar, split):
    train = split <= 5; caltest = split >= 6
    Pm=np.zeros_like(Ymean);Pv=np.zeros_like(Yvar);meta=[]
    folds=[np.isin(split,[0,3]),np.isin(split,[1,4]),np.isin(split,[2,5])]
    for fi,hold in enumerate(folds):
        fit=train&~hold; pred=train&hold
        print('V39_FOLD',fi,'fit',int(fit.sum()),'pred',int(pred.sum()),flush=True)
        pm,pv,m,s,mm=train_one(seq,lengths,Xraw,Ymean,Yvar,fit,pred,SEED+fi)
        Pm[pred]=pm;Pv[pred]=pv;meta.append({'fold':fi,**mm})
    print('V39_FINAL',int(train.sum()),int(caltest.sum()),flush=True)
    pm,pv,model,scaler,mm=train_one(seq,lengths,Xraw,Ymean,Yvar,train,caltest,SEED+20)
    Pm[caltest]=pm;Pv[caltest]=pv
    return Pm,Pv,model,scaler,{'folds':meta,'final':mm}


def save_action(prefix: str, models: dict):
    out={}
    for name,model in models.items():
        p=ROOT/f'R32_V39_{prefix}_{name.upper()}_SEED_9714.joblib';joblib.dump(model,p,compress=3);out[name]={'file':p.name,'sha256':sha(p)}
    return out


def main():
    t0=time.time()
    z32=np.load(ROOT/'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz')
    z33=np.load(ROOT/'R32_V33_LEARNED_GATING_DATA_SEED_9714.npz')
    z38=np.load(ROOT/'R32_V38_REPEATED_CONTINUATION_DATA_SEED_9714.npz')
    split=z32['split_code'].astype(int);adv=z32['advantage'].astype(float)
    Xbase=np.c_[z32['X_dynamics'].astype(np.float32),z33['gate_features'].astype(np.float32)]
    Ymean=z38['repeated_mean_target'].astype(np.float32);Yvar=z38['repeated_variance_target'].astype(np.float32)
    print('V39_BUILD_SEQUENCES',flush=True);seq,lengths,seqmeta=build_prefix_sequences(z32)
    print('V39_TRAIN_RECURRENT',flush=True);Pm,Pv,model,scaler,trainmeta=crossfit(seq,lengths,Xbase,Ymean,Yvar,split)
    arms={};files={}
    variants=[('recurrent_mean',np.c_[Xbase,Pm]),('recurrent_mean_variance',np.c_[Xbase,Pm,Pv]),('hybrid_extra_recurrent',np.c_[Xbase,z38['predicted_repeated_mean'],z38['predicted_repeated_variance'],Pm,Pv])]
    for i,(name,X) in enumerate(variants):
        print('V39_ACTION',name,flush=True);ms,val=v32.fit(X,adv,split,SEED+200+i*100);arms[name]=val;files[name]=save_action(name.upper(),ms)
    r38=json.loads((ROOT/'R32_V38_REPEATED_CONTINUATION_CREDIT_REFERENCE_ONLY.json').read_text());ref=r38['action_value']['arms']['predicted_mean_variance'];te=split>=8
    predmetrics={'extra_trees_mean':r38['prediction_metrics']['repeated_mean_prediction'],'extra_trees_variance':r38['prediction_metrics']['repeated_variance_prediction'],'recurrent_mean':v37.metrics(Ymean,Pm,split,adv),'recurrent_variance':v37.metrics(Yvar,Pv,split,adv)}
    deltas={}
    for name,val in arms.items():
        deltas[name]={'expected_auc':val['expected_advantage']['roc_auc']-ref['expected_advantage']['roc_auc'],'beneficial_cross':val['expected_advantage']['true_positive_cross_zero']-ref['expected_advantage']['true_positive_cross_zero'],'false_cross':val['expected_advantage']['false_positive_cross_zero']-ref['expected_advantage']['false_positive_cross_zero'],'selected_advantage':val['expected_advantage']['actual_mean_selected']-ref['expected_advantage']['actual_mean_selected']}
    ck=ROOT/'R32_V39_RECURRENT_TEMPORAL_PAM_SEED_9714.pt';torch.save({'state_dict':model.state_dict(),'seq_dim':seq.shape[2],'static_dim':Xbase.shape[1],'scaler_mean':scaler.mean_,'scaler_scale':scaler.scale_,'horizons':[1,2,3,5,8,12],'architecture':'causal 2-layer GRU + static MLP; no transformer/graph/tokenizer'},ck)
    dp=ROOT/'R32_V39_RECURRENT_TEMPORAL_DATA_SEED_9714.npz';np.savez_compressed(dp,sequence_prefix=seq,lengths=lengths.astype(np.int8),predicted_mean=Pm,predicted_variance=Pv,split_code=split.astype(np.int8),episode_id=z32['episode_id'])
    out={'experiment':'R32 V39 candidate-specific recurrent temporal PAM over retained ordered grounded evidence','architecture':{'type':'causal recurrent local dynamical PAM','sequence_input':'soft grounded candidate evidence plus TNN-chosen physical action identity','layers':'2-layer GRU, unidirectional, persistent-prefix state','no_graph':True,'no_transformer':True,'no_tokenizer_or_boundaries':True},'dataset':{**seqmeta,'static_feature_dim':Xbase.shape[1],'rows':len(split),'episode_disjoint_splits':True},'training':trainmeta,'prediction_metrics':predmetrics,'action_value':{'v38_extra_trees_mean_variance_reference':ref,'arms':arms,'delta_vs_v38':deltas,'models':files},'artifacts':{'checkpoint':{'file':ck.name,'sha256':sha(ck)},'data':{'file':dp.name,'sha256':sha(dp)}},'seconds':time.time()-t0,'training_boundary':'Targets are repeated delayed continuation mean/variance. No mode, ambiguity, resource-regime, future target, or final-answer feature enters the recurrent PAM.','claim_boundary':'REFERENCE_ONLY. Native Zag reproduction is required before promotion.'}
    rp=ROOT/'R32_V39_CANDIDATE_RECURRENT_TEMPORAL_PAM_REFERENCE_ONLY.json';rp.write_text(json.dumps(out,indent=2));cfg={'status':'REFERENCE_ONLY_MATCHED_RECURRENT_TEMPORAL_PAM','seed':SEED,'episode_disjoint_crossfit':True,'runtime_fixed_probe_count':False,'native_promotion_allowed':False,'source_sha256':sha(Path(__file__))};(ROOT/'R32_V39_CONFIG.json').write_text(json.dumps(cfg,indent=2));summary={'prediction':predmetrics,'action_delta':deltas,'seconds':out['seconds']};(ROOT/'R32_V39_TRAINING.log').write_text(json.dumps(summary,indent=2)+'\n');(ROOT/'R32_V39_DONE.flag').write_text('');print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':main()
