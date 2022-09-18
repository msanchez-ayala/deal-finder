import requests
import string

from src import base_requester

MENS_SALE_ALL_QUERY_ID = 'N-1z0xcmkZ8t6'


class Requester(base_requester.BaseRequester):
    SESSION_ENDPOINT = 'https://shop.lululemon.com'
    REQUEST_ENDPOINT = f'{SESSION_ENDPOINT}/api/s'
    MAX_PAGE_SIZE = 20

    def _make_request_params(self, page_num: int) -> str:
        return {
            "Ntt": self._format_search_terms(),
            "genderAffinity": "all",
            "page\\[offset\\]": f"{page_num}"}

    def _format_search_terms(self) -> str:
        return "+".join(self.search_terms)

    def _extract_products_from_response(
            self, response: requests.Response) -> list[dict]:
        return [response_entry for response_entry in response.json()['included']
                if response_entry.get('pdp-url')]

