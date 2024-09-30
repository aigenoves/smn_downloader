import datetime
from pathlib import Path
import logging
import logging.handlers
import traceback

STATIONS_REPLACEMENTS_NAME = {
    "ESCUELA DE AVIACION MILITA": "ESCUELA DE AVIACION MILITAR AERO",
    "ESC.AVIACION MILITAR AERO": "ESCUELA DE AVIACION MILITAR AERO",
    "PRESIDENCIA ROQUE SAENZ PE": "PRESIDENCIA ROQUE SAENZ PENA AERO",
    "PCIA.": "PRESIDENCIA ROQUE SAENZ PENA AERO",
    "VILLA DE MARIA DEL RIO SEC": "VILLA DE MARIA DEL RIO SECO",
    "VILLA MARIA DEL RIO SECO": "VILLA DE MARIA DEL RIO SECO",
    "BUENOS AIRES": "BUENOS AIRES OBSERVATORIO",
    "LA QUIACA OBS.": "LA QUIACA OBSERVATORIO",
    "LAS FLORES AERO": "LAS FLORES",
    "OBERA AERO": "OBERA",
    "PILAR OBS.": "PILAR OBSERVATORIO",
    "SAN FERNANDO": "SAN FERNANDO AERO",
    "VENADO TUERTO": "VENADO TUERTO AERO",
}


class Logger:

    def __set_logger(self) -> logging.Logger:

        main_path = Path(__file__).resolve()
        main_directory = main_path.parent.parent
        relative_path = main_directory / "logs"
        log_file = relative_path / "app.log"

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(log_file, encoding="latin1")
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s", "%d-%m-%Y %H:%M:%S"
        )
        file_handler.setFormatter(formatter)

        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(file_handler)
        return logger

    @classmethod
    def add_to_log(cls, level: str, message: str) -> None:
        try:
            logger = cls.__set_logger(cls)
            if level == "critical":
                logger.critical(message)
            elif level == "debug":
                logger.debug(message)
            elif level == "error":
                logger.error(message)
            elif level == "info":
                logger.info(message)
            elif level == "warning":
                logger.warning(message)
        except Exception as e:
            print(traceback.format_exc())
            print(e)


def generate_dates_until_today(
    start_date: datetime.date = datetime.date(2017, 11, 26),
    end_date: datetime.date = datetime.date.today() - datetime.timedelta(days=1),
) -> list[str]:
    """
    Genera una lista de fechas en el formato YYYYMMDD desde el 1 de enero del año dado hasta hoy.

    :param start_year: El año desde el cual empezar a generar fechas.
    :return: Una lista de strings con fechas en el formato YYYYMMDD.
    """
    if start_date > end_date:
        raise ValueError(
            "La fecha de inicio no puede ser mayor o igual a la fecha actual."
        )

    if start_date < datetime.date(2017, 11, 26):
        start_date = datetime.date(2017, 11, 26)

    dates = []
    current_date = start_date

    while current_date <= end_date:
        dates.append(current_date.strftime("%Y%m%d"))
        current_date += datetime.timedelta(days=1)

    return dates


def coords_dms_to(degrees: int, minutes: int) -> float:
    decimal = degrees + (-minutes / 60)
    print(degrees, minutes, decimal)
    return decimal


def replace_station_name(name: str) -> str:
    return STATIONS_REPLACEMENTS_NAME.get(name, "")
