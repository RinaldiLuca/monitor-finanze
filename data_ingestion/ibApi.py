import requests
import json
from data_models.transaction import ApiTransactionRaw


def get_new_token(KEY_PATH: str = "keys.json"):
    url = "https://bankaccountdata.gocardless.com/api/v2/token/new/"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    with open(KEY_PATH, "rb") as f:
        data = json.load(f)

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()["access"]
        else:
            raise
    except:
        raise


def get_institutions(ACCESS_TOKEN: str) -> list[dict]:
    url = "https://bankaccountdata.gocardless.com/api/v2/institutions/"
    headers = {"accept": "application/json", "Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"country": "it"}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise
    except:
        raise


def make_requisition(ACCESS_TOKEN: str, bank_id: str, _ref: str = "111"):
    try:
        response = requests.post(
            url="https://bankaccountdata.gocardless.com/api/v2/requisitions/",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {ACCESS_TOKEN}",
            },
            json={
                "redirect": "http://www.yourwebpage.com",
                "institution_id": bank_id,
                "reference": _ref,
                "user_language": "IT",
            },
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise
    except:
        raise


def get_requisitions(ACCESS_TOKEN: str):
    try:
        response = requests.get(
            url="https://bankaccountdata.gocardless.com/api/v2/requisitions/",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {ACCESS_TOKEN}",
            },
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise
    except:
        raise


def get_requisition_byId(ACCESS_TOKEN: str, id: str):
    try:
        response = requests.get(
            url=f"https://bankaccountdata.gocardless.com/api/v2/requisitions/{id}/",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {ACCESS_TOKEN}",
            },
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise
    except:
        raise


def get_transactions(ACCESS_TOKEN: str, account: str) -> list[ApiTransactionRaw]:
    try:
        response = requests.get(
            url=f"https://bankaccountdata.gocardless.com/api/v2/accounts/{account}/transactions/",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {ACCESS_TOKEN}",
            },
        )
        if response.status_code == 200:
            data = response.json()
            trxs = [
                ApiTransactionRaw(
                    booking_dt=tx["bookingDate"],
                    value_dt=tx["valueDate"],
                    amount=tx["transactionAmount"]["amount"],
                    description=tx["remittanceInformationUnstructured"],
                    external_id=tx["transactionId"],
                )
                for tx in data["transactions"]["booked"]
            ]
            return trxs
        else:
            raise
    except:
        raise


# In futuro bisogna implementare lo status: booked vs pending
