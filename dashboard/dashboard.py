import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='Olist E-Commerce Dashboard', page_icon='🛍️', layout='wide')

# =============================================================================
# Tema warna
# =============================================================================
C = {
    'blue': '#2a78d6', 'orange': '#eb6834', 'aqua': '#1baf7a', 'yellow': '#eda100',
    'magenta': '#e87ba4', 'green': '#008300', 'violet': '#6250d6', 'red': '#e34948',
    'gray': '#c9c8c3', 'ink': '#1f2430', 'muted': '#6b6a66',
}
REGION_COLORS = {'Sudeste': C['blue'], 'Sul': C['aqua'], 'Nordeste': C['orange'],
                 'Centro-Oeste': C['violet'], 'Norte': C['magenta']}
REGION_OF = {
    **dict.fromkeys(['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'], 'Norte'),
    **dict.fromkeys(['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'], 'Nordeste'),
    **dict.fromkeys(['DF', 'GO', 'MT', 'MS'], 'Centro-Oeste'),
    **dict.fromkeys(['ES', 'MG', 'RJ', 'SP'], 'Sudeste'),
    **dict.fromkeys(['PR', 'RS', 'SC'], 'Sul'),
}
SEGMENT_COLORS = {
    'Loyal Customers': C['green'], 'Promising High Value': C['blue'], 'New Customers': C['aqua'],
    'Need Attention': C['yellow'], "Can't Lose Them": C['orange'], 'At Risk Loyal': C['magenta'],
    'Hibernating': C['violet'],
}
REVIEW_COLORS = {1: '#d1373f', 2: '#ef8a62', 3: '#c9c8c3', 4: '#67a9cf', 5: '#2166ac'}
BLUE_SCALE = ['#9ec5f4', '#5598e7', '#2a78d6', '#1c5cab', '#0d366b']
WARM_SCALE = ['#f6b48a', '#eb6834', '#c94f1f', '#8f3410', '#5c1f08']

st.markdown("""
<style>
.block-container {padding-top: 3.2rem; padding-bottom: 2rem;}
.hero {
    background: linear-gradient(120deg, #1c5cab 0%, #2a78d6 45%, #6250d6 100%);
    border-radius: 18px; padding: 26px 32px; color: white; margin-bottom: 18px;
    box-shadow: 0 8px 24px rgba(42,120,214,.25);
}
.hero h1 {color: white; font-size: 2.0rem; margin: 0 0 4px 0; padding: 0;}
.hero p {color: rgba(255,255,255,.88); margin: 0; font-size: 0.98rem;}
.hero .chip {display:inline-block; background: rgba(255,255,255,.18); border-radius: 999px;
             padding: 3px 12px; margin: 10px 6px 0 0; font-size: .82rem;}
.kpi {
    min-height: 150px;
    background: white; border-radius: 14px; padding: 16px 18px; border: 1px solid #ecebe7;
    border-top: 5px solid var(--accent); box-shadow: 0 2px 10px rgba(20,20,40,.05); height: 100%;
}
.kpi .icon {font-size: 1.3rem;}
.kpi .label {white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: #6b6a66; font-size: .78rem; text-transform: uppercase; letter-spacing: .04em; margin-top: 2px;}
.kpi .value {color: #1f2430; font-size: 1.65rem; font-weight: 700; line-height: 1.2; margin-top: 2px;}
.kpi .delta {font-size: .82rem; margin-top: 4px;}
.up {color: #1a8a4a;} .down {color: #d1373f;} .flat {color: #6b6a66;}
.insight {
    border-left: 5px solid var(--accent); background: var(--bg); border-radius: 10px;
    padding: 12px 16px; margin: 6px 0 14px 0; color: #1f2430; font-size: .95rem;
}
.seg-card {border-radius: 12px; padding: 14px 16px; color: white; height: 100%;}
.seg-card h4 {color: white; margin: 0 0 6px 0; font-size: 1.05rem;}
.seg-card p {margin: 0; font-size: .9rem; color: rgba(255,255,255,.92);}
div[data-testid="stTabs"] button p {font-size: 1rem; font-weight: 600;}

/* ---- Kunci tema terang, apa pun tema browser/OS ---- */
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #fafbfd !important; color: #1f2430 !important; color-scheme: light !important;
}
[data-testid="stHeader"] {background: rgba(250,251,253,.85) !important;}
[data-testid="stHeader"] *, [data-testid="stToolbar"] * {color: #1f2430 !important;}
section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
    background: linear-gradient(180deg, #f3f7fd 0%, #f7f5ff 100%) !important;
}
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stApp p, .stApp li, .stApp label, .stApp span, .stApp small,
[data-testid="stMarkdownContainer"], [data-testid="stCaptionContainer"],
[data-testid="stWidgetLabel"] * {color: #1f2430;}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {color: #6b6a66 !important;}
.hero, .hero *, .seg-card, .seg-card * {color: white !important;}
/* metric */
[data-testid="stMetric"] {background: white; border: 1px solid #ecebe7; border-radius: 12px; padding: 12px 16px;}
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * {color: #1f2430 !important;}
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * {color: #6b6a66 !important;}
/* input: selectbox, multiselect, date */
div[data-baseweb="select"] > div, div[data-baseweb="input"], div[data-baseweb="input"] input,
div[data-baseweb="base-input"], div[data-baseweb="base-input"] input {
    background-color: white !important; color: #1f2430 !important; border-color: #d6d5d0 !important;
}
div[data-baseweb="select"] *, div[data-baseweb="input"] * {color: #1f2430 !important;}
div[data-baseweb="select"] svg {fill: #6b6a66 !important;}
div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li, div[data-baseweb="popover"] div[role="listbox"],
div[data-baseweb="calendar"], div[data-baseweb="calendar"] * {background-color: white !important; color: #1f2430 !important;}
div[data-baseweb="popover"] li:hover {background-color: #eef5fd !important;}
span[data-baseweb="tag"] {background-color: #2a78d6 !important;}
span[data-baseweb="tag"] * {color: white !important;}
/* tombol segmented & pills */
[data-testid="stButtonGroup"] button {background: white !important; color: #1f2430 !important; border-color: #d6d5d0 !important;}
[data-testid="stButtonGroup"] button * {color: #1f2430 !important;}
[data-testid="stButtonGroup"] button[aria-checked="true"], [data-testid="stButtonGroup"] button[kind*="Active"] {
    background: #eef5fd !important; border-color: #2a78d6 !important;}
[data-testid="stButtonGroup"] button[aria-checked="true"] *, [data-testid="stButtonGroup"] button[kind*="Active"] * {color: #2a78d6 !important;}
/* tabs, expander, slider */
div[data-testid="stTabs"] button p {color: #52514e !important;}
div[data-testid="stTabs"] button[aria-selected="true"] p {color: #2a78d6 !important;}
[data-testid="stExpander"] details {background: white !important; border-color: #ecebe7 !important;}
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary * {color: #1f2430 !important;}
[data-testid="stSliderTickBarMin"], [data-testid="stSliderTickBarMax"] {color: #6b6a66 !important;}
/* tabel HTML */
.tbl {width: 100%; border-collapse: separate; border-spacing: 0; background: white; border: 1px solid #ecebe7;
      border-radius: 12px; overflow: hidden; font-size: .9rem;}
.tbl th {background: #f1f4fa; color: #52514e !important; text-align: left; font-weight: 600; padding: 9px 12px;}
.tbl td {color: #1f2430 !important; padding: 8px 12px; border-top: 1px solid #f0efeb;}
.tbl td.num {text-align: right; font-variant-numeric: tabular-nums;}
.tbl tr:hover td {background: #f7faff;}
.bar {background: #e6eef9; border-radius: 99px; height: 8px; width: 100%; min-width: 70px;}
.bar > div {background: #2a78d6; height: 8px; border-radius: 99px;}
</style>
""", unsafe_allow_html=True)


