import requests

url = "https://api.exchangerate.host/symbols"

response = requests.get(url)
print(response.url)  # This will show the real URL it's hitting
print(response.json())

