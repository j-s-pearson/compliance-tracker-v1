from datetime import date, datetime

from compliance_tracker.constants import DATE_FORMATS


def get_now_iso() -> str:
    return datetime.now().date().isoformat()

def date_to_iso(input_date: str) -> str:
    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(input_date.strip(), fmt)
            return dt.date().isoformat()
        except ValueError:
            continue
    raise ValueError(f"Unrecognised date format: {input_date}.")

def is_before_now(iso_date: str) -> bool:
    today = datetime.now().date()
    dt = date.fromisoformat(iso_date)
    return dt < today
