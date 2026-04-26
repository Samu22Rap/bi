# BI Dashboard — Loja de Roupas Omnichannel

Dashboard acadêmico em Streamlit conectado ao Supabase.
Dados sintéticos para fins de estudo.

## Deploy em 5 passos

### 1. Criar projeto no Supabase
1. Acesse [supabase.com](https://supabase.com) e crie uma conta gratuita
2. Clique em **New Project** → escolha um nome e senha
3. Aguarde o projeto inicializar (~2 min)
4. Vá em **Project Settings → API** e copie:
   - `Project URL`  →  será o `SUPABASE_URL`
   - `anon public`  →  será o `SUPABASE_KEY`

### 2. Popular o banco
1. No painel do Supabase, clique em **SQL Editor → New Query**
2. Abra o arquivo `sql/setup.sql` deste projeto
3. Cole todo o conteúdo no editor e clique em **Run**
4. Confirme que as tabelas aparecem em **Table Editor**

### 3. Subir o código no GitHub
```bash
git init
git add .
git commit -m "BI Dashboard Omnichannel"
git remote add origin https://github.com/SEU_USUARIO/bi-dashboard.git
git push -u origin main
```

### 4. Deploy no Streamlit Cloud (gratuito)
1. Acesse [share.streamlit.io](https://share.streamlit.io) com sua conta GitHub
2. Clique em **New app**
3. Selecione seu repositório e o arquivo `app.py`
4. Vá em **Advanced settings → Secrets** e adicione:
```toml
SUPABASE_URL = "https://xxxxxxxxxxxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```
5. Clique em **Deploy** — em ~1 minuto o link estará ativo

### 5. Testar localmente (opcional)
```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edite secrets.toml com suas credenciais reais
streamlit run app.py
```

## Estrutura do projeto
```
bi_dashboard/
├── app.py                        # App principal
├── requirements.txt              # Dependências Python
├── .streamlit/
│   ├── config.toml               # Tema e configurações
│   └── secrets.toml.example      # Template de credenciais
└── sql/
    └── setup.sql                 # Script de criação das tabelas
```

## Páginas do dashboard
| Página | Conteúdo |
|---|---|
| 📈 Executivo | KPIs globais, receita mensal, gauge de conversão |
| 📣 Marketing | CAC por canal, ROI por campanha, ranking |
| 👗 Produtos | Receita por categoria, margem, descontos |
| 👥 Clientes | Perfil, faixa de renda, UF, fidelidade |
| 🔍 Diagnóstico | Funil de conversão, análise por dispositivo, suporte |
