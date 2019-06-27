class DarkSky:

    def __init__(self, darksky_url, darksky_key):
        self.darksky_url = darksky_url
        self.darksky_key = darksky_key

    def get(self, latitude, longitude):
        import requests

        darksky_data = requests.get(
            f"{self.darksky_url}/{self.darksky_key}/{latitude},{longitude}"
        )

        return(darksky_data.json())
