import re
from pathlib import Path
from datetime import datetime
from typing import Any
import pandas as pd
from .utils import coords_dms_to, Logger, replace_station_name


main_path = Path(__file__).resolve()
main_directory = main_path.parent.parent
relative_path = main_directory / "data"
stations_smn_file = relative_path / "estaciones_smn.parquet"
df = pd.read_parquet(stations_smn_file)


stations_names = df["nombre"].tolist()


def datohorario(data_file: Path) -> pd.DataFrame:
    """
    Recorre todas las carpetas en la ruta dada, parsea los archivos de texto usando regex y
    genera un único archivo parquet de salida.

    Args:
        data_dir (Path): Ruta al directorio base (por ejemplo, "data").
    """

    all_data = []
    with open(data_file, "r", encoding="latin1") as file:
        lines = file.readlines()
        for line in lines:
            if line[0].isdigit():
                messure_date = datetime.strptime(line[0:8].strip(), "%d%m%Y")
                hour = f"{int(line[8:14].strip()):02d}:00"  # Hora
                temperature = (
                    float(line[14:20].strip()) if line[14:20].strip() != "" else None
                )  # Temperatura
                humidity = (
                    int(line[20:25].strip()) if line[20:25].strip() != "" else None
                )  # Humedad
                pressure = (
                    float(line[25:33].strip()) if line[25:33].strip() != "" else None
                )  # Presión
                wind_dir = (
                    int(line[33:38].strip()) if line[33:38].strip() != "" else None
                )  # Direccion del viento
                wind_vel = (
                    float(line[38:45].strip()) if line[38:45].strip() != "" else None
                )  # Velocidad del viento
                location = (
                    line[45:].strip()
                    if line[45:].strip()[0:5] != "PCIA."
                    else replace_station_name("PCIA.")
                )  # Ubicación
                fecha_hora = datetime.combine(
                    messure_date.date(), datetime.strptime(hour, "%H:%M").time()
                )
                if location in stations_names:
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
                elif replace_station_name(location) != "":
                    all_data.append(
                        [
                            fecha_hora,
                            temperature,
                            humidity,
                            pressure,
                            wind_dir,
                            wind_vel,
                            replace_station_name(location),
                        ]
                    )
                    message = f"{location}->{replace_station_name(location)} archivo: {str(data_file).split('/')[-1]}"
                    Logger.add_to_log("info", message=message)

                else:
                    message = f"No existe la estacion con nombre {location} archivo: {str(data_file).split('/')[-1]}"
                    Logger.add_to_log("warning", message=message)

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
