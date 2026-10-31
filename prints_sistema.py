import sys
from playwright.sync_api import sync_playwright
S='.'; import os, json
NUM=json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
B='https://dmb.sistemaafiliado.com.br/wp-admin/admin.php?page='
LIMPA=r'''()=>{
 document.querySelectorAll('img.emoji').forEach(i=>i.replaceWith(document.createTextNode(i.alt)));
 const tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=tw.nextNode()){n.nodeValue=n.nodeValue.replace(/Ofertas de Dyego de melo Barbosa/g,'Minhas Ofertas').replace(/Olá, joao/g,'Olá!')}
 document.querySelectorAll('.oa-aviso-info,[class*=oaa-ren],.oa-duas-colunas,#wp-admin-bar-my-account').forEach(e=>e.style.display='none');
 [...document.querySelectorAll('#wpbody-content *')].forEach(e=>{const t=(e.innerText||'').trim();
   if(/^(Meu plano|\d+ configurações pendentes)/.test(t)&&t.length<120)e.style.display='none'});
 document.querySelectorAll('.oa-colunas-auto > *').forEach(e=>{if(/Conecte a Shopee ou a Lomadee|Precisa recomeçar/.test(e.innerText)&&!/De onde vieram/.test(e.innerText))e.style.display='none'});
 document.querySelectorAll('canvas').forEach(cv=>{const box=cv.closest('.oa-box,.oa-card-grafico,.oa-colunas-auto > *');if(box&&!/De onde vieram/.test(box.innerText))box.style.display='none'});
 document.querySelectorAll('*').forEach(e=>{const cs=getComputedStyle(e);if(cs.position==='fixed'&&e.offsetWidth<100&&e.offsetHeight<200&&!e.closest('#wpadminbar'))e.style.display='none'});
 document.querySelectorAll('#wp-admin-bar-root-default > li').forEach(li=>{if(/Renovar/.test(li.innerText))li.style.display='none'});
}'''
DASH=NUM.get('painel',['186','42','12','58','214','9'])
def grafico(pg, series):
    pg.evaluate('''(series)=>{const cs=[...document.querySelectorAll('canvas')];
      cs.forEach((cv,i)=>{const ch=window.Chart&&Chart.getChart?Chart.getChart(cv):null; if(!ch||!series[i])return;
        ch.data.datasets.forEach((d,j)=>{d.data=series[i][j%series[i].length]}); ch.update('none');})}''', series)

def entrar(b):
    c=b.new_context(); pg=c.new_page()
    pg.goto('https://dmb.sistemaafiliado.com.br/wp-login.php')
    pg.fill('#user_login',os.environ['DMB_USER']); pg.fill('#user_pass',os.environ['DMB_PASS']); pg.click('#wp-submit')
    pg.wait_for_load_state('networkidle')
    if 'wp-login' in pg.url: raise SystemExit('LOGIN FALHOU: usuario/senha errados ou site pausado')
    c.storage_state(path=S+'/prints_sistema/state.json'); c.close()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    os.makedirs(S+'/prints_sistema',exist_ok=True); entrar(b)
    for vw,suf in [((1366,900),''),((412,900),'-cel')]:
        c=b.new_context(viewport={'width':vw[0],'height':vw[1] if vw[0]>500 else 1100}, device_scale_factor=2, locale='pt-BR', storage_state=S+'/prints_sistema/state.json')
        pg=c.new_page(); pg.route('**/s.w.org/**', lambda r: r.abort()); pg.route('**/wp-emoji*', lambda r: r.abort()); pg.route('**/gravatar.com/**', lambda r: r.abort())
        # Dashboard
        pg.goto(B+'oferta-automatica', wait_until='networkidle'); pg.wait_for_timeout(1500); pg.evaluate(LIMPA)
        pg.evaluate('''(v)=>{const n=document.querySelectorAll('.oa-card-numero');v.slice(0,6).forEach((x,i)=>{if(n[i])n[i].textContent=x});
          if(n[6])n[6].innerHTML='<small>R$</small>'+v[6]; if(n[7])n[7].textContent='0';}''', DASH+[NUM.get('comissao','47,30')])
        grafico(pg, [[[2,3,4,3,5,4,6,4,5,4,5,4,4,5]],[[6,9,11,8,14,12,17,15,13,19,16,21,18,23]]])
        pg.wait_for_timeout(800); pg.screenshot(path=f'{S}/prints_sistema/painel{suf}.png', full_page=False)
        # Analytics
        pg.goto(B+'oa-analytics', wait_until='networkidle'); pg.wait_for_timeout(1500); pg.evaluate(LIMPA)
        pg.evaluate('''()=>{const n=document.querySelectorAll('.oa-card-numero');['214','9','R$ 47,30','R$ 31,80'].forEach((x,i)=>{if(n[i])n[i].textContent=x});
          const vals={'Site':0,'Telegram':47,'WhatsApp':96,'Instagram':71};
          document.querySelectorAll('strong').forEach(s=>{if(s.style.width!=='50px')return;const row=s.parentElement;const t=row.innerText;
            for(const k in vals){if(t.includes(k)){s.textContent=vals[k];const bar=[...row.querySelectorAll('div')].find(d=>d.children.length===1&&d.firstElementChild.tagName==='DIV');
              if(bar){bar.firstElementChild.style.width=(vals[k]/96*100)+'%';bar.firstElementChild.style.minWidth='0';}}}})}''')
        grafico(pg, [[[2,3,4,3,5,4,6,4,5,4,5,4,4,5],[6,9,11,8,14,12,17,15,13,19,16,21,18,23],[0,1,0,0,1,0,1,0,2,0,1,1,0,2]]])
        pg.wait_for_timeout(800); pg.screenshot(path=f'{S}/prints_sistema/analytics{suf}.png', full_page=False)
        c.close()
    b.close()

from PIL import Image
for f,h in [('painel-cel.png',1840),('analytics-cel.png',1780)]:
    im=Image.open(S+'/prints_sistema/'+f); im.crop((0,0,im.width,h)).save(S+'/prints_sistema/'+f)
print('prints ok')
