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
            print("URL: " + url)
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
        print("API Status: " + str(json_status) + " = A successful route call.")
        print("=============================================")
        print("Directions from " + orig + " to " + dest)
        print("Trip Duration:   " + json_data["route"]["formattedTime"])
        print("=============================================")
        print("Directions:")
        for maneuver in json_data["route"]["legs"][0]["maneuvers"]:
            print(f"{maneuver['narrative']} ({'%.2f' % (maneuver['distance'] * 1.61)} km)")
        print("=============================================\n")
    elif json_status == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")
    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")
    else:
        print("************************************************************************")
        print("For Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")

if __name__ == "__main__":
    get_directions()