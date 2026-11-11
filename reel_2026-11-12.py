import base64, os
from playwright.sync_api import sync_playwright

OUT = 'posts/2026-11-12'
LOGO = 'data:image/png;base64,' + base64.b64encode(open('logo_t.png','rb').read()).decode()
WAVES = ''.join(
    f'<path d="M0 {120+i*6} C 270 {40+i*9}, 540 {200-i*7}, 810 {110+i*4} S 1080 {60+i*8}, 1080 {90+i*5}" '
    f'stroke="rgba(47,140,255,{0.10+i*0.012})" stroke-width="1.6" fill="none"/>' for i in range(16))

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;font-family:'Poppins',sans-serif;color:#fff;background:#020409;position:relative;overflow:hidden;text-transform:uppercase}
.glow{position:absolute;inset:0;background:radial-gradient(ellipse 70% 45% at 50% 42%,rgba(20,90,220,.35) 0%,rgba(5,20,60,.25) 45%,transparent 75%),radial-gradient(circle at 100% 0%,rgba(30,120,255,.35),transparent 30%),radial-gradient(circle at 0% 100%,rgba(30,120,255,.25),transparent 30%)}
.waves{position:absolute;left:0;right:0;bottom:-20px;height:300px}
.wrap{position:relative;height:100%;padding:160px 70px 220px;display:flex;flex-direction:column;align-items:center;text-align:center}
.wrap.story{padding:300px 70px 300px}
.logo{width:520px;height:340px;background:url(LOGO) center/contain no-repeat;filter:drop-shadow(0 0 30px rgba(40,130,255,.5))}
.kicker{font-weight:700;font-size:34px;letter-spacing:1px;margin-top:20px}
.kicker b{color:#2f9bff}
.w{background:linear-gradient(180deg,#ffffff 0%,#dfe6f0 55%,#9aa6b8 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 4px 6px rgba(0,0,0,.6))}
.b{background:linear-gradient(180deg,#5ec2ff 0%,#2b8cff 50%,#1560e8 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 0 18px rgba(40,140,255,.55))}
h1{font-weight:700;font-size:100px;line-height:1.02;letter-spacing:-1px}
h2{font-weight:700;font-size:92px;line-height:1.06;letter-spacing:-1px}
.mid{margin:auto 0;padding-top:40px;width:100%}
.list{margin-top:46px;display:flex;flex-direction:column;gap:22px;width:100%}
.item{display:flex;align-items:center;gap:26px;padding:22px 34px;border-radius:22px;background:linear-gradient(90deg,rgba(25,80,190,.35),rgba(10,25,60,.25));border:2px solid rgba(60,150,255,.55);font-weight:700;font-size:40px;text-align:left;box-shadow:0 0 25px rgba(40,130,255,.15)}
.item i{font-style:normal;flex:none;width:62px;height:62px;border-radius:50%;background:#1f7bff;display:flex;align-items:center;justify-content:center;font-size:32px;box-shadow:0 0 18px rgba(40,140,255,.7)}
.item.x i{background:#c62f3f;box-shadow:0 0 18px rgba(230,60,80,.6)}
.sub{font-size:36px;font-weight:500;color:#c3d3ee;margin-top:36px;text-transform:none}
.stores{display:flex;flex-wrap:wrap;justify-content:center;gap:20px;margin-top:50px}
.store{padding:24px 38px;border-radius:20px;font-size:40px;font-weight:700;background:rgba(20,70,180,.3);border:2px solid #2f8cff;box-shadow:0 0 22px rgba(40,140,255,.3)}
.cta{margin-top:50px;padding:38px 60px;border-radius:26px;background:linear-gradient(180deg,#3aa0ff,#1560e8);font-size:56px;font-weight:700;box-shadow:0 0 40px rgba(40,140,255,.6)}
.pill{margin-top:40px;padding:26px 50px;border-radius:40px;font-size:50px;font-weight:700;background:rgba(47,140,255,.25);border:2px solid #2f8cff}
.foot{font-size:32px;font-weight:700;color:#9fc0ef;margin-top:40px}
""".replace('LOGO', LOGO)

def doc(inner, story=False):
    cls = 'wrap story' if story else 'wrap'
    return (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="glow"></div>'
            f'<svg class="waves" viewBox="0 0 1080 300" preserveAspectRatio="none">{WAVES}</svg>'
            f'<div class="{cls}"><div class="logo"></div>{inner}</div></body></html>')

slides = [
 doc('<div class="mid"><h1><span class="w">NÃO SABE O QUE</span><br><span class="b">POSTAR HOJE?</span></h1><div class="sub">Você não é o único 👀</div></div>'),
 doc('<div class="mid"><div class="kicker">O <b>PROBLEMA</b></div><h2 style="margin-top:30px"><span class="w">GARIMPAR OFERTA</span><br><span class="b">TODO DIA CANSA</span></h2><div class="list"><div class="item x"><i>✕</i>Procura produto e não acha</div><div class="item x"><i>✕</i>Posta a mesma coisa de sempre</div></div></div>'),
 doc('<div class="mid"><div class="kicker">O <b>SISTEMA</b></div><h2 style="margin-top:30px"><span class="w">ESCOLHE PELO</span><br><span class="b">NICHO DO SEU GRUPO</span></h2><div class="list"><div class="item"><i>✓</i>Olha as categorias do grupo</div><div class="item"><i>✓</i>Confere se o produto está na loja</div></div></div>'),
 doc('<div class="mid"><div class="kicker">COMO <b>FUNCIONA</b></div><h2 style="margin-top:30px"><span class="w">CONFIGURA UMA VEZ</span><br><span class="b">NO COMPUTADOR</span></h2><div class="list"><div class="item"><i>✓</i>Depois acompanha pelo celular</div><div class="item"><i>✓</i>Posta nos grupos 24 horas</div></div></div>'),
 doc('<div class="mid"><h2><span class="w">SHOPEE, ML</span><br><span class="b">E LOMADEE</span></h2><div class="stores"><div class="store">SHOPEE</div><div class="store">MERCADO LIVRE</div><div class="store">LOMADEE</div></div><div class="sub">Amazon e Magalu por link ou extensão</div></div>'),
 doc('<div class="mid"><div class="kicker">COMECE <b>HOJE</b></div><h2 style="margin-top:30px"><span class="w">TESTE 7 DIAS</span><br><span class="b">GRÁTIS</span></h2><div class="cta">LINK NA BIO</div><div class="sub">ou mande “QUERO” no Direct<br><b style="color:#fff">sistemaafiliado.com.br/assinar</b></div></div>'),
]

story = doc(
 '<div class="mid"><div class="kicker">NÃO SABE O QUE <b>POSTAR HOJE?</b></div>'
 '<h1 style="margin-top:40px"><span class="w">O SISTEMA</span><br><span class="b">ESCOLHE POR VOCÊ</span></h1>'
 '<div class="pill">POST NOVO NO PERFIL 👆</div></div>'
 '<div class="foot">TESTE 7 DIAS GRÁTIS — LINK NA BIO</div>', story=True)

os.makedirs(OUT, exist_ok=True)
tmp = 'reel_tmp'; os.makedirs(tmp, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1920})
    for i, h in enumerate(slides, 1):
        pg.set_content(h); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{tmp}/t{i}.png')
    pg.set_content(story); pg.wait_for_timeout(300)
    pg.screenshot(path=f'{OUT}/story_1112.jpg', type='jpeg', quality=88)
    b.close()
print('ok')
