from src import models


BASE_TEXT_STYLING = "float: left; width: 50%; box-sizing: border-box; font-family: arial;"


def make_product_card_html(product: models.Product, swatch_num: int) -> str:
    product_url = f'https://shop.lululemon.com{product.pdp_url}'
    image_url = product.swatches[swatch_num].primary_img
    product_name = product.display_name
    price_range = product.sale_price_range
    return f"""  
    <div id="product-card" style="display: inline-block; margin: 24px 12px 0px 0px; height: 20%; width: 15%;">
        <a id="image-with-link" href="{product_url}">
            <img src="{image_url}" style="width:100%">
        </a>
        
        <div id="text-row" style="display: flex; margin-top: 6px;">
            <div id="product-name-text" class="texts" style="{BASE_TEXT_STYLING} margin-left: 2%; font-weight: bold;">
              {product_name}
            </div>
            <div id="price-range" class="texts" style="{BASE_TEXT_STYLING} margin-right: 2%; text-align:right; font-weight: lighter">
              {price_range}
            </div>
        </div>
    </div>
    """


def make_product_card_htmls(products: list[models.Product]) -> str:
    prod_card_htmls = []
    for product in products:
        num_swatches = len(product.swatches)
        for idx in range(num_swatches):
            prod_card_htmls.append(make_product_card_html(product, idx))
    return '\n'.join(prod_card_htmls)


def make_products_html(products: list[models.Product]) -> str:
    products = make_product_card_htmls(products)
    return f"""
    <body>
        <div style="height: 100%; width: 100%;">
            {products}
        </div>
    <body>
    """