def style_fig(fig, height=420, legend=True):
    fig.update_layout(
        template='plotly_white', height=height, margin=dict(l=10, r=10, t=95 if legend else 55, b=10),
        font=dict(family='Inter, Segoe UI, sans-serif', size=13, color=C['ink']),
        title=dict(y=0.98, yanchor='top', yref='container', x=0.01, font=dict(size=16)), hoverlabel=dict(bgcolor='white', font_size=13),
        showlegend=legend, legend=dict(orientation='h', yanchor='bottom', y=1.0, xanchor='left', x=0, title=None, font=dict(size=12)),
        plot_bgcolor='white', paper_bgcolor='white',
    )
    fig.update_xaxes(showgrid=False, linecolor='#d6d5d0')
    fig.update_yaxes(gridcolor='#ecebe7', zeroline=False)
    if fig.layout.title.text and not fig.layout.title.text.startswith('<b>'):
        fig.update_layout(title_text=f'<b>{fig.layout.title.text}</b>')
    return fig


def insight(text, accent=C['blue'], bg='#eef5fd'):
    st.markdown(f'<div class="insight" style="--accent:{accent}; --bg:{bg}">💡 {text}</div>', unsafe_allow_html=True)


def kpi_card(col, icon, label, value, delta, accent, higher_is_better=True):
    if delta is None or np.isnan(delta):
        d_html = '<div class="delta flat">● seluruh periode data</div>'
    else:
        good = (delta >= 0) == higher_is_better
        cls = 'flat' if abs(delta) < 0.0005 else ('up' if good else 'down')
        arrow = '▲' if delta >= 0 else '▼'
        d_html = f'<div class="delta {cls}">{arrow} {abs(delta):.1%} vs periode lalu</div>'
    col.markdown(f'<div class="kpi" style="--accent:{accent}"><div class="icon">{icon}</div>'
                 f'<div class="label">{label}</div><div class="value">{value}</div>{d_html}</div>',
                 unsafe_allow_html=True)


def brl(v):
    if abs(v) >= 1e6:
        return f'R$ {v/1e6:,.2f} jt'
    if abs(v) >= 1e3:
        return f'R$ {v/1e3:,.1f} rb'
    return f'R$ {v:,.2f}'


# =============================================================================
# Data
# =============================================================================
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_data.csv')
    df = pd.read_csv(path, parse_dates=['order_purchase_timestamp', 'order_delivered_customer_date',
                                        'order_estimated_delivery_date'])
    df['region'] = df.customer_state.map(REGION_OF)
    df['product_category_name_english'] = df['product_category_name_english'].fillna('unknown')
    return df


def to_orders(df):
    """Satu baris per pesanan."""
    return (df.groupby('order_id')
            .agg(customer_unique_id=('customer_unique_id', 'first'), customer_state=('customer_state', 'first'),
                 region=('region', 'first'), lat=('lat', 'first'), lng=('lng', 'first'),
                 purchase=('order_purchase_timestamp', 'first'), delivery_days=('delivery_days', 'first'),
                 is_late=('is_late', 'first'), review_score=('review_score', 'first'),
                 revenue=('price', 'sum'), freight=('freight_value', 'sum'))
            .reset_index())


