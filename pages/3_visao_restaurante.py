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

st.set_page_config(
    page_title='Visão Restaurantes',
    page_icon="🍽️",
    layout='wide'
)

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

    with st.container(): #metricas gerais
        st.markdown('## Métricas gerais')
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

            st.metric('Distancia Média',round(distancia_media,2))
        with c3:
            mean_delivery_time=data[data['Festival']=='Yes']['Deliver_time'].mean().round(2)
            st.metric('Tempo c/Fest.',mean_delivery_time)
        with c4:
            std_delivery_time=data[data['Festival']=='Yes']['Deliver_time'].std().round(2)
            st.metric('Std temp. c/Fest',std_delivery_time)
        with c5:
            mean_delivery_time=data[data['Festival']=='No']['Deliver_time'].mean().round(2)
            st.metric('Tempo s/Fest',mean_delivery_time)
        with c6:
            std_delivery_time=data[data['Festival']=='No']['Deliver_time'].std().round(2)
            st.metric('Std Temp. s/Fest',std_delivery_time)
    st.markdown('---')

    with st.container():
        st.markdown('### Tempo médio de entrega por cidade')
        def pieGraph_tempo_medio_cidade(data):
            from plotly import express as py
            df_aux=data.groupby(['City'])['Deliver_time'].mean().reset_index()
            fig=py.pie(data_frame=df_aux,names='City',values='Deliver_time')
            return fig

        st.plotly_chart(pieGraph_tempo_medio_cidade(data),use_container_width=True)

    st.markdown('---')

    with st.container():

        c1,c2=st.columns(2)

        with c1:
            st.markdown('### Distribuição do tempo por cidade')
            def barGraph_tempo_por_cidade(dados):
                data=dados
                colunas=['City','Deliver_time']
                df=data[colunas]
                df=df.groupby(['City']).agg({'Deliver_time':['mean','std']}).reset_index()
                df.columns=['City','avg_time','std_time']

                import plotly.express as px
                
                fig = px.bar(
                    df, 
                    x='City', 
                    y='avg_time', 
                    error_y='std_time', 
                    title='',
                    labels={'City': 'City', 'avg_time': ''}
                )
                return fig
            st.plotly_chart(barGraph_tempo_por_cidade(dados=data),use_container_width=True)
        
        with c2:
            st.markdown('### Tempo médio por tipo de entrega')

            def table_city_orderType_time(data):
                df=data.copy()
                df=df.groupby(['City','Type_of_order']).agg({'Deliver_time':['mean','std']})
                df.columns=['mean_time','std_time']
                df=df.reset_index()
                return df
            st.dataframe(table_city_orderType_time(data),hide_index=True)
    st.markdown('---')

    with st.container():
        st.markdown('### Tempo médio por cidade e trafego')

        def pieGraph_city_traffic_time(dados):
            df=dados.copy()
            colunas=['City','Deliver_time','Road_traffic_density']
            df=df[colunas]
            df=df.groupby(['City','Road_traffic_density']).agg({'Deliver_time':['mean','std']})
            df.columns=['mean_time','std_time']
            df=df.reset_index().fillna(0)
            from plotly import express as px
            fig=px.sunburst(df,path=['City','Road_traffic_density'],
                            values='mean_time',color='std_time',
                            color_continuous_scale='RdBu',
                            )
            return fig
        st.plotly_chart(pieGraph_city_traffic_time(data),use_container_width=True)
            
            
    st.markdown("---")

#========================================
with v_tatica:
    pass

#========================================
with v_geografica:
    pass
    