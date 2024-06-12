import request

class Recuest():
    def __init__(self):
        r = request

    def get_trade_link(self, url):
        self.r.get(url)
        if self.r.status_code == 200:
            print(self.r.json())