import json, subprocess, sys, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__))
OFF = {1: 0, 2: 4.3, 3: 13.7, 4: 15.8, 5: 29.7, 6: 39.0}
FIX = {'Chopi,': 'Shopee,', 'Lomadi.': 'Lomadee.', 'Gere': 'gera', 'Camilla': 'Camila', 'um': 'um'}
pal = json.load(open(f'{D}/palavras.json'))
pal['6'][4][0] = 'o'           # "com o grupo"
pal['5'][-1][0] = 'ofertas.'
pal['4'][2][0] = 'o WhatsApp'
caps = []
for k, ws in pal.items():
    o = OFF[int(k)]; cur = []
    for w, a, b in ws:
        w = FIX.get(w, w)
        txt = ' '.join(x[0] for x in cur)
        if cur and (len(txt) + len(w) > 18 or cur[-1][0][-1] in '.?!' or (cur[-1][0][-1]==',' and len(txt)>=8)):
            caps.append(cur); cur = []
        cur.append([w, a + o, b + o])
    caps.append(cur)
CAPS = []
for i, c in enumerate(caps):
    nxt = caps[i + 1][0][1] if i + 1 < len(caps) else 1e9
    fim = min(nxt, c[-1][2] + 0.5)
    CAPS.append({'a': c[0][1], 'b': fim, 'w': [[w, a] for w, a, b in c]})

DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 50.0
FPS = 30
saida = sys.argv[2] if len(sys.argv) > 2 else f'{D}/video_mudo.mp4'
so = [float(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else None
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto(f'file://{D}/vsl.html'); pg.wait_for_timeout(800)
    pg.evaluate('c=>{CAPS=c}', CAPS)
    if so:
        for t in so:
            pg.evaluate(f'render({t})'); pg.screenshot(path=f'{D}/prev_{t}.jpg', type='jpeg', quality=80)
        sys.exit()
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', saida], stdin=subprocess.PIPE)
    for f in range(int(DUR * FPS)):
        pg.evaluate(f'render({f / FPS})')
        ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
    ff.stdin.close(); ff.wait()
    b.close()
print('ok', saida)
