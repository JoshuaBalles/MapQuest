# Import necessary modules
import urllib.parse
import requests
from requests.exceptions import RequestException

# Define the MapQuest API endpoint and the API key
MAIN_API = "https://www.mapquestapi.com/directions/v2/route?"
KEY = "NyjRA8irpWWldyZAKvqnnHncR7osQg9r"

# Function to get directions
def get_directions():
    while True:
        # Prompt the user for the starting location
        orig = input("Starting Location: ")
        if orig in ("quit", "q"):
            break

        # Prompt the user for the destination
        dest = input("Destination: ")
        if dest in ("quit", "q"):
            break

        try:
            # Construct the URL for the MapQuest API
            url = construct_url(orig, dest)
            print("\nFetching directions...")
            # Fetch data from the API
            json_data = fetch_data(url)

            if json_data:
                # Process and display the directions
                process_data(json_data, orig, dest)
        except (RequestException, ConnectionError):
            # Handle network and connection errors
            print("An error occurred. Please check your internet connection.")
        except Exception as e:
            # Handle unexpected errors
            print("An unexpected error occurred:", str(e))

# Function to construct the API request URL
def construct_url(orig, dest):
    params = {
        "key": KEY,
        "from": orig,
        "to": dest
    }
    return MAIN_API + urllib.parse.urlencode(params)

# Function to fetch data from the MapQuest API
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Function to process and display the directions
def process_data(json_data, orig, dest):
    json_status = json_data.get("info", {}).get("statuscode")

    if json_status == 0:
        # Display directions if status code is 0 (success)
        print("\n" + "=" * 50)
        print(f"Directions from {orig} to {dest}")
        print("=" * 50)
        directions = json_data["route"]["legs"][0]["maneuvers"]
        for i, maneuver in enumerate(directions, start=1):
            # Print step-by-step directions and distances
            print(f"{i}. {maneuver['narrative']} ({'%.2f' % (maneuver['distance'] * 1.61)} km)")
        print("=" * 50)
    elif json_status == 402:
        # Handle invalid user inputs
        print("\nStatus Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
    elif json_status == 611:
        # Handle missing location entries
        print("\nStatus Code: " + str(json_status) + "; Missing an entry for one or both locations.")
    else:
        # Display a link to MapQuest's documentation for other status codes
        print("\nFor Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")

# Entry point of the script
if __name__ == "__main__":
    print("Welcome to the MapQuest Directions App!")
    get_directions()