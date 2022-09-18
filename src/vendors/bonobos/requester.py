import requests
from src import base_requester


class Requester(base_requester.BaseRequester):
    SESSION_ENDPOINT = 'https://bonobos.com'
    REQUEST_ENDPOINT = 'https://ac.cnstrc.com/autocomplete'
    MAX_PAGE_SIZE = 42

    def _make_request_params(self, page_num: int) -> dict:
        return {"query": self._format_search_terms(),
                "autocomplete_key": "key_Mp65OJnW8U79Olpq",
                "c": "ciojs-2.451.6",
                "num_results_Products": "4",
                "num_results_Search Suggestions": "6",
                "i": "a41460bd-c860-4a3e-8569-9588032e96b6",
                "s": "8",
                "_dt": "1663252911541"}

    def _get_request_endpoint(self) -> str:
        formatted_search_terms = self._format_search_terms()
        return f'{self.REQUEST_ENDPOINT}/{formatted_search_terms}'

    def _extract_products_from_response(
            self, response: requests.Response) -> list[dict]:
        return response.json()['sections']['Products']

    def _format_search_terms(self) -> str:
        return " ".join(self.search_terms)
