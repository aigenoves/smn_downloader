import os
import datetime
from pathlib import Path
import streamlit as st
import pandas as pd


from src.datodiario import fetch_daily_data
from src.utils import generate_dates_until_today
from src import parser


main_path = Path(__file__).resolve()
main_directory = main_path.parent
relative_path = main_directory / "data"

text_area_placeholder = st.empty()
last_five_processed = []

st.title("Procesar estaciones")

stations_file = relative_path / "estaciones_smn.txt"
output_parquet_file = relative_path / "estaciones_smn.parquet"
stations = parser.estaciones(stations_file)

stations.to_parquet(output_parquet_file, engine="pyarrow")
