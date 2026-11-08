# Reel da tirinha "Furadeira no grupo das mães" (fotos realistas do Gemini) - 11/11 19h
import base64, os, subprocess
from playwright.sync_api import sync_playwright

PASTA = 'posts/2026-11-11-tirinha'
TMP = '/tmp/claude-0/-home-claude/9cbd0631-5475-5531-a229-dd0477b33b42/scratchpad/tir1111'
os.makedirs(TMP, exist_ok=True)
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
LOGO = 'data:image/png;base64,' + b64('logo_t.png')

BASE = """*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;font-family:'Poppins','Noto Color Emoji',sans-serif;position:relative;background:#000}
.foto{position:absolute;inset:0;background-size:cover;background-position:center}
.som{position:absolute;left:0;right:0;top:0;height:760px;background:linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,0))}
.balao{position:absolute;left:70px;right:70px;top:250px;background:#fff;color:#111;border-radius:34px;padding:38px 46px;font-weight:700;font-size:58px;line-height:1.18;text-align:center;box-shadow:0 10px 40px rgba(0,0,0,.35)}
.balao:after{content:'';position:absolute;left:50%;bottom:-34px;margin-left:-30px;border:30px solid transparent;border-top:36px solid #fff;border-bottom:0}
.quem{display:block;font-size:40px;color:#1560e8;margin-bottom:8px}
.gancho{position:absolute;left:50px;right:50px;top:230px;padding:46px 40px;border-radius:30px;background:rgba(2,6,20,.82);border:3px solid #2f8cff;box-shadow:0 0 40px rgba(40,140,255,.45);text-align:center;text-transform:uppercase;color:#fff;font-weight:700;font-size:86px;line-height:1.05}
.gancho b{color:#4fb0ff}
"""

def foto(img, dentro):
    return f'<html><head><style>{BASE}</style></head><body><div class="foto" style="background-image:url(data:image/jpeg;base64,{b64(img)})"></div><div class="som"></div>{dentro}</body></html>'

q = lambda n: f'{PASTA}/quadro{n}.jpg'
telas = [
    foto(q(1), '<div class="gancho">Seu grupo está<br><b>perdendo gente?</b></div>'),
    foto(q(1), '<div class="balao">Mandei uma furadeira no grupo das mães… de&nbsp;novo&nbsp;🤦‍♀️</div>'),
    foto(q(2), '<div class="balao">3 pessoas saíram do grupo hoje 😰</div>'),
    foto(q(3), '<div class="balao">Ninguém aguenta oferta repetida e fora do assunto…</div>'),
    foto(q(4), '<div class="balao"><span class="quem">Carol:</span>No meu, cada grupo recebe só ofertas do assunto dele, sem ficar repetindo.</div>'),
    foto(q(5), '<div class="balao">Agora o meu grupo só cresce 💕</div>'),
]

WAVES = ''.join(f'<path d="M0 {120+i*6} C 270 {40+i*9}, 540 {200-i*7}, 810 {110+i*4} S 1080 {60+i*8}, 1080 {90+i*5}" stroke="rgba(47,140,255,{0.10+i*0.012})" stroke-width="1.6" fill="none"/>' for i in range(16))
CTA = f"""<html><head><style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;font-family:'Poppins','Noto Color Emoji',sans-serif;color:#fff;background:#020409;position:relative;text-align:center}}
.glow{{position:absolute;inset:0;background:radial-gradient(ellipse 70% 45% at 50% 42%,rgba(20,90,220,.35) 0%,rgba(5,20,60,.25) 45%,transparent 75%),radial-gradient(circle at 100% 0%,rgba(30,120,255,.35),transparent 30%),radial-gradient(circle at 0% 100%,rgba(30,120,255,.25),transparent 30%)}}
.waves{{position:absolute;left:0;right:0;bottom:-20px;height:300px}}
.wrap{{position:relative;height:100%;padding:250px 70px 260px;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.logo{{width:560px;height:360px;background:url({LOGO}) center/contain no-repeat;filter:drop-shadow(0 0 30px rgba(40,130,255,.5))}}
h2{{font-weight:700;font-size:84px;line-height:1.05;text-transform:uppercase;margin-top:40px}}
.sub{{font-size:46px;font-weight:600;color:#4fb0ff;margin-top:34px;line-height:1.25}}
.cta{{margin-top:60px;padding:36px 54px;border-radius:60px;background:linear-gradient(180deg,#3aa0ff,#1560e8);font-size:52px;font-weight:700;box-shadow:0 0 40px rgba(40,140,255,.6)}}
.dm{{font-size:40px;font-weight:600;margin-top:34px;color:#dfe8f8}}</style></head><body>
<div class="glow"></div><svg class="waves" viewBox="0 0 1080 300" preserveAspectRatio="none">{WAVES}</svg>
<div class="wrap"><div class="logo"></div><h2>Oferta certa<br>no grupo certo.</h2>
<div class="sub">Cada grupo recebe ofertas do assunto dele, sem repetir o mesmo produto toda hora.</div>
<div class="cta">Teste 7 dias grátis<br>LINK DA BIO 👆</div><div class="dm">ou mande QUERO no Direct 💬</div></div></body></html>"""
telas.append(CTA)

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for i, h in enumerate(telas):
        pg.set_content(h); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{TMP}/t{i}.png')
    b.close()

dur = [2.0, 2.6, 3.0, 3.0, 3.0, 3.0, 4.0]
xf = [0.3, 0.4, 0.4, 0.4, 0.4, 0.4]
ent, fil = [], []
for i, d in enumerate(dur):
    ent += ['-loop', '1', '-t', str(d), '-i', f'{TMP}/t{i}.png']
    n = int(d * 30)
    if i < len(dur) - 1:  # zoom leve nas fotos
        fil.append(f'[{i}:v]scale=2160:3840,zoompan=z=\'min(1+0.0009*on,1.08)\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={n}:s=1080x1920:fps=30,setsar=1,format=yuv420p[v{i}]')
    else:
        fil.append(f'[{i}:v]scale=1080:1920,fps=30,setsar=1,format=yuv420p[v{i}]')
cur, t = 'v0', dur[0]
for i in range(1, len(dur)):
    off = t - xf[i - 1]
    fil.append(f'[{cur}][v{i}]xfade=transition=fade:duration={xf[i-1]}:offset={off:.2f}[x{i}]')
    cur, t = f'x{i}', off + dur[i]
total = t
saida = f'{PASTA}/reel_tirinha_1111.mp4'
cmd = ['ffmpeg', '-y', '-v', 'error'] + ent + ['-f', 'lavfi', '-t', f'{total:.2f}', '-i', 'anullsrc=r=44100:cl=stereo',
       '-filter_complex', ';'.join(fil), '-map', f'[{cur}]', '-map', f'{len(dur)}:a',
       '-c:v', 'libx264', '-preset', 'veryfast', '-profile:v', 'main', '-level', '4.0', '-pix_fmt', 'yuv420p', '-r', '30',
       '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', saida]
subprocess.run(cmd, check=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'{TMP}/t0.png', '-q:v', '3', f'{PASTA}/capa_tirinha_1111.jpg'], check=True)
print('ok', saida, round(total, 2))
