import datetime


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
