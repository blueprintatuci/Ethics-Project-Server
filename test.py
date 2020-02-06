import requests

URL = "https://ethic-blueprint.herokuapp.com/"

r = requests.get(url = URL) 
print(r.status_code)