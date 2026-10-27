import base64
from playwright.sync_api import sync_playwright

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
.logo{width:520px;height:340px;background:url(LOGO) center/contain no-repeat;filter:drop-shadow(0 0 30px rgba(40,130,255,.5))}
.kicker{font-weight:700;font-size:34px;letter-spacing:1px;margin-top:20px}
.kicker b{color:#2f9bff}
.w{background:linear-gradient(180deg,#ffffff 0%,#dfe6f0 55%,#9aa6b8 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 4px 6px rgba(0,0,0,.6))}
.b{background:linear-gradient(180deg,#5ec2ff 0%,#2b8cff 50%,#1560e8 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 0 18px rgba(40,140,255,.55))}
h1{font-weight:700;font-size:104px;line-height:1.02;letter-spacing:-1px;-webkit-text-stroke:1.5px transparent}
h2{font-weight:700;font-size:88px;line-height:1.06;letter-spacing:-1px}
.mid{margin:auto 0;padding-top:40px;width:100%}
.list{margin-top:46px;display:flex;flex-direction:column;gap:22px;width:100%}
.item{display:flex;align-items:center;gap:26px;padding:22px 34px;border-radius:22px;background:linear-gradient(90deg,rgba(25,80,190,.35),rgba(10,25,60,.25));border:2px solid rgba(60,150,255,.55);font-weight:700;font-size:40px;text-align:left;box-shadow:0 0 25px rgba(40,130,255,.15)}
.item i{font-style:normal;flex:none;width:62px;height:62px;border-radius:50%;background:#1f7bff;display:flex;align-items:center;justify-content:center;font-size:32px;box-shadow:0 0 18px rgba(40,140,255,.7)}
.item.x i{background:#c62f3f;box-shadow:0 0 18px rgba(230,60,80,.6)}
.sub{font-size:36px;font-weight:500;color:#c3d3ee;margin-top:36px;text-transform:none}
.stores{display:flex;flex-wrap:wrap;justify-content:center;gap:20px;margin-top:50px}
.store{padding:24px 38px;border-radius:20px;font-size:40px;font-weight:700;background:rgba(20,70,180,.3);border:2px solid #2f8cff;box-shadow:0 0 22px rgba(40,140,255,.3)}
.cta{margin-top:50px;padding:38px 60px;border-radius:26px;background:linear-gradient(180deg,#3aa0ff,#1560e8);font-size:56px;font-weight:700;box-shadow:0 0 40px rgba(40,140,255,.6)}
.foot{width:100%;display:flex;justify-content:space-between;align-items:center;font-size:28px;font-weight:600;color:#7f97c4;margin-top:20px}
.arrow{color:#fff;background:rgba(47,140,255,.25);border:2px solid #2f8cff;padding:14px 30px;border-radius:40px}
""".replace('LOGO', LOGO)

def page(inner, n, total=6, last=False):
    foot = f'<div class="foot"><span>{n}/{total}</span>' + ('<span></span>' if last else '<span class="arrow">ARRASTE ➜</span>') + '</div>'
    return (f'<html><head><style>{CSS}</style></head><body><div class="glow"></div>'
            f'<svg class="waves" viewBox="0 0 1080 300" preserveAspectRatio="none">{WAVES}</svg>'
            f'<div class="wrap"><div class="logo"></div>{inner}{foot}</div></body></html>')


def rpage(inner):
    return (f'<html><head><style>{CSS}</style></head><body><div class="glow"></div>'
            f'<svg class="waves" viewBox="0 0 1080 300" preserveAspectRatio="none">{WAVES}</svg>'
            f'<div class="wrap"><div class="logo"></div>{inner}</div></body></html>')
slides = [
 rpage('<div class="mid"><div class="kicker">AFILIADO, <b>PARE AGORA</b></div><h1 style="margin-top:40px"><span class="w">3 ERROS QUE</span><br><span class="b">TRAVAM SUAS VENDAS</span></h1><div class="sub">O terceiro quase todo mundo comete 👀</div></div>'),
 rpage('<div class="mid"><div class="kicker">ERRO <b>1</b></div><h2 style="margin-top:30px"><span class="w">POSTAR SÓ QUANDO</span><br><span class="b">SOBRA TEMPO</span></h2><div class="list"><div class="item x"><i>✕</i>Grupo parado esfria</div><div class="item x"><i>✕</i>Membro sai e não volta</div></div></div>'),
 rpage('<div class="mid"><div class="kicker">ERRO <b>2</b></div><h2 style="margin-top:30px"><span class="w">GARIMPAR OFERTA</span><br><span class="b">UMA POR UMA</span></h2><div class="list"><div class="item x"><i>✕</i>Horas no celular todo dia</div><div class="item x"><i>✕</i>Quando posta, já acabou</div></div></div>'),
 rpage('<div class="mid"><div class="kicker">ERRO <b>3</b></div><h2 style="margin-top:30px"><span class="w">DEPENDER SÓ</span><br><span class="b">DE UMA LOJA</span></h2><div class="list"><div class="item x"><i>✕</i>Menos oferta boa</div><div class="item x"><i>✕</i>Menos chance de comissão</div></div></div>'),
 rpage('<div class="mid"><h2><span class="w">O SISTEMA QUE</span><br><span class="b">POSTA SOZINHO</span></h2><div class="list"><div class="item"><i>✓</i>Busca ofertas 24h</div><div class="item"><i>✓</i>Gera seu link de afiliado</div><div class="item"><i>✓</i>Posta nos seus grupos</div></div><div class="stores"><div class="store">SHOPEE</div><div class="store">MERCADO LIVRE</div><div class="store">AMAZON</div><div class="store">MAGALU</div><div class="store">LOMADEE</div></div></div>'),
 rpage('<div class="mid"><div class="kicker">TRANSFORME <b>CLIQUES EM VENDAS</b></div><h2 style="margin-top:30px"><span class="w">PARE DE GARIMPAR.</span><br><span class="b">DEIXE O SISTEMA POSTAR.</span></h2><div class="cta">MANDE “QUERO” NO DIRECT</div><div class="sub">e receba o link na hora — ou toque no link da bio<br><b style="color:#fff">sistemaafiliado.com.br/assinar</b></div></div>'),
]
from playwright.sync_api import sync_playwright
import os
os.makedirs('/home/claude/reel',exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    for i,h in enumerate(slides,1):
        pg.set_content(h); pg.wait_for_timeout(300); pg.screenshot(path=f'/home/claude/reel/t{i}.png')
    b.close()
print('ok')
