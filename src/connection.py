import urllib.parse

import requests


def connection_api():
    client_id = "9f9bc5b3-998d-40ea-b538-b129c8412e83"
    redirect_uri = "https://127.0.0.1:8000/oauth2/callback"
    #secret = "XLwBUbenls6c7ebSJPlRyuQzGYiAl8zgt2blrAev"
    url = "https://gderabota.ru/oauth/authorize"

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        "Content-Type": "application/json",
    }
    data = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        # "scope": ""
    }

    encode_params = urllib.parse.urlencode(data)
    full_url = f"{url}?{encode_params}"
    try:
        response = requests.request("GET", full_url, headers=header)
        response.raise_for_status()

        # print("URL для перенаправления пользователя:\n", response.url)
        # print("Куки:\n", response.cookies.get_dict().get("XSRF-TOKEN"))  # Выводим куки
        return response.url


    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


def login_connection(url: str):

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Content-Type': 'application/json'
    }

    #data = {
        #"email": email
    #}

    response = requests.request("GET", url,  headers=header)
    response.raise_for_status()
    result = response.json()
    return result

if __name__ == "__main__":
    x = connection_api()
    print(x)
    #z = login_connection(x)
    #print(z)
