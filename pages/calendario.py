import pandas as pd
import streamlit as st

from streamlit_calendar import calendar
from datetime import datetime
st.set_page_config(page_title='Calendário Solicitações',
                   page_icon=':calendar:',
                   layout='centered')

# Estilos personalizados para o calendário
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
""", unsafe_allow_html=True)


# Mapeamento dos modos para os valores esperados pelo calendário
modos_traduzidos = {
    "Visão Geral": "daygrid",
    "Visão por Horário ": "timegrid",
    "Linha do Tempo": "timeline",
    "Lista de Demandas": "list",
    "Múltiplos Meses": "multimonth",
}
modo_selecionado = st.selectbox(
    "Selecione o modo do calendário:",
    options=list(modos_traduzidos.keys()),
)
mode = modos_traduzidos[modo_selecionado]

# Eventos de exemplo
events = [
    {
        "title": "Event 1",
        "color": "#FF6C6C",
        "start": "2026-07-03",
        "end": "2026-07-05",
        "resourceId": "a",
    },
    {
        "title": "Event 2",
        "color": "#FFBD45",
        "start": "2026-07-01",
        "end": "2026-07-10",
        "resourceId": "b",
    },
    {
        "title": "Event 3",
        "color": "#FF4B4B",
        "start": "2026-07-20",
        "end": "2026-07-20",
        "resourceId": "c",
    },
    {
        "title": "Event 4",
        "color": "#FF6C6C",
        "start": "2026-07-23",
        "end": "2026-07-25",
        "resourceId": "d",
    },
    {
        "title": "Event 5",
        "color": "#FFBD45",
        "start": "2026-07-29",
        "end": "2026-07-30",
        "resourceId": "e",
    },
    {
        "title": "Event 6",
        "color": "#FF4B4B",
        "start": "2026-07-28",
        "end": "2026-07-20",
        "resourceId": "f",
    },
    {
        "title": "Event 7",
        "color": "#FF4B4B",
        "start": "2026-07-01T08:30:00",
        "end": "2026-07-01T10:30:00",
        "resourceId": "a",
    },
    {
        "title": "Event 8",
        "color": "#3D9DF3",
        "start": "2026-07-01T07:30:00",
        "end": "2026-07-01T10:30:00",
        "resourceId": "b",
    },
    {
        "title": "Event 9",
        "color": "#3DD56D",
        "start": "2026-07-02T10:40:00",
        "end": "2026-07-02T12:30:00",
        "resourceId": "c",
    },
    {
        "title": "Event 10",
        "color": "#FF4B4B",
        "start": "2026-07-15T08:30:00",
        "end": "2026-07-15T10:30:00",
        "resourceId": "d",
    },
    {
        "title": "Event 11",
        "color": "#3DD56D",
        "start": "2026-07-15T07:30:00",
        "end": "2026-07-15T10:30:00",
        "resourceId": "e",
    },
    {
        "title": "Event 12",
        "color": "#3D9DF3",
        "start": "2026-07-21T10:40:00",
        "end": "2026-07-21T12:30:00",
        "resourceId": "f",
    },
    {
        "title": "Event 13",
        "color": "#FF4B4B",
        "start": "2026-07-17T08:30:00",
        "end": "2026-07-17T10:30:00",
        "resourceId": "a",
    },
    {
        "title": "Event 14",
        "color": "#3D9DF3",
        "start": "2026-07-17T09:30:00",
        "end": "2026-07-17T11:30:00",
        "resourceId": "b",
    },
    {
        "title": "Event 15",
        "color": "#3DD56D",
        "start": "2026-07-17T10:30:00",
        "end": "2026-07-17T12:30:00",
        "resourceId": "c",
    },
    {
        "title": "Event 16",
        "color": "#FF6C6C",
        "start": "2026-07-17T13:30:00",
        "end": "2026-07-17T14:30:00",
        "resourceId": "d",
    },
    {
        "title": "Event 17",
        "color": "#FFBD45",
        "start": "2026-07-17T15:30:00",
        "end": "2026-07-17T16:30:00",
        "resourceId": "e",
    },
]

# Configurações comuns para o calendário
calendar_options = {
    "themeSystem": "bootstrap5",
    "editable": "true",
    "navLinks": "true",
    "selectable": "true",
}


# Configurações específicas para cada modo
if mode == "daygrid":
    data_atual_formatada = datetime.now().strftime("%Y-%m-%d")
    calendar_options = {
        **calendar_options,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridDay,dayGridWeek,dayGridMonth",
        },
        "titleFormat": {
            "year": "numeric",
            "month": "long",
            "day": "numeric"
        },
        "buttonText": {
            "today":    'Hoje',
            "dayGridMonth":    'Mês',
            "dayGridWeek":     'Semana',
            "dayGridDay":      'Dia',
            "list":     'Lista'
        },
        "initialDate": data_atual_formatada,
        "initialView": "dayGridMonth",
    }
elif mode == "timegrid":
    calendar_options = {
        **calendar_options,
        "headerToolbar": {
            "left": "title",
            "right": "today prev,next timeGridDay,timeGridWeek",
        },
        "titleFormat": {
            "year": "numeric",
            "month": "long",
            "day": "numeric"
        },
        "buttonText": {
            "today":    'Hoje',
            "timeGridWeek":     'Semana',
            "timeGridDay":      'Dia',
            "list":     'lista'
        },
        "initialView": "timeGridWeek",
    }
elif mode == "timeline":
    data_atual_formatada = datetime.now().strftime("%Y-%m-%d")
    calendar_options = {
        **calendar_options,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "timelineDay,timelineWeek,timelineMonth",
        },
        "titleFormat": {
            "year": "numeric",
            "month": "long",
            "day": "numeric"
        },
        "buttonText": {
            "today":    'Hoje',
            "timelineMonth":    'Mês',
            "timelineWeek":     'Semana',
            "timelineDay":      'Dia',
            "list":     'lista'
        },
        "initialDate": data_atual_formatada,
        "initialView": "timelineMonth",
    }
elif mode == "list":
    data_atual_formatada = datetime.now().strftime("%Y-%m-%d")
    calendar_options = {
        **calendar_options,
        "buttonText": {
            "today":    'Hoje',
        },
        "initialDate": data_atual_formatada,
        "initialView": "listMonth",
    }
elif mode == "multimonth":
    calendar_options = {
        **calendar_options,
        "initialView": "multiMonthYear",
    }

# Renderiza o calendário com as opções e eventos configurados
state = calendar(
    events=st.session_state.get("events", events),
    options=calendar_options,
    custom_css="""

    /* Estilos personalizados para os eventos */
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    
        /* Estilos personalizados para os botões e título do calendário */
        .fc-button-primary {
            background-color: #022A89 !important; /* Força o azul UCB nos botões */
            border-color: #022A89 !important;
            color: #ffffff !important;
        }
        .fc-button-primary:hover {
            background-color: #011C5C !important; /* Azul mais escuro no hover */
            border-color: #011C5C !important;
        }
        .fc-button-active {
            background-color: #FFCC00 !important; /* Amarelo ouro para o botão ativo */
            border-color: #FFCC00 !important;
            color: #022A89 !important;
        }
        .fc-toolbar-title {
            font-size: 1.8rem;
            color: #022A89;
            font-family: Arial, sans-serif;
        }
    """,
    key=mode
)

