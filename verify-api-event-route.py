import requests
path = "/api/events"
base_url = "http://localhost:8002"
endpoint = f"{base_url}{path}"
reponse = requests.get(endpoint)
print(reponse, type(reponse), reponse.get("items"))