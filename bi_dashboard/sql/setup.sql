-- =============================================================================
-- BI Loja de Roupas Omnichannel — Setup Supabase
-- Execute este script no SQL Editor do seu projeto Supabase
-- Todos os dados são sintéticos para fins acadêmicos
-- =============================================================================

-- ── 1. TABELA: kpis_resumo ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS kpis_resumo (
  indicador       TEXT PRIMARY KEY,
  valor           NUMERIC,
  unidade         TEXT,
  meta            NUMERIC,
  status          TEXT   -- 'ok' | 'alert' | 'neutral'
);

ALTER TABLE kpis_resumo ENABLE ROW LEVEL SECURITY;
CREATE POLICY "leitura_publica" ON kpis_resumo FOR SELECT USING (true);

INSERT INTO kpis_resumo VALUES
  ('receita_total',          2245955.61, 'BRL',    NULL,       'neutral'),
  ('pedidos',                6778,       'unid',   NULL,       'neutral'),
  ('sessoes',                254578,     'unid',   NULL,       'neutral'),
  ('taxa_conversao',         2.66,       '%',      3.06,       'alert'),
  ('cac',                    141.82,     'BRL',    113.46,     'alert'),
  ('ticket_medio',           331.36,     'BRL',    NULL,       'ok'),
  ('roi_marketing',          3.69,       'x',      NULL,       'ok'),
  ('investimento_marketing', 156143.10,  'BRL',    NULL,       'neutral'),
  ('novos_clientes',         1101,       'unid',   NULL,       'neutral'),
  ('clientes_cadastrados',   1500,       'unid',   NULL,       'neutral')
ON CONFLICT (indicador) DO UPDATE
  SET valor = EXCLUDED.valor, meta = EXCLUDED.meta, status = EXCLUDED.status;


-- ── 2. TABELA: receita_mensal ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS receita_mensal (
  mes                     TEXT PRIMARY KEY,
  mes_num                 INT,
  receita                 NUMERIC,
  pedidos                 INT,
  sessoes                 INT,
  taxa_conversao          NUMERIC,
  investimento_marketing  NUMERIC,
  novos_clientes          INT,
  ticket_medio            NUMERIC
);

ALTER TABLE receita_mensal ENABLE ROW LEVEL SECURITY;
CREATE POLICY "leitura_publica" ON receita_mensal FOR SELECT USING (true);

INSERT INTO receita_mensal VALUES
  ('Jan/25', 1, 318420.50,  980,  37800, 2.59, 23850.00, 162, 324.92),
  ('Fev/25', 2, 352180.30, 1040,  40200, 2.59, 24600.00, 178, 338.63),
  ('Mar/25', 3, 386740.90, 1112,  42350, 2.63, 26200.00, 188, 347.79),
  ('Abr/25', 4, 394210.70, 1145,  43500, 2.63, 26800.00, 192, 344.29),
  ('Mai/25', 5, 408630.40, 1198,  45128, 2.66, 27400.00, 196, 341.09),
  ('Jun/25', 6, 385773.81, 1303,  45600, 2.86, 27293.10, 185, 296.07)
ON CONFLICT (mes) DO UPDATE
  SET receita = EXCLUDED.receita, pedidos = EXCLUDED.pedidos,
      sessoes = EXCLUDED.sessoes, taxa_conversao = EXCLUDED.taxa_conversao,
      investimento_marketing = EXCLUDED.investimento_marketing,
      novos_clientes = EXCLUDED.novos_clientes, ticket_medio = EXCLUDED.ticket_medio;


-- ── 3. TABELA: cac_por_canal ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cac_por_canal (
  canal           TEXT PRIMARY KEY,
  investimento    NUMERIC,
  novos_clientes  INT,
  cac             NUMERIC,
  roi             NUMERIC
);

ALTER TABLE cac_por_canal ENABLE ROW LEVEL SECURITY;
CREATE POLICY "leitura_publica" ON cac_por_canal FOR SELECT USING (true);

INSERT INTO cac_por_canal VALUES
  ('Meta Ads',       65280.40, 380, 171.79, 2.84),
  ('Google Ads',     47920.30, 285, 168.14, 3.12),
  ('Influenciadores', 20480.10,  98, 209.00, 2.40),
  ('Direto',              0.00,  56,   0.00, 0.00),
  ('E-mail',          8970.20, 138,  65.00, 7.20),
  ('Orgânico',        13492.10, 144,  93.70, 5.80)
ON CONFLICT (canal) DO UPDATE
  SET investimento = EXCLUDED.investimento, novos_clientes = EXCLUDED.novos_clientes,
      cac = EXCLUDED.cac, roi = EXCLUDED.roi;


