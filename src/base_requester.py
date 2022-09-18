import enum
import requests
import string
import time
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
              "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 "
              "Safari/605.1.15")

MAX_PAGE_NUM = 10

# ==============================================================================
# Helpers
# ==============================================================================


def _get_cookie(endpoint: str, session: requests.Session) -> str:
    """
    :param endpoint: An endpoint for which to retrieve headers.
    :param session: The session for which to extract cookies.
    """
    response = session.get(endpoint, headers={"User-Agent": USER_AGENT})
    if not response.ok:
        print(f'ERROR: Cannot establish connection with {endpoint}')
    cookie_dict = session.cookies.get_dict()
    cookie_kv_pairs = [f'{key}={value}' for key, value in cookie_dict.items()]
    cookie_str = ';'.join(cookie_kv_pairs)
    return cookie_str


def _get_headers(endpoint: str) -> dict[str]:
    """
    :param endpoint: An endpoint for which to retrieve headers.
    """
    session = requests.Session()
    cookie = _get_cookie(endpoint, session)
    return {
        "Content-Type": "application/json",
        "Origin": endpoint,
        "Accept-Language": "en-us",
        "cookie": cookie,
        "User-Agent": USER_AGENT
    }


# ==============================================================================
# Requesters
# ==============================================================================


@dataclass(frozen=True)
class BaseRequester:
    """
    :cvar session endpoint: The endpoint to use to establish a session. Can just be
        the homepage URL.
    :cvar REQUEST_ENDPOINT: The endpoint to use for the request
    :cvar MAX_PAGE_SIZE: Empirically determined maximum results per page without
        breaking the query.
    """
    SESSION_ENDPOINT: ClassVar[str]
    REQUEST_ENDPOINT: ClassVar[str]
    MAX_PAGE_SIZE: ClassVar[str]
    PAYLOAD_TEMPLATE: ClassVar[string.Template]

    search_terms: list[str] = field(default_factory=list)

    def get_all_products(self) -> list[dict[str, str]]:
        """
        A list of dicts representing all products.
        """
        all_products = []
        page_num = 1
        while page_num <= MAX_PAGE_NUM:
            if not (products := self._get_products(page_num)):
                break
            all_products.extend(products)
            print(f'Success: {page_num=}')
            page_num += 1
            time.sleep(0.1)
        return all_products

    def _get_products(self, page_num: int) -> list[dict[str, str]]:
        """
        Return the JSON for presumably a subset of all available products.
        """
        response = self._make_request(page_num)
        if response.status_code != requests.codes.ok:
            print(f'ERROR: Can\'t get products from request endpoint '
                  f'{self.REQUEST_ENDPOINT}')
            print(f'ERROR {response.status_code}: {response.reason} {response.request.url = }')
            return None
        return self._extract_products_from_response(response)

    def _make_request(self, page_num: int):
        endpoint = self._get_request_endpoint()
        headers = _get_headers(self.SESSION_ENDPOINT)
        params = self._make_request_params(page_num)
        response = requests.get(
            endpoint,
            headers=headers,
            params=params)
        return response

    def _get_request_endpoint(self) -> str:
        return self.REQUEST_ENDPOINT

    def _make_request_params(self, page_num: int) -> dict:
        return dict()

    def _extract_products_from_response(
            self, response: requests.Response) -> list[dict]:
        raise NotImplementedError
