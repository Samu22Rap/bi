"""
BI — Loja de Roupas Omnichannel
Dashboard acadêmico em Streamlit + Supabase
Dados sintéticos para fins de estudo.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from supabase import create_client, Client

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="BI | Loja Omnichannel",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS global ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Fundo geral */
[data-testid="stAppViewContainer"] { background: #f0f3f7; }
[data-testid="stSidebar"]          { background: #1a3a5c !important; }
[data-testid="stSidebar"] * { color: #c8d8ea !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 14px; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 6px; }

/* Cards KPI */
.kpi-card {
    background: white;
    border-radius: 10px;
    padding: 18px 20px;
    border-left: 5px solid #2e6da4;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    margin-bottom: 4px;
}
.kpi-card.ok   { border-left-color: #1e7e46; background: #f0faf4; }
.kpi-card.alert{ border-left-color: #c0392b; background: #fdf2f1; }

.kpi-label { font-size: 11px; font-weight: 700; text-transform: uppercase;
             letter-spacing: 1px; color: #6b7b8d; margin-bottom: 4px; }
.kpi-value { font-size: 24px; font-weight: 800; color: #1a3a5c; line-height: 1.1; }
.kpi-value.ok    { color: #1e7e46; }
.kpi-value.alert { color: #c0392b; }
.kpi-meta  { font-size: 11px; color: #888; margin-top: 3px; }

/* Títulos de página */
.page-title {
    font-size: 22px; font-weight: 800; color: #1a3a5c;
    border-left: 5px solid #e8a020;
    padding-left: 12px; margin-bottom: 4px;
}
.page-sub { font-size: 13px; color: #6b7b8d; margin-bottom: 24px; }

/* Badge de período */
.badge {
    display: inline-block; background: #2e6da4; color: white;
    font-size: 11px; font-weight: 700; padding: 3px 10px;
    border-radius: 12px; letter-spacing: 0.5px;
}
.badge-warn { background: #c0392b; }

/* Divider */
.divider { border-top: 1px solid #dde4ed; margin: 20px 0; }

/* Tabela personalizada */
.stDataFrame { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Conexão Supabase ──────────────────────────────────────────────────────────
@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )

# ── Loaders de dados (cache 5 min) ────────────────────────────────────────────
@st.cache_data(ttl=300)
def load(tabela: str) -> pd.DataFrame:
    sb = get_supabase()
    res = sb.table(tabela).select("*").execute()
    return pd.DataFrame(res.data)

def load_all() -> dict:
    return {
        "kpis":         load("kpis_resumo"),
        "mensal":       load("receita_mensal"),
        "cac_canal":    load("cac_por_canal"),
        "campanhas":    load("roi_por_campanha"),
        "categorias":   load("receita_por_categoria"),
        "funil":        load("funil_dispositivo"),
        "cli_canal":    load("clientes_por_canal"),
        "cli_uf":       load("clientes_por_uf"),
        "renda":        load("renda_faixa"),
        "atendimento":  load("motivos_atendimento"),
        "conv_canal":   load("conversao_por_canal"),
    }

# ── Helpers ───────────────────────────────────────────────────────────────────
CORES = ["#2e6da4", "#e8a020", "#1e7e46", "#c0392b", "#8e44ad", "#16a085", "#d35400"]

def kpi(col, label: str, valor: str, meta: str = "", status: str = "neutral"):
    cls = "ok" if status == "ok" else ("alert" if status == "alert" else "")
    col.markdown(f"""
    <div class="kpi-card {cls}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value {cls}">{valor}</div>
        <div class="kpi-meta">{meta}</div>
    </div>""", unsafe_allow_html=True)

def get_kpi(df: pd.DataFrame, indicador: str, campo: str = "valor"):
    row = df[df["indicador"] == indicador]
    return float(row[campo].values[0]) if len(row) else 0.0

def fmt_brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_n(v: float) -> str:
    return f"{int(v):,}".replace(",", ".")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 20px 0;">
        <div style="font-size:22px; font-weight:800; color:#fff;">📊 BI Omnichannel</div>
        <div style="font-size:12px; color:#8ab4d4; margin-top:4px;">Loja de Roupas | 2025</div>
    </div>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "Navegação",
        ["📈  Executivo", "📣  Marketing", "👗  Produtos", "👥  Clientes", "🔍  Diagnóstico"],
        label_visibility="collapsed",
    )

    st.markdown('<div style="margin-top:40px; font-size:11px; color:#5a7a9a; line-height:1.8;">'
                '📅 Jan – Jun 2025<br>🎓 Projeto Acadêmico<br>'
                '⚠️ Dados sintéticos</div>', unsafe_allow_html=True)

# ── Carrega dados ─────────────────────────────────────────────────────────────
try:
    D = load_all()
except Exception as e:
    st.error(f"Erro ao conectar ao Supabase: {e}")
    st.info("Verifique as credenciais em `.streamlit/secrets.toml`.")
    st.stop()

# =============================================================================
# PÁGINA 1 — EXECUTIVO
# =============================================================================
if "Executivo" in pagina:
    st.markdown('<div class="page-title">Visão Executiva</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Panorama geral do desempenho do e-commerce · Jan–Jun 2025</div>',
                unsafe_allow_html=True)

    kpis  = D["kpis"]
    mensal = D["mensal"].sort_values("mes_num")

    # ── KPI cards ──
    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Receita Total",       fmt_brl(get_kpi(kpis, "receita_total")),   "Jan–Jun 2025")
    kpi(c2, "Pedidos Válidos",     fmt_n(get_kpi(kpis, "pedidos")),           "Pedidos processados")
    kpi(c3, "Sessões no Site",     fmt_n(get_kpi(kpis, "sessoes")),           "Visitas ao e-commerce")
    kpi(c4, "Invest. Marketing",   fmt_brl(get_kpi(kpis, "investimento_marketing")), "Total acumulado")

    st.markdown("<div style='margin:16px 0'></div>", unsafe_allow_html=True)

    c5, c6, c7, c8 = st.columns(4)
    conv  = get_kpi(kpis, "taxa_conversao")
    meta_conv = get_kpi(kpis, "taxa_conversao", "meta")
    kpi(c5, "Taxa de Conversão",
        f"{conv:.2f}%",
        f"Meta: {meta_conv:.2f}% | Gap: {conv - meta_conv:+.2f} p.p.",
        "alert")

    cac = get_kpi(kpis, "cac")
    meta_cac = get_kpi(kpis, "cac", "meta")
    kpi(c6, "CAC",
        fmt_brl(cac),
        f"Meta: {fmt_brl(meta_cac)} | Gap: {fmt_brl(cac - meta_cac)}",
        "alert")

    kpi(c7, "Ticket Médio",
        fmt_brl(get_kpi(kpis, "ticket_medio")),
        "2,3× o CAC atual  ▲", "ok")

    roi = get_kpi(kpis, "roi_marketing")
    kpi(c8, "ROI de Marketing",
        f"{roi:.2f}× ({roi*100:.0f}%)",
        "Retorno por R$ 1 investido", "ok")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Gráfico 1: Receita + Conversão mensais ──
    col_a, col_b = st.columns([2, 1])

    with col_a:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=mensal["mes"], y=mensal["receita"],
            name="Receita (R$)", marker_color="#2e6da4",
            yaxis="y1", opacity=0.85,
        ))
        fig.add_trace(go.Scatter(
            x=mensal["mes"], y=mensal["taxa_conversao"],
            name="Conversão (%)", mode="lines+markers",
            line=dict(color="#e8a020", width=3),
            marker=dict(size=7),
            yaxis="y2",
        ))
        fig.add_hline(y=3.06, line_dash="dash", line_color="#c0392b",
                      annotation_text="Meta 3,06%", yref="y2",
                      annotation_position="bottom right")
        fig.update_layout(
            title="Receita Mensal e Taxa de Conversão",
            yaxis=dict(title="Receita (R$)", tickprefix="R$ ", tickformat=",.0f"),
            yaxis2=dict(title="Conversão (%)", overlaying="y", side="right",
                        ticksuffix="%", showgrid=False),
            legend=dict(orientation="h", y=-0.15),
            height=360, margin=dict(t=50, b=60),
            plot_bgcolor="white", paper_bgcolor="white",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=conv,
            delta={"reference": meta_conv, "valueformat": ".2f",
                   "suffix": " p.p.", "increasing": {"color": "#1e7e46"},
                   "decreasing": {"color": "#c0392b"}},
            number={"suffix": "%", "valueformat": ".2f"},
            title={"text": "Conversão Atual<br><span style='font-size:12px;color:#888'>Meta: 3,06%</span>"},
            gauge={
                "axis": {"range": [0, 5], "ticksuffix": "%"},
                "bar": {"color": "#c0392b"},
                "steps": [
                    {"range": [0, meta_conv], "color": "#fde8e6"},
                    {"range": [meta_conv, 5], "color": "#d4edda"},
                ],
                "threshold": {"line": {"color": "#1e7e46", "width": 3},
                              "thickness": 0.85, "value": meta_conv},
            },
        ))
        fig2.update_layout(height=360, margin=dict(t=60, b=20),
                           paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Gráfico 2: Pedidos mensais ──
    fig3 = px.bar(
        mensal, x="mes", y="pedidos",
        title="Pedidos por Mês",
        labels={"mes": "", "pedidos": "Pedidos"},
        color_discrete_sequence=["#2e6da4"],
        text="pedidos",
    )
    fig3.update_traces(textposition="outside")
    fig3.update_layout(height=280, plot_bgcolor="white", paper_bgcolor="white",
                       margin=dict(t=50, b=20))
    st.plotly_chart(fig3, use_container_width=True)


# =============================================================================
# PÁGINA 2 — MARKETING
# =============================================================================
elif "Marketing" in pagina:
    st.markdown('<div class="page-title">Marketing</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Desempenho de campanhas, CAC por canal e ROI de investimentos</div>',
                unsafe_allow_html=True)

    kpis      = D["kpis"]
    cac_canal = D["cac_canal"].sort_values("cac", ascending=False)
    campanhas = D["campanhas"].sort_values("roi", ascending=False)
    mensal    = D["mensal"].sort_values("mes_num")

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Invest. Total",    fmt_brl(get_kpi(kpis, "investimento_marketing")), "Todas as plataformas")
    kpi(c2, "ROI Consolidado",  f"{get_kpi(kpis, 'roi_marketing'):.2f}×",
        "R$ 4,69 por R$ 1,00 investido", "ok")
    kpi(c3, "CAC Médio",        fmt_brl(get_kpi(kpis, "cac")),
        f"Meta: {fmt_brl(get_kpi(kpis, 'cac', 'meta'))}", "alert")
    kpi(c4, "Novos Clientes",   fmt_n(get_kpi(kpis, "novos_clientes")), "No período")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # CAC por canal (excluindo Direto onde CAC=0)
        df_cac = cac_canal[cac_canal["cac"] > 0].sort_values("cac")
        cores_cac = ["#1e7e46" if v <= 113.46 else "#c0392b" for v in df_cac["cac"]]
        fig = px.bar(df_cac, x="cac", y="canal", orientation="h",
                     title="CAC por Canal de Aquisição",
                     labels={"cac": "CAC (R$)", "canal": ""},
                     text=df_cac["cac"].apply(lambda v: f"R$ {v:.0f}"),
                     color=df_cac["cac"].apply(lambda v: "Abaixo da meta" if v <= 113.46 else "Acima da meta"),
                     color_discrete_map={"Abaixo da meta": "#1e7e46", "Acima da meta": "#c0392b"})
        fig.add_vline(x=113.46, line_dash="dash", line_color="#1a3a5c",
                      annotation_text="Meta R$113", annotation_position="top right")
        fig.update_traces(textposition="outside")
        fig.update_layout(height=340, plot_bgcolor="white", paper_bgcolor="white",
                          margin=dict(t=50, b=20), showlegend=True,
                          legend=dict(orientation="h", y=-0.18))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig2 = px.bar(campanhas.head(8), x="roi", y="campanha", orientation="h",
                      title="ROI por Campanha (top 8)",
                      labels={"roi": "ROI (×)", "campanha": ""},
                      text=campanhas.head(8)["roi"].apply(lambda v: f"{v:.1f}×"),
                      color="plataforma",
                      color_discrete_sequence=CORES)
        fig2.update_traces(textposition="outside")
        fig2.update_layout(height=340, plot_bgcolor="white", paper_bgcolor="white",
                           margin=dict(t=50, b=20),
                           legend=dict(orientation="h", y=-0.18))
        st.plotly_chart(fig2, use_container_width=True)

    # ── Gráfico: investimento vs novos clientes mensais ──
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=mensal["mes"], y=mensal["investimento_marketing"],
        name="Invest. Marketing (R$)", marker_color="#2e6da4", opacity=0.8, yaxis="y1",
    ))
    fig3.add_trace(go.Scatter(
        x=mensal["mes"], y=mensal["novos_clientes"],
        name="Novos Clientes", mode="lines+markers",
        line=dict(color="#e8a020", width=3), marker=dict(size=7), yaxis="y2",
    ))
    fig3.update_layout(
        title="Investimento em Marketing vs. Novos Clientes por Mês",
        yaxis=dict(title="Investimento (R$)", tickprefix="R$ ", tickformat=",.0f"),
        yaxis2=dict(title="Novos Clientes", overlaying="y", side="right", showgrid=False),
        legend=dict(orientation="h", y=-0.15),
        height=300, plot_bgcolor="white", paper_bgcolor="white", margin=dict(t=50, b=60),
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ── Tabela ranking campanhas ──
    st.markdown("#### Ranking de Eficiência das Campanhas")
    df_tab = campanhas[["campanha", "plataforma", "investimento", "receita_atribuida",
                         "novos_clientes", "cac", "roi"]].copy()
    df_tab.columns = ["Campanha", "Plataforma", "Investimento (R$)", "Receita Atrib. (R$)",
                      "Novos Clientes", "CAC (R$)", "ROI (×)"]
    df_tab["Investimento (R$)"] = df_tab["Investimento (R$)"].map(lambda v: f"R$ {v:,.2f}")
    df_tab["Receita Atrib. (R$)"] = df_tab["Receita Atrib. (R$)"].map(lambda v: f"R$ {v:,.2f}")
    df_tab["CAC (R$)"]   = df_tab["CAC (R$)"].map(lambda v: f"R$ {v:.2f}")
    df_tab["ROI (×)"]    = df_tab["ROI (×)"].map(lambda v: f"{v:.2f}×")
    st.dataframe(df_tab.reset_index(drop=True), use_container_width=True, hide_index=True)


# =============================================================================
# PÁGINA 3 — PRODUTOS
# =============================================================================
elif "Produtos" in pagina:
    st.markdown('<div class="page-title">Produtos</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Mix de produtos, receita por categoria, margem e descontos</div>',
                unsafe_allow_html=True)

    kpis     = D["kpis"]
    cats     = D["categorias"].sort_values("receita", ascending=False)

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Receita Total",   fmt_brl(get_kpi(kpis, "receita_total")))
    kpi(c2, "Itens Vendidos",  "13.279",       "Linhas de pedido")
    kpi(c3, "Ticket Médio",    fmt_brl(get_kpi(kpis, "ticket_medio")), "", "ok")
    kpi(c4, "SKUs Ativos",     "96",           "Produtos no catálogo")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        fig = px.bar(cats, x="receita", y="categoria", orientation="h",
                     title="Receita por Categoria (R$)",
                     labels={"receita": "Receita (R$)", "categoria": ""},
                     text=cats["receita"].apply(lambda v: f"R$ {v/1000:.0f}k"),
                     color_discrete_sequence=["#2e6da4"])
        fig.update_traces(textposition="outside")
        fig.update_layout(height=320, plot_bgcolor="white", paper_bgcolor="white",
                          margin=dict(t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig2 = px.bar(cats, x="categoria", y="desconto_medio_pct",
                      title="Desconto Médio por Categoria (%)",
                      labels={"desconto_medio_pct": "Desconto (%)", "categoria": ""},
                      text=cats["desconto_medio_pct"].apply(lambda v: f"{v:.1f}%"),
                      color="desconto_medio_pct",
                      color_continuous_scale=["#1e7e46", "#e8a020", "#c0392b"])
        fig2.update_traces(textposition="outside")
        fig2.update_layout(height=320, plot_bgcolor="white", paper_bgcolor="white",
                           margin=dict(t=50, b=20), coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        fig3 = px.bar(cats, x="categoria", y="margem_pct",
                      title="Margem Bruta por Categoria (%)",
                      labels={"margem_pct": "Margem (%)", "categoria": ""},
                      text=cats["margem_pct"].apply(lambda v: f"{v:.1f}%"),
                      color_discrete_sequence=["#1e7e46"])
        fig3.update_traces(textposition="outside")
        fig3.update_layout(height=300, plot_bgcolor="white", paper_bgcolor="white",
                           margin=dict(t=50, b=20))
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        fig4 = px.scatter(
            cats, x="ticket_medio", y="pedidos",
            size="receita", color="categoria",
            title="Ticket Médio vs. Volume de Pedidos",
            labels={"ticket_medio": "Ticket Médio (R$)", "pedidos": "Pedidos"},
            color_discrete_sequence=CORES, size_max=50,
        )
        fig4.update_layout(height=300, plot_bgcolor="white", paper_bgcolor="white",
                           margin=dict(t=50, b=20))
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("#### Resumo por Categoria")
    df_tab = cats.copy()
    df_tab.columns = ["Categoria", "Receita (R$)", "Pedidos", "Ticket Médio (R$)",
                      "Desconto Médio (%)", "Margem (%)"]
    df_tab["Receita (R$)"]      = df_tab["Receita (R$)"].map(lambda v: f"R$ {v:,.2f}")
    df_tab["Ticket Médio (R$)"] = df_tab["Ticket Médio (R$)"].map(lambda v: f"R$ {v:.2f}")
    df_tab["Desconto Médio (%)"]= df_tab["Desconto Médio (%)"].map(lambda v: f"{v:.1f}%")
    df_tab["Margem (%)"]        = df_tab["Margem (%)"].map(lambda v: f"{v:.1f}%")
    st.dataframe(df_tab.reset_index(drop=True), use_container_width=True, hide_index=True)


# =============================================================================
# PÁGINA 4 — CLIENTES
# =============================================================================
elif "Clientes" in pagina:
    st.markdown('<div class="page-title">Clientes</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Perfil, distribuição geográfica e comportamento da base de clientes</div>',
                unsafe_allow_html=True)

    kpis     = D["kpis"]
    cli_c    = D["cli_canal"].sort_values("total_clientes", ascending=False)
    cli_uf   = D["cli_uf"].sort_values("total_clientes", ascending=False)
    renda    = D["renda"]

    cadastrados = int(get_kpi(kpis, "clientes_cadastrados"))
    compradores = int(get_kpi(kpis, "novos_clientes"))
    ativacao    = compradores / cadastrados * 100 if cadastrados else 0

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Clientes Cadastrados", fmt_n(cadastrados), "Base total CRM")
    kpi(c2, "Clientes Compradores", fmt_n(compradores), "Com ao menos 1 pedido")
    kpi(c3, "Taxa de Ativação",     f"{ativacao:.1f}%",
        "Cadastrados que compraram", "ok")
    kpi(c4, "Clientes s/ E-mail",   "~8%",
        "Qualidade cadastral", "alert")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        fig = px.bar(cli_c, x="canal", y="total_clientes",
                     title="Clientes por Canal de Aquisição",
                     labels={"canal": "", "total_clientes": "Clientes"},
                     text="total_clientes",
                     color_discrete_sequence=["#2e6da4"])
        fig.update_traces(textposition="outside")
        fig.update_layout(height=320, plot_bgcolor="white", paper_bgcolor="white",
                          margin=dict(t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig2 = px.pie(renda, names="faixa", values="total_clientes",
                      title="Distribuição por Faixa de Renda",
                      color_discrete_sequence=CORES,
                      hole=0.42)
        fig2.update_traces(textinfo="percent+label")
        fig2.update_layout(height=320, paper_bgcolor="white",
                           showlegend=False, margin=dict(t=50, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        fig3 = px.bar(cli_uf.head(12), x="uf", y="total_clientes",
                      title="Top 12 Estados por Concentração de Clientes",
                      labels={"uf": "UF", "total_clientes": "Clientes"},
                      text="total_clientes",
                      color_discrete_sequence=["#1a3a5c"])
        fig3.update_traces(textposition="outside")
        fig3.update_layout(height=300, plot_bgcolor="white", paper_bgcolor="white",
                           margin=dict(t=50, b=20))
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        cli_c_sorted = cli_c.sort_values("score_fidelidade_medio", ascending=False)
        fig4 = px.bar(cli_c_sorted, x="canal", y="score_fidelidade_medio",
                      title="Score Médio de Fidelidade por Canal",
                      labels={"canal": "", "score_fidelidade_medio": "Score (0–100)"},
                      text=cli_c_sorted["score_fidelidade_medio"].apply(lambda v: f"{v:.0f}"),
                      color="score_fidelidade_medio",
                      color_continuous_scale=["#fde8e6", "#e8a020", "#1e7e46"])
        fig4.update_traces(textposition="outside")
        fig4.update_layout(height=300, plot_bgcolor="white", paper_bgcolor="white",
                           margin=dict(t=50, b=20), coloraxis_showscale=False)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("#### Perfil por Canal de Aquisição")
    df_tab = cli_c[["canal", "total_clientes", "score_fidelidade_medio", "ticket_medio"]].copy()
    df_tab.columns = ["Canal", "Clientes", "Score Fidelidade", "Ticket Médio (R$)"]
    df_tab["Ticket Médio (R$)"] = df_tab["Ticket Médio (R$)"].map(lambda v: f"R$ {v:.2f}")
    df_tab["Score Fidelidade"]  = df_tab["Score Fidelidade"].map(lambda v: f"{v:.1f}")
    st.dataframe(df_tab.reset_index(drop=True), use_container_width=True, hide_index=True)


# =============================================================================
# PÁGINA 5 — DIAGNÓSTICO
# =============================================================================
elif "Diagnóstico" in pagina:
    st.markdown('<div class="page-title">Diagnóstico</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Investigação das causas da baixa conversão e CAC elevado</div>',
                unsafe_allow_html=True)

    funil      = D["funil"]
    atend      = D["atendimento"].sort_values("quantidade", ascending=False)
    conv_canal = D["conv_canal"].sort_values("taxa_conversao", ascending=False)

    # Métricas de funil mobile vs desktop
    mob    = funil[funil["dispositivo"] == "Mobile"].iloc[0]
    desk   = funil[funil["dispositivo"] == "Desktop"].iloc[0]
    conv_m = mob["pedidos"] / mob["sessoes"] * 100
    conv_d = desk["pedidos"] / desk["sessoes"] * 100

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Conversão Mobile",  f"{conv_m:.2f}%",
        "Maior volume, menor eficiência", "alert")
    kpi(c2, "Conversão Desktop", f"{conv_d:.2f}%",
        "Menor volume, maior eficiência", "ok")
    kpi(c3, "Tickets de Suporte", "900",
        "Registros no período")
    kpi(c4, "Principal Motivo Suporte", "Troca Tamanho",
        "31,7% dos atendimentos", "alert")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Funil de conversão ──
    funil_total = funil.sum(numeric_only=True)
    etapas = ["Sessões", "Add to Cart", "Checkout", "Pedidos"]
    valores = [int(funil_total["sessoes"]), int(funil_total["add_to_cart"]),
               int(funil_total["checkout"]), int(funil_total["pedidos"])]
    pcts = [f"{v/valores[0]*100:.1f}%" for v in valores]

    fig_funil = go.Figure(go.Funnel(
        y=etapas,
        x=valores,
        textinfo="value+percent initial",
        marker={"color": ["#2e6da4", "#e8a020", "#c0392b", "#1e7e46"]},
        connector={"line": {"color": "#dde4ed", "width": 2}},
    ))
    fig_funil.update_layout(
        title="Funil de Conversão — Jornada Completa do Cliente",
        height=380, paper_bgcolor="white", margin=dict(t=50, b=20),
    )
    st.plotly_chart(fig_funil, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        funil_disp = funil.copy()
        funil_disp["taxa_conv"] = funil_disp["pedidos"] / funil_disp["sessoes"] * 100
        cores_conv = ["#c0392b" if v < 2.66 else "#1e7e46" for v in funil_disp["taxa_conv"]]
        fig2 = px.bar(funil_disp, x="dispositivo", y="taxa_conv",
                      title="Taxa de Conversão por Dispositivo",
                      labels={"dispositivo": "", "taxa_conv": "Conversão (%)"},
                      text=funil_disp["taxa_conv"].apply(lambda v: f"{v:.2f}%"),
                      color="dispositivo",
                      color_discrete_sequence=["#c0392b", "#1e7e46", "#e8a020"])
        fig2.add_hline(y=2.66, line_dash="dash", line_color="#1a3a5c",
                       annotation_text="Média 2,66%")
        fig2.update_traces(textposition="outside")
        fig2.update_layout(height=320, plot_bgcolor="white", paper_bgcolor="white",
                           margin=dict(t=50, b=20), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        fig3 = px.bar(conv_canal, x="taxa_conversao", y="canal", orientation="h",
                      title="Taxa de Conversão por Canal de Origem",
                      labels={"taxa_conversao": "Conversão (%)", "canal": ""},
                      text=conv_canal["taxa_conversao"].apply(lambda v: f"{v:.2f}%"),
                      color="taxa_conversao",
                      color_continuous_scale=["#c0392b", "#e8a020", "#1e7e46"])
        fig3.add_vline(x=2.66, line_dash="dash", line_color="#1a3a5c",
                       annotation_text="Média 2,66%")
        fig3.update_traces(textposition="outside")
        fig3.update_layout(height=320, plot_bgcolor="white", paper_bgcolor="white",
                           margin=dict(t=50, b=20), coloraxis_showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    # ── Funil por dispositivo (detalhe) ──
    col_c, col_d = st.columns(2)

    with col_c:
        fig4 = go.Figure()
        for i, row in funil.iterrows():
            fig4.add_trace(go.Bar(
                name=row["dispositivo"],
                x=["Sessões", "Add to Cart", "Checkout", "Pedidos"],
                y=[row["sessoes"], row["add_to_cart"], row["checkout"], row["pedidos"]],
            ))
        fig4.update_layout(
            title="Funil por Dispositivo (volume)",
            barmode="group", height=320,
            plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(t=50, b=20),
            legend=dict(orientation="h", y=-0.18),
        )
        st.plotly_chart(fig4, use_container_width=True)

    with col_d:
        fig5 = px.bar(atend, x="quantidade", y="motivo", orientation="h",
                      title="Motivos de Atendimento (top ocorrências)",
                      labels={"quantidade": "Tickets", "motivo": ""},
                      text=atend["percentual"].apply(lambda v: f"{v:.1f}%"),
                      color="quantidade",
                      color_continuous_scale=["#2e6da4", "#c0392b"])
        fig5.update_traces(textposition="outside")
        fig5.update_layout(height=320, plot_bgcolor="white", paper_bgcolor="white",
                           margin=dict(t=50, b=20), coloraxis_showscale=False)
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown("#### Detalhamento dos Motivos de Atendimento")
    df_tab = atend.copy()
    df_tab.columns = ["Motivo", "Qtd. Tickets", "% do Total", "Resolução Média (dias)"]
    df_tab["% do Total"] = df_tab["% do Total"].map(lambda v: f"{v:.1f}%")
    df_tab["Resolução Média (dias)"] = df_tab["Resolução Média (dias)"].map(lambda v: f"{v:.1f} dias")
    st.dataframe(df_tab.reset_index(drop=True), use_container_width=True, hide_index=True)


# ── Rodapé ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; font-size:11px; color:#aaa;
            border-top:1px solid #dde4ed; padding-top:20px; margin-top:32px;">
    Projeto Acadêmico de Business Intelligence &mdash;
    Dados Sintéticos &mdash; Uso Exclusivamente Educacional
</div>
""", unsafe_allow_html=True)
