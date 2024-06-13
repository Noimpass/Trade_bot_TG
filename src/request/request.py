import requests

class Request():
    def __init__(self):
        self.r = requests

    def get_profile_id(self, url):
        response = self.r.get(url)
        if response.status_code == 200:
            steam_id = 76561197960265728 + int(url.split("=")[1].split("&")[0])
            return steam_id
        else:
            return None
        
    def get_profile_name(self, steam_id):
        steam_link = f"https://steamcommunity.com/profiles/{steam_id}"
        response = self.r.get(steam_link)
        if response.status_code == 200:
            steam_name = response.text.split('<title>Steam Community :: ')[1].split('</title>')[0]
            print(steam_name)
            return steam_link, steam_name
        else:
            return None