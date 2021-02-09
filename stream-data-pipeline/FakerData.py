from faker import Faker
import time
import random
import os
import numpy as np
from datetime import datetime, timedelta

LINE = """\
 "{fullname}" - - [{time_local}] "{user_name}" "{email}" "{iban}" "{ipv6}" "{mac_address}" "{address}"\
"""


def generate_log_line():
    """ Perform the generation of a line of fake data
    :keyword: none
    :return: line of data
    """
    fake = Faker()
    now = datetime.now()
    fullname = fake.name()
    time_local = now.strftime('%d/%b/%Y:%H:%M:%S')
    user_name = fake.user_name()
    email = fake.email()
    iban = fake.iban()
    ipv6 = fake.ipv6()
    mac_address = fake.mac_address()
    address = fake.address()

    log_line = LINE.format(
        fullname=fullname,
        time_local=time_local,
        user_name=user_name,
        email=email,
        iban=iban,
        ipv6=ipv6,
        mac_address=mac_address,
        address=address
    )

    return log_line

#Testing fake data generation
for _ in range(5):
    print(generate_log_line())
