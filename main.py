import time
from multiprocessing.pool import ThreadPool
from pprint import pprint

from util import setup_session, BATCH_SIZE, generator_emails, REFERAL_CODE, BATCHES, get_new_identity


def main():
    while True:
        # get_new_identity()
        with ThreadPool(processes=BATCHES) as p:
            p.map(send_batch, range(BATCHES))


def send_batch(_):
    with ThreadPool(processes=BATCH_SIZE) as p:
        statuses = p.map(process_email, generator_emails())
    merged = {k: v for x in statuses for k, v in x.items() if v == "error"}
    if len(list(merged.keys())) > 0:
        pprint(merged, indent=4)


def process_email(email):
    try:
        print(email)
        s = setup_session()
        # resp = s.get(f"https://uk.robinhood.com/{REFERAL_CODE}")
        # if not resp.ok:
        #     return {email: "error"}
        # resp = s.options("https://api.robinhood.com/midlands/tailgate/devonshire/spot/")
        # if not resp.ok:
        #     return {email: "error"}
        post_data = {
            "email": email,
            "referral_code": REFERAL_CODE
        }
        sleep_time = 1e-14
        while True:
            resp = s.post("https://api.robinhood.com/midlands/tailgate/devonshire/spot/", data=post_data)
            if int(resp.status_code) != 429:
                break
            time.sleep(sleep_time)
            sleep_time *= 2.0
        if not resp.ok:
            return {email: "error"}
        # resp = s.get(f"https://api.robinhood.com/midlands/tailgate/devonshire/spot/{email}/")
        # if not resp.ok:
        #     return {email: "error"}
        return {email: "ok"}
    except:
        return {email: "error"}


if __name__ == '__main__':
    main()
