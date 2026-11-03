import os
from PIL import Image
src = open('reel_build.py').read().split('slides = [')[0]
exec(src)
from playwright.sync_api import sync_playwright

slides = [
 rpage('<div class="mid"><div class="kicker">SEU GRUPO <b>PAROU?</b></div><h1 style="margin-top:40px"><span class="w">O GRUPO DE OFERTAS</span><br><span class="b">ESFRIA EM SILÊNCIO</span></h1><div class="sub">Três dicas para ele voltar a vender 👀</div></div>'),
 rpage('<div class="mid"><div class="kicker">DICA <b>1</b></div><h2 style="margin-top:30px"><span class="w">POSTE NO MESMO</span><br><span class="b">HORÁRIO</span></h2><div class="list"><div class="item"><i>✓</i>Membro aprende quando abrir</div><div class="item"><i>✓</i>Hábito faz o grupo voltar</div></div></div>'),
 rpage('<div class="mid"><div class="kicker">DICA <b>2</b></div><h2 style="margin-top:30px"><span class="w">MENSAGEM CURTA</span><br><span class="b">COM PREÇO E LINK</span></h2><div class="list"><div class="item"><i>✓</i>Produto, preço e link</div><div class="item"><i>✓</i>Sem texto que enrola</div></div></div>'),
 rpage('<div class="mid"><div class="kicker">DICA <b>3</b></div><h2 style="margin-top:30px"><span class="w">DEIXE O REPETIDO</span><br><span class="b">COM O SISTEMA</span></h2><div class="list"><div class="item"><i>✓</i>Busca ofertas sozinho</div><div class="item"><i>✓</i>Gera seu link de afiliado</div><div class="item"><i>✓</i>Posta no grupo 24h</div></div></div>'),
 rpage('<div class="mid"><div class="kicker">NA <b>PRÁTICA</b></div><h2 style="margin-top:30px"><span class="w">VOCÊ CUIDA</span><br><span class="b">DA COMUNIDADE</span></h2><div class="list"><div class="item x"><i>✕</i>Garimpar oferta na mão</div><div class="item"><i>✓</i>Acompanhar e responder</div></div></div>'),
 rpage('<div class="mid"><h2><span class="w">QUER SEU GRUPO</span><br><span class="b">VENDENDO TODO DIA?</span></h2><div class="cta">MANDE “QUERO” NO DIRECT</div><div class="sub">e receba o link na hora — ou toque no link da bio<br><b style="color:#fff">sistemaafiliado.com.br/assinar</b></div></div>'),
]

os.makedirs('posts/2026-11-04', exist_ok=True)
D = 'posts/2026-11-04'
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for i, h in enumerate(slides, 1):
        pg.set_content(h); pg.wait_for_timeout(300); pg.screenshot(path=f'/home/claude/t{i}.png')
    # story: same model, CTA + "post novo"
    html = rpage('<div class="mid"><div class="kicker">POST NOVO <b>NO PERFIL 👆</b></div>'
        '<h1 style="margin-top:40px"><span class="w">SEU GRUPO DE OFERTAS</span><br><span class="b">ESTÁ PARADO?</span></h1>'
        '<div class="sub">Três dicas para ele voltar a vender</div>'
        '<div class="cta">MANDE “QUERO” NO DIRECT</div></div>')
    pg.set_content(html); pg.wait_for_timeout(300); pg.screenshot(path='/home/claude/story_raw.png')
    b.close()
Image.open('/home/claude/t1.png').convert('RGB').save(f'{D}/capa_1104.jpg', quality=88)
Image.open('/home/claude/story_raw.png').convert('RGB').save(f'{D}/story_1104.jpg', quality=88)
print('ok')
