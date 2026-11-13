import json, subprocess, sys, os
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__))
OFF={1:0,2:3.1,3:11.0,4:16.6}
FIX={'Chopin,':'Shopee,','Coupon,':'Cupom,','Fryer?':'fryer?','enche.':'encha.'}
pal=json.load(open(f'{D}/palavras.json'));caps=[]
for k,ws in pal.items():
    o=OFF[int(k)];cur=[]
    for w,a,b in ws:
        w=FIX.get(w,w);txt=' '.join(x[0] for x in cur)
        if cur and (len(txt)+len(w)>18 or cur[-1][0][-1] in '.?!' or (cur[-1][0][-1]==',' and len(txt)>=8)):caps.append(cur);cur=[]
        cur.append([w,a+o,b+o])
    caps.append(cur)
CAPS=[{'a':c[0][1],'b':min(caps[i+1][0][1] if i+1<len(caps) else 1e9,c[-1][2]+.5),'w':[[w,a] for w,a,b in c]} for i,c in enumerate(caps)]
DUR=22.0;FPS=30;versao=sys.argv[1];saida=sys.argv[2];so=[float(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else None
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto(f'file://{D}/ach.html');pg.wait_for_timeout(800);pg.evaluate('([c,v])=>{CAPS=c;VERSAO=v}',[CAPS,versao])
    if so:
        for t in so:pg.evaluate(f'render({t})');pg.screenshot(path=f'{D}/prev_{t}.jpg',type='jpeg',quality=80)
        sys.exit()
    ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',saida],stdin=subprocess.PIPE)
    for f in range(int(DUR*FPS)):
        pg.evaluate(f'render({f/FPS})');ff.stdin.write(pg.screenshot(type='jpeg',quality=92))
    ff.stdin.close();ff.wait()
print('ok',saida)
