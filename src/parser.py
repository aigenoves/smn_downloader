import re
from pathlib import Path
from datetime import datetime
from typing import Any
import pandas as pd

pattern = re.compile(
    r"(\d{8})\s+(\d+)\s+(-?[\d.]+)\s+(\d+)\s+(-?[\d.]+)\s+(\d+)\s+(-?[\d.]+)\s+(.+)"
)


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
            match = pattern.match(line)
            if match:
                messure_date = datetime.strptime(match.group(1), "%d%m%Y")

                hour = f"{int(match.group(2)):02d}:00"  # Hora
                temperature = float(match.group(3))  # Temperatura
                humidity = int(match.group(4))  # Humedad
                pressure = float(match.group(5))  # Presión
                wind_dir = int(match.group(6))  # Direccion del viento
                wind_vel = float(match.group(7))  # Velocidad del viento
                location = match.group(8).strip()  # Ubicación
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
