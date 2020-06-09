from datetime import datetime

import pytz

from config import get_config

_config = get_config()

_timezone = []
for tz_str in _config.get("CurrentDatetime", "Timezone").split(","):
    try:
        _timezone.append(pytz.timezone(tz_str))
    except Exception as e:
        print(f"Failed to load timezone: {tz_str}")
        print(f"Error: {e}")
if not _timezone:
    _timezone = [pytz.UTC]


class _TimezoneRotate:
    COUNT_TO_NEXT = _config.getint("CurrentDatetime", "ToNext")
    COUNT_CURRENT = 0

    CURRENT_IDX = 0

    TZ_COUNT = len(_timezone)  # Storing this to improve performance

    @classmethod
    def get_tz(cls):
        tz = _timezone[cls.CURRENT_IDX]

        cls.COUNT_CURRENT += 1
        if cls.COUNT_CURRENT < cls.COUNT_TO_NEXT:
            return tz

        cls.COUNT_CURRENT = 0
        cls.CURRENT_IDX += 1

        if cls.CURRENT_IDX >= cls.TZ_COUNT:
            cls.CURRENT_IDX = 0

        return tz


def get_current_date_time() -> str:
    # Expression will be processed in `current_dt.html`
    tz = _TimezoneRotate.get_tz()

    return datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(tz).strftime(f"%Y-%m-%d|%H:%M:%S|{tz.zone}")
