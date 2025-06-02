import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import csv

#Configura aspectos graficos de la pagina
#ConfiguracionDeLaPagina: none ---> none   
def configuracionDeLaPagina():
    st.set_page_config(
        page_title="Tokyo",
        page_icon='logo.jpg',
        layout="wide",
        initial_sidebar_state="auto",)



#Recibe un string que representa el nombre del archivo a leer
#Lee y transforma los archivos csv a Listas
#leer_csv: string ---> List
def leer_csv(nombre_archivo:str):
    with open(nombre_archivo, "r", encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=",")
        next(lector, None)
        data = []
        for fila in lector:
            data.append(fila)
        return data

def testLeer_csv():
    assert(leer_csv("ArchivoPrueba.csv")==[['andres', 'cornejo', 'rosario'], ['agustin', 'cires', 'rosario']])


#Recibe un parámetro precios de tipo lista que contiene valores numéricos.
#Retorna el valor máximo de la lista.
#precio_maximo: List ---> int
def precio_maximo(precios:list):
    return max(precios)

def testPrecio_maximo():
    assert(precio_maximo([1,5,2])==5)
    assert(precio_maximo([10,-5,2])==10)
    assert(precio_maximo([3,4,15])==15)


#Recibe una lista.
#Retorna una lista sin repeticiones de los elementos de la lista original.
#lista_sin_repetir List ---> List
def lista_sin_repetir(tipos:list):
    return list(set(tipos))

def testLista_sin_repetir():
    assert(lista_sin_repetir(["enero","enero"])==["enero"])
    assert(lista_sin_repetir(["septiembre","septiembre","septiembre"])==["septiembre"])


#Recibe una lista con las habitaciones. 
#Retorna una lista de porcentajes correspondientes a cada tipo de habitación.
#datos_de_habitacion: List ---> List
def datos_de_habitacion(tipos:list):
    if (len(tipos)>0):
        count = len(tipos)
        porcentaje_entire = tipos.count("Entire home/apt") / count
        porcentaje_Private = tipos.count("Private room") / count
        porcentaje_Shared = tipos.count("Shared room") / count
        porcentaje_Hotel = tipos.count("Hotel room") / count
        return [porcentaje_entire, porcentaje_Hotel, porcentaje_Private, porcentaje_Shared]
    elif (len(tipos)==0):
        return []
    

def testDatos_de_habitacion():
    assert(datos_de_habitacion(["Entire home/apt","Private room","Shared room","Hotel room"])==[0.25,0.25,0.25,0.25])
    assert(datos_de_habitacion(["Entire home/apt"])==[1,0,0,0])
    assert(datos_de_habitacion(["Private room","Shared room","Hotel room","Hotel room"])==[0,0.50,0.25,0.25])

#Recibe un parámetro lista_fechas de tipo lista que contiene fechas en formato string. 
#Retorna un diccionario con la cantidad de repeticiones de cada mes.
#contar_repeticiones_meses: List ---> Dict
def contar_repeticiones_meses(lista_fechas:list):
    contador_meses = {}
    for fecha in lista_fechas:
        _,mes, _ = fecha.split("-") 
        mes_numero = int(mes)
        if mes_numero in contador_meses:
            contador_meses[mes_numero] += 1
        else:
            contador_meses[mes_numero] = 1
    contador_meses_ordenado = dict(sorted(contador_meses.items(), key=lambda x: x[0]))
    return contador_meses_ordenado

def testContar_repeticiones_meses():
    assert(contar_repeticiones_meses(["2023-5-10","2023-5-10","2023-5-10","2023-5-10"])=={5: 4})
    assert(contar_repeticiones_meses(["2023-5-10","2023-5-10","2023-5-10"])=={5:3})
    assert(contar_repeticiones_meses(["2023-5-10","2023-5-10"])=={5:2})

#Recibe una lista datos que contiene la informacion del archivo csv. 
#Retorna una figura de torta (pie chart) utilizando los datos de habitación.
#graficoDeTorta: List ---> Figure
def graficoDeTorta(datos:list):
    fig1, ax1 = plt.subplots()
    tipos_habitacion = [fila[8] for fila in datos]
    porciones_agrandadas = [0, 1, 2]
    explode = [0.1 if i in porciones_agrandadas else 0 for i in range(4)]
    ax1.pie(datos_de_habitacion(tipos_habitacion),labels=["Entire home/apt","Private room","Shared room","Hotel room"], autopct='%1.1f%%', startangle=90, explode=explode)
    ax1.axis('equal')  # Para asegurar que la torta sea un círculo y no una elipse
    return fig1

#barriosElegidos:list, precioMaxElegido:int, hostsElegidos:list, y tipoPlazo:str.
#Retorna una lista de datos filtrados según los parámetros.
#cambiarDatosMapa: List List Int List String ---> List
def cambiarDatosMapa(datos:list, barriosElegidos:list, precioMaxElegido:int, hostsElegidos:list, tipoPlazo:str):
    datos_Filtrados = datos
    if barriosElegidos:
        datos_Filtrados = [fila for fila in datos_Filtrados if fila[5] in barriosElegidos]
    if precioMaxElegido:
        datos_Filtrados = [fila for fila in datos_Filtrados if int(fila[9]) <= precioMaxElegido]
    if hostsElegidos:
        datos_Filtrados = [fila for fila in datos_Filtrados if fila[3] in hostsElegidos]
    if tipoPlazo == "Corto":
        datos_Filtrados = [fila for fila in datos_Filtrados if int(fila[10]) <= 30]
    elif tipoPlazo == "Largo":
        datos_Filtrados = [fila for fila in datos_Filtrados if int(fila[10]) > 30]
    elif precioMaxElegido==0:
        datos_Filtrados = []
    return datos_Filtrados

