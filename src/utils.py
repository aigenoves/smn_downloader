from datetime import datetime, timedelta


def generate_dates_until_today(
    start_date: datetime = datetime(2017, 11, 26)
) -> list[str]:
    """
    Genera una lista de fechas en el formato YYYYMMDD desde el 1 de enero del año dado hasta hoy.

    :param start_year: El año desde el cual empezar a generar fechas.
    :return: Una lista de strings con fechas en el formato YYYYMMDD.
    """
    end_date = datetime.now() - timedelta(days=1)
    if start_date.date() > end_date.date():
        raise ValueError(
            "La fecha de inicio no puede ser mayor o igual a la fecha actual."
        )

    if start_date < datetime(2017, 11, 26):
        start_date = datetime(2017, 11, 26)

    dates = []
    current_date = start_date

    while current_date.date() <= end_date.date():
        dates.append(current_date.strftime("%Y%m%d"))
        current_date += timedelta(days=1)

    return dates
