import numpy as np, wave
import sys
SR = 44100; D = float(sys.argv[1]); N = int(SR * D)
t = np.arange(N) / SR
bpm = float(sys.argv[2]); SH = int(sys.argv[3]); beat = 60 / bpm; bar = beat * 4
def f(m): m = m + SH; return 440 * 2 ** ((m - 69) / 12)
PROGS={'a':[[48,55,60,64],[43,55,59,62],[45,57,60,64],[41,53,57,60]],'b':[[45,57,60,64],[41,53,57,60],[48,55,60,64],[43,55,59,62]],'c':[[41,53,57,60],[43,55,59,62],[45,57,60,64],[48,55,60,64]],'d':[[48,55,60,64],[45,57,60,64],[41,53,57,60],[43,55,59,62]]}
prog=PROGS[sys.argv[4]]
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(1)
nbars = int(D / bar) + 1
for b in range(nbars):
    ch = prog[b % 4]; s0 = b * bar
    i0 = int(s0 * SR); i1 = min(N, int((s0 + bar) * SR))
    if i0 >= N: break
    tt = t[i0:i1] - s0
    env = np.minimum(1, tt / 0.4) * np.minimum(1, (bar - tt) / 0.3 + 0.2)
    for k, m in enumerate(ch):
        for det, side in ((-0.15, 'L'), (0.15, 'R')):
            v = np.sin(2 * np.pi * f(m + 12 if k else m) * (1 + det / 100) * tt) * 0.045 * env
            (L if side == 'L' else R)[i0:i1] += v
    # bass
    L[i0:i1] += np.sin(2 * np.pi * f(ch[0] - 12) * tt) * 0.11 * env
    R[i0:i1] += np.sin(2 * np.pi * f(ch[0] - 12) * tt) * 0.11 * env
    # arp eighths
    arp = [ch[1] + 12, ch[2] + 12, ch[3] + 12, ch[2] + 24]
    for e in range(8):
        st = s0 + e * beat / 2
        j0 = int(st * SR); j1 = min(N, j0 + int(0.5 * SR))
        if j0 >= N: break
        u = t[j0:j1] - st
        m = arp[e % 4]
        v = (np.sin(2 * np.pi * f(m) * u) + 0.3 * np.sin(4 * np.pi * f(m) * u)) * np.exp(-u * 7) * 0.06
        pan = 0.5 + 0.3 * np.sin(e)
        L[j0:j1] += v * (1 - pan) * 2 * 0.7; R[j0:j1] += v * pan * 2 * 0.7
    # drums start after 2 bars
    if b >= 1:
        for q in range(4):
            st = s0 + q * beat; j0 = int(st * SR); j1 = min(N, j0 + int(0.3 * SR))
            if j0 >= N: break
            u = t[j0:j1] - st
            kick = np.sin(2 * np.pi * (50 + 90 * np.exp(-u * 30)) * u) * np.exp(-u * 12) * 0.28
            L[j0:j1] += kick; R[j0:j1] += kick
            hs = st + beat / 2; h0 = int(hs * SR); h1 = min(N, h0 + int(0.06 * SR))
            if h0 < N:
                n = rng.standard_normal(h1 - h0); n = np.diff(n, prepend=0) * np.exp(-np.arange(h1 - h0) / SR * 60) * 0.035
                L[h0:h1] += n; R[h0:h1] += n
            if q in (1, 3):
                c0 = j0; c1 = min(N, c0 + int(0.15 * SR))
                n = rng.standard_normal(c1 - c0) * np.exp(-np.arange(c1 - c0) / SR * 25) * 0.06
                L[c0:c1] += n; R[c0:c1] += n
fade = np.minimum(1, t / 1.0) * np.minimum(1, (D - t) / 1.5)
L *= fade; R *= fade
st = np.stack([L, R], 1); st = st / np.max(np.abs(st)) * 0.8
w = wave.open(sys.argv[5], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
