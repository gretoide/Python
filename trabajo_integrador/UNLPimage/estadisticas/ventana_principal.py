import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import ast
import json 
from wordcloud import WordCloud
from itertools import product
from collections import Counter

# Paths base
RUTA_ARCHIVO = os.path.abspath(os.path.dirname(__file__))
RUTA_BASE = os.path.abspath(os.path.join(RUTA_ARCHIVO, '..'))

# Paths de archivos
DATABASE = os.path.join(RUTA_BASE, 'database')
json_file = os.path.join(DATABASE, 'datos.json')
image_file = os.path.join(DATABASE, 'datos_imagenes.csv')
logs_file = os.path.join(RUTA_BASE, 'log', 'event_log.csv')
style_file = os.path.join(RUTA_BASE, 'estadisticas', 'style.scss')
js_file = os.path.join(RUTA_BASE, 'estadisticas', 'script.js')

# Readers para los archivos
df_image = pd.read_csv(image_file, delimiter=';')
df_logs = pd.read_csv(logs_file, delimiter=';')

# Variable de estado para controlar la visibilidad del gráfico
show_chart = True
show_persons = True
# Datos para el gráfico
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

# Manejando el estilo de la página
with open(style_file, 'r') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    with open(js_file, 'r') as f:
        st.markdown(f'<script>{f.read()}</script>', unsafe_allow_html=True)



st.markdown(
    """

    <div class="cssFont_1" data-glitch="Analisis de Datos - UNLPimage">Analisis de Datos - UNLPimage</div>

    """, unsafe_allow_html=True
)






st.sidebar.markdown(
"""

<div class="text-sidebar" data-glitch=" 📷 Imágenes"> 📷 Imágenes</div>

"""
    , unsafe_allow_html=True)


if st.sidebar.button('Tipo de imagen', key='-TIPO-IMAGEN-'):
    show_persons = not show_persons
    show_chart = not show_chart

    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()


    # Contar la cantidad de imágenes por tipo
    tipo_counts = df_image['tipo'].value_counts()

    # Generar el gráfico de torta
    fig, ax = plt.subplots()
    ax.pie(tipo_counts, labels=tipo_counts.index, autopct='%1.1f%%')
    ax.set_title('Porcentaje según tipo de imagen')

    # Mostrar el gráfico de torta en Streamlit
    st.pyplot(fig)


