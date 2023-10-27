import urllib.parse
import requests
from requests.exceptions import RequestException

MAIN_API = "https://www.mapquestapi.com/directions/v2/route?"
KEY = "NyjRA8irpWWldyZAKvqnnHncR7osQg9r"

def get_directions():
    while True:
        orig = input("Starting Location: ")
        if orig in ("quit", "q"):
            break

        dest = input("Destination: ")
        if dest in ("quit", "q"):
            break

        try:
            url = construct_url(orig, dest)
            print("\nFetching directions...")
            json_data = fetch_data(url)

            if json_data:
                process_data(json_data, orig, dest)
        except (RequestException, ConnectionError):
            print("An error occurred. Please check your internet connection.")
        except Exception as e:
            print("An unexpected error occurred:", str(e))

def construct_url(orig, dest):
    params = {
        "key": KEY,
        "from": orig,
        "to": dest
    }
    return MAIN_API + urllib.parse.urlencode(params)

def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def process_data(json_data, orig, dest):
    json_status = json_data.get("info", {}).get("statuscode")

    if json_status == 0:
        print("\n" + "=" * 50)
        print(f"Directions from {orig} to {dest}")
        print("=" * 50)
        directions = json_data["route"]["legs"][0]["maneuvers"]
        for i, maneuver in enumerate(directions, start=1):
            print(f"{i}. {maneuver['narrative']} ({'%.2f' % (maneuver['distance'] * 1.61)} km)")
        print("=" * 50)
    elif json_status == 402:
        print("\nStatus Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
    elif json_status == 611:
        print("\nStatus Code: " + str(json_status) + "; Missing an entry for one or both locations.")
    else:
        print("\nFor Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")

if __name__ == "__main__":
    print("Welcome to the MapQuest Directions App!")
    get_directions()