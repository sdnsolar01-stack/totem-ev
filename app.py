import streamlit as st
import time

# Configuração da página
st.set_page_config(page_title="SDN EV - Totem", layout="centered", initial_sidebar_state="collapsed")

# Remover elementos visuais padrão
st.markdown("""
    <style>
    .stApp { background-color: black; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

if "tela" not in st.session_state:
    st.session_state.tela = 1
if "valor" not in st.session_state:
    st.session_state.valor = 0

# --- TELA 1: INÍCIO ---
if st.session_state.tela == 1:
    st.image("tela1_inicio.jpg")
    
    col1, col2, col3 = st.columns([3, 2, 1])
    with col3:
        if st.button("▶ INICIAR"):
            st.session_state.tela = 2
            st.rerun()

# --- TELA 2: SELEÇÃO DE VALORES ---
elif st.session_state.tela == 2:
    st.image("tela2_valores.jpg")
    
    st.markdown("<h3 style='text-align: center; color: white;'>Selecione o valor da recarga:</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("R$ 20,00"):
            st.session_state.valor = 20
            st.session_state.tela = 3
            st.rerun()
        if st.button("R$ 40,00"):
            st.session_state.valor = 40
            st.session_state.tela = 3
            st.rerun()
    with col2:
        if st.button("R$ 30,00"):
            st.session_state.valor = 30
            st.session_state.tela = 3
            st.rerun()
        if st.button("R$ 50,00"):
            st.session_state.valor = 50
            st.session_state.tela = 3
            st.rerun()

# --- TELA 3: PAGAMENTO ---
elif st.session_state.tela == 3:
    st.image("tela3_pagamento.jpg")
    st.markdown(f"<h2 style='text-align: center; color: #00FF66;'>VALOR SELECIONADO: R$ {st.session_state.valor},00</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: white;'>Aguardando confirmação de pagamento...</h4>", unsafe_allow_html=True)
    
    time.sleep(5)
    st.session_state.tela = 4
    st.rerun()

# --- TELA 4: CARREGANDO (SIMULAÇÃO DINÂMICA) ---
elif st.session_state.tela == 4:
    placeholder = st.empty()
    
    for i in range(1, 15):
        kwh = i * 1.31
        tempo = i * 2
        porc = i * 7
        if porc > 100: porc = 100
        
        with placeholder.container():
            st.image("tela4_carregando.jpg")
            st.markdown(f"""
                <div style='text-align: center; color: white; font-family: monospace; font-size: 22px;'>
                    <b>⚡ {kwh:.2f} kWh</b> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; <b>⏱️ {tempo} min</b> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; <b>🔋 {porc}%</b>
                </div>
            """, unsafe_allow_html=True)
        time.sleep(1)
    
    time.sleep(2)
    st.session_state.tela = 1
    st.rerun()