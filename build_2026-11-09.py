import base64, os
from playwright.sync_api import sync_playwright
from PIL import Image

OUT = 'posts/2026-11-09'
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
 page('<div class="mid"><div class="kicker">AFILIADO, <b>PRESTA ATENÇÃO</b></div>'
      '<h1 style="margin-top:40px"><span class="w">VOCÊ MANDA LINK</span><br><span class="b">QUE NÃO ABRE?</span></h1>'
      '<div class="sub">Clique perdido é venda que não volta…</div></div>', 1),
 page('<div class="mid"><h2><span class="w">O CLIENTE CLICA</span><br><span class="b">E DÁ DE CARA COM…</span></h2><div class="list">'
      '<div class="item x"><i>✕</i>Produto esgotado</div>'
      '<div class="item x"><i>✕</i>Produto que saiu da loja</div>'
      '<div class="item x"><i>✕</i>Página de erro</div></div>'
      '<div class="sub">Ele fecha a tela e <b style="color:#fff">não compra mais.</b></div></div>', 2),
 page('<div class="mid"><div class="kicker">ANTES DE <b>POSTAR</b></div><h2 style="margin-top:20px"><span class="w">O SISTEMA</span><br><span class="b">CONFERE PRA VOCÊ</span></h2><div class="list">'
      '<div class="item"><i>✓</i>Vê se o produto ainda está na loja</div>'
      '<div class="item"><i>✓</i>Não manda oferta morta</div>'
      '<div class="item"><i>✓</i>Gera o seu link de afiliado</div></div></div>', 3),
 page('<div class="mid"><h2><span class="w">VOCÊ DECIDE</span><br><span class="b">ONDE POSTAR</span></h2><div class="list">'
      '<div class="item"><i>1</i>Em quais grupos postar</div>'
      '<div class="item"><i>2</i>Quais lojas entram</div>'
      '<div class="item"><i>3</i>Quando você quer acompanhar</div></div>'
      '<div class="sub">Você escolhe. O sistema executa, 24h.</div></div>', 4),
 page('<div class="mid"><div class="kicker">PARA <b>PENSAR</b></div><h2 style="margin-top:30px"><span class="w">QUANTA VENDA</span><br><span class="b">VOCÊ JÁ PERDEU ASSIM?</span></h2>'
      '<div class="sub" style="font-size:44px">Conta aqui nos comentários 👇</div></div>', 5),
 page('<div class="mid"><div class="kicker">TESTE <b>GRÁTIS</b> POR 7 DIAS</div><h2 style="margin-top:30px"><span class="w">PARE DE POSTAR</span><br><span class="b">LINK MORTO.</span></h2>'
      '<div class="cta">TESTE 7 DIAS GRÁTIS</div>'
      '<div class="sub">LINK NA BIO — ou mande “QUERO” no Direct<br><b style="color:#fff">sistemaafiliado.com.br/assinar</b></div></div>', 6, last=True),
]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1080,'height':1350})
    for i, html in enumerate(slides, 1):
        pg.set_content(html); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{OUT}/slide{i}.png')
        Image.open(f'{OUT}/slide{i}.png').convert('RGB').save(f'{OUT}/{i:02d}.jpg', quality=88)
        os.remove(f'{OUT}/slide{i}.png')
    b.close()
print('ok carrossel')
