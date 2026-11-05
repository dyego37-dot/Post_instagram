import os, subprocess
from PIL import Image
src = open('reel_build.py').read().split('slides = [')[0]
exec(src)
from playwright.sync_api import sync_playwright

slides = [
 rpage('<div class="mid"><div class="kicker">COMEÇAR <b>É MAIS SIMPLES</b></div><h1 style="margin-top:40px"><span class="w">3 PASSOS PARA</span><br><span class="b">COMEÇAR AGORA</span></h1><div class="sub">Do cadastro ao primeiro post automático 👀</div></div>'),
 rpage('<div class="mid"><div class="kicker">PASSO <b>1</b></div><h2 style="margin-top:30px"><span class="w">CRIE SUA CONTA</span><br><span class="b">E TESTE 7 DIAS</span></h2><div class="list"><div class="item"><i>✓</i>Teste grátis de 7 dias</div><div class="item"><i>✓</i>Comece sem complicação</div></div></div>'),
 rpage('<div class="mid"><div class="kicker">PASSO <b>2</b></div><h2 style="margin-top:30px"><span class="w">ESCOLHA ONDE</span><br><span class="b">VAI POSTAR</span></h2><div class="list"><div class="item"><i>✓</i>Seus grupos de WhatsApp</div><div class="item"><i>✓</i>Telegram e Instagram</div></div></div>'),
 rpage('<div class="mid"><div class="kicker">PASSO <b>3</b></div><h2 style="margin-top:30px"><span class="w">ESCOLHA AS LOJAS</span><br><span class="b">QUE VOCÊ QUER</span></h2><div class="stores"><div class="store">SHOPEE</div><div class="store">MERCADO LIVRE</div><div class="store">LOMADEE</div><div class="store">MAGALU</div></div></div>'),
 rpage('<div class="mid"><div class="kicker">DEPOIS <b>É COM O SISTEMA</b></div><h2 style="margin-top:30px"><span class="w">BUSCA E POSTA</span><br><span class="b">24 HORAS</span></h2><div class="list"><div class="item"><i>✓</i>Busca ofertas sozinho</div><div class="item"><i>✓</i>Gera seu link de afiliado</div><div class="item"><i>✓</i>Monta a mensagem e posta</div></div></div>'),
 rpage('<div class="mid"><h2><span class="w">PRONTO PARA</span><br><span class="b">COMEÇAR?</span></h2><div class="cta">MANDE “QUERO” NO DIRECT</div><div class="sub">e receba o link na hora — ou toque no link da bio<br><b style="color:#fff">sistemaafiliado.com.br/assinar</b></div></div>'),
]

D = 'posts/2026-11-06'
os.makedirs(D, exist_ok=True)
story_html = rpage('<div class="mid"><div class="kicker">POST NOVO <b>NO PERFIL 👆</b></div>'
    '<h1 style="margin-top:40px"><span class="w">3 PASSOS PARA</span><br><span class="b">COMEÇAR AGORA</span></h1>'
    '<div class="sub">Do cadastro ao primeiro post automático</div>'
    '<div class="cta">MANDE “QUERO” NO DIRECT</div></div>')
story_html = story_html.replace('padding:160px 70px 220px', 'padding:270px 70px 270px')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for i, h in enumerate(slides, 1):
        pg.set_content(h); pg.wait_for_timeout(300); pg.screenshot(path=f'/home/claude/t{i}.png')
    pg.set_content(story_html); pg.wait_for_timeout(300); pg.screenshot(path='/home/claude/story_raw.png')
    b.close()
Image.open('/home/claude/t1.png').convert('RGB').save(f'{D}/capa_1106.jpg', quality=88)
Image.open('/home/claude/story_raw.png').convert('RGB').save(f'{D}/story_1106.jpg', quality=88)
print('ok')
