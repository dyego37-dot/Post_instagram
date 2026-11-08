import base64, os
from playwright.sync_api import sync_playwright
from PIL import Image
LOGO = 'data:image/png;base64,' + base64.b64encode(open('logo_t.png','rb').read()).decode()
WAVES = ''.join(
    f'<path d="M0 {120+i*6} C 270 {40+i*9}, 540 {200-i*7}, 810 {110+i*4} S 1080 {60+i*8}, 1080 {90+i*5}" '
    f'stroke="rgba(47,140,255,{0.10+i*0.012})" stroke-width="1.6" fill="none"/>' for i in range(16))
CSS = open('build.py').read().split('CSS = """')[1].split('""".replace')[0].replace('LOGO', LOGO)
CSS += """
body{height:1920px}
.wrap{padding:270px 70px 270px!important}
.logo{width:380px;height:250px}
h2{font-size:92px}
"""
def rpage(inner):
    return (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="glow"></div>'
            f'<svg class="waves" viewBox="0 0 1080 300" preserveAspectRatio="none">{WAVES}</svg>'
            f'<div class="wrap"><div class="logo"></div>{inner}</div></body></html>')
story = rpage('<div class="mid"><div class="kicker">AFILIADO, <b>ATENÇÃO</b></div>'
      '<h2 style="margin-top:30px"><span class="w">LINK QUE NÃO ABRE</span><br><span class="b">É VENDA PERDIDA</span></h2>'
      '<div class="sub" style="font-size:44px;color:#fff;margin-top:50px">O sistema confere antes de postar</div>'
      '<div class="sub" style="font-size:40px;margin-top:70px;color:#9fd0ff">POST NOVO NO PERFIL 👆</div>'
      '<div class="sub" style="font-size:40px;margin-top:40px;color:#fff;font-weight:700">TESTE 7 DIAS GRÁTIS — LINK NA BIO</div></div>')
OUT = 'posts/2026-11-09'
os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1080,'height':1920})
    pg.set_content(story); pg.wait_for_timeout(300)
    pg.screenshot(path=f'{OUT}/story_1109.png')
    b.close()
Image.open(f'{OUT}/story_1109.png').convert('RGB').save(f'{OUT}/story_1109.jpg', quality=88)
os.remove(f'{OUT}/story_1109.png')
print('ok story')
