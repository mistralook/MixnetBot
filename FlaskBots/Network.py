import requests

PORTS = [8000, 9000, 10000]


def get_all_servers():
    response = requests.get(url="http://127.0.0.1:5000/get-mixers")
    print("In get all servers",response.json())
    return response.json()["servers"]
    # return [f"http://127.0.0.1:{port}" for port in PORTS]


# def get_all_servers():
#     return [
#         "http://127.0.0.1:8000",
#         "http://127.0.0.1:9000"
#     ]
