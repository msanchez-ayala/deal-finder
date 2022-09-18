from dataclasses import dataclass

from src.vendors.lululemon import requester


@dataclass
class ProductParser:
    product: dict[str, str]

    def derive_sale_percentage(self) -> int:
        cur_price = self.get_current_price()
        fraction = cur_price / self._get_list_price()
        sale_frac = 1 - fraction
        return int(100 * sale_frac)

    def get_product_name(self) -> str:
        return self.product['display-name']

    def get_current_price(self) -> float:
        if self._is_on_sale():
            return self._get_sale_price()
        else:
            return self._get_list_price()

    def get_primary_image_url(self) -> str:
        return self.product['sku-sku-images'][0]

    def get_product_url(self) -> str:
        return requester.Requester.SESSION_ENDPOINT + self.product['pdp-url']

    # ==========================================================================
    # Internal
    # ==========================================================================

    # NOTE list-price and sale-price are lists, but we'll just assume the lowest
    # value for simplicity

    def _get_sale_price(self) -> float:
        return float(self.product['product-sale-price'][0])

    def _get_list_price(self) -> float:
        return float(self.product['list-price'][0])

    def _is_on_sale(self) -> bool:
        return self.product['product-on-sale'] == "1"