def summary(orders):
    if orders.empty:
        return dict(n=0, rev=np.nan, aov=np.nan, late=np.nan, review=np.nan)
    return dict(n=len(orders), rev=orders.revenue.sum(), aov=orders.revenue.mean(),
                late=orders.is_late.mean(), review=orders.review_score.mean())


def rfm_segment(r, f, m):
    if f >= 2 and r >= 3:
        return 'Loyal Customers'
    if f >= 2:
        return 'At Risk Loyal'
    if r >= 4 and m >= 4:
        return 'Promising High Value'
    if r >= 4:
        return 'New Customers'
    if r <= 2 and m >= 4:
        return "Can't Lose Them"
    if r <= 2:
        return 'Hibernating'
    return 'Need Attention'


def build_rfm(orders):
    ref = orders.purchase.max() + pd.Timedelta(days=1)
    rfm = (orders.assign(total=orders.revenue + orders.freight)
           .groupby('customer_unique_id')
           .agg(last_purchase=('purchase', 'max'), frequency=('order_id', 'nunique'),
                monetary=('total', 'sum'), state=('customer_state', 'first'))
           .reset_index())
    rfm['recency'] = (ref - rfm.last_purchase).dt.days
    if len(rfm) >= 5:
        rfm['R'] = pd.qcut(rfm.recency.rank(method='first'), 5, labels=[5, 4, 3, 2, 1]).astype(int)
        rfm['M'] = pd.qcut(rfm.monetary.rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    else:
        rfm['R'], rfm['M'] = 3, 3
    rfm['F'] = pd.cut(rfm.frequency, bins=[0, 1, 2, np.inf], labels=[1, 2, 3]).astype(int)
    rfm['segment'] = [rfm_segment(r, f, m) for r, f, m in zip(rfm.R, rfm.F, rfm.M)]
    return rfm


all_df = load_data()
min_date = all_df.order_purchase_timestamp.min().date()
max_date = all_df.order_purchase_timestamp.max().date()

# =============================================================================
# Sidebar
# =============================================================================
with st.sidebar:
    st.markdown('## 🛍️ Olist Insight')
    st.caption('Brazilian E-Commerce · pesanan delivered')
    preset = st.selectbox('Periode cepat', ['Semua data (Jan 2017 – Agu 2018)', 'Tahun 2017', 'Jan – Agu 2018',
                                            'Black Friday (Nov 2017)', 'Kustom'])
    presets = {
        'Semua data (Jan 2017 – Agu 2018)': (min_date, max_date),
        'Tahun 2017': (pd.Timestamp('2017-01-01').date(), pd.Timestamp('2017-12-31').date()),
        'Jan – Agu 2018': (pd.Timestamp('2018-01-01').date(), max_date),
        'Black Friday (Nov 2017)': (pd.Timestamp('2017-11-01').date(), pd.Timestamp('2017-11-30').date()),
    }
    if preset == 'Kustom':
        dr = st.date_input('Rentang tanggal', value=[min_date, max_date], min_value=min_date, max_value=max_date)
        start_date, end_date = (dr if isinstance(dr, (list, tuple)) and len(dr) == 2 else (min_date, max_date))
    else:
        start_date, end_date = presets[preset]

    regions = st.multiselect('Wilayah', list(REGION_COLORS), placeholder='Semua wilayah')
    state_options = sorted(all_df[all_df.region.isin(regions)].customer_state.unique()) if regions \
        else sorted(all_df.customer_state.unique())
    states = st.multiselect('State', state_options, placeholder='Semua state')
    st.divider()
    st.caption('Sumber: Olist Brazilian E-Commerce Public Dataset')
    st.caption('Dibuat oleh **Horasio** · Proyek Analisis Data Dicoding')

scope = all_df
if regions:
    scope = scope[scope.region.isin(regions)]
if states:
    scope = scope[scope.customer_state.isin(states)]

dates = scope.order_purchase_timestamp.dt.date
main_df = scope[(dates >= start_date) & (dates <= end_date)]
span = pd.Timestamp(end_date) - pd.Timestamp(start_date) + pd.Timedelta(days=1)
prev_start = (pd.Timestamp(start_date) - span).date()
prev_df = scope[(dates >= prev_start) & (dates < start_date)]

if main_df.empty:
    st.warning('Tidak ada pesanan untuk kombinasi filter ini. Coba ubah periode atau wilayah.')
    st.stop()

orders = to_orders(main_df)
cur = summary(orders)
prev = summary(to_orders(prev_df)) if prev_start >= min_date and not prev_df.empty else None

# =============================================================================
# Header & KPI
# =============================================================================
scope_label = ', '.join(states) if states else (', '.join(regions) if regions else 'Seluruh Brasil')
st.markdown(f"""
<div class="hero">
  <h1>🛍️ Dashboard Penjualan & Kepuasan Pelanggan</h1>
  <p>Analisis marketplace Olist: tren penjualan, kategori produk, performa pengiriman, segmentasi pelanggan, dan peta sebaran.</p>
  <span class="chip">📅 {start_date:%d %b %Y} – {end_date:%d %b %Y}</span>
  <span class="chip">📍 {scope_label}</span>
  <span class="chip">🧾 {cur['n']:,} pesanan</span>
</div>
""", unsafe_allow_html=True)


def rel(key):
    if prev is None or not prev[key] or np.isnan(prev[key]):
        return None
    return cur[key] / prev[key] - 1


cols = st.columns(5)
kpi_card(cols[0], '🧾', 'Total pesanan', f"{cur['n']:,}", rel('n'), C['blue'])
kpi_card(cols[1], '💰', 'Revenue', brl(cur['rev']), rel('rev'), C['aqua'])
kpi_card(cols[2], '🛒', 'Nilai per pesanan', brl(cur['aov']), rel('aov'), C['violet'])
kpi_card(cols[3], '🚚', 'Pesanan terlambat', f"{cur['late']:.1%}", rel('late'), C['orange'], higher_is_better=False)
kpi_card(cols[4], '⭐', 'Rata-rata review', f"{cur['review']:.2f} / 5", rel('review'), C['yellow'])
st.write('')

tab1, tab2, tab3, tab4, tab5 = st.tabs(['📈 Tren Penjualan', '🏷️ Produk', '🚚 Pengiriman & Review',
                                        '👥 Segmentasi Pelanggan', '🗺️ Peta'])

# =============================================================================
# Tab 1 - Tren
# =============================================================================
with tab1:
    c1, c2 = st.columns([1, 1])
    metric = c1.segmented_control('Metrik', ['Revenue', 'Jumlah pesanan'], default='Revenue', key='metric')
    gran = c2.segmented_control('Granularitas', ['Harian', 'Mingguan', 'Bulanan'], default='Bulanan', key='gran')
    metric = metric or 'Revenue'
    gran = gran or 'Bulanan'
    freq = {'Harian': 'D', 'Mingguan': 'W-MON', 'Bulanan': 'MS'}[gran]
    ts = (orders.set_index('purchase').resample(freq)
          .agg(revenue=('revenue', 'sum'), n=('order_id', 'count')).reset_index())
    ycol = 'revenue' if metric == 'Revenue' else 'n'
    peak = ts.loc[ts[ycol].idxmax()]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ts.purchase, y=ts[ycol], mode='lines+markers' if gran != 'Harian' else 'lines',
        line=dict(color=C['blue'], width=3, shape='spline', smoothing=0.6), marker=dict(size=7),
        fill='tozeroy', fillcolor='rgba(42,120,214,0.12)',
        hovertemplate='%{x|%d %b %Y}<br>' + ('R$ %{y:,.0f}' if ycol == 'revenue' else '%{y:,} pesanan') + '<extra></extra>',
        name=metric))
    fig.add_trace(go.Scatter(x=[peak.purchase], y=[peak[ycol]], mode='markers',
                             marker=dict(size=16, color=C['orange'], line=dict(color='white', width=3)),
                             hoverinfo='skip', showlegend=False))
    fig.add_annotation(x=peak.purchase, y=peak[ycol], text='🔥 Puncak: ' + (f'{peak.purchase:%b %Y}' if gran == 'Bulanan' else (f'minggu {peak.purchase:%d %b %Y}' if gran == 'Mingguan' else f'{peak.purchase:%d %b %Y}')),
                       showarrow=True, arrowhead=0, ax=0, ay=-40, font=dict(color=C['orange'], size=13),
                       bgcolor='white', bordercolor=C['orange'], borderpad=4)
    fig.update_yaxes(rangemode='tozero', title='Revenue (R$)' if ycol == 'revenue' else 'Jumlah pesanan')
    fig.update_layout(title=f'{metric} {gran.lower()}')
    st.plotly_chart(theme=None, figure_or_data=style_fig(fig, 430, legend=False), width='stretch')

    if len(orders) and prev is not None and prev['rev']:
        insight(f"Revenue periode ini <b>{brl(cur['rev'])}</b>, "
                f"{'naik' if cur['rev'] >= prev['rev'] else 'turun'} <b>{abs(cur['rev']/prev['rev']-1):.1%}</b> "
                f"dibanding periode sebelumnya dengan panjang yang sama.")
    else:
        insight('Pada data lengkap, puncak pesanan terjadi di <b>November 2017</b> (Black Friday), '
                'dan revenue Jan–Agu 2018 tumbuh ±141% dibanding Jan–Agu 2017.')

    c1, c2 = st.columns([1.35, 1])
    with c1:
        heat = orders.assign(day=orders.purchase.dt.dayofweek, hour=orders.purchase.dt.hour)
        hm = heat.pivot_table(index='day', columns='hour', values='order_id', aggfunc='count', fill_value=0)
        hm = hm.reindex(index=range(7), columns=range(24), fill_value=0)
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        fig = px.imshow(hm.values, x=[f'{h:02d}' for h in range(24)], y=days, aspect='auto',
                        color_continuous_scale=BLUE_SCALE, labels=dict(x='Jam', y='', color='Pesanan'))
        fig.update_traces(hovertemplate='%{y}, jam %{x}:00<br>%{z:,} pesanan<extra></extra>', xgap=2, ygap=2)
        fig.update_layout(title='Kapan pelanggan paling banyak belanja?')
        st.plotly_chart(theme=None, figure_or_data=style_fig(fig, 360, legend=False), width='stretch')
    with c2:
        reg = orders.groupby('region').revenue.sum().reset_index().sort_values('revenue', ascending=False)
        fig = px.pie(reg, names='region', values='revenue', hole=0.6, color='region', color_discrete_map=REGION_COLORS)
        fig.update_traces(textinfo='percent', textfont_size=13, marker=dict(line=dict(color='white', width=2)),
                          hovertemplate='%{label}<br>R$ %{value:,.0f} (%{percent})<extra></extra>', sort=False)
        fig.update_layout(title='Kontribusi revenue per wilayah',
                          annotations=[dict(text=f"<b>{brl(cur['rev'])}</b><br>total", showarrow=False, font_size=14)])
        st.plotly_chart(theme=None, figure_or_data=style_fig(fig, 360), width='stretch')
    busiest = hm.stack().idxmax()
    insight(f"Jam tersibuk ada di hari <b>{days[busiest[0]]} pukul {busiest[1]:02d}:00</b>. Jadwalkan push notification "
            f"dan flash sale di jam-jam berwarna gelap pada heatmap.", C['violet'], '#f2f0fc')