def testCambiarDatosMapa():
    assert(cambiarDatosMapa(leer_csv('ArchivoPruebas2.csv'),['Kita Ku'],8336,['Kei'],"Corto")==leer_csv('ArchivoPruebas3.csv'))

#barriosElegidos:list, precioMaxElegido:int, hostsElegidos:list, y tipoPlazo:str.
#Retorna un diccionario con las coordenadas de latitud y longitud correspondientes a cada alquiler.
#mapaCompleto: List List int List String ---> Dict
def mapaCompleto(datos:list, barriosElegidos:list, precioMaxElegido:int, hostsElegidos:list, tipoPlazo:str):
    lat = [float(fila[6]) for fila in cambiarDatosMapa(datos, barriosElegidos, precioMaxElegido, hostsElegidos, tipoPlazo)]
    lon = [float(fila[7]) for fila in cambiarDatosMapa(datos, barriosElegidos, precioMaxElegido, hostsElegidos, tipoPlazo)]
    if not lat or not lon:
        return None
    return {'lat': lat, 'lon': lon}

def testMapaCompleto():
    assert(mapaCompleto(leer_csv('ArchivoPruebas2.csv'),['Kita Ku'],8336,['Kei'],"Corto"))=={'lat':[float(fila[6]) for fila in cambiarDatosMapa(leer_csv('ArchivoPruebas2.csv'), ['Kita Ku'],8336,['Kei'],"corto")], 'lon':[float(fila[7]) for fila in cambiarDatosMapa(leer_csv('ArchivoPruebas2.csv'), ['Kita Ku'],8336,['Kei'],"corto")]}

#Recibe un parámetro datosRewiews de tipo lista que contiene información sobre reseñas. 
#Retorna un DataFrame con los datos de las repeticiones de los meses.
#graficoBarras: List ---> DataFrame
def graficoBarras(datosRewiews:list):
    lista_fechas = [fila[1] for fila in datosRewiews]
    data = contar_repeticiones_meses(lista_fechas)
    return pd.DataFrame.from_dict(data, orient='index', columns=['Meses'])

#Recibe los mismos parámetros que la función cambiarDatosMapa. 
#Retorna un string que representa la cantidad total de alquileres.
#cantAlquileres: List List Number List String ---> String
def cantAlquileres(datos:list, barriosElegidos:list, precioMaxElegido:int, hostsElegidos:list, tipoPlazo:str):
    return str(len(cambiarDatosMapa(datos, barriosElegidos, precioMaxElegido, hostsElegidos, tipoPlazo)))

def testCantAlquileres():
    assert(cantAlquileres(leer_csv('ArchivoPruebas2.csv'),['Kita Ku'],8336,['Kei'],"corto"))=='1'

#Funcion que ejecuta todos los test del programa
#testTokyo: None ---> None
def testTokyo():
    testLeer_csv()
    testPrecio_maximo()
    testLista_sin_repetir()
    testDatos_de_habitacion()
    testContar_repeticiones_meses()
    testCambiarDatosMapa()
    testMapaCompleto()
    testCantAlquileres()


#Función principal que ejecuta el programa y organiza la interfaz gráfica.
#main: None ---> None
def main():

    configuracionDeLaPagina()

    st.title("Tokyo")
    
    #leer archivos y guardar informacion en una variable
    datosBarrio = leer_csv("neighbourhoods.csv")
    datos = leer_csv("listings.csv")
    datosReviews = leer_csv("reviews.csv")

    #guarda los nombres de todos los barrios en una variable
    barrios = [fila[1] for fila in datosBarrio]

    #organiza la pagina
    c1, c2 = st.columns([3, 7])

    c1.divider()

    max_precio = precio_maximo([int(fila[9]) for fila in datos])
    precioMaxElegido = c1.slider("Selecciona el precio maximo: ", min_value=0, max_value=max_precio,value=max_precio,step=1)
    
    c1.divider()

    barriosElegidos = c1.multiselect('Selecciona los barrios donde quiera hospedarse: ', barrios)
    
    c1.divider()

    tipoPlazo = c1.radio("Seleccione un tipo de plazo 👉", options=["Ambos", "Corto", "Largo"])
    
    c1.divider()

    hosts = lista_sin_repetir([fila[3] for fila in datos])

    hostsElegidos = c1.multiselect('Selecciona cuales host quiere ver: ', hosts)
    
    c1.divider()

    c1.title("Total de alquileres: " + cantAlquileres(datos, barriosElegidos, precioMaxElegido, hostsElegidos, tipoPlazo))

    c1.divider()

    c1.pyplot(graficoDeTorta(datos))

    c2.map(mapaCompleto(datos, barriosElegidos, precioMaxElegido,hostsElegidos,tipoPlazo))
    
    c2.bar_chart(graficoBarras(datosReviews))
    #------------------------------------TESTS-----------------------------------------#
    testTokyo()
    #------------------------------------TESTS-----------------------------------------#

if __name__ == '__main__':
    main()