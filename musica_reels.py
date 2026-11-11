# Música de fundo própria (sem direito autoral) para os Reels.
# Uso: python3 musica_reels.py DURACAO VIRADA TOM VARIACAO saida.wav
#   VIRADA = segundo em que a história fica feliz (0 = só parte animada)
import sys, wave
import numpy as np

SR = 44100
D = float(sys.argv[1]); TURN = float(sys.argv[2]); SH = int(sys.argv[3]); VAR = int(sys.argv[4]); OUT = sys.argv[5]
N = int(SR * D); t = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(VAR)
f = lambda m: 440 * 2 ** ((m + SH - 69) / 12)

def add(i0, sig, pan=0.5, g=1.0):
    i0 = int(i0 * SR)
    if i0 >= N or i0 + len(sig) <= 0: return
    if i0 < 0: sig = sig[-i0:]; i0 = 0
    sig = sig[:N - i0]
    L[i0:i0 + len(sig)] += sig * g * (1 - pan) * 2 * 0.7
    R[i0:i0 + len(sig)] += sig * g * pan * 2 * 0.7

def tone(m, dur, decay, harm=(1, .4, .15), vib=0):
    u = np.arange(int(dur * SR)) / SR
    ph = 2 * np.pi * f(m) * u + vib * np.sin(2 * np.pi * 5 * u)
    s = sum(a * np.sin((k + 1) * ph) for k, a in enumerate(harm))
    return s * np.exp(-u * decay) * np.minimum(1, u / 0.008)

def pad(chord, dur, g):
    u = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, u / 0.6) * np.minimum(1, (dur - u) / 0.5)
    s = np.zeros(len(u))
    for m in chord:
        for det in (-0.12, 0.12):
            s += np.sin(2 * np.pi * f(m) * (1 + det / 100) * u)
    return s * env * g

# ---------- parte triste/melancólica (antes da virada) ----------
SAD = [[[57, 60, 64], [53, 57, 60], [48, 52, 55], [52, 55, 59]],   # Am F C Em
       [[57, 60, 64], [50, 53, 57], [52, 55, 59], [57, 60, 64]],   # Am Dm Em Am
       [[57, 60, 64], [53, 57, 60], [50, 53, 57], [52, 56, 59]]][VAR % 3]  # Am F Dm E
if TURN > 0:
    bar = 60 / 72 * 4
    b = 0; s0 = 0.0
    while s0 < TURN + 0.6:
        ch = SAD[b % 4]
        add(s0, pad(ch, bar + 0.5, 0.05), 0.5)
        add(s0, tone(ch[0] - 24, bar, 0.6, (1, .2)) * 0.18)
        mel = [ch[2] + 12, ch[1] + 12, ch[0] + 12, ch[1] + 12]
        for k, m in enumerate(mel):  # piano lento
            add(s0 + k * bar / 4 + (0.04 if k % 2 else 0), tone(m, 2.2, 1.6, (1, .5, .2, .08)) * 0.11, 0.35 + 0.3 * (k % 2))
        b += 1; s0 += bar
    # some aos poucos na virada
    k = np.clip((TURN + 0.4 - t) / 0.8, 0, 1)
    L *= k; R *= k
    # subida (riser) + brilho na virada
    rl = 1.2; u = np.arange(int(rl * SR)) / SR
    n = rng.standard_normal(len(u)); n = np.convolve(n, np.ones(6) / 6, 'same')
    add(TURN - rl, n * (u / rl) ** 2 * 0.12)
    for m in (72, 76, 79, 84):
        add(TURN, tone(m, 1.5, 3, (1, .3)) * 0.07, 0.5)

# ---------- parte alegre/animada (depois da virada) ----------
HAPPY = [[[48, 55, 60, 64], [43, 55, 59, 62], [45, 57, 60, 64], [41, 53, 57, 60]],   # C G Am F
         [[41, 53, 57, 60], [43, 55, 59, 62], [48, 55, 60, 64], [48, 55, 60, 64]],   # F G C C
         [[48, 55, 60, 64], [45, 57, 60, 64], [41, 53, 57, 60], [43, 55, 59, 62]]][VAR % 3]  # C Am F G
bpm = 120 + (VAR % 3) * 2; beat = 60 / bpm; bar = beat * 4
b = 0; s0 = TURN
while s0 < D:
    ch = HAPPY[b % 4]
    add(s0, pad([m + 12 for m in ch[1:]], bar, 0.028))
    for q in range(8):  # baixo saltado
        add(s0 + q * beat / 2, tone(ch[0] - 12 + (12 if q % 2 else 0), beat / 2, 6, (1, .5, .2)) * 0.16)
    arp = [ch[1] + 12, ch[2] + 12, ch[3] + 12, ch[2] + 24, ch[3] + 12, ch[2] + 12, ch[1] + 24, ch[3] + 12]
    for e in range(8):  # arpejo brilhante
        add(s0 + e * beat / 2, tone(arp[e], 0.4, 8, (1, .3, .1)) * 0.075, 0.5 + 0.3 * np.sin(e))
    for q in range(4):  # bateria
        st = s0 + q * beat
        u = np.arange(int(0.3 * SR)) / SR
        add(st, np.sin(2 * np.pi * (48 + 110 * np.exp(-u * 32)) * u) * np.exp(-u * 11) * 0.32)
        hh = rng.standard_normal(int(0.05 * SR)); hh = np.diff(hh, prepend=0) * np.exp(-np.arange(len(hh)) / SR * 70) * 0.05
        add(st + beat / 2, hh, 0.6)
        if q in (1, 3):
            cl = rng.standard_normal(int(0.18 * SR)) * np.exp(-np.arange(int(0.18 * SR)) / SR * 22) * 0.09
            add(st, cl, 0.45)
    b += 1; s0 += bar

fade = np.minimum(1, t / 0.6) * np.minimum(1, (D - t) / 1.2)
st = np.stack([L * fade, R * fade], 1)
st = st / np.max(np.abs(st)) * 0.85
w = wave.open(OUT, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