# =============================================================================
# Tab 2 - Produk
# =============================================================================
with tab2:
    cat = (main_df.groupby('product_category_name_english')
           .agg(revenue=('price', 'sum'), orders=('order_id', 'nunique'), avg_price=('price', 'mean'))
           .sort_values('revenue', ascending=False).reset_index())
    cat['share'] = cat.revenue / cat.revenue.sum()
    cat['label'] = cat.product_category_name_english.str.replace('_', ' ').str.title()

    top_n = st.slider('Tampilkan berapa kategori teratas?', 5, 20, 10)
    top = cat.head(top_n)
    st.markdown(f'#### Top {top_n} kategori menyumbang **{top.share.sum():.1%}** revenue')

    c1, c2 = st.columns([1.1, 1])
    with c1:
        plot = top.iloc[::-1]
        colors = [C['blue'] if i >= len(plot) - 3 else '#9ec5f4' for i in range(len(plot))]
        fig = go.Figure(go.Bar(
            x=plot.revenue, y=plot.label, orientation='h', marker=dict(color=colors, cornerradius=6),
            text=[f'{s:.1%}' for s in plot.share], textposition='outside',
            customdata=np.stack([plot.orders, plot.avg_price], axis=1),
            hovertemplate='<b>%{y}</b><br>Revenue: R$ %{x:,.0f}<br>Pesanan: %{customdata[0]:,}'
                          '<br>Harga rata-rata: R$ %{customdata[1]:,.2f}<extra></extra>'))
        fig.update_xaxes(title='Revenue (R$)', range=[0, plot.revenue.max() * 1.15])
        fig.update_layout(title='Ranking revenue (3 teratas disorot)')
        st.plotly_chart(theme=None, figure_or_data=style_fig(fig, 120 + 32 * top_n, legend=False), width='stretch')
    with c2:
        tm = top.copy()
        ramp = ['#b7d3f6', '#86b6ef', '#5598e7', '#2a78d6', '#1c5cab', '#104281', '#0d366b']
        idx = np.linspace(0, len(ramp) - 1, len(tm)).round().astype(int)[::-1]
        fig = go.Figure(go.Treemap(
            labels=tm.label, parents=[''] * len(tm), values=tm.revenue, customdata=tm.share,
            marker=dict(colors=[ramp[i] for i in idx], line=dict(color='white', width=2)),
            texttemplate='<b>%{label}</b><br>%{customdata:.1%} dari total', textfont_size=13,
            hovertemplate='<b>%{label}</b><br>R$ %{value:,.0f}<extra></extra>', tiling=dict(pad=2)))
        fig.update_traces(root_color='white')
        fig.update_layout(title='Proporsi revenue (treemap)', coloraxis_showscale=False)
        st.plotly_chart(theme=None, figure_or_data=style_fig(fig, 120 + 32 * top_n, legend=False), width='stretch')

    c1, c2 = st.columns([1.2, 1])
    with c1:
        sc = cat[cat.orders >= 20].copy()
        sc['highlight'] = np.where(sc.index < 10, 'Top 10 revenue', 'Kategori lain')
        fig = px.scatter(sc, x='orders', y='avg_price', size='revenue', color='highlight', size_max=45,
                         hover_name='label', log_x=True, log_y=True,
                         color_discrete_map={'Top 10 revenue': C['orange'], 'Kategori lain': '#9ec5f4'},
                         labels={'orders': 'Jumlah pesanan (log)', 'avg_price': 'Harga rata-rata item (R$, log)'})
        fig.update_traces(marker=dict(line=dict(color='white', width=1.5), opacity=0.85),
                          hovertemplate='<b>%{hovertext}</b><br>Pesanan: %{x:,}<br>Harga rata-rata: R$ %{y:,.2f}<extra></extra>')
        fig.update_xaxes(dtick=1, minor=dict(showgrid=False))
        fig.update_yaxes(dtick=1)
        fig.update_layout(title='Volume vs harga: dari mana revenue datang?')
        st.plotly_chart(theme=None, figure_or_data=style_fig(fig, 420), width='stretch')
    with c2:
        st.markdown('##### 🔻 Kategori dengan revenue terendah')
        low = cat.tail(8).sort_values('revenue')[['label', 'revenue', 'orders']]
        mx = low.revenue.max()
        rows = ''.join(f'<tr><td>{r.label}</td><td><div class="bar"><div style="width:{r.revenue / mx * 100:.0f}%"></div></div></td>'
                       f'<td class="num">R$ {r.revenue:,.0f}</td><td class="num">{r.orders:,}</td></tr>'
                       for r in low.itertuples())
        st.markdown(f'<table class="tbl"><tr><th>Kategori</th><th>Revenue</th><th></th><th>Pesanan</th></tr>{rows}</table>',
                    unsafe_allow_html=True)
    best = top.iloc[0]
    insight(f"<b>{best.label}</b> memimpin dengan {best.share:.1%} revenue. Kategori di kanan atas scatter plot "
            f"(volume tinggi sekaligus harga tinggi) adalah prioritas utama untuk promosi dan ketersediaan stok.",
            C['orange'], '#fdf0ea')