if st.sidebar.button('Máximos - ancho y alto', key='-ANCHO-ALTO-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Leer el archivo de logs
    df = pd.read_csv(image_file, delimiter=';')

    # Obtener los valores máximos de ancho y alto
    max_width = df['tamano'].str.extract('(\d+) x \d+').astype(int).max().values[0]
    max_height = df['tamano'].str.extract('\d+ x (\d+)').astype(int).max().values[0]

    # Crear la figura y el eje
    fig, ax = plt.subplots()

    # Configurar el tamaño de la figura
    fig.set_size_inches(6, 4)

    # Configurar los límites del eje
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Configurar el texto
    ax.text(5, 7, f'Valor máximo de ancho: {max_width}', fontsize=12, ha='center', va='center')
    ax.text(5, 5, f'Valor máximo de alto: {max_height}', fontsize=12, ha='center', va='center')

    # Ocultar los ejes
    ax.axis('off')

    # Mostrar la figura en Streamlit
    st.pyplot(fig)


if st.sidebar.button('Relación - ancho y alto', key='-RELACION-ANCHO-ALTO-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Leer el archivo CSV
    df = pd.read_csv(image_file, delimiter=';')

    # Extraer el ancho y el alto como columnas separadas
    df['ancho'] = df['tamano'].str.extract('(\d+) x \d+').astype(int)
    df['alto'] = df['tamano'].str.extract('\d+ x (\d+)').astype(int)

    # Generar el gráfico de dispersión
    fig, ax = plt.subplots()
    ax.scatter(df['ancho'], df['alto'])
    ax.set_xlabel('Ancho')
    ax.set_ylabel('Alto')
    ax.set_title('Relación entre Ancho y Alto de las Imágenes')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

if st.sidebar.button('Evolución de actividad', key='-EVOLUCION-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Leer el archivo CSV
    df_images = pd.read_csv(image_file, delimiter=';')

    # Convertir la columna de fecha y hora a tipo datetime
    df_images['ultima_actualizacion'] = pd.to_datetime(df_images['ultima_actualizacion'], format='%Y-%m-%d %H:%M:%S.%f')

    # Agrupar por fecha y contar la cantidad de actualizaciones
    actualizaciones_por_fecha = df_images.groupby(df_images['ultima_actualizacion'].dt.date).size()

    # Crear el gráfico de líneas
    fig, ax = plt.subplots()
    actualizaciones_por_fecha.plot(kind='line', marker='o')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Cantidad de actualizaciones')
    ax.set_title('Evolución de la cantidad de actualizaciones')

    # Rotar las etiquetas del eje x para una mejor visualización
    plt.xticks(rotation=45)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

if st.sidebar.button('Cambios diarios', key='-OPERACIONES-SEMANALES-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Leer el archivo de registros de eventos
    df_images = pd.read_csv(image_file, delimiter=';')

    # Convertir la columna 'ultima_actualizacion' a tipo datetime
    df_images['ultima_actualizacion'] = pd.to_datetime(df_images['ultima_actualizacion'], format='%Y-%m-%d %H:%M:%S.%f')

    # Obtener la fecha de última actualización para cada registro
    df_images['FECHA_ACTUALIZACION'] = df_images['ultima_actualizacion'].dt.date

    # Obtener el día de la semana para cada fecha de última actualización
    df_images['DIA_SEMANA'] = df_images['ultima_actualizacion'].dt.day_name()

    # Contar la cantidad de cambios por día de la semana
    cambios_por_dia = df_images['DIA_SEMANA'].value_counts().sort_index()

    # Establecer el orden deseado de los días de la semana
    orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    cambios_por_dia = cambios_por_dia.reindex(orden_dias)

    # Crear el gráfico de barras o de torta
    fig, ax = plt.subplots()
    ax.bar(cambios_por_dia.index, cambios_por_dia)
    ax.set_title('Cambios realizados por día de la semana')
    ax.set_xlabel('Día de la semana')
    ax.set_ylabel('Cantidad de cambios')
    plt.xticks(rotation=45)
    st.pyplot(fig)


st.sidebar.markdown(
    """
    <div class="text-sidebar" data-glitch="🎨 Collage">🎨 Collage</div>
    """
    , unsafe_allow_html=True)

if st.sidebar.button('TOP 5 Imágenes', key='-PLANTILLAS-COLLAGES-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Leer el archivo CSV
    data = pd.read_csv(logs_file, delimiter=';')

    # Filtrar las filas que corresponden a los collages
    collages_data = data[data['OPERACION'] == 'Nuevo Collage']

    # Crear una lista de todas las imágenes utilizadas en los collages
    all_images = []
    for images_list in collages_data['VALORES'].apply(ast.literal_eval):
        all_images.extend(images_list)

    # Contar las ocurrencias de cada imagen
    image_counts = Counter(all_images)

    # Obtener el top 5 de imágenes más utilizadas
    top_images = image_counts.most_common(5)

    # Crear una tabla para mostrar el top 5 de imágenes
    image_table = pd.DataFrame(top_images, columns=['Imagen', 'Apariciones'])
    image_table.index += 1
    # Mostrar la tabla en Streamlit
    st.dataframe(image_table)

if st.sidebar.button('Tags Utilizados', key='-TAGS-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Crear un DataFrame a partir del CSV
    data = pd.read_csv(image_file, delimiter=';')

    # Obtener todos los tags en una lista
    tags_list = data['tags'].str.split(',').sum()

    # Eliminar los espacios en blanco de cada tag y convertir a minúsculas
    lista_procesada = [item.lower().replace(" ", "") for item in tags_list]
    
    # Convertir la lista en una Serie para eliminar duplicados
    unique_tags = pd.Series(lista_procesada).unique()

    # Crear un DataFrame con los tags únicos
    unique_tags_df = pd.DataFrame({'Tag': unique_tags})

    # Incrementar el índice en 1
    unique_tags_df.index += 1
    
    # Mostrar la tabla de tags únicos
    st.write("Listado de tags:")
    st.dataframe(unique_tags_df)

if st.sidebar.button('Tags más utilizados', key='-MAX-TAGS-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Crear un DataFrame a partir del CSV
    data = pd.read_csv(image_file, delimiter=';')

    # Obtener todos los tags en una lista
    tags_list = data['tags'].str.split(',').sum()

    lista_procesada = [item.lower().replace(" ", "") for item in tags_list]

    # Contar la frecuencia de cada tag
    lista_procesada = pd.Series(tags_list).value_counts()

    # Obtener los 3 tags más utilizados
    top_3_tags = lista_procesada.head(3)

    # Crear un DataFrame con los resultados
    top_tags_df = pd.DataFrame({'Tag': top_3_tags.index, 'Repetidos': top_3_tags.values})



    # Crear la tabla con etiquetas (labels)
    table_data = [top_tags_df.columns.tolist()] + top_tags_df.values.tolist()

    # Crear la imagen de la tabla
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    table = ax.table(cellText=table_data, loc='center', cellLoc='center')
    table.set_fontsize(14)
    table.scale(1.2, 1.2)
    
    # Crear la imagen de la tabla
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    table = ax.table(cellText=table_data, loc='center', cellLoc='center', colWidths=[0.3, 0.3])
    table.set_fontsize(14)
    table.scale(1.2, 1.2)

    # Establecer estilos para los encabezados de columna
    for i, key in enumerate(table_data[0]):
        cell = table[0, i]
        cell.set_text_props(weight='bold')
        cell.set_facecolor('#e6e6e6')
        cell.set_edgecolor('black')

    # Establecer estilos para las celdas de datos
    for i in range(1, len(table_data)):
        for j in range(len(table_data[i])):
            cell = table[i, j]
            cell.set_edgecolor('black')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)


if st.sidebar.button('Nube de Tags', key='-NUBE-COLLAGE-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Crear un DataFrame a partir del CSV
    data = pd.read_csv(image_file, delimiter=';')

    # Obtener todos los tags en una lista
    tags_list = data['tags'].str.split(',').sum()
    lista_procesada = [item.lower().replace(" ", "") for item in tags_list]
    # Convertir la lista en una cadena separada por espacios
    tags_text = ' '.join(lista_procesada)

    # Crear la nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(tags_text)

    # Crear la figura y el eje
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    # Mostrar la figura en Streamlit
    st.pyplot(fig)

if st.sidebar.button('Nube de Titulos', key='-NUBE-TITULO-COLLAGE-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Crear un DataFrame a partir del CSV
    data = pd.read_csv(logs_file, delimiter=';')

    # Filtrar las filas que corresponden a collages
    collages_data = data[data['OPERACION'] == 'Nuevo Collage']

    # Obtener los títulos de los collages
    titulos_collages = collages_data['TEXTOS'].tolist()

    # Unir los títulos en una sola cadena
    titulos_collages_str = ' '.join(titulos_collages)

    # Crear la nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(titulos_collages_str)

    # Crear la figura y el eje
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    # Mostrar la figura en Streamlit
    st.pyplot(fig)

if st.sidebar.button('Calcular tamaño promedio (bytes)', key='-TAMANO_BYTES-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()


    # Leer el archivo JSON
    with open(json_file) as file:
        data_json = json.load(file)

    data_images = pd.read_csv(image_file, delimiter=';')
    data_images['tamano'] = data_images['tamano'].str.extract('(\d+)').astype(float)  # Convertir la columna 'tamano' a float

    perfiles_json = set()
    for item in data_json:
        perfiles_json.add(item['Alias'])

    perfiles_images = set(data_images['ultimo_perfil'].unique())

    perfiles = perfiles_json.union(perfiles_images)

    promedio_bytes_por_perfil = {}
    for perfil in perfiles:
        imagenes_actualizadas = data_images[data_images['ultimo_perfil'] == perfil]
        tamano_promedio = imagenes_actualizadas['tamano'].mean()
        if np.isnan(tamano_promedio):
            tamano_promedio = 0
        promedio_bytes_por_perfil[perfil] = tamano_promedio


    tabla_bytes_promedio = pd.DataFrame({
        'Perfil': promedio_bytes_por_perfil.keys(),
        'Tamaño promedio (bytes)': promedio_bytes_por_perfil.values()
    })

    # Ordenar la tabla por tamaño promedio en orden descendente
    tabla_bytes_promedio = tabla_bytes_promedio.sort_values(by='Tamaño promedio (bytes)', ascending=False)

    st.table(tabla_bytes_promedio)



# Columna de Memes

st.sidebar.markdown(
    """
    <div class="text-sidebar" data-glitch="😄 Memes">😄 Memes</div>
    """
    , unsafe_allow_html=True)

if st.sidebar.button('TOP 5 Plantillas', key='-PLANTILLAS-MEMES-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Leer el archivo CSV
    data = pd.read_csv(logs_file, delimiter=';')

    # Filtrar las filas que corresponden a los memes
    memes_data = data[data['OPERACION'] == 'Nuevo Meme']

    # Obtener la frecuencia de cada meme
    meme_counts = memes_data['VALORES'].value_counts().head(5)

    # Obtener la lista de los 5 memes más utilizados
    top_memes = meme_counts.index.tolist()
    
    # Mostrar el top 5 de memes en una tabla
    meme_table = pd.DataFrame({'Meme': top_memes, 'Apariciones': meme_counts.values})
    meme_table = meme_table.sort_values('Apariciones', ascending=False)
    meme_table.index += 1


    # Mostrar la tabla en Streamlit
    st.dataframe(meme_table)

if st.sidebar.button('Nube de Textos', key='-NUBE-MEMES-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Leer el archivo CSV
    data = pd.read_csv(logs_file, delimiter=';')

    # Filtrar las filas que corresponden a los memes
    memes_data = data[data['OPERACION'] == 'Nuevo Meme']

    # Obtener todos los textos de los memes en una cadena
    textos = ' '.join(memes_data['TEXTOS'].dropna().tolist())

    # Crear la nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(textos)

    # Mostrar la nube de palabras
    fig = plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    # Mostrar la figura en Streamlit
    st.pyplot(fig)


st.sidebar.markdown(
    """
    <div class="text-sidebar" data-glitch="📊 Actividad">📊 Actividad</div>
    """
    , unsafe_allow_html=True)

if st.sidebar.button('Cantidad de operaciones', key='-CANT-USUARIOS-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Leer el archivo de logs
    df_logs = pd.read_csv(logs_file, delimiter=';')

    # Contar la cantidad de cada operación
    operaciones_counts = df_logs['OPERACION'].value_counts()

    # Crear el gráfico de barras
    fig, ax = plt.subplots()
    operaciones_counts.plot(kind='bar')
    ax.set_xlabel('Operación')
    ax.set_ylabel('Cantidad')
    ax.set_title('Cantidad de cada operación realizada')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

if st.sidebar.button('Operaciones diarias', key='-OPERACIONES-DIARIAS-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Leer el archivo de registros de eventos
    df_logs = pd.read_csv(logs_file, delimiter=';')

    # Convertir la columna 'HORA' a tipo datetime
    df_logs['HORA'] = pd.to_datetime(df_logs['HORA'], format='%Y%m%d%H%M')

    # Obtener la fecha de última actualización para cada registro
    df_logs['FECHA_ACTUALIZACION'] = df_logs['HORA'].dt.date

    # Obtener el día de la semana para cada fecha de última actualización
    df_logs['DIA_SEMANA'] = df_logs['HORA'].dt.day_name()

    # Contar la cantidad de cambios por día de la semana
    cambios_por_dia = df_logs['DIA_SEMANA'].value_counts().sort_index()

    # Crear el gráfico de barras
    fig, ax = plt.subplots()
    dias_semana_ordenados = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    cambios_por_dia = cambios_por_dia.reindex(dias_semana_ordenados)
    ax.bar(cambios_por_dia.index, cambios_por_dia)
    ax.set_title('Cambios realizados por día de la semana')
    ax.set_xlabel('Día de la semana')
    ax.set_ylabel('Cantidad de cambios')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)


if st.sidebar.button('Operaciones por usuario', key='-OPERACIONES-USUARIOS-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Leer el archivo de logs
    df_logs = pd.read_csv(logs_file, delimiter=';')

    # Crear una lista de colores para las operaciones
    operaciones = df_logs['OPERACION'].unique()
    colores = plt.cm.get_cmap('tab20', len(operaciones))

    # Contar la cantidad de operaciones por nick y por tipo de operación
    operaciones_por_nick = df_logs.groupby(['ALIAS', 'OPERACION']).size().unstack(fill_value=0)

    # Crear el gráfico de barras apilado horizontal
    fig, ax = plt.subplots()
    nicks = operaciones_por_nick.index
    operaciones_por_nick = operaciones_por_nick.values.T
    bars = ax.barh(nicks, operaciones_por_nick[0], color=colores(0), label=operaciones[0])

    for i in range(1, len(operaciones)):
        bars += ax.barh(nicks, operaciones_por_nick[i], left=np.sum(operaciones_por_nick[:i], axis=0),
                        color=colores(i), label=operaciones[i])

    # Configurar el estilo del gráfico
    ax.legend(loc='lower right')
    ax.set_xlabel('Cantidad')
    ax.set_ylabel('Nick')
    ax.set_title('Cantidad de operaciones por nick')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)



st.sidebar.markdown(
    """
    <div class="text-sidebar" data-glitch="📈 Porcentaje por géneros">📈 Porcentaje por géneros</div>
    """
    , unsafe_allow_html=True)


if st.sidebar.button('Imágenes etiquetadas', key='-IMAGENES-ETIQUETADAS-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()

    # Leer el archivo JSON
    with open(json_file) as file:
        data = json.load(file)

    # Crear un DataFrame a partir del JSON
    df_json = pd.DataFrame(data)

    # Unir los DataFrames por el campo 'ALIAS'
    df_merged = pd.merge(df_logs, df_json, left_on='ALIAS', right_on='Alias', how='left')

    # Filtrar las operaciones deseadas
    operacion_deseada = 'Nueva imagen etiquetada'
    df_filtrado = df_merged[df_merged['OPERACION'] == operacion_deseada]

    # Contar la cantidad de operaciones filtradas por sexo
    operaciones_por_sexo = df_filtrado['Sexo'].value_counts()

    # Crear el gráfico de tarta
    fig, ax = plt.subplots()
    ax.pie(operaciones_por_sexo, labels=operaciones_por_sexo.index, autopct='%1.1f%%')
    ax.set_title(f'Comparación de operaciones por genero')
    st.pyplot(fig)

if st.sidebar.button('Imágenes actualizadas', key='-ACTUALIZADAS-ETIQUETADAS-'):
    show_chart = not show_chart
    show_persons = not show_persons
    if st.button('Ocultar gráfico'):
        show_chart = not show_chart

    # Ocultar el gráfico si la variable de estado es False
    if not show_chart:
        st.empty()
    else:
        plt.plot(x, y)
        st.pyplot()
        
    # Leer el archivo JSON
    with open(json_file) as file:
        data = json.load(file)

    # Crear un DataFrame a partir del JSON
    df_json = pd.DataFrame(data)

    # Unir los DataFrames por el campo 'ALIAS'
    df_merged = pd.merge(df_logs, df_json, left_on='ALIAS', right_on='Alias', how='left')

    # Filtrar las operaciones deseadas
    operacion_deseada = 'Modificacion de imagen previamente clasificada' 
    df_filtrado = df_merged[df_merged['OPERACION'] == operacion_deseada]

    # Contar la cantidad de operaciones filtradas por sexo
    operaciones_por_sexo = df_filtrado['Sexo'].value_counts()

    # Crear el gráfico de tarta
    fig, ax = plt.subplots()
    ax.pie(operaciones_por_sexo, labels=operaciones_por_sexo.index, autopct='%1.1f%%')
    ax.set_title(f'Comparación de operaciones por genero')
    st.pyplot(fig)


if show_persons:
    st.markdown(
    """
    <script src="https://kit.fontawesome.com/e2f1cbcc9b.js" crossorigin="anonymous"></script>    
    <figure class="snip1566">
    <img src="https://i.imgur.com/CzIFUVF.png" alt="FotoDePerfil" />
    <figcaption><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 496 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg></figcaption>
    <a href="https://github.com/khazius5/"></a>
    </figure>
    <figure class="snip1566">
    <img src="https://i.imgur.com/L4qz0yd.png" alt="FotoDePerfil" />
    <figcaption><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 496 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg></figcaption>
    <a href="https://github.com/gretoide/"></a>
    </figure>
    <figure class="snip1566">
    <img src="https://i.imgur.com/pe8c327.png" alt="FotoDePerfil" />
    <figcaption><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 496 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg></figcaption>
    <a href="https://github.com/AdrianASambido"></a>
    </figure>
    <figure class="snip1566">
    <img src="https://i.imgur.com/gLON4CD.png" alt="FotoDePerfil" />
    <figcaption><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 496 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg></figcaption>
    <a href="https://github.com/AlvarezLandolfi97"></a>
    </figure>
    """
    , unsafe_allow_html=True)