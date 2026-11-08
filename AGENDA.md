# Agenda de posts do @sistemaafiliados

O plugin **Agendador de Posts** (instalado em sistemaafiliado.com.br) lê o arquivo `agenda.json`
a cada 5 minutos, baixa as mídias para o site e publica no Instagram e no Facebook na hora marcada.
Substitui o Metricool (o plano grátis só publica 20 por mês).

## Formato

```json
{
  "fuso": "America/Sao_Paulo",
  "posts": [
    {
      "id": "2026-11-09-1900-tirinha-mae-filha",
      "quando": "2026-11-09 19:00",
      "tipo": "carrossel",
      "redes": ["instagram", "facebook"],
      "titulo": "Nome curto que aparece no painel",
      "legenda": "Texto do post…",
      "midias": ["posts/2026-11-09-tirinha/01.jpg", ["posts/x.jpg", "https://outro-endereco/x.jpg"]],
      "capa": "posts/…/capa.jpg",
      "colaboradores": ["futeboll_totall"],
      "cancelado": false
    }
  ]
}
```

- `id`: único e nunca reaproveitado (o plugin usa para não publicar duas vezes).
- `quando`: hora de Brasília (`AAAA-MM-DD HH:MM`).
- `tipo`: `imagem`, `carrossel`, `reel` ou `story` (story sem legenda; imagem ou vídeo).
- `midias`: caminho dentro deste repositório ou endereço completo. Uma lista dentro da lista
  são alternativas: tenta a primeira, se não baixar usa a seguinte.
- `capa`: só para Reels (opcional).
- `colaboradores`: até 3 contas convidadas como colaboradoras (não vale para story).
- `cancelado: true`: não publica.
- Mudanças num post que ainda não saiu são aplicadas sozinhas; depois de publicado, mudar não faz nada.
- Post que passar de 12 horas do horário sem sair não é publicado sozinho (aparece como
  "Passou do horário" no painel, com o botão "Publicar agora").
