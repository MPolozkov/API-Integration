import os
import urllib

from fastapi import HTTPException, APIRouter, Request
from urllib.parse import urlparse, urlunparse
import httpx

from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

authorize_url = os.getenv("AUTHORIZE_URL")
token_url = os.getenv("TOKEN_URL")


router = APIRouter()


@router.get("/connect")
async def connection_api():
    """Создает URL для авторизации пользователя через OAuth2."""
    data = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": ""
    }
    encode_params = urllib.parse.urlencode(data)
    full_url = f"{authorize_url}?{encode_params}"

    try:
        return full_url

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/oauth2/callback")
async def callback(request: Request):
    """Обработчик callback-а OAuth2. Получает `code` из callback URL."""

    try:
        redirect_url = str(request.url)

        parsed_url = urlparse(redirect_url)
        url_http = urlunparse(parsed_url._replace(scheme='http'))

        parsed_url = urllib.parse.urlparse(str(url_http))
        query_params = urllib.parse.parse_qs(parsed_url.query)

        error = query_params.get('error', [None])[0]

        if error:
            error_description = query_params.get('error_description', [''])[0]
            raise HTTPException(status_code=400, detail=f"Ошибка OAuth2: {error}. {error_description}")

        code = query_params.get('code', [None])[0]
        print(code)

        if code:
            return code
        else:
            raise HTTPException(status_code=400, detail="Code отсутствует в URL редиректа")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/oauth2/token")
async def token(auth_code: str):
    """Получение токена"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        "Content-Type": "application/json"
    }

    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": auth_code
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(token_url, headers=headers, json=data, follow_redirects=False)
            response.raise_for_status()
            token_data = response.json()

            return token_data

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
