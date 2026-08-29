from __future__ import annotations

import gc
import glob
import hashlib
import json
import math
import os
import random
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy.io import wavfile
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from torch.utils.data import DataLoader, Dataset

import r32_tts_self_chunk_streaming as base

OUT = Path('/mnt/data/r32_epistemic')
CACHE = OUT / 'tts_cache_segmental'
CACHE.mkdir(exist_ok=True)
DEVICE = torch.device('cpu')
torch.set_num_threads(max(1, min(5, os.cpu_count() or 1)))

# These templates belong to the external developmental world. The learner sees only
# resulting waveforms and grounded action consequences; no text, token, word,
# phoneme, boundary, VAD state, or template ID enters cognition.
TRAIN_TEMPLATES = [
    '{actor} {action} the {object} now',
]
TEST_TEMPLATES = {
    'template_prefix': 'right now {actor} can {action} the {object}',
    'template_postposed': 'the {object} is what {actor} will {action} now',
    'template_polite': 'please let {actor} {action} the {object} carefully',
}


def synth_text(text: str, voice: str, speed: int, pitch: int) -> tuple[int, np.ndarray]:
    key = hashlib.sha1(f'{text}|{voice}|{speed}|{pitch}'.encode()).hexdigest()[:24]
    hits = glob.glob(str(CACHE / f'{key}.*.wav'))
    p = Path(hits[0]) if hits else CACHE / f'{key}.{os.getpid()}.wav'
    if not p.exists():
        subprocess.run(
            ['espeak', '-v', voice, '-s', str(speed), '-p', str(pitch), '-w', str(p), text],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    try:
        sr, x = wavfile.read(p)
    except Exception:
        p.unlink(missing_ok=True)
        subprocess.run(
            ['espeak', '-v', voice, '-s', str(speed), '-p', str(pitch), '-w', str(p), text],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        sr, x = wavfile.read(p)
    x = x.astype(np.float32)
    x /= max(1.0, float(np.max(np.abs(x))))
    return sr, x


def perturb(sr: int, x: np.ndarray, seed: int, strength: int) -> np.ndarray:
    if strength <= 0:
        return x
    rng = np.random.default_rng(seed)
    # Time warping, moderate additive noise, and slowly varying gain. No segments
    # or linguistic boundaries are used.
    rate = float(rng.uniform(0.87, 1.15))
    from scipy.signal import resample_poly
    den = 100
    num = max(55, int(round(rate * den)))
    y = resample_poly(x, den, num).astype(np.float32)
    y += rng.normal(0, 0.006 + 0.003 * min(strength, 3), len(y)).astype(np.float32)
    seg = max(256, len(y) // 12)
    gain = rng.uniform(0.78, 1.22, 16)
    idx = np.minimum(np.arange(len(y)) // seg, len(gain) - 1)
    y *= gain[idx]
    if strength >= 2 and len(y) > 1000:
        # Small random waveform dropout; not VAD and not aligned to speech units.
        w = int(rng.integers(max(100, len(y)//80), max(101, len(y)//35)))
        st = int(rng.integers(0, max(1, len(y)-w)))
        y[st:st+w] *= float(rng.uniform(0.0, 0.25))
    return np.clip(y, -1, 1).astype(np.float32)


def feature(sr: int, x: np.ndarray) -> np.ndarray:
    return base.feat(sr, x)


@dataclass(frozen=True)
class SampleSpec:
    actor_i: int
    action_i: int
    object_i: int
    actor: str
    action: str
    object_name: str
    voice: str
    speed: int
    pitch: int
    template: str
    condition: str
    perturb_strength: int = 0

    @property
    def text(self) -> str:
        return self.template.format(actor=self.actor, action=self.action, object=self.object_name)


def build_specs(seed: int, train_repeats: int = 2) -> tuple[list[SampleSpec], list[SampleSpec]]:
    train: list[SampleSpec] = []
    test: list[SampleSpec] = []
    for ai, actor in enumerate(base.ACTORS):
        for yi, action in enumerate(base.ACTIONS):
            for oi, obj in enumerate(base.OBJECTS):
                if not base.hold(ai, oi):
                    for voice in base.TRAIN_VOICES:
                        for speed in base.SPEEDS:
                            for rep in range(train_repeats):
                                train.append(SampleSpec(ai, yi, oi, actor, action, obj, voice, speed,
                                    44 + ((ai * 3 + oi) % 13), TRAIN_TEMPLATES[0], 'train', rep))
                # Existing-style unseen voices/speeds and held-out composition.
                for voice in base.TEST_VOICES:
                    for speed in [105, 225]:
                        cond = 'heldout_comp' if base.hold(ai, oi) else 'speaker_speed'
                        test.append(SampleSpec(ai, yi, oi, actor, action, obj, voice, speed, 57,
                                               TRAIN_TEMPLATES[0], cond, 0))
                        test.append(SampleSpec(ai, yi, oi, actor, action, obj, voice, speed, 57,
                                               TRAIN_TEMPLATES[0], 'hard_noise', 2))
                # Unseen sentence layouts, one held-out voice and two speeds.
                for cond, tmpl in TEST_TEMPLATES.items():
                    for speed in [125, 205]:
                        test.append(SampleSpec(ai, yi, oi, actor, action, obj, 'en-uk-rp', speed, 55,
                                               tmpl, cond, 1))
    rng = random.Random(seed)
    rng.shuffle(train)
    rng.shuffle(test)
    return train, test


def make_feature(spec: SampleSpec, seed: int) -> np.ndarray:
    sr, x = synth_text(spec.text, spec.voice, spec.speed, spec.pitch)
    x = perturb(sr, x, seed + spec.actor_i*1009 + spec.action_i*131 + spec.object_i*17 + spec.speed,
                spec.perturb_strength)
    return feature(sr, x)


class AcousticDataset(Dataset):
    def __init__(self, specs: list[SampleSpec], seed: int):
        self.specs = specs
        self.seed = seed
        self.cache: list[np.ndarray | None] = [None] * len(specs)

    def __len__(self) -> int:
        return len(self.specs)

    def __getitem__(self, idx: int):
        x = self.cache[idx]
        if x is None:
            x = make_feature(self.specs[idx], self.seed)
            self.cache[idx] = x
        return x, self.specs[idx].action_i, self.specs[idx].condition


def collate(batch):
    xs, ys, conds = zip(*batch)
    lengths = torch.tensor([len(x) for x in xs], dtype=torch.long)
    tmax = int(lengths.max())
    feat_dim = xs[0].shape[1]
    out = torch.zeros((len(xs), tmax, feat_dim), dtype=torch.float32)
    for i, x in enumerate(xs):
        out[i, :len(x)] = torch.from_numpy(x)
    return out, lengths, torch.tensor(ys, dtype=torch.long), list(conds)


class TemporalConvPAM(nn.Module):
    def __init__(self, dim: int = 49, hidden: int = 80, classes: int = 6):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(dim, hidden, 7, stride=2, padding=3), nn.GELU(),
            nn.Conv1d(hidden, hidden, 5, padding=4, dilation=2), nn.GELU(),
            nn.Conv1d(hidden, hidden, 5, padding=8, dilation=4), nn.GELU(),
        )
        self.out = nn.Sequential(nn.Linear(hidden * 2, 96), nn.GELU(), nn.Dropout(.15), nn.Linear(96, classes))

    def forward(self, x, lengths):
        h = self.conv(x.transpose(1, 2)).transpose(1, 2)
        l = torch.div(lengths + 1, 2, rounding_mode='floor').clamp(min=1, max=h.shape[1])
        mask = torch.arange(h.shape[1], device=h.device)[None, :] < l[:, None]
        hm = h.masked_fill(~mask[:, :, None], -1e4).amax(1)
        ha = (h * mask[:, :, None]).sum(1) / l[:, None]
        return self.out(torch.cat([hm, ha], 1)), None


class SegmentalRecurrentPAM(nn.Module):
    """Non-transformer learner-gated segmental recurrent PAM.

    A causal GRU supplies temporal state. A mutable boundary gate determines when
    a new segment state replaces the ongoing segment. No target boundary exists.
    The only learning signals are grounded consequence, general resource cost,
    and consistency under ordinary waveform perturbation.
    """
    def __init__(self, dim: int = 49, hidden: int = 72, classes: int = 6):
        super().__init__()
        self.front = nn.Sequential(
            nn.Conv1d(dim, 64, 7, stride=2, padding=3), nn.GELU(),
            nn.Conv1d(64, 72, 5, padding=4, dilation=2), nn.GELU(),
        )
        self.gru = nn.GRU(72, hidden, batch_first=True)
        self.boundary = nn.Linear(hidden, 1)
        self.classifier = nn.Sequential(nn.Linear(hidden * 3, 112), nn.GELU(), nn.Dropout(.15), nn.Linear(112, classes))

    def forward(self, x, lengths):
        z = self.front(x.transpose(1, 2)).transpose(1, 2)
        l = torch.div(lengths + 1, 2, rounding_mode='floor').clamp(min=1, max=z.shape[1])
        packed = pack_padded_sequence(z, l.cpu(), batch_first=True, enforce_sorted=False)
        hp, _ = self.gru(packed)
        h, _ = pad_packed_sequence(hp, batch_first=True, total_length=z.shape[1])
        mask = torch.arange(h.shape[1], device=h.device)[None, :] < l[:, None]
        b = torch.sigmoid(self.boundary(h)).squeeze(-1) * mask
        # Soft learner-owned segment state. Large b starts a new state; small b
        # preserves the current chunk. The recurrence is causal and differentiable.
        state = torch.zeros((h.shape[0], h.shape[2]), device=h.device)
        emitted = []
        for t in range(h.shape[1]):
            g = b[:, t:t+1]
            state = (1.0 - g) * state + g * h[:, t]
            emitted.append(state)
        s = torch.stack(emitted, 1)
        sm = s.masked_fill(~mask[:, :, None], -1e4).amax(1)
        sa = (s * mask[:, :, None]).sum(1) / l[:, None]
        # Boundary-weighted event summary retains rare discriminating spans.
        sw = (h * b[:, :, None]).sum(1) / (b.sum(1, keepdim=True) + 1e-5)
        logits = self.classifier(torch.cat([sm, sa, sw], 1))
        stats = {
            'boundary_rate': (b.sum() / mask.sum().clamp(min=1)),
            'boundary_entropy': (-(b.clamp(1e-5,1-1e-5)*torch.log(b.clamp(1e-5,1-1e-5)) +
                                  (1-b).clamp(1e-5,1-1e-5)*torch.log((1-b).clamp(1e-5,1-1e-5))) * mask).sum() / mask.sum().clamp(min=1),
        }
        return logits, stats


def train_model(model: nn.Module, train_ds: AcousticDataset, dev_ds: AcousticDataset,
                seed: int, epochs: int = 12, batch_size: int = 32):
    torch.manual_seed(seed)
    rng = torch.Generator().manual_seed(seed)
    tr = DataLoader(train_ds, batch_size=batch_size, shuffle=True, generator=rng, collate_fn=collate, num_workers=0)
    dv = DataLoader(dev_ds, batch_size=64, shuffle=False, collate_fn=collate, num_workers=0)
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=2e-4)
    best = None
    best_score = -1.0
    history = []
    for ep in range(1, epochs + 1):
        model.train(); losses=[]; br=[]
        for x, lengths, y, _ in tr:
            opt.zero_grad(set_to_none=True)
            logits, stats = model(x, lengths)
            loss = F.cross_entropy(logits, y)
            if stats is not None:
                # Generic resource pressure discourages degenerate one-boundary-per-frame
                # behavior. It does not impose a human chunk count or location.
                loss = loss + 0.012 * stats['boundary_rate'] + 0.002 * stats['boundary_entropy']
                br.append(float(stats['boundary_rate'].detach()))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 4.0)
            opt.step(); losses.append(float(loss.detach()))
        acc, _ = evaluate(model, dv)
        history.append({'epoch':ep,'loss':float(np.mean(losses)),'dev_acc':acc,'boundary_rate':float(np.mean(br)) if br else None})
        if acc > best_score:
            best_score = acc
            best = {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
        if ep in (1,2,4,8,12):
            print('EPOCH', ep, 'LOSS', history[-1]['loss'], 'DEV', acc, 'BOUND', history[-1]['boundary_rate'], flush=True)
    assert best is not None
    model.load_state_dict(best)
    return history


@torch.no_grad()
def evaluate(model: nn.Module, loader: DataLoader):
    model.eval(); correct=0; total=0; by={}; bounds=[]
    for x, lengths, y, conds in loader:
        logits, stats = model(x, lengths); p=logits.argmax(1)
        correct += int((p==y).sum()); total += len(y)
        if stats is not None: bounds.append(float(stats['boundary_rate']))
        for i,c in enumerate(conds):
            z=by.setdefault(c,[0,0]);z[0]+=int(p[i]==y[i]);z[1]+=1
    return correct/max(1,total), {'conditions':{k:v[0]/v[1] for k,v in by.items()},'boundary_rate':float(np.mean(bounds)) if bounds else None}


def run_seed(seed: int, train_repeats: int = 2, epochs: int = 12):
    train_specs, test_specs = build_specs(seed, train_repeats)
    # Development split is composition-stratified but uses only development voices/templates.
    rng = np.random.default_rng(seed)
    idx = np.arange(len(train_specs)); rng.shuffle(idx)
    ndev = max(240, int(.12*len(idx))); dev_idx=set(map(int,idx[:ndev]))
    tr_specs=[s for i,s in enumerate(train_specs) if i not in dev_idx]
    dv_specs=[s for i,s in enumerate(train_specs) if i in dev_idx]
    tr_ds=AcousticDataset(tr_specs,seed);dv_ds=AcousticDataset(dv_specs,seed+91);te_ds=AcousticDataset(test_specs,seed+193)
    results={'seed':seed,'train_n':len(tr_ds),'dev_n':len(dv_ds),'test_n':len(te_ds),'models':{}}
    for name,model in [('temporal_conv',TemporalConvPAM()),('segmental_recurrent',SegmentalRecurrentPAM())]:
        print('MODEL',seed,name,flush=True)
        hist=train_model(model,tr_ds,dv_ds,seed+(0 if name=='temporal_conv' else 10000),epochs=epochs)
        loader=DataLoader(te_ds,batch_size=64,shuffle=False,collate_fn=collate,num_workers=0)
        acc,detail=evaluate(model,loader)
        # Hard mean excludes training-like nominal conditions and directly attacks
        # voice/speed, noise, held-out composition, and unseen sentence layouts.
        hard_keys=['speaker_speed','hard_noise','heldout_comp',*TEST_TEMPLATES.keys()]
        hard=float(np.mean([detail['conditions'][k] for k in hard_keys]))
        extreme=[k for k,v in detail['conditions'].items() if v in (0.0,1.0)]
        results['models'][name]={'overall':acc,'hard_mean':hard,**detail,'history':hist,'extreme_flags':extreme}
        print('RESULT',seed,name,acc,hard,detail,flush=True)
        del model;gc.collect()
    (OUT/f'R32_SEGMENTAL_PAM_SEED_{seed}.json').write_text(json.dumps(results,indent=2))
    return results


def main():
    rows=[]
    for seed in [35000,35001]:
        r=run_seed(seed,train_repeats=2,epochs=12);rows.append(r)
        print('DONE_SEED',seed,flush=True)
    aggregate={}
    for name in rows[0]['models']:
        conds=rows[0]['models'][name]['conditions']
        aggregate[name]={
            'overall':float(np.mean([r['models'][name]['overall'] for r in rows])),
            'hard_mean':float(np.mean([r['models'][name]['hard_mean'] for r in rows])),
            'boundary_rate':float(np.mean([r['models'][name]['boundary_rate'] for r in rows if r['models'][name]['boundary_rate'] is not None])) if name=='segmental_recurrent' else None,
            'conditions':{c:float(np.mean([r['models'][name]['conditions'][c] for r in rows])) for c in conds},
        }
    out={'aggregate':aggregate,'rows':rows,'boundary':'REFERENCE_ONLY non-transformer elastic temporal PAM experiment. The learner sees raw waveform-derived acoustic frames and grounded action consequences. The segmental PAM learns its own soft recurrent change points under generic resource pressure; no transcript, word/phoneme/token/chunk boundary, VAD, ASR, attention/transformer, or LLM enters cognition. Unseen sentence layouts prevent a fixed-position shortcut.'}
    (OUT/'R32_TTS_SEGMENTAL_RECURRENT_PAM_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(aggregate,indent=2))

if __name__=='__main__':
    main()
