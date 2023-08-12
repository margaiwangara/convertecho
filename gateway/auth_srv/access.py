import requests
from config import settings


def login(request):
    auth = request.authorization

    if not auth:
        return None, ("Invalid credentials", 401)

    basic_auth = (auth.username, auth.password)

    response = requests.post(
        f"http://{settings.AUTH_SERVICE_ADDRESS}/login", auth=basic_auth)

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
