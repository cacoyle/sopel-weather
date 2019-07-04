from sopel_modules.weather import wz
import pytest
import os

from httmock import urlmatch, all_requests, HTTMock

@all_requests
def http_mock(url, request):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "json", (url.query if url.query else url.path[1:]))) as f:
        return {
            "status_code": 200,
            "content": f.read()
        }

@pytest.fixture(scope="module")
def make_wz():
    h = wz.WZ("http://localhost", "appid", "appcode", "http://localhost", "id")
    yield(h)

def test_wz(make_wz):
    with HTTMock(http_mock):
        make_wz.get("90210")
        make_wz.get("K4R1E5")
        make_wz.get("Los Angeles, CA")

        with pytest.raises(Exception):
            make_wz.get("K4R1E4")