-- ── 4. TABELA: roi_por_campanha ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS roi_por_campanha (
  campanha           TEXT PRIMARY KEY,
  plataforma         TEXT,
  investimento       NUMERIC,
  receita_atribuida  NUMERIC,
  novos_clientes     INT,
  roi                NUMERIC,
  cac                NUMERIC
);

ALTER TABLE roi_por_campanha ENABLE ROW LEVEL SECURITY;
CREATE POLICY "leitura_publica" ON roi_por_campanha FOR SELECT USING (true);

INSERT INTO roi_por_campanha VALUES
  ('E-mail Base Fidelidade', 'E-mail',       3240.50,  26640.90, 52, 7.22,  62.32),
  ('Orgânico SEO Blog',      'Orgânico',     2100.00,  16182.00, 44, 6.71,  47.73),
  ('Meta Retargeting',       'Meta Ads',    14820.30,  80230.80, 88, 4.41, 168.41),
  ('Google Shopping',        'Google Ads',  18420.00,  82890.00, 98, 3.50, 187.96),
  ('Meta Prospecting',       'Meta Ads',    22340.80,  78193.48,145, 2.50, 154.07),
  ('Google Search Brand',    'Google Ads',   9820.00,  27496.00, 62, 1.80, 158.39),
  ('Influenciadores',        'Influenc.',   20480.10,  49152.24, 98, 1.40, 209.00),
  ('Display Retargeting',    'Google Ads',  19680.30,  32271.69, 125, 0.64, 157.44)
ON CONFLICT (campanha) DO UPDATE
  SET plataforma = EXCLUDED.plataforma, investimento = EXCLUDED.investimento,
      receita_atribuida = EXCLUDED.receita_atribuida, novos_clientes = EXCLUDED.novos_clientes,
      roi = EXCLUDED.roi, cac = EXCLUDED.cac;


-- ── 5. TABELA: receita_por_categoria ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS receita_por_categoria (
  categoria          TEXT PRIMARY KEY,
  receita            NUMERIC,
  pedidos            INT,
  ticket_medio       NUMERIC,
  desconto_medio_pct NUMERIC,
  margem_pct         NUMERIC
);

ALTER TABLE receita_por_categoria ENABLE ROW LEVEL SECURITY;
CREATE POLICY "leitura_publica" ON receita_por_categoria FOR SELECT USING (true);

INSERT INTO receita_por_categoria VALUES
  ('Feminino',    853463.13, 2580, 330.80, 12.4, 46.2),
  ('Calçados',    494110.24, 1354, 364.86, 10.8, 48.1),
  ('Masculino',   404272.01, 1218, 331.91, 11.2, 44.8),
  ('Acessórios',  269514.67,  918, 293.59, 14.6, 52.3),
  ('Infantil',    224595.56,  708, 317.22,  9.8, 43.7)
ON CONFLICT (categoria) DO UPDATE
  SET receita = EXCLUDED.receita, pedidos = EXCLUDED.pedidos,
      ticket_medio = EXCLUDED.ticket_medio, desconto_medio_pct = EXCLUDED.desconto_medio_pct,
      margem_pct = EXCLUDED.margem_pct;


-- ── 6. TABELA: funil_dispositivo ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS funil_dispositivo (
  dispositivo   TEXT PRIMARY KEY,
  sessoes       INT,
  add_to_cart   INT,
  checkout      INT,
  pedidos       INT
);

ALTER TABLE funil_dispositivo ENABLE ROW LEVEL SECURITY;
CREATE POLICY "leitura_publica" ON funil_dispositivo FOR SELECT USING (true);

INSERT INTO funil_dispositivo VALUES
  ('Mobile',  152747, 18330, 9137,  3406),
  ('Desktop',  89402, 13410, 8941,  2983),
  ('Tablet',   12429,  1119,  783,   389)
ON CONFLICT (dispositivo) DO UPDATE
  SET sessoes = EXCLUDED.sessoes, add_to_cart = EXCLUDED.add_to_cart,
      checkout = EXCLUDED.checkout, pedidos = EXCLUDED.pedidos;


-- ── 7. TABELA: clientes_por_canal ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS clientes_por_canal (
  canal                   TEXT PRIMARY KEY,
  total_clientes          INT,
  score_fidelidade_medio  NUMERIC,
  ticket_medio            NUMERIC
);

ALTER TABLE clientes_por_canal ENABLE ROW LEVEL SECURITY;
CREATE POLICY "leitura_publica" ON clientes_por_canal FOR SELECT USING (true);

