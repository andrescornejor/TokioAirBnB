import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def cargar_datos(archivo):
    datos = pd.read_csv(archivo)
    return datos

st.title("Tokyo")

ruta_archivo = "listings.csv"

datos = cargar_datos(ruta_archivo)
st.map(datos)

conteo_tipos = datos['room_type'].value_counts()
porcentaje_tipos = (conteo_tipos / len(datos)) * 100
fig, grafico1 = plt.subplots()
porciones_agrandadas = [0, 1, 3]
explode = [0.1 if i in porciones_agrandadas else 0 for i in range(len(porcentaje_tipos))]
grafico1.pie(porcentaje_tipos, labels=['']*len(porcentaje_tipos), autopct='%1.1f%%', startangle=90, explode=explode)
grafico1.axis('equal')
plt.legend(porcentaje_tipos.index, loc='center left', bbox_to_anchor=(1, 0.5))
st.pyplot(fig)

valorMaximo = datos['price'].max()

valor = st.slider("Selecciona el rango de precio(Anda solo el slider pero no interactua con nada)", 0, valorMaximo)

st.write("Valor seleccionado:", valor)