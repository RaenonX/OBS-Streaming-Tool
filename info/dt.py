from datetime import datetime
from typing import Optional


def get_current_date_time(suffix: Optional[str] = None) -> str:
    dt_expr = datetime.now().strftime("%Y-%m-%d|%H:%M:%S")  # Returned expression will be split by "|"

    return f"{dt_expr}{' ' + suffix if suffix else ''}"
