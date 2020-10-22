import requests
import time
import json
from exceptions import *


def load_settings() -> dict:
    try:
        with open('settings.txt', 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        if cfg['amount'] < 10:
            raise InvalidAmount("Wrong amount. Min amount is 10.")
        return cfg

    except FileNotFoundError:
        config = {"amount": 10, "qiwi_api": ""}
        with open('settings.txt', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        raise InvalidSettings("Fill settings.txt")

def send_steam(login: str) -> dict:
    s = requests.Session()
    s.headers['Accept'] = 'application/json'
    s.headers['Content-Type'] = 'application/json'
    s.headers['authorization'] = 'Bearer ' + API_TOKEN

    postjson = {"id":"","sum": {"amount":"","currency":"643"},"paymentMethod": {"type":"Account","accountId":"643"},"fields": {"account":""}}
    postjson['id'] = str(int(time.time() * 1000))
    postjson['sum']['amount'] = str(PAYMENT)
    postjson['fields']['account'] = login

    res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/25549/payments', json = postjson)
    # If exception simplejson.errors.JSONDecodeError recheck qiwi api token
    return res.json()

def load_accs() -> list:
    try:
        with open('accs_for_dep.txt', 'r', encoding='utf-8') as f:
            accs = f.readlines()
            if accs != []:
               accs = [x.split(':')[0] for x in accs]
            else:
                raise AccsNotFound("Fill accs_for_dep.txt")
            return accs
    except FileNotFoundError:
        with open('accs_for_dep.txt', 'w', encoding='utf-8') as f:
            pass
        raise AccsNotFound("Fill accs_for_dep.txt")

cfg = load_settings()
accs = load_accs()

PAYMENT = cfg['amount']
API_TOKEN = cfg['qiwi_api']

if API_TOKEN == "":
    raise InvalidApi("Wrong api.")

print("Payment amount: {}\nCount accounts: {}".format(str(PAYMENT), str(len(accs))))

input("Press Enter for continue...")

for acc in accs:
    print("account: {}".format(acc))
    print("response:", send_steam(acc))
else:
    print("Well done!")
    time.sleep(120)
    quit()