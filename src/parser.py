import re
from pathlib import Path
from datetime import datetime
from typing import Any
import pandas as pd
from .utils import coords_dms_to


def datohorario(data_file: Path) -> pd.DataFrame:
    """
    Recorre todas las carpetas en la ruta dada, parsea los archivos de texto usando regex y
    genera un único archivo parquet de salida.

    Args:
        data_dir (Path): Ruta al directorio base (por ejemplo, "data").
    """

    all_data = []
    with open(data_file, "r", encoding="latin-1") as file:
        lines = file.readlines()
        for line in lines:
            if line[0].isdigit():
                messure_date = datetime.strptime(line[0:8].strip(), "%d%m%Y")
                hour = f"{int(line[8:14].strip()):02d}:00"  # Hora
                temperature = (
                    float(line[14:20].strip()) if line[14:20].strip() != "" else 0
                )  # Temperatura
                humidity = (
                    int(line[20:25].strip()) if line[20:25].strip() != "" else 0
                )  # Humedad
                pressure = (
                    float(line[25:33].strip()) if line[25:33].strip() != "" else 0
                )  # Presión
                wind_dir = (
                    int(line[33:38].strip()) if line[33:38].strip() != "" else 0
                )  # Direccion del viento
                wind_vel = (
                    float(line[38:45].strip()) if line[38:45].strip() != "" else 0
                )  # Velocidad del viento
                location = line[45:].strip()  # Ubicación
                fecha_hora = datetime.combine(
                    messure_date.date(), datetime.strptime(hour, "%H:%M").time()
                )

                all_data.append(
                    [
                        fecha_hora,
                        temperature,
                        humidity,
                        pressure,
                        wind_dir,
                        wind_vel,
                        location,
                    ]
                )
    return pd.DataFrame(
        all_data,
        columns=[
            "fecha_hora",
            "temperatura",
            "humedad",
            "presion",
            "viento_d",
            "viento_v",
            "ubicacion",
        ],
    )


def estaciones(data_file: Path) -> pd.DataFrame:
    all_data = []
    with open(data_file, "r", encoding="latin-1") as file:
        lines = file.readlines()[1:]
        for i, line in enumerate(lines):
            print(f"{i}: {line[57:62]}")
            station_name = line[0:34].strip()
            state_name = line[34:54].strip()
            lat_degree = int(line[54:57].strip())
            lat_minute = int(line[57:62].strip())
            lon_degree = int(line[62:69].strip())
            lon_minute = int(line[69:74].strip())
            height = int(line[74:81].strip())
            number = int(line[81:90].strip())
            oaci_code = line[90:].strip()

            all_data.append(
                [
                    station_name,
                    state_name,
                    coords_dms_to(
                        lat_degree,
                        lat_minute,
                    ),
                    coords_dms_to(lon_degree, lon_minute),
                    height,
                    number,
                    oaci_code,
                ]
            )
    return pd.DataFrame(
        all_data,
        columns=[
            "nombre",
            "provincia",
            "lat",
            "lon",
            "altura",
            "numero",
            "oaci",
        ],
    )
