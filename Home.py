import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon="🏠",
    layout='wide'
)


image_path='imagens/logo.png'
image=Image.open(image_path)
st.sidebar.image(image,width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write('# Curry Company Growth Dashboard')

st.markdown(
    """ 
    Dashboar Criado para acompanhar principais métricas da Curry Company.

    #### COMO USAR O DASHBOARD?
    * Visão de Negócio
        * Visão Gerencial   : Métricas gerais de comportamento
        * Visão Tática      : Reports semanais de crescimento
        * Visão Geográfica  : insigts de localização
    * Visão de Entregadores
        * Acompanhamento das métircas semanais de crescimento
    * Visão de Restaurantes
        * Indicadores semanais de crescimento dos restaurantes
    
    #### AJUDA
    email do suporte: 
        matheus.salles_1994@hotmail.com

"""
)

