import base64, os
from playwright.sync_api import sync_playwright
from PIL import Image
OUT='posts/2026-11-15'; os.makedirs(OUT,exist_ok=True)
LOGO='data:image/png;base64,'+base64.b64encode(open('logo_t.png','rb').read()).decode()
WAVES=''.join(f'<path d="M0 {120+i*6} C 270 {40+i*9}, 540 {200-i*7}, 810 {110+i*4} S 1080 {60+i*8}, 1080 {90+i*5}" stroke="rgba(47,140,255,{0.10+i*0.012})" stroke-width="1.6" fill="none"/>' for i in range(16))
CSS="""
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;font-family:'Poppins',sans-serif;color:#fff;background:#020409;position:relative;overflow:hidden;text-transform:uppercase}
.glow{position:absolute;inset:0;background:radial-gradient(ellipse 80% 40% at 50% 45%,rgba(20,90,220,.35) 0%,rgba(5,20,60,.25) 45%,transparent 75%),radial-gradient(circle at 100% 0%,rgba(30,120,255,.35),transparent 30%),radial-gradient(circle at 0% 100%,rgba(30,120,255,.25),transparent 30%)}
.waves{position:absolute;left:0;right:0;bottom:-20px;height:420px}
.wrap{position:relative;height:100%;padding:250px 80px 250px;display:flex;flex-direction:column;align-items:center;text-align:center}
.logo{width:320px;height:210px;background:url(LOGO) center/contain no-repeat;filter:drop-shadow(0 0 30px rgba(40,130,255,.5))}
.kicker{font-weight:700;font-size:40px;letter-spacing:1px;margin-top:10px}
.kicker b{color:#2f9bff}
.w{background:linear-gradient(180deg,#fff 0%,#dfe6f0 55%,#9aa6b8 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 4px 6px rgba(0,0,0,.6))}
.b{background:linear-gradient(180deg,#5ec2ff 0%,#2b8cff 50%,#1560e8 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 0 18px rgba(40,140,255,.55))}
h2{font-weight:700;font-size:92px;line-height:1.05;letter-spacing:-1px;margin-top:50px}
.card{margin-top:70px;width:100%;padding:44px 40px;border-radius:30px;background:linear-gradient(90deg,rgba(25,80,190,.35),rgba(10,25,60,.25));border:2px solid rgba(60,150,255,.55);box-shadow:0 0 35px rgba(40,130,255,.2);font-size:48px;font-weight:700}
.cta{margin-top:60px;padding:30px 50px;border-radius:26px;background:linear-gradient(180deg,#3aa0ff,#1560e8);font-size:52px;font-weight:700;box-shadow:0 0 40px rgba(40,140,255,.6)}
.foot{position:absolute;left:0;right:0;bottom:250px;text-align:center;font-size:40px;font-weight:700;color:#9fb3d6}
"""
html=f"""<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="glow"></div>
<svg class="waves" viewBox="0 0 1080 300" preserveAspectRatio="none">{WAVES}</svg>
<div class="wrap"><div class="logo" style="background-image:url({LOGO})"></div>
<div class="kicker">QUANTOS GRUPOS <b>VOCÊ CUIDA?</b></div>
<h2><span class="w">CUIDAR SOZINHO</span><br><span class="b">TEM LIMITE</span></h2>
<div class="card">POST NOVO NO PERFIL 👆</div>
<div class="cta" style="font-size:44px">VEJA NO FEED</div>
</div>
<div class="foot">TESTE 7 DIAS GRÁTIS — LINK NA BIO</div>
</body></html>"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1080,'height':1920}); pg.set_content(html); pg.wait_for_timeout(500)
    pg.screenshot(path=f'{OUT}/_s.png'); Image.open(f'{OUT}/_s.png').convert('RGB').save(f'{OUT}/story_1115.jpg',quality=88); os.remove(f'{OUT}/_s.png'); b.close()
print('ok')
