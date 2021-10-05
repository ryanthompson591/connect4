import requests

URL = "https://connect4.gamesolver.org/solve?pos=45"
page = requests.get(URL)

print(page.text)
