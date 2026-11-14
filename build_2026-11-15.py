import base64, os
from playwright.sync_api import sync_playwright
from PIL import Image

OUT = 'posts/2026-11-15'
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
h2{font-weight:700;font-size:78px;line-height:1.06;letter-spacing:-1px}
.mid{margin:auto 0;padding-top:40px;width:100%}
.list{margin-top:46px;display:flex;flex-direction:column;gap:22px;width:100%}
.item{display:flex;align-items:center;gap:26px;padding:22px 34px;border-radius:22px;background:linear-gradient(90deg,rgba(25,80,190,.35),rgba(10,25,60,.25));border:2px solid rgba(60,150,255,.55);font-weight:700;font-size:40px;text-align:left;box-shadow:0 0 25px rgba(40,130,255,.15)}
.item i{font-style:normal;flex:none;width:62px;height:62px;border-radius:50%;background:#1f7bff;display:flex;align-items:center;justify-content:center;font-size:32px;box-shadow:0 0 18px rgba(40,140,255,.7)}
.sub{font-size:36px;font-weight:500;color:#c3d3ee;margin-top:36px;text-transform:none}
.cta{margin-top:50px;padding:38px 60px;border-radius:26px;background:linear-gradient(180deg,#3aa0ff,#1560e8);font-size:56px;font-weight:700;box-shadow:0 0 40px rgba(40,140,255,.6)}
.foot{width:100%;display:flex;justify-content:space-between;align-items:center;font-size:28px;font-weight:600;color:#7f97c4;margin-top:20px}
.arrow{color:#fff;background:rgba(47,140,255,.25);border:2px solid #2f8cff;padding:14px 30px;border-radius:40px}
.phone{position:relative;margin:34px auto 0;width:430px;height:720px;border-radius:56px;background:#0b0f19;border:3px solid rgba(90,170,255,.8);padding:16px;box-shadow:0 0 60px rgba(40,140,255,.45),inset 0 0 0 2px #1b2433}
.phone .scr{width:100%;height:100%;border-radius:42px;background-size:100% auto;background-position:top center;background-repeat:no-repeat;background-color:#eef3fb}
.phone:before{content:"";position:absolute;top:26px;left:50%;transform:translateX(-50%);width:110px;height:26px;border-radius:20px;background:#0b0f19;z-index:2}
.tag{position:absolute;right:70px;bottom:150px;font-size:20px;font-weight:600;color:#9fb3d6;letter-spacing:1px;background:rgba(10,20,45,.7);padding:8px 16px;border-radius:12px;border:1px solid rgba(90,150,255,.35);text-transform:uppercase}
.row{display:flex;gap:40px;align-items:center;width:100%;margin-top:30px}
.row .phone{margin:0;flex:none;width:400px;height:680px}
.row .list{margin-top:0}
.row .item{font-size:34px;padding:20px 26px}
.laptop{margin:0 auto 0;width:940px}
.laptop .tela{border:3px solid rgba(90,170,255,.8);border-bottom:none;border-radius:28px 28px 0 0;padding:14px;background:#0b0f19;box-shadow:0 0 60px rgba(40,140,255,.4)}
.laptop .tela div{height:520px;border-radius:14px;background-size:100% auto;background-position:top;background-color:#eef3fb}
.laptop .base{height:34px;margin:0 -40px;border-radius:0 0 30px 30px;background:linear-gradient(180deg,#2a3550,#121a2b);border:2px solid rgba(90,170,255,.5)}
""".replace('LOGO', LOGO)

def page(inner, n, total=6, last=False):
    foot = f'<div class="foot"><span>{n}/{total}</span>' + ('<span></span>' if last else '<span class="arrow">ARRASTE ➜</span>') + '</div>'
    return (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="glow"></div>'
            f'<svg class="waves" viewBox="0 0 1080 300" preserveAspectRatio="none">{WAVES}</svg>'
            f'<div class="wrap"><div class="logo"></div>{inner}{foot}</div></body></html>')

def img(f):
    return 'data:image/png;base64,'+base64.b64encode(open('prints_sistema/'+f,'rb').read()).decode()
P1,P2,P3=img('painel-cel.png'),img('analytics-cel.png'),img('painel.png')
TAG='<div class="tag">Imagem ilustrativa</div>'
def phone(src,pos='top'):
    return f'<div class="phone"><div class="scr" style="background-image:url({src});background-position:center {pos}"></div></div>'

slides = [
 # 1 - pergunta de dor
 page('<div class="mid"><div class="kicker">1 GRUPO <b>DÁ. 3 JÁ NÃO.</b></div>'
      '<h2 style="margin-top:34px;font-size:84px"><span class="w">QUANTOS GRUPOS</span><br><span class="w">VOCÊ CONSEGUE</span><br><span class="b">CUIDAR SOZINHO?</span></h2>'
      '<div class="sub">Se você ainda copia oferta grupo por grupo, já sabe a resposta</div></div>', 1),
 # 2 - o sistema cuida de todos
 page('<div class="kicker">O SISTEMA CUIDA <b>DE TODOS</b></div><h2 style="margin-top:14px;font-size:70px"><span class="w">AO MESMO TEMPO</span><br><span class="b">CADA UM NO SEU NICHO</span></h2>'
      '<div class="row">'+phone(P1)+'<div class="list">'
      '<div class="item"><i>🔍</i>Busca as ofertas</div>'
      '<div class="item"><i>✅</i>Escolhe as certas</div>'
      '<div class="item"><i>🚀</i>Posta em cada grupo</div></div></div>'+TAG, 2),
 # 3 - nicho
 page('<div class="kicker">OFERTA CERTA <b>NO GRUPO CERTO</b></div><h2 style="margin-top:14px;font-size:70px"><span class="w">CADA GRUPO</span><br><span class="b">RECEBE O SEU ASSUNTO</span></h2>'
      '<div class="list" style="margin-top:60px">'
      '<div class="item"><i>📱</i>Grupo de eletrônicos</div>'
      '<div class="item"><i>🏠</i>Grupo de casa e cozinha</div>'
      '<div class="item"><i>👗</i>Grupo de moda e beleza</div>'
      '<div class="item"><i>🛒</i>Grupo de achadinhos</div></div>'
      '<div class="sub">O sistema escolhe pelas categorias do seu grupo</div>', 3),
 # 4 - painel por canal
 page('<div class="kicker">TUDO NUM <b>PAINEL SÓ</b></div><h2 style="margin-top:14px;font-size:70px"><span class="w">VOCÊ VÊ DE ONDE</span><br><span class="b">VEM CADA CLIQUE</span></h2>'
      '<div class="row">'+phone(P2,'25%')+'<div class="list">'
      '<div class="item"><i>💬</i>WhatsApp</div>'
      '<div class="item"><i>📸</i>Direct do Instagram</div>'
      '<div class="item"><i>✈️</i>Telegram</div></div></div>'+TAG, 4),
 # 5 - configura uma vez + pergunta
 page('<div class="kicker">CONFIGURA <b>UMA VEZ</b></div><h2 style="margin-top:14px;font-size:70px"><span class="w">DEPOIS ACOMPANHA</span><br><span class="b">DE QUALQUER LUGAR</span></h2>'
      '<div class="sub" style="margin-top:20px">Quantos grupos você cuida hoje? Conta aqui 👇</div>'
      '<div class="laptop"><div class="tela"><div style="background-image:url('+P3+')"></div></div><div class="base"></div></div>'+TAG, 5),
 # 6 - CTA
 page('<div class="mid"><div class="kicker">QUER O SEU <b>RODANDO?</b></div><h2 style="margin-top:30px"><span class="w">TESTE 7 DIAS</span><br><span class="b">GRÁTIS 🚀</span></h2>'
      '<div class="cta">LINK NA BIO</div>'
      '<div class="sub">ou mande “QUERO” no Direct<br><b style="color:#fff">sistemaafiliado.com.br/assinar</b></div></div>', 6, last=True),
]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width':1080,'height':1350})
    for i, html in enumerate(slides, 1):
        pg.set_content(html); pg.wait_for_timeout(400)
        pg.screenshot(path=f'{OUT}/slide{i}.png')
        Image.open(f'{OUT}/slide{i}.png').convert('RGB').save(f'{OUT}/{i:02d}.jpg', quality=88)
        os.remove(f'{OUT}/slide{i}.png')
    b.close()
print('ok')
