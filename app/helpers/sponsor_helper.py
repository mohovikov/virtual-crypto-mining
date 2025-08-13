from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta


def add_sponsor_time(current_expire, amount, unit):
    """
    Добавляет время к sponsor_expire.

    :param current_expire: datetime или None
    :param amount: int — количество
    :param unit: str — hours | days | months | years
    :return: datetime — новая дата окончания
    """
    now = datetime.now(timezone.utc)
    start_time = max(now, current_expire or now)

    if unit == "hours":
        return start_time + timedelta(hours=amount)
    elif unit == "days":
        return start_time + timedelta(days=amount)
    elif unit == "months":
        return start_time + relativedelta(months=amount)
    elif unit == "years":
        return start_time + relativedelta(years=amount)
    else:
        raise ValueError(f"Неверная единица измерения: {unit}")
