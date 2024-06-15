
#========================================
#prepare data
from A0_data import read_data,clean_data
data=read_data()
data=clean_data(data=data)
#========================================
#bibliotecas
from datetime import datetime
import plotly as px

#========================================
#layout
#========================================
import streamlit as st

#========================================
#Barra Lateral
#========================================
st.sidebar.image('./imagens/logo.png',width=120)
st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

date_slider=st.sidebar.slider(
                        'Até qual valor?',
                        value=datetime(2022,4,13),
                        min_value=datetime(2022,2,11),
                        max_value=datetime(2022,4,6),
                        format="DD-MM-YYYY"
                    )

st.sidebar.markdown("""---""")
traffic_options=st.sidebar.multiselect('Quais as condições do trânsito',
                      ['Low','Medium','High','Jam'],
                      default=['Low','Medium','High','Jam'])
#========================================
#Header
#========================================
st.header('Market Place - Visão Empresa')
st.header(date_slider)

#========================================
#Layout
#========================================

tab1,tab2,tab3=st.tabs(['Vistão Gerencial','Visão Tática','Visão Geográfica'])

with tab1:
    st.markdown('# Orders by Day')
    st.markdown('#teste')
    fig=px.bar(data,x='Order_Date',y='ID')
    st.plotly_chart(fig,use_container_width=True)
    
with tab2:
    pass
with tab2:
    pass