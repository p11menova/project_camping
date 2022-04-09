import datetime as dt
import random


def make_dates():
    format_to = "%d.%m.%Y"
    format_form ="%Y-%m-d" #strptime
    now = dt.datetime.now()

    start_of_hiking = now + dt.timedelta(days=random.randint(1, 30)) # дата начала
    end_of_hiking = start_of_hiking + dt.timedelta(days=random.randint(6, 20))


    return start_of_hiking.strftime(format_to), end_of_hiking.strftime(format_to)

make_dates()
print('2020-05-98'.strptime("%Y-%m-d").strftime('%d.%m.%Y'))
