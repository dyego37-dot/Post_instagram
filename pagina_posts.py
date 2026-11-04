#!/usr/bin/env python3
"""Monta as miniaturas dos posts para a página "Posts do @sistemaafiliados".

Uso: python3 pagina_posts.py PASTA_DE_SAIDA [dias]
Gera PASTA_DE_SAIDA/p/AAAA-MM-DD/*.jpg (miniaturas de 720 px) e p/index.json
com os últimos `dias` dias (padrão 21) e todos os futuros.
"""
import json, os, re, sys, datetime
from PIL import Image

REPO = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1]
dias = int(sys.argv[2]) if len(sys.argv) > 2 else 21
limite = (datetime.date.today() - datetime.timedelta(days=dias)).isoformat()
index = {}
for d in sorted(os.listdir(os.path.join(REPO, "posts"))):
    m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})(-tirinha)?", d)
    if not m or m.group(1) < limite:
        continue
    dia, tarde = m.group(1), bool(m.group(2))
    src = os.path.join(REPO, "posts", d)
    imgs = sorted(f for f in os.listdir(src) if f.lower().endswith((".jpg", ".jpeg", ".png")))
    story = [f for f in imgs if f.lower().startswith("story")]
    capa = [f for f in imgs if f.lower().startswith("capa")]
    telas = [f for f in imgs if f not in story and f not in capa]
    reel = any(f.lower().endswith(".mp4") for f in os.listdir(src))
    post = capa if (reel and capa) else telas or capa
    os.makedirs(os.path.join(out, "p", d), exist_ok=True)
    if tarde:
        # tirinha das 19h: todas as imagens vão para "tarde" do dia
        def mini2(f):
            nome = os.path.splitext(f)[0] + ".jpg"
            im = Image.open(os.path.join(src, f)).convert("RGB")
            im.thumbnail((720, 1280))
            im.save(os.path.join(out, "p", d, nome), "JPEG", quality=80)
            return f"p/{d}/{nome}"
        index.setdefault(dia, {"post": [], "story": [], "reel": False})["tarde"] = [mini2(f) for f in imgs]
        continue
    def mini(f):
        nome = os.path.splitext(f)[0] + ".jpg"
        im = Image.open(os.path.join(src, f)).convert("RGB")
        im.thumbnail((720, 1280))
        im.save(os.path.join(out, "p", d, nome), "JPEG", quality=80)
        return f"p/{d}/{nome}"
    index.setdefault(dia, {}).update({"post": [mini(f) for f in post], "story": [mini(f) for f in story], "reel": reel})
with open(os.path.join(out, "p", "index.json"), "w") as fh:
    json.dump(index, fh)
print(json.dumps({d: {k: len(v) if isinstance(v, list) else v for k, v in x.items()} for d, x in index.items()}))
