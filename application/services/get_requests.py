import requests


def get_astronaut():
    url = "http://api.open-notify.org/astros.json"
    r = requests.get(url, auth=("user", "pass"))
    numbers_astronauts = len(r.json()["people"])
    print(f"Currently {numbers_astronauts} astronauts.")
