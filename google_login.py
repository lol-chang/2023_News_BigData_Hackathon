
import os
from fastapi.responses import JSONResponse


from fastapi import FastAPI, Request
from fastapi_sso.sso.google import GoogleSSO

from utils.getConfig import get_config


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
CLIENT_ID = get_config().get("Google Client Token", "CLIENT_ID")
CLIENT_SECRET = get_config().get("Google Client Token", "CLIENT_SECRET")

app = FastAPI()

sso = GoogleSSO(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://127.0.0.1:8000/auth/callback",
    allow_insecure_http=True,
)


@app.get("/auth/login")
async def auth_init():
    with sso:
        return await sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})


@app.get("/auth/callback")
async def auth_callback(request: Request):
    with sso:
        user = await sso.verify_and_process(request)

    data = {
        "id": user.id,
        "email": user.email,
        "display_name": user.display_name
    }

    return JSONResponse(content=data, headers={"Content-Type": "application/json; charset=UTF-8"})