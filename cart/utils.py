import datetime
import string
import random


def generate_order_id():
    date_str = datetime.datetime.now().strftime('%Y%m%d%H%M')[2:]
    rand_str = ''.join([random.choice(string.digits) for i in range(3)])
    return date_str + rand_str
