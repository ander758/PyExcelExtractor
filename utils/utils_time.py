from xlrd.xldate import XLDateTooLarge, XLDateBadDatemode, XLDateNegative, XLDateAmbiguous, _XLDAYS_TOO_LARGE
import datetime


def summarize_durations(duration_list):
    """
    :param duration_list: List of durations, E.g. ['02:10:00', '00:45:00']
    :return: Sum of all durations
    """
    total_secs = 0
    for duration in duration_list:
        time_parts = [int(s) for s in str(duration).split(':')]
        total_secs += (time_parts[0] * 60 + time_parts[1]) * 60 + time_parts[2]
    total_secs, sec = divmod(total_secs, 60)
    hr, min = divmod(total_secs, 60)
    return "%d:%02d:%02d" % (hr, min, sec)


def time_to_seconds(time):
    """
    :param time: 'HH:MM:SS'
    :return: Total seconds
    """
    if type(time) == datetime.time:
        time = str(time)
    hrs = int(time[:2])
    mins = int(time[3:-3])
    sec = int(time[-2:])
    return hrs + mins / 60 + sec / 3600


def xldate_as_datetime(xldate, datemode):
    """
    https://stackoverflow.com/questions/1108428/how-do-i-read-a-date-in-excel-format-in-python
    :param xldate: worksheet.cell(rowx, colx).value - Float
    :param datemode: xlrd.open_workbook(path).datemode
    :return: datetime
    """
    if datemode not in (0, 1):
        raise XLDateBadDatemode(datemode)
    if xldate == 0.00:
        return datetime.time(0, 0, 0)
    if xldate < 0.00:
        raise XLDateNegative(xldate)
    xldays = int(xldate)
    frac = xldate - xldays
    seconds = int(round(frac * 86400.0))
    assert 0 <= seconds <= 86400
    if seconds == 86400:
        seconds = 0
        xldays += 1
    if xldays >= _XLDAYS_TOO_LARGE[datemode]:
        raise XLDateTooLarge(xldate)

    if xldays == 0:
        # second = seconds % 60; minutes = seconds // 60
        minutes, second = divmod(seconds, 60)
        # minute = minutes % 60; hour    = minutes // 60
        hour, minute = divmod(minutes, 60)
        return datetime.time(hour, minute, second)

    if xldays < 61 and datemode == 0:
        raise XLDateAmbiguous(xldate)

    return (datetime.datetime.fromordinal(xldays + 693594 + 1462 * datemode)
            + datetime.timedelta(seconds=seconds))
