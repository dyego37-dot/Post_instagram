import base64, os
from playwright.sync_api import sync_playwright
from PIL import Image

OUT = 'posts/2026-11-23'
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
      '<h1 style="margin-top:40px"><span class="w">VOCÊ TEM MEDO</span><br><span class="w">DE PAGAR</span> <span class="b">E NÃO</span><br><span class="b">VENDER?</span></h1>'
      '<div class="sub">Muita gente fica no grupo sem começar…</div></div>', 1),
 page('<div class="mid"><h2><span class="w">O QUE</span><br><span class="b">PESA NA DECISÃO</span></h2><div class="list">'
      '<div class="item"><i>✓</i>Não saber se a oferta vai sair</div>'
      '<div class="item"><i>✓</i>Ficar pagando sem ver resultado</div>'
      '<div class="item"><i>✓</i>Não ter tempo de testar</div>'
      '<div class="item"><i>✓</i>Medo de jogar dinheiro fora</div></div></div>', 2),
 page('<div class="mid"><h2><span class="w">COMO</span><br><span class="b">FICA MAIS LEVE</span></h2><div class="list">'
      '<div class="item"><i>1</i>Teste grátis de 7 dias</div>'
      '<div class="item"><i>2</i>Você configura uma vez, no começo</div>'
      '<div class="item"><i>3</i>Vê as ofertas saindo no seu grupo</div>'
      '<div class="item"><i>4</i>Decide depois de ver funcionando</div></div></div>', 3),
 page('<div class="mid"><div class="kicker">O PAINEL <b>MOSTRA</b></div><h2 style="margin-top:20px"><span class="w">CADA OFERTA</span><br><span class="b">QUE SAIU</span></h2>'
      '<div class="list"><div class="item"><i>✓</i>Quais grupos receberam</div>'
      '<div class="item"><i>✓</i>De onde vem cada clique</div>'
      '<div class="item"><i>✓</i>Acompanha tudo pelo celular</div></div></div>', 4),
 page('<div class="mid"><div class="kicker">PERGUNTA <b>PRA VOCÊ</b></div><h2 style="margin-top:30px"><span class="w">O QUE MAIS</span><br><span class="b">TE PREOCUPA?</span></h2>'
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
         '<h2 style="margin-top:30px"><span class="w">VOCÊ TEM MEDO</span><br><span class="b">DE PAGAR E NÃO VENDER?</span></h2>'
         '<div class="sub" style="font-size:44px;color:#fff;margin-top:50px">Teste 7 dias e veja funcionando</div>'
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
    pg2.screenshot(path=f'{OUT}/story_1123.png')
    b.close()
Image.open(f'{OUT}/story_1123.png').convert('RGB').save(f'{OUT}/story_1123.jpg', quality=88)
os.remove(f'{OUT}/story_1123.png')
print('ok')
