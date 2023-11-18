
import os
from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, Request
from fastapi_sso.sso.google import GoogleSSO
import fastapi

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
CLIENT_ID = "142977308709-8rmnnqbjqqg421il5t3rjh8b3f4f1s7p.apps.googleusercontent.com"
CLIENT_SECRET ="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"

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)