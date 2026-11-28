import base64
from playwright.sync_api import sync_playwright
LOGO='data:image/png;base64,'+base64.b64encode(open('logo_t.png','rb').read()).decode()
WAVES=''.join(f'<path d="M0 {120+i*6} C 270 {40+i*9}, 540 {200-i*7}, 810 {110+i*4} S 1080 {60+i*8}, 1080 {90+i*5}" stroke="rgba(47,140,255,{0.10+i*0.012})" stroke-width="1.6" fill="none"/>' for i in range(16))
html=f'''<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;font-family:'Poppins',sans-serif;color:#fff;background:#020409;position:relative;overflow:hidden;text-transform:uppercase}}
.glow{{position:absolute;inset:0;background:radial-gradient(ellipse 80% 40% at 50% 45%,rgba(20,90,220,.38),rgba(5,20,60,.25) 50%,transparent 80%),radial-gradient(circle at 100% 0%,rgba(30,120,255,.35),transparent 30%)}}
.waves{{position:absolute;left:0;right:0;bottom:0;height:520px}}
.wrap{{position:relative;height:100%;padding:250px 80px 250px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.logo{{width:420px;height:260px;background:url({LOGO}) center/contain no-repeat;filter:drop-shadow(0 0 30px rgba(40,130,255,.5));margin-bottom:10px}}
.kicker{{font-weight:700;font-size:38px;letter-spacing:1px;margin-top:20px}}
.kicker b{{color:#2f9bff}}
.w{{background:linear-gradient(180deg,#fff 0%,#dfe6f0 55%,#9aa6b8 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 4px 6px rgba(0,0,0,.6))}}
.b{{background:linear-gradient(180deg,#5ec2ff 0%,#2b8cff 50%,#1560e8 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 0 18px rgba(40,140,255,.55))}}
h1{{font-weight:700;font-size:96px;line-height:1.04;letter-spacing:-1px;margin-top:40px}}
.pill{{margin-top:70px;padding:34px 52px;border-radius:30px;background:linear-gradient(180deg,#3aa0ff,#1560e8);font-size:50px;font-weight:700;box-shadow:0 0 40px rgba(40,140,255,.6)}}
.foot{{margin-top:60px;font-size:34px;font-weight:600;color:#9fb3d6;border:2px solid #2f8cff;border-radius:40px;padding:18px 34px;background:rgba(47,140,255,.2)}}
</style></head><body><div class="glow"></div>
<svg class="waves" viewBox="0 0 1080 300" preserveAspectRatio="none">{WAVES}</svg>
<div class="wrap"><div class="logo"></div>
<div class="kicker">PERGUNTA <b>DO AFILIADO</b></div>
<h1><span class="w">VOCÊ SABE</span><br><span class="b">QUANTO GANHOU</span><br><span class="w">ESTE MÊS?</span></h1>
<div class="pill">POST NOVO NO PERFIL 👆</div>
<div class="foot">TESTE 7 DIAS GRÁTIS — LINK NA BIO</div>
</div></body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.set_content(html); pg.wait_for_timeout(400)
    pg.screenshot(path='posts/2026-11-29/story_1129.png')
    b.close()
from PIL import Image
Image.open('posts/2026-11-29/story_1129.png').convert('RGB').save('posts/2026-11-29/story_1129.jpg',quality=88)
import os; os.remove('posts/2026-11-29/story_1129.png')
print('story ok')
