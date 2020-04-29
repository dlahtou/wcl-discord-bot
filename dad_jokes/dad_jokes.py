import requests
import urllib

ICANHAZDADJOKE_API_PATH = 'https://icanhazdadjoke.com/'

def get_dad_joke():
    r = requests.get(
        ICANHAZDADJOKE_API_PATH,
        headers={'Accept': 'text/plain'},
        )
    if r.status_code == 200:
        print("Sending dad joke!")
        return r.text
    else:
        return "Error retrieving dad joke, " + r.status_code
