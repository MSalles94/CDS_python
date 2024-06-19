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
#========================================
#Header
#========================================
st.header('Market Place - Visão Empresa')

filtro_linhas=((data['Order_Date']<date_slider)&
               (data['Road_traffic_density'].isin(traffic_options))&
               (data['City'].isin(city))
               )
data=data.loc[filtro_linhas,:]
#========================================
#Layout
#========================================

v_gerencial,v_tatica,v_geografica=st.tabs(['Vistão Gerencial',
                                 'Visão Tática',
                                 'Visão Geográfica'])

#========================================
with v_gerencial:

    with st.container():

        st.markdown('# Orders by day')

        cols=['ID','Order_Date']
        df_aux=data.loc[:,cols].groupby('Order_Date').count().reset_index()
        fig=px.bar(df_aux,x='Order_Date',y='ID')
        st.plotly_chart(fig,use_container_width=True)

        vg_col1,vg_col2=st.columns(2)

    with st.container():
        #=================
        with vg_col1:
            st.markdown('## Orders per traffic density')

            df_aux=data.groupby('Road_traffic_density')[['ID']].count().reset_index()
            fig=px.pie(data_frame=df_aux,names='Road_traffic_density',values='ID')
            st.plotly_chart(fig,use_container_width=True)


        #=================
        with vg_col2:
            st.markdown('## Orders per Traffic density per city')
            df_aux=data.groupby(['City','Road_traffic_density'])[['ID']].count().reset_index()
            fig=px.scatter(df_aux,x='City',y='Road_traffic_density',size='ID',color='City')
            st.plotly_chart(fig,use_container_width=True)
    with st.container():
        #traffic density per city
        st.markdown('## Traffic density per city')

        tabela=data.copy()
        tabela=tabela.groupby(['City', 'Road_traffic_density'])[['ID']].count().reset_index()
        tabela['%ped'] = 100 * ( tabela['ID'] / tabela['ID'].sum() )
        fig=px.bar( tabela, x='City', y='%ped', color='Road_traffic_density', barmode='group')
        st.plotly_chart(fig,use_container_width=True)
#========================================
with v_tatica:
    with st.container():
        st.markdown('# Orders per week')
        tabela=data.copy()
        tabela['week']=tabela['Order_Date'].dt.strftime( "%U" ).astype(int)
        tabela=tabela.groupby(['week'])[['ID']].count().reset_index()
        fig=px.bar(tabela,x='week',y='ID')
        st.plotly_chart(fig,use_container_width=True)

    with st.container():
        st.markdown('# Unique deliver person per week')
        tabela=data.copy()
        tabela['week']=tabela['Order_Date'].dt.strftime( "%U" ).astype(int)
        tabela=tabela.groupby(['Delivery_person_ID','week'])[[]].count().reset_index()
        tabela=tabela.groupby(['week'])[['Delivery_person_ID']].count().reset_index()
        fig=px.line(tabela,x='week',y='Delivery_person_ID')
        st.plotly_chart(fig,use_container_width=True)

#========================================
with v_geografica:
    st.markdown('# Central location of city per traffic density')

    from folium import Map,Marker
    from streamlit_folium import folium_static

    columns = [
    'City',
    'Road_traffic_density',
    'Delivery_location_latitude',
    'Delivery_location_longitude'
    ]
    tabela=data[columns]

    tabela=tabela.groupby(['City','Road_traffic_density']).median().reset_index()
    map_=Map(zoom_start=11)
    for  index, location_info in tabela.iterrows():
        
        Marker(
            [location_info['Delivery_location_latitude'],
            location_info['Delivery_location_longitude']],
            popup=location_info[['City','Road_traffic_density']]
        ).add_to( map_ )
    folium_static(map_,width=1024,height=600)
    