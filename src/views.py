import requests


def api_connect(email: str) -> str | None:
    url = f"https://gderabota.ru/login"

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'


    headers = {
        'Content-Type': 'application/json',
        'User-Agent': user_agent
    }


    data = {
        'email': email,
    }

    try:
        response = requests.request("POST", url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при инициализации входа: {e}")
        return None


if __name__ == "__main__":
    x = api_connect('pipl82308@gmail.com')
    print(x)

