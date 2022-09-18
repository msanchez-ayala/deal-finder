from typing import Protocol

MIN_SALE_PERCENTAGE = 40


class ProductParser(Protocol):
    product: dict[str, str]

    def derive_sale_percentage(self) -> int:
        ...

    def get_product_name(self) -> str:
        ...

    def get_current_price(self) -> float:
        ...

    def get_primary_image_url(self) -> str:
        ...

    def get_product_url(self) -> str:
        ...


FONT_STYLING = 'font-family: arial;'
BASE_TEXT_STYLING = f'float: left; box-sizing: border-box; {FONT_STYLING}'


def make_product_card_html(parser: ProductParser) -> str:
    product_url = parser.get_product_url()
    image_url = parser.get_primary_image_url()
    product_name = parser.get_product_name()
    current_price = parser.get_current_price()
    sale_percentage = parser.derive_sale_percentage()
    return f"""  
    <div class="product-card" style="display: inline-block; margin: 24px 12px 0px 0px; height: 20%; width: 23%;">
        <a class="image-with-link" href="{product_url}">
            <img src="{image_url}" style="width:100%">
        </a>
        
        <div class="text-row" style="display: flex; margin-top: 6px;">
            <div class="product-name-text" style="{BASE_TEXT_STYLING} width: 70%; margin-left: 2%; font-weight: bold;">
              {product_name}
            </div>
            <div class="price-range" style="{BASE_TEXT_STYLING} width: 30%; margin-right: 2%; text-align:right; font-weight: lighter">
              ${current_price} ({sale_percentage}%)
            </div>
        </div>
    </div>
    """


def make_product_card_htmls(products: list[dict],
                            parser_class: type(ProductParser)) -> str:
    prod_card_htmls = []
    for product in products:
        parser = parser_class(product)
        if parser.derive_sale_percentage() < MIN_SALE_PERCENTAGE:
            continue
        prod_card_htmls.append(make_product_card_html(parser))
    return '\n'.join(prod_card_htmls)


def make_vendor_html(vendor_name: str,
                     products: list[dict],
                     parser_class: type(ProductParser)) -> str:
    products = make_product_card_htmls(products, parser_class)
    return f"""
    <div style="width: 100%; display: block;">
        <div style="{FONT_STYLING} width: 100%; font-size: 4ex; margin: 0px">{vendor_name}</div>
        <div style="margin-bottom: 24px;">{products}</div>
    </div>
    """


def make_header_html(search_terms: list[str]) -> str:
    return f"""
    <div>
      <h1 style="{FONT_STYLING}">Vendor Search</h1>
      <h3 style="{FONT_STYLING}">Search terms: {" ".join(search_terms)}</h3>
    </div>
    """


def make_aggregate_html(vendor_htmls: list[str],
                        search_terms: list[str]) -> str:
    header = make_header_html(search_terms)
    vendors = '\n'.join(vendor_htmls)
    return f"""
    <body>
        {header}
        {vendors}
    <body>
    """
