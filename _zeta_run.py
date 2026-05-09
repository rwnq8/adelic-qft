#!/usr/bin/env python3
"""Compute Riemann zeta zeros to N with file-based logging and checkpointing."""
import mpmath as mp, pickle, time, math, os, sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
BATCH = int(sys.argv[2]) if len(sys.argv) > 2 else 500

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE, f'zeta_results_{N}.pkl')
CHECKPOINT = os.path.join(BASE, f'zeta_checkpoint_{N}.pkl')
LOG = os.path.join(BASE, f'zeta_log_{N}.txt')

def log(msg):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg)  # Also try stdout

log(f'Starting zeta computation: N={N}, batch={BATCH}')

if os.path.exists(CHECKPOINT):
    with open(CHECKPOINT, 'rb') as f:
        d = pickle.load(f)
    zeros = d['zeros']
    sn = d.get('next_n', len(zeros) + 1)
    log(f'Resuming from checkpoint: {len(zeros)} zeros, starting at n={sn}')
else:
    zeros, sn = [], 1
    log('Fresh start')

t0 = time.time()
for bs in range(sn, N + 1, BATCH):
    be = min(bs + BATCH - 1, N)
    for n in range(bs, be + 1):
        zeros.append(float(mp.zetazero(n).imag))
    e = time.time() - t0
    pct = be / N * 100
    rate = be / e if e > 0 else 0
    eta = (N - be) / rate if rate > 0 else 0
    log(f'n={be:6d}  {pct:5.1f}%  {rate:.1f}z/s  ETA={eta/60:.1f}min')
    with open(CHECKPOINT, 'wb') as f:
        pickle.dump({'zeros': zeros, 'next_n': be + 1}, f)

tt = time.time() - t0
s = [zeros[i+1] - zeros[i] for i in range(len(zeros) - 1)]
ns = [s[i] / (2*math.pi / math.log(zeros[i+1] / (2*math.pi))) for i in range(len(s))]
mn = sum(ns) / len(ns) if ns else 0

log(f'DONE: {len(zeros)} zeros in {tt/60:.1f} minutes')
log(f'Range: {zeros[0]:.6f} to {zeros[-1]:.6f}')
log(f'Mean normalized spacing: {mn:.6f}')

pickle.dump({
    'zeros': zeros, 'spacings': s, 'norm_spacings': ns,
    'mean_norm': mn, 'count': len(zeros), 'time': tt
}, open(OUTPUT, 'wb'))
log(f'Saved results to {OUTPUT}')
