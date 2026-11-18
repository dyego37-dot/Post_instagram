import base64, os
from playwright.sync_api import sync_playwright
from PIL import Image

OUT = 'posts/2026-11-19'
os.makedirs(OUT, exist_ok=True)
LOGO = 'data:image/png;base64,' + base64.b64encode(open('logo_t.png','rb').read()).decode()
WAVES = ''.join(
    f'<path d="M0 {120+i*6} C 270 {40+i*9}, 540 {200-i*7}, 810 {110+i*4} S 1080 {60+i*8}, 1080 {90+i*5}" '
    f'stroke="rgba(47,140,255,{0.10+i*0.012})" stroke-width="1.6" fill="none"/>' for i in range(16))
CSS = open('build.py').read().split('CSS = """')[1].split('""".replace')[0].replace('LOGO', LOGO)

def page(inner, n, total=6, last=False):
    foot = f'<div class="foot"><span>{n}/{total}</span>' + ('<span></span>' if last else '<span class="arrow">ARRASTE ➜</span>') + '</div>'
    return (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="glow"></div>'
            f'<svg class="waves" viewBox="0 0 1080 300" preserveAspectRatio="none">{WAVES}</svg>'
            f'<div class="wrap"><div class="logo"></div>{inner}{foot}</div></body></html>')

slides = [
 page('<div class="mid"><div class="kicker">VOCÊ TEM <b>MEDO?</b></div>'
      '<h1 style="margin-top:40px"><span class="w">VOCÊ TEM MEDO</span><br><span class="w">DE</span> <span class="b">CONFIGURAR</span><br><span class="b">E ERRAR?</span></h1>'
      '<div class="sub">Muita gente nem começa por causa disso…</div></div>', 1),
 page('<div class="mid"><h2><span class="w">O QUE</span><br><span class="b">ASSUSTA</span></h2><div class="list">'
      '<div class="item"><i>✓</i>Medo de mexer e estragar tudo</div>'
      '<div class="item"><i>✓</i>Medo de postar oferta errada</div>'
      '<div class="item"><i>✓</i>Achar que precisa saber de tecnologia</div>'
      '<div class="item"><i>✓</i>Medo de perder tempo sem resultado</div></div></div>', 2),
 page('<div class="mid"><h2><span class="w">É MAIS SIMPLES</span><br><span class="b">DO QUE PARECE</span></h2><div class="list">'
      '<div class="item"><i>1</i>Configuração feita uma vez, no começo</div>'
      '<div class="item"><i>2</i>Passo a passo do cadastro à primeira oferta</div>'
      '<div class="item"><i>3</i>Vídeos de como conectar cada canal</div>'
      '<div class="item"><i>4</i>Você não precisa programar nada</div></div></div>', 3),
 page('<div class="mid"><div class="kicker">DEPOIS <b>DA CONFIGURAÇÃO</b></div><h2 style="margin-top:20px"><span class="w">O SISTEMA</span><br><span class="b">FAZ O RESTO</span></h2>'
      '<div class="list"><div class="item"><i>✓</i>Busca as ofertas e gera seu link</div>'
      '<div class="item"><i>✓</i>Confere se o produto ainda está na loja</div>'
      '<div class="item"><i>✓</i>Posta nos seus grupos 24h</div>'
      '<div class="item"><i>✓</i>Você acompanha pelo celular</div></div></div>', 4),
 page('<div class="mid"><div class="kicker">PERGUNTA <b>PRA VOCÊ</b></div><h2 style="margin-top:30px"><span class="w">QUAL PARTE</span><br><span class="b">TE DÁ MAIS MEDO?</span></h2>'
      '<div class="sub">Conta aqui nos comentários 👇</div></div>', 5),
 page('<div class="mid"><div class="kicker">TESTE <b>7 DIAS GRÁTIS</b></div><h2 style="margin-top:30px"><span class="w">TESTE 7 DIAS GRÁTIS</span><br><span class="b">LINK NA BIO</span></h2>'
      '<div class="cta">MANDE “QUERO” NO DIRECT</div>'
      '<div class="sub">ou acesse<br><b style="color:#fff">sistemaafiliado.com.br/assinar</b></div></div>', 6, last=True),
]

story_css = CSS + """
body{height:1920px}
.wrap{padding:270px 70px 270px!important}
.logo{width:380px;height:250px}
h2{font-size:92px}
"""
story = (f'<html><head><meta charset="utf-8"><style>{story_css}</style></head><body><div class="glow"></div>'
         f'<svg class="waves" viewBox="0 0 1080 300" preserveAspectRatio="none">{WAVES}</svg>'
         f'<div class="wrap"><div class="logo"></div><div class="mid"><div class="kicker">AFILIADO, <b>ATENÇÃO</b></div>'
         '<h2 style="margin-top:30px"><span class="w">VOCÊ TEM MEDO</span><br><span class="b">DE CONFIGURAR?</span></h2>'
         '<div class="sub" style="font-size:44px;color:#fff;margin-top:50px">Configura uma vez e o sistema posta sozinho</div>'
         '<div class="sub" style="font-size:40px;margin-top:70px;color:#9fd0ff">POST NOVO NO PERFIL 👆</div>'
         '<div class="sub" style="font-size:40px;margin-top:40px;color:#fff;font-weight:700">TESTE 7 DIAS GRÁTIS — LINK NA BIO</div></div></div></body></html>')

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1080,'height':1350})
    for i, html in enumerate(slides, 1):
        pg.set_content(html); pg.wait_for_timeout(300)
        tmp = f'{OUT}/slide{i}.png'
        pg.screenshot(path=tmp)
        Image.open(tmp).convert('RGB').save(f'{OUT}/{i:02d}.jpg', quality=88)
        os.remove(tmp)
    pg2 = b.new_page(viewport={'width':1080,'height':1920})
    pg2.set_content(story); pg2.wait_for_timeout(300)
    pg2.screenshot(path=f'{OUT}/story_1119.png')
    b.close()
Image.open(f'{OUT}/story_1119.png').convert('RGB').save(f'{OUT}/story_1119.jpg', quality=88)
os.remove(f'{OUT}/story_1119.png')
print('ok')
