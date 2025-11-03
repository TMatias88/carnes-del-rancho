import os, base64, hashlib, requests
from datetime import datetime, timezone

PTP_LOGIN = os.getenv("PTP_LOGIN", "")
PTP_TRANKEY = os.getenv("PTP_TRANKEY", "")
PTP_ENDPOINT = os.getenv("PTP_ENDPOINT", "").rstrip("/")
RETURN_URL = os.getenv("RETURN_URL", "")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

def _auth():
    seed = datetime.now(timezone.utc).isoformat()
    tran_key = base64.b64encode(hashlib.sha1((seed + PTP_TRANKEY).encode()).digest()).decode()
    return {"login": PTP_LOGIN, "seed": seed, "tranKey": tran_key}

def create_session(order_number: str, total_crc: str, description: str, email: str):
    payload = {
        "auth": _auth(),
        "payment": {
            "reference": order_number,
            "description": description,
            "amount": {"currency": "CRC", "total": str(total_crc)},
            "buyer": {"email": email} if email else None
        },
        "returnUrl": f"{RETURN_URL}?order={order_number}",
        "notifyUrl": WEBHOOK_URL,
        "ipAddress": "127.0.0.1",
        "userAgent": "Django"
    }
    r = requests.post(PTP_ENDPOINT + "/session", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

def query_session(request_id: str):
    r = requests.post(f"{PTP_ENDPOINT}/session/{request_id}", json={"auth": _auth()}, timeout=30)
    r.raise_for_status()
    return r.json()
