from . import jalali
from tzlocal import get_localzone

def jalali_date_time_converter(time):
    jmonth = [
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
    ]

    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)
    for index, month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    time = time.astimezone(get_localzone())
    
    hour='PM' if((time.hour) <= 12) else 'AM'
    # output = f"{time_to_list[2]} {time_to_list[1]} {time_to_list[0]} . {time.hour}:{time.minute}"
    output = f"{time.hour if((time.hour) <= 12) else (time.hour)-12}:{time.minute} {hour}"

    return output


def jalali_converter(time):
    jmonth = [
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
    ]
    # time=timezone.localtime()

    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)
    for index, month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = f"{time_to_list[2]} {time_to_list[1]} {time_to_list[0]}"
    return output


def date(time):
    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time = jalali.Gregorian(time_to_str).persian_string()
    return time[0:4]