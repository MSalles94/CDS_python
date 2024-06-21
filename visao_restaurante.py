#streamlit run visao_negocio.py

#========================================
#prepare data
from A0_data import read_data,clean_data
data=read_data()
data=clean_data(data=data)
#========================================
#bibliotecas
from datetime import datetime
import plotly.express as px

#========================================
#layout
#========================================
import streamlit as st

#========================================
#Barra Lateral
#========================================
def criar_barra_lateral():
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
    city=st.sidebar.multiselect('Tipo de cidade',
                        ['Urban', 'Metropolitian', 'Semi-Urban'],
                        default=['Urban', 'Metropolitian', 'Semi-Urban'])
    st.sidebar.markdown("""---""")
    filtro_linhas=((data['Order_Date']<date_slider)&
               (data['Road_traffic_density'].isin(traffic_options))&
               (data['City'].isin(city)))
    return filtro_linhas

filtro_linhas=criar_barra_lateral()

#aplicar filtro
data=data.loc[filtro_linhas,:]

#========================================
#Header
#========================================
st.header('Market Place - Visão Restaurantes')

#========================================
#Layout
#========================================

v_gerencial,v_tatica,v_geografica=st.tabs(['Vistão Gerencial',
                                 '_',
                                 '_'])

#========================================
with v_gerencial:

    with st.container():
        c1,c2,c3,c4,c5,c6=st.columns(6)

        with c1:
            entregador_unico=len(data['Delivery_person_ID'].unique())
            st.metric('Entregadores',entregador_unico)
        with c2:
            def calc_distancia_media(data):
                def calc_distancia(row):
                    lat=row['Restaurant_latitude']-row['Delivery_location_latitude']
                    lon=row['Restaurant_longitude']-row['Delivery_location_longitude']
                    dist=((lat**2)+(lon**2))**(1/2)
                    return dist
                data['distancia']=data.apply(calc_distancia,axis=1)
                return data['distancia'].mean()
            distancia_media=calc_distancia_media(data)
            st.metric('Distancia Média',distancia_media)
        with c3:
            mean_delivery_time=data[data['Festival']=='Yes']['Deliver_time'].mean().round(2)
            st.metric('Tempo médio c/Festival',mean_delivery_time)
        with c4:
            std_delivery_time=data[data['Festival']=='Yes']['Deliver_time'].std().round(2)
            st.metric('Desvio Tempo c/Festival  ',std_delivery_time)
        with c5:
            mean_delivery_time=data[data['Festival']=='No']['Deliver_time'].mean().round(2)
            st.metric('Tempo médio s/Festival',mean_delivery_time)
        with c6:
            std_delivery_time=data[data['Festival']=='No']['Deliver_time'].std().round(2)
            st.metric('Desvio Tempo s/Festival  ',std_delivery_time)
    st.markdown('---')

    with st.container():
        st.markdown('distancia media por cidade')

    st.markdown('---')

    with st.container():

        c1,c2=st.columns(2)

        with c1:
            st.markdown('distribuição do tempo por cidade')
            def tempo_medio_cidade():
                #tempo de entrega médio por cidade
                st.markdown('## Tempo médio de entrega por cidade')

                from plotly import express as py
                df_aux=data.groupby(['City'])['Deliver_time'].mean().reset_index()

                fig=py.pie(data_frame=df_aux,names='City',values='Deliver_time')
                st.plotly_chart(fig,use_container_width=True)
            tempo_medio_cidade()
        with c2:
            st.markdown('Tempo médio por tipo de entrega')
    st.markdown('---')

    with st.container():
        st.markdown('Tempo médio por cidade e trafego')
            
            
    st.markdown("---")

#========================================
with v_tatica:
    pass

#========================================
with v_geografica:
    pass
    