import base64, os
from playwright.sync_api import sync_playwright
from PIL import Image

OUT = 'posts/2026-10-29'
os.makedirs(OUT, exist_ok=True)

LOGO = 'data:image/png;base64,' + base64.b64encode(open('logo_t.png','rb').read()).decode()

WAVES = ''.join(
    f'<path d="M0 {120+i*6} C 270 {40+i*9}, 540 {200-i*7}, 810 {110+i*4} S 1080 {60+i*8}, 1080 {90+i*5}" '
    f'stroke="rgba(47,140,255,{0.10+i*0.012})" stroke-width="1.6" fill="none"/>' for i in range(16))

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:'Poppins',sans-serif;color:#fff;background:#020409;position:relative;overflow:hidden;text-transform:uppercase}
.glow{position:absolute;inset:0;background:radial-gradient(ellipse 70% 45% at 50% 42%,rgba(20,90,220,.35) 0%,rgba(5,20,60,.25) 45%,transparent 75%),radial-gradient(circle at 100% 0%,rgba(30,120,255,.35),transparent 30%),radial-gradient(circle at 0% 100%,rgba(30,120,255,.25),transparent 30%)}
.waves{position:absolute;left:0;right:0;bottom:-20px;height:300px}
.wrap{position:relative;height:100%;padding:60px 70px 70px;display:flex;flex-direction:column;align-items:center;text-align:center}
.logo{width:380px;height:250px;background:url(LOGO) center/contain no-repeat;filter:drop-shadow(0 0 30px rgba(40,130,255,.5))}
.kicker{font-weight:700;font-size:34px;letter-spacing:1px;margin-top:20px}
.kicker b{color:#2f9bff}
.w{background:linear-gradient(180deg,#ffffff 0%,#dfe6f0 55%,#9aa6b8 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 4px 6px rgba(0,0,0,.6))}
.b{background:linear-gradient(180deg,#5ec2ff 0%,#2b8cff 50%,#1560e8 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 0 18px rgba(40,140,255,.55))}
h1{font-weight:700;font-size:104px;line-height:1.02;letter-spacing:-1px}
h2{font-weight:700;font-size:78px;line-height:1.06;letter-spacing:-1px}
.mid{margin:auto 0;padding-top:40px;width:100%}
.list{margin-top:46px;display:flex;flex-direction:column;gap:22px;width:100%}
.item{display:flex;align-items:center;gap:26px;padding:22px 34px;border-radius:22px;background:linear-gradient(90deg,rgba(25,80,190,.35),rgba(10,25,60,.25));border:2px solid rgba(60,150,255,.55);font-weight:700;font-size:40px;text-align:left;box-shadow:0 0 25px rgba(40,130,255,.15)}
.item i{font-style:normal;flex:none;width:62px;height:62px;border-radius:50%;background:#1f7bff;display:flex;align-items:center;justify-content:center;font-size:32px;box-shadow:0 0 18px rgba(40,140,255,.7)}
.item.x i{background:#c62f3f;box-shadow:0 0 18px rgba(230,60,80,.6)}
.sub{font-size:36px;font-weight:500;color:#c3d3ee;margin-top:36px;text-transform:none}
.cta{margin-top:50px;padding:38px 60px;border-radius:26px;background:linear-gradient(180deg,#3aa0ff,#1560e8);font-size:56px;font-weight:700;box-shadow:0 0 40px rgba(40,140,255,.6)}
.foot{width:100%;display:flex;justify-content:space-between;align-items:center;font-size:28px;font-weight:600;color:#7f97c4;margin-top:20px}
.arrow{color:#fff;background:rgba(47,140,255,.25);border:2px solid #2f8cff;padding:14px 30px;border-radius:40px}
""".replace('LOGO', LOGO)

def page(inner, n, total=6, last=False):
    foot = f'<div class="foot"><span>{n}/{total}</span>' + ('<span></span>' if last else '<span class="arrow">ARRASTE ➜</span>') + '</div>'
    return (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="glow"></div>'
            f'<svg class="waves" viewBox="0 0 1080 300" preserveAspectRatio="none">{WAVES}</svg>'
            f'<div class="wrap"><div class="logo"></div>{inner}{foot}</div></body></html>')

slides = [
 page('<div class="mid"><div class="kicker">AFILIADO, <b>PRESTA ATENÇÃO</b></div>'
      '<h1 style="margin-top:40px"><span class="w">3 MITOS SOBRE</span><br><span class="b">SER AFILIADO</span></h1>'
      '<div class="sub">Um deles pode estar te fazendo desistir…</div></div>', 1),
 page('<div class="mid"><div class="kicker">MITO <b>1</b></div><h2 style="margin-top:20px"><span class="w">"PRECISA TER</span><br><span class="b">MUITOS SEGUIDORES"</span></h2><div class="list">'
      '<div class="item x"><i>✕</i>Quem indica oferta em grupo não aparece</div>'
      '<div class="item"><i>✓</i>O que vale é a oferta certa no momento certo</div></div></div>', 2),
 page('<div class="mid"><div class="kicker">MITO <b>2</b></div><h2 style="margin-top:20px"><span class="w">"TEM QUE FICAR</span><br><span class="b">O DIA TODO POSTANDO"</span></h2><div class="list">'
      '<div class="item x"><i>✕</i>Garimpar e postar na mão cansa</div>'
      '<div class="item"><i>✓</i>O sistema busca e posta nos grupos 24h</div></div></div>', 3),
 page('<div class="mid"><div class="kicker">MITO <b>3</b></div><h2 style="margin-top:20px"><span class="w">"SÓ DÁ CERTO</span><br><span class="b">NUMA LOJA"</span></h2><div class="list">'
      '<div class="item x"><i>✕</i>Depender de uma única loja</div>'
      '<div class="item"><i>✓</i>Shopee, Mercado Livre, Amazon, Magalu e Lomadee</div></div></div>', 4),
 page('<div class="mid"><div class="kicker">O QUE <b>FAZ A DIFERENÇA</b></div><h2 style="margin-top:20px"><span class="w">CONSTÂNCIA E</span><br><span class="b">AUTOMAÇÃO</span></h2><div class="list">'
      '<div class="item"><i>1</i>Grupo que recebe oferta todo dia</div>'
      '<div class="item"><i>2</i>Link de afiliado gerado para você</div>'
      '<div class="item"><i>3</i>Mensagem pronta, sem garimpo manual</div></div></div>', 5),
 page('<div class="mid"><div class="kicker">COMECE <b>AGORA</b></div><h2 style="margin-top:30px"><span class="w">DEIXE O SISTEMA</span><br><span class="b">TRABALHAR POR VOCÊ</span></h2>'
      '<div class="cta">MANDE “QUERO” NO DIRECT</div>'
      '<div class="sub">e receba o link na hora — ou toque no link da bio<br><b style="color:#fff">sistemaafiliado.com.br/assinar</b></div></div>', 6, last=True),
]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1080,'height':1350})
    for i, html in enumerate(slides, 1):
        pg.set_content(html); pg.wait_for_timeout(300)
        png = f'/tmp/_s{i}.png'
        pg.screenshot(path=f'{OUT}/slide{i}.png')
        Image.open(f'{OUT}/slide{i}.png').convert('RGB').save(f'{OUT}/{i:02d}.jpg', quality=88)
        os.remove(f'{OUT}/slide{i}.png')
    b.close()
print('ok')
