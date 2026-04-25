## Deploy (Gunicorn + Nginx) e CSS (/static)

Se o site sobe “sem CSS”, quase sempre é porque o servidor/reverse-proxy não está entregando `GET /static/...`.

### 1) Verifique no servidor

- Acesse: `/static/css/index.css`
- Se der `404`, o problema é entrega de estáticos.

### 2) Rodando só com Gunicorn (sem Nginx)

No diretório `principal/`:

```bash
gunicorn -b 0.0.0.0:8000 run:app
```

O Flask já expõe os arquivos estáticos por padrão em `/static`.

### 3) Com Nginx na frente

Opção A (mais simples): encaminhar `/static` para o app (o Flask serve):

```nginx
location /static/ {
  proxy_pass http://127.0.0.1:8000;
  proxy_set_header Host $host;
}

location / {
  proxy_pass http://127.0.0.1:8000;
  proxy_set_header Host $host;
  proxy_set_header X-Forwarded-Proto $scheme;
}
```

Opção B (mais comum): Nginx serve direto do filesystem:

```nginx
location /static/ {
  alias /caminho/para/ProjetoProfessores/principal/app/static/;
  expires 7d;
}

location / {
  proxy_pass http://127.0.0.1:8000;
  proxy_set_header Host $host;
  proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 4) Se estiver atrás de proxy com “prefixo” (ex.: /portal)

Se o app estiver publicado em um subcaminho, ative o `ProxyFix` no servidor:

```bash
export TRUST_PROXY=1
```

E no Nginx passe o prefixo (exemplo):

```nginx
proxy_set_header X-Forwarded-Prefix /portal;
```

Isso ajuda o `url_for()` a montar URLs corretas quando existe prefixo/proxy.

