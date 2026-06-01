import pandas as pd
import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime

st.set_page_config(
    page_title='Calendário Solicitações',
    page_icon=':calendar:',
    layout='wide'
)

# -------------------------------------------------------
# ESTILOS GLOBAIS
# -------------------------------------------------------
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .stApp { background-color: #F2F5FB; }

        .page-header {
            background: linear-gradient(135deg, #011E6B 0%, #0A4FD4 100%);
            border-radius: 14px;
            padding: 22px 30px;
            margin-bottom: 18px;
            box-shadow: 0 4px 18px rgba(1,30,107,0.18);
        }
        .page-header h1 {
            color: #FFFFFF;
            font-size: 20px;
            font-weight: 700;
            margin: 0 0 3px 0;
            font-family: Arial, sans-serif;
            letter-spacing: 0.2px;
        }
        .page-header p {
            color: #A8C8F8;
            font-size: 12px;
            margin: 0;
            font-family: Arial, sans-serif;
        }

        .filter-card {
            background: #FFFFFF;
            border-radius: 12px;
            padding: 18px 22px 14px 22px;
            margin-bottom: 14px;
            border: 1px solid #DDE6F5;
            box-shadow: 0 2px 8px rgba(2,42,137,0.05);
        }

        .section-label {
            font-size: 10.5px;
            font-weight: 700;
            color: #8494B4;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .legend-wrap {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }
        .legend-pill {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            font-size: 12.5px;
            font-weight: 500;
            color: #1E2D52;
            background: #F5F8FF;
            border-radius: 999px;
            padding: 5px 13px 5px 9px;
            border: 1.5px solid #DDE6F5;
            white-space: nowrap;
        }
        .legend-dot {
            width: 11px;
            height: 11px;
            border-radius: 50%;
            flex-shrink: 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.15);
        }

        div[data-testid="stSelectbox"] label {
            font-size: 11px !important;
            font-weight: 700 !important;
            color: #5A6E96 !important;
            text-transform: uppercase;
            letter-spacing: 0.7px;
        }
        div[data-testid="stSelectbox"] > div > div {
            border-radius: 9px !important;
            border: 1.5px solid #C8D8EE !important;
            background-color: #FAFCFF !important;
            font-size: 13.5px !important;
        }

        .detail-card {
            background: #FFFFFF;
            border-radius: 12px;
            border: 1px solid #DDE6F5;
            box-shadow: 0 2px 10px rgba(2,42,137,0.07);
            overflow: hidden;
            margin-top: 18px;
        }
        .detail-card-header {
            background: linear-gradient(135deg, #011E6B 0%, #0A4FD4 100%);
            padding: 15px 22px;
            color: #FFFFFF;
            font-size: 15px;
            font-weight: 600;
            font-family: Arial, sans-serif;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .detail-card-header .badge {
            background: rgba(255,255,255,0.2);
            border-radius: 999px;
            padding: 2px 11px;
            font-size: 12px;
            font-weight: 500;
        }
        .detail-card-body { padding: 6px; }

        div[data-testid="stDataFrame"] { border-radius: 0 !important; }
    </style>
""", unsafe_allow_html=True)


# -------------------------------------------------------
# CABEÇALHO
# -------------------------------------------------------
st.markdown("""
    <div class="page-header">
        <h1>📅 Calendário de Solicitações</h1>
        <p>Universidade Católica de Brasília &nbsp;·&nbsp; Portal Atende</p>
    </div>
""", unsafe_allow_html=True)


# -------------------------------------------------------
# CARREGAMENTO DOS DADOS
# -------------------------------------------------------
@st.cache_data
def carregar_dados():
    df = pd.read_csv('data/atendimentos.csv', encoding='latin1', sep=';')
    df['Abertura']   = pd.to_datetime(df['Abertura'],   dayfirst=True, errors='coerce')
    df['Fechamento'] = pd.to_datetime(df['Fechamento'], dayfirst=True, errors='coerce')
    return df

df = carregar_dados()


# -------------------------------------------------------
# PALETA DE STATUS
# Complementar ao azul marinho do site.
# Todos passam contraste WCAG AA sobre branco.
#
#  Terracota  — Em andamento       (quente/ativo)
#  Esmeralda  — Concluído confirm. (positivo/encerrado)
#  Violeta    — Concluído a resp.  (pendência/aguarda)
#  Ardósia    — Cancelado          (neutro/inativo)
# -------------------------------------------------------
cores_status = {
    'Em andamento':          '#B84E1A',
    'Concluído confirmado':  '#1A7055',
    'Concluído a responder': '#513DA0',
    'Cancelado':             '#52637E',
}

def cor_evento(status):
    return cores_status.get(status, '#0A4FD4')


# -------------------------------------------------------
# FILTROS + LEGENDA
# -------------------------------------------------------
st.markdown('<div class="filter-card">', unsafe_allow_html=True)
col_tipo, col_modo, col_leg = st.columns([1, 1, 2])

with col_tipo:
    tipos = ['Todos'] + sorted(df['TIPO_ABERTURA'].dropna().unique().tolist())
    tipo_selecionado = st.selectbox('Tipo de Atendimento', tipos)

with col_modo:
    modos_traduzidos = {
        'Visão Mensal':      'daygrid',
        'Visão Semanal':     'timegrid',
        'Linha do Tempo':    'timeline',
        'Lista de Demandas': 'list',
        'Múltiplos Meses':   'multimonth',
    }
    modo_selecionado = st.selectbox('Modo de Visualização', list(modos_traduzidos.keys()))

with col_leg:
    st.markdown('<div class="section-label">Legenda de Status</div>', unsafe_allow_html=True)
    pills = ''.join([
        f'<span class="legend-pill">'
        f'<span class="legend-dot" style="background:{cor}"></span>{label}'
        f'</span>'
        for label, cor in cores_status.items()
    ])
    st.markdown(f'<div class="legend-wrap">{pills}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

mode = modos_traduzidos[modo_selecionado]


# -------------------------------------------------------
# FILTRO + PREPARAÇÃO DOS DADOS
# -------------------------------------------------------
df_filtrado = df.copy()
if tipo_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['TIPO_ABERTURA'] == tipo_selecionado]

df_valido = df_filtrado.dropna(subset=['Abertura']).copy()
df_valido['data_abertura'] = df_valido['Abertura'].dt.strftime('%Y-%m-%d')


# -------------------------------------------------------
# GERAÇÃO DE EVENTOS
# - daygrid / multimonth  → data só (sem hora) → blocos de dia inteiro
# - timegrid / timeline   → com horário        → exibição por hora
# - list                  → com horário        → listagem precisa
# -------------------------------------------------------
events = []
usar_hora = mode in ('timegrid', 'timeline', 'list')

for _, row in df_valido.iterrows():
    if usar_hora:
        inicio = row['Abertura'].strftime('%Y-%m-%dT%H:%M:%S')
        fim    = (
            row['Fechamento'].strftime('%Y-%m-%dT%H:%M:%S')
            if pd.notna(row['Fechamento'])
            else (row['Abertura'] + pd.Timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
        )
    else:
        inicio = row['Abertura'].strftime('%Y-%m-%d')
        fim    = (
            (row['Fechamento'] + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
            if pd.notna(row['Fechamento'])
            else (row['Abertura'] + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        )

    events.append({
        'title': f"{row['Atendimento']} | {row['Assunto']}",
        'color': cor_evento(row['Status']),
        'start': inicio,
        'end':   fim,
        'extendedProps': {
            'data_dia':   row['data_abertura'],
            'status':     str(row['Status']),
            'campus':     str(row['CAMPUS']),
            'atendente':  str(row['Atendente responsável']),
            'tipo':       str(row['TIPO_ABERTURA']),
            'abertura':   row['Abertura'].strftime('%d/%m/%Y %H:%M'),
            'fechamento': row['Fechamento'].strftime('%d/%m/%Y %H:%M') if pd.notna(row['Fechamento']) else 'Em aberto',
        }
    })


# -------------------------------------------------------
# OPÇÕES DO CALENDÁRIO
# -------------------------------------------------------
data_hoje = datetime.now().strftime('%Y-%m-%d')

base = {
    'themeSystem': 'bootstrap5',
    'navLinks':    'true',
    'selectable':  'true',
    'locale':      'pt-br',
    'buttonText': {
        'today':         'Hoje',
        'dayGridMonth':  'Mês',
        'dayGridWeek':   'Semana',
        'dayGridDay':    'Dia',
        'timeGridWeek':  'Semana',
        'timeGridDay':   'Dia',
        'timelineMonth': 'Mês',
        'timelineWeek':  'Semana',
        'timelineDay':   'Dia',
        'list':          'Lista',
    },
    'initialDate': data_hoje,
}

if mode == 'daygrid':
    calendar_options = {
        **base,
        'initialView':  'dayGridMonth',
        'dayMaxEvents': 2,
        'headerToolbar': {
            'left':   'today prev,next',
            'center': 'title',
            'right':  'dayGridDay,dayGridWeek,dayGridMonth',
        },
    }
elif mode == 'timegrid':
    calendar_options = {
        **base,
        'initialView':   'timeGridWeek',
        'eventMaxStack': 10,   # semanal/diário: mostra até 10 por coluna de hora
        'headerToolbar': {
            'left':  'title',
            'right': 'today prev,next timeGridDay,timeGridWeek',
        },
    }
elif mode == 'timeline':
    calendar_options = {
        **base,
        'initialView': 'timelineMonth',
        'headerToolbar': {
            'left':   'today prev,next',
            'center': 'title',
            'right':  'timelineDay,timelineWeek,timelineMonth',
        },
    }
elif mode == 'list':
    calendar_options = {
        **base,
        'initialView': 'listMonth',
        'headerToolbar': {
            'left':   'today prev,next',
            'center': 'title',
            'right':  '',
        },
    }
elif mode == 'multimonth':
    calendar_options = {
        **base,
        'initialView':  'multiMonthYear',
        'dayMaxEvents': 2,
    }


# -------------------------------------------------------
# RENDERIZAÇÃO DO CALENDÁRIO
# -------------------------------------------------------
state = calendar(
    events=events,
    options=calendar_options,
    custom_css="""
    /* Fundo e borda */
    .fc {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 2px 12px rgba(2,42,137,0.07);
    }

    /* Eventos */
    .fc-event {
        border-radius: 6px !important;
        border: none !important;
        font-size: 11.5px !important;
        padding: 1px 5px !important;
    }
    .fc-event-past  { opacity: 0.70; }
    .fc-event-time  { font-style: normal; font-size: 10.5px; opacity: 0.80; }
    .fc-event-title { font-weight: 600; }

    /* Botões */
    .fc-button-primary {
        background-color: #022A89 !important;
        border-color: #022A89 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        font-size: 12.5px !important;
        font-weight: 600 !important;
        padding: 5px 15px !important;
        letter-spacing: 0.2px;
        box-shadow: 0 2px 6px rgba(2,42,137,0.2) !important;
    }
    .fc-button-primary:hover {
        background-color: #011C5C !important;
        border-color: #011C5C !important;
    }
    .fc-button-primary:not(:disabled).fc-button-active {
        background-color: #FFCC00 !important;
        border-color: #FFCC00 !important;
        color: #022A89 !important;
        box-shadow: none !important;
    }

    /* Título */
    .fc-toolbar-title {
        font-size: 1.35rem !important;
        color: #011E6B !important;
        font-family: Arial, sans-serif;
        font-weight: 700;
        letter-spacing: -0.3px;
    }

    /* Cabeçalho dos dias */
    .fc-col-header-cell {
        background-color: #F0F4FA !important;
        border-color: #DDE6F5 !important;
    }
    .fc-col-header-cell-cushion {
        color: #022A89 !important;
        font-weight: 700;
        font-size: 12.5px;
        text-decoration: none !important;
        padding: 8px 4px !important;
    }

    /* Células dos dias */
    .fc-daygrid-day {
        border-color: #E8EEF8 !important;
    }
    .fc-daygrid-day-number {
        color: #2C3E6B !important;
        font-weight: 600;
        font-size: 13px;
        text-decoration: none !important;
    }
    .fc-day-today {
        background-color: #EBF0FF !important;
    }
    .fc-day-today .fc-daygrid-day-number {
        background: #022A89;
        color: #FFFFFF !important;
        border-radius: 50%;
        width: 26px;
        height: 26px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Link "+X mais" */
    .fc-daygrid-more-link {
        background: #EBF0FF !important;
        color: #022A89 !important;
        font-weight: 700;
        font-size: 11px;
        border-radius: 4px;
        padding: 1px 5px !important;
    }

    /* Timegrid linhas de hora */
    .fc-timegrid-slot {
        border-color: #EEF2FA !important;
        height: 36px !important;
    }
    .fc-timegrid-slot-label {
        font-size: 11px;
        color: #7A8FAF !important;
    }

    /* Lista */
    .fc-list-event:hover td { background: #F0F4FF !important; }
    .fc-list-day-cushion { background: #F0F4FA !important; }
    .fc-list-day-text, .fc-list-day-side-text {
        color: #022A89 !important;
        font-weight: 700;
    }
    """,
    key=mode
)


# -------------------------------------------------------
# DETALHES AO CLICAR
# -------------------------------------------------------
if state.get('eventClick'):
    ext      = state['eventClick']['event'].get('extendedProps', {})
    data_dia = ext.get('data_dia')

    if data_dia:
        df_dia         = df_valido[df_valido['data_abertura'] == data_dia].copy()
        data_formatada = pd.to_datetime(data_dia).strftime('%d/%m/%Y')

        st.markdown(f"""
            <div class="detail-card">
                <div class="detail-card-header">
                    📋 Solicitações de {data_formatada}
                    <span class="badge">{len(df_dia)} registro(s)</span>
                </div>
                <div class="detail-card-body">
        """, unsafe_allow_html=True)

        st.dataframe(
            df_dia[[
                'Atendimento', 'Assunto', 'Status',
                'CAMPUS', 'Atendente responsável',
                'TIPO_ABERTURA', 'Abertura', 'Fechamento'
            ]].rename(columns={
                'Atendente responsável': 'Atendente',
                'TIPO_ABERTURA':         'Tipo',
            }).reset_index(drop=True),
            use_container_width=True,
            height=320,
        )

        st.markdown('</div></div>', unsafe_allow_html=True)
