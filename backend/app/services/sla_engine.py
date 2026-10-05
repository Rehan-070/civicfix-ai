import datetime

CATEGORY_SLA_HOURS = {
    "Pothole": 72,
    "Garbage": 24,
    "Overflowing Garbage Bin": 24,
    "Broken Streetlight": 48,
    "Water Leakage": 24,
    "Drainage Problem": 48,
    "Damaged Road": 72,
    "Damaged Footpath": 120,
    "Fallen Tree": 12,
}

DEFAULT_SLA_HOURS = 72

def get_sla_hours(category: str) -> int:
    """Returns SLA hours deterministically based on issue category."""
    return CATEGORY_SLA_HOURS.get(category, DEFAULT_SLA_HOURS)

def calculate_sla_deadline(submitted_at: datetime.datetime, sla_hours: int) -> datetime.datetime:
    """Calculates the exact SLA deadline timestamp."""
    if submitted_at.tzinfo is None:
        submitted_at = submitted_at.replace(tzinfo=datetime.timezone.utc)
    return submitted_at + datetime.timedelta(hours=sla_hours)

def is_sla_breached(submitted_at: datetime.datetime, sla_hours: int, now: datetime.datetime = None) -> bool:
    """Deterministically checks if SLA deadline has passed."""
    if now is None:
        now = datetime.datetime.now(datetime.timezone.utc)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=datetime.timezone.utc)
        
    deadline = calculate_sla_deadline(submitted_at, sla_hours)
    return now > deadline
