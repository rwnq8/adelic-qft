#!/usr/bin/env python3
"""Compute Riemann zeta zeros to height N with checkpointing.
Usage: python _zeta_compute.py [N] [batch_size]
Default: N=100000, batch=2000
Writes checkpoint file after each batch.
"""
import mpmath as mp
import pickle, os, sys, time, math

TOTAL = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
BATCH = int(sys.argv[2]) if len(sys.argv) > 2 else 2000

BASE = os.path.dirname(os.path.abspath(__file__))
CHECKPOINT = os.path.join(BASE, f'zeta_checkpoint_{TOTAL}.pkl')
RESULTS = os.path.join(BASE, f'zeta_results_{TOTAL}.pkl')

if os.path.exists(CHECKPOINT):
    with open(CHECKPOINT, 'rb') as f:
        d = pickle.load(f)
    zeros = d['zeros']
    start_n = d.get('next_n', len(zeros) + 1)
    print(f'Resuming from checkpoint: {len(zeros)} zeros, starting at n={start_n}')
else:
    zeros, start_n = [], 1

t0 = time.time()
for bs in range(start_n, TOTAL + 1, BATCH):
    be = min(bs + BATCH - 1, TOTAL)
    for n in range(bs, be + 1):
        zeros.append(float(mp.zetazero(n).imag))
    e = time.time() - t0
    pct = be / TOTAL * 100
    rate = be / e if e > 0 else 0
    eta = (TOTAL - be) / rate if rate > 0 else 0
    print(f'  n={be:6d}  {pct:5.1f}%  {rate:.1f}z/s  ETA={eta/60:.1f}min', flush=True)
    with open(CHECKPOINT, 'wb') as f:
        pickle.dump({'zeros': zeros, 'next_n': be + 1}, f)

tt = time.time() - t0
s = [zeros[i+1] - zeros[i] for i in range(len(zeros) - 1)]
ns = [s[i] / (2*math.pi / math.log(zeros[i+1] / (2*math.pi))) for i in range(len(s))]
mn = sum(ns) / len(ns)
print(f'\nDone: {len(zeros)} zeros in {tt/60:.1f} minutes')
print(f'Range: {zeros[0]:.6f} to {zeros[-1]:.6f}')
print(f'Mean normalized spacing: {mn:.6f}')

pickle.dump({
    'zeros': zeros, 'spacings': s, 'norm_spacings': ns,
    'mean_norm': mn, 'count': len(zeros), 'time': tt
}, open(RESULTS, 'wb'))
print(f'Saved to {RESULTS}')
