import requests
import string

from src import base_requester


class Requester(base_requester.BaseRequester):
    SESSION_ENDPOINT = 'https://shop.lululemon.com'
    REQUEST_ENDPOINT = f'{SESSION_ENDPOINT}/api/s'
    MAX_PAGE_SIZE = 20

    def _make_request_params(self, page_num: int) -> str:
        page_offset = (page_num - 1) * self.MAX_PAGE_SIZE
        return {
            "Ntt": self._format_search_terms(),
            "genderAffinity": "all",
            "page[offset]": str(page_offset),
            "page[limit]": str(self.MAX_PAGE_SIZE)
        }

    def _format_search_terms(self) -> str:
        return "+".join(self.search_terms)

    def _extract_products_from_response(
            self, response: requests.Response) -> list[dict]:
        return [response_entry for response_entry in response.json()['included']
                if response_entry.get('pdp-url')]