INSERT INTO clientes_por_canal VALUES
  ('Meta Ads',       380, 42.3, 298.40),
  ('Google Ads',     285, 38.7, 318.20),
  ('Orgânico',       195, 61.4, 372.80),
  ('E-mail',         138, 68.2, 395.60),
  ('Influenciadores', 98, 35.1, 285.90),
  ('Direto',          56, 72.8, 412.30)
ON CONFLICT (canal) DO UPDATE
  SET total_clientes = EXCLUDED.total_clientes,
      score_fidelidade_medio = EXCLUDED.score_fidelidade_medio,
      ticket_medio = EXCLUDED.ticket_medio;


-- ── 8. TABELA: clientes_por_uf ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS clientes_por_uf (
  uf              TEXT PRIMARY KEY,
  total_clientes  INT
);

ALTER TABLE clientes_por_uf ENABLE ROW LEVEL SECURITY;
CREATE POLICY "leitura_publica" ON clientes_por_uf FOR SELECT USING (true);

INSERT INTO clientes_por_uf VALUES
  ('SP', 448), ('RJ', 187), ('MG', 165), ('RS', 134), ('PR', 112),
  ('SC',  82), ('BA',  78), ('DF',  62), ('CE',  58), ('PE',  52),
  ('GO',  42), ('ES',  38), ('Outros', 42)
ON CONFLICT (uf) DO UPDATE SET total_clientes = EXCLUDED.total_clientes;


-- ── 9. TABELA: renda_faixa ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS renda_faixa (
  faixa           TEXT PRIMARY KEY,
  total_clientes  INT,
  ticket_medio    NUMERIC
);

ALTER TABLE renda_faixa ENABLE ROW LEVEL SECURITY;
CREATE POLICY "leitura_publica" ON renda_faixa FOR SELECT USING (true);

INSERT INTO renda_faixa VALUES
  ('Até R$ 2 mil',       312, 248.90),
  ('R$ 2–5 mil',         489, 318.40),
  ('R$ 5–8 mil',         428, 372.60),
  ('Acima de R$ 8 mil',  271, 487.20)
ON CONFLICT (faixa) DO UPDATE
  SET total_clientes = EXCLUDED.total_clientes, ticket_medio = EXCLUDED.ticket_medio;


-- ── 10. TABELA: motivos_atendimento ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS motivos_atendimento (
  motivo               TEXT PRIMARY KEY,
  quantidade           INT,
  percentual           NUMERIC,
  resolucao_media_dias NUMERIC
);

ALTER TABLE motivos_atendimento ENABLE ROW LEVEL SECURITY;
CREATE POLICY "leitura_publica" ON motivos_atendimento FOR SELECT USING (true);

INSERT INTO motivos_atendimento VALUES
  ('Troca de tamanho',        285, 31.7, 3.2),
  ('Problema no checkout',    198, 22.0, 1.4),
  ('Entrega atrasada',        165, 18.3, 4.8),
  ('Produto diferente',       112, 12.4, 5.1),
  ('Cancelamento de pedido',   89,  9.9, 1.8),
  ('Dúvidas gerais',           51,  5.7, 0.9)
ON CONFLICT (motivo) DO UPDATE
  SET quantidade = EXCLUDED.quantidade, percentual = EXCLUDED.percentual,
      resolucao_media_dias = EXCLUDED.resolucao_media_dias;


-- ── 11. TABELA: conversao_por_canal ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS conversao_por_canal (
  canal             TEXT PRIMARY KEY,
  sessoes           INT,
  pedidos           INT,
  taxa_conversao    NUMERIC,
  bounce_rate       NUMERIC
);

ALTER TABLE conversao_por_canal ENABLE ROW LEVEL SECURITY;
CREATE POLICY "leitura_publica" ON conversao_por_canal FOR SELECT USING (true);

INSERT INTO conversao_por_canal VALUES
  ('E-mail',       18420,  882, 4.79, 28.4),
  ('Orgânico',     52380, 2146, 4.10, 34.2),
  ('Direto',       24810,  892, 3.60, 31.8),
  ('Google Ads',   68920, 1831, 2.66, 48.6),
  ('Meta Ads',     72480, 1624, 2.24, 52.3),
  ('Influenc.',    17568,  403, 2.29, 49.7)
ON CONFLICT (canal) DO UPDATE
  SET sessoes = EXCLUDED.sessoes, pedidos = EXCLUDED.pedidos,
      taxa_conversao = EXCLUDED.taxa_conversao, bounce_rate = EXCLUDED.bounce_rate;
