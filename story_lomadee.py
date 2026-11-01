import os
from PIL import Image
src=open('reel_build.py').read().split('slides = [')[0]
exec(src)
html = rpage('<div class="mid"><div class="kicker">POST NOVO <b>NO PERFIL 👆</b></div>'
 '<h1 style="margin-top:40px"><span class="w">VOCÊ JÁ CONHECE</span><br><span class="b">A LOMADEE?</span></h1>'
 '<div class="sub">Uma conta só, mais de 300 marcas cadastradas</div>'
 '<div class="cta">MANDE “QUERO” NO DIRECT</div></div>')
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.set_content(html); pg.wait_for_timeout(300); pg.screenshot(path='/tmp/s.png'); b.close()
Image.open('/tmp/s.png').convert('RGB').save('posts/2026-11-03/story_1103.jpg', quality=88)
print('ok')
