import streamlit as st
import pandas as pd
import numpy as np
import plotly as px
import plotly.express as px
from bokeh.plotting import figure
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.markdown("""
 <style>
     [data-testid=stSidebar] {
         background-color: #FFDE59;
     }
 </style>
 """, unsafe_allow_html=True)


st.sidebar.image("logo.png", use_column_width=True)
st.title("🚨 Police Incident Reports from 2018 to 2020 in San Francisco 🚨")
st.markdown("---")

df = pd.read_csv("Police.csv")
st.markdown("The data shown below  belongs to incident reports in the city of San francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police districts, neighborhood in which it happened, type of incidentin category and subcategory, exact location and resoluntion.")

mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Day of Week']
mapa['Police District'] = df['Police District']
mapa['Neighborhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()

subset_data2 = mapa
police_district_input = st.sidebar.multiselect(
'Police District',
mapa.groupby('Police District').count().reset_index()['Police District'].tolist())
if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]


subset_data1 = subset_data2
neighborhood_input = st.sidebar.multiselect(
'Neighborhood',
subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist())
if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect(
    'Incident Category',
    subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())

if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]

subset_data

st.markdown('It is important to mention that any police district can aswer to any incident, the neighborhood in which it happened is not related to the police distrcit')
st.markdown('**Crime locations in San Francisco**')
st.map(subset_data)



cuenta_dias = subset_data['Day'].value_counts()
cuenta_promedio = cuenta_dias.mean()
df1 = pd.DataFrame({'Day': cuenta_dias.index, 'Count': cuenta_dias.values})
df1['Color'] = df1['Count'].apply(lambda x: 'Above Average' if x > cuenta_promedio else 'Below Average')

fig1 = px.bar(df1, x='Day', y='Count', color='Color')
media_2 = "{:.2f}".format(cuenta_promedio) 
fig1.add_hline(y=cuenta_promedio, line_dash="dash", line_color="green", annotation_text=f"Promedio: {media_2}",
              annotation_position="bottom right")

fig1.update_layout(
    title='Cantidad de incidentes por día',
    xaxis_title='Día de la semana',
    yaxis_title='Cantidad de incidentes')

resolution_counts = subset_data['Resolution'].value_counts().reset_index()
resolution_counts.columns = ['Resolution', 'Count']

fig = px.bar(resolution_counts, y='Resolution', x='Count', orientation='h')
fig.update_layout(
    title='Resolución de Incidentes',
    xaxis_title='Cantidad',
    yaxis_title='Tipo de Resolución',
    bargap=0.2,
    showlegend=False
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1)

with col2:
    st.plotly_chart(fig)

st.sidebar.markdown("**Filtro de Fecha**")
fecha_inicio = pd.to_datetime(mapa['Date'].min()).date()  
fecha_fin = pd.to_datetime(mapa['Date'].max()).date()   

if st.sidebar.checkbox("Filtrar por Fecha"):
    fecha_seleccionada = st.sidebar.date_input("Selecciona un rango de fechas", (fecha_inicio, fecha_fin))
    boton_reset = st.sidebar.button("Reset")
else:
    fecha_seleccionada = (fecha_inicio, fecha_fin)
    boton_reset = False

mapa['Date'] = pd.to_datetime(mapa['Date']).dt.date

if boton_reset:
    subset_data_filtered = mapa
else:
    subset_data_filtered = mapa[(mapa['Date'] >= fecha_seleccionada[0]) & (mapa['Date'] <= fecha_seleccionada[1])]

st.markdown('**Cantidad de incidentes por fecha**')
st.line_chart(subset_data_filtered['Date'].value_counts())


st.markdown('**Type of crimmes commited**')
st.bar_chart(subset_data['Incident Category'].value_counts())

agree = st.button('Click to see Incident Subcategories')
if agree:
    st.markdown('**Subtype of crimes committed**')
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())


