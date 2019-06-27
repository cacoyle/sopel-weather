
class Here:

    def __init__(self, here_url, here_app_id, here_app_code):

        self.here_url = here_url
        self.here_app_id = here_app_id
        self.here_app_code = here_app_code

    def _location(self, **kwargs):

        import requests

        params = kwargs.copy()
        params.update({"app_id": self.here_app_id})
        params.update({"app_code": self.here_app_code})

        location = requests.get(
            self.here_url,
            params
        )

        results = []

        for v in location.json()["Response"]["View"]:
            for result in v["Result"]:
                results.append(result)

        return(results)

    def location(self, search_string):
        from . import utils

        results = []

        country = utils.postal_code(search_string)

        if country:
            results = self._location(
                postalcode=search_string,
                country=country
            )
        else:
            results = self._location(
                searchtext=search_string
            )

        if len(results) == 0:
            raise Exception(f"No results found for {search_string}")
        elif len(results) > 1:
            matches = ' '.join([x["Location"]["Address"]["Label"] for x in results])
            raise Exception(f"Multiple results found for {search_string}: {matches}")

        return(results[0])
