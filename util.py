import json
import random
import string

import requests
from stem import Signal
from stem.control import Controller

BATCH_SIZE = 100
BATCHES = 5
REFERAL_CODE = "CHMX"

# TO Request URL with SOCKS over TOR
PROXY = 'socks5://localhost:9050'

with open("male.txt") as f:
    names = f.readlines()
    males = [str(m).strip().title() for m in names]

with open("female.txt") as f:
    names = f.readlines()
    females = [str(m).strip().title() for m in names]

with open("last.txt") as f:
    names = f.readlines()
    lasts = [str(m).strip().title() for m in names]


def generator_emails():
    # joined = males + females
    # random.shuffle(joined)
    # random.shuffle(lasts)
    # emails = [
    #     "gmail",
    #     "hotmail",
    #     "outlook",
    #     "googlemail"
    # ]
    # for fname in joined[:BATCH_SIZE]:
    #     for lname in lasts[:BATCH_SIZE]:
    #         domain = random.choice(emails)
    #         chars = "".join([random.choice(string.ascii_letters) for _ in range(2)])
    #         yield f"{fname}{chars}{lname}@{domain}.com"

    for _ in range(BATCH_SIZE):
        yield "".join([random.choice(string.ascii_letters) for _ in range(32)]) + "@gmail.com"

    # word = "alexanderfanthome"
    # # word = string.ascii_lowercase
    # for prod in product((".", ""), repeat=len(word) - 1):
    #     mixed = [char for tpl in zip(word, prod + ("",)) for char in tpl]
    #     new_word = "".join(mixed)
    #     yield f"{new_word}@gmail.com"


def setup_session():
    s = requests.Session()
    s.headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
    }
    # s.proxies = {
    #     'all_proxy': PROXY,
    #     'http': PROXY,
    #     'https': PROXY
    # }
    return s


def get_new_identity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)


def get_current_ip():
    session = requests.session()

    session.proxies = {
        'all_proxy': PROXY,
        'http': PROXY,
        'https': PROXY
    }

    try:
        r = session.get('http://httpbin.org/ip')
    except Exception as e:
        print(str(e))
    else:
        return json.loads(r.text)["origin"].split(", ")[0]


if __name__ == '__main__':
    for _ in range(5):
        print(get_current_ip())
        get_new_identity()
