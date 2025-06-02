import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

def leercsv1():
    nombre_archivo = "neighbourhoods.csv"
    with open(nombre_archivo, "r", encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=",")
        # Omitir el encabezado
        next(lector, None)
        barrios = []
        for fila in lector:
            barrios.append(fila[1])
        return barrios

def leercsv2():
    nombre_archivo = "listings.csv"
    with open(nombre_archivo, "r", encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=",")
        # Omitir el encabezado
        next(lector, None)
        precios = []
        host = []
        habitacion = []
        for fila in lector:
            precios.append(int(fila[9]))
            host.append((fila[3]))
            habitacion.append((fila[8]))
        datos= [precios]+[host]+[habitacion]
        # 0 para precios 1 para host 2 para tipo de habitacion
        return datos

def leercsv3():
    nombre_archivo = "reviews.csv"
    with open(nombre_archivo, "r", encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=",")
        # Omitir el encabezado
        next(lector, None)
        fechas = []
        for fila in lector:
            fechas.append(fila[1])
        return fechas


def precio_maximo(precios):
    preciomayor = 0
    for precio in precios:
        if precio > preciomayor:
            preciomayor = precio
    return preciomayor



def lista_sin_repetir(tipos):
    nuevalista=[]
    for str in tipos:
        if str not in nuevalista:
            nuevalista.append(str)
    return nuevalista

def datos_de_habitacion(tipos):
    count=0
    for x in tipos:
        count +=1
    porcentaje_entire= tipos.count("Entire home/apt")/count
    porcentaje_Private=tipos.count("Private room")/count
    porcentaje_Shared=tipos.count("Shared room")/count
    porcentaje_Hotel=tipos.count("Hotel room")/count
    return [porcentaje_entire,porcentaje_Hotel,porcentaje_Private,porcentaje_Shared]

def contar_repeticiones_meses(lista_fechas):
    contador_meses = {}
    for fecha in lista_fechas:
        _,mes, _ = fecha.split("-") 
        mes_numero = int(mes)
        if mes_numero in contador_meses:
            contador_meses[mes_numero] += 1
        else:
            contador_meses[mes_numero] = 1
    contador_meses_ordenado = dict(sorted(contador_meses.items(), key=lambda x: x[0]))
    lista_repeticiones = list(contador_meses_ordenado.values())
    return lista_repeticiones

def main():
    datos=leercsv2()
    c1,c2 = st.columns([3,7])
    c1.divider()
    c1.slider("seleccion de precio maximo",min_value=0,max_value=precio_maximo(datos[0]),value=0,step=1)
    c1.divider()
    barrios=leercsv1()
    c1.multiselect('selecciona los barrios deseados',barrios)
    c1.divider()
    c1.radio("tipo de plazo 👉",options=["ambos", "corto", "largo"],)
    c1.divider()
    c1.multiselect('selecciona los host deseados',lista_sin_repetir(datos[1]))
    c1.divider()
    fig1, ax1 = plt.subplots()
    ax1.pie(datos_de_habitacion(datos[2]), labels=lista_sin_repetir(datos[2]), autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Para asegurar que la torta sea un círculo y no una elipse
    c1.pyplot(fig1)
    c2.write("aca va el mapa")
    df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [35.6895, 139.6917],columns=['lat', 'lon'])
    c2.map(df)
    c2.write("ocupacion desde el 2011 hasta el 2023")
    data = contar_repeticiones_meses(leercsv3())
    df = pd.DataFrame(data)
    c2.bar_chart(df)

if __name__ == '__main__':
    main()