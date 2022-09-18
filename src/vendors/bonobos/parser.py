import math
from dataclasses import dataclass

from src.vendors.bonobos import requester


@dataclass
class ProductParser:
    product: dict[str, str]

    def derive_sale_percentage(self) -> int:
        first_swatch = self.get_swatches()[0]
        fraction = self.get_current_price() / first_swatch['full_price']
        sale_frac = 1 - fraction
        return int(100 * sale_frac)

    def get_product_name(self) -> str:
        return self.product['value']

    def get_current_price(self) -> float:
        """
        Search through all swatches and return lowest price.
        """
        lowest_price = math.inf
        for swatch in self.get_swatches():
            lowest_price = min((lowest_price, swatch['current_price']))
        return lowest_price

    def get_primary_image_url(self) -> str:
        first_swatch = self.get_swatches()[0]
        return first_swatch['primary_image_url']

    def get_product_url(self) -> str:
        products_endpoint = f'{requester.Requester.SESSION_ENDPOINT}/products/'
        return products_endpoint + self.product['data']['url']

    def get_swatches(self) -> list[dict]:
        return self.product['data']['swatches']