# =============================================================================
# Tab 3 - Pengiriman & Review
# =============================================================================
with tab3:
    on_time = orders[~orders.is_late]
    late = orders[orders.is_late]
    c1, c2, c3 = st.columns(3)
    c1.metric('⭐ Review pesanan tepat waktu', f'{on_time.review_score.mean():.2f}')
    c2.metric('⭐ Review pesanan terlambat', f'{late.review_score.mean():.2f}' if len(late) else '-',
              delta=f'{late.review_score.mean() - on_time.review_score.mean():.2f} poin' if len(late) else None)
    c3.metric('⏱️ Rata-rata lama kirim', f'{orders.delivery_days.mean():.1f} hari')

    c1, c2 = st.columns([1, 1.25])
    with c1:
        dist = (orders.dropna(subset=['review_score'])
                .assign(status=lambda d: np.where(d.is_late, 'Terlambat', 'Tepat waktu'),
                        score=lambda d: d.review_score.round().clip(1, 5).astype(int))
                .groupby(['status', 'score']).size().reset_index(name='n'))
        dist['pct'] = dist.n / dist.groupby('status').n.transform('sum')
        fig = go.Figure()
        for s in [1, 2, 3, 4, 5]:
            d = dist[dist.score == s]
            fig.add_trace(go.Bar(y=d.status, x=d.pct, orientation='h', name=f'{s} ★',
                                 marker=dict(color=REVIEW_COLORS[s], line=dict(color='white', width=2)),
                                 text=[f'{v:.0%}' if v >= 0.09 else '' for v in d.pct], textposition='inside',
                                 insidetextanchor='middle',
                                 hovertemplate=f'{s} bintang: ' + '%{x:.1%}<extra>%{y}</extra>'))
        fig.update_layout(barmode='stack', title='Distribusi bintang review')
        fig.update_xaxes(tickformat='.0%', range=[0, 1])
        st.plotly_chart(theme=None, figure_or_data=style_fig(fig, 330), width='stretch')
    with c2:
        orders['bin'] = pd.cut(orders.delivery_days, [0, 7, 14, 21, 30, np.inf],
                               labels=['≤7 hari', '8–14 hari', '15–21 hari', '22–30 hari', '>30 hari'])
        b = orders.groupby('bin', observed=False).agg(review=('review_score', 'mean'), n=('order_id', 'count')).reset_index()
        fig = go.Figure(go.Bar(
            x=b.bin.astype(str), y=b.review, marker=dict(color=['#1baf7a', '#67a9cf', '#eda100', '#eb6834', '#d1373f'],
                                                         cornerradius=8),
            text=[f'{v:.2f}' if pd.notna(v) else '' for v in b.review], textposition='outside',
            customdata=b.n, hovertemplate='%{x}<br>Review rata-rata: %{y:.2f}<br>%{customdata:,} pesanan<extra></extra>'))
        fig.add_hline(y=4, line=dict(color=C['muted'], width=1, dash='dot'),
                      annotation_text='batas review 4', annotation_position='top right')
        fig.update_yaxes(range=[0, 5.2], title='Rata-rata review')
        fig.update_layout(title='Makin lama pengiriman, makin turun review (binning)')
        st.plotly_chart(theme=None, figure_or_data=style_fig(fig, 330, legend=False), width='stretch')

    sdf = (orders.groupby(['customer_state', 'region'])
           .agg(late_rate=('is_late', 'mean'), days=('delivery_days', 'mean'),
                review=('review_score', 'mean'), n=('order_id', 'count'))
           .reset_index())
    c1, c2 = st.columns([1.25, 1])
    with c1:
        s2 = sdf.sort_values('late_rate', ascending=False)
        fig = px.bar(s2, x='customer_state', y='late_rate', color='region', color_discrete_map=REGION_COLORS,
                     custom_data=['n', 'days'], labels={'customer_state': 'State', 'late_rate': 'Pesanan terlambat'})
        fig.update_traces(marker_cornerradius=4,
                          hovertemplate='<b>%{x}</b><br>Terlambat: %{y:.1%}<br>%{customdata[0]:,} pesanan'
                                        '<br>Rata-rata %{customdata[1]:.1f} hari<extra></extra>')
        fig.add_hline(y=orders.is_late.mean(), line=dict(color=C['ink'], width=1),
                      annotation_text=f'rata-rata {orders.is_late.mean():.1%}', annotation_position='top right')
        fig.update_xaxes(categoryorder='array', categoryarray=s2.customer_state)
        fig.update_yaxes(tickformat='.0%')
        fig.update_layout(title='Persentase keterlambatan per state')
        st.plotly_chart(theme=None, figure_or_data=style_fig(fig, 400), width='stretch')
    with c2:
        sdf['size'] = np.sqrt(sdf.n)
        fig = px.scatter(sdf, x='days', y='review', size='size', color='region', text='customer_state', size_max=42,
                         color_discrete_map=REGION_COLORS,
                         labels={'days': 'Rata-rata lama kirim (hari)', 'review': 'Rata-rata review'})
        fig.update_traces(textposition='middle center', textfont=dict(size=9, color='white'),
                          marker=dict(line=dict(color='white', width=1.5), opacity=0.9),
                          hovertemplate='<b>%{text}</b><br>%{x:.1f} hari · review %{y:.2f}<extra></extra>')
        fig.update_layout(title='Lama kirim vs review per state')
        st.plotly_chart(theme=None, figure_or_data=style_fig(fig, 400), width='stretch')
    worst = sdf[sdf.n >= 30].sort_values('late_rate', ascending=False).head(3)
    if len(worst):
        insight(f"State dengan keterlambatan tertinggi: <b>{', '.join(worst.customer_state)}</b>. "
                f"Review rata-rata mulai turun di bawah 4 saat pengiriman melewati <b>21 hari</b>, jadi target SLA "
                f"pengiriman ke wilayah ini sebaiknya ≤21 hari.", C['red'], '#fdeeee')

