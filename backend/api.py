import hashlib
import hmac
import os
import time
import urllib.parse
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="CU_project API")


class ValidateInitDataRequest(BaseModel):
    init_data: str
    max_age_seconds: int = 60 * 60


class ValidateInitDataResponse(BaseModel):
    ok: bool
    user_id: Optional[int] = None


@app.get("/health")
def health():
    return {"ok": True}


def _check_webapp_signature(init_data: str, bot_token: str) -> dict:
    """
    Validate Telegram WebApp initData signature.
    Ref: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
    """
    parsed = urllib.parse.parse_qsl(init_data, keep_blank_values=True)
    data = dict(parsed)
    received_hash = data.pop("hash", None)
    if not received_hash:
        raise HTTPException(status_code=400, detail="Missing hash in init_data")

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256).digest()
    calc_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calc_hash, received_hash):
        raise HTTPException(status_code=401, detail="Invalid init_data signature")
    return data


@app.post("/telegram/validate_init_data", response_model=ValidateInitDataResponse)
def validate_init_data(body: ValidateInitDataRequest):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise HTTPException(status_code=500, detail="Server missing TELEGRAM_BOT_TOKEN env var")

    data = _check_webapp_signature(body.init_data, bot_token)

    auth_date = data.get("auth_date")
    if auth_date:
        age = int(time.time()) - int(auth_date)
        if age > body.max_age_seconds:
            raise HTTPException(status_code=401, detail="init_data expired")

    user_id = None
    user_raw = data.get("user")
    if user_raw:
        # user is a JSON string in initData
        # we keep it minimal here (front-end can send full user JSON to backend if needed)
        try:
            import json

            user_id = int(json.loads(user_raw).get("id"))
        except Exception:
            user_id = None

    return ValidateInitDataResponse(ok=True, user_id=user_id)

