from datetime import datetime, timedelta

from dateutil import parser


def _to_time_delta_str(t_delta: timedelta) -> str:
    h = t_delta.seconds // 3600
    m = (t_delta.seconds - 3600 * h) // 60
    s = t_delta.seconds % 60

    if h > 3:
        return f"{h + t_delta.days * 24:02}:{m:02}:{s:02}"
    else:
        return f"{h * 60 + m:02}:{s:02}"


def get_timer_diff(dt_str: str, *, count_up: bool = False, end_message: str = "") -> str:
    """
    Parse ``dt_str`` and calculate the difference between now and the parsed :class:`datetime`.

    If the parse failed, return ``ERR``.

    If the due time of the timer has passed:

    - ``count_up`` is ``True``, return the difference between now and the past :class:`datetime`.
      ``end_message`` will be ignored.

    - ``count_up`` is ``False``, return the end message,
      which is either the specified one or an empty string by default.

    .. note::
        The beginning of ``end_message`` **MUST NOT** be either ``+`` or ``-``,
        because the first character will be used to determine the status of the timer.

    :param dt_str: datetime string to be parsed and calculated
    :param count_up: if the timer should count up
    :param end_message: end message of the timer, if not counting up
    :return: expression of the timer status
    :raises ValueError: if `end_message` starts with either + or -
    """
    if count_up is None:
        count_up = False

    if end_message is None:
        end_message = ""

    if end_message.startswith("+") or end_message.startswith("-"):
        raise ValueError("`end_message` must not start with either + or -")

    try:
        dt = parser.parse(dt_str, ignoretz=True)
    except (ValueError, OverflowError):
        return "ERROR"

    now = datetime.now()

    if dt > now:
        return f"-{_to_time_delta_str(dt - now)}"
    else:
        if count_up:
            return f"+{_to_time_delta_str(now - dt)}"
        else:
            return end_message
