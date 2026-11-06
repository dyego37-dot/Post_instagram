import base64, os
from playwright.sync_api import sync_playwright

OUT = 'posts/2026-11-07'
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
 page('<div class="mid"><div class="kicker">AFILIADO, <b>SEM MISTÉRIO</b></div>'
      '<h1 style="margin-top:40px"><span class="w">O QUE O SISTEMA</span><br><span class="b">FAZ SOZINHO?</span></h1>'
      '<div class="sub">E o que ainda fica com você…</div></div>', 1),
 page('<div class="mid"><h2><span class="w">SOZINHO ELE</span><br><span class="b">FAZ ISSO</span></h2><div class="list">'
      '<div class="item"><i>✓</i>Busca as ofertas nas lojas</div>'
      '<div class="item"><i>✓</i>Gera o seu link de afiliado</div>'
      '<div class="item"><i>✓</i>Monta a mensagem pronta</div>'
      '<div class="item"><i>✓</i>Posta nos seus grupos 24h</div></div></div>', 2),
 page('<div class="mid"><h2><span class="w">QUEM DECIDE</span><br><span class="b">É VOCÊ</span></h2><div class="list">'
      '<div class="item"><i>1</i>Em quais grupos postar</div>'
      '<div class="item"><i>2</i>Quais lojas entram</div>'
      '<div class="item"><i>3</i>Quando você quer acompanhar</div></div>'
      '<div class="sub">Você escolhe. O sistema executa.</div></div>', 3),
 page('<div class="mid"><div class="kicker">SEM <b>PROGRAMAÇÃO</b></div><h2 style="margin-top:20px"><span class="w">TUDO NUM</span><br><span class="b">PAINEL SÓ</span></h2>'
      '<div class="list"><div class="item"><i>✓</i>Ofertas encontradas</div>'
      '<div class="item"><i>✓</i>O que já foi postado</div>'
      '<div class="item"><i>✓</i>Acompanha pelo celular</div></div></div>', 4),
 page('<div class="mid"><div class="kicker">ANTES DE <b>DECIDIR</b></div><h2 style="margin-top:30px"><span class="w">TESTE O SISTEMA</span><br><span class="b">GRÁTIS POR 7 DIAS</span></h2>'
      '<div class="sub">Depois você vê se faz sentido pra você</div></div>', 5),
 page('<div class="mid"><div class="kicker">TRANSFORME <b>CLIQUES EM VENDAS</b></div><h2 style="margin-top:30px"><span class="w">PARE DE GARIMPAR.</span><br><span class="b">DEIXE O SISTEMA POSTAR.</span></h2>'
      '<div class="cta">MANDE “QUERO” NO DIRECT</div>'
      '<div class="sub">e receba o link na hora — ou toque no link da bio<br><b style="color:#fff">sistemaafiliado.com.br/assinar</b></div></div>', 6, last=True),
]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1080,'height':1350})
    for i, html in enumerate(slides, 1):
        pg.set_content(html); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{OUT}/slide{i}.png')
        from PIL import Image
        Image.open(f'{OUT}/slide{i}.png').convert('RGB').save(f'{OUT}/{i:02d}.jpg', quality=88)
        os.remove(f'{OUT}/slide{i}.png')
    b.close()
print('ok')
