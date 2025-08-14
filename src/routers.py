from fastapi import HTTPException, Query, APIRouter, Request
from fastapi.responses import RedirectResponse
from typing import Optional
import urllib.parse
import httpx
import json


CLIENT_ID = "9f9bc5b3-998d-40ea-b538-b129c8412e83"
CLIENT_SECRET = "XLwBUbenls6c7ebSJPlRyuQzGYiAl8zgt2blrAev"
REDIRECT_URI = "https://127.0.0.1:8000/oauth2/callback"
AUTHORIZE_URL = "https://gderabota.ru/oauth/authorize"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    "Content-Type": "application/json",
}

redirect_url_global = ""

router = APIRouter()


@router.get("/connect")
async def connection_api():
    """Создает URL для авторизации пользователя через OAuth2."""
    data = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
    }
    encode_params = urllib.parse.urlencode(data)
    full_url = f"{AUTHORIZE_URL}?{encode_params}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(full_url, headers=HEADERS, follow_redirects=False)
            response.raise_for_status()

            redirect_url_global = response.headers.get("Location")
            if redirect_url_global:
                return RedirectResponse(redirect_url_global)  # перенаправление
            else:
                raise HTTPException(status_code=500, detail="Location header not found")

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def login_submit(requests: Request, email: str):
    """Получает данные с формы логина, отправляет их и редиректит обратно."""

    global redirect_url_global

    if not redirect_url_global:
        raise HTTPException(status_code=400, detail="Redirect URL not available")

    form_data = {
        "email": email
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(redirect_url_global, data=form_data, follow_redirects=True)
            response.raise_for_status()
            return RedirectResponse(redirect_url_global)

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/oauth2/callback")
async def oauth2_callback():
    """Получает code и обменивает на access_token."""
    token_data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        #"code": code,
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(AUTHORIZE_URL, headers=HEADERS, json=token_data)
            response.raise_for_status()
            token = response.json()
            return token # Возвращаем access_token, refresh_token
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

