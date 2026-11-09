import os, subprocess
from PIL import Image
src = open('reel_build.py').read().split('slides = [')[0]
exec(src)
from playwright.sync_api import sync_playwright

slides = [
 rpage('<div class="mid"><h1><span class="w">VOCÊ SABE QUAL</span><br><span class="w">OFERTA TROUXE</span><br><span class="b">CLIQUE?</span></h1></div>'),
 rpage('<div class="mid"><div class="kicker">POSTANDO <b>NO ESCURO</b></div><h2 style="margin-top:30px"><span class="w">VOCÊ POSTA E</span><br><span class="b">NÃO VÊ O RESULTADO</span></h2><div class="list"><div class="item x"><i>✕</i>Não sabe de onde veio o clique</div><div class="item x"><i>✕</i>Repete oferta que ninguém clicou</div></div></div>'),
 rpage('<div class="mid"><div class="kicker">O PAINEL <b>MOSTRA</b></div><h2 style="margin-top:30px"><span class="w">DE ONDE VEM</span><br><span class="b">CADA CLIQUE</span></h2><div class="list"><div class="item"><i>✓</i>Cliques por canal: WhatsApp, Instagram e Telegram</div><div class="item"><i>✓</i>Ofertas que geram clique</div></div></div>'),
 rpage('<div class="mid"><div class="kicker">VOCÊ ACOMPANHA <b>NO CELULAR</b></div><h2 style="margin-top:30px"><span class="w">OFERTAS POSTADAS</span><br><span class="b">E CLIQUES NO PAINEL</span></h2><div class="list"><div class="item"><i>✓</i>Ofertas encontradas e postadas</div><div class="item"><i>✓</i>Comissão e cliques em um lugar</div></div></div>'),
 rpage('<div class="mid"><h2><span class="w">O SISTEMA POSTA</span><br><span class="b">E MOSTRA O RESULTADO</span></h2><div class="stores"><div class="store">SHOPEE</div><div class="store">MERCADO LIVRE</div><div class="store">LOMADEE</div></div><div class="sub">Busca, gera seu link e posta 24 horas</div></div>'),
 rpage('<div class="mid"><h2><span class="w">TESTE</span><br><span class="b">7 DIAS GRÁTIS</span></h2><div class="cta">LINK NA BIO</div><div class="sub">ou mande “QUERO” no Direct<br><b style="color:#fff">sistemaafiliado.com.br/assinar</b></div></div>'),
]
DUR = [2, 3, 3, 3, 3, 3]
D = 'posts/2026-11-10'
os.makedirs(D, exist_ok=True)
os.makedirs('/home/claude/reel', exist_ok=True)

story_html = rpage('<div class="mid"><div class="kicker">POST NOVO <b>NO PERFIL 👆</b></div>'
    '<h2 style="margin-top:40px"><span class="w">VOCÊ SABE QUAL</span><br><span class="b">OFERTA TROUXE CLIQUE?</span></h2>'
    '<div class="sub">O painel mostra de onde vem cada clique</div>'
    '<div class="sub" style="font-size:40px;margin-top:90px;color:#fff;font-weight:700">TESTE 7 DIAS GRÁTIS — LINK NA BIO</div></div>')
story_html = story_html.replace('padding:160px 70px 220px', 'padding:270px 70px 270px')
story_html = story_html.replace('.logo{width:520px;height:340px', '.logo{width:520px;height:340px')
story_html = story_html.replace('<body>', '<body><style>body{height:1920px}</style>', 1)
story_html = story_html.replace('<html><head>', '<html><head><meta charset="utf-8">', 1)

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for i, h in enumerate(slides, 1):
        pg.set_content(h); pg.wait_for_timeout(300); pg.screenshot(path=f'/home/claude/reel/t{i}.png')
    pg.set_content(story_html); pg.wait_for_timeout(300); pg.screenshot(path='/home/claude/reel/story_raw.png')
    b.close()
Image.open('/home/claude/reel/t1.png').convert('RGB').save(f'{D}/capa_1110.jpg', quality=88)
Image.open('/home/claude/reel/story_raw.png').convert('RGB').save(f'{D}/story_1110.jpg', quality=88)

# segmentos com zoom leve (sem fade de entrada)
segs = []
for i, d in enumerate(DUR, 1):
    out = f'/home/claude/reel/s{i}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loop', '1', '-i', f'/home/claude/reel/t{i}.png', '-t', str(d),
        '-vf', "scale=2160:3840,zoompan=z='min(zoom+0.0006,1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p",
        '-c:v', 'libx264', '-preset', 'veryfast', '-profile:v', 'main', '-level', '4.0', '-pix_fmt', 'yuv420p', '-r', '30', out],
        check=True, capture_output=True)
    segs.append(out)

T = 0.5
inputs = []
for s in segs:
    inputs += ['-i', s]
fc = []
prev = '[0:v]'
acc = DUR[0]
for i in range(1, len(segs)):
    off = round(acc - T, 3)
    tag = f'[v{i}]' if i < len(segs) - 1 else '[vout]'
    fc.append(f'{prev}[{i}:v]xfade=transition=fade:duration={T}:offset={off}{tag}')
    prev = tag
    acc += DUR[i] - T
total = acc
fc_str = ';'.join(fc)
OUTV = f'{D}/reel_1110.mp4'
subprocess.run(['ffmpeg', '-y'] + inputs + ['-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
    '-filter_complex', fc_str, '-map', '[vout]', '-map', f'{len(segs)}:a',
    '-c:v', 'libx264', '-preset', 'veryfast', '-profile:v', 'main', '-level', '4.0', '-pix_fmt', 'yuv420p', '-r', '30',
    '-c:a', 'aac', '-b:a', '128k', '-t', str(round(total, 3)), '-movflags', '+faststart', OUTV],
    check=True, capture_output=True)
print('ok reel', round(total, 2))