# =============================================================================
# Tab 4 - RFM
# =============================================================================
with tab4:
    rfm = build_rfm(orders)
    seg = (rfm.groupby('segment')
           .agg(customers=('customer_unique_id', 'count'), revenue=('monetary', 'sum'),
                recency=('recency', 'mean'), frequency=('frequency', 'mean'), monetary=('monetary', 'mean'))
           .reset_index())
    seg['pct_c'] = seg.customers / seg.customers.sum()
    seg['pct_r'] = seg.revenue / seg.revenue.sum()

    c1, c2, c3 = st.columns(3)
    c1.metric('🕒 Rata-rata Recency', f'{rfm.recency.mean():.0f} hari')
    c2.metric('🔁 Pelanggan repeat order', f'{(rfm.frequency > 1).mean():.1%}')
    c3.metric('💳 Rata-rata Monetary', brl(rfm.monetary.mean()))

    c1, c2 = st.columns([1, 1.2])
    with c1:
        fig = px.treemap(seg, path=['segment'], values='customers', color='segment',
                         color_discrete_map=SEGMENT_COLORS)
        fig.update_traces(texttemplate='<b>%{label}</b><br>%{value:,} pelanggan<br>%{percentRoot:.1%}',
                          textfont_size=13, marker=dict(line=dict(color='white', width=3)),
                          hovertemplate='<b>%{label}</b><br>%{value:,} pelanggan<extra></extra>')
        fig.update_traces(root_color='white')
        fig.update_layout(title='Komposisi pelanggan per segmen')
        st.plotly_chart(theme=None, figure_or_data=style_fig(fig, 420, legend=False), width='stretch')
    with c2:
        long = seg.melt(id_vars='segment', value_vars=['pct_c', 'pct_r'], var_name='metric', value_name='pct')
        long['metric'] = long.metric.map({'pct_c': 'Porsi pelanggan', 'pct_r': 'Porsi revenue'})
        order = seg.sort_values('pct_r').segment
        fig = px.bar(long, y='segment', x='pct', color='metric', barmode='group', orientation='h',
                     color_discrete_map={'Porsi pelanggan': '#9ec5f4', 'Porsi revenue': C['orange']},
                     category_orders={'segment': list(order)[::-1]})
        fig.update_traces(marker_cornerradius=4, hovertemplate='%{y}: %{x:.1%}<extra>%{fullData.name}</extra>')
        fig.update_xaxes(tickformat='.0%', title=None)
        fig.update_yaxes(title=None)
        fig.update_layout(title='Porsi pelanggan vs porsi revenue')
        st.plotly_chart(theme=None, figure_or_data=style_fig(fig, 420), width='stretch')

    st.markdown('#### 🎯 Strategi per segmen')
    actions = {
        'Loyal Customers': 'Program membership, early access promo, dan reward poin.',
        'Promising High Value': 'Dorong pembelian kedua dengan rekomendasi produk dan voucher cross-sell.',
        'New Customers': 'Onboarding email dan voucher ongkir untuk order kedua.',
        'Need Attention': 'Promo personal berdasarkan kategori yang pernah dibeli.',
        "Can't Lose Them": 'Kampanye win-back dengan diskon besar; nilai belanjanya tinggi.',
        'At Risk Loyal': 'Hubungi ulang dengan penawaran eksklusif sebelum benar-benar hilang.',
        'Hibernating': 'Kampanye berbiaya rendah (newsletter musiman).',
    }
    picked = st.pills('Pilih segmen', list(SEGMENT_COLORS), default="Can't Lose Them", key='seg_pick')
    picked = picked or "Can't Lose Them"
    row = seg[seg.segment == picked]
    c1, c2 = st.columns([1, 1.4])
    with c1:
        if len(row):
            r = row.iloc[0]
            st.markdown(f"""<div class="seg-card" style="background:{SEGMENT_COLORS[picked]}">
                <h4>{picked}</h4>
                <p>👥 {r.customers:,} pelanggan ({r.pct_c:.1%}) · 💰 {r.pct_r:.1%} revenue</p>
                <p>🕒 Recency {r.recency:.0f} hari · 🔁 {r.frequency:.2f}x · 💳 {brl(r.monetary)}/pelanggan</p>
                <p style="margin-top:8px"><b>Aksi:</b> {actions[picked]}</p></div>""", unsafe_allow_html=True)
        else:
            st.info('Tidak ada pelanggan di segmen ini untuk filter yang dipilih.')
    with c2:
        top_c = (rfm[rfm.segment == picked].sort_values('monetary', ascending=False).head(8)
                 [['customer_unique_id', 'state', 'recency', 'frequency', 'monetary']])
        top_c['customer_unique_id'] = top_c.customer_unique_id.str[:12] + '…'
        rows = ''.join(f'<tr><td><code>{r.customer_unique_id}</code></td><td>{r.state}</td><td class="num">{r.recency:,}</td>'
                       f'<td class="num">{r.frequency}</td><td class="num">R$ {r.monetary:,.2f}</td></tr>'
                       for r in top_c.itertuples())
        st.markdown('<table class="tbl"><tr><th>Pelanggan</th><th>State</th><th>Recency (hari)</th><th>Frequency</th>'
                    f'<th>Monetary</th></tr>{rows}</table>', unsafe_allow_html=True)
    with st.expander('ℹ️ Cara segmentasi dibuat'):
        st.markdown("""
- **R** dan **M** diberi skor 1–5 dengan binning kuantil (R makin baru makin tinggi).
- **F** diberi skor dengan aturan bisnis: 1 pesanan = 1, 2 pesanan = 2, ≥3 pesanan = 3, karena ±97% pelanggan hanya belanja sekali.
- Segmen ditentukan dengan aturan manual (tanpa machine learning), misalnya *Can't Lose Them* = R ≤ 2 dan M ≥ 4.
""")

