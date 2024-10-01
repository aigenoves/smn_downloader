from pathlib import Path
import json

import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import folium
from folium.plugins import MarkerCluster


def popup_function(feature):
    nombre_poligono = feature["properties"].get("nam", "Sin nombre")
    region = "Región Cuyana"
    return folium.GeoJsonPopup(f"{nombre_poligono}<br>Región: {region}")


main_path = Path(__file__).resolve()
main_directory = main_path.parent
relative_path = main_directory / "data"

# Cargar el archivo parquet


stations_file = relative_path / "estaciones_smn.parquet"
df = pd.read_parquet(stations_file)
cuyo_json_file = relative_path / "cuyo.json"  # Ruta al archivo GeoJSON

with open(cuyo_json_file) as f:
    cuyo = json.load(f)

if "lat" in df.columns and "lon" in df.columns:
    # Mostrar el DataFrame para verificar
    st.write(df.head())

    # Crear un mapa usando latitud y longitud
    map = folium.Map(
        location=[df["lat"].mean(), df["lon"].mean()],
        zoom_start=10,
        tiles="https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png",
        attr='&copy; <a href="http://www.argenmap.com.ar">Argenmap</a>',
    )
    marker_cluster = MarkerCluster().add_to(map)

    # Agregar los puntos al mapa
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"Lat: {row['lat']}, Lon: {row['lon']}",
            icon=folium.Icon(color="red"),
        ).add_to(marker_cluster)

    folium.GeoJson(
        cuyo,
        name="Region de Cuyo",
        popup=folium.GeoJsonPopup(
            fields=["nam"], aliases=["Provincia:"], localize=True, labels=True
        ),
    ).add_to(map)

    # Renderizar el mapa en Streamlit
    st_folium = st_folium(map, width=725)
else:
    st.error("El archivo no contiene columnas de latitud ('lat') y longitud ('lon').")


# https://eviet.cancilleria.gob.ar/es/content/regiones-argentinas-0
