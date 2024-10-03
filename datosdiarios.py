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

min_date = datetime.date(2017, 11, 26)
max_date = datetime.date.today() - datetime.timedelta(days=1)


def download(start_date: datetime.date, end_date: datetime.date, out_file_name: str):
    st.write(
        "Inicio:",
        start_date.strftime("%d/%m/%Y"),
        "fin:",
        end_date.strftime("%d/%m/%Y"),
    )

    dates_list = generate_dates_until_today(start_date, end_date)

    last_five_downloads = []

    text_area_placeholder = st.empty()

    for day in dates_list:
        file_name = f"datohorario{day}.txt"
        save_path: Path = relative_path / f"{day[0:4]}" / f"{day[4:6]}" / file_name

        url: str = (
            f"https://ssl.smn.gob.ar/dpd/descarga_opendata.php?file=observaciones/datohorario{day}.txt"
        )
        if not save_path.exists():
            fetch_daily_data(url, save_path)
            last_five_downloads.append(file_name)

            if len(last_five_downloads) > 5:
                last_five_downloads.pop(0)
                with text_area_placeholder.container():
                    text_area_content = "\n".join(last_five_downloads)
                    text_area_placeholder.text_area(
                        "Archivos descargados:", text_area_content, height=200
                    )

    st.success("¡Todos los archivos han sido descargados!")

    output_parquet_file = relative_path / output_file_name

    if os.path.exists(output_parquet_file):
        previus_data = pd.read_parquet(output_parquet_file, engine="pyarrow")
    else:
        previus_data = pd.DataFrame()

    new_data = []
    for txt_file in relative_path.rglob("*.txt"):
        datahorario_smn = parser.datohorario(txt_file)
        new_data.append(datahorario_smn)

    if new_data:
        new_data = pd.concat(new_data, ignore_index=True)
        if previus_data.empty:
            previus_data = new_data
        else:
            previus_data = pd.concat([previus_data, datahorario_smn], ignore_index=True)

    previus_data.to_parquet(output_parquet_file, engine="pyarrow")


st.title("Descargar datos diarios desde el SMN")


output_file_name = st.text_input(
    "Nombre del arhivo de salida:", value="datosdiarios_smn.parquet"
)

try:
    start_date, end_date = st.date_input(
        "Seleccione un rango de fechas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY",
    )
except ValueError:
    st.error("Por favor, seleccione un rango de fechas")

if st.button("Descargar información"):
    if output_file_name and start_date and end_date:
        download(start_date, end_date, output_file_name)
    else:
        st.error("Por favor, ingresa los campos antes de continuar")