# =============================================================================
# Tab 5 - Peta
# =============================================================================
with tab5:
    c1, c2 = st.columns([1, 1])
    map_metric = c1.segmented_control('Warna bubble berdasarkan',
                                      ['Pesanan terlambat', 'Rata-rata review', 'Revenue'],
                                      default='Pesanan terlambat', key='map_metric') or 'Pesanan terlambat'
    view = c2.segmented_control('Tampilan', ['Bubble per state', 'Kepadatan pelanggan'],
                                default='Bubble per state', key='map_view') or 'Bubble per state'
    geo_state = (orders.dropna(subset=['lat', 'lng']).groupby('customer_state')
                 .agg(lat=('lat', 'mean'), lng=('lng', 'mean'), n=('order_id', 'count'),
                      late=('is_late', 'mean'), review=('review_score', 'mean'), revenue=('revenue', 'sum'))
                 .reset_index())
    if view == 'Bubble per state':
        col, scale, fmt, title = {
            'Pesanan terlambat': ('late', WARM_SCALE, '.0%', 'Terlambat'),
            'Rata-rata review': ('review', ['#d1373f', '#f6e7a1', '#1a8a4a'], '.2f', 'Review'),
            'Revenue': ('revenue', BLUE_SCALE, ',.0f', 'Revenue (R$)'),
        }[map_metric]
        bg = orders.dropna(subset=['lat', 'lng'])
        bg = bg.sample(min(len(bg), 15000), random_state=1)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=bg.lng, y=bg.lat, mode='markers', hoverinfo='skip', showlegend=False,
                                 marker=dict(size=4, color='#86b6ef', opacity=0.4)))
        fig.add_trace(go.Scatter(
            y=geo_state.lat, x=geo_state.lng, text=geo_state.customer_state, mode='markers+text',
            textposition='middle center', textfont=dict(size=10, color='white'),
            customdata=np.stack([geo_state.n, geo_state.late, geo_state.review, geo_state.revenue], axis=1),
            marker=dict(size=np.sqrt(geo_state.n) / np.sqrt(geo_state.n.max()) * 60 + 14, color=geo_state[col],
                        colorscale=scale, line=dict(color='white', width=1.5), opacity=0.92,
                        colorbar=dict(title=title, tickformat=fmt, thickness=14, len=0.7)),
            hovertemplate='<b>%{text}</b><br>%{customdata[0]:,} pesanan<br>Terlambat: %{customdata[1]:.1%}'
                          '<br>Review: %{customdata[2]:.2f}<br>Revenue: R$ %{customdata[3]:,.0f}<extra></extra>',
            showlegend=False))
        fig.update_layout(title=f'{map_metric} per state (ukuran bubble = jumlah pesanan)')
    else:
        pts = orders.dropna(subset=['lat', 'lng'])
        pts = pts.sample(min(len(pts), 30000), random_state=1)
        fig = go.Figure()
        for reg_name, color in REGION_COLORS.items():
            d = pts[pts.region == reg_name]
            fig.add_trace(go.Scatter(x=d.lng, y=d.lat, mode='markers', name=reg_name,
                                     marker=dict(size=3, color=color, opacity=0.55),
                                        hovertemplate=f'{reg_name}<extra></extra>'))
        fig.update_layout(title='Sebaran lokasi pelanggan per wilayah (sampel titik)',
                          legend=dict(itemsizing='constant', orientation='h', y=1.0, yanchor='bottom', x=0))
    fig.update_xaxes(range=[-75, -33], visible=False)
    fig.update_yaxes(range=[-35, 6], visible=False, scaleanchor='x', scaleratio=1)
    fig.update_layout(height=680, margin=dict(l=0, r=0, t=70, b=0), paper_bgcolor='white', plot_bgcolor='white',
                      font=dict(family='Inter, Segoe UI, sans-serif', color=C['ink']),
                      title=dict(text=f'<b>{fig.layout.title.text}</b>', x=0.01, y=0.98, yref='container', font=dict(size=16)))
    st.plotly_chart(fig, theme=None, width='stretch')
    insight('Pelanggan sangat terkonsentrasi di tenggara (SP, RJ, MG), sedangkan bubble dengan keterlambatan tinggi '
            'berkumpul di pesisir timur laut yang jauh dari pusat penjual. Gunakan zoom & hover untuk melihat detail tiap state.',
            C['aqua'], '#e9f7f1')

st.caption('© 2026 · Horasio · Data: Olist Brazilian E-Commerce Public Dataset (Kaggle)')