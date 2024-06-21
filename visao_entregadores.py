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
st.header('Market Place - Visão Entregador')

#========================================
#Layout
#========================================

v_gerencial,v_tatica,v_geografica=st.tabs(['Vistão Gerencial',
                                 '_',
                                 '_'])

#========================================
with v_gerencial:

    with st.container():
        st.markdown(""" # Overall Metrics""")
        vg_col1,vg_col2,vg_col3,vg_col4=st.columns(4)
        with vg_col1:
        
            maior_idade=data['Delivery_person_Age'].max()
            vg_col1.metric('Maior idade',maior_idade)

        with vg_col2:
            menor_idade=data['Delivery_person_Age'].min()
            vg_col2.metric('Menor idade',menor_idade)

        with vg_col3:
            melhor_condicao=data['Vehicle_condition'].max()
            vg_col3.metric('Melhor Condição ',melhor_condicao)

        with vg_col4:
            pior_condicao=data['Vehicle_condition'].min()
            vg_col4.metric('Pior Condição ',pior_condicao)
    st.markdown("---")

    #================

    with st.container():
        st.markdown(""" # Avaliações""" )

        vg_col1,vg_col2=st.columns(2)
        with vg_col1:
            st.markdown('##### Avaliação média por entregador')
            
            df_rating=(data .groupby(['Delivery_person_ID'])[['Delivery_person_Ratings']]
                            .mean()
                            .reset_index())
            st.dataframe(df_rating,hide_index=True,height=550)

        with vg_col2:

            with st.container():
                st.markdown('##### Avaliação média por trânsito')
                df_rating=(data .groupby(['Road_traffic_density'])[['Delivery_person_Ratings']]
                                .agg(['mean', 'std'])
                                .reset_index())
                df_rating.columns=['Road_traffic_density','Delivery_mean','Delivery_std']
                st.dataframe(df_rating,hide_index=True)
            st.markdown("---")

            with st.container():
                st.markdown('##### Avaliação média por clima')
                df_rating=(data .groupby(['Weatherconditions'])[['Delivery_person_Ratings']]
                                .agg(['mean', 'std'])
                                .reset_index())
                df_rating.columns=['Weatherconditions','Delivery_mean','Delivery_std']
                st.dataframe(df_rating,hide_index=True)

    st.markdown("---")

    #================

    with st.container():
        st.markdown(""" # Velocidade de Entrega """)

        vg_col1,vg_col2=st.columns(2)

        with vg_col1:
            st.markdown('Top 10 mais rápidos')

            def top10_rapidos():
                df_x=data.copy()

                df_x['tempo']=df_x['Time_taken(min)'].map(lambda x:float(x.replace('(min)','')))
                df_x=(df_x  .groupby(['City','Delivery_person_ID'])[['tempo']]
                            .mean()
                            .reset_index()
                            .sort_values(by='tempo')
                            .reset_index(drop=True))
                
                df_x.index=df_x.index+1
                df_x=df_x.head(10)
                st.dataframe(df_x)
            top10_rapidos()
            
            
        with vg_col2:
            st.markdown('Top 10 mais lentos')
            def top10_lentos():
                df_x=data.copy()
                df_x['tempo']=df_x['Time_taken(min)'].map(lambda x:float(x.replace('(min)','')))
                df_x=(df_x  .groupby(['City','Delivery_person_ID'])[['tempo']]
                            .mean()
                            .reset_index()
                            .sort_values(by='tempo',ascending=False)
                            .reset_index(drop=True))
                df_x.index=df_x.index+1
                df_x=df_x.head(10)
                st.dataframe(df_x)
            top10_lentos()
            
    st.markdown("---")
#========================================
with v_tatica:
    pass

#========================================
with v_geografica:
    pass